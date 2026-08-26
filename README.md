# unspeak

A writing skill for coding agents. It removes LLM tells and keeps the writer's voice. Works with any harness that reads SKILL.md (Claude Code, Codex, Cursor, and others).

Two rules run it. Don't use slangy metaphors that fit any context and so mean nothing concrete, and delete every word that doesn't communicate. An LLM sentence wraps its point in a setup and a tail, and the fix is always the same, say the point plainly.

## Examples

"My throughput has never been higher" becomes "I ship more PRs than I did in December".

"The cache had a correctness problem that survived every release" becomes "We never fixed the correctness problem in the cache".

"One conflict worth your call" becomes "This needs a decision".

"These credentials expire the moment the task ends, so there is no persistent credential to exfiltrate" loses the tail, because the reader can infer it.

## Install

```
git clone https://github.com/arni-labs/unspeak ~/.claude/skills/unspeak
```

## How it works

SKILL.md holds the rules (vocabulary, sentence structures, claims, framing, chatbot residue, format). references/vocabulary.md lists the words an agent must not use, and the agent reads it before writing. proofread.py runs after, catches what the agent missed, and compares the draft against your own writing (Burrows's Delta over frequent words and punctuation, with bands derived from your samples).

## Your voice

Put your own prose in references/reference-writing/, one file per register. references/style.md collects your personal rules, the corrections that are yours and not slop. Both start empty. General corrections go to the vocabulary and the rules, personal ones to your style file, and you approve every promotion.

`/unspeak add word, phrase, "bad snippet"` files new offenders directly.
