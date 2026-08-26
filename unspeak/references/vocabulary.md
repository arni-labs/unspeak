# Vocabulary

Read this list and do not use these words. They are abstract, metaphorical,
and out of place where LLMs put them, and each use displaces the word that
would express the meaning accurately in that context. A word here is allowed
only when no other word truly expresses the required meaning.

This file is for you, the writing agent, first. `proofread.py` reads the same
`words` blocks as a second pass, to catch what you missed. It is not the
mechanism. Adding a word needs no code change. Three blocks sit apart from the
main list because the script treats them differently, not because the words
differ in kind.

## Words

```words
load-bearing, earn its keep, pay for itself, belt and suspenders, seams, rung,
the unlock, honest take, moving the needle, the long pole, heavy lifting,
table stakes, north star, sharp edges, happy path, blast radius, on the hook,
shape, surface, substrate, wedge, vector, locus, nexus, primitive, harness,
bedrock, scaffolding, modality, paradigm, flywheel, endgame, gold-plating,
ratchet, lens, axis, spine, backbone, fabric, tapestry, landscape, realm,
ecosystem, journey, roadmap, cornerstone, linchpin, crucible, gateway,
currency, worth, state, matters, fire, reach for, reaches for,
govern, governed, governs, the best part, stay put, come and go, comes and goes,
here's what, still early, we're early, beats, verbatim, centerpiece, gauntlet, bolted,
panel, not perfect yet, isn't perfect yet, rather than, arm, arms,
land, lands, landed, landing, each one, the easy part, the hard part,
no one, no single, just one, single,
bucket, buckets,
bolt on, spin up, spins up, spun up, belongs, belong,
coin, gate, architect, onboard, action, gift, medal, sunset, greenlight,
delve, testament, pivotal, crucial, robust, seamless, leverage, utilize, foster,
underscore, showcase, vibrant, intricate, myriad, plethora, paramount, holistic,
meticulous, garner, interplay, elevate, unlock, embark, beacon, nestled,
groundbreaking, renowned, breathtaking, cutting-edge, game-changer,
ever-evolving, multifaceted, transformative, nuanced, navigate, resonate,
streamline, empower, bolster, spearhead, catalyze, illuminate, cultivate,
galvanize, augment, encompass, quintessential, burgeoning, nascent, poised,
overarching, daunting, thriving, bustling, actionable, impactful, learnings,
synergy, best practices, thought leader, deep dive, unpack, comprehensive,
serves as, stands as, boasts, features, represents, marks, presents, embodies,
symbolizes, speaks to, reflects broader,
it is important to note, it is worth noting, in order to, due to the fact that,
at the end of the day, when it comes to, at its core, in today's,
the reality is, in terms of, going forward, that being said, worth noting,
worth your, worth a look, has the ability to, needless to say,
suffice it to say, in a world where, more than ever, let's dive in,
let's explore, let's break this down, here's what you need to know,
in conclusion, in summary, make no mistake, let that sink in, full stop,
the real question is, here's the thing, plot twist, what if I told you,
the catch, the kicker
```

## Physical verbs on abstract subjects

Apart because these are correct with a concrete subject. The script flags them
only when the subject is abstract.

```words
survive, hold, carry, sit, live, rest, stick, bear, weather, ride, hang,
lean, anchor, thread, plumb, bake, wire, keep, reach
```

## Chatbot residue

Apart because these are not word choices. They are leftovers from a chat
interface and always come out.

```words
great question, excellent point, you're absolutely right, that's a great,
i hope this helps, let me know if, would you like me to, want me to,
should i continue, of course!, certainly!, as of my last update,
up to my last training update, while specific details are limited,
based on available information, let me think, breaking this down,
to answer your question, you're asking about, i'd be happy to
```

## Absence words

Apart because an absence is information only when someone was checking. The
script flags these only as the subject of a claim and skips ordinary determiners.

```words
nobody, nothing, everything, anything, everyone, none, never, always
```

## Spared phrases

Literal uses of banned words. A hit inside one of these phrases passes.

```words
landing page, landing pages, s3 bucket, s3 buckets, storage bucket,
storage buckets, gcs bucket
```

## Structural nouns

Apart because this is a carve-out. `load-bearing` directly
before one of these is construction terminology and passes.

```words
wall, beam, column, joist, truss, girder, rafter, footing, slab, lintel, stud,
partition, masonry, pier, member
```
