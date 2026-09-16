# SpecAssay Quickstart

## step one: see a Thread Report

<!-- @covers FR-DOCS-60 -->

This page takes you from a blank Claude Code session to a **Thread Report**, the
one-comment briefing SpecAssay posts on a change, saying what moved on the thread
and what rode along untraced, on a tiny sample project you build here. You will
mint one promise, build it, prove it, break it on purpose, watch the **Gate** (the
deterministic check that refuses work with a hidden hole in it) refuse, fix it,
and read the result. Target: one short sitting, unassisted.

You do not need to know Spec Kit or SpecAssay to follow it. Every block is a
paste-block that ends with a **You should now see** receipt, so if something goes
wrong you can name the block it went wrong in.

> No hand-holding and dive right in?
> [https://github.com/rdryfoos/specassay](https://github.com/rdryfoos/specassay)

---

## Pinned, as of 2026-09-15

| Thing | Pinned to |
| --- | --- |
| SpecAssay | **v0.4.13**, released 2026-09-04. This is the version the sitting below was captured against, not necessarily the one you will install: see the note under the table. |
| GitHub Spec Kit | **v1.0.4**, the newest version SpecAssay has been run against end to end (`docs/submission/test-evidence.md`, 2026-09-04). Spec Kit v1.0.5 and v1.0.6 exist and SpecAssay's manifests accept them (`>=0.14.0,<2.0.0`); they are not what this page's receipts were captured on. |
| uv | 0.8.17 |
| Python | 3.11.15 |
| git | 2.43.0 |

**One divergence, named rather than hidden (2026-09-16).** SpecAssay v0.5.0 is
being cut, and `main`'s catalogs point at it, so `specify bundle install` will
give you v0.5.0 while the receipts below were captured on v0.4.13. The release is
a repair release: it makes SpecAssay read a project's own configured ID grammar
everywhere instead of assuming the stock one. This sitting uses the stock grammar
throughout, so nothing here is expected to read differently, and the block-by-block
receipts are what a v0.4.13 run really printed. They have not yet been re-captured
on v0.5.0 by a cold operator, which is the only thing that would let this table say
v0.5.0 honestly. Until then: if your run differs from a receipt below in any way,
that difference is a finding and we want it (see *When you stumble*, at the end).

**Where the receipts come from.** Every block below was run in order, on
2026-09-15, against those exact versions, and the output quoted under each block
is that run's real output, trimmed to the lines that carry the receipt, never a
sketch of what it might say. That run was on Linux, not a Mac.
macOS and Linux are both first-class for these commands, and the only difference
we expect is the `python:` version string and your own paths. **If your Mac shows
anything else different, that difference is a finding: report it** (see *When
you stumble*, at the end).

An unpinned quickstart rots silently, so this one carries its versions and its
date. If you are reading it long after 2026-09-15, the versions above are what it
was true for.

---

## Before you start

You need four things. Block 1 checks three of them; the fourth is your account.

- **Claude Code, on a paid plan.** Claude Code requires a Pro, Max, Team,
  Enterprise, or Console account; the free Claude.ai plan does not include Claude
  Code access ([Claude Code setup docs](https://code.claude.com/docs/en/setup)).
  It needs macOS 13.0+ and 4 GB+ RAM.
- **A Mac.** macOS is what this version of the page is written and trialed for.
  Linux works the same way; Windows needs Git Bash or WSL, because the Gate is a
  bash script.
- **git**, any recent version.
- **Python 3**, version 3.8 or newer, on your `PATH` as `python3` or `python`,
  which is what the Gate runs on. Spec Kit's own CLI wants Python 3.11 or newer
  ([Spec Kit v1.0.4 installation guide](https://github.com/github/spec-kit/blob/v1.0.4/docs/installation.md));
  block 2 says what to do if yours is older.

You run every block below in your terminal, inside a Claude Code session or in a
plain shell, your choice. Nothing here needs Claude Code to *do* anything for you
yet; step one is you driving the tools by hand, so you can see what each one
actually does.

---

## 1. Check the machine

```bash
git --version
python3 --version
uv --version || echo "uv: not installed — block 2 installs it"
```

**You should now see** three lines: a git version, a Python version of 3.8 or
newer, and either a uv version or the `not installed` note. Ours:

```text
git version 2.43.0
Python 3.11.15
uv 0.8.17
```

If `git --version` or `python3 --version` fails on a Mac, the usual fix is
`xcode-select --install`, which installs Apple's command line tools; rerun this
block afterward. If `python3` is still missing, or older than 3.8, install a
current Python from [python.org](https://www.python.org/downloads/) or Homebrew.

---

## 2. Install Spec Kit, pinned

**uv** is the Python tool installer Spec Kit ships through; **Spec Kit** is
GitHub's spec-driven development toolkit, the workflow SpecAssay rides on. Skip
the first line if block 1 already printed a uv version.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.0.4
specify --version
```

**You should now see** the pinned version, exactly:

```text
specify 1.0.4
```

If `uv tool install` stops saying it cannot find a suitable Python, run
`uv python install 3.11` and repeat the `uv tool install` line; that fetches a
Python for uv's own use and leaves your system Python alone. If `uv` is not found
after the install script, open a new terminal window first: the installer adds it
to your `PATH` for new shells.

---

## 3. Make the sample project

`specify init` scaffolds a Spec Kit project; `--integration claude` installs the
Spec Kit skills into `.claude/skills` so Claude Code can drive them later.

```bash
cd ~
specify init specassay-tour --integration claude --non-interactive
cd specassay-tour
printf '__pycache__/\ntrace-manifest*.json\nbase.trace-manifest.json\nthread-report.md\n' > .gitignore
git init -q
git add -A && git commit -qm "Spec Kit project, before SpecAssay"
git log --oneline -1
```

**You should now see** `Project ready.` from `specify init`, a *Next Steps* panel,
and then one commit line like:

```text
34e0dd3 Spec Kit project, before SpecAssay
```

If `git commit` stops with *"Please tell me who you are"*, git has no identity on
this machine yet. Set one and rerun the commit line:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Two notes on what just happened. `specify init` does **not** create a git
repository for you at v1.0.4 (git is an opt-in Spec Kit extension), which is why
you ran `git init` yourself; the Thread Report in block 11 needs git history to
know what changed. And the `.gitignore` line keeps the tour's emitted files out of
git so the Thread Report's file list stays about your code; in a real repository,
whether you commit the emitted manifest is your call, and CI emits it either way.

---

## 4. Layer in SpecAssay

SpecAssay installs as a Spec Kit **bundle**, a named set of components Spec Kit
installs in one operation. These three `catalog add` commands tell Spec Kit where
to find it; the fourth installs it.

```bash
specify preset catalog add \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/presets.json \
  --name specassay --install-allowed

specify extension catalog add \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/extensions.json \
  --name specassay --install-allowed

specify bundle catalog add \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/bundles.json \
  --id specassay --policy install-allowed

specify bundle install specassay
```

**You should now see**, as the last two lines:

```text
Updated execute permissions on 4 script(s) recursively
✓ Installed 'specassay' (2 added, 0 already present).
```

The two components are the **preset** (durable-ID grammar appended to Spec Kit's
templates) and the **extension** `specassay-check` (the Gate and the file it
emits). If the CLI asks you to confirm a URL, say yes: it asks once per install
source. If instead you see *"Bundle 'specassay' resolves only from a
discovery-only source ('community')"*, you are not inside the project directory:
`cd ~/specassay-tour` and rerun the four commands.

The bundle also installs Claude Code skills: `/speckit-specassay-check-gate`,
`-mint`, `-matrix`, `-portfolio`, `-dig`. This page calls the scripts directly
instead, so that what you see is exactly what the Gate does, with nothing
interpreting it for you.

---

## 5. Run the Gate on nothing

The **registry** is the one file that holds your durable IDs (`PRD.md` by
default); a **durable ID** is a name like `AC-GREET-10` minted once at intent and
never renumbered. You have no registry yet, so make an empty one and run the
Gate against it.

```bash
touch PRD.md
bash .specify/extensions/specassay-check/scripts/check-traceability.sh
echo "exit: $?"
```

**You should now see** a green run that refuses to take credit for being green:

```text
SpecAssay Check (Gate 2) starting
  python: python3 (3.11.15)
  config: .specify/extensions/specassay-check/specassay-check-config.yml (from specassay-check-config.yml)
Wrote trace-manifest.v5beta.json (0 rows, schemaVersion 5, beta)
Wrote trace-manifest.json (0 rows) gate.ok=True
SpecAssay Check (Gate 2): OK, registry empty (0 IDs in PRD.md)
  Nothing is promised yet, so there is nothing to check. The Gate stays green until a first ID exists; this green proves nothing.
  Mint a first ID, either way:
    greenfield (new work): mint the IDs for a story before writing its spec; ...
    brownfield (existing docs, no IDs yet): pick one requirement from a doc you already have and mint it with the same command, ...
exit: 0
```

(The real output prints the full command for each on-ramp; it is abridged here
only to keep this page short.)

Two files got written even with nothing to check. The one that matters is the
**trace-manifest** (`trace-manifest.json`): the small, portable record of what the
Gate found (every ID, its state, what carries it, what proves it, and whether the
Gate passed), which any viewer can read without re-scanning your repository. The
`.v5beta.json` beside it is the next schema version, carrying two things v4
cannot; ignore it for the tour.

Read the first three lines every time you run the Gate: which Python it found, and
which config file it resolved. If that third line says `config: MISSING`, it also
prints the one `cp` command that scaffolds the config, and the run continues on
template defaults meanwhile. On Spec Kit v1.0.4 the bundle install scaffolds it
for you, which is why ours says `from specassay-check-config.yml`.

This is the empty-green case, and it is the first honest thing SpecAssay says to
you: **green on an empty registry means nothing has been promised, not that
anything has been checked.** Everything from here is you giving it something to
check.

---

## 6. Mint one toy promise

**Minting** is writing a durable ID into the registry at the moment you settle the
intent, never inferred from code afterward. `mint-id.sh` picks the next free
number (always a multiple of ten) and appends the line in the file's own style.

```bash
bash .specify/extensions/specassay-check/scripts/mint-id.sh AC GREET \
  --append 'Given a name, when the greeter runs, then it returns "Hello, <name>!".'
cat PRD.md
bash .specify/extensions/specassay-check/scripts/check-traceability.sh
echo "exit: $?"
```

**You should now see** the ID, the registry line, and then your first honest red:

```text
AC-GREET-10
appended to PRD.md
REMINDER: state the coverage basis plainly in the mint commit.
  Already-built work this mint is only now registering: "coverage registered, not newly attributed."
  New work this mint is starting: say that instead. Either is honest; silence about which is not.
- AC-GREET-10 — Given a name, when the greeter runs, then it returns "Hello, <name>!".
FAIL: registry ID missing from specs: AC-GREET-10
FAIL: registry ID missing from tasks: AC-GREET-10
FAIL: silent gap: AC-GREET-10 has no test and no open tracked-debt task
Wrote trace-manifest.json (1 rows) gate.ok=False
SpecAssay Check (Gate 2): FAILED
exit: 1
```

On a real repository your first mint usually looks slightly different: you point
the config's `registry:` key at a document you already have, or mint one ID whose
statement names the requirement in that document. One is enough to start, and you
never go back and backfill IDs for everything already built: the tour mints from
nothing only because the tour starts from nothing.

Three refusals, and all three are correct. You have promised something
(`AC-GREET-10` is an **acceptance criterion**: one testable statement of what
"done" means) and nothing in the repository answers for it yet. The third line is
the core refusal, a **silent gap**: an acceptance criterion with neither a proof
nor an openly admitted debt. The Gate wrote `trace-manifest.json` anyway; it
records refusals rather than hiding them.

---

## 7. Give it a spec and a task

Two ways to clear that red, and they teach the difference between hidden and
admitted incompleteness. This block takes the honest-debt route first: a
**spec** (the Spec Kit feature document that references the ID, never re-mints
it) and an open **task** carrying a `**Carries**:` mark (the task-side line naming
which ID that task serves).

```bash
mkdir -p specs/greet
cat > specs/greet/spec.md <<'EOF'
# Feature Spec — Greeter

Inherits its registry IDs from `PRD.md`; it references them, never re-mints them.

## Acceptance criteria

- AC-GREET-10 — Given a name, when the greeter runs, then it returns "Hello, <name>!".
EOF
cat > specs/greet/tasks.md <<'EOF'
# Tasks — Greeter

- [ ] T001 Build the greeter and write its proof — **Carries**: AC-GREET-10
EOF
bash .specify/extensions/specassay-check/scripts/check-traceability.sh
python3 -c "import json;[print(r['id'], r['status']) for r in json.load(open('trace-manifest.json'))['rows']]"
cp trace-manifest.json base.trace-manifest.json
git add -A && git commit -qm "Mint AC-GREET-10 with its spec and task (new work, tracked debt)"
git tag thread-base
```

**You should now see** green, and one row in a named state:

```text
Wrote trace-manifest.json (1 rows) gate.ok=True
SpecAssay Check (Gate 2): OK (1 registry IDs)
AC-GREET-10 tracked-debt
```

**`tracked-debt`** means started, proof missing, and admitted on an open task:
visible, on the books, not hidden. That is why the Gate passes: passing never
means "everything is done", it means nothing unfinished is *hidden* at
acceptance-criterion altitude.

The last three lines set up block 11. `base.trace-manifest.json` is a snapshot of
the thread as it stands right now, and the `thread-base` tag marks the commit it
belongs to; the Thread Report compares *before* against *after*, so it needs both.

---

## 8. Build it and prove it

Now the other route: real code and a real test. The **`@covers` mark** is the
one-line comment on the code that serves an intent; the **proof** is a test whose
*name* carries the acceptance criterion's ID, which is how the Gate knows which
test answers for which promise. `src/banner.py` is deliberately unmarked, a small
helper written along the way, the kind of thing block 11 will notice.

```bash
mkdir -p src tests
cat > src/greet.py <<'EOF'
"""The greeter.

@covers AC-GREET-10
"""


def greet(name):
    return f"Hello, {name}!"
EOF
cat > src/banner.py <<'EOF'
"""A little helper written along the way. It carries no @covers mark."""


def banner(text):
    return "=" * len(text)
EOF
touch tests/__init__.py
cat > tests/test_greet.py <<'EOF'
import unittest

from src.greet import greet


class GreetTests(unittest.TestCase):
    def test_AC_GREET_10_greets_by_name(self):
        self.assertEqual(greet("Tom"), "Hello, Tom!")
EOF
cat > specs/greet/tasks.md <<'EOF'
# Tasks — Greeter

- [x] T001 Build the greeter and write its proof — **Carries**: AC-GREET-10
EOF
python3 -m unittest discover -s tests -t .
bash .specify/extensions/specassay-check/scripts/check-traceability.sh
python3 -c "import json;[print(r['id'], r['status']) for r in json.load(open('trace-manifest.json'))['rows']]"
```

**You should now see** the test pass, the Gate pass, and the row move:

```text
Ran 1 test in 0.000s

OK
Wrote trace-manifest.json (1 rows) gate.ok=True
SpecAssay Check (Gate 2): OK (1 registry IDs)
AC-GREET-10 proven
```

(Rewriting `tasks.md` ticks the task's checkbox, `- [ ]` to `- [x]`, now that the
work is done. A ticked task is no longer an open admission of debt, which is
exactly what block 9 is about to exploit.)

**`proven`** is a narrow claim, and worth reading precisely: a named carrier
exists. It is a fact that a test named for this criterion exists, not a claim
that your code is correct. By default the Gate matches the test by *name* without
running it, and says so in the manifest as `gate.executionVerified: false`. Point
the config's `test_results:` key at a JUnit XML file from your own test run and
`proven` then requires a *passing* test; the Gate never silently upgrades the
claim behind your back.

---

### The four states, in one table

You have now produced three of the four states a row can be in. The fourth,
`backlog`, is what you would have seen in block 7 had you written the open task
*without* the spec, an ID minted on purpose and not picked up yet:

| What exists for the ID | State | Gate |
| --- | --- | --- |
| An open task carrying it, nothing else | `backlog`, anointed backlog: minted on purpose, not picked up | passes |
| A spec and an open task carrying it | `tracked-debt`: started, proof owed, admitted | passes |
| A spec, a task, and a test named for it | `proven`: a named carrier exists | passes |
| A spec and a test, but no task | `proven` | **refuses**: `registry ID missing from tasks` |
| Nothing (block 6), or a ticked task and no test (block 9) | `GAP` | **refuses**: `silent gap` |

Rows three and four together are worth a second look: a row can read `proven` and
the Gate can still refuse, because the states describe one ID while the refusals
also police whether the registry, the specs, and the tasks agree on which IDs
exist at all. (Each of the five lines above was run on 2026-09-15 against the
pinned versions; blocks 6 to 9 produce three of them in front of you.)

---

## 9. Break it on purpose

Green is a screenshot. Red is the demo. Rename the proof so it no longer names the
criterion: the same move as deleting the test, but sneakier, because the test
suite stays green.

```bash
cat > tests/test_greet.py <<'EOF'
import unittest

from src.greet import greet


class GreetTests(unittest.TestCase):
    def test_greets_by_name(self):
        self.assertEqual(greet("Tom"), "Hello, Tom!")
EOF
python3 -m unittest discover -s tests -t .
bash .specify/extensions/specassay-check/scripts/check-traceability.sh
echo "exit: $?"
python3 -c "import json;[print(r['id'], r['status']) for r in json.load(open('trace-manifest.json'))['rows']]"
```

**You should now see** a passing test suite *and* a refusing Gate:

```text
Ran 1 test in 0.000s

OK
FAIL: silent gap: AC-GREET-10 has no test and no open tracked-debt task
Wrote trace-manifest.json (1 rows) gate.ok=False
SpecAssay Check (Gate 2): FAILED
exit: 1
AC-GREET-10 GAP
```

That gap between the two lines is the whole point of the tool. Your tests are
green. Your promise is unanswered. Nothing in an ordinary CI run would have told
you, because the code still has its `@covers` mark and the task is still ticked:
it *looks* finished. **`GAP`** is the state for exactly this: an acceptance
criterion with neither a proof nor an open debt, so the Golden Thread (the line
tying intent to build to proof) is broken, and the Gate refuses. Exit code 1 is
what would fail your build.

---

## 10. Fix it

```bash
cat > tests/test_greet.py <<'EOF'
import unittest

from src.greet import greet


class GreetTests(unittest.TestCase):
    def test_AC_GREET_10_greets_by_name(self):
        self.assertEqual(greet("Tom"), "Hello, Tom!")
EOF
bash .specify/extensions/specassay-check/scripts/check-traceability.sh
echo "exit: $?"
python3 -c "import json;[print(r['id'], r['status']) for r in json.load(open('trace-manifest.json'))['rows']]"
```

**You should now see** green again, and the row back where it was:

```text
Wrote trace-manifest.json (1 rows) gate.ok=True
SpecAssay Check (Gate 2): OK (1 registry IDs)
exit: 0
AC-GREET-10 proven
```

Green, red, green. You have now seen the Gate pass work it can vouch for and
refuse work it cannot, on a thread you minted yourself.

---

## 11. Land the Thread Report

The **Thread Report** is the briefing SpecAssay posts on a pull request: what
moved on the thread, the touched story walked top to bottom, and the changed files
that sit **off the thread**, changed but carrying no mark tying them to an
intent this change moved. It illuminates; it never refuses. In CI it runs on every
pull request and posts one comment; here you run it by hand, comparing the
snapshot you saved in block 7 against the thread as it stands now.

```bash
git add -A && git commit -qm "Build and prove AC-GREET-10"
git diff --name-only thread-base
git diff --name-only thread-base | python3 .specify/extensions/specassay-check/scripts/thread-report.py \
  --base base.trace-manifest.json \
  --head trace-manifest.json \
  --changed-files - \
  --config .specify/extensions/specassay-check/specassay-check-config.yml \
  --project-root . \
  --out thread-report.md
cat thread-report.md
```

**You should now see** the five changed files, then the report:

```text
## 🧵 Thread Report

🟢 **Golden Thread intact**

### What moved
- 🟢 **`AC-GREET-10`** — `tracked-debt` → **`proven`** · `test_greet.py` `greet.py`

### Thread Status
**GREET**

| ID | Status | |
|----|--------|--|
| `AC-GREET-10` | 🟢 proven | ◀ changed |

### Off Thread
2 changed files sit **off the thread** — changed, but nothing in them carries a mark tying it to an intent this PR moved. Not a defect (a refactor and unwanted scope look identical here); just worth a glance:

- `src/banner.py`
- `tests/__init__.py`
```

Read it as a reviewer would. *What moved*: one promise went from admitted debt to
proven, and here are the two files that did it. *Thread Status*: the GREET story
as it stands after the change. *Off Thread*: `src/banner.py`, which you wrote,
which is harmless, and which nothing in the repository ties to any stated intent.
The tool refuses to guess whether that is a tidy-up or scope nobody asked for,
because from here those look identical; it hands you a spotlight, not a verdict.

`--project-root .` is not optional: without it the tool measures paths from the
config file's own directory and reads every changed file as off-thread.

---

## 12. Open Loupe and look at what you made

**Loupe** is a viewer for the emitted file: it reads a `trace-manifest.json` and
nothing else: it never re-scans your repository and never mints anything.

```bash
echo "Load this file into Loupe: $PWD/trace-manifest.json"
```

Open **<https://loupe.dryfoos.com/app/>**, click **Load Manifest…**, and pick the
path that command printed.

**You should now see** one row, `AC-GREET-10`, green, with the header reading that
the Golden Thread is intact. That is the same file the Gate wrote in block 10 and
the same file the Thread Report read in block 11: one small, portable record of
what you promised, what carries it, and what proves it.

Want to see the other color? Redo block 9 (break the proof), rerun the Gate, and
load the file again: one row, red, and a header saying the thread is broken. The
manifest is written on refusal too, so the break is in the file, not just on your
screen.

---

## What just happened

You put one promise into a registry, built it, proved it, and watched a
deterministic check agree, then broke the promise quietly, and watched the same
check refuse while your test suite still said everything was fine. The file it
emitted, `trace-manifest.json`, carries that whole story in a form a viewer, a
reviewer, or a colleague three years from now can read without you in the room.
The Thread Report turned that file into a briefing about one change: what moved
on the thread, and what changed alongside it that nothing on the thread accounts
for.

**The next step.** This page is step one, see a Thread Report on a toy project
you built in a sitting; step two raises a full governed estate, a real repository
under the thread with the orchestration layer driving it, and lands when its own
trial completes.

---

## When you stumble

Everywhere you stumble is a finding, not a failure: this page is on trial as much
as the tool is. Reply to whoever sent you here with:

1. **The block number** you were in.
2. **The command** you ran.
3. **What you actually saw**: the last ten lines or so, pasted, unpolished. Do
   not clean it up, and do not fix it silently: a workaround you found and did not
   report is a stumble the next person repeats.
4. **Anything the page assumed that was not true on your machine**: a missing
   tool, a different version string, a prompt this page did not mention.

Two more things worth reporting even though they are not stumbles: **how long the
sitting actually took you**, start to finish, including reading (this page claims
no number of minutes because no cold operator has produced a measured one yet;
yours would be the first), and **any step where you had to stop and think about
what a word meant**.

Findings land in this repository's running log, `docs/docs-gaps.md`, each with
what broke, how it was found, and what closed it.

---

## Clearing up

The tour project is disposable. When you are done with it:

```bash
cd ~ && rm -rf specassay-tour
```

That removes the project and everything this page installed into it. uv and the
`specify` CLI stay on your machine; `uv tool uninstall specify-cli` removes the
CLI too, if you would rather end where you started.

---

*This walkthrough is `FR-DOCS-60` in this repository's own registry: see
[`PRD.md`](./PRD.md).*

*It is also published as a web page at
[www.specassay.com/start](https://www.specassay.com/start), which
is rendered from this file at whatever commit `main` carries. That page holds no
copy of these words: this file is the source, so corrections belong here and
reach the page on its next build.*

*Next, when you want the full reference rather than a walkthrough: the
[README](./README.md) for what SpecAssay is and how it installs into a real
project, [`PROMOTION-CONTRACT.md`](./PROMOTION-CONTRACT.md) for the rules the Gate
enforces, [`docs/thread-report.md`](./docs/thread-report.md) for the Thread Report
in CI, and [`docs/troubleshooting.md`](./docs/troubleshooting.md), where every
entry was taught by a real incident.*
