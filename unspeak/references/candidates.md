# Candidates

Corrections collected during work. Agents append here. Only the user promotes an
entry to `vocabulary.md` or to SKILL.md.

A word cut once is noise. Cut three times across different documents, it is a
candidate.

Format: date, what the agent wrote, what the user wrote, and the pattern if one is
already named.

---

## 2026-08-25, first session

The whole set below came from one conversation, which is why the counts are
high. Everything marked **promoted** is already in SKILL.md or `vocabulary.md`.

| Agent wrote | User wrote | Pattern | Status |
|---|---|---|---|
| "The word that cannot be wrong" (heading) | — | Relative-clause title | promoted |
| "The finding that matters" (heading) | — | Relative-clause title | promoted |
| "publishing only the flattering one is the behavior this project exists to criticize" | "We criticize publishing only the good ones, so we publish both." | Buried verb | promoted |
| "One conflict worth your call" | "This needs a decision." | Performed precision | promoted |
| "Do not build a composite AI-ness score. Their corpus is the evidence against it." | "Don't do Z. It didn't work for X." | Chopped sentences, buried verb | promoted |
| "the cheap version costs nothing" | — | Not yet named | open |
| "the dictionary maintains itself" | — | Non-literal predicate | promoted |
| "If the reader would do nothing differently at 4 cars" | — | Example leaking into an abstract rule | open |
| "the piece worth taking" | — | Performed precision, and an unclear referent | promoted as vocabulary (`worth`) |
| "encode at the strongest rung that fits" | "encode at the strongest that fits" | Borrowed idiom | promoted |
| "We edited 7 cars out of the frames" | "We edited the cars out." | Decorative number | promoted |

Words named directly: `seams`, `shape`, `land`, `name` (verb), `unlock`, `rung`,
`honest take`. All promoted. `belt and suspenders` promoted too, although the user
had not encountered it.

## Open items

**"the cheap version costs nothing."** Flagged by the user, and neither of us
named it. It is not quite performed precision and not quite procedural filler.
A candidate reading: the sentence asserts a cost of zero that nobody priced,
which puts it with the non-events, since both report a measurement that was
never taken. Needs a decision before it becomes a rule.

**Example leaking into a rule.** When stating an abstract test, the agent
went back for a concrete noun from an earlier example and bound the rule to
it. This is why examples live in `examples.md` and rules stay abstract in
SKILL.md. Whether it is also a pattern to flag in prose is open.

## 2026-08-26, bake-off review of this skill's own output

The user read the six-way bake-off output produced with this skill and rejected
most of it. Everything below came from that read.

Promoted by the user in the same session:

| Item | Went to |
|---|---|
| Superlative claims ("throughput has never been higher") | SKILL.md Claims 9 + style.md Rule 4 |
| "It's more than X. It's Y" and "means more than" | SKILL.md 7, setup before the point |
| Consequence tail ("so there is no credential to exfiltrate") | SKILL.md 15 |
| Emphasis tail ("no exceptions, nothing deferred") | SKILL.md 16 |
| "carries/has its own contract" | SKILL.md 17, owned abstraction |
| "never reconstructing one afterwards" | SKILL.md 18, trailing participle |
| "gets no extra vote" | SKILL.md 19, unexplained metaphor |
| Illustrative lists for breadth | SKILL.md Claims 10 + style.md Rule 5 |
| govern, governed, the best part, stay put, come and go, here's what, still early, we're early | vocabulary |
| keep (kept) | physical verbs |
| "make correct behavior unsurprising" | removed from AGENTS.md |

Bug found by this review: the verb inflection regex never matched y-verbs, so
"carries" passed every scan since the list was written. Fixed in proofread.py.

Open, needs the user's decision:

**"rather than".** Flagged twice in the output as an LLM contrast tail
("delegating better rather than typing faster"). But the user's own corpus uses
it 7 times (5 in the essay, 2 in X posts). The difference may be a manufactured
foil versus a real alternative. Judgment-only for now, no flag.

**"apply", "the work".** Named as overused LLM verbs/nouns that need concrete
replacements in context. Too common to flag as bare words without drowning the
report. Not promoted, watching for repeats.

## 2026-08-26, bake-off review of the comparator outputs

The user read samples A, C, E, F. Sample G skipped (their call, enough).

- A (stop-slop): nothing to adopt. "The shift goes past automation. I rethought
  what the development environment is" did better than our version but still splits into
  two sentences.
- C (avoid-ai-writing): nothing to adopt.
- E (blader/humanizer): nothing to adopt.
- F (cursor unslop): two wins, one mechanism. It replaced the superlative with
  "I'm shipping more now than when I typed everything myself", and its closing
  paragraph restated the point personally instead of neutrally. Both trace to
  that skill's "Adding soul" section (be specific, have opinions, use I). Now
  the Voice section in SKILL.md. The user's own wording of that closing is in
  examples.md.

Promoted to vocabulary from this read: `verbatim`, `centerpiece`, `gauntlet`,
`bolted`, `bolt on`, `spin up`, `belongs`, `belong`.

Also promoted as policy: agents read vocabulary.md and follow it themselves.
The script verifies afterward, it is not the first line.

## 2026-08-26, A/B review

The user read the with-proofread version, stopped reading the without version early,
and rejected both. Everything promoted the same session:

- **Example leakage named as a phenomenon.** The output reused
  "when I typed everything myself" and the user's own closing paragraph
  word for word from examples.md, and "so nobody has to reconstruct one afterwards"
  survived because an agent had written it into an example's good side.
  Now: a leak rule in SKILL.md, a 5-gram leak detector, and the contaminated
  example fixed.
- **`rather than` banned outright**, reversing the earlier judgment-only call.
  The user's corpus uses it 7 times, and the ban is their explicit decision
  over that tension.
- **`panel` to vocabulary.** Note: the user's own AGENTS.md uses "panel" for
  the review trio, and that file may want the same edit.
- **`not perfect yet` to vocabulary**, with `reach` joining the physical verbs
  and configuration/config joining the abstract subjects, from the draft line
  about user scope configuration and background agents.
- New structures: contrast tail, negative capability, grand speak.
- Still unsolved: the with-proofread version's closing carried no voice of its
  own. The Voice sentence instructs it, and nothing enforces or measures it.

- `arm` promoted to vocabulary (2026-08-26). Experiment jargon the user never
  uses and finds meaningless. Same class as the plain-stage-language rule that
  already banned it in their notes; say "the version with X" or "the run
  without X".

- 2026-08-26, hook false positives fixed same day they appeared: `bake` fired
  on the compound bake-off (hyphenated compounds now skip), and `live`/`lives`
  fired as adjective and noun ("a live session", "our lives"; an article,
  copula, or possessive directly before now skips, "the value lives in Redis"
  still fires). 9 regression cases pass.

- 2026-08-26, `land` moved from the subject-gated physical verbs to the
  main list (`land`, `lands`, `landed`, `landing`). The subject check misses
  pronoun subjects ("when it lands"), and the user flagged exactly that use.

- 2026-08-26, from the taste-test read: `each one` to vocabulary; two new
  patterns promoted. Drumroll (Sentences 22): the same point repeated in short
  sentences to build toward a non-revelation. Opening tease (Framing 16):
  dangling the payoff detail in the first sentence as a hook.

- 2026-08-26, from the README examples read: `the easy part`/`the hard part`
  and `bucket` to vocabulary (spared: s3/storage/gcs bucket, via the new
  general Spared phrases block). Novelized detail promoted to Framing 17
  ("the kind of slowness users feel and stop reporting", "the way wellness
  apps promise"): cut the color, give the measurable fact. Loader bug found
  by the s3 spare: tokens with digits were dropped from words blocks.

- 2026-08-26, from the second README tech example: the unspeak output itself
  was rejected as narrative ("we trusted it a little less every time we
  waited", "in a place we rarely opened"). Framing 18 added: technical
  writing is mechanism, numbers, and steps; no story arc, no feelings, no
  scene. The failure shows the skill can strip tells and still produce the
  wrong register.

- 2026-08-26, user promotion: `no one`, `no single`, `just one`, `single` to
  vocabulary. The one-ness emphasis family (`a single query`, `no single cause`): the
  count adds no information to the plain sentence.
