# Examples

Bad and good. Both sides are quoted so `proofread.py` skips them.

These teach the pattern, never the words. Reusing an example's wording in output
is a defect, and the leak check flags any five consecutive words taken from a
good side.

## Pairs

**Buried verb**
Bad: "publishing only the flattering one is the behavior this project exists to criticize"
Good: "We criticize publishing only the good ones, so we publish both."

**Buried verb**
Bad: "What this migration does is reduce the auth layer."
Good: "This migration reduces the auth layer."

**Non-literal predicate**
Bad: "The cache had a correctness problem that survived every release."
Good: "We never fixed the correctness problem in the cache."

**Borrowed idiom**
Bad: "encode at the strongest rung that fits"
Good: "encode at the strongest that fits"

**Metaphor noun**
Bad: "reduce the surface area of the auth layer"
Good: "remove three of the five auth entry points"

**Moral adjective on a non-agent**
Bad: "a more honest shape for the data"
Good: "a curve that matches the measurements"

**Decorative number**
Bad: "We edited 7 cars out of the frames."
Good: "We edited the cars out."

**Performed precision**
Bad: "One conflict worth your call."
Good: "This needs a decision."

**Non-event**
Bad: "Median latency went up by 3 milliseconds. Nobody has complained."
Good: "Median latency went up by 3 milliseconds."

**Staged narration**
Bad: "A customer revoked access and then watched the old answer come back."
Good: "The cache served a revoked grant for up to 60 seconds."

**Chopped sentences**
Bad: "It had no preference for symmetry. No aesthetic prior. No nostalgia for human taste."
Good: "It did not favor symmetry or human-looking designs."

**Binary contrast**
Bad: "The question isn't the model. It's the eval."
Good: "The eval matters more than the model."

**Procedural filler**
Bad: "That is a larger change than this one and it needs a design review first."
Good: cut.

**Relative-clause title**
Bad: "## The word that cannot be wrong"
Good: "## Metaphor verbs"

**Superficial -ing clause**
Bad: "The launch adds file search, highlighting the team's commitment to workflows."
Good: "The launch adds file search, so users find old drafts without leaving the editor."

**Significance inflation**
Bad: "The launch marks a pivotal moment for the company."
Good: "The launch is the company's first paid product."

**Vague attribution**
Bad: "Experts believe it plays a crucial role in the ecosystem."
Good: cut, or name the expert.

**Copula avoidance**
Bad: "Gallery 825 serves as the exhibition space and boasts 3,000 square feet."
Good: "Gallery 825 is the exhibition space. It has 3,000 square feet."

**Diff-anchored writing**
Bad: "This function was added to replace the previous approach of iterating."
Good: "This function uses a hash map for O(1) lookups."

**Fake-profound kicker**
Bad: "The future isn't coming. It's already here."
Good: cut. End on the last concrete sentence.

**Narrated candor**
Bad: "Two caveats I would rather flag than let you discover later: X and Y."
Good: "Two caveats: X and Y."

**Unfalsifiable closer**
Bad: "This may become one of the most important trends of the next cycle."
Good: "This may exceed spot pricing for parallel workloads by 2027."

## From the bake-off review

The user rewrote or rejected these from this skill's own output. Their wording
where quoted.

**Superlative claim**
Bad: "My throughput has never been higher."
Good: the specific or honest claim, "I ship more PRs than I did in December."

**Setup before the point**
Bad: "Done means more than passing tests. Done means the agent built it..."
Good: "For something to be done, the agent has to build it, start it, click through the changed flow, and curl the endpoints."

**Consequence tail**
Bad: "Those credentials expire the moment the task ends, so there is no persistent credential to exfiltrate."
Good: "Those credentials expire the moment the task ends."

**Owned abstraction**
Bad: "Every repo I own carries its own contract."
Good: "Every repo includes a distilled AGENTS.md, a verify skill, and a REVIEW.md."

**Non-literal predicate, and restructuring instead of patching**
Bad: "The machine keeps what it has learned across tasks; tools and context persist even as instances come and go."
Good: "The agent can create new tools while working on a task, and they are saved in Temper and available on all new instances."

**Trailing participle**
Bad: "Decisions get recorded at the moment they're made, never reconstructing one afterwards."
Good: "Decisions get recorded at the moment they are made."

**Ending without the wrap**
Bad: "The old loop is still here, in a different form. ... And the gains come from delegating better rather than typing faster."
Good: "The loop has changed. I define intent, review decisions, and curate rules. The agents implement, verify, deploy, and prove it works."

**Closing paragraph, personal restatement (from the bake-off, cursor unslop's output, reworded by the user)**
Bad: "The traditional dev loop hasn't disappeared. It's been transformed. ... And that future isn't coming. It's already here."
Interesting but off: "The step that used to be mine belongs to something else."
Good: "Most steps that I used to do are done by something else now. I decide what should exist and judge whether I like the answer, and that seems to actually be the part that I wanted to be doing."
