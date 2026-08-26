#!/usr/bin/env python3
"""Proofread prose against the unspeak rules.

Reports spans and names the rule each one breaks. It does not score the text
and it does not guess who wrote it: a weighted sum of pattern hits does not
separate machine prose from human prose, which the one published measurement of
that idea found at ROC-AUC 0.501.

Adding a word to references/vocabulary.md changes what this flags. No code edit.

    proofread.py draft.md
    proofread.py draft.md --json
    proofread.py before.md after.md      # what the rewrite did
    proofread.py --self                  # run on this skill's own files
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
VOCAB = SKILL_DIR / "references" / "vocabulary.md"
STYLE = SKILL_DIR / "references" / "style.md"
REFERENCE_DIR = SKILL_DIR / "references" / "reference-writing"

# Divergence against the author's own writing needs enough tokens for the
# distributions to be stable. Below this it is sampling noise, so the check stays
# dark and says so rather than reporting a figure nobody should trust.
DIVERGENCE_MIN_WORDS = 2000

# An abstract subject is what makes a physical verb non-literal. "The box sits"
# is fine; "the decision sits" is not. Without this gate the vocabulary fires on
# ordinary English.
ABSTRACT_SUBJECTS = {
    "argument", "assumption", "claim", "decision", "change", "approach", "rule",
    "design", "system", "problem", "idea", "point", "question", "answer",
    "issue", "concern", "risk", "constraint", "pattern", "principle", "value",
    "cost", "benefit", "tradeoff", "result", "finding", "insight", "concept",
    "theory", "model", "framework", "structure", "logic", "reasoning", "story",
    "narrative", "thesis", "premise", "conclusion", "distinction", "difference",
    "relationship", "tension", "culture", "market", "data", "evidence",
    "complexity", "abstraction", "interface", "contract", "invariant", "spec",
    "plan", "goal", "intent", "meaning", "sense", "word", "sentence", "code",
    # Artifact nouns. "Every repo carries its own contract" slipped through
    # because repo was missing: an artifact is as unable to carry as an idea is.
    "repo", "repository", "machine", "box", "instance", "tool", "skill",
    "file", "feature", "test", "loop", "pipeline", "workflow", "cache",
    "configuration", "config", "setting", "settings",
}

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")
WORD = re.compile(r"[A-Za-z']+")


@dataclass
class Finding:
    line: int
    rule: str
    text: str
    note: str = ""


# ── exemptions ────────────────────────────────────────────────────────────
# A file that lists banned words must not fail on its own list. Blanking
# preserves line and column offsets so reported positions stay correct.

_FENCED = re.compile(r"^(?:```|~~~)[^\n]*\n[\s\S]*?^(?:```|~~~)[ \t]*$", re.M)
_TABLE = re.compile(r"(?:^[ \t]*\|[^\n]*\|[ \t]*(?:\n[ \t]*\|[^\n]*\|[ \t]*)+)", re.M)
_QUOTE_BLOCK = re.compile(r"(?:^[ \t]*>[^\n]*(?:\n[ \t]*>[^\n]*)*)", re.M)
_INLINE_CODE = re.compile(r"`[^`\n]+`")
_QUOTED = re.compile(r"\"[^\"\n]{1,300}\"|“[^”\n]{1,300}”")
_FRONTMATTER = re.compile(r"\A---\n[\s\S]*?\n---\n")


def mask(text: str) -> str:
    """Blank spans the rules exempt, keeping every offset intact."""
    def blank(m: re.Match) -> str:
        return re.sub(r"[^\n]", " ", m.group(0))

    for pattern in (_FRONTMATTER, _FENCED, _TABLE, _QUOTE_BLOCK, _INLINE_CODE, _QUOTED):
        text = pattern.sub(blank, text)
    return text


# ── vocabulary ────────────────────────────────────────────────────────────

HEADER_CELLS = {"verb", "idiom", "word", "replace", "---"}


def load_vocabulary(path: Path = VOCAB) -> dict[str, list[str]]:
    """Parse references/vocabulary.md into word lists, keyed by section.

    Only table rows and fenced ```words blocks are read. Prose is never parsed,
    so notes and carve-outs can be written freely without becoming flag terms.
    An earlier version scraped prose too, which put "checking" and "column" on
    the flag list and made every "is" in the skill fire as filler.
    """
    if not path.exists():
        sys.exit(f"vocabulary not found: {path}")

    sections: dict[str, list[str]] = {}
    current: str | None = None
    in_block = False

    for line in path.read_text().splitlines():
        heading = re.match(r"^##\s+(.*)", line)
        if heading:
            current = heading.group(1).strip().lower()
            sections.setdefault(current, [])
            in_block = False
            continue
        if current is None:
            continue

        if line.startswith("```"):
            in_block = line.strip() == "```words"
            continue

        if in_block:
            for item in line.split(","):
                item = item.strip().rstrip(".").lower()
                if item and re.fullmatch(r"[a-z][a-z0-9' -]{1,38}", item):
                    sections[current].append(item)
            continue

        row = re.match(r"^\|\s*([a-z][a-z' -]+?)\s*\|", line, re.I)
        if row:
            cell = row.group(1).strip().lower()
            if cell not in HEADER_CELLS:
                sections[current].append(cell)

    return sections


def section(vocab: dict[str, list[str]], *keys: str) -> list[str]:
    """Look up a block by heading. A leading ^ demands an exact match, which the
    main "words" block needs because its name is a substring of every other."""
    for key in keys:
        exact = key.startswith("^")
        needle = key[1:] if exact else key
        for name, words in vocab.items():
            if name == needle if exact else needle in name:
                return words
    return []


# ── checks on one document ────────────────────────────────────────────────

def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _inflections(stem: str) -> str:
    """All forms of a verb, as one alternation. The naive stem+(s|es|ed|ing)
    missed every y-verb: carry(?:s|es|ed|ing) never matches "carries", which is
    exactly how 'carries its own contract' got through the bake-off."""
    forms = [stem, stem + "s", stem + "es"]
    if stem.endswith("y"):
        forms += [stem[:-1] + "ies", stem[:-1] + "ied", stem + "ing"]
    elif stem.endswith("e"):
        forms += [stem + "d", stem[:-1] + "ing"]
    else:
        forms += [stem + "ed", stem + "ing"]
    # doubled-consonant participles for short stems: sit -> sitting
    if re.search(r"[^aeiou][aeiou][^aeiouwxy]$", stem):
        forms += [stem + stem[-1] + "ing", stem + stem[-1] + "ed"]
    return "|".join(re.escape(f) for f in sorted(set(forms), key=len, reverse=True))


IRREGULAR = {"keep": ["kept"], "hold": ["held"], "sit": ["sat"], "stick": ["stuck"],
             "bear": ["bore", "borne"], "ride": ["rode", "ridden"], "hang": ["hung"],
             "come and go": ["comes and goes", "came and went"]}

# Two false positives the live hook produced on its first day.
# "bake-off" is a compound noun, not the verb bake; "live" and "lives" are
# usually the adjective ("a live session") or the noun ("our lives"), told
# apart by what directly precedes them.
COMPOUND_SKIP = re.compile(r"[-\w]-$")
ADJ_BEFORE = re.compile(r"\b(?:a|an|the|this|that|is|are|was|were|go|goes|went|gone|"
                        r"stay|stays|stayed|still|now|our|their|my|your|its)\s+$", re.I)
ADJ_ONLY = {"live", "lives"}


def check_physical_verbs(text: str, verbs: list[str]) -> list[Finding]:
    """Flag a physical verb whose subject is abstract."""
    out = []
    for verb in verbs:
        stem = verb.split()[0]
        alts = _inflections(stem)
        extra = "|".join(re.escape(w) for w in IRREGULAR.get(stem, []))
        if extra:
            alts = alts + "|" + extra
        for m in re.finditer(rf"\b(?:{alts})\b", text, re.I):
            before = text[max(0, m.start() - 24):m.start()]
            if COMPOUND_SKIP.search(before) or text[m.end():m.end() + 1] == "-":
                continue
            if m.group(0).lower() in ADJ_ONLY and ADJ_BEFORE.search(before):
                continue
            window = text[max(0, m.start() - 90):m.start()]
            window = window.rsplit(".", 1)[-1]
            subjects = {w.lower() for w in WORD.findall(window)}
            hit = subjects & ABSTRACT_SUBJECTS
            if hit:
                out.append(Finding(
                    line_of(text, m.start()),
                    "non-literal predicate",
                    m.group(0),
                    f"abstract subject: {', '.join(sorted(hit))}",
                ))
    return out


def clause_around(text: str, start: int, end: int) -> str:
    """The clause the match sits in, with the match marked, so feedback shows
    the use and which word fired."""
    left = max(text.rfind(ch, 0, start) for ch in ".!?\n")
    right_candidates = [text.find(ch, end) for ch in ".!?\n"]
    right = min((r for r in right_candidates if r != -1), default=len(text))
    marked = text[left + 1:start] + "<<" + text[start:end] + ">>" + text[end:right]
    return " ".join(marked.split())[:100]


def check_words(text: str, words: list[str], rule: str,
                carve_out: list[str] | None = None) -> list[Finding]:
    out = []
    for word in words:
        for m in re.finditer(rf"\b{re.escape(word)}\b", text, re.I):
            if carve_out and word == "load-bearing":
                following = text[m.end():m.end() + 40].strip().lower()
                if any(following.startswith(n) for n in carve_out):
                    continue
            out.append(Finding(line_of(text, m.start()), rule, m.group(0),
                               clause_around(text, m.start(), m.end())))
    return out


# Only a subject making a claim counts. "Nobody has complained" reports a
# measurement nobody took; "everything else on this page" is a determiner. The
# first version flagged both, which is the kind of check that trains a writer to
# ignore the tool.
ABSENCE = re.compile(
    r"(?:^|(?<=[.!?]\s)|(?<=[,;]\s))\s*(nobody|no one|nothing|none)\s+"
    r"(?:has|have|had|is|are|was|were|will|would|ever|\w+(?:s|ed))\b",
    re.I | re.M,
)


def check_absence(text: str) -> list[Finding]:
    return [
        Finding(line_of(text, m.start()), "non-event", m.group(0).strip(),
                "an absence is information only when someone was checking")
        for m in re.finditer(ABSENCE, text)
    ]


EXTRA = [
    # Anchored to the start of a sentence. Mid-sentence "what X is" is usually an
    # embedded question ("I know what this is"), not a pseudo-cleft, and flagging
    # those trained the tool to be ignored.
    (re.compile(r"(?:^|(?<=[.!?]\s)|(?<=[.!?]\n))\s*what\s+(?:\w+\s+){1,3}is\s+\w", re.I | re.M),
     "what X is Y", "say it directly"),
    (re.compile(r"\b(?:one|a single)\s+\w+\s+worth\s+(?:your|the|a)\b", re.I),
     "one X worth Y", "say what needs doing"),
    (re.compile(r"^[ \t]*(?:[-*]\s+)?\*\*[^*\n]{3,60}\*\*[.:]\s+[^\n]*?[.!?]\s+[A-Z][^\n]*?[.!?]", re.M),
     "bold label then a paragraph", "use a colon and one sentence"),
    (re.compile(r"\b(?:it'?s|is|was|are|were)\s+not\s+(?:just\s+|only\s+|merely\s+)?[^.\n]{2,45}[,.]\s*(?:it'?s|it is|they'?re|but)\b", re.I),
     "binary contrast", "state the second half directly"),
    (re.compile(r"\b(?:isn'?t|aren'?t|wasn'?t|weren'?t)\s+(?:just\s+|only\s+|about\s+)?[^.\n]{2,45}[,.]\s*(?:it'?s|it is|they'?re|but)\b", re.I),
     "binary contrast", "state the second half directly"),
    (re.compile(r"\bthe\s+(?:question|problem|answer|issue)\s+(?:is|isn'?t)\s+not\b", re.I),
     "binary contrast", "state it directly"),
    (re.compile(r",\s+(?:highlighting|underscoring|emphasizing|showcasing|reflecting|symbolizing|demonstrating)\s+\w+", re.I),
     "superficial -ing clause", "delete, or replace with the fact"),
    (re.compile(r"\b(?:it\s+is|it'?s|this\s+is)\s+(?:about\s+)?more\s+than\s+\w+[^.\n]{0,40}[.;]\s*(?:it|this)\b", re.I),
     "setup before the point", "cut the comparison and state the thing"),
    (re.compile(r"\bmeans\s+more\s+than\b", re.I),
     "setup before the point", "just say what it means"),
    (re.compile(r",?\s+so\s+there\s+(?:is|are)\s+no\b[^.\n]{3,60}", re.I),
     "consequence tail", "the reader can infer it: cut"),
    (re.compile(r"\bstill\s+(?:early|here)\b|\bwe'?re\s+early\b|\bit'?s\s+early\b", re.I),
     "vocabulary", "an LLM flag phrase"),
    (re.compile(r",\s+not\s+(?:because\s+)?(?:my|your|our|the|a|an|just)?\s*[a-z][^.;\n]{2,80}[.;]", re.I),
     "contrast tail", "drop the foil and keep the claim"),
    (re.compile(r"\bin\s+a\s+way\s+(?:i|we|you)\s+(?:didn'?t|never|couldn'?t|hadn'?t)\b", re.I),
     "anticipation frame", "say what happened without the surprise wrapper"),
    (re.compile(r",?\s*which\s+(?:is|was)\s+a\s+\w+\s+(?:combination|feeling|thing|experience|place)\b", re.I),
     "self-appraisal", "the reader decides what it was"),
    (re.compile(r",?\s*so\s+(?:nobody|no one)\s+(?:has|have|needs?)\s+to\b[^.\n]{0,50}", re.I),
     "consequence tail", "the sentence already implies it: cut"),
    (re.compile(r"\bbefore\s+anyone\s+(?:says|calls|claims)\b", re.I),
     "grand speak", "state the condition plainly"),
    (re.compile(r"[\u2192\u2190\u21d2\u21d0\u27a1]"), "unicode arrow", ""),
    (re.compile(r"^#{1,6}[^\n]*[\U0001F300-\U0001FAFF\u2600-\u27BF]", re.M), "emoji in heading", ""),
    (re.compile(r"^\s*[-*]\s+\*\*([^*\n]{2,30})\*\*:\s*\1", re.I | re.M),
     "inline-header list", "the label restates the line"),
]


def check_extra(text: str) -> list[Finding]:
    out = []
    for pattern, rule, note in EXTRA:
        for m in re.finditer(pattern, text):
            out.append(Finding(line_of(text, m.start()), rule, m.group(0)[:60], note))
    return out


def check_heading_restated(text: str) -> list[Finding]:
    """A heading followed by one short line that repeats it."""
    out = []
    for m in re.finditer(r"^#{1,6}\s+(.+)\n+([^\n#>|*-][^\n]{0,90})$", text, re.M):
        head = set(w.lower() for w in WORD.findall(m.group(1)) if len(w) > 3)
        body = set(w.lower() for w in WORD.findall(m.group(2)) if len(w) > 3)
        overlap = len(head & body)
        length = len(WORD.findall(m.group(2)))
        # One shared word is a topic sentence doing its job. Two, in a line
        # short enough to carry nothing else, is the heading said twice.
        if head and length <= 10 and (overlap >= 2 or (overlap and length <= 5)):
            out.append(Finding(line_of(text, m.start()), "heading restated", m.group(2)[:60]))
    return out


BURIED = [
    (re.compile(r"\bwhat\s+\w+(?:\s+\w+)?\s+(?:does|did|is doing)\s+is\b", re.I), "what X does is"),
    (re.compile(r"\bit\s+is\s+\w+(?:\s+\w+){0,3}\s+that\b", re.I), "it is N that"),
    (re.compile(r"\bthere\s+(?:is|are)\s+\w+(?:\s+\w+){0,3}\s+that\b", re.I), "there is N that"),
    (re.compile(r"\bis\s+the\s+\w+(?:\s+\w+){0,2}\s+(?:that|which)\s+\w+", re.I), "is the N that V"),
    (re.compile(r"\b(?:makes?|made)\s+a\s+decision\b", re.I), "nominalization"),
    (re.compile(r"\bperforms?\s+an?\s+analysis\b", re.I), "nominalization"),
    (re.compile(r"\bprovides?\s+support\s+for\b", re.I), "nominalization"),
    (re.compile(r"\bhas\s+the\s+ability\s+to\b", re.I), "nominalization"),
]


def check_buried_verbs(text: str) -> list[Finding]:
    out = []
    for pattern, label in BURIED:
        for m in re.finditer(pattern, text):
            out.append(Finding(line_of(text, m.start()), "buried verb", m.group(0), label))
    return out


def check_headings(text: str) -> list[Finding]:
    out = []
    for m in re.finditer(r"^#{1,6}\s+(.*)$", text, re.M):
        head = m.group(1).strip()
        if re.match(r"^(The|A|An)\s+\w+\s+(that|which)\s+\w+", head, re.I):
            out.append(Finding(line_of(text, m.start()), "relative-clause title", head))
        words = re.findall(r"\b[A-Za-z][a-z]+\b", head)
        if len(words) >= 3 and sum(w[0].isupper() for w in words) > len(words) * 0.7:
            out.append(Finding(line_of(text, m.start()), "title case heading", head))
    return out


def sentences(text: str) -> list[str]:
    """Prose only. Headings, bullets, quotes, tables and numbered items are
    reference registers where a clipped line is the correct form, so counting
    them as sentences turns every spec and changelog into a stub run."""
    prose = re.sub(r"^#{1,6}.*$", "", text, flags=re.M)
    prose = re.sub(r"^\s*(?:[-*|>]|\d+\.)\s.*$", "", prose, flags=re.M)
    return [s.strip() for s in SENTENCE_SPLIT.split(prose) if len(WORD.findall(s)) > 1]


def check_stub_runs(text: str, limit: int = 6, run: int = 3) -> list[Finding]:
    out, streak = [], []
    for s in sentences(text):
        if len(WORD.findall(s)) <= limit:
            streak.append(s)
            continue
        if len(streak) >= run:
            out.append(Finding(line_of(text, text.find(streak[0])), "chopped sentences",
                               " ".join(streak)[:120], f"{len(streak)} in a row"))
        streak = []
    if len(streak) >= run:
        out.append(Finding(line_of(text, text.find(streak[0])), "chopped sentences",
                           " ".join(streak)[:120], f"{len(streak)} in a row"))
    return out


def check_openers(text: str) -> list[Finding]:
    out, streak = [], []
    for s in sentences(text):
        first = (WORD.findall(s) or [""])[0].lower()
        if streak and first == streak[-1][0]:
            streak.append((first, s))
        else:
            if len(streak) >= 3:
                out.append(Finding(line_of(text, text.find(streak[0][1])), "repeated opener",
                                   streak[0][0], f"{len(streak)} sentences in a row"))
            streak = [(first, s)]
    if len(streak) >= 3:
        out.append(Finding(line_of(text, text.find(streak[0][1])), "repeated opener",
                           streak[0][0], f"{len(streak)} sentences in a row"))
    return out


def check_punctuation(text: str) -> list[Finding]:
    out = []
    for m in re.finditer(r"[—–]", text):
        out.append(Finding(line_of(text, m.start()), "dash", m.group(0), "no em or en dashes"))
    for m in re.finditer(r"[“”‘’]", text):
        out.append(Finding(line_of(text, m.start()), "curly quote", m.group(0)))
    prose = re.sub(r"^\s*(?:[-*|>#]|\d+\.)\s.*$", "", text, flags=re.M)
    words = len(WORD.findall(prose))
    semis = prose.count(";")
    if words and semis * 1000 / words > _semicolon_ceiling():
        out.append(Finding(1, "semicolon rate", f"{semis} in {words} words",
                           f"{semis * 1000 / words:.1f} per 1000, author ceiling {_semicolon_ceiling():.0f}"))
    return out


_SEMI_CEILING = None


def _semicolon_ceiling() -> float:
    """Derived from the reference corpus, like every other threshold: the p90
    of the author's own per-chunk semicolon rate. The first version hardcoded
    4 per 1000, and the author writes at 13."""
    global _SEMI_CEILING
    if _SEMI_CEILING is None:
        chunks = reference_chunks(None)
        if len(chunks) >= 9:
            rates = [c.count(";") * 1000 / max(len(WORD.findall(c)), 1) for c in chunks]
            _SEMI_CEILING = max(_percentile(rates, 0.9), 4.0)
        else:
            _SEMI_CEILING = 4.0
    return _SEMI_CEILING


# ── stylometry, absolute ──────────────────────────────────────────────────

def stylometry(text: str) -> dict[str, float]:
    sents = sentences(text)
    lengths = [len(WORD.findall(s)) for s in sents]
    paras = [p for p in re.split(r"\n\s*\n", text) if len(WORD.findall(p)) > 15]
    para_lengths = [len(sentences(p)) for p in paras]
    words = WORD.findall(text)
    return {
        "sentences": len(sents),
        "sentence_mean": round(statistics.mean(lengths), 1) if lengths else 0.0,
        "sentence_spread": round(statistics.pstdev(lengths), 1) if len(lengths) > 1 else 0.0,
        "paragraph_spread": round(statistics.pstdev(para_lengths), 1) if len(para_lengths) > 1 else 0.0,
        "words": len(words),
        "mean_word_length": round(statistics.mean([len(w) for w in words]), 1) if words else 0.0,
    }


def stylometry_findings(stats: dict[str, float]) -> list[Finding]:
    """Thresholds here are provisional. They come from judgment plus one 118-word
    reference, not from measurement, and they get replaced by bands once
    the reference corpus passes DIVERGENCE_MIN_WORDS.

    Rhythm uniformity is gated at document length. On 400 paragraphs of 2026
    assistant prose it never fired at paragraph size, so the paragraph-level
    version was measuring nothing."""
    out = []
    if stats["sentences"] >= 20 and stats["sentence_spread"] < 5.0:
        out.append(Finding(1, "uniform rhythm",
                           f"spread {stats['sentence_spread']} over {stats['sentences']} sentences",
                           "provisional threshold 5.0"))
    return out


def verbatim_of(text: str) -> str:
    """Only text between the verbatim markers counts as the author's writing.
    Anything outside was written by an agent and must never enter the reference."""
    m = re.search(r"^<!-- verbatim -->\s*$(.*?)^<!-- /verbatim -->\s*$", text, re.S | re.M)
    return m.group(1) if m else ""


def corpus_status() -> tuple[int, bool]:
    total = 0
    if REFERENCE_DIR.exists():
        for path in REFERENCE_DIR.glob("*.md"):
            total += len(WORD.findall(mask(verbatim_of(path.read_text()))))
    return total, total >= DIVERGENCE_MIN_WORDS




# ── voice axis ────────────────────────────────────────────────────────────
# Proximity to the author, measured the way the VOICE.md harness did it:
# every threshold is derived from the reference corpus itself, never set by
# hand. The corpus is cut into 220-word chunks; each metric's band is the
# p10-p90 range of the chunks, so "in band" means "within the author's own
# variation". The distance instrument is Burrows's Delta over the most
# frequent words, which won the harness bake-off, with one addition: the
# per-word z-scores are reported, so the number names the words causing it.

CHUNK_WORDS = 220
CHUNK_MIN = 140
MFW_N = 150
VOICE_MIN_DRAFT = 150


def _register_of(text: str) -> str:
    m = re.search(r"^register:\s*(\w+)", text, re.M)
    return m.group(1) if m else "unknown"


def reference_chunks(register: str | None = None) -> list[str]:
    """Raw ~220-word slices with punctuation intact. An earlier version chunked
    bare word lists, which stripped every comma and sentence break and collapsed
    all the metric bands to zero-width."""
    chunks = []
    if not REFERENCE_DIR.exists():
        return chunks
    for path in sorted(REFERENCE_DIR.glob("*.md")):
        raw = path.read_text()
        if register and _register_of(raw) != register:
            continue
        tokens = verbatim_of(raw).split()
        for i in range(0, len(tokens), CHUNK_WORDS):
            c = tokens[i:i + CHUNK_WORDS]
            if len(c) >= CHUNK_MIN:
                chunks.append(" ".join(c))
    return chunks


# Punctuation marks join the Delta feature set as pseudo-words. Authorship work
# has long used them; here they carry the em-dash and comma habits that the
# word list alone cannot see.
PUNCT_FEATURES = [",", ";", ":", "(", "?", "!", "\u2014", "."]


def _rates(text: str, mfw: list[str]) -> list[float]:
    words = WORD.findall(text.lower())
    n = max(len(words), 1)
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    vec = [counts.get(w, 0) * 1000 / n for w in mfw]
    vec += [text.count(ch) * 1000 / n for ch in PUNCT_FEATURES]
    return vec


def _percentile(vals: list[float], q: float) -> float:
    v = sorted(vals)
    k = (len(v) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


class VoiceProfile:
    """Burrows's Delta profile plus per-metric bands, all from the corpus."""

    def __init__(self, chunks: list[str]):
        self.n_chunks = len(chunks)
        counts = {}
        for c in chunks:
            for w in WORD.findall(c.lower()):
                counts[w] = counts.get(w, 0) + 1
        self.mfw = [w for w, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:MFW_N]]
        self.features = self.mfw + PUNCT_FEATURES
        vecs = [_rates(c, self.mfw) for c in chunks]
        self.mu = [statistics.mean(col) for col in zip(*vecs)]
        # Sigma floor: one occurrence in a chunk is 1000/CHUNK_WORDS per-1k,
        # so half an occurrence is the smallest difference a chunk can express.
        # A feature the author never uses would otherwise have sigma ~0 and a
        # single stray mark would blow the whole Delta up.
        floor = 500 / CHUNK_WORDS
        self.sigma = [max(statistics.pstdev(col), floor) for col in zip(*vecs)]
        self.delta_band = _percentile([self._delta_of(v) for v in vecs], 0.9)
        self.metric_bands = {}
        per_chunk = [chunk_metrics(t) for t in chunks]
        for key in per_chunk[0]:
            vals = [m[key] for m in per_chunk]
            self.metric_bands[key] = (_percentile(vals, 0.1), _percentile(vals, 0.9))

    def _delta_of(self, vec: list[float]) -> float:
        return statistics.mean(abs((vec[i] - self.mu[i]) / self.sigma[i])
                               for i in range(len(vec)))

    # Function words: the closed classes plus punctuation. Delta itself runs
    # over every feature, but the attribution shows only these, because a
    # content word high in the z-list is the draft's topic, not its author,
    # and telling an agent to use "agents" less is empty feedback.
    FUNCTION = set("""the a an and or but if then so of to in on at by for with from as is are
        was were be been being it its this that these those i you we they he she her his
        not no do does did done have has had will would can could should may might must
        what which who when where how there here all any some more most much many one two
        also just only even still than into over under about after before between out up
        down off again once because while against through during within without me my your
        our their them him us""".split())

    def score(self, text: str):
        vec = _rates(text, self.mfw)
        zs = [(vec[i] - self.mu[i]) / self.sigma[i] for i in range(len(vec))]
        delta = statistics.mean(abs(z) for z in zs)
        names = self.mfw + ["punct " + repr(ch) for ch in PUNCT_FEATURES]
        attributable = [(n, z) for n, z in zip(names, zs)
                        if n in self.FUNCTION or n.startswith("punct ")]
        devs = sorted(attributable, key=lambda t: -abs(t[1]))
        over = [(w, z) for w, z in devs if z > 1.5][:6]
        under = [(w, z) for w, z in devs if z < -1.5][:6]
        return delta, over, under


def chunk_metrics(text: str) -> dict[str, float]:
    words = WORD.findall(text)
    n = max(len(words), 1)
    sents = sentences(text) or [text]
    lens = [len(WORD.findall(s)) for s in sents]
    openers = [WORD.findall(s)[0].lower() for s in sents if WORD.findall(s)]
    top = max((openers.count(o) for o in set(openers)), default=0)
    return {
        "sentence mean": statistics.mean(lens) if lens else 0.0,
        "sentence spread": statistics.pstdev(lens) if len(lens) > 1 else 0.0,
        "commas /1k": text.count(",") * 1000 / n,
        "semicolons /1k": text.count(";") * 1000 / n,
        "colons /1k": text.count(":") * 1000 / n,
        "parentheses /1k": text.count("(") * 1000 / n,
        "questions /1k": text.count("?") * 1000 / n,
        "top opener share": top / max(len(openers), 1),
    }


# What the agent should do about an out-of-band metric, phrased as an action.
METRIC_ADVICE = {
    "sentence mean": ("split sentences", "join short sentences"),
    "sentence spread": ("even the rhythm out", "vary sentence length more"),
    "commas /1k": ("cut commas, split clauses", "the author strings clauses with commas"),
    "semicolons /1k": ("cut semicolons", "the author uses semicolons more than this"),
    "colons /1k": ("cut colons", "the author uses colons more than this"),
    "parentheses /1k": ("cut parentheticals", "the author uses parentheses; asides can go in them"),
    "questions /1k": ("cut rhetorical questions", "the author asks questions more than this"),
    "top opener share": ("vary sentence openers", ""),
}


def _registers_available() -> list[str]:
    regs = []
    if REFERENCE_DIR.exists():
        for path in sorted(REFERENCE_DIR.glob("*.md")):
            r = _register_of(path.read_text())
            if r not in regs and r != "unknown":
                regs.append(r)
    return regs


def voice_report(raw: str, register: str | None = None):
    """Returns (lines, ok). A pooled multi-register corpus inflates every sigma
    and loosens the Delta band, so the draft is compared per register and judged
    against the closest one. The verdict covers Delta and the metric bands both:
    a draft can match the author's vocabulary and still not sound like them."""
    regs = [register] if register else (_registers_available() or [None])
    profiles = []
    for r in regs:
        chunks = reference_chunks(r)
        words = sum(len(c.split()) for c in chunks)
        # The gate is chunk count, not raw words: sigma and the p10-p90 bands
        # come from the chunks, and nine 220-word chunks is where they stop
        # being noise. A word floor on top of that just re-counts the same thing.
        if len(chunks) >= 9:
            profiles.append((r, VoiceProfile(chunks), words))
    if not profiles:
        total = sum(len(c.split()) for c in reference_chunks(None))
        return [f"voice axis dark: no register has {DIVERGENCE_MIN_WORDS}+ reference words (corpus {total})"], True

    text = mask(raw)
    n_draft = len(WORD.findall(text))
    if n_draft < VOICE_MIN_DRAFT:
        return [f"voice axis skipped: draft {n_draft} words, needs {VOICE_MIN_DRAFT}"], True

    scored = []
    for r, prof, words in profiles:
        delta, over, under = prof.score(text)
        scored.append((delta / prof.delta_band, delta, r, prof, over, under))
    scored.sort()
    ratio, delta, r, prof, over, under = scored[0]

    delta_ok = delta <= prof.delta_band
    lines = []
    reg_note = f" (closest register: {r})" if r else ""
    tag = "within the author's range" if delta_ok else "revise toward the reference"
    lines.append(f"delta {delta:.2f} vs author band <= {prof.delta_band:.2f}{reg_note}  ({tag})")
    if over:
        lines.append("  overused vs author: " + ", ".join(f"{w} (+{z:.1f}s)" for w, z in over))
    if under:
        lines.append("  underused vs author: " + ", ".join(f"{w} ({z:.1f}s)" for w, z in under))

    # Metrics are judged against the union of the register bands: the author
    # writes in every register the corpus holds, and a social habit is not a
    # deviation because the draft's vocabulary matched the essays. Each band is
    # p10-p90, so by construction it excludes a fifth of the author's own
    # chunks; the verdict therefore tolerates one out-of-band metric, which is
    # what genuine author text produces.
    out_of_band = 0
    dm = chunk_metrics(raw)
    for key in prof.metric_bands:
        lo = min(pr.metric_bands[key][0] for _, pr, _ in profiles)
        hi = max(pr.metric_bands[key][1] for _, pr, _ in profiles)
        v = dm[key]
        if v < lo * 0.95 or v > hi * 1.05:
            out_of_band += 1
            high, low = METRIC_ADVICE.get(key, ("reduce", "increase"))
            advice = high if v > hi else low
            if advice:
                lines.append(f"{key} {v:.1f} vs author {lo:.1f}-{hi:.1f}: {advice}")
    return lines, delta_ok and out_of_band <= 1


# ── example leakage ───────────────────────────────────────────────────────
# The examples teach shape, never phrases. In the A/B run an agent closed its
# post with the user's own example sentence word for word, which reads as
# theirs while being a copy. Any 5 consecutive words shared with an example's
# good side is flagged.

_LEAK_GRAMS = None


def _example_grams() -> set[tuple[str, ...]]:
    global _LEAK_GRAMS
    if _LEAK_GRAMS is None:
        grams = set()
        path = SKILL_DIR / "references" / "examples.md"
        if path.exists():
            for line in path.read_text().splitlines():
                if line.startswith("Good:"):
                    words = [w.lower() for w in WORD.findall(line)]
                    for i in range(len(words) - 4):
                        grams.add(tuple(words[i:i + 5]))
        _LEAK_GRAMS = grams
    return _LEAK_GRAMS


def check_example_leak(text: str) -> list[Finding]:
    grams = _example_grams()
    if not grams:
        return []
    out, words, positions = [], [], []
    for m in re.finditer(WORD, text):
        words.append(m.group(0).lower())
        positions.append(m.start())
    hit_at = set()
    for i in range(len(words) - 4):
        if tuple(words[i:i + 5]) in grams and i not in hit_at:
            for j in range(i, i + 5):
                hit_at.add(j)
            out.append(Finding(line_of(text, positions[i]), "example leak",
                               " ".join(words[i:i + 8]),
                               "copied from examples.md: say it your own way"))
    return out


# One action per rule, so the deslop report tells the agent what to do,
# not only where it failed.
RULE_ADVICE = {
    "vocabulary": "say what the clause means without this word",
    "non-literal predicate": "the subject cannot do this verb: write what happened",
    "borrowed idiom": "say it neutrally",
    "non-event": "an absence is information only if someone was checking: cut or cite the check",
    "buried verb": "find the real verb and make it the main verb",
    "what X is Y": "say it directly: subject, verb, object",
    "one X worth Y": "state what needs doing",
    "binary contrast": "state the second half and drop the negation",
    "chopped sentences": "join them with and or because",
    "repeated opener": "vary how sentences start",
    "chatbot residue": "delete: this is chat interface residue",
    "superficial -ing clause": "delete the clause or replace it with the fact",
    "dash": "replace with a comma, period, or parentheses",
    "curly quote": "use straight quotes",
    "semicolon rate": "use fewer semicolons",
    "unicode arrow": "write the relation in words",
    "emoji in heading": "remove",
    "title case heading": "use sentence case",
    "relative-clause title": "name the thing instead",
    "heading restated": "cut the line that repeats the heading",
    "inline-header list": "the label repeats the line: keep one",
    "bold label then a paragraph": "one sentence after the colon",
    "uniform rhythm": "vary sentence length",
    "example leak": "the example teaches the shape, not the words",
    "contrast tail": "drop the foil and keep the claim",
    "grand speak": "state the condition plainly",
}


def deslop_feedback(findings: list[Finding]) -> list[str]:
    by_rule: dict[str, list[Finding]] = {}
    for f in findings:
        by_rule.setdefault(f.rule, []).append(f)
    lines = []
    for rule, fs in sorted(by_rule.items(), key=lambda kv: -len(kv[1])):
        more = f"  (+{len(fs)-3} more)" if len(fs) > 3 else ""
        advice = RULE_ADVICE.get(rule, "")
        lines.append(f"{len(fs):>3}x {rule}{more}" + (f"  -> {advice}" if advice else ""))
        for x in fs[:3]:
            where = x.note if x.note and rule in ("vocabulary", "personal style", "borrowed idiom") else x.text[:60]
            lines.append(f"      l{x.line}: {where!r}")
    return lines


# ── two documents ─────────────────────────────────────────────────────────

NUMBER = re.compile(r"\b\d[\d,.]*%?\b")
PROPER = re.compile(r"\b[A-Z][a-zA-Z]{2,}\b")


def compare(before: str, after: str, vocab: dict[str, list[str]]) -> list[Finding]:
    """What the rewrite did. Preservation failures matter more than any tell."""
    out = []

    lost_numbers = set(NUMBER.findall(before)) - set(NUMBER.findall(after))
    if lost_numbers:
        out.append(Finding(0, "number changed or dropped", ", ".join(sorted(lost_numbers)),
                           "a rewrite never alters a figure"))

    stop = {"The", "This", "That", "These", "Those", "And", "But", "For", "Not", "Its"}
    lost_names = (set(PROPER.findall(before)) - set(PROPER.findall(after))) - stop
    if lost_names:
        out.append(Finding(0, "name dropped", ", ".join(sorted(lost_names))))

    before_hits = len(run_checks(before, vocab))
    after_hits = len(run_checks(after, vocab))
    if after_hits > before_hits:
        out.append(Finding(0, "residual grew", f"{before_hits} -> {after_hits}",
                           "the pass added more than it removed"))
    return out


# ── driver ────────────────────────────────────────────────────────────────

def load_style() -> dict[str, list[str]]:
    """Same format as the vocabulary, read from style.md. Missing file is fine:
    a fresh install has no personal layer yet."""
    if not STYLE.exists():
        return {}
    return load_vocabulary(STYLE)


def run_checks(raw: str, vocab: dict[str, list[str]],
               src_path: Path | None = None) -> list[Finding]:
    # Pattern checks read the masked text so quoted examples do not fire.
    # Rhythm checks read the raw text: masking blanks a quoted span, which
    # shortens the sentence around it and invents stub runs that are not there.
    text = mask(raw)
    style = load_style()
    keep = {w.lower() for w in section(style, "terms of art")}

    def kept(f: Finding) -> bool:
        """A term of art protects its exact match and any match inside it:
        "state machine" in the keep list also spares a hit on bare "state"
        when it sits inside that phrase."""
        if f.text.lower() in keep:
            return True
        clause = (f.note or "").lower().replace("<<", "").replace(">>", "")
        return any(f.text.lower() in phrase and phrase in clause
                   for phrase in keep if " " in phrase)

    findings: list[Finding] = []
    findings += check_physical_verbs(text, section(vocab, "physical verbs"))
    findings += [f for f in check_words(text, section(vocab, "^words"), "vocabulary",
                                        carve_out=section(vocab, "structural nouns"))
                 if not kept(f)]
    findings += check_words(text, section(style, "personal vocabulary"), "personal style")
    spare = [w.lower() for w in section(vocab, "spared phrases")]
    def spared(f: Finding) -> bool:
        clause = (f.note or "").lower().replace("<<", "").replace(">>", "")
        return any(f.text.lower() in term and term in clause for term in spare)
    findings = [f for f in findings if not spared(f)]
    findings += check_absence(text)
    findings += check_buried_verbs(text)
    findings += check_headings(text)
    findings += check_stub_runs(raw)
    findings += check_openers(raw)
    findings += check_words(text, section(vocab, "chatbot residue"), "chatbot residue")
    findings += check_extra(text)
    findings += check_heading_restated(text)
    if src_path is None or src_path.name != "examples.md":
        # examples.md is the gram source; scanning it against itself is noise.
        findings += check_example_leak(text)
    findings += check_punctuation(text)
    findings += stylometry_findings(stylometry(raw))
    return sorted(findings, key=lambda f: (f.line, f.rule))


def report(path: Path, findings: list[Finding], stats: dict[str, float],
           raw: str | None = None, register: str | None = None) -> None:
    print(f"\n{path}  ({int(stats['words'])} words, {int(stats['sentences'])} sentences)")
    if not findings:
        print("  deslop: clean")
    else:
        print(f"  deslop: {len(findings)} findings")
        for line in deslop_feedback(findings):
            print("  " + line)
    if raw is not None:
        lines, ok = voice_report(raw, register)
        print(f"  voice: {'ok' if ok else 'ADJUST'}")
        for line in lines:
            print("    " + line)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self", action="store_true", help="run on this skill's own files")
    ap.add_argument("--register", help="compare only against reference files with this register")
    args = ap.parse_args()

    vocab = load_vocabulary()
    words, live = corpus_status()

    paths = list(args.files)
    if args.self:
        # reference-writing/ is the author's verbatim prose, kept as data.
        # Linting it would demand edits that corrupt the reference, so the
        # self-scan covers the skill's own files only.
        paths = [SKILL_DIR / "SKILL.md"] + sorted(
            p for p in (SKILL_DIR / "references").rglob("*.md")
            if REFERENCE_DIR not in p.parents)

    if not paths:
        ap.error("give a file, or --self")

    if len(paths) == 2 and not args.self:
        before, after = (p.read_text() for p in paths)
        findings = compare(before, after, vocab) + run_checks(after, vocab)
        if args.json:
            print(json.dumps([asdict(f) for f in findings], indent=1))
        else:
            report(paths[1], findings, stylometry(mask(after)), raw=after, register=args.register)
        return 1 if findings else 0

    total = 0
    payload = {}
    for path in paths:
        raw = path.read_text()
        findings = run_checks(raw, vocab, src_path=path)
        total += len(findings)
        if args.json:
            entry = {"findings": [asdict(f) for f in findings]}
            if not args.self:
                lines, ok = voice_report(raw, args.register)
                entry["voice"] = {"ok": ok, "feedback": lines}
            payload[str(path)] = entry
        else:
            # The self-scan checks the skill's own files for tells; comparing
            # instruction files to the author's prose would be noise.
            report(path, findings, stylometry(mask(raw)),
                   raw=None if args.self else raw, register=args.register)

    if args.json:
        print(json.dumps(payload, indent=1))
    else:
        print(f"\nreference corpus: {words} words")
        print(f"divergence checks: {'live' if live else f'dark, needs {DIVERGENCE_MIN_WORDS}'}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
