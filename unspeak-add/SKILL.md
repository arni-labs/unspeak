---
name: unspeak-add
description: File new LLM-tell words, phrases, or bad snippets into the unspeak skill's lists. Use when the user invokes /unspeak-add followed by the items.
---

# Unspeak add

The arguments are a promotion, already decided: the user is dumping offenders for you to file into the `unspeak` skill in the sibling folder `../unspeak/`.

Allocate every item yourself:

1. LLM words and phrases go into the main words block of `../unspeak/references/vocabulary.md`.
2. Personal-only items (ordinary English this user avoids, or a term of art the vocabulary wrongly flags) go into `../unspeak/references/style.md`.
3. Snippets with a fix go into `../unspeak/references/examples.md` as a bad/good pair.
4. Anything you cannot place goes into `../unspeak/references/candidates.md` marked unsure.

Show the user what went where. This command is the one case where you edit the lists directly. With no arguments, ask what to file.
