# The Thread Report — the *illuminate* rung

> **Status: shipped.** The tool
> (`extensions/specassay-check/scripts/thread-report.py`), the CI workflow
> (`.github/workflows/thread-report.yml`), and a live example
> ([PR #1](https://github.com/rdryfoos/specassay/pull/1) on the bundled
> `examples/example-app`) all exist today. This note is the reference; the
> *why* lives in [`scope-and-pull-requests.md` §4](scope-and-pull-requests.md),
> and the designed walkthrough lives at
> [specassay.com/thread-report](https://specassay.com/thread-report).

A passing Gate proves the Golden Thread holds: every intent you wrote down is
built and proven, with nothing *hidden* at acceptance-criterion altitude. But a
green check quietly borrows credibility for **everything** in the diff — including
the changes that touch no intent at all. A reviewer still has to read the whole
diff to find them.

The Thread Report closes that gap without adding a gate. On every pull request,
SpecAssay posts **one comment** — a briefing of what moved on the thread, the
touched story walked end to end, and the changed files that sit *far from the
thread*. It **illuminates; it never refuses**. It posts **beside** your PR and
changes nothing about it — not the title, not the description, not the diff.

## What it posts

The comment has three sections plus a one-line header. This is the real report
from [PR #1](https://github.com/rdryfoos/specassay/pull/1), where a developer
paid off tracked debt (`AC-SYNC-02`, the disjoint-field merge) by adding the
proof that was owed, and dropped in a small `metrics.py` along the way.

### Header — the Gate line

```
**Gate:** ✅ Golden Thread intact  ·  **This PR:** +1 proven
```

Read from the manifest's `gate.ok` plus the base↔head diff. A passing Gate does
**not** mean "everything is done" — it means nothing *unfinished* is *hidden* at
AC altitude. The summary counts what actually moved: proofs promoted to
`proven`, other status moves, carriers added, IDs minted or retired.

### 1. What moved

The base-vs-head manifest diff, in prose:

```
- 🟢 **AC-SYNC-02** — `tracked-debt` → **`proven`** ⬆
```

Status changes (with an ⬆/⬇ arrow by rank: `GAP < backlog < tracked-debt <
proven`), carriers added (`@covers` or `test_AC_*` appearing where the status
already held), IDs **🆕 minted**, IDs **🪦 retired**. If nothing on the thread
moved, it says so plainly.

### 2. The thread now

For each **domain** the PR touched (the middle ID token — `US-SYNC-01` →
`SYNC`), the whole family walked top-down (`US → FR → NFR → AC`) as it stands
*after* this PR, with the moved rows flagged `◀ changed`:

```
**SYNC**
| ID          | Status     |           |
|-------------|------------|-----------|
| `US-SYNC-01`| 🔵 backlog |           |
| `FR-SYNC-01`| 🔵 backlog |           |
| `AC-SYNC-01`| 🟢 proven  |           |
| `AC-SYNC-02`| 🟢 proven  | ◀ changed |
```

A reviewer sees the entire thread the change lives on, not just the diff lines.

### 3. Far from the thread

The whole point. Changed files that carry **no mark** tying them to an intent
this PR moved:

```
1 changed file(s) sit **far from the thread** …
- `src/metrics.py`
```

`metrics.py` changed, but nothing in it carries an `@covers`, is a named proof,
or edits the registry / a spec / a tasks file. A legitimate refactor and
unwanted scope look **identical** from here, so the machine refuses to guess. It
hands the reviewer a spotlight, not a verdict. If every changed file carries a
mark, the section says so.

## How it decides "far"

`classify_changed()` buckets each changed path as **on-thread** or **far**:

- **on-thread** if the path is in the head manifest's coverage
  (`implementations`) or `proofs`, is the `registry` file, or matches the
  `specs` / `tasks` globs from the config.
- **far** otherwise.

One subtlety it handles: `git diff --name-only` gives **repo-relative** paths
(`examples/example-app/src/sync.py`), but the manifest and config globs are
**project-relative** (`src/sync.py`). The `--project-root` (defaulting to the
config file's directory) bridges them — files under it are matched
project-relative; files **outside** the governed project are skipped, not
flagged. Without this bridge every changed file would read as "far."

Each bucketed file records a reserved `distance` field — binary today
(`0` on-thread / `1` far). It is deliberately not surfaced as a number yet: the
field is reserved so a future grader (same-directory, import-adjacent,
call-graph proximity) can refine "far" into degrees without a schema change. The
report today speaks in the honest binary — *on the thread* or *far from it*.

## Doctrine — illuminate, affirm, refuse

Three postures, in increasing intervention and decreasing frequency:

- **Illuminate — always on.** The briefing above. It surfaces what's
  decision-relevant and renders no verdict. "Far from the thread" lives here.
  The tool **always exits 0**; it never fails a build.
- **Affirm — opt-in.** A team can escalate the off-thread list to a one-click
  human tick (see `offthread_ack` below). That is a *person's* verdict behind a
  lightweight config — never the machine's.
- **Refuse — rare, provable.** The Gate blocks only on what it can **prove** is a
  defect: a silent AC gap, an invented ID, exact-set drift. Off-thread is not
  machine-decidable as a defect, so it never earns a refusal.

> The machine may only refuse what it can prove is a defect. For the rest, it
> makes a human look.

## Configuration

Two controls split the off-thread signal into *information* and *ceremony*:

- **`offthread_list: always`** — the information: the named list is in every
  report. Pure illuminate, not a toggle.
- **`offthread_ack: off | record | required`** — the ceremony (CLI flag
  `--offthread-ack`):
  - `off` (default) — pure illuminate; just the list.
  - `record` — adds a *"these untraced changes are incidental"* tick to record,
    informational only.
  - `required` — the **affirm** rung: a human must tick before merge. Wire the
    block in a separate CI step; the report tool itself still exits 0.

The report also reads `registry`, `specs`, and `tasks` from the SpecAssay config
to know which paths are intrinsically on-thread.

## Running it

### By hand

```sh
python3 extensions/specassay-check/scripts/thread-report.py \
  --base  base.trace-manifest.json \
  --head  head.trace-manifest.json \
  --changed-files changed.txt \
  --config examples/example-app/specassay-check-config.yml \
  --offthread-ack off \
  --out report.md
```

`--changed-files` takes a file (one path per line) or `-` for stdin. It reads
schema v3 / v4 manifests and has zero dependencies.

### In CI

`.github/workflows/thread-report.yml` runs on `pull_request` and:

1. Emits the **head** manifest with Gate 2 against the PR checkout.
2. Emits the **base** manifest via `git worktree add` at
   `pull_request.base.sha`, run through the *same* checker (stable emitter).
3. Collects changed files with `git diff --name-only base...HEAD`.
4. Builds the report and posts it as a **sticky** comment (marker
   `<!-- specassay-thread-report -->`, updated in place on each push) via
   `actions/github-script`.

It needs `permissions: pull-requests: write` and always succeeds — the report is
a comment, never a check.

## Scope note

This is the mechanical form of the *illuminate* rung argued in
[`scope-and-pull-requests.md` §4](scope-and-pull-requests.md). The Gate proves
**completeness of declared intent**, not **minimality**; the Thread Report is
how the PR — the review unit, the one altitude where *build → intent* is
affordable — carries the minimality conversation, as a briefing rather than a
block.
