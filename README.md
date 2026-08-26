# unspeak

![unspeak banner](banner.png)

A writing skill for coding agents to remove LLM tells and keep the writer's voice. Works with any harness that reads SKILL.md (Claude Code, Codex, Cursor, and others).

## Use

- `/unspeak` rewrites the draft in front of you. Add words to direct it: `/unspeak this file`, `/unspeak write about ...`.
- `/unspeak-init` builds your voice reference: paste a few pieces of your writing, the agent files them.
- `/unspeak-add word, phrase, "bad snippet"` files new offenders into the lists.
- `python3 unspeak/proofread.py draft.md` checks a file without an agent.

## Examples

The first two paragraphs of a technical post and a personal blog. The draft is a vanilla model writing from a bare prompt; the rewrite is an agent told only "unspeak this draft", with a reference corpus and style file installed.

<table>
<tr><th>Draft</th><th>unspeak</th></tr>
<tr><td>Last month, our internal ops dashboard started timing out during peak hours. Not every load — just enough to generate a steady trickle of complaints from the warehouse team, who use it to track order fulfillment in real time. The first instinct was &quot;add more caching,&quot; but we wanted to understand what was actually slow before papering over it.<br><br>We started with our Postgres slow query log, filtered to anything over 500ms in the last 24 hours. One query stood out immediately: it powered the &quot;Orders Pending Fulfillment&quot; widget, and it was averaging 4.2 seconds — with tail latencies spiking past 12 seconds during the 9am shift-change rush.</td><td>Our internal ops dashboard started timing out during peak hours last month, and the complaints came from the warehouse team, who use it to track order fulfillment. The first suggestion was more caching, but we wanted to find the slow part first.<br><br>We filtered the Postgres slow query log to anything over 500ms in the last 24 hours. The query behind the &quot;Orders Pending Fulfillment&quot; widget averaged 4.2 seconds, with p99 at 12 seconds during the 9am shift change.</td></tr>
</table>

<table>
<tr><th>Draft</th><th>unspeak</th></tr>
<tr><td>I bought a used tenor ukulele on a Tuesday in March, mostly because the guitar in my closet had twelve years of dust on it and felt like a rebuke every time I opened the closet door. The ukulele felt smaller, less judgmental. Four strings instead of six. A toy, I told myself, so it wouldn&#x27;t matter if I was bad at it.<br><br>I was very bad at it. My fingers, forty-one years old and calibrated for typing and chopping onions, did not want to hold a C chord. They wanted to do literally anything else. The first week, I could get through &quot;Riptide&quot; if you squinted with your ears — chunks of silence where a chord change should be, a buzzing string I never quite pinned down.</td><td>I bought a used tenor ukulele on a Tuesday in March, mostly because the guitar in my closet had twelve years of dust on it and I had stopped opening that door. Four strings instead of six, a smaller body, and I told myself it was a toy, so being bad at it would cost me nothing.<br><br>I was bad at it. My fingers are forty-one years old and trained for typing and chopping onions, and they would not hold a C chord. In the first week I could get through &quot;Riptide&quot; if you allowed for the silences where the chord changes go, and for one string that buzzed the whole way through, which I never traced.</td></tr>
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
