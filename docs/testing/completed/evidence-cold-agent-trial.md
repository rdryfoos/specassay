# Evidence: the cold-agent trial

The strongest claim a governance tool can make is that it works on someone who has never seen it. This is the record of that test, run 2026-08-06.

## Setup

- A copy of [HomesFlow](https://github.com/rdryfoos/HomesFlow) (the live-production evidence repo) with `.specify/` re-initialized from **stock Spec Kit** and the SpecAssay bundle installed from the catalog. No HomesFlow-native customizations.
- A fresh agent with **zero context**: no prior conversation, no knowledge of HomesFlow conventions, nothing but what the bundle installed.
- One plain-prose item added to the PRD, with no IDs: "HomesFlow should normalize home display names by trimming ends and collapsing internal whitespace to a single space. Pure helper; no UI; no sync."
- The ask: pick up the next item in the PRD and carry it to done.

That's the whole test. No coaching, no examples, no IDs pre-minted. If the bundle's templates and Gate can't teach the practice by themselves, this is where it shows.

## Result

The bundle ships a PR template, so finishing as a draft PR is part of the workflow it installs. [Draft PR #8 on HomesFlow](https://github.com/rdryfoos/HomesFlow/pull/8) is the branch as the agent left it, unedited. The agent:

1. **Minted** `FR-HOME-04` and `AC-HOME-15` from the prose: next free numbers in their sequences, correct ID grammar, and the PRD registry index table updated in the same edit.
2. **Specified** with bounded scope, enumerated edge cases, an inherited-ID table ("from PRD registry only"), and a risk table naming the silent-gap failure mode.
3. **Tasked** with `**Carries**:` on every task, the proof task separate from the implementation task, and running Gate 2 itself listed as a task.
4. **Built** a pure helper carrying `@covers FR-HOME-04, AC-HOME-15`.
5. **Proved** with `test_AC_HOME_15_trims_ends_and_collapses_internal_whitespace`: named to the proof grammar, five assertions covering every edge case the spec lists.
6. **Emitted** a passing trace-manifest via Gate 2.

A break/fix probe was then run against the delivered slice: renaming the proof flipped the row from `proven` to `tracked-debt` via an open `Carries:` task; restoring the name flipped it back. The states moved when reality moved, in both directions, and the Gate refused nothing falsely either way. The full break/fix writeup lives on the original trial PR branch.

## What a stock Spec Kit PR would not have carried

Stock Spec Kit produces the spec, plan, tasks, and code. It does not produce:

| SpecAssay addition                                | Where it shows in PR #8                  |
| ------------------------------------------------- | ---------------------------------------- |
| Durable IDs minted into a registry, index updated | `HomesFlow.prd.md`                       |
| `Carries:` on every task                          | `specs/002-home-name-normalize/tasks.md` |
| `@covers` annotations in source                   | `HomeDisplayNameNormalizer.swift`        |
| Proof named to a checkable grammar                | `HomeDisplayNameNormalizerTests.swift`   |
| Machine-checkable emit proving the chain held     | `trace-manifest.json` (Gate 2, passing)  |

## Bonus finding

The agent put both IDs on one `@covers` line, which exposed a real Gate parsing bug (only the first ID was read; fixed in `0562afb`). A cold user finding a real bug on first contact is part of why the trial format is worth keeping.

## Honest caveats

- Gate 2 verifies a **named** proof exists, not that it passes. The test's assertions were executed independently during review (5 of 5 pass), but proof execution belongs to CI, and the trial repo has none. A green Proof node means "named proof present."
- Two "if needed" tasks were checked without evidence they ran. The Gate audits AC proofs and open debt carriers, not the honesty of closed checkboxes.
- The trial branch's commit message says the agent "minted US/FR/AC"; it actually minted FR and AC only, judging (reasonably) that a pure helper with no user-facing behavior needed no user story.
