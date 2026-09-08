# Evidence: does the thread actually help an agent?

The cold-agent trial answered *can an agent use this?* It could not answer *does it help?* One agent, one item, no control. This is the record of the controlled version, run 2026-08-31 and 2026-09-01: **163 agent runs, three arms, pre-registered predictions, hidden executable acceptance tests, and a blind grader.** $165.69 and 11.7 agent-hours of machine time.

The question it was built to answer, in the words it was asked: *do we have any evidence the thread ever really helped an AI agent execute a request, or is all the help for humans?* Before this ran, the honest answer was no measured evidence and one anecdote. It is no longer no, and the shape of the yes is narrower and more interesting than the marketing instinct would have written.

## Setup

A Java/Spring insurance codebase with a 36-row registry, snapshotted into three arms that differ **only** in how much thread is present:

| arm | registry, manifest, `@covers`, Gate | prose spec pointers in source | `specs/` |
| --- | :-: | :-: | :-: |
| **THREADED** | yes | yes (35 files) | yes |
| **AS-DEPLOYED** | no | yes (35 files) | yes |
| **STRIPPED** | no | no | yes |

AS-DEPLOYED is the honest middle: what a careful team has before it adopts anything, javadoc pointers to specs and nothing machine-checkable. Keeping it in the design is what makes the result a dose response rather than a two-way comparison against a strawman.

Every arm is a `git archive` snapshot with an identical git surface (one branch, one commit, one tag) so nothing leaks through the object store. `specs/` is present in all three, pinned to one commit. All three build green at 35 tests. Agents got an identical prompt template with a plain-prose ticket: no mention of registries, IDs, threads, or SpecAssay, in any arm. The harness could not tell the agent which condition it was in, because there was nothing in the harness to tell.

Two instruments graded every run:

- **Hidden executable acceptance oracles.** JUnit tests written from the spec criteria *before any run*, frozen with the rubrics, validated against the pristine snapshot so a vacuous pass was impossible, and never shown to any agent in any arm. This is ground truth.
- **A blind LLM rubric.** Scrubbed diff bundles, arm identity removed mechanically, sealed id-to-cell map. This is the instrument most teams actually reach for.

## Result 1: on a task that turns on stated intent, the thread won outright

Ticket: flood-zone disclosure on a home quote. The behaviour depends on what the business promised, and one criterion (refer the prospect to a separate flood policy) cannot be inferred from any code in the repository. Eight runs per arm, scored by the hidden oracle:

| arm | oracle score |
| --- | ---: |
| **THREADED** | **1.000 ± 0.000** |
| AS-DEPLOYED | 0.667 ± 0.282 |
| STRIPPED | 0.396 ± 0.086 |

Threaded minus stripped: **+0.604**, exact permutation p = 0.000155, **p = 0.0019 after Bonferroni** over all twelve contrasts, Cliff's δ = **+1.00**. Complete separation: every threaded run beat every stripped run. The dose ordering held, threaded above as-deployed above stripped, exactly as pre-registered.

**It did not generalise, and the report says so.** Of five scoreable tasks, one moved. Two were aggregate nulls, one was a pre-registered null that behaved as predicted, one failed as an instrument and was excluded, and a sealed holdout task opened afterward was also an aggregate null. The effect is real, replicated in mechanism, and **task-shaped**: it lives where the answer has to be looked up rather than inferred.

## Result 2: agents consult the thread exactly when the task needs it

n = 120, no exceptions. Whether the agent opened a spec feature file at all:

| | THREADED | AS-DEPLOYED | STRIPPED |
| --- | :-: | :-: | :-: |
| tasks with a promise at stake | 8/8 each | 8/8 each | **0/8 each** |
| tasks with no promise | **0** | **0** | **0** |

Registry content entered the agent's context in 32 of 32 threaded runs on promise-bearing tasks and 0 of 56 everywhere else, including zero threaded runs on the task with nothing promised. The agent did not read the registry because it was there. It read the registry because the ticket turned on something only the registry recorded, and skipped it otherwise.

Unprompted, and with nothing in the prompt suggesting it, threaded runs authored `@covers` marks in 20 of 32 runs and proof-grammar test names in 31 of 32. No control run did either. **The practice is legible enough from the artifacts alone that a cold agent picks it up and continues it.**

## Result 3: without a pointer, agents produce a confident near-miss

This is the finding with the most carry, and it was pre-registered as a distinct metric. When a ticket pins an exact quantity or wording, where does the agent get the number?

Two routes to the same wrong answer:

- **It borrows.** On a threshold-and-window task the stripped arm took its values from a nearby local analogue in 69% of cases (threaded 28%, as-deployed 25%). All eight stripped runs used a neighbouring rule's "more than 2 in the past 3 years" instead of the promised "2 or more during the current term", and all eight reused an existing 45-day window instead of the promised 60 days.
- **It invents.** On the holdout task, exact denied-state wording: threaded 0.500, as-deployed 0.375, **stripped 0.000**. Not one stripped run produced the pinned string. All of them wrote defensible English that was not what was promised.

Borrowed or invented, the output is fluent, plausible, review-friendly, and wrong in exactly the place the business cared about. **This is what a missing thread costs, and it is not visible as an error.**

## Result 4: the AI reviewer could not tell fluent from correct

Reported here as a first-class result, because it governs how every other number should be read, including these ones.

Across the 84 runs carrying both instruments, the blind LLM rubric and the executable oracle **were uncorrelated: Pearson r = −0.031.** The rubric over-credited by +0.131 on average. Of the 40 runs the oracle called broken, **the rubric called 29 of them excellent — 72.5%.** As a share of everything graded, 29 of 84 runs (35%) were broken work called near-perfect.

Those failures **cluster hard, and not where you would hope.**

- **By condition: no signal** (permutation p = 0.52). The reviewer was about equally deaf on threaded work as on stripped work. Having a thread does not make a model reviewer more reliable.
- **By task and break type: strong** (permutation p = 0.0016). Rates ran from 100% to 0%.

Sorting the individual acceptance criteria by how often the reviewer missed a genuine failure produces a clean line:

| defect the tests caught | reviewer missed it |
| --- | ---: |
| a scheduled notice that never fires at all | 17/17 (100%) |
| a required referral simply absent | 6/6 (100%) |
| behaviour present but unconditional | 11/13 (85%) |
| state correct in memory, lost on save | 11/13 (85%) |
| wrong branch taken (declined instead of issued) | 0/16 (0%) |
| wrong string where exact wording was pinned | 0/16 (0%) |

**The reviewer sees what is written and cannot see what is missing or what only exists at runtime.** Wrong words and wrong branches are in the diff. Omissions, unconditional behaviour, non-persistence, and jobs that never fire are not.

The misses were not marginal calls. Of the 29 false positives, 22 failed exactly three acceptance criteria and 6 failed four, while most correctly-scored runs failed none.

**This is the receipt for a design decision SpecAssay had previously only asserted: the Gate is deterministic on purpose.** A Gate that asked a model whether the thread held would have passed most of the broken work in this experiment. Row states move on parsed marks, named proofs, and exact-set registry checks because those are checkable, and "does this look right" measurably is not. The three questions a diff cannot answer, and an executable proof answers for free, are *did it fire*, *only when it should have*, and *is it still there after a save*.

## Honest caveats

The limits are the credibility. All of them:

- **One estate.** One Java/Spring repository, 36 registry rows, one Gate configuration. Nothing here transfers to a large codebase without being re-measured, and a small registry is the pre-registered reason to expect small effects on navigation cost.
- **One model, on both sides.** Every worker run and every rubric grade was Claude Sonnet 5. The reviewer finding is a finding about *this* model reading diffs, not about LLM review in general, and worker and grader sharing a family is a real confound.
- **Two days.** 2026-08-31 and 2026-09-01. Model behaviour moves; these numbers have a shelf life.
- **A snapshot, not a project.** Cold agents on frozen twins for a single ticket each. This measures pickup, not the compounding cost of maintaining a thread over months, which is the thing practitioners most want to know and this design cannot see.
- **One task in five moved.** The aggregate effect is not general. Reporting F1 without that sentence would be a misuse of it.
- **Task and break type are confounded** in Result 4. Each task contributed one bundle of criteria, so "blind to omissions" and "lenient on that task" fit the data equally well. Two within-task splits favour the break-type reading and both rest on single-digit counts. **The sample is too thin to call it.**
- **No speed claim.** A secondary efficiency analysis was exploratory and post hoc. It found the threaded arm cost no more effort than no thread at all while buying accuracy, and the pointers-only arm paid for its ambiguity in wandering. That is an economics observation on one task, not a benchmark.
- **Agents, not humans.** This says nothing about whether the thread helps people, which was never in doubt and was never tested here.
- **A known imperfection, left in.** One manifest row in the threaded arm cites a path that had moved. It was found mid-battery and deliberately **not** patched, because the protocol was frozen and patching would have broken poolability. It biases against the threaded arm, which is the safe direction.

**The narrative version**, written for a general audience rather than this one, is Field Note 05 on dryfoos.com: [**Fluent and Wrong**](https://dryfoos.com/field-notes/fluent-and-wrong/).

## Where the records are

Held in the experiment room, not in this repository: the pre-registered protocol, four dated amendments, five recorded caveats, the sealed holdout terms, the frozen rubrics and hidden tests, every run directory with transcript and diff and oracle output, and the analysis scripts that regenerate every number above from those records. `RESULTS-final.md` is the consolidation; `APPENDIX-reviewer-clustering.md` is Result 4 in full.

The pilot that shook the harness out (19 runs) is reported separately and **is not pooled** with the battery, because a protocol amendment landed between them.
