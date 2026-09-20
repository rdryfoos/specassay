# SpecAssay Quickstart

## See a Thread Report

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

> **Not into hand-holding and wanna dive right in?**
> [https://github.com/rdryfoos/specassay](https://github.com/rdryfoos/specassay)

> <!-- site:divider -->
> **Starting from a machine with nothing on it?**
> A companion page sets the machine up first, and it is read in the terminal
> rather than in a browser. Paste
> `curl -fsSL https://specassay.com/FIRST-LIGHT | less` and it comes to you.
> Three steps: it installs Claude Code, signs you in, and hands you a blank page
> to write down what you are actually promising, in your own words, which is half
> an hour and the part it exists for. Reading it changes nothing on your machine,
> and you can come back here at any point: block 1 checks what you have rather
> than assuming it.

---

## Pinned, as of 2026-09-17

| Thing | Pinned to |
| --- | --- |
| SpecAssay | **v0.5.1**, released 2026-09-17. This is what `specify bundle install` gives you, and it is what every receipt below was captured on. |
| GitHub Spec Kit | **v1.0.4**. SpecAssay's manifests accept `>=0.14.0,<2.0.0`, and the floor was checked at v0.5.1 on 2026-09-17: the bundle installs and the Gate runs on Spec Kit 0.14.0, though that version does not scaffold the settings file, so the Gate there reports `config: MISSING` and continues on defaults. v1.0.5 and v1.0.6 exist and the manifests accept them; they are not what this page was captured on. |
| uv | 0.8.17 |
| Python | 3.11.15 |
| git | 2.43.0 |

**Where the receipts come from.** Every block below was run in order, on
2026-09-17, against those exact versions, and the output quoted under each block
is that run's real output, trimmed to the lines that carry the receipt, never a
sketch of what it might say. All twelve were re-captured that day on v0.5.1. The
previous capture was on v0.4.13, and every receipt reproduced unchanged, which is
worth knowing and is not the same as having assumed it. That run was on Linux,
not a Mac.
macOS and Linux are both first-class for these commands, and the only difference
we expect is the `python:` version string and your own paths. **If your Mac shows
anything else different, that difference is a finding: report it** (see *When
you stumble*, at the end).

An unpinned quickstart rots silently, so this one carries its versions and its
date. If you are reading it long after 2026-09-17, the versions above are what it
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
  ([Spec Kit v1.0.4 installation guide](https://github.com/github/spec-kit/blob/v1.0.4/docs/installation.md)); <!-- specassay:pinned Spec Kit -->
  block 2 says what to do if yours is older.

You run every block below in your terminal, inside a Claude Code session or in a
plain shell, your choice. Nothing here needs Claude Code to *do* anything for you
yet; step one is you driving the tools by hand, so you can see what each one
actually does.

**If the commands look daunting, skip them.** They are here so the page is
runnable, not because you have to read them. Every block opens with a plain
sentence or two saying what it is about to do and why, and closes with a plain
sentence saying what just happened. Read only those, skip every grey box in
between, and you will still come out understanding what this tool is for. That
is a real claim about this page, not a courtesy: it was written to survive a
reader who never types a single line.

---

## 1. Check the machine

Three tools have to already be on this machine: git, Python, and a Python
installer called uv. This block just asks each one its version, so you find out
now rather than three blocks in.

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

Nothing has been installed or changed yet. You have only confirmed the machine
is ready.

If `git --version` or `python3 --version` fails on a Mac, the usual fix is
`xcode-select --install`, which installs Apple's command line tools; rerun this
block afterward. If `python3` is still missing, or older than 3.8, install a
current Python from [python.org](https://www.python.org/downloads/) or Homebrew.

---

## 2. Install Spec Kit, pinned

SpecAssay is not a standalone program. It attaches to **Spec Kit**, which is
GitHub's toolkit for writing down what software should do before building it. So
Spec Kit gets installed first, and pinned to one exact version, so that what you
see on your screen matches what is written on this page.

**uv** is the Python tool installer Spec Kit ships through. Skip the first line
if block 1 already printed a uv version.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.0.4
specify --version
```

**You should now see** the pinned version, exactly:

```text
specify 1.0.4
```

Spec Kit is now on your machine, at the version this page was written against.
It has not been pointed at any project yet.

If `uv tool install` stops saying it cannot find a suitable Python, run
`uv python install 3.11` and repeat the `uv tool install` line; that fetches a
Python for uv's own use and leaves your system Python alone. If `uv` is not found
after the install script, open a new terminal window first: the installer adds it
to your `PATH` for new shells.

---

## 3. Make the sample project

Now a throwaway project to work in, so nothing on this page touches anything you
care about. You can delete the whole folder when you are done and nothing else on
your machine will change.

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

You now have an empty project with Spec Kit's own scaffolding in it, and one
commit recording what it looked like before SpecAssay arrived.

Two notes on what just happened. `specify init` does **not** create a git
repository for you at v1.0.4 (git is an opt-in Spec Kit extension), <!-- specassay:pinned Spec Kit -->
which is why
you ran `git init` yourself; the Thread Report in block 11 needs git history to
know what changed. And the `.gitignore` line keeps the tour's emitted files out of
git so the Thread Report's file list stays about your code; in a real repository,
whether you commit the emitted manifest is your call, and CI emits it either way.

---

## 4. Layer in SpecAssay

Time to add SpecAssay itself. It arrives as two pieces: a **preset**, which
changes what Spec Kit's templates ask you to write, and an **extension**, which
is the Gate, the check that reads what you wrote. Block 5 is where the Gate
starts doing something.

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

SpecAssay is installed. Nothing has been checked yet, because you have not
written anything down for it to check.

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

You just installed the thing this page is about, so here is what it is. The
**Gate** is a check you run, the way you run your tests. It reads two kinds
of thing you already write: the promises you have written down in plain English,
and the code and tests in your repository. Then it answers one question. **For
every promise you have written down, is there something in this repository that
answers for it?** If yes, it passes. If a promise has quietly ended up with
nothing behind it, it refuses and names the promise.

That is the whole idea. Everything else on this page is you giving the Gate
something to check and watching what it says.

The promises live in one file, called the **registry**. Yours will be `PRD.md`,
which the Gate reads by default. Each promise in it gets a **durable ID**, a name
like `AC-GREET-10` that you give it once, when you decide to promise the thing,
and never renumber afterwards. The name is what lets the Gate match a promise to
the test that answers for it, so the name has to hold still.

You have not promised anything yet, and that is deliberate. Running the Gate on
an empty registry first is the clearest way to see what it means when it says
yes. So make the empty file and run it.

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

**What just happened, in one sentence:** the Gate passed, and then told you the
pass was worth nothing.

That is the sentence to take from this block. Most tools that pass go quiet. This
one passed and immediately said so in plain words: *nothing is promised yet, so
there is nothing to check*, and *this green proves nothing*. It will keep saying
that until you promise something.

Think about what the alternative would look like. A check that reads an empty
registry, finds no broken promises, prints `OK`, and stops has told you the truth
and left you with a false impression. You would be looking at a green result on a
project where nothing has been checked at all. Refusing to take credit for that
is the first honest thing this tool does, and it is the same instinct behind
everything it does later: a pass always comes with the scope of what was actually
examined.

Two smaller things from that output, which you can take on trust for now.

The Gate wrote a file called `trace-manifest.json`. That is its record of what it
found: every promise, what state each one is in, what carries it, what proves it,
and whether the Gate passed. It is a small plain file, and it is the thing other
tools read later in this tour, in blocks 11 and 12, instead of scanning your
repository again. A second file with `v5beta` in the name is a draft of the next
version of that format; ignore it here.

The first three lines of every run tell you which Python it found and which
settings file it is using. Worth a glance each time. If that third line ever says
`config: MISSING`, the Gate keeps going on built-in defaults and prints the one
command that creates the settings file for you.

(The output above is abridged in one place: the real run prints the full command
for each of those two on-ramps, which is too wide for this page.)

---

## 6. Mint one toy promise

Now write down exactly one promise, and nothing else. No code, no test, no plan.
Then run the Gate again and watch it refuse, because a promise with nothing
behind it is precisely what it is looking for.

**Minting** is the word for writing a promise into the registry at the moment you
decide on it, rather than working out afterwards what the code seems to have
promised. `mint-id.sh` picks the next free number (always a multiple of ten) and
appends the line in the file's own style.

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

**What just happened:** you wrote down a promise, and the Gate stopped your
build over it.

Three refusals, and all three are correct. You have promised something
(`AC-GREET-10` is an **acceptance criterion**: one testable statement of what
"done" means) and nothing in the repository answers for it yet. The third line is
the core refusal, a **silent gap**: an acceptance criterion with neither a proof
nor an openly admitted debt. The Gate wrote `trace-manifest.json` anyway; it
records refusals rather than hiding them.

---

## 7. Give it a spec and a task

There are two honest ways to answer that refusal, and the difference between them
is the point of the whole tool. This block takes the first one: admit the work is
not done yet. You are not going to write any code here. You are going to say, on
the record, that this promise is started and its proof is still owed, and the
Gate is going to accept that and go green.

Mechanically that means a **spec** (the Spec Kit feature document that references
the ID, never re-mints it) and an open **task** carrying a `**Carries**:` mark
(the task-side line naming which ID that task serves).

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

**What just happened:** you cleared a refusal without writing a line of code, by
admitting in writing that the work is unfinished. That is allowed, and it is
supposed to be.

**`tracked-debt`** means started, proof missing, and admitted on an open task:
visible, on the books, not hidden. That is why the Gate passes: passing never
means "everything is done", it means nothing unfinished is *hidden* at
acceptance-criterion altitude.

The last three lines set up block 11. `base.trace-manifest.json` is a snapshot of
the thread as it stands right now, and the `thread-base` tag marks the commit it
belongs to; the Thread Report compares *before* against *after*, so it needs both.

---

## 8. Build it and prove it

Now the second honest answer: actually do the work. Write the code, write a test,
and name the test after the promise so that a machine can see which test answers
for which promise. That naming is the whole trick, and it is the only thing this
tool asks you to do differently from normal.

The **`@covers` mark** is the
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

**What just happened:** the promise moved from admitted debt to answered, because
a test now carries its name. You did not tell the Gate that. It worked it out
from the test's name.

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

This is the block the tool exists for, so it is worth reading even if you read
nothing else. You are about to break the link between the promise and the test
that answers for it, by renaming the test. Nothing else changes. The code still works. The test
still passes. Your test suite will report success. On any ordinary project this
is invisible, and it is how a promise quietly ends up with nothing behind it:
nobody deleted anything, a name just drifted.

Watch what the two tools say about the same repository.

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

**What just happened:** your test suite said everything is fine, and the Gate
said a promise has nothing answering for it. Both are correct, about the same
repository, at the same moment. That disagreement is the thing this tool was
built to produce.

That gap between the two lines is the whole point of the tool. Your tests are
green. Your promise is unanswered. Nothing in an ordinary CI run would have told
you, because the code still has its `@covers` mark and the task is still ticked:
it *looks* finished. **`GAP`** is the state for exactly this: an acceptance
criterion with neither a proof nor an open debt, so the Golden Thread (the line
tying intent to build to proof) is broken, and the Gate refuses. Exit code 1 is
what would fail your build.

---

## 10. Fix it

Put the name back. That is the entire fix, and it is worth noticing how small it
is: the repair for a broken promise here is to say again, in the test's name,
which promise it answers.

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

**What just happened:** the promise is answered again, and the Gate went green
without being told to.

Green, red, green. You have now seen the Gate pass work it can vouch for and
refuse work it cannot, on a promise you wrote yourself. If you stop reading here,
you have the idea.

---

## 11. Land the Thread Report

The Gate answers one question: does anything have a promise with nothing behind
it. That is a yes or a no, and it is the half that can stop a build. This block is
the other half, the half that talks to a person.

The **Thread Report** is a short briefing posted on a change, saying what that
change did to the promises: which ones moved, and which files were edited that no
promise claims. It never refuses anything. It just tells the reviewer what to
look at.

One line saying what this change did, and under it what moved and which changed
files sit **off the thread**, changed but carrying no mark tying them to an intent
this change moved. It illuminates; it never refuses. In CI it runs on every
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

🟢 **Golden Thread intact** · **1** proved · **2** files off thread

<details>
<summary><b>What moved</b> — 1 row in 1 family</summary>

**GREET**

| ID | Moved | Changed in |
|----|-------|------------|
| `AC-GREET-10` | `tracked-debt` → 🟢 **`proven`** | `test_greet.py` `greet.py` |

</details>

<details>
<summary><b>Off thread</b> — 2 changed files sit off the thread</summary>

Changed, but nothing in them carries a mark tying them to an intent this PR moved. Not a defect (a refactor and unwanted scope look identical here); just worth a glance:

- `src/banner.py`
- `tests/__init__.py`

</details>
```

**What just happened:** you got the paragraph a reviewer would get, generated
from the same file the Gate wrote, with nobody writing a summary by hand.

On a pull request those `<details>` blocks render as two collapsed lines you can
click open. Here in your terminal you are seeing the raw Markdown, tags and all,
which is the same text GitHub turns into that.

Read it as a reviewer would, starting with the one line at the top. That line is
the whole verdict: the thread is intact, one promise proved on this change, two
changed files sit off the thread. If nothing there surprises you, you are done
reading.

Click down when it does. *What moved* names the promise, the move it made
(`tracked-debt` → `proven`) and the two files that did it. *Off thread* names
`src/banner.py`, which you wrote, which is harmless, and which nothing in the
repository ties to any stated intent. The tool refuses to guess whether that is a
tidy-up or scope nobody asked for, because from here those look identical; it
hands you a spotlight, not a verdict.

The report shows what *moved*, and footnotes the rest. On a toy project with one
promise there is no rest; on a real one, a family's unchanged rows are summarised
under its table by status rather than listed, so the report stays about this
change without losing the state around it.

`--project-root .` is not optional: without it the tool measures paths from the
config file's own directory and reads every changed file as off-thread.

---

## 12. Open Loupe and look at what you made

One last look, at the file rather than the tools. Everything you have seen since
block 5 came out of one small file the Gate writes. This block opens that file in
something that has never seen your repository, to show that the record stands on
its own.

**Loupe** is a viewer for the emitted file: it reads a `trace-manifest.json` and
nothing else, it never re-scans your repository, and it never mints anything.

```bash
echo "Load this file into Loupe: $PWD/trace-manifest.json"
```

Open **<https://loupe.dryfoos.com/app/>**, click **Load Manifest…**, and pick the
path that command printed.

**You should now see** one row, `AC-GREET-10`, green, with the header reading that
the Golden Thread is intact. That is the same file the Gate wrote in block 10 and
the same file the Thread Report read in block 11: one small, portable record of
what you promised, what carries it, and what proves it.

**What just happened:** a tool that knows nothing about your project told you the
state of your promises, from a file alone. That portability is why the record
exists as a file instead of as output on a screen.

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
