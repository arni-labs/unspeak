---
name: unspeak-init
version: "0.2.0"
description: Set up the unspeak writing skill for a new user. Collects their writing samples into the reference corpus and starts their personal style file. Use when the user invokes /unspeak-init or asks to set unspeak up.
---

# Unspeak init

This command sets up the personal layers of the `unspeak` skill, which lives in the sibling folder `../unspeak/`.

1. Ask the user to paste two or three pieces of their own writing, or to name files or links you can read. Prefer published or deliberately written prose over chat or dictation.
2. For every piece, create a file in `../unspeak/references/reference-writing/`, one per register (technical, essay, social). Wrap the text in `<!-- verbatim -->` and `<!-- /verbatim -->` markers and fill the frontmatter (register, source, word count). Put nothing of your own inside the markers.
3. If `../unspeak/references/style.md` is missing, copy its section skeleton from the unspeak SKILL.md description of the file: Rules, Never, Use, Terms of art, Personal vocabulary, Unconfirmed. Leave every section empty.
4. Run `python3 ../unspeak/proofread.py` on one of the new files and tell the user which checks came alive at the current corpus size.
5. Run `python3 ../unspeak/proofread.py --voice-md` to write `../unspeak/references/VOICE.md`: their voice as one file, in the layout and band schema of a Katagami writing style. Bands appear per register once it has about 2,000 words.
6. Prove the file works: ask one fresh subagent to read only `VOICE.md` and write about 300 words in one register, then run `proofread.py --register <register>` on the result. Tell the user what it reported, and that they can hand `VOICE.md` to any agent.

The skill works before this setup exists. Never ask the user to copy files anywhere; you do the filing.
