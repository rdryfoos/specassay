# Thread Report — the *illuminate* rung

> **Status: shipped.** The tool
> (`extensions/specassay-check/scripts/thread-report.py`), the CI workflow
> (`.github/workflows/thread-report.yml`), and two live examples — green
> [PR #1](https://github.com/rdryfoos/specassay/pull/1) and broken
> [PR #2](https://github.com/rdryfoos/specassay/pull/2) on the bundled
> `examples/example-app` — all exist today. This note is the reference; the
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
touched story walked end to end, and the changed files that sit *off the
thread*. It **illuminates; it never refuses**. It posts **beside** your PR and
changes nothing about it — not the title, not the description, not the diff.

## What it posts

The comment has a one-line header plus three sections. This is the real report
from green [PR #1](https://github.com/rdryfoos/specassay/pull/1), where a
developer paid off tracked debt (`AC-SYNC-02`, the disjoint-field merge) by
adding the proof that was owed, and dropped in a small `metrics.py` along the
way.

### Header — the Gate line

```
## 🧵 Thread Report

🟢 **Golden Thread intact**
```

One line, one fact: does the thread hold. `🟢 Golden Thread intact` when
`gate.ok` is true; `🔴 Golden Thread broken` when it isn't (see *The broken
path* below). No colour on the word — the dot carries it, so it reads the same
in a comment (where GitHub strips inline colour) and on the page. A passing Gate
does **not** mean "everything is done"; it means nothing *unfinished* is
*hidden* at AC altitude.

### 1. What moved

The base-vs-head manifest diff, in prose:

```
- 🟢 **AC-SYNC-02** — `tracked-debt` → **`proven`** · `test_sync.py` `sync.py`
```

Status changes, carriers added, IDs **🆕 minted**, IDs **🪦 retired**. The
trailing files are the **on-thread** files *this PR changed* that carry the
moved ID — its proof and `@covers` — rendered so the reviewer can click straight
to the change that did the moving.

### 1b. Intent Changed

The one section that's about the intent itself, not the code. When a PR
**restates** an existing registry ID — changes its *wording* — the report
surfaces it, because the **build and proof** written against the old wording may
now be subtly wrong while still passing:

```
### Intent Changed
⚠️ 1 intent was restated — its wording moved under the code and tests written
against the old text. Re-confirm each still satisfies the new statement.

- **AC-SYNC-01** — restated
  - was: _A change made offline appears on a second device within 5s of reconnect._
  - now: _A change made offline appears on a second device within 3s of reconnect._
  - re-confirm:
    - `sync.py:51`
    - `test_sync.py:37` — ⚠ still contains the old `5s`
```

(The report says *code and tests*; here in the reference we use the vocabulary —
the **build** and its **proof**.)

Detection is whitespace-insensitive (a reflow or typo-in-spacing is not a
restatement); *any* substantive wording change flags. The **re-confirm** list is
the row's build + proof (`implementations` + `proofs`), linked to their
**current code** (`blob@head`) — the reviewer clicks each and checks it still
satisfies the new statement.

**How hard the report leans depends on what it can prove** — three tiers, in
decreasing confidence:

1. **Pinpointed.** The reword changed a *concrete token* (a number-with-unit like
   `5s`, a quoted literal, an ALL-CAPS identifier) **and** that old value still
   appears in the build or proof. The report flags the exact line: *"still
   contains the old `5s`."* In the example the proof still asserts *5s* while the
   criterion now says *3s* — green and wrong, caught mechanically.
2. **Value changed, not located.** A concrete token changed, but it isn't found
   verbatim in the code or tests: *"Value `200ms` → `100ms` changed, but not
   found verbatim… re-confirm by reading."* Honest that it can't point at a line.
3. **Prose.** No concrete token changed (a sentence was tightened): *"Prose
   change — no literal value to pin down; re-confirm the build and its proof by
   reading them against the new wording."* The default — it admits the machine
   can't judge and hands the human the list.

The line holds throughout: the machine may **illuminate** richer detail (tier 1),
but it only ever asks a human to look — it never *refuses* on a restatement. This
is the blast-radius integrity property argued in
[`scope-and-pull-requests.md` §5](scope-and-pull-requests.md), made mechanical
and surfaced on the PR that moves the intent (`intent_ack` escalates it to a
human tick — see *Configuration*). A restated intent also lights up *Thread
Status* (`◀ changed`).

**The two shapes, told apart by the carriers.** A restatement arrives either as
a **PR from Intent** (the wording moves alone — live
[PR #4](https://github.com/rdryfoos/specassay/pull/4)) or a **PR from the
Field**, the discovery PR (the carriers move in the same PR — live
[PR #5](https://github.com/rdryfoos/specassay/pull/5)). The re-confirm list
annotates each carrier that was touched in this PR — *`◀ updated in this PR`*,
linked to its diff — so the shapes read differently at a glance: untouched
carriers owe a re-confirm; updated ones carry their re-confirmation in the same
diff. The partial case renders both marks at once: *updated in this PR* yet
*still contains the old value*.

With minted / retired (in *What moved*) and restated here, the report now covers
all three legible-intent-diff types.

### 2. Thread Status

For each **domain** the PR touched (the middle ID token — `US-SYNC-01` →
`SYNC`), the family walked top-down (`US → FR → NFR → AC`) as it stands *after*
this PR, with moved rows flagged `◀ changed`:

```
**SYNC**
| ID          | Status     |           |
|-------------|------------|-----------|
| `AC-SYNC-01`| 🟢 proven  |           |
| `AC-SYNC-02`| 🟢 proven  | ◀ changed |

+2 untouched backlog rows not shown.
```

**Untouched `backlog` rows are hidden** — a story this PR didn't move doesn't
need its inert planning rows reprinted every time. The count of what's hidden is
stated, never silently dropped. A reviewer sees the live part of the thread the
change lives on, not the whole planning tree.

### 3. Off Thread

The whole point. Changed files that carry **no mark** tying them to an intent
this PR moved:

```
1 changed file sits **off the thread** …
- src/metrics.py
```

`metrics.py` changed, but nothing in it carries an `@covers`, is a named proof,
or edits the registry / a spec / a tasks file. A legitimate refactor and
unwanted scope look **identical** from here, so the machine refuses to guess. It
hands the reviewer a spotlight, not a verdict. If every changed file carries a
mark, the section says so.

## Clickable — a spotlight you can click

Given `--pr-url` (and `--head-sha`), the report renders live links, so the
reviewer moves from briefing to exact line in one click:

- **Changed files** (the off-thread list, and the on-thread build and proof in
  *What moved*) → their **diff hunk in this PR**: `…/pull/N/files#diff-<sha256(path)>`.
- **IDs** → their **registry line**: `…/blob/<head-sha>/<registry>#L<line>`.
- **`◀ changed`** (in *Thread Status*) → the **diff** that moved that row: the
  carrier's hunk (proof / `@covers`) for a code move, or the **registry file's**
  hunk when the move is a restatement or a mint (the change is the wording
  itself), so each moved row jumps to its change.
- **Re-confirm build and proof** (in *Intent Changed*) → their **current code**
  (`blob@head`), not a diff — the build and proof usually didn't change; you're
  being sent *to* them to re-check against the new wording.

The `#diff-<sha256>` anchor is GitHub's stable (if undocumented) convention; the
blob link is the fully-documented form. Without `--pr-url` the report degrades
gracefully to plain code spans, so running it by hand still works.

## How it decides on-thread vs off

`classify_changed()` buckets each changed path as **on-thread** or **off**:

- **on-thread** if the path is in the head manifest's coverage
  (`implementations`) or `proofs`, is the `registry` file, or matches the
  `specs` / `tasks` globs from the config.
- **off-thread** otherwise.

One subtlety it handles: `git diff --name-only` gives **repo-relative** paths
(`examples/example-app/src/sync.py`), but the manifest and config globs are
**project-relative** (`src/sync.py`). The `--project-root` (defaulting to the
config file's directory) bridges them — files under it are matched
project-relative; files **outside** the governed project are skipped, not
flagged. Without this bridge every changed file would read as "off-thread."

Each bucketed file records a reserved `distance` field — binary today
(`0` on-thread / `1` off). It is deliberately not surfaced as a number yet: the
field is reserved so a future grader (same-directory, import-adjacent,
call-graph proximity) can refine "off-thread" into degrees without a schema
change. The report today speaks in the honest binary — *on the thread* or *off
it*.

## The broken path — post the report, then block

When the head Gate refuses (a silent AC gap, an invented ID, exact-set drift),
the Thread Report **still posts** — headed `🔴 Golden Thread broken`, with the
offending row shown moving *into* `GAP`. That is the most illuminating moment the
feature has, so it is not silent. The report tool **always exits 0**; refusing
is not its job.

The **block** is a separate step. The workflow's emit steps tolerate a broken
Gate (the Gate always *writes* the manifest, then exits non-zero — the workflow
reads the written manifest and moves on). After the comment posts, a final
`Gate verdict` step re-reads `gate.ok` and fails the job if the thread is
broken. So the comment illuminates and the check refuses — two steps, never one.
See broken [PR #2](https://github.com/rdryfoos/specassay/pull/2): the red report
is posted *and* the check is failed.

## Doctrine — illuminate, affirm, refuse

Three postures, in increasing intervention and decreasing frequency:

- **Illuminate — always on.** The briefing. It surfaces what's decision-relevant
  and renders no verdict. "Off thread" lives here. The tool never fails
  a build.
- **Affirm — opt-in.** A team can escalate the off-thread list to a one-click
  human tick (`offthread_ack`, below). That is a *person's* verdict behind a
  lightweight config — never the machine's.
- **Refuse — rare, provable.** The Gate blocks only on what it can **prove** is a
  defect: a silent AC gap, an invented ID, exact-set drift. Off-thread is not
  machine-decidable as a defect, so it never earns a refusal.

> The machine may only refuse what it can prove is a defect. For the rest, it
> makes a human look.

## Configuration

`offthread_ack` is a real key in the SpecAssay config, read by the tool
(`--offthread-ack` overrides it):

- **`off`** (default) — pure illuminate: the off-thread list is shown, no tick.
- **`record`** — adds a *"these untraced changes are incidental"* tick to
  record, informational only.
- **`required`** — the **affirm** rung: a human must tick before merge. Wire the
  actual block in a separate CI step; the report tool itself still exits 0.

`intent_ack` is the twin key for the **Intent Changed** section (`--intent-ack`
overrides it), with the same three settings — `off` illuminates, `record` adds
an informational tick, `required` makes a human confirm each restated intent
still holds before merge. The tick only appears on a PR that actually restates
an intent. Same doctrine as `offthread_ack`: the report illuminates and records
the human's verdict; it never renders the verdict itself.

The report also reads `registry`, `specs`, and `tasks` from the config to know
which paths are intrinsically on-thread.

## Running it

### By hand

```sh
python3 extensions/specassay-check/scripts/thread-report.py \
  --base  base.trace-manifest.json \
  --head  head.trace-manifest.json \
  --changed-files changed.txt \
  --config examples/example-app/specassay-check-config.yml \
  --pr-url https://github.com/OWNER/REPO/pull/N \
  --head-sha "$HEAD_SHA" \
  --out report.md
```

`--changed-files` takes a file (one path per line) or `-` for stdin. `--pr-url`
/ `--head-sha` are optional (they enable links). It reads schema v3 / v4
manifests and has zero dependencies.

### In CI

`.github/workflows/thread-report.yml` runs on `pull_request` and:

1. Emits the **head** manifest with Gate 2 (tolerating a broken Gate — it relies
   on the manifest the Gate always writes).
2. Emits the **base** manifest via `git worktree add` at
   `pull_request.base.sha`, the same way.
3. Collects changed files with `git diff --name-only base...HEAD`.
4. Builds the report (passing `--pr-url` / `--head-sha` from the event) and posts
   it as a **sticky** comment (marker `<!-- specassay-thread-report -->`, updated
   in place on each push).
5. A final `Gate verdict` step re-reads `gate.ok` and **fails the job** if the
   thread is broken — the block, posted separately from the briefing.

It needs `permissions: pull-requests: write`.

## Scope note

This is the mechanical form of the *illuminate* rung argued in
[`scope-and-pull-requests.md` §4](scope-and-pull-requests.md). The Gate proves
**completeness of declared intent**, not **minimality**; the Thread Report is
how the PR — the review unit, the one altitude where *build → intent* is
affordable — carries the minimality conversation, as a briefing rather than a
block.
