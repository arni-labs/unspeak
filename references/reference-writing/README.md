# Reference writing

Your own prose, used two ways: as the target the proofreader compares a draft
against, and as the thing to read when you need to know what good looks like
here rather than in general.

## Adding your own

Drop a `.md` file in this directory. Wrap your text in the markers below, and
put nothing of your own outside them. `proofread.py` reads only what is between
them, so notes, frontmatter, and commentary never contaminate the measurement.

```
<!-- verbatim -->
your writing
<!-- /verbatim -->
```

## What to put in

Small and clean, not large and mixed. A few hundred words you would defend
sentence by sentence do more for the corpus than ten thousand of anything else.

- Keep one file per register. Technical prose, a blog post, and a short social
  post are three different registers, and averaging them produces a target that
  matches none of them. Name the register in the frontmatter.
- Exclude anything an LLM touched, including drafts you edited rather than
  wrote. A reference that has already absorbed the patterns cannot detect them.
- Prefer published or deliberately written prose. Dictated text carries
  stutters, repetition and transcription errors, and it is a different register
  from writing: it uses a smaller vocabulary and shorter clauses, which moves
  every distribution measured here. Chat logs are the worst source, because most
  of what sits in them was pasted rather than composed.

## Size

Vocabulary and sentence-length checks work from the first file. Distribution
checks stay dark below 2,000 words, and `proofread.py` reports the current
count and which checks are live.
