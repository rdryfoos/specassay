# Thread Report: the *illuminate* rung

> **Status: shipped.** The tool
> (`extensions/specassay-check/scripts/thread-report.py`), the CI workflow
> (`.github/workflows/thread-report.yml`), and two live examples, green
> [PR #1](https://github.com/rdryfoos/specassay/pull/1) and broken
> [PR #2](https://github.com/rdryfoos/specassay/pull/2) on the bundled
> `examples/example-app`, all exist today. This note is the reference; the
> *why* lives in [`scope-and-pull-requests.md` §4](scope-and-pull-requests.md),
> and the designed walkthrough lives at
> [specassay.com/thread-report](https://specassay.com/thread-report).

A passing Gate means every requirement you wrote down has code and a test, or an
openly declared debt, with nothing unfinished hidden at acceptance-criterion
altitude. But a green check quietly borrows credibility for **everything** in the
diff, including the changes that answer for no requirement at all. A reviewer still
has to read the whole diff to find them.

The Thread Report closes that gap without adding a gate. On every pull request,
SpecAssay posts **one comment**: what the change did to your requirements, the
reworded ones with the code and tests that need checking, and the changed files no
requirement claims. It **reports; it never blocks**. It posts **beside** your pull
request and changes nothing about it: not the title, not the description, not the
diff.

**The words it uses are ordinary ones**, ruled 2026-10-02: requirements, tests and
pull requests. Three house words survive because the comment needs them, and the
comment defines all three in its own last line (*Golden Thread*, *off thread*,
*mint*). Nothing above that line asks a reader to learn a word first.

## What it posts

The comment is **one line a reviewer reads, and everything else one click
down**. The examples below come from green
[PR #1](https://github.com/rdryfoos/specassay/pull/1), where a developer paid
off tracked debt (`AC-SYNC-02`, the disjoint-field merge) by adding the proof
that was owed, and dropped in a small `metrics.py` along the way.

**A note on why it is shaped this way.** The first Thread Report to render on a
real estate (Chalkup, 2026-09-17) was longer than a reviewer would read: every
moved row appeared twice, once as a bullet and again as a table row marked
changed; the family tables listed rows that had not moved beside the ones that
had; and the gate log that produced the report sat open at the bottom. The trims
below are display, not truth. Nothing was dropped, only collapsed.

### The verdict line

```
## 🧵 Thread Report

🟢 **Ready to review** · **1** now has a test · **1** changed file no requirement claims
```

One line, and it is meant to be the whole read for most pull requests: **what to do
next**, then the counts that say what the change did. Three states, and no more:

| State | When | What it tells the reviewer |
| --- | --- | --- |
| `🟢 **Ready to review**` | the Gate passes, nothing was reworded, no required tick is waiting | read the diff as you normally would |
| `🟡 **Needs a person**` | the Gate passes, but a requirement was reworded or a required tick is waiting | something here cannot be settled by a machine |
| `🔴 **Do not merge yet**` | the Gate refuses | the separate check is red and says why |

The amber state exists because the two facts behind it were known and never said. A
reworded requirement has code and tests written against the old wording, and a
`required` tick is unticked the moment the report renders, since a tick attests to
one head and the report reposts on every push. A green line in either case would
have been true about the Gate and misleading about the merge.

No colour on the words; the dot carries it, so the line reads the same in a comment
(where GitHub strips inline colour) and on a page. A passing Gate does **not** mean
"everything is done"; it means nothing unfinished is hidden at acceptance-criterion
altitude.

The counts name only what happened: a term appears when its count is non-zero, so a
pull request that added no requirement never says "0 new requirements". Every count
agrees in number with itself, down to one changed file reading `file`. The terms:

| Count | Means |
| --- | --- |
| `**2** now have a test` | requirements that reached `proven` on this change |
| `**1** now has a declared debt` | requirements that reached `tracked-debt` |
| `**1** has neither` | requirements that reached `GAP` |
| `**1** back to not started` | requirements that reached `backlog` |
| `**1** new requirement` | minted in this change |
| `**1** retired` | retired in this change |
| `**1** reworded` | the wording of the requirement itself moved |
| `**1** gained code or a test, state unchanged` | a carrier was added without a state change |
| `**no requirements changed**` | said out loud rather than going quiet |
| `**2** changed files no requirement claims` / `**every changed file is claimed**` | one or the other, always |

The four state names in the tables (`proven`, `tracked-debt`, `backlog`, `GAP`) and
their badges are **manifest values**, not display words: a viewer renders them and
[`trace-manifest-schema.md`](trace-manifest-schema.md) defines them, so the
plain-words pass left them exactly as they were.

### 1. Reworded requirements

The one section that is about the requirement itself, not the code. When a pull
request **rewords** an existing registry ID, the report surfaces it, because the code
and test written against the old wording may now be subtly wrong while still
passing:

```
### Reworded requirements
⚠️ 1 requirement was reworded. Its code and tests were written against the old
wording, so check that each still satisfies the new one.

- **AC-SYNC-01** — reworded
  - was: _A change made offline appears on a second device within 5s of reconnect._
  - now: _A change made offline appears on a second device within 3s of reconnect._
  - check:
    - `sync.py:51`
    - `test_sync.py:37` — ⚠ still contains the old `5s`
```

Detection is whitespace-insensitive (a reflow or a typo in spacing is not a
rewording); any substantive wording change flags. The **check** list is the
requirement's code and tests (`implementations` + `proofs`), linked to their current
state (`blob@head`); the reviewer clicks each and confirms it still satisfies the new
wording.

**How hard the report leans depends on what it can prove.** Three tiers, in
decreasing confidence:

1. **Pinpointed.** The rewording changed a *concrete token* (a number with a unit
   like `5s`, a quoted literal, an ALL-CAPS identifier) **and** that old value still
   appears in the code or a test. The report flags the exact line: *"still contains
   the old `5s`."* In the example the test still asserts *5s* while the requirement
   now says *3s*: green and wrong, caught mechanically.
2. **Value changed, not located.** A concrete token changed, but it is not found
   literally in the code or tests: *"The value changed from `200ms` to `100ms`, and
   neither appears literally in the code or tests. Check by reading."* Honest that it
   cannot point at a line.
3. **Wording only.** No concrete token changed, because a sentence was tightened:
   *"Wording only, with no value to search for. Read the code and its test against
   the new wording."* The default: it admits the machine cannot judge and hands the
   person the list.

The line holds throughout: the machine may show richer detail (tier 1), but it only
ever asks a person to look; it never refuses on a rewording. This is the
blast-radius integrity property argued in
[`scope-and-pull-requests.md` §5](scope-and-pull-requests.md), made mechanical and
surfaced on the pull request that moves the requirement (`intent_ack` escalates it to
a human tick; see *Configuration*). A reworded requirement also appears in *What
changed*, marked `✍️ reworded`, pointing at the registry hunk that reworded it.

**A reworded requirement always reads `🟡 Needs a person`** on the verdict line, even
with the Gate green and the tick off, because nothing but a person can say whether
the old code still answers the new wording.

**The two shapes, told apart by the carriers.** A rewording arrives either as a
**pull request from intent** (the wording moves alone: live
[PR #4](https://github.com/rdryfoos/specassay/pull/4)) or a **pull request from the
field**, the discovery one (the code and tests move in the same pull request: live
[PR #5](https://github.com/rdryfoos/specassay/pull/5)). The check list annotates each
file that was touched here (*`◀ changed in this pull request`*, linked to its diff),
so the shapes read differently at a glance: untouched files owe a check; changed ones
carry their answer in the same diff. The partial case renders both marks at once:
*changed in this pull request* yet *still contains the old value*.

With new and retired requirements (in *What changed*) and reworded ones here, the
report covers all three legible kinds of intent diff.

### 2. What changed

Folded. One section, not two: the table carries the move *and* the state, so no fact
is stated twice. For each **area** the pull request touched (the middle ID token:
`US-SYNC-01` → `SYNC`), the requirements this change moved, walked top down
(`US → FR → NFR → AC`):

```
<details>
<summary><b>What changed</b> — 1 requirement in 1 area</summary>

**SYNC**

| ID | What changed | Where |
|----|--------------|-------|
| `AC-SYNC-02` | `tracked-debt` → 🟢 **`proven`** | `test_sync.py` `sync.py` |

<sub>+3 requirements in this area did not change, not listed: 2 🔵 backlog, 1 🟢 proven.</sub>

</details>
```

The **What changed** cell says what the requirement did: a state transition,
`🆕 new`, `🪦 retired (the ID is never reused)`, `✍️ reworded`, or code or a test
added with the state held. A requirement that did more than one of those (new *and*
reworded) carries both, separated by `·`, on its one line.

**Where** names the files *this pull request changed* that answer for the moved ID
(its test and `@covers` line), so the reviewer can click straight to the change that
did the moving. For a new or reworded requirement the move lives in the registry, so
it points there instead. When the move came from a file that answers for nothing of
its own, a task line gaining a `**Carries**` say, the cell is an em dash: absence
renders as absence, never as an invented link.

**Requirements this change did not move are footnoted, not listed**, with their
states counted so the state is still there without the reading. A report about this
change should show what changed; the area around it is context, one summarised line
of it. An area where everything moved carries no footnote at all.

### 3. Changed files no requirement claims

The whole point, and also folded. Changed files that answer for **no requirement**
this change moved:

```
<details>
<summary><b>Changed files no requirement claims</b> — 1 file</summary>

Changed, but nothing in it names a requirement this pull request moved. Not a
defect: a refactor and unwanted scope look the same here. Worth a glance:

- src/metrics.py

</details>
```

`metrics.py` changed, but nothing in it carries an `@covers` line, is a test named
for a requirement, or edits the registry, a spec or a tasks file. A legitimate
refactor and unwanted scope look **identical** from here, so the machine refuses to
guess. It hands the reviewer a spotlight, not a verdict. If every changed file
answers for a requirement, the report says so in one unfolded line: *Every changed
file names a requirement. Nothing is unclaimed.*

The section's own house word, *off thread*, now appears only in the footer, with its
definition beside it. The section itself says what it means.

**The human tick never folds.** When `offthread_ack` is `record` or `required`, the
checkbox renders *outside* the `<details>`, because a `required` tick holds a merge
and a checkbox nobody can see is not a ceremony. The same goes for *Reworded
requirements*, which is never folded at all: it asks the reader to go and check
something.

### 4. The run behind this report

Optional, folded, and never written by the report itself. `--receipts FILE` renders
that file's Markdown at the end of the report under one click. It exists because the
run that produced a report, a gate log or a toolchain line, is a receipt rather than
a headline: worth keeping, not worth leading with. The report never reads, parses or
reformats what it is given; the caller owns that text.

### 5. The footer, and the three words it defines

One line, last, and the only place the comment uses a word a stranger would have to
be taught:

```
This comment reports; it never blocks. A changed file no requirement claims is a
note, not a failure. Words used here: Golden Thread, the chain from a requirement
to the code and test that answer for it. Off thread, a changed file no requirement
claims. Mint, to write a new requirement into the registry. Set `offthread_ack:
record|required` in the SpecAssay config to add a human tick.
```

Ruled 2026-10-02: the words belong here, with the teaching attached, and not in the
line a stranger reads first.

## Clickable: a spotlight you can click

Given `--pr-url` (and `--head-sha`), the report renders live links, so the
reviewer moves from briefing to exact line in one click:

- **Changed files** (the unclaimed list, and the **Where** column of *What
  changed*) → their **diff hunk in this pull request**:
  `…/pull/N/files#diff-<sha256(path)>`. For a rewording or a new requirement that
  column points at the **registry file's** hunk instead, because the change *is* the
  wording.
- **IDs** → their **registry line**: `…/blob/<head-sha>/<registry>#L<line>`.
- **The check list** (in *Reworded requirements*) → the **current code and tests**
  (`blob@head`), not a diff: they usually did not change, and you are being sent *to*
  them to read against the new wording.

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
config file's directory) bridges them: files under it are matched
project-relative; files **outside** the governed project are skipped, not
flagged. Without this bridge every changed file would read as "off-thread."

Each bucketed file records a reserved `distance` field, binary today
(`0` on-thread / `1` off). It is deliberately not surfaced as a number yet: the
field is reserved so a future grader (same-directory, import-adjacent,
call-graph proximity) can refine "off-thread" into degrees without a schema
change. The report today speaks in the honest binary: *on the thread* or *off
it*.

## The broken path: post the report, then block

When the head Gate refuses (a silent AC gap, an invented ID, exact-set drift),
the Thread Report **still posts**, headed `🔴 Do not merge yet`, with the
offending requirement shown moving *into* `GAP`. That is the most illuminating moment the
feature has, so it is not silent. The report tool **always exits 0**; refusing
is not its job.

The **block** is a separate step. The workflow's emit steps tolerate a broken
Gate (the Gate always *writes* the manifest, then exits non-zero; the workflow
reads the written manifest and moves on). After the comment posts, a final
`Gate verdict` step re-reads `gate.ok` and fails the job if the thread is
broken. So the comment illuminates and the check refuses: two steps, never one.
See broken [PR #2](https://github.com/rdryfoos/specassay/pull/2): the red report
is posted *and* the check is failed.

## Doctrine: illuminate, affirm, refuse

Three postures, in increasing intervention and decreasing frequency:

- **Illuminate: always on.** The briefing. It surfaces what is decision-relevant
  and renders no verdict of its own; the amber verdict says a person is needed, not
  that anything is wrong. The unclaimed-files list lives here. The tool never fails
  a build.
- **Affirm: opt-in.** A team can escalate the unclaimed-files list to a one-click
  human tick (`offthread_ack`, below). That is a *person's* verdict behind a
  lightweight config, never the machine's.
- **Refuse: rare, provable.** The Gate blocks only on what it can **prove** is a
  defect: a silent AC gap, an invented ID, exact-set drift. Off-thread is not
  machine-decidable as a defect, so it never earns a refusal.

> The machine may only refuse what it can prove is a defect. For the rest, it
> makes a human look.

## Configuration

`offthread_ack` is a real key in the SpecAssay config, read by the tool
(`--offthread-ack` overrides it):

- **`off`** (default). Pure illuminate: the unclaimed-files list is shown, no tick.
- **`record`**. Adds a *"these unclaimed changes are incidental"* tick to record,
  informational only. It asks for nothing, so it leaves the verdict green.
- **`required`**. The **affirm** rung: a human must tick before merge. The
  report tool itself still exits 0; enforcement is separate wiring, and it
  ships (below).

`intent_ack` is the twin key for the **Reworded requirements** section
(`--intent-ack` overrides it), with the same three settings: `off` illuminates,
`record` adds an informational tick, `required` makes a person confirm each reworded
requirement still holds before merge. The tick only appears on a pull request that
actually rewords one. A `required` tick of either kind reads `🟡 Needs a person` on
the verdict line, because it is unticked the moment the report renders. Same doctrine as `offthread_ack`: the report illuminates and records
the human's verdict; it never renders the verdict itself.

**How `required` blocks (shipped).** The ticks are real GitHub task-list
checkboxes in the report comment; anyone with write access can tick them.
After posting, the workflow sets a **`specassay/ack`** commit status on the PR
head: *failure* while any required box is unticked. Ticking a box edits the
comment, which fires [`ack-gate.yml`](../.github/workflows/ack-gate.yml); it
re-reads the boxes and flips the status to *success* when all required ticks
are given. To make the status a hard stop, add `specassay/ack` to the branch's
required status checks (branch protection); without that it's a visible
red/green signal, not a block. Ticks **reset on every new push**: the report
reposts with fresh boxes, because a tick attests to a specific head, not to
the PR forever.

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
/ `--head-sha` are optional (they enable links). `--receipts FILE` appends that
file's Markdown, folded, at the end of the report; a missing file costs the
appendix and warns on stderr, never the report. It reads schema v3 / v4
manifests and has zero dependencies.

### In CI

`.github/workflows/thread-report.yml` runs on `pull_request` and:

1. Emits the **head** manifest with Gate 2 (tolerating a broken Gate; it relies
   on the manifest the Gate always writes).
2. Emits the **base** manifest via `git worktree add` at
   `pull_request.base.sha`, the same way.
3. Collects changed files with `git diff --name-only base...HEAD`.
4. Builds the report (passing `--pr-url` / `--head-sha` from the event) and posts
   it as a **sticky** comment (marker `<!-- specassay-thread-report -->`, updated
   in place on each push).
5. A final `Gate verdict` step re-reads `gate.ok` and **fails the job** if the
   thread is broken: the block, posted separately from the briefing.

It needs `permissions: pull-requests: write`.

## Scope note

This is the mechanical form of the *illuminate* rung argued in
[`scope-and-pull-requests.md` §4](scope-and-pull-requests.md). The Gate proves
**completeness of declared intent**, not **minimality**; the Thread Report is
how the PR (the review unit, the one altitude where *build → intent* is
affordable) carries the minimality conversation, as a briefing rather than a
block.
