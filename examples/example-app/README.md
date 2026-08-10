# Collaborative Lists — a worked SpecAssay example

A tiny, genuinely-runnable "collaborative lists" app (a shared to-do/notes app
with device sync, offline support, inline edit, accessibility, and a perf
requirement). It exists as a **worked example + practice playground** for
Spec Kit + SpecAssay: a real, self-contained project whose Golden Thread —
intent → build → proof — is hallmarked by **Gate 2** (the SpecAssay Check), and
which emits a clean `trace-manifest.json`.

Everything is intentionally small. The point is not the app; it is the
*traceability shape*: durable IDs minted once in the PRD, inherited by specs and
tasks, served by `@covers` marks in source and `test_AC_*` proofs in tests, and
checked as an exact set by the Gate.

## Layout

```
examples/example-app/
├── PRD.md                        # the ID registry: 10 durable IDs + statements
├── specs/
│   ├── sync/spec.md              # sync feature — inherits registry IDs
│   ├── sync/tasks.md             # sync tasks (incl. open tracked-debt TODO)
│   ├── edit/spec.md              # inline-edit feature
│   ├── edit/tasks.md             # edit tasks
│   └── backlog/tasks.md          # anointed-backlog TODO (mints AC-EDIT-01)
├── src/
│   ├── sync.py                   # sync engine — @covers AC-SYNC-01 / AC-SYNC-02
│   ├── edit.py                   # inline edit (commit-on-blur); undo = backlog
│   └── a11y.py                   # keyboard reachability + announcements
├── tests/
│   ├── test_sync.py              # test_AC_SYNC_01_*, test_AC_OFFL_01_*
│   ├── test_a11y.py              # test_AC_A11Y_01_*
│   └── test_edit.py              # commit-on-blur behavior (no undo AC yet)
├── specassay-check-config.yml    # Gate 2 config for this project
└── trace-manifest.json           # emitted Gate output (git-ignored; run the Gate)
```

## Run the tests

From this directory:

```bash
python -m pytest
```

All tests pass. The three `test_AC_*` proofs are what flip the matching
acceptance criteria to **proven** in the manifest.

## Run Gate 2 (the SpecAssay Check) against this project

The check locates its target via `SPECASSAY_PROJECT_ROOT` and its config via
`SPECASSAY_CONFIG`. From the **repository root** (`specassay/`):

```bash
SPECASSAY_PROJECT_ROOT="$PWD/examples/example-app" \
SPECASSAY_CONFIG="$PWD/examples/example-app/specassay-check-config.yml" \
bash extensions/specassay-check/scripts/check-traceability.sh
```

This writes `examples/example-app/trace-manifest.json` and prints
`SpecAssay Check (Gate 2): OK (10 registry IDs)`.

### Expected result

`gate.ok: true`, 0 GAP, and this status split:

| ID | Status | Why |
|----|--------|-----|
| AC-SYNC-01 | **proven** | `@covers AC-SYNC-01` in `src/sync.py` + `test_AC_SYNC_01_*` |
| AC-OFFL-01 | **proven** | `test_AC_OFFL_01_*` (no `@covers` needed) |
| AC-A11Y-01 | **proven** | `test_AC_A11Y_01_*` |
| AC-SYNC-02 | **tracked-debt** | `@covers AC-SYNC-02` in source + open `- [ ] … **Carries**: AC-SYNC-02` task, but no test yet |
| AC-EDIT-01 | **backlog (anointed)** | carried only by the open `- [ ]` TODO in `specs/backlog/tasks.md` — not in any spec, no `@covers`, no test |
| US-SYNC-01, FR-SYNC-01, US-EDIT-01, FR-EDIT-01, NFR-PERF-01 | **backlog** | in specs + tasks (exact-set holds) but no own `@covers`/test — planning altitude |

`statusCounts`: `{proven: 3, tracked-debt: 1, GAP: 0, backlog: 6}`.

## How the statuses are decided (the rules this example demonstrates)

- **Exact-set rule.** The registry IDs (PRD) must equal the IDs referenced in
  `specs/**/spec.md` and in `specs/**/tasks.md`. Specs/tasks may not invent IDs,
  and no registry ID may sit unclaimed — *except* anointed backlog.
- **Anointed backlog.** A registry ID whose **only** carrier is an open
  `- [ ] … **Carries**: <ID>` TODO is legal backlog, not drift. That is
  AC-EDIT-01: it is deliberately absent from every spec and has no `@covers`/test
  — the open TODO is what proves the intent is minted on purpose.
- **Silent-gap check (ACs only).** Every `AC-*` in the registry must have either
  a `test_AC_*` proof or an open tracked-debt TODO. Otherwise the Gate fails.
- **Tracked debt vs. backlog.** An open TODO on an AC that has already *started*
  (it appears in a spec or has a `@covers` mark) is **tracked-debt**
  (AC-SYNC-02). An open TODO on an AC that has **not** started is **backlog**
  (AC-EDIT-01).

## Practice

The whole point of anointed backlog is that the mint is already done for you —
the ID exists in the registry and an open TODO carries it. Your job is the rest
of the Golden Thread: **build it (add an `@covers` mark) → prove it (add a
`test_AC_*` test) → re-run the Gate → watch the status flip.** Pick one:

1. **AC-EDIT-01 — inline-edit undo** *(the obvious first target)*.
   Mint is done (`specs/backlog/tasks.md` T900). Implement `InlineEditor.undo()`
   in `src/edit.py` so it restores the prior committed value in one step, and add
   a one-line `# @covers AC-EDIT-01` mark on it. Write
   `test_AC_EDIT_01_undo_restores_prior_value` in `tests/test_edit.py`. Re-run
   the Gate: AC-EDIT-01 goes `backlog → proven`. (To keep exact-set closed you
   may also promote it from `specs/backlog/tasks.md` into `specs/edit/`.)

2. **AC-SYNC-02 — disjoint-field merge** *(convert tracked-debt to proven)*.
   The `@covers AC-SYNC-02` mark and the merge code already exist in
   `src/sync.py`; only the proof is missing (that is why it reads *tracked-debt*).
   Write `test_AC_SYNC_02_disjoint_edits_merge` proving two devices editing
   *different* fields of the same item both survive a reconcile. Then close the
   T005 TODO in `specs/sync/tasks.md`. Status: `tracked-debt → proven`.

3. **NFR-PERF-01 / a perf AC — virtualized render** *(mint-then-prove, harder)*.
   NFR-PERF-01 is planning-altitude backlog today. Mint a new acceptance
   criterion under it (e.g. `AC-PERF-01 — rendering 1,000 items visits only the
   visible window`) by adding it to `PRD.md` **and** an open `**Carries**` TODO
   (anointed backlog), then build a tiny windowing helper with `@covers AC-PERF-01`
   and prove it with `test_AC_PERF_01_*`. This exercises the full loop including
   the mint step and the exact-set rule.

After any change, re-run `python -m pytest` and the Gate command above, and diff
`trace-manifest.json` to see the row you moved.
