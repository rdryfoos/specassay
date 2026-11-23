# The objective tier, in a manifest you can read

`objective-tier.trace-manifest.v5beta.json` is the v5 manifest a real Gate run
emitted for the sample project in `objective-tier/`. It is here so the tier can
be read rather than described: three objective rows, a story whose first parent
is an objective, a requirement serving two of them, and a criterion with a real
passing test underneath.

## How it was made

Everything in `objective-tier/` is invented. There is no night-walking app, and
nothing in the sample is copied from any real project's case or registry.

```bash
SPECASSAY_PROJECT_ROOT="$PWD/samples/objective-tier" \
SPECASSAY_CONFIG="$PWD/samples/objective-tier/specassay-check-config.yml" \
  bash extensions/specassay-check/scripts/check-traceability.sh
```

Run from the repository root, with the extension in this working tree. The
verdict, verbatim:

```
Wrote trace-manifest.v5beta.json (7 rows, schemaVersion 5, beta)
Wrote trace-manifest.json (4 rows) gate.ok=True
SpecAssay Check (Gate 2): OK (4 registry IDs)
```

Seven rows in v5 and four in v4: the three objective rows live in the v5 file
only, because v4 is a frozen contract. The project's own emitted manifests are
git-ignored like every other project's; the copy committed here is the one
with the sample's name on it.

## What to look at

**The walk this tier exists for.** Start at `AC-WALK-01`, whose `proofs` names
the real test, and follow the first entry of `parents` at each hop:

```
AC-WALK-01  ->  FR-WALK-01  ->  US-WALK-01  ->  OBJ-WALK-10
criterion       requirement     intent          objective
```

Before this change the walk stopped at `US-WALK-01`, because the row above a
story had nowhere to live.

**The first parent is the next tier up.** `US-WALK-01`'s parents are
`["OBJ-WALK-10"]`: for a story the next tier up is its objective.
`FR-WALK-01`'s are `["US-WALK-01", "OBJ-WALK-10", "OBJ-POWER-10"]`: the row
above it in the document first, and the two objectives it also serves riding
after, so a walk cannot jump the story tier. The order is load-bearing, not
cosmetic.

**More than one objective on one row.** `FR-WALK-01` declares
`**Serves**: OBJ-WALK-10, OBJ-POWER-10`. That is the cross-cutting shape the
list spelling of `parents` was drafted for in v5 and never had an emitter for
until now.

**The colour rule, rolled up.** `OBJ-WALK-10` reads `proven` and carries
`rollup: {rows: 3, proven: 1, backlog: 2, ...}`: the weakest *started* status
beneath it is `proven`, and the two planning-altitude rows are counted without
being coloured. `OBJ-POWER-10` has no story serving it and reads `backlog`
with no rollup at all. The rule is stated in full in
`docs/trace-manifest-v5.md`.

**Where an objective comes from.** Each objective row's `origin` is
`{"kind": "case-line", "path": "CASE.md", "line": N}`. Objectives are not
registry rows; they are defined in the case, which is why `statusCounts` still
counts the registry's four rows and `totals.objectiveCount` says there are
three more.

## What this sample does not show

The IDs in `CASE.md` were typed by a hand. `FR-CASE-10` says the Gate assigns
them and writes them back into the case, and that half is not built: it is
still carried by `T929`. Nesting a story under an objective as a second
citation form (`AC-CASE-30b`) is not built either, so every edge here is a
declared `Serves`.

The sample is green, so it shows neither refusal. Both are in
`extensions/specassay-check/tests/test_case_objective_tier.py`: a story naming
an objective the case does not define turns the run red, and a story serving
nothing is counted and reported until a project sets `block_orphan_story`.
