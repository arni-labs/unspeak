# unspeak

![unspeak banner](banner.png)

A writing skill for coding agents to remove LLM tells and keep the writer's voice. Works with any harness that reads SKILL.md (Claude Code, Codex, Cursor, and others).

## Use

- `/unspeak` rewrites the draft in front of you. Add words to direct it: `/unspeak this file`, `/unspeak write about ...`.
- `/unspeak-init` builds your voice reference: paste a few pieces of your writing, the agent files them.
- `/unspeak-add word, phrase, "bad snippet"` files new offenders into the lists.
- `python3 unspeak/proofread.py draft.md` checks a file without an agent.

## Examples

The first two paragraphs of a technical post and a personal blog, both written from the same bare brief by fresh agents. Left: no skill. Right: the full unspeak flow (imitation of the author's samples, tell hunt, proofread, reviewer subagent).

<table>
<tr><th>No skill</th><th>unspeak</th></tr>
<tr><td>Our ops dashboard has a panel called &quot;Orders by region, last 30 days.&quot; It took 11 seconds to load. Everything else on the page came back in under 200ms.<br><br>The query behind it was unremarkable:</td><td>Our billing dashboard rendered at 8.4s p95. I sorted pg_stat_statements by total_exec_time. The top query took 38% of execution time on the primary and ran 940 times an hour.<br><br>It counts usage events per day for one account, over the range the date picker sends:</td></tr>
</table>

<table>
<tr><th>No skill</th><th>unspeak</th></tr>
<tr><td>I bought the piano at thirty-eight, from a woman in Cheltenham who was moving to a flat with no room for it. An upright Yamaha, middle C slightly yellowed, the whole thing smelling faintly of furniture polish. Two men carried it up my stairs and swore at the corner by the bathroom. Then it sat there for eleven days while I found reasons not to touch it.<br><br>What broke the standoff was lowering the bar. Not an hour. Twenty minutes, after the kettle goes on in the morning, before anyone else is up. Scales for five, then whatever I&#x27;m working on. Right now that&#x27;s the first page of a Satie piece I will probably never finish properly.</td><td>I rented a cello two years ago and I keep renewing it. Marta, my teacher, found it for me, and for the first few months my left fingertips split and I taped them before bed.<br><br>I practice in the morning before my daughter is up, and most of it is scales, C major up and back down, then the same run in E flat, which I still can&#x27;t play cleanly, then a page of whatever étude Marta assigned, played slowly enough that I hear my finger come down flat and fix it before the next note. She won&#x27;t let me speed a passage up until it&#x27;s clean three times in a row. I resented that rule for most of the first year, and now I set the metronome myself (lower than she would).</td></tr>
</table>

## Install

Three skills, three folders. Clone and link them into your skills directory:

```
git clone https://github.com/arni-labs/unspeak
ln -s "$PWD/unspeak/unspeak" "$PWD/unspeak/unspeak-init" "$PWD/unspeak/unspeak-add" ~/.claude/skills/
```

## How it works

SKILL.md has the rules (vocabulary, sentence structures, claims, framing, chatbot residue, format). references/vocabulary.md lists the words an agent must not use, and the agent reads it before writing. proofread.py catches what the agent missed, and compares the draft against your own writing (Burrows's Delta over frequent words and punctuation, bands derived from your samples).

## Your voice

Put your own prose in references/reference-writing/, one file per register. references/style.md collects your personal rules. General corrections go to the vocabulary and the rules, personal ones to your style file.
