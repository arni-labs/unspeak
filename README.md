# unspeak

A writing skill for coding agents. It removes LLM tells from text and keeps the writer's own voice. Works with any harness that reads `SKILL.md` (Claude Code, Codex, Cursor, and others).

Two rules run the whole skill:

1. Don't use slangy metaphors that fit any context and so mean nothing concrete.
2. Every word should serve a purpose. Delete words that don't communicate clearly.

An LLM sentence wraps its point in a setup and a tail. The skill names the shapes that wrapping takes and the fix is always the same: say the point plainly.

## Examples

Before: "My throughput has never been higher."
After: "I ship more PRs than I did in December."

Before: "The cache had a correctness problem that survived every release."
After: "We never fixed the correctness problem in the cache."

Before: "One conflict worth your call."
After: "This needs a decision."

Before: "These credentials expire the moment the task ends, so there is no persistent credential to exfiltrate."
After: "These credentials expire the moment the task ends."

## Install

Copy this folder into your agent's skills directory:

```
git clone https://github.com/arni-labs/unspeak ~/.claude/skills/unspeak
```

## How it works

- `SKILL.md` holds the rules: vocabulary, sentence structures, claims, framing, chatbot residue, format.
- `references/vocabulary.md` lists the words the agent must not use. The agent reads it first and follows it. `proofread.py` reads the same lists afterward to catch what the agent missed.
- `proofread.py` also compares a draft against your own writing (Burrows's Delta over frequent words and punctuation, with bands derived from your samples) and reports which words and habits diverge.

## Your voice

Drop your own prose into `references/reference-writing/`, one file per register, wrapped in the markers its README describes. `references/style.md` collects your personal rules, the corrections that are yours and not slop. Both start empty and grow from your feedback: general corrections go to the vocabulary and the rules, personal ones to your style file, and you approve every promotion.

`/unspeak add word, phrase, "bad snippet"` files new offenders directly.
