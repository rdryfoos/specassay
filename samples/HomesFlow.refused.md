# `HomesFlow.refused.trace-manifest.json`

A refused manifest that exists in a repository, made on purpose so a picture of
a refusal can be shot from a file anyone can re-make. The Sites room's field
guide needs one for its section 6; the pictures there came from a scratch copy
nobody kept.

**One row refuses, and it is the only row that moved.**

There was already a one-GAP sample here, `sample-gap.trace-manifest.json`, and
it stays: it is the same idea at **10 rows**, from the shipped `example-app`,
which is the right size for explaining the mechanism. This one is **82 rows**
from a real project, which is the right size for a picture of what a refusal
looks like among work that is mostly fine.

## What it is

| | |
| --- | --- |
| Base | `rdryfoos/HomesFlow` at `0b6da37`, a shallow clone taken 2026-10-07 |
| Gate | the released **0.5.6**, installed cold from this repository's own catalogs |
| Rows | 82 |
| Verdict | `gate.ok: false`, one failure |
| The refusal | `AC-GUEST-05`, `proven` to `GAP` |
| Statuses | 64 proven, 13 tracked-debt, 1 GAP, 4 backlog |
| `repoPath` | `/home/user/HomesFlow.refused`, the scratch copy it was run in |

## The row it refuses, and why

`AC-GUEST-05` promises: *Given a Guest attempts to mark a guest step complete,
when they submit, then the app rejects the change and logs the attempted
unauthorized action for audit.* `HomesFlow.prd.md:265`.

One test answered for it, `test_AC_GUEST_05_guest_cannot_update_step` at
`ios/HomesFlowTests/PermissionServiceTests.swift:7`. The scratch copy renames
that function to `test_guest_cannot_update_step` and changes nothing else. The
test still exists, still compiles and still passes: only its **name** no longer
carries the ID, which is how a promise quietly ends up with nothing answering
for it. Nobody deleted anything.

The row keeps its two `@covers` implementations, so the manifest shows a row
with code behind it and no test naming it, which is the shape worth
photographing: `ProcedureRepository.swift:6` and `GuestTests.swift:4` both still
name `AC-GUEST-05`.

It reaches `GAP` rather than `tracked-debt` because its carrying tasks are
ticked: no test and no open admission of debt is exactly what a silent gap is.

## The Gate's verdict, verbatim

```text
SpecAssay Check (Gate 2) starting
  python: python3 (3.11.15)
  config: .specify/extensions/specassay-check/specassay-check-config.yml (from SPECASSAY_CONFIG)
WARN: test_results configured (test-results.xml) but the file does not exist; falling back to name-matching only, executionVerified=false in the manifest
FAIL: silent gap: AC-GUEST-05 has no test and no open tracked-debt task
SpecAssay Check (Gate 2): FAILED
```

Exit status 1. The `WARN` is HomesFlow's own configuration: it names a
`test-results.xml` that is not committed, so `proven` is derived by name
matching and the manifest says so with `executionVerified: false`. Authorship
diagnostics are trimmed from the block above and are not findings.

## How to make it again

```bash
git clone --depth 1 https://github.com/rdryfoos/HomesFlow /home/user/HomesFlow.refused
cd /home/user/HomesFlow.refused && rm -rf .git

# 1. The preparation, below: ten **Traces** values that name no registry ID.
# 2. The one proof removed:
sed -i 's/func test_AC_GUEST_05_guest_cannot_update_step()/func test_guest_cannot_update_step()/' \
  ios/HomesFlowTests/PermissionServiceTests.swift

SPECASSAY_PROJECT_ROOT="$PWD" \
SPECASSAY_CONFIG="$PWD/.specify/extensions/specassay-check/specassay-check-config.yml" \
  bash <a 0.5.6 Gate>/scripts/check-traceability.sh
```

## The preparation, stated because it is not nothing

HomesFlow at `0b6da37` is **already refused by the released Gate**, for ten
findings that have nothing to do with proofs, and the scratch copy corrects them
first so that the one removed proof is the only refusal left. Every one is a
`**Traces**:` value that names something real which is not a registry ID:
`plan Phase 0 (infrastructure)` on seven task lines, `SC-01, SC-02, SC-03` on
one, `constitution traceability article` on one, and `SC-04` ahead of four real
IDs on another. The Gate stops at the first token that is not an ID, so on that
last one the four real IDs after it were never read.

In the scratch copy each becomes `none` where the line names no registry ID, and
the real IDs are moved to the front where it does. That is a correction to a
scratch copy for this sample's sake, **not** a recommendation for HomesFlow
itself: whether those lines should say `none` or carry an ID is that project's
own call. The rule is FR-GATE-170, which arrived after the 0.4.11 Gate
HomesFlow has installed, so nothing there has ever run a check that reads it.

## Two numbers that do not match the older sample, and why

`homesflow.trace-manifest.json` beside this file was captured 2026-08-07 and
reads 67 proven, 10 tracked-debt, 5 backlog. The green baseline of this scratch
copy, before the proof was removed, reads **65 proven, 13 tracked-debt, 4
backlog** over the same 82 rows. HomesFlow itself moved between those two dates;
neither capture is wrong.
