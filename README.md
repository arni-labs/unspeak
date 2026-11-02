# unspeak

![unspeak banner](banner.png)

A writing skill for coding agents to remove LLM tells and keep the writer's voice. Works with any harness that reads SKILL.md (Claude Code, Codex, Cursor, and others).

## Use

- `/unspeak` rewrites the draft in front of you. Add words to direct it: `/unspeak this file`, `/unspeak write about ...`.
- `/unspeak-init` builds your voice reference: paste a few pieces of your writing, the agent files them.
- `/unspeak-add word, phrase, "bad snippet"` files new offenders into the lists.
- `python3 unspeak/proofread.py draft.md` checks a file without an agent.
- `python3 unspeak/proofread.py --voice-md` writes `unspeak/references/VOICE.md`, your voice as one file you can hand to any agent.

## Examples

A technical post and a personal blog. The source drafts were written by a bare model with no skill, no user config, and no instructions beyond the topic. The right column is an agent given only "unspeak this draft" with the skill installed. Excerpts, the opening of each piece.

<table>
<tr><th>Draft</th><th>unspeak</th></tr>
<tr><td><strong>The Query That Was Quietly Taking Down Our Dashboard</strong><br><br>Last month, our internal ops dashboard started timing out during peak hours. Not every load — just enough to generate a steady trickle of complaints from the warehouse team, who use it to track order fulfillment in real time. The first instinct was "add more caching," but we wanted to understand what was actually slow before papering over it.<br><br>We ran <code>EXPLAIN ANALYZE</code> and found the problem right away: a sequential scan over <code>orders</code>, which had grown to 38 million rows. The <code>status</code> column had an index, but Postgres was ignoring it — because <code>status = 'pending'</code> matched roughly 22% of the table (pending orders pile up during promotions and don't get archived quickly), so the planner correctly decided a full scan beat an index scan on that column alone.</td><td><strong>Fixing the pending-orders query</strong><br><br>Our ops dashboard timed out during peak hours last month. It didn't fail on every load, and the warehouse team, who track order fulfillment on it, kept reporting it. Someone suggested a cache, but we went to the Postgres slow query log first, filtered to anything over 500ms in the last 24 hours.<br><br><code>EXPLAIN ANALYZE</code> showed a sequential scan over <code>orders</code>, which has grown to 38M rows. There was an index on <code>status</code>, and the planner skipped it because <code>status = 'pending'</code> matches about 22% of the table, so a full scan costs less than an index scan on <code>status</code> alone.</td></tr>
</table>

<table>
<tr><th>Draft</th><th>unspeak</th></tr>
<tr><td><strong>Fifteen Minutes With the Wrong Notes</strong><br><br>I bought a used tenor ukulele on a Tuesday in March, mostly because the guitar in my closet had twelve years of dust on it and felt like a rebuke every time I opened the closet door. The ukulele felt smaller, less judgmental. Four strings instead of six. A toy, I told myself, so it wouldn't matter if I was bad at it.<br><br>I was very bad at it. My fingers, forty-one years old and calibrated for typing and chopping onions, did not want to hold a C chord. They wanted to do literally anything else. The first week, I could get through "Riptide" if you squinted with your ears — chunks of silence where a chord change should be, a buzzing string I never quite pinned down.</td><td><strong>Fifteen minutes on the ukulele</strong><br><br>I bought a used tenor ukulele in March. The guitar in my closet had sat there twelve years without being tuned, and I wanted an instrument with fewer strings that I hadn't already failed at (a tenor, because the neck is wider and my fingers aren't small). I told myself it was a toy, so being bad at it wouldn't count.<br><br>I was bad at it. My fingers are forty-one and they know how to type and hold a knife, not make a C chord, so the first week I got through "Riptide" with gaps where the chord changes should have been and one string buzzing that I never tracked down.</td></tr>
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

`/unspeak-init` also writes references/VOICE.md from those two: an excerpt of each sample, your confirmed rules, and per-register numbers measured from your writing (sentence length and spread, punctuation rates, vocabulary range, function-word distance). It uses the same layout and band schema as a [Katagami](https://katagami.ai) writing style, so any agent can write in your voice from that file alone, and Katagami's checker can score a draft against it. It is built, never edited: run `proofread.py --voice-md` after you add a sample or confirm a rule.
