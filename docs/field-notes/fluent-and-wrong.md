# Fluent and Wrong

*Field note, September 2026. What happened when we stopped asking an AI whether the work looked right and started asking whether it ran.*

Every argument we had for keeping a traceability thread was an argument about people. Humans read the registry, humans follow the pointers, humans stay oriented. Fine. But most code now is written by agents, so the uncomfortable question is whether the thread ever helps the machine, or whether all of the help is for us.

## The design, in four sentences

We took one Java codebase and cut three copies that differ only in how much thread is present: one with the full apparatus, one with informal prose pointers to specs and nothing machine checkable, and one with neither. We wrote the acceptance tests first, from the specifications, froze them, and never showed them to any agent in any arm. We handed cold agents an ordinary plain prose ticket with no mention of registries, IDs, or traceability, ran 163 of them, and graded every result twice: once with those hidden executable tests, and once with a blind AI reviewer reading only a scrubbed diff. Predictions were written down before the first run.

The second grader was meant to be a convenience. It became the finding.

## The number we went looking for

On a task turning on what the business actually promised, the threaded arm was right every time and the thread free arm was right less than half the time.

| what the agent had | acceptance score, 8 runs each |
| --- | ---: |
| the full thread | 1.000 |
| informal prose pointers only | 0.667 |
| no thread at all | 0.396 |

Complete separation: every threaded run beat every thread free run, a gap of 0.604 that survives correction for twelve comparisons.

Now the sentence that has to follow it. Of five scoreable tasks, one moved. The effect is real and narrow, and it lives where an answer has to be looked up rather than worked out. We also logged when agents went to read the spec at all, and across 120 runs the pattern was perfect: where something had been promised, agents in both pointer bearing arms opened the spec 8 times out of 8 and thread free agents opened it 0 times out of 8; where nothing had been promised, nobody opened anything in any arm. Agents do not read documentation because it exists. They read it when the ticket turns on something only the documentation knows.

## What happens when there is nothing to look up

An agent asked for a rule with a specific threshold, and given no way to find the promised one, does not stop and ask. It finds a nearby rule that resembles the request and quietly adopts that rule's numbers. All 8 thread free runs on one task took a neighbouring rule's "more than 2 in the past 3 years" instead of the promised "2 or more during the current term", and all 8 reused an existing 45 day window where 60 was promised.

With no neighbour to borrow from, it invents. On a task requiring an exact piece of customer facing wording, 0 of 8 thread free runs produced the pinned phrase. All 8 wrote reasonable English that was not what the business had committed to.

Borrowed or invented, the result is the same: code that compiles, passes its own tests, reads well in review, and is wrong in exactly the place the business cared about. Nobody wrote a bug. Somebody answered a question they could not look up.

## The finding we did not go looking for

Across the 84 runs graded by both instruments, the AI reviewer's scores and the executable tests' scores were uncorrelated. Pearson r was minus 0.031. Not weak. Unrelated.

Of the 40 runs the tests called broken, the reviewer called 29 of them excellent, 72.5%. Against everything it graded, 29 of 84 runs, or 35%, were broken work scored near perfect. These were not close calls: of those 29, twenty two failed exactly three acceptance criteria and six failed four, while most correctly scored runs failed none.

## Where the reviewer is deaf

The useful question is whether the failures cluster, because if they do, a deterministic check knows where to stand. They cluster, and not where you would guess.

Not by condition. The reviewer was about equally unreliable on threaded and thread free work, p equals 0.52. Good documentation does not make a model better at reading your diff.

By kind of defect, hard, from 100% missed to 0% missed, p equals 0.0016:

- A scheduled notice that never fires at all: missed 17 of 17.
- A required referral simply absent: missed 6 of 6.
- Behaviour present but firing unconditionally instead of only in the right case: missed 11 of 13.
- State correct in memory and lost on save: missed 11 of 13.
- The wrong branch taken, declining where it should have issued: missed 0 of 16.
- The wrong string where exact wording was pinned: missed 0 of 16.

The rule falls out. The reviewer sees what is written and cannot see what is missing or what only exists at runtime. A wrong word is in the diff; a wrong branch is in the diff. A job that never runs, a check that never applies, a field that never survives a save: none of those have a diff hunk, and a reader looking at code cannot see an absence.

The weakest joint, stated plainly: each task contributed one bundle of defect types, so "blind to absences" and "lenient on that task" fit the numbers about equally well. Two comparisons inside a single task favour defect type, and both rest on single digit counts. The sample is too thin to settle it. What is settled is that the failures cluster somewhere sharp, and that condition is not where.

## Why our Gate stays deterministic

People ask, fairly, why we do not just have an AI look at it. This is why. A Gate that asked a model whether the thread held would have waved through most of the broken work in this experiment, confidently, in fluent prose. The three questions worth spending determinism on are the three a diff cannot answer: did it fire, did it fire only when it should have, and is it still there after a save.

## Limits

163 agent runs on one Java and Spring codebase with a 36 row registry, run 31 August and 1 September 2026. Every worker run and every review was Claude Sonnet 5, so the reviewer finding is about that model reading diffs rather than AI review in general, and grader and worker sharing a model family is a real confound. These were cold agents taking a single ticket each on a frozen snapshot, which measures pickup and says nothing about what maintaining a thread costs over months. One task in five moved, and quoting the winning task without that sentence would be a misuse of it. Nothing here is a claim about speed, and nothing here is a claim about humans, who were never in doubt and were never tested.

The full record, the pre registered predictions, the amendments, the caveats we recorded against ourselves, and the scripts that regenerate every number above are kept with the experiment.

*Rik Dryfoos*
