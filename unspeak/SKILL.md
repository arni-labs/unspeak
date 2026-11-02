---
name: unspeak
version: "0.2.0"
description: Remove LLM tells from writing. Applies to every sentence you produce, not only when asked.
---

# Unspeak

## Write by imitation, clean by rules

Imitation leads and the rules verify. Banning tells one by one only moves the model to its next-most-trained register, so the target voice has to come from the author's own writing, and the rules then strip what leaked through.

1. **Immerse.** When `references/style.md` or `references/reference-writing/` exist, reading them is mandatory before writing a word. Pick the sample whose register matches the task and read it whole. It is writing you are about to continue. The style file's rules bind exactly like this file's.
2. **Write as the author.** Draft the piece as a continuation of that author's work: their sentence swing, their punctuation, what they would notice and what they would leave out. Do not think about the rule lists while drafting. When you are generating from scratch (a new piece, no draft given), put the sample itself at the top of your working context first: `proofread.py --sample --register <register>` prints it, and you write directly under it, then delete the sample from the output.
3. **Hunt tells.** Now take the draft through every section below and `references/vocabulary.md`, and remove or rewrite everything they name. Nothing on these lists survives because the draft came out voice-first.
4. **Verify.** Run `proofread.py` and fix what it names, on both axes, until it passes. It reports deslop findings with what to do about each, and distance from the reference writing (Burrows's Delta plus the author's own metric bands) with the words and habits causing it.
5. **Review.** Spawn a fresh subagent as reviewer and apply what it finds. This step is mandatory: the script only sees patterns, and the writer of a draft cannot see their own residue. Give the reviewer this skill's directory and the draft, and this brief: read SKILL.md, references/vocabulary.md, references/style.md, and the reference samples, then name what in the draft still breaks a rule, still reads as an LLM, or does not sound like the author, quoting each place and saying what to do instead. The reviewer must find things to improve, a pass verdict is not an output it can produce; if the draft is strong, its findings get smaller, never absent. Apply the findings that are right, run `proofread.py` once more, and only then return the piece.

Never reuse wording from `references/examples.md` or the reference writing: they teach the pattern, and copying their words into output is a defect the leak check flags.

The words in `references/vocabulary.md` are abstract, metaphorical, and out of place; use the word that expresses the meaning in that context.

1. **Don't use slangy metaphors that fit any context and so mean nothing concrete.**
2. **Every word should serve a purpose, delete words that don't communicate clearly and create filler prose.**

An LLM sentence wraps its point in a setup and a tail. The structures below are the shapes that wrapping takes, and the fix is always the same: say the point plainly.

## Remove from your vocabulary or replace with a direct word that fits the specific sentence and conveys exact meaning

1. **Non-literal predicates:** abstract subject, physical verb, as in "the assumption survives" or "the design sits below".
2. **Trade colloquialisms you have no part in:** "load-bearing", "earn its keep", "seams", "rung"; default to neutral.
3. **Metaphor nouns:** "surface", "substrate", "shape", "flywheel".
4. **Verbed nouns:** "coin", "gate", "architect", "onboard".
5. **Moral adjectives on a non-agent:** "an honest shape", "flagged honestly".
6. **Inflated diction:** "delve", "pivotal", "robust", "seamless", "leverage"; use down to earth words.
7. **Copula avoidance:** "serves as", "boasts", "features", "represents"; use is or has.
8. **Adverbs propping a weak verb:** "significantly improves"; give the number or change the verb.
9. **Hedge stacks:** "could potentially", "may eventually"; be affirmative.
10. **Invented labels and vocabulary:** coining "the supervision paradox" instead of describing the mechanism.
11. **Novelty inflation:** "she coined the term", "a problem nobody names".

## Don't use these sentence structures

1. **Buried verb:** "What this does is reduce latency", "X is the behavior we criticize"; use [subject] [verb] [object].
2. **`What X is, is Y`:** "What this needs is a rewrite"; say "This needs a rewrite".
3. **`The X that does Y`:** "The word that cannot be wrong"; name the thing.
4. **`One X worth Y`:** "One conflict worth your call"; say what needs doing.
5. **Nominalization:** "made a decision", "performs an analysis", "has the ability to".
6. **Chopped sentences:** several short sentences that could have been one straightforward sentence.
7. **Setup before the point:** "Not X, it's Y", "It's more than X. It's Y", "Done means more than X"; delete the setup and say Y.
8. **Negative listing:** "Not a X. Not a Y. A Z"; just say Z.
9. **False range:** "from X to Y" where the ends are not on one scale.
10. **Agentless passive:** "queries are validated"; use [subject] [verb] [object].
11. **Colon reveal:** "The detail that makes it work: a second agent".
12. **Aphorism formula:** "X is the language of Y", "the currency of Z".
13. **Bold label then a paragraph:** a bold statement followed by several sentences of explanation; use a colon and one sentence.
14. **Uniform rhythm:** every sentence the same length.
15. **Consequence tail:** "...so there is no persistent credential to exfiltrate"; the reader can infer it, cut it.
16. **Emphasis tail:** "with no exceptions, nothing deferred" after a sentence that already said it.
17. **Owned abstraction:** "every repo carries its own contract"; name the actual things instead.
18. **Trailing participle:** "...never reconstructing one afterwards"; make it a plain clause: "so it doesn't have to reconstruct it".
19. **Unexplained metaphor:** "the authoring agent gets no extra vote"; give the mechanism instead of the figure.
22. **Drumroll:** the same point repeated in short sentences to build toward a reveal that is not one ("Every submission came back polished. The layouts worked. They all worked."); say it once and move on.
20. **Contrast tail:** "the repository is the portable unit, not my dotfiles", "delegating better rather than typing faster"; drop the foil, keep the claim.
21. **Negative capability:** "user config never reaches a background agent"; say it from the actor: "a background agent has no access to user config".

## When making claims don't pollute them with

1. **Decorative numbers that are irrelevant:** "7 cars in the frame"; why 7, why cars, and are these specifics important or just an example? Either explain using the correct higher-order abstraction, or, if details are required, list all of them instead of random ones.
2. **Non-events:** "Nobody complained", "Nothing broke".
3. **Vague attribution:** "experts believe", "studies show"; name the source or cut the claim.
4. **Significance inflation:** "a pivotal moment", "a testament to"; explain what happened.
5. **Superficial -ing clauses:** "...highlighting the team's commitment"; delete, or replace with the fact.
6. **Unfalsifiable closers:** "may become one of the most important trends"; predict something checkable.
7. **Procedural filler:** "this needs a design review first", true of nearly anything.
8. **Universal quantifiers:** "taught in every first-year course"; use the real scope.
9. **Superlative claim:** "throughput has never been higher"; make the claim specific or honest instead of bigger.
10. **Illustrative list:** examples listed to perform breadth, "from anywhere: my laptop, Claude's cloud, Cursor's cloud"; list only what the reader needs.
11. **Specificity as texture:** prices, clock times, ages, and model numbers sprinkled to make invented prose feel lived-in ("$1,900 Yamaha at 37, 25 minutes at 6:40am, 40 to 63 bpm"). A detail earns its place by carrying a feeling or a fact the piece needs, and a piece supports one or two. Everywhere, they read as set dressing.

## Framing

1. **Staged narration:** "...and then watched the old answer come back"; write what happened.
17. **Novelized detail:** "the kind of slowness users feel and stop reporting", "the way wellness apps promise"; cut the color and give the measurable fact.
18. **Narrative in technical writing:** "we trusted it a little less every time we waited", "in a place we rarely opened", "adding an index would have been a guess"; technical writing is mechanism, numbers, and steps, and every sentence must give the reader information. No story arc, no feelings, no scene.
2. **Throat-clearing:** "Here's the thing:", "The truth is,".
3. **Rhetorical setup:** "What if I told you", "Think about it:", "The catch?".
4. **Faux insight:** "what nobody tells you", "the part everyone misses".
5. **Interpretive metadiscourse:** "This distinction matters", "As you can see".
6. **Self-labeling significance:** "That last one is the contrarian one"; let the content show it.
7. **Emotional flatline:** "What surprised me most", "I was fascinated to learn".
8. **Narrated candor:** "To be fully transparent:", "I'd rather flag this than let you find it".
9. **Phantom objection:** "I'm not saying X", "Some might argue", with no such claim in the text.
10. **Fake alternative:** "A tempting approach would be X, but", for an option nobody would take.
11. **Fake-profound kicker:** the deep closing line; cut it and end concretely.
12. **Summary recap:** "In conclusion", "Ultimately", or a final paragraph restating the piece.
13. **Diff-anchored writing:** "This was added to replace the old approach"; describe how it works now.
14. **Heading restated:** a heading followed by one line repeating it.
15. **Grand speak:** "before anyone says the work is complete"; say the condition plainly.
16. **Opening tease:** dangling the payoff detail in the first sentence ("...until I had eleven answers in front of me at once"); start with the situation.
19. **Self-appraisal:** the writer grading their own experience as they report it: "bad in a way I didn't anticipate", "which is a strange combination to sit in for an hour", "not because I had any reason to think I'd be good". Report what happened and what you did; the reader decides what was strange. When the tells below are all removed, this is the register the model retreats to, so hunt it deliberately: at most one appraisal in a piece, and only where the experience alone cannot say it.
20. **Anticipation frame:** "in a way I didn't expect", "what I didn't anticipate was"; the adjectival cousin of emotional flatline. Say what happened without the surprise wrapper.
21. **Vague-way qualifier:** "badly in a particular way", "a specific kind of quiet", "a certain kind of tired"; the phrase promises precision and delivers none. Name the way, or drop the qualifier.

## Chatbot residue

1. **Sycophancy:** "Great question!", "You're absolutely right!".
2. **Assistant artifacts:** "I hope this helps!", "Let me know if...", "Would you like me to".
3. **Acknowledgment loop:** restating the question before answering.
4. **Reasoning leak:** "Let me think", "Step 1:", `Breaking this down`, and any other reasoning meant to stay internal.
5. **Cutoff disclaimer:** "As of my last update", "while specific details are limited".
6. **Fingerprints:** `citeturn0search0`, `utm_source=chatgpt.com`, `[Your Name]`, zero-width characters.

## Format

1. No em dashes, no unicode arrows. Parentheses are fine, semicolons sparingly, quotes straight.
2. Sentence case headings. No emoji. No decorative bold.
3. No inline-header lists that restate the label: "**Performance:** Performance improved".
4. Prose for argument, lists for parallel items.

## Voice

Embody the writer and say the thing in the most true, accurate, and earnest way it can be said: their experience, plainly, with no embellishment and no metaphor.

## First run

The skill works before any personal layer exists: the rules and vocabulary apply in full, and `proofread.py` reports the voice comparison as dark instead of failing. Never ask the user to copy files anywhere.

When `references/reference-writing/` has no samples or `style.md` is empty, offer once to set them up, and run the same flow whenever the user invokes `/unspeak-init` (its own skill, in the sibling folder `unspeak-init/`): ask the user to paste two or three pieces of their own writing, or name files or links you can read. You create the register files, wrap the text in the `<!-- verbatim -->` markers, fill the frontmatter, run `proofread.py` on a sample, write their `VOICE.md` with `proofread.py --voice-md`, and tell the user which checks came alive. If they decline, keep writing under the general rules and offer again only when they correct your voice.

## Commands

`/unspeak` is for writing only: "/unspeak write about...", "/unspeak this draft", or bare, which applies to the draft in front of you. Setup lives in `/unspeak-init` and list promotion in `/unspeak-add`, separate skills in sibling folders.

## Corrections: how this skill learns

Every correction from the user feeds one of two layers. Allocate it with one test: **would this read as an LLM giveaway in a stranger's text, or is it just not how this author writes?**

1. **General (slop).** The correction would apply to anyone: a tell, a banned word, a structure. Append their version, yours, and the date to `references/candidates.md`. A word cut three times across different documents is a candidate for `vocabulary.md` or a new SKILL.md item.
2. **Personal (style).** Ordinary English the author avoids, a formatting habit, a term of art the vocabulary wrongly flags. Append to the Unconfirmed section of `references/style.md` with the date and the correction.

The user promotes. Never edit `vocabulary.md`, the confirmed part of `style.md`, or this file yourself. Bring candidates clearly and concisely and let them decide. When unsure which layer, put it in candidates.md and say you are unsure. After a promotion or a new sample, rebuild `VOICE.md` with `proofread.py --voice-md`; a normal run says when it is out of date.

A new user starts with an empty `style.md` and their own files in `reference-writing/`. Everything else transfers as is.  
  
Self-audit, think about "What makes this obviously AI generated?" and fix remaining tells.

## Files

- `references/vocabulary.md`: the word lists. Read it and follow it; `proofread.py` reads the same lists to verify, so adding a word needs no code change.
- `references/examples.md`: good and bad.
- `references/style.md`: the user's personal rules, terms of art, and personal vocabulary. Grows from corrections.
- `references/reference-writing/`: the user's own prose, one file per register. Replaceable. See its README.
- `references/VOICE.md`: the user's voice as one file, for any agent or tool without this skill. Same layout and band schema as a Katagami writing style (VOICE.md v3.3-lean, `katagami:voice-bands/v1`): sample excerpts, the confirmed rules from `style.md`, and numbers measured per register. `proofread.py --voice-md` builds it from the files above; never edit it by hand.

