# Changelog

All notable changes to the SpecAssay bundle. Versions follow [semver](https://semver.org);
the bundle version leads, component versions are listed per release.

## Unreleased

### A test's name, not every string in the file (FR-GATE-220)

A criterion is proven by a test whose *name* is the ID. The scan was a per-line
grep over the whole test file, which cannot tell a name from an argument, so any
string that happened to contain an ID read as a passing test.

Found in Loupe, 2026-10-02, running 0.5.5 against it: six IDs that appear nowhere
but inside fixture rows handed to a forest builder, written
`row({ id: "AC-UI-40", type: "AC" })`, read as six passing tests and produced 7 of
the 8 findings that run reported. Five of the six named domains Loupe's registry
has never had. Loupe's own titles, `it("AC-BUILD-10: ...")`, were right the whole
time.

The rule now reads the file for its convention. A file that declares even one
string-titled test is read strictly: only the start of the first string argument
to `it`, `test` or `describe` counts as a name, with any delimiter after the ID
(a colon, a space, a parenthesis), and an ID anywhere else in that file is data.
A file that declares none keeps the plain reading, because data cannot look like a
function name, so a function-named suite sees no change at all.

Measured on Loupe at `b045352`: **8 findings before, 1 after**, and all 84 of its
rows hold the status they had, so nothing it had honestly earned was lost. The one
survivor is Loupe's own, a task whose `**Carries**` reads `n/a` where the Gate
accepts `none`.

Where a registry row does lose a proof it only ever had by mention, the run says
so once, naming the row, the file and the line, rather than letting a status move
on upgrade without a word.

Narrowing `test_ac_regex` was never a workaround for this: every vitest, jest and
`node:test` project writes its names as strings, and has no shape to narrow to.

**A second law about awk, found writing this one.** The rule reads structure, and
structure only: the project's own ID grammar is matched by `grep`, never by awk.
awk's `match()` is not longest-match everywhere. Against the stock grammar,
mawk 1.3.4 returns `AC_GATE_10` for `AC_GATE_100a`, where gawk and grep both
return the whole ID, so the first cut of this change silently truncated every
three-digit ID on a mawk machine and left the Gate refusing a project over IDs it
had invented. Measured 2026-10-05. The existing guard against `awk -v` was about
escape processing and said to use the environment instead, which does not help:
the defect is the engine, not the channel. A second guard now reads every shipped
script for a configured pattern anywhere near an awk call.

## 0.5.5 (2026-10-02)

Components: bundle 0.5.5, extension 0.5.5, preset 0.5.5.

**A hotfix, and the release it carries.** 0.5.4 could not run on a Mac at all, and
said nothing about it. That is fixed here, along with the two blind spots that let
it ship. The rest of this release is the cold path, which reached a Thread Report
on a pull request with nobody building plumbing, and the Thread Report's plain-words
pass.

### The digests, and the pin table moves to 0.5.5

The three catalog digests, computed from the published assets rather than from a
local build, and agreeing with the digest GitHub reports for each asset:

```text
specassay-0.5.5.zip         2acb33dfa5ccf4b3e61de762355aba9d28b0f3396d44a4a4b7a40a484501d6e2
specassay-check-0.5.5.zip   c1c1ead275fd638960debc3c80a3da4af759f044612f72417e41aaea1f54cb8e
specassay-preset-0.5.5.zip  9bc17b8b8aeb58bc1c0c61099df398496794d3c40fcf8cd028a80077023376e7
```

Proved load-bearing rather than merely present: with one hex character changed and
the catalog served over localhost, `specify bundle install` refuses with
`Integrity check failed`, names both digests, and installs nothing.

**ONBOARD's pin table now reads v0.5.5**, because all thirteen blocks were replayed
on the released bundle, installed from these catalogs, with Spec Kit pinned at 1.0.4
from its own tag as block 2 says. Ten blocks reproduced unchanged. Block 4 reports
seven shipped scripts where it reported four, since the Gate became a launcher and an
implementation. And block 11's list of changed files no requirement claims is back to
**two**, correcting a capture taken earlier the same day: that one showed seven,
because it was taken in a project built by hand instead of by block 3, and block 3
writes a `.gitignore` that keeps the manifests and `__pycache__` out of the diff. The
page was right and the capture was wrong. Only replaying from block 1 finds that.

### 0.5.4 did not run on macOS, and reported success

`FR-GATE-200`. `check-traceability.sh` 0.5.4 does not parse under **bash 3.2.57**,
which is macOS's system bash and the only bash on a stock Mac. Found by the Spudnik
room on a Mac Mini, 2026-10-02, installing 0.5.4 the cold way from the catalogs.
The Gate ran nothing: no manifest, no verdict, no registry count.

One construct, introduced in 0.5.4 with the Carries value rule:

```bash
carries_verdict="$(
  CARRIES_LINE="$line" ... "$PYTHON" - <<'CARRIESPY'
  ...
CARRIESPY
)"
```

A here-document inside a command substitution. bash 4 and newer parse it; 3.2 scans
for the closing paren without honouring the here-document, reads the Python body as
shell, and the file then fails hundreds of lines later with an error naming neither
the line nor the cause, which is why the reported line numbers pointed into an
unrelated heredoc. The fix is to redirect the here-document to a file and read the
file.

**Which releases are affected: 0.5.4 only.** Established by scanning the script at
every tag from v0.5.0 to v0.5.4 for that shape, not by bisecting a symptom. 0.5.0,
0.5.1, 0.5.2 and 0.5.3 are clean.

### A check that cannot run is now red

`FR-GATE-190`, and the worse of the two defects. bash exits 2 on a parse failure,
which is honest, and two ordinary ways of calling a checker throw that status away:
a pipeline reports its last element's status, so `check | tail` is 0, and
`2>/dev/null` discards the message. Both measured on 2026-10-02. That is how a
Gate that ran nothing read as green.

`check-traceability.sh` is now a small launcher, deliberately plain enough for bash
3.2 to parse and run, around `check-traceability.impl.sh`, which is the Gate. The
launcher refuses three things the Gate cannot refuse from inside itself:

```text
SpecAssay Check (Gate 2): FAILED to run -- this bash cannot parse the check (bash 3.2.57(1)-release)
SpecAssay Check (Gate 2): FAILED to run -- the check exited 0 without writing a manifest, so there is no run to trust
SpecAssay Check (Gate 2): FAILED to run -- the check itself is missing at <path>
```

Each one is non-zero, each one names the bash that could not parse it, and each one
is printed on **both** stdout and stderr: a pipeline's status belongs to the filter
and no checker can change that, so the refusal goes where a piping caller reads it
instead of a verdict. The implementation touches a sentinel the moment the manifest
lands, and no exit 0 is allowed through without it. Tested with a deliberately
broken copy, three ways.

**Callers do not change.** `check-traceability.sh` is still the entry point every
document, command and workflow names.

### CI now runs on the platform its users are on

`FR-GATE-200`. `self-gate.yml` ran on Linux bash 5 only, so neither it nor the
cold-path end-to-end test could have caught this; both of that day's cold runs were
Linux too. The workflow is now a matrix over `ubuntu-latest` and `macos-latest`,
with every step on both, plus one the Linux job cannot have: the system bash's own
parse of every shipped script, named `/bin/bash` by absolute path, because `bash` in
PATH on a GitHub macOS runner is Homebrew's 5.x and an adopter's Mac is not.

A cheap guard runs on both runners as well: no shipped script may open a
here-document inside a command substitution, refused by shape. And `extension.yml`
now declares the floor it is tested against, `bash >= 3.2`, where it said `bash` and
meant whichever bash the author happened to have.

### The catalogs are checked against the release they claim

`FR-GATE-210`, from the 0.5.5 checklist. `catalogs/*.json` is what
`specify bundle install specassay` reads, and nothing checked it. The drift it was
written for: the extension and preset catalogs each carried a per-entry
`updated_at` of 2026-09-23 beside an entry describing 0.5.4, released 2026-10-01.
Now every entry's version and download URL must name the version `bundle.yml`
declares, a per-entry stamp may not disagree with its own file, the three files must
agree with each other, no stamp may be in the future, and the bash floor must be
repeated in the catalog, which is the copy an installer reads before anything is
downloaded. The digest stays outside the check, because the release pull request
removes it and the digests pull request restores it from assets that do not exist
until the tag.

### Two checklist items done, one deferred, and why

- **`docs/submission/CHEATSHEET.md` lines 21 and 271: done**, and the fix was a
  classification rather than a re-dating. Line 21 reads *"Filed 2026-09-23 at
  0.5.2"*, which names when something happened and can never be re-observed: it is
  provenance, and is now marked so. Line 271 says the community catalog resolves
  both components at 0.5.2, which is a version belonging to **another subject**, the
  class this checker grew for Spec Kit's own pins. Re-observed on 2026-10-02 against
  `catalog.community.json` for all three component types: still 0.5.2, because 0.5.3
  and 0.5.4 were deliberately not submitted and go in with the next filing. The page
  now says that.
- **`docs/trace-manifest-schema.md` line 99: done.** *"from v0.5.4 the value is
  checked"* was marked as a current claim, so it demanded an edit at every release
  while being a statement about history. Marked provenance.
- **ONBOARD's pin table: deferred, and it cannot be done here.** Moving the pin means
  replaying every block on the release being cut, and a faithful replay installs the
  released bundle from the catalogs, which do not exist until the tag. So the pin can
  only move after a tag, never inside the release pull request that precedes it. It
  stays at v0.5.1 with the reason it already carries, and the replay is a post-tag
  pull request against 0.5.5, beside the digests one.

### The cold path, and the report in plain words

Everything already on main for this release: #58 to #61 closed the five cold-path
gaps, and #62 rewrote every string the Thread Report prints. Their entries follow
below, unchanged from when they landed.

### The preset no longer looks like a finished install

`FR-COLD-10`. `specify preset add specassay` installs the templates and no Gate.
It printed `Preset 'SpecAssay' v0.5.4 installed`, `specify extension list` then
read `No extensions installed.`, and nothing between those two lines said the
check the templates name was absent (observed 2026-10-02, Spec Kit 1.0.5).

The preset manifest now declares the extension it depends on:

```yaml
requires:
  speckit_version: ">=0.14.0,<2.0.0"
  extensions:
    - id: "specassay-check"
```

so Spec Kit itself ends a preset-only install with the missing piece and the
command that resolves it:

```text
!  This preset depends on extensions that are not satisfied:
    specassay-check is not installed
      Install with: specify extension add specassay-check
```

A warning and not a refusal, because that is the only shape Spec Kit offers: its
own code records a missing dependency as a report rather than an install failure.
Spec Kit reads the key from 1.0.4 on <!-- specassay:pinned Spec Kit --> and older
releases ignore it, validating only `requires.speckit_version`, so the declaration
costs the floor the bundle still accepts nothing.

**And the three documents a stranger meets first now say which single line brings
the Gate**: the start page, this project's README, and the README that ships
inside the preset, which was the one teaching the preset-only install.

**What the 2026-09-26 ledger had half wrong.** It read as though the start page
pointed a stranger at the preset. It never did: both it and the README already
gave `specify bundle install specassay`. The defect was the silent install, not
the instructions, and saying so is cheaper than carrying a correction nobody
made.

### A registry to start from, and the grammar beside it

`FR-COLD-20`. Nothing in the install created a registry. The composed spec template
forbade minting where the user was standing (*"do not mint new IDs here"*),
`mint-id.sh` refused with `registry not found`, and the mint command's own
instructions told an agent to create the file empty. So the first thing a stranger
had to do after installing was invent a file nobody had described.

```bash
bash .specify/extensions/specassay-check/scripts/mint-id.sh --init
```

writes the registry from a seed the extension now ships. The seed states the ID
grammar in full, which was previously spread between a spec template, a
constitution template and a Gate refusal: the four types, a domain of 2 to 6
uppercase characters, two or more digits, the optional sibling letter, the decade
scheme and the reserved collision lane. It carries one example row of each of the
four types with the `**Authorship**:` mark on it, and says what the four
authorship words mean. `--init` never overwrites an existing registry.

**A mint now prints the whole line, not just the ID**, so no registry line is
composed by hand, and it takes the one field the tool will not fill in:

```bash
mint-id.sh AC LOGIN --authorship case --append "Given a wrong password, ..."
```

```text
AC-LOGIN-10
appended to PRD.md:
  - AC-LOGIN-10 — Given a wrong password, ... **Authorship**: case
```

`--authorship` is validated against the same four values the Gate accepts, so a
mint cannot write a value the Gate would refuse. Omitted, the row reads as
unassigned and the mint says so in one line. **Every row the documented command had
ever written came out unassigned**, which nothing in the command hinted at; that
was found reproducing the cold path rather than reasoning about it.

### A fenced registry line is a quotation, not a mint

`FR-GATE-180`. `FR-GATE-40` settled this in v0.4.x for `@covers` marks and test
names: <!-- specassay:provenance --> a mark inside a fenced code block is a
teaching example, and counting it as a live claim makes a document that explains
the tool refuse the project that reads it. The registry's own reader was left out
of that fix.

Found writing the seed above, which could not carry an example of the thing it
exists to explain: four fenced example rows produced three refusals each on a
project's first Gate run. Now the Gate's definition-line scan, its duplicate-id
detection, and `mint-id.sh`'s next-number, style and collision scans all read the
registry through one shared fence filter, so no two readers of the file can
disagree about what is minted. Lines are blanked rather than deleted, so every line
number the Gate reports still points at the real line.

**One upgrade hazard, stated rather than left to be discovered:** a project that
today has a fenced row which a spec or a task references will see that reference
turn into drift, named plainly, because the row it pointed at has stopped existing.
This repository's own registry was unaffected: 109 rows before the change and 109
after.

### The CI that posts the report now ships, and one command places it

`FR-COLD-30`. After a full install, `find .github -type f` returned nothing, so a
pull request ran nothing and no comment appeared. The plumbing a stranger had to
write for themselves was the 124-line workflow this repository had written for its
own example app: check out the base, run the Gate twice, collect the changed files,
call the report, post a comment through the API. Nothing in the installed tree so
much as used the words "Thread Report".

```bash
bash .specify/extensions/specassay-check/scripts/install-ci.sh
```

```text
wrote .github/workflows/specassay.yml (project root: .)
  On every pull request it runs the Gate on the head and on the base, posts one Thread Report comment saying what the change did to your promises, and fails the check if the Gate refuses. A local run before you push is still worth having; this is the run that protects the thread.
  Commit it along with .specify/, then open a pull request.
```

The extension carries `ci/specassay.yml`: one file, two jobs, no secrets. On every
pull request it runs the Gate on the head and on the base, builds the report, posts
one comment and updates it in place on later pushes, sets the `specassay/ack` status
when the config asks for a human tick, and then fails the check in a separate step,
so the red tick is the block and the comment never is. On an edit to that comment it
re-reads the ticks. A project in a subdirectory gets its own root written into the
workflow; nothing has to be edited by hand. `install-ci.sh` refuses rather than
overwrite a workflow that differs, printing the `diff` to look at first.

**Why a command and not the installer.** Spec Kit cannot place a file outside
`.specify/extensions/<id>/`. Its extension manifest provides commands, templates,
scripts and config and deploys every one of them under that directory; the only
`.github` paths the CLI writes are Copilot prompts and `.github/hooks/speckit.json`;
and hooks are agent-side events rather than install-time ones. Read from Spec Kit
1.0.5's own source <!-- specassay:pinned Spec Kit --> rather than assumed. So the
bundle ships the workflow and one documented command places it.

**A local run is still worth having** before you push, or through the
`after_implement` hook. It is hygiene; the pull-request run is what protects the
thread, because it happens whether or not the author has the tool installed.

**And the broken link is gone.** The extension README pointed at this repository's
own workflow by a relative path that resolved to nothing in an adopter's checkout,
which was the only account of this plumbing anybody had.

### The cold path is proved by walking it

`FR-COLD-40`, and `US-COLD-10` with it. One test builds a throwaway repository, puts
the bundle's files where an install puts them, and walks a stranger's whole path to
the text of a Thread Report comment: the registry from the seed, a green run on no
promises, one minted row with its author named, the first honest red, the spec and
the task, the CI installed, the build and its proof, and the report the pull request
would carry.

**It fails if any step is not a shipped command.** Every command is declared before
it runs, and the test refuses one that is neither a shipped script nor a plain `git`
call, so hand-built plumbing cannot be slipped in to make the path pass. That guard
is itself held to a test, because without it the test could be made green by adding
whatever the path turned out to need.

It runs as a named step in `self-gate.yml`, on every pull request and every push to
main: this is the one test whose failure means a stranger cannot get started, so a
reviewer should meet it by name rather than as one dot among a hundred and seventy.

**Writing it changed the design, which is why it was worth writing.** The four data
steps of the pull-request run were shell inside the workflow YAML, where no test
could reach them without re-typing them and letting the two drift. They now live in
`ci-thread-report.sh`, which the workflow calls and the test drives, so what CI runs
is what the proof runs. The workflow keeps only the two steps that need GitHub.

**What it does not cover**, said in the test rather than implied: GitHub posting the
comment. The comment's body is the marker line plus the report the test reads, so the
untested part is one API call in a step whose script is asserted separately. Covering
it would need a real repository and a real pull request.

This is the test the 2026-09-26 ledger lacked, which is why every one of that
ledger's five findings had to be re-derived by hand before any of this could be
fixed, and why one of them turned out to have been wrong.

### The Thread Report says what to do next, in plain words

`FR-THREAD-20`. The comment a reviewer reads now speaks in requirements, tests and
pull requests. The verdict line says the next action rather than the state of a
metaphor, in three states:

```text
🟢 **Ready to review** · **1** now has a test · **1** changed file no requirement claims
🟡 **Needs a person** · **1** reworded · **every changed file is claimed**
🔴 **Do not merge yet** · **1** has neither · **2** changed files no requirement claims
```

**Amber is the state the comment could not say before.** The Gate passes, and either
a requirement was reworded (its code and tests were written against the old wording)
or a `required` tick is waiting, which it always is the moment the report renders,
since a tick attests to one head and the report reposts on every push. A green line
in either case was true about the Gate and misleading about the merge.

Everywhere else: *Intent Changed* is **Reworded requirements**; *What moved* is
**What changed**, with `| ID | What changed | Where |`; *Off thread* is **Changed
files no requirement claims**; `re-confirm` is `check`; `🆕 minted` is `🆕 new`;
`✍️ restated` is `✍️ reworded`; `+1 proof` is `+1 test`. The authorship sentence
reads `1 requirement came from the case, 3 from the project (design 1, retrospective
1, constitution 1).`, and a count of one now agrees with itself: the verdict line
printed `1 files off thread` until today, while the fold summary under it said
`1 changed file` correctly, which is two readers of one count disagreeing inside one
comment.

**Three house words survive, in the comment's own last line, each with its
definition beside it**: Golden Thread, off thread, and mint. Nothing above that line
asks a reader to learn a word before acting.

**What deliberately did not change.** The four manifest states and their badges
(`proven`, `tracked-debt`, `backlog`, `GAP`), because a viewer renders them and
[`docs/trace-manifest-schema.md`](docs/trace-manifest-schema.md) defines them. Every
tick line's `- [ ] ` prefix and backticked `..._ack: required`)_ suffix, which three
workflows match by regex to hold a merge; a test now pins that shape so the words
inside can move again without the mechanism breaking. And the dated receipts in
`docs/submission/test-evidence.md` (lines 55, 151 and 184) and on demo pull requests
#1 to #5, which record what a past run printed and would be falsified by a rewrite.

The inventory behind the pass was taken by running the real script over twelve
fixture states rather than reading its source, with each of the strings paired to the
test, document or page that reads it. That is why the pass is one change rather than
a trail of small ones: twenty-three strings had a test reading them.

**Queued, not here:** Loupe prints `Golden Thread intact` and `Golden Thread broken`
itself, from the manifest rather than from this report, so one manifest is currently
described two ways; the Sites pages and the two baked hero images carry the old words
in their copy and alt text; the README inside the released zips regenerates at the
next cut.

### Before the next tag, two things this stack deliberately left alone

Neither is cold-path work, and both were ruled to wait rather than ride along here.

- **`docs/submission/CHEATSHEET.md` has two dated 0.5.2 observations**, at lines 21
  and 271. They warn at two releases behind and **refuse at three**, which is the
  next cut: the doc-version check goes red until they are re-observed on the release
  being cut, or given a stated reason to keep (`<!-- specassay:stale-ok why -->`).
  Re-observe them rather than marking them: they are receipts of a real run, and the
  honest fix is another real run.
- **ONBOARD's receipts span two dates now.** Blocks 5, 6 and 12 were captured on
  2026-10-02 against this unreleased change; the other ten are the 2026-09-17 run on
  v0.5.1, <!-- specassay:stale-ok the record of which run each block came from; re-observing it is the replay this very line asks for -->
  and the pin table still names that release. Replaying every block on the release
  being cut is what lets the pin move, and it is the open item the 0.5.4 release
  pull request already named.

## 0.5.4 (2026-10-01)

Components: bundle 0.5.4, extension 0.5.4, preset 0.5.4.

Two things a registry could not say before, and one consequence of the clock.

### A registry row can say who asked for it

`FR-GATE-160`. Every row can now name **who authored it**, in a field of its own
called `authorship`, declared on the registry line and carried on the v5 row:

```markdown
- AC-PAY-10 — Given a declined card, when checkout submits, then the reason is shown. **Authorship**: case
```

Four values and no fifth. **`case`**: the row states a promise from the project's
CASE, in the reader's words or on their behalf. **`design`**: a design decision,
a screen rule, a control, an order, something the reader assumed rather than
promised. **`retrospective`**: minted from a retrospective or a defect.
**`constitution`**: a principle demanded the row, not that the row sits in
`CONSTITUTION.md`.

**A sentence carrying two authors** takes the authorship of the clause that
caused the row to be minted. The other clause is a finding for the registry's
owner, not a second value. There is no list value: a row none of the four will
take is a finding to report, not a reason to invent one.

**The Thread Report says it in one sentence above the table**, so the question
"did the business ask for this, or did we decide it?" is answered without
opening anything:

> 10 promises from the case, 21 from the project (design 19, retrospective 2, constitution 0).

**What a project with an unfilled registry sees.** A row with no authorship is a
**diagnostic naming the ID**, not a failure: every registry predates this field,
and refusing an unfilled row would red an adopter on upgrade for work nobody has
asked them to do. A row whose value is **outside the four fails**, naming the ID
and the value, because a row claiming an author that does not exist reads as
answered. While any row is unassigned the report says how many rather than
presenting part of the registry as the whole.

**It is deliberately not the `origin` field**, which already shipped on every v5
row meaning where the row lives (`{kind: "registry-line", path, line}`) and whose
`ledger` kind belongs to another emitter. One word must not carry both.

### A Carries mark must name what it carries

`FR-GATE-170`. Reported by the Bang room: the check tested only that the mark was
**present**, so `**Carries**: TBD` satisfied it. A task could declare that it
carried something and name nothing, which is the undeclared debt this tool exists
to refuse, sitting inside the field that exists to declare it.

The value is now read as the run of registry-shaped IDs after the mark and is
valid in two forms: **one or more registry IDs**, optionally followed by prose on
the same line, or **exactly the word `none`**, meaning this line carries no
promise. `none` is a hand's declaration at promotion time; the Gate never writes
it and never infers it from silence. Anything else fails, naming the task and the
value: `TBD`, an empty value, and the near misses `nothing`, `n/a` and `later`.

Reading stops at the first token that is not an ID rather than refusing the rest
of the line, because a task that names its IDs and then says why on the same line
is the normal shape, not an error.

**`none` lines are counted, never hidden.** `totals.carriesNoneCount` carries the
number and the Thread Report says it in words beside the authorship sentence, so
a registry whose edges are thinning is met as a sentence.

### What a project still on 0.5.1 observations will now see

`check-doc-versions.py` refuses an observation three releases behind the version
being cut. **At 0.5.4, a doc line dated against 0.5.1 crosses that line:** a
project whose docs still quote 0.5.1 numbers will see those lines refuse where
0.5.3 only warned, naming the file and line. The fix is the one the message
names: re-observe the number on the release being cut, or write the reason for
keeping the old one into the page with `<!-- specassay:stale-ok why -->`. This
repository's own eight such lines were re-read as part of this cut.

### Everything else since v0.5.3

Read from the log rather than recalled: `58f0802..main` carries exactly two
commits, `1492853` (the 0.5.3 digests, restoring `sha256` to the three catalogs
once the v0.5.3 assets existed) and `60b7e27` (authorship, above). There is
nothing else in this cut.

## 0.5.3 (2026-09-25)

Components: bundle 0.5.3, extension 0.5.3, preset 0.5.3.

A single-defect patch. No behaviour changes for input that was already
correct; nothing new is minted beyond the IDs that carry the fix.

### A line ending is not a verdict

`FR-GATE-150`, `AC-GATE-150`, `AC-GATE-150b`. Found on the first Windows run
of the Bang walk, 2026-09-24, Git Bash with Python 3.12.10: the Gate returned
`"ok": false` with eleven failures, every one of the form

```text
untraced scope (test name): AC-UI-10\r not in registry
```

beside `proven` rows for those same IDs and `GAP: 0`. Nothing was wrong with
the code under test. The Gate was failing on its own plumbing.

The junit filter rewrote `test_acs.txt` with `open(path, "w")`, whose text
mode emits `\r\n` on Windows, and the three Bash comparisons downstream
compare byte for byte: `grep -qx` against the registry at the orphan-test
check, `grep -qx` again at the silent-gap check, and `comm -23` against the
covers set at uncovered-proof. `AC-UI-10\r` matches none of them. What made
it read as a data problem rather than a line ending one is that the
manifest's own reader strips each line, so the statuses stayed right while
the failures beside them were impossible. That is the capture-method failure
`PROMOTION-CONTRACT.md` rule 12 names, one platform over: two readers of one
file disagreeing, and the tool reporting the disagreement as a fault in the
work.

**Fixed at both ends, deliberately.** The writer takes `newline="\n"`; the
Bash normalizes the file with `tr -d '\r'` after the filter runs. Either
alone closes the reported bug, and neither alone survives the other end being
replaced by an older extension left in a project, a shim, or an editor.

**The config readers strip too**, found while surveying for others of the
same kind. `yaml_scalar` and `yaml_list` took the rest of the line verbatim,
so a `specassay-check-config.yml` checked out under Git for Windows' default
`core.autocrlf=true` would parse `registry: "PRD.md"` as a filename carrying
a carriage return and refuse with `registry not found: PRD.md`, naming a file
that is right there. The Windows run that found the first defect never hit
this one, because the installer writes the config with LF.

Reproduced on Linux before anything was changed, by injecting a
`SPECASSAY_PYTHON` shim that rewrites the handoff files the way Windows text
mode does, and the four tests in
`extensions/specassay-check/tests/test_gate_150_crlf_handoff.py` were
confirmed red on the pre-fix script first. They are permanent.

### Housekeeping

- The two `0.5.0` mentions in `PRD.md` were re-read and marked provenance:
  each names *when* a decision was taken, not a number observed on a release,
  and they had been ageing as observations on the strength of the dates
  around them.
- The 0.5.2 submission drafts are marked as the record of a landed round
  rather than a current claim, now that #4711, #4713 and #4715 have merged.

## 0.5.2 (2026-09-23)

Components: bundle 0.5.2, extension 0.5.2, preset 0.5.2.

**Corrected 2026-09-25: the catalogs moved to v0.5.2 and the round landed.**
This entry shipped saying the catalogs would stay pinned at v0.5.1 while
#4690, #4691 and #4692 were under review. That ruling was reversed two days
later and the sentence stopped being true; it is corrected here rather than
deleted, because the reversal is the lesson. Spec Kit's validator reads
`bundle.yml` on the **default branch**, not the tag an issue names, so
publishing v0.5.2 while those three were open invalidated them the moment
`main` carried the new manifest: #4692 was refused on exactly that mismatch
and the other two were pre-empted. The catalogs then moved with the refiling,
and `catalogs/*.json` have read 0.5.2 since. The refiled #4711, #4713 and
#4715 landed on 2026-09-24 as merged catalog PRs #4735, #4717 and #4737,
with the three community catalogs now carrying 0.5.2. The rule this bought
is written up in `docs/submission/CHEATSHEET.md`: **freeze the manifest while
a submission is open.**

### A task is one logical line, however many lines it occupies

`FR-GATE-140`. A `**Carries**:` list that soft-wraps onto a continuation line now
carries the same IDs it would carry unwrapped, and the mark counts wherever in
the task it sits. Before this, two scans read one `tasks.md` and disagreed one
line apart: the exact-set scan read every line and counted a wrapped ID as
claimed, while the pending scan matched only the physical `- [ ]` line and never
saw it. The Gate reported a silent gap where the truth was that two parsers
differed, which is rule 12 inside the tool that exists to refuse it.

**Ruled fold rather than refuse.** Refusing a wrapped list would make an author
break their wrapping to satisfy the parser, red every adopter whose `tasks.md`
already wraps, and put the parser's limitation on the author. Found in the Bang
rehearsal on v0.5.1, where three acceptance criteria reported as gaps for no
reason a reader could find.

**Upgrade note:** if a wrapped `Carries` list has been reporting phantom gaps,
they disappear on upgrade. No registry change is needed and no status is
reclassified: this repository's own manifest was diffed row by row and nothing
moved.

### `trace-manifest.v5beta.json` writes `parents[]`, the spelling its spec declares

The v5 rows are built from the v4 rows, so v4's scalar `parent` rode through and
`parents` was never written. Every edge the Gate has derived since `FR-GATE-90`
was present under a name no v5 reader looks for, and invisible to the one viewer
built to draw it. On this repository's own manifest: 35 rows carried the
singular and none carried the plural; now 35 carry the plural and none the
singular.

**v4 is unchanged and keeps `parent`.** It is a frozen contract with strict
validators, and renaming a field there is not a spelling fix. A row with no
parent gets `[]`, which the v5 doc already reads as the domain-grouping
fallback, so no edge is invented.

**Consumers of `trace-manifest.v5beta.json` that read `parent` must read
`parents` instead.** Nothing reading v4 alone changes.

### The objective tier, minted as intent only

No code. `PRD.md` gains an `OBJ-` tier above story, in the practice's own order:
the promise first, the build later. `CASE.md` holds bets, scored by measures in
the world; `PRD.md` holds promises, proven by named tests; a green objective
means its promises were kept, not that the bet paid. Objective IDs are assigned
by the Gate and written back into `CASE.md`, never typed by a person, and the
Gate never renumbers. Objectives are read by heading, so any numbering on the
CASE template's questions is decoration.

Release cut lines (`Release: <name>`, a declared short list, an exact-set check)
are minted in the same pass and sequenced behind the tier.

Twenty-five rows, every one anointed backlog. **Nothing in this section changes
the Gate's behaviour in 0.5.2.**

### Also in this release

- The preset README carries a pinned release install line beside the
  version-agnostic one, because a catalog entry's documentation has to show the
  exact download URL the entry declares.
- `docs/submission/` records the 0.5.1 catalog resubmission: #4690 extension,
  #4691 preset, #4692 bundle, superseding #4649, #4650 and #4651, with the
  validator run IDs and what each earlier issue failed on.
- `FIRST-LIGHT.md` is served as a page at `specassay.com/bang` rather than piped
  into a pager, and its prose no longer assumes a terminal. `ONBOARD.md` carries
  the marker that page's build anchors on.

### A stale version number is now refused, not noticed

Four instances of one failure had been patched by hand, later each time: the
README's install verification, the README's Spec Kit compatibility line,
`ONBOARD.md`'s pin table, and the paste-from digests. `scripts/check-doc-versions.py`
answers the class instead of the instances (`FR-DOCS-70`).

It is deliberately not a generator. A generated receipt is unfalsifiable by its
reader: they cannot check it against anything, only trust the generator, which
makes the documentation a self-report, the one epistemic class this tool exists
to refuse. So the receipt stays human-written and the machine refuses it when it
lies. That is now `PROMOTION-CONTRACT.md` rule 11.

- **Every version number says which kind of claim it is.** A current claim, a
  dated observation, a declared range, a pinned dependency, or provenance. A
  bare number is refused, because nobody can tell later whether it meant
  current or historical, and that ambiguity is what rots.
- **A current claim must equal the version being cut**, and a quoted range must
  equal what the bundle manifest declares.
- **A dated observation carries an age**, measured in releases. Past the
  threshold it is refused unless the page states why it is kept, where a reader
  sees the reason.
- Runs in **Self Gate at pull-request time**, which is where the failure should
  be seen, and in the **release workflow before anything is built**, which is
  what makes it a refusal.
- `scripts/**` joined this repo's own `src_globs`, having been ungoverned scope
  since the beginning.

The first sweep refused 304 times and ended at 0 with two honest warnings. Five
were real defects rather than missing annotations, the sharpest a submission
checklist row claiming the latest release was v0.4.13 while naming
`specassay-0.3.4.zip` as its artifact.
<!-- specassay:stale-ok quotes the two stale numbers the defect contained; correcting them here would delete the finding -->

### The capture method can lie about the thing being captured

`PROMOTION-CONTRACT.md` rule 12, recorded on a ruling that the lesson outweighed
the fix. Twice in one sitting an instrument misreported the material it was
pointed at: a Gate run piped through `grep` reported the pipe's exit status
rather than the Gate's, which would have published a refusal as a pass in a
quoted receipt, and a search reported a phrase missing because it wrapped across
a line. A number you did not watch being produced is a number you do not know.

## 0.5.1 (2026-09-17)

A display release. The Gate is untouched: not a line of
`check-traceability.sh` changed, no status derives differently, no exit code
moved, no manifest field appeared or vanished. What changed is the Thread
Report, the illuminate rung, which renders what the Gate already decided.

**Why 0.5.1 and not 0.6.0.** Nothing this release ships can refuse anything that
passed before, which is the test 0.5.0's own minor bump was argued on. The one
new surface, `--receipts`, is additive and off by default: a caller passing no
`--receipts` gets the same behaviour it got yesterday, bar the rendering. The
rendered text *did* change shape, and that is the only thing that could break a
consumer — so the consumers were checked rather than assumed. The estate that
drives this tool captures the report's stdout whole and never parses inside it.
The one machine reader of the report's own text, this repo's `ack-gate`
workflow, matches a required tick by regex; the tick still renders outside every
fold and the regex still finds it. No known consumer breaks. (Strict semver
would call a new flag a MINOR bump; under semver §4 a 0.x line is exempt, and
this estate's practice has moved the minor digit for newly-possible refusals —
0.4.13 shipped the whole `dig` command as a patch. If that convention is ever
retired ahead of 1.0, this is the release where the two rules disagree.)

### The Thread Report reads in five seconds, and folds the rest

The first Thread Report to render on a real estate was longer than a reviewer
would read. Three trims, all display: nothing was dropped, only collapsed.

- **One verdict line.** The report opens with the thread's state and the counts
  that say what the change did — rows proved, rows moved to admitted debt,
  changed files off thread, plus minted, retired, restated, moved to `GAP` or
  carrier-added when they occur. A term appears only when its count is
  non-zero, so a PR that minted nothing never says "0 minted"; a PR that moved
  nothing says so rather than going quiet.
- **Every move is stated once.** "What moved" and "Thread Status" had been
  saying the same thing twice — each changed row as a bullet, then again as a
  table row marked `◀ changed`. The bullets are gone and the family tables
  absorbed them, carrying the move *and* the state. The `◀ changed` marker went
  with them: every row in the table moved now, so a marker saying so says
  nothing.
- **Unmoved rows are footnoted, not listed**, with their status counts, the way
  untouched backlog rows already were. Where a row moved with no carrier to
  point at, the cell is an em dash rather than blank: absence renders as
  absence, never an invented link.
- **`--receipts FILE`** renders a caller's Markdown folded at the end of the
  report. The run that produced a report is a receipt, not a headline. The
  report never reads, parses or reformats that text; a missing file costs the
  appendix and warns on stderr, never the report.
- **Two things never fold**, and the criterion says so by name: *Intent
  Changed*, because a restated promise asks the reader to go re-confirm
  something, and a required human tick, because it holds a merge. A warning
  behind a click is a warning nobody read.

Minted as `FR-THREAD-10` / `AC-THREAD-10`: the **display contract only**. A
shipped tool this repo's own registry did not govern was the assay office
running an ungoverned instrument, and the display is the promise a reader can
hold us to. Governing the tool's behaviour more broadly waits until there is
behaviour worth naming. Six of the eighteen new tests are that criterion's
proof, one per clause.

### Correction to the 0.5.0 notes (2026-09-17)

0.5.0's lead said that an unproven criterion carried by an open task is
`backlog`, a legal passing state, and that this is what made the proof-direction
defect silent. That is true of one of its two shapes. When the ID is *also*
named in a spec, the same unproven row reads `tracked-debt` instead. Both are
legal passing states, so the failure was silent either way and nothing in the
0.5.0 fix or its tests changes — but the upgrade evidence measured
`tracked-debt`, not `backlog`, and the notes named only one.

Recorded here rather than edited into the published 0.5.0 section. Rewriting a
released note in place is the same shape as re-pinning receipts that were never
re-earned: the correction is dated and points back, so the record shows both
what was said and when it was corrected.

## 0.5.0 (2026-09-16)

**One class, not six defects.** SpecAssay lets a project declare its own ID
grammar, test-name grammar, coverage mark, carry mark, and retirement mark.
The front door read those declarations; several back rooms assumed the stock
`TYPE-DOMAIN-NN` shape anyway. Wherever that happened, the tool quietly stopped
being about the project's promises and started being about SpecAssay's. This
release settles the rule the whole family now holds to: **wherever a configured
grammar is consumed, it is consumed as configured** — never rebuilt by a
hardcoded rule, never interpolated raw into a pattern or a command, never
guessed at from a shape the config never promised.

Found by running SpecAssay against a real estate whose IDs are dotted
(`AC-5.6.1a`). The worst of it failed *silently*: an unproven criterion carried
by an open task is `backlog`, a legal passing state, so a Gate that could not
reach a single test stayed green for ever while nothing ever became proven.
Silent green is the one failure this tool exists to refuse, and it was here,
inside the refuser.

Eleven regression tests come with the fix
(`extensions/specassay-check/tests/test_gate_110_nonstock_grammar.py`), on
fixtures carrying dotted IDs, an underscore-bearing ID, an alternation in
`id_regex`, and a retirement mark containing a slash. Ten of them fail against
the v0.4.13 tag and pass after. A release that fixed these without tests that
would have caught them would repeat the original error.

All three components move to 0.5.0 together, per the versioning law recorded
under 0.3.3: preset 0.5.0, extension `specassay-check` 0.5.0, bundle 0.5.0.

### Upgrade-blocker: read this before upgrading

**This release can refuse a registry that v0.4.13 accepted.** Proof matching is
now separator-insensitive, which is what makes a dotted or underscore-bearing
grammar provable at all. The one case it cannot serve is two IDs that differ
only in punctuation: `AC-1-2` and `AC-12` reduce to the same key, so a test
named for either could be credited to the wrong row. Rather than guess, the Gate
fails with an `ambiguous-id-key` finding naming both IDs (`FR-GATE-120`).

If your registry carries such a pair, your first run on 0.5.0 goes red where
0.4.13 was green. That is not a mystery refusal and not a regression: v0.4.13
never looked, and could have been crediting the wrong row the whole time.

**The remedy:** the Gate names the clashing IDs, so pick the one that is wrong
and retire it. Retire it properly rather than deleting the line, with a
`**Retires**: <id> (<YYYY-MM-DD>): <reason>` record on an open task, then mint a
replacement whose ID differs by more than punctuation. The retired row keeps its
history and the manifest keeps saying so. Nothing else in 0.5.0 changes a status
your registry already had.

### Repairs: the configured grammar is consumed as configured

Each of these restores a promise the registry already carries, so none of them
mints a new ID. The row each repair answers to is named with it.

- **The proof direction could not reach a non-stock ID** (Rule 6, the contract
  that a named test proves an AC). The engine rebuilt a registry ID from a test
  name with `tr '_' '-'`, so `test_AC_5_6_1_a_...` resolved to `AC-5-6-1-a`,
  which matches no entry. For any estate with dotted IDs, *no* acceptance
  criterion was reachable by *any* test. The mapping is now derived from the
  registry's own IDs by separator-insensitive lookup, so any grammar the config
  admits round-trips: both sides of the comparison come from the config's own
  output. A token that resolves to no registry ID keeps its old treatment, so
  untraced scope is still reported rather than lost.
- **The JUnit reader carried the same hardcode** (`FR-GATE-80`, `AC-GATE-80`).
  `id_forms()` built candidate spellings of an ID by rule. It is gone: a passing
  test is now matched on the test's own name, as the report itself spells it.
- **Name matching is bounded** (`FR-GATE-80`, `AC-GATE-80`). A needle now has to
  sit on an alphanumeric boundary, so `AC_1` no longer matches inside `AC_10`.
- **A configured `id_regex` with a top-level alternation escaped the def-line
  anchor** (`FR-GATE-50`'s duplicate-ID check, which this defect defeated).
  `def_line_regex` interpolated the value bare into `^...%s...$`, so the
  trailing branch matched anywhere on any line and a registry that minted each
  ID once read as dozens of definition lines. The grammar is now grouped at the
  point of interpolation.
- **A configured mark containing a slash broke the command that read it**
  (`FR-GATE-30`, which defines the retirement record). `retires_regex` was
  interpolated into a `sed` substitution, so a value like
  `\*\*Retires/Withdraws\*\*:` closed the `s///` early. The mark is now passed to
  `awk` as data and never becomes part of a command's syntax.
- **The mark travels through the environment, not `awk -v`** (`FR-GATE-30`,
  same row, second round). A `-v` assignment is escape-processed, so gawk read
  the `\*` in `\*\*Retires\*\*:` as a plain `*` while mawk passed it through: the
  same config parsed on one machine and not on another. `ENVIRON[]` is not
  escape-processed, so the mark reaches `match()` as the bytes the config
  declared. Caught by CI rather than by the suite, because the container that
  wrote the first fix runs mawk and the runner runs gawk. A static test now
  refuses any configured pattern passed to awk through `-v`, which catches the
  class in either environment; a behavioural test cannot, on a machine with only
  one awk.
- **Orphan scoping went silent on a grammar with no domain segment**
  (`FR-GATE-40`, `AC-GATE-40`, `AC-GATE-41`). `is_local_domain()` took the
  second hyphen-separated field; a dotted ID has none, so no unknown ID ever
  looked local and drift was never reported. Where a registry's IDs carry no
  domain, every unknown ID is now treated as local and reported: the check errs
  loud rather than silent.

`mint-id.sh` also now reads the configured `id_regex` for definition-line
detection and for finding the highest existing number, instead of assuming the
stock shape.

### New promises, minted for this release

Three things 0.5.0 does that no existing row promised. They are registered in
`PRD.md`, claimed in `specs/self-gate-config/spec.md`, carried by `T923`, and
each is proven by a named test:

- **`FR-GATE-110` / `AC-GATE-110` — an empty or unreadable test report is
  refused, not believed.** A `test_results` report containing zero test cases
  was read as "nothing passed", which demoted every criterion and returned a
  green run with `executionVerified: true`. It is the absence of evidence, not
  evidence of absence. It now exits 2 with the reason named, writes no manifest,
  and points at the likely cause: a toolchain that writes one report per test
  framework and leaves the others empty. Observed on Swift 6.3.3, where
  `swift test --xunit-output` wrote only the swift-testing file, with no cases,
  for an XCTest-only run; whose bug *that* is belongs to the toolchain, but
  trusting the file was ours. A report the parser cannot read takes the same
  exit.
- **`FR-GATE-120` / `AC-GATE-120` — IDs that collide under proof matching are
  refused, not resolved by guess.** See the upgrade-blocker note above.
- **`FR-GATE-130` / `AC-GATE-130` — `mint-id.sh` refuses to compose an ID the
  configured `id_regex` rejects.** Issuing scope the Gate would then refuse was
  the same assumption in the opposite direction. The refusal quotes the
  configured grammar, shows the ID it declined to compose, and says to mint by
  hand into the registry in the grammar the config declares.

The class itself stays unminted. A row that promised "every configured value is
consumed as configured" would be a slogan the Gate cannot check, and the rows
above already carry the parts of it that can be proven.

### Also in this release

- **Compatibility claim names what is proven.** `requires.speckit_version`
  moves from `>=0.14.0` to `>=0.14.0,<2.0.0` in all three manifests, after
  v0.4.13 was run end to end on Spec Kit 1.0.4 (install by catalog and by
  direct download, Gate, mint, refusal, upgrade from v0.4.12;
  `docs/submission/test-evidence.md`). The upper bound is the major line,
  not the last patch tested: Spec Kit enforces this field as a hard
  install refusal and shipped three patches in three days that week, so a
  literal `<=1.0.4` would refuse every adopter on the next one. Catalogs
  and paste-from docs follow at the cut.
- **README:** `specify bundle install` scaffolds the config on Spec Kit
  1.0.3 and later (github/spec-kit#4285); the README said it never did,
  which was true of 0.15.3.dev0 only.
- **`ONBOARD.md`** names its one divergence rather than hiding it: its receipts
  were captured on v0.4.13 and have not yet been re-captured by a cold operator
  on v0.5.0. Tracked as `docs/docs-gaps.md` item 11.

## 0.4.13 (2026-09-04)

Two threads in one release. First, the cold-install findings from the
first Windows tester on record (2026-09-03: senior engineer, Git Bash, no
Spec Kit experience, brownfield repo with specs under `docs/**`), fixed in
the order he hit them (`FR-GATE-100`, `T920`). Second, everything that
landed on `main` between the 0.4.12 tag and this one without a release:
five Gate features and the whole `dig` command, all registry-governed
(`PRD.md`) and each proven by named tests in the engine's own suite,
which grew from 27 tests to 81. All three components move to 0.4.13
together, per the versioning law recorded under 0.3.3.

### Cold install (2026-09-03)

- **Green on an empty registry now says what to do next.** `OK (0 registry
  IDs)` was correct and taught nothing. The Gate still exits 0, but states
  the registry is empty, that nothing is promised yet, that green will
  hold until something is, and prints two runnable on-ramps to a first ID:
  greenfield (mint before the Spec Kit spec) and brownfield (mint one ID
  against a requirement in a doc you already have, no backfill). A missing
  registry file gets the same two choices under its refusal.
- **Python is detected, not hardcoded.** `SPECASSAY_PYTHON`, then
  `python3`, then `python`, each probed for 3.8 or newer; none usable is a
  one-line FAIL with an install hint and exit 2, before any scanning. The
  same detection went into `commit-advisory.sh`. Tests cover the fallback
  and the failure path with interpreter shims on `PATH`.
- **The Gate reports its own config state on its first lines**, every run:
  the path it resolved and how, or `MISSING` plus the one `cp` command
  that scaffolds it. The root README's "if Gate config wasn't scaffolded"
  sentence now points at that report instead of asking the user to guess.
- **The extension README is written for the person who just installed
  it**: what it is, what each config key controls, what a run produces,
  what green and red mean, the first-run on-ramp. Developer notes moved to
  `extensions/specassay-check/DEVELOPING.md`.
- **Prerequisites and platforms stated up front** in the root README: a
  pointer to Spec Kit for anyone new to it, the three-install chain (uv,
  Spec Kit, SpecAssay) named as designed, and macOS/Linux first-class with
  Windows requiring Git Bash or WSL.
- **`mint-id.sh` counts lettered ACs.** `AC-GATE-90a/b/c` did not count
  toward the highest existing number, so a mint offered `AC-GATE-90`
  again. Found running the documented command as a receipt for this
  change.
- **Registry hygiene:** `FR-DIG-60`, `FR-DIG-70`, `AC-DIG-70`, and
  `AC-DIG-80` were cited by `specs/dig/spec.md`, `T918`/`T919`, and
  `dig.py` since 2026-08-22 but never minted into `PRD.md`, which kept
  this repo's own Self Gate red from 2026-08-23. Registered now, marked as
  coverage registered rather than newly attributed.

### Gate features shipped since 0.4.12 (all 2026-08-21 and 2026-08-22)

- **`--matrix` (`FR-GATE-10`, `T905`).** Writes `coverage.md` and
  `coverage.svg` from the same run's already-computed rows: a summary
  table, per-type sections, a generated-file banner, family status colors
  in canonical order, the manifest's own `generatedAt` as visible text.
  Never a second scan, never a second viewer. New command
  `speckit.specassay-check.matrix`.
- **`--portfolio` (`FR-GATE-20`, `T906`).** Writes `portfolio-snapshot.md`
  for a cold reader with zero context: plain-prose opening, no CI banner,
  scoped explicitly to this one repo's registry. Shares `coverage.svg`
  with `--matrix`. New command `speckit.specassay-check.portfolio`.
- **`retired`, a genuine fifth status (`FR-GATE-30`, `T907`).** Derives
  only from an explicit, dated, reasoned `**Retires**: <ids> (YYYY-MM-DD):
  reason` record on an open task; there is no settable field. In
  `trace-manifest.json` (v4, frozen at four values) a retired row leaves
  `rows[]` for a top-level `retired: [{id, date, reason}]` list; in
  `trace-manifest.v5beta.json` it is a normal fifth row status. A
  malformed record refuses before any scanning, no manifest written.
- **`proofs[]` inherits execution-verified filtering (`FR-GATE-80`,
  `T914`).** With `test_results` configured, a test name that matches
  only inside a comment no longer appears in an ID's `proofs[]`; the same
  filter `status_for()` already applied, now at the second call site.
- **Parentage (`FR-GATE-90`, `T915`).** Opt-in `parent_derivation:
  heading-nesting` derives a `parent` edge per row from the registry
  document's own heading and list nesting, never from ID naming. Every row
  with descendants carries a composition rollup over its whole subtree at
  any depth, with a total row count. v5beta only. Dogfooded here: turning
  it on caught real mis-nesting in this repo's own `PRD.md`.

### `specassay dig`: archaeology mode, the no-LLM floor (`T916` to `T919`)

- New command `speckit.specassay-check.dig` (`scripts/dig.py`, pure
  Python, no dependencies, no LLM, no `--anoint` flag by law). Points at
  any repo, SpecAssay-governed or not, and writes `dig-report.json` in
  the operator's own current directory: a first-pass candidate registry
  from test names and bodies, routes, README and `docs/*.md` prose and
  tables, and recent commit history. Every row is `epistemicClass:
  "inferred"` with a `provenance` file and line; nothing it writes is
  ever registered, covered, or gated.
- Level two (`T917`): README table mining recovers spec/scenario/test
  tables completely; `candidateProof` first-class on every row; known
  framework smoke tests labeled low confidence with a reason.
- Level three (`T918`): `candidateBuild` per row from the proof test's own
  project-package imports, resolved to real declaration files; Java and
  Python import shapes both dogfooded against real repos.
- Structure emission (`T919`): stable `rowId` per row and a
  `candidateParent` list with basis `"table-adjacency"`.
- Reference output from a real target: `samples/insurance-java.dig-report.json`.

### Catalog correction

- `catalogs/extensions.json` said the extension provides 2 commands; it
  has provided 5 since dig, matrix, and portfolio shipped. Corrected.

## 0.4.12 — 2026-08-20

`orphan-covers`/`orphan-test` and the manifest emitter both had real,
found-in-production bugs; both are fixed, both now carry regression
tests — the engine's first automated test suite, not just hand-verified
scratch fixtures.

- **`orphan-covers` domain scoping (Rule 4).** A citation of another
  project's real `@covers` line — quoted as a teaching example in a doc,
  or another project's ID mentioned in prose — used to fail the Gate as
  an orphan, with no way to tell a citation from a real local claim. Now
  scoped two ways: an ID whose domain was never minted into the local
  registry is treated as a citation, the same `is_local_domain()`
  reasoning `orphan-spec`/`orphan-task` already used; and a mark inside a
  markdown fenced code block or inline backtick span is ignored
  regardless of domain, so a project can safely quote its own real IDs
  as examples. Found founding this repo's own self-governed registry:
  `docs/**` in `src_globs` failed immediately on doc files quoting other
  projects' `@covers` lines.
- **Manifest emitter dedup.** `implementations[]` and `proofs[]` had no
  dedup, unlike the `carryingTasks` debt-collection loop right next to
  them, which already deduped. Overlapping `src_globs`/`test_globs`
  entries, or a `./x` vs `x` glob spelling, hand the same mark to the
  glob expander twice under two different literal path strings — a real
  emit carried this in 62 of 100 rows. Deduped both on
  `(id, normpath(path), line)`.
- **Config keys that silently meant nothing now refuse instead.** A
  list-type config key (`src_globs`, `test_globs`) written as an inline
  YAML array (`src_globs: ["src/**"]`) instead of a block list parsed to
  an empty list with zero signal — no `FAIL`, no `DIAGNOSTIC`, every row
  silently read `backlog`. Same silent trap for a key present with no
  items under it at all. Both now refuse loudly before any scanning
  happens — the offending line, the accepted shape, and a pointer to
  `docs/troubleshooting.md`, and no `trace-manifest.json` is written: a
  manifest built on a config known to be misread would carry confident
  wrong claims, worse than none. Found twice in one day preparing a
  cold-agent trial's own reproduction fixtures — the exact silent-gap
  shape this tool exists to refuse in everyone else's config, never
  checked for in its own.
- **New: an automated test suite for the engine itself**
  (`extensions/specassay-check/tests/`, 27 tests). Every rule above has
  regression coverage, including the two verbatim configs that actually
  failed while preparing the cold-agent trial fixtures — the regression
  fixtures are the real incidents, not a paraphrase of them. Verified
  the suite has real teeth, not just green tests: reverted to the
  pre-fix script and confirmed the relevant tests correctly fail against
  it before restoring the fix.

Also shipped this cycle, evidence attached rather than asserted: a real,
independently-reverified cold-agent trial (a fresh, uncoached agent
completing one plain-language requirement on a real public repo
unrelated to this project, installing from these same public catalogs)
— `docs/testing/completed/evidence-cold-agent-trial-observed-2026-08-19.md`.

## 0.4.11 — 2026-08-18

Fix: `commit-advisory.sh` silently did nothing when actually installed
the way its own README says to (`.git/hooks/commit-msg` as a symlink
to the real script). `dirname "$0"` resolves relative to the
*symlink's* own location (`.git/hooks`), not the real script's
location; `EXT_DIR` computed wrong, the config lookup silently failed
`[[ -f "$CONFIG" ]] || exit 0`, and the advisory never ran — found by
testing the real installed hook in a real repo, not just the
standalone script, which had been passing the whole time and masked
it. Fixed by resolving the real path with `python3 -c
'os.path.realpath(...)'` (portable; BSD `readlink` has no `-f`)
before computing `EXT_DIR`. Verified against both invocation shapes:
the real symlink-installed hook in speccost's own repo, and the
standalone script called directly.

## 0.4.10 — 2026-08-18

The paved roads for rule 6a's own arrival
(`speccost-honesty-economics-2026-08-17_1.md`'s own standing design
law: "the honest path must be the shortest path; every governance
obligation names its paved road or it is not law yet"):

- **Marks at work time.** `presets/specassay/templates/tasks-template.md`:
  test tasks now name the exact proof (file path and function name)
  before the code exists, not "a test for this AC" left to be decided
  later; implementation tasks that create or first touch a source file
  now carry the exact `@covers` line to paste, pre-written in the task
  itself. New `scripts/commit-advisory.sh`: a `commit-msg` hook,
  install once per clone, warn-only and never blocking, flags when a
  commit message names a registry ID but no staged file carries a
  matching `@covers` mark.
- **Registration mints.** `mint-id.sh --append` now prints a reminder
  after every real append: state the coverage basis plainly in the
  mint commit, "coverage registered, not newly attributed" for
  already-built work this mint is only now registering, or say it's
  new work instead. Either is honest; silence about which is not.
- **Fresh data and status re-triage**: already real before this
  release (a working `refresh.sh` and a loaded launchd extraction
  pulse in the wild, rule 6a's own derivation making manual re-triage
  extinct) — confirmed, not rebuilt.

Verified: `commit-advisory.sh` tested against three real scratch
cases (missing mark warns and exits 0; a real mark present stays
silent; no ID mentioned stays silent). `mint-id.sh`'s reminder
verified to print only on a real `--append`, never on a dry-run mint.

## 0.4.9 — 2026-08-17

Rule 6a: **proven derives from a passing proof, not a matching name.**
The founding-sentence repair. `proof_hits.txt` was always built by
static `grep` against a test-name pattern; nothing ever confirmed the
matched test actually passes, isn't a stub, or isn't a skip a grep
still sees. Status has been a self-report all along, the same failure
class as an undeclared tally line or a self-marked checkbox, on the
most important word in the system. Rule 6's own text already said the
quiet part out loud: "a fact that a carrier exists, not a claim the
code is correct."

New config key, `test_results`: a JUnit XML path (pytest
`--junit-xml=...`, node:test's junit reporter, vitest's junit
reporter — all three test runners in active use across this project
family already produce this format natively). When set, `proven`
requires at least one *passing* testcase whose name or classname
contains the ID (hyphenated or underscored form, covering both this
family's Python and JS test-naming conventions), not merely a
name-pattern match. Cross-referencing happens once, in the same place
`test_acs.txt` is already built, so every downstream consumer (the
silent-gap check, `uncovered-proof`, `status_for()`'s own `tested`
set) inherits the corrected meaning for free.

New manifest field, `gate.executionVerified`: `true` when
`test_results` was configured and found; `false` when it was absent,
with a loud `WARN:` on stderr, never a silent fallback. A project that
hasn't wired this up yet keeps working exactly as before — nothing
breaks on upgrade — but the manifest now says plainly which meaning of
`proven` is in effect, rather than implying the stronger one by
default.

Verified both directions against a real, controlled scratch fixture:
a genuinely failing test named to match a real AC, under the old
name-matching-only path, showed `proven`, `gate.ok: true`,
`executionVerified: false` — the exact gilt this rule exists to catch.
The same fixture with `test_results` configured showed `GAP`,
`gate.ok: false`, `executionVerified: true`. Also verified against
SpecCost's own real suite (148 passing tests, real `pytest
--junit-xml` output): `executionVerified: true`, 78 `proven`, zero
demotions — the re-triage this rule's own arrival makes possible found
nothing wrong there, the expected outcome for a repo whose suite was
already genuinely green throughout.

## 0.4.8 — 2026-08-17

`uncovered-proof` (v0.4.7) gains the mechanism its own report-only
posture was always meant to lead to: a per-project opt-in to blocking.
New config key, `block_uncovered_proof: true`
(`config-template.yml`, `specassay-check-config.yml`). When set, the
same finding that would have gone to `gate.diagnostics[]` is recorded
via `record_fail` instead, exactly like every other Gate check
(`orphan-covers`, `silent-gap`, etc.): it appears in `gate.failures[]`
and flips `gate.ok` to `false`. Unset (the default), behavior is
unchanged from v0.4.7.

Verified both directions against a real scratch fixture: an uncovered
AC passes with `gate.ok: true` under the default, fails with
`gate.ok: false` and a real `uncovered-proof` entry in
`gate.failures[]` once `block_uncovered_proof: true` is set, and
clears again once the missing `@covers` mark is actually added.

The convention this key exists to support (PROMOTION-CONTRACT.md
Rule 4a): a project flips to blocking only once its own backlog is
actually clear, and the flip itself carries a dated comment recording
when and why, in that project's own config, so enforcement status is
itself traceable rather than a silent behavior change on upgrade.

## 0.4.7 — 2026-08-17

New Gate 2 diagnostic, `uncovered-proof`: an ID with a real, passing
proof that no file's own `@covers` mark names. The mirror of the
already-shipped `orphan-covers` check (an `@covers` mark naming an ID
that isn't registered); the reverse direction was never gated, so a
real, tested, `proven` ID could sit with no source-level
self-documentation indefinitely, invisible to Gate 2 and to anyone who
didn't cross-reference `@covers` lines against test names by hand.

Found dogfooding SpecCost: `common/bind.py`'s own `@covers` line never
listed `AC-BIND-10/20/30`, going back to the file's very first commit,
even though the tests proving them existed in that same commit.
Surveyed across five real projects with this same, newly-patched check
run in report-only mode (never affecting `gate.ok`): SpecCost alone
carries 30 more instances of the identical pattern, spanning eight
source files; Tally and Loupe (clewloupe) carry zero; SpecAssay's own
reference `example-app` (what every new adopter copies first) carries
two. Every instance found is the same one-line fix `bind.py`'s was:
append the missing ID(s) to a file's already-existing `@covers` line,
no logic change.

- Ships report-only: `gate.diagnostics[]`, a new array alongside
  `gate.failures[]`, parallel in shape (`{ kind, detail, id? }`) but
  never sets `fail=1` and never flips `gate.ok`. A named, visible
  finding whose blocking-vs-diagnostic ruling is deliberately deferred
  (PROMOTION-CONTRACT.md Rule 4a, new this release) rather than forced
  by the same commit that first makes the gap visible project-wide.
- Applies to every ID type (`AC`, `FR`, `NFR`, `US`), not only `AC`:
  rule 6's `proven` grants status from a test alone for every type, so
  the same silent asymmetry exists at every altitude, not just AC.
- No config or command surface changed; existing registries need no
  edits. `trace-manifest.json`'s `gate` object gains one new key;
  existing consumers reading only `gate.ok`/`gate.failures` are
  unaffected.

## 0.4.6 — 2026-08-16

`check-traceability.sh` had two sites (the tracked-debt task excerpt,
`pending_hits.txt`; the `@covers` excerpt, `covers_hits.txt`) that
truncated a matched line with `cut -c1-N`, byte-oriented under the
script's own `LC_ALL=C`. A multi-byte UTF-8 character landing across
the cut boundary (an em dash is 3 bytes) got sliced in half, producing
an invalid partial sequence that later crashed the Python side reading
it back with `UnicodeDecodeError`. Found dogfooding SpecCost: a real
`tasks.md` line whose own em-dash separator happened to land at
exactly byte 199-201 crashed Gate 2 outright.

- Fixed by moving truncation out of bash entirely: both sites now pass
  the full, untruncated excerpt through to their hit files, and
  truncate in Python (`excerpt[:200]`, `excerpt[:160]`) instead, where
  string slicing is codepoint-safe by construction, never byte-oriented.
- Both hit-file reads (`covers_hits.txt`, `pending_hits.txt`) also
  gained `encoding="utf-8", errors="replace"`, matching the registry
  read's own existing defensive posture, as a second line of defense.
- Verified against a scratch fixture reproducing the exact real crash
  line in both directions (pre-fix: `UnicodeDecodeError`; fixed: a
  clean 200-character excerpt, em dash intact, not replaced or
  mangled) and smoke-tested against SpecCost's real registry.
- No config or command surface changed; existing registries need no
  edits.

Components: bundle 0.4.6 · extension `specassay-check` 0.4.6 · preset
`specassay` 0.4.6.

## 0.4.5 — 2026-08-15

`check-traceability.sh` now emits `trace-manifest.v5beta.json`
alongside its existing `trace-manifest.json`, never in place of it.
`docs/trace-manifest-v5.md`'s own stated bar for the Gate's *primary*
emit to move from `v4` to `v5` is "once the beta settles", meaning the
first external emitter (`clew`) has pushed on the field shapes; that
hasn't happened, so `v4` stays the default output unchanged. The new
file is reshaped from data the Gate already computes, not new
computation: `tier` from the `US`/`FR`/`NFR`/`AC` prefix already
parsed, `origin` as `registry`'s own `{path, line}` under its v5
spelling, `emitter` as the `{name, version}` object v5 requires.

- `parents`/`rollup` are deliberately left absent. SpecAssay has no
  real per-ID parent edge today, only the domain-grouping convention
  the prefix already encodes; the v5 doc explicitly designs for this,
  an absent `parents` falls back to domain-grouping in any v5 reader.
  Inventing edges from a guess was rejected in favor of staying honest
  about what the Gate actually knows. Practical effect: a `v5beta` file
  opened in Loupe renders as a flat list today, not yet a threaded
  intent → requirement → criterion descent.
- Output path is derived from the existing `manifest_path` config
  (`.json` → `.v5beta.json`); no new required config key.
- Verified against a scratch fixture (both files write, correct row
  counts, correct `tier` values) and smoke-tested against SpecCost's
  real 60-ID registry.

Components: bundle 0.4.5 · extension `specassay-check` 0.4.5 · preset
`specassay` 0.4.5.

## 0.4.4 — 2026-08-15

`check-traceability.sh`'s registry extraction had a third site with the
same underlying flaw v0.4.2 and v0.4.3 already fixed twice at two other
sites: the loop that builds each ID's *displayed* `statement` text and
`registry.line` pointer for `trace-manifest.json` still did its own
independent blind `id_ in line` substring scan over the raw registry
text, never rescoped to `def_line_hits.txt` the way v0.4.2 rescoped the
registry's own ground-truth ID set. Found while dogfooding SpecCost:
`FR-SPOOL-20`/`NFR-SPOOL-20` and `FR-SPOOL-30`/`NFR-SPOOL-30` each
showed byte-identical wrong statement text, both pairs pulled from a
Non-goals paragraph's parenthetical citation instead of either ID's own
bullet. Worse than a plain citation-vs-mint mixup: because the match is
substring containment, not equality, a shorter ID's own literal name is
contained inside a longer sibling's name (`"FR-SPOOL-20" in "...NFR-
SPOOL-20..."` is `True`), so this could misattribute one ID's displayed
statement to a completely different ID's own real bullet, not just to
stray prose.

- Fixed by reusing `def_line_hits.txt` (`id|lineno`, definition-shaped
  lines only, already computed for the registry-extraction fix) instead
  of re-deriving a second, disagreeing match against raw registry text.
- Status and proofs (`proven`/`tracked-debt`/`backlog`/`GAP`) were never
  wrong, only the displayed statement text and line pointer for IDs
  whose real bullet wasn't the first line in the file to mention them;
  this is a display-correctness fix, not a coverage-logic change.
- Verified against a scratch fixture in both directions (pre-fix: two
  sibling IDs share one wrong, non-definitional line; fixed: each
  resolves to its own real bullet and line number) and smoke-tested
  against SpecCost's real registry, where this was found.
- No config or command surface changed; existing registries need no
  edits.

Components: bundle 0.4.4 · extension `specassay-check` 0.4.4 · preset
`specassay` 0.4.4.

## 0.4.3 — 2026-08-15

`check-traceability.sh`'s spec/tasks-side extraction had the same
underlying flaw v0.4.2 fixed on the registry side, just at a different
site: any ID-shaped string anywhere in `spec.md`/`tasks.md`, including
inside another row's own prose (this time, a real regression: citing
`AC-USER-03` while explaining the v0.4.2 bug, inside `BIND`'s own spec
and tasks files), got flagged as `spec-orphan`/`task-orphan`, an
untraced reference to an ID this project never minted.

- Unlike the registry (one canonical bullet shape), `spec.md`/`tasks.md`
  have no single line shape a fix could scope to: FR/NFR bullets,
  trailing-parenthetical Acceptance Scenario references, and risk-table
  cells are all legitimate, different shapes. Scoping to any one of
  them would have traded a fixed false positive for new false
  negatives on real claims written in the others.
- Fixed differently: `spec-orphan`/`task-orphan` now only fire for an
  ID whose domain segment (the middle of `TYPE-DOMAIN-NN`) is one this
  registry has actually minted into. A citation of another project's
  real ID, in a domain this registry has never used, is no longer
  mistaken for a local orphan. A same-domain typo (`FR-BIND-99` when
  only `FR-BIND-10` exists) still fails exactly as before, verified
  against a fixture built specifically to check that trade-off wasn't
  silently given away.
- Verified against a scratch fixture in both directions (pre-fix
  spuriously fails on a cited foreign ID; fixed does not, while a real
  same-domain orphan still fails) and smoke-tested against SpecCost's
  real 58-ID registry, where this exact regression was found.
- No config or command surface changed; existing registries need no
  edits.

Components: bundle 0.4.3 · extension `specassay-check` 0.4.3 · preset
`specassay` 0.4.3.

## 0.4.2 — 2026-08-15

`check-traceability.sh` built its ground-truth registry ID set with a
blind `grep -Eoh "$ID_RE" "$REGISTRY"` over the whole file, so any ID
string appearing anywhere in the registry, including inside another
row's own prose (a cross-reference, a range-summary table endpoint, a
different project's ID cited for context), was read as a mint. Found
while dogfooding SpecCost: a `FR-SPLIT-20` statement citing HomesFlow's
`AC-USER-03` for context got misread as a 55th minted ID, and Gate 2
failed it as an untraced, untested, silent gap that was never actually
minted.

- Registry extraction now reuses the same definition-line scoping
  `duplicate-id` detection already used (`lib-def-line.sh`'s
  `def_line_regex()`): a bullet that actually mints an ID, not any line
  that merely contains one. `registry.txt` (the set everything else is
  compared against) is derived from that scoped extraction, not a
  separate blind grep.
- Verified both directions against a scratch fixture: the pre-fix
  script spuriously mints and fails on a cited-but-not-minted ID; the
  fixed script does not. Also smoke-tested against SpecCost's real
  58-ID registry with zero regressions.
- No config or command surface changed; existing registries need no
  edits.

Components: bundle 0.4.2 · extension `specassay-check` 0.4.2 · preset
`specassay` 0.4.2.

## 0.4.1 — 2026-08-15

`mint-id.sh` shipped in 0.4.0 but was never reachable by a cold user.
`extension.yml` registered only `speckit.specassay-check.gate` as a
command; the mint script existed only as a file someone would have to
already know about and invoke by hand. Found while dogfooding
SpecCost: everything worked for us specifically because the tool had
just been hand-built by the same session using it, not because a real
adopter could discover any of it.

- **New command, `speckit.specassay-check.mint`**, wired into
  `extension.yml` and installed like any other extension command.
  Wraps `mint-id.sh` for both primary minting and `--resolve`.
- **Registry bootstrap, documented for the first time.** Neither the
  README nor any command previously said what to do when the
  registry file doesn't exist yet. The new command's steps cover it
  (create the file empty, mint normally, style falls back to a plain
  `- ID — statement` line with nothing to imitate); the README gets a
  matching "No registry yet?" section.
- Verified against a genuinely cold scratch project: `specify init`,
  `specify extension add --dev`, then only what the new command file
  says, no prior knowledge of the script's existence or syntax. Ends
  with a real first mint.

Components: bundle 0.4.1 · extension `specassay-check` 0.4.1 · preset
`specassay` 0.4.1.

## 0.4.0 — 2026-08-14

Concurrent minting stops failing silently, and a new tool makes it cheap to
avoid failing at all.

- **`mint-id.sh`** (new): mints the next ID for a given prefix and area by
  scanning the registry for the highest existing number, rather than
  requiring a human or agent to eyeball the file and guess. Mints land on
  multiples of ten (`AC-HOME-10`, `AC-HOME-20`, ...); a brand-new area
  starts at 10. The step size does not reduce how often two branches
  collide on the same next number (both compute from the same
  last-observed state regardless of step size), but it reserves the `1`
  through `9` offset off every decade exclusively for resolving a
  collision, so fixing one is a purely local `+1` (`mint-id.sh --resolve
  AC-HOME-20` → `AC-HOME-21`) with no need to recompute the registry's
  current state. The ones digit doubles as a free collision counter for
  that slot. Reuses the same config discovery and registry conventions as
  `check-traceability.sh`.
- **`duplicate-id` Gate refusal** (new failure kind): two independent
  definition lines minting the same ID used to merge cleanly and vanish
  silently, because the exact-set check dedupes the registry with `sort
  -u` before looking at it, and the trace-manifest only ever kept the
  first matching line's statement. Gate 2 now detects any ID with more
  than one definition-shaped line and refuses, naming both line numbers.
  Detection is scoped to definition-shaped lines only (a shared pattern
  with `mint-id.sh`'s own style-detection, `lib-def-line.sh`) so a
  range-summary table using an ID as a range endpoint, or any other line
  that merely mentions an ID, is never mistaken for a second mint of it;
  verified against HomesFlow's real registry (0 false positives across 82
  IDs) and a new fixture, `samples/sample-duplicate-id.trace-manifest.json`.
- Registry-only for this release. Duplicate detection does not extend to
  specs or tasks referencing an ID more than once, which is repetition,
  not minting.
- `mint-id.sh` and the duplicate-id refusal are a matched pair: the decade
  scheme's payoff is a cheap resolution at the exact moment the Gate
  refuses a collision. Shipping the mint helper without the refusal would
  leave the collision-masking hole open; shipping the refusal without the
  helper would leave collision resolution as manual arithmetic.

Components: bundle 0.4.0 · extension `specassay-check` 0.4.0 · preset
`specassay` 0.4.0.

## 0.3.4 — 2026-08-13

- **The preset's own README pointed at a stale asset.** `presets/specassay/README.md`
  ships inside the preset zip, and its install command still named
  `v0.3.1/specassay-preset-0.2.0.zip` even after two version bumps, because
  neither sweep grepped that file. Found by Copilot review on the generated
  preset PR. Fixed, and since the file ships inside the artifact, the fix
  needed a real release rather than a docs-only push: republishing v0.3.3's
  assets under the same tag with different contents would have repeated the
  exact mismatch this bundle exists to catch.

Components: bundle 0.3.4 · extension `specassay-check` 0.3.4 · preset
`specassay` 0.3.4.

## 0.3.3 — 2026-08-13

Two findings from Spec Kit review, and a versioning rule to keep them from
recurring.

- **Required tools are declared.** `extension.yml` carried `tools: []` while
  the submission text promised `python3 (>=3.8)`, so the generated catalog
  entry reported every Python 3 as compatible. The extension now declares
  `bash` and `python3 >=3.8` in the schema the catalog uses. The constraint
  is conservative on purpose: the shipped code parses on 3.7, and 3.8 is what
  is supported and tested.
- **All three components share the bundle's version, from here on.** Spec
  Kit's preset workflow expects a release tag matching the preset's own
  version, and a preset at 0.2.1 riding in a v0.3.2 release cannot satisfy
  that. Component versions now move together with the bundle, so the release
  tag always matches every component.

Components: bundle 0.3.3 · extension `specassay-check` 0.3.3 · preset
`specassay` 0.3.3.

## 0.3.2 — 2026-08-13

- Author metadata fixed to **"Rik Dryfoos"** (was "Rik Dryfoos / Dryfoos
  Consulting") in `extension.yml`, `preset.yml`, and `bundle.yml`. The
  v0.3.1 release assets were built before this rename landed on `main`,
  so they still carried the old string; this release re-packages with
  the corrected metadata. Component-only change, no behavior difference.

Components: bundle 0.3.2 · extension `specassay-check` 0.3.2 · preset 0.2.1.

## 0.3.1 — 2026-08-11

- Command renamed `speckit.specassay.check` → **`speckit.specassay-check.gate`**
  to satisfy Spec Kit's extension-namespace rule (commands must follow
  `speckit.{extension-id}.{command}`). Behavior unchanged.

Components: bundle 0.3.1 · extension `specassay-check` 0.3.1 · preset 0.2.0.

## 0.3.0 — 2026-08-11

The productization release: the bundle is now **SpecAssay** end to end, and the
pull-request layer ships.

- **Renamed** from the working name *clewseau* — bundle `specassay`, extension
  `specassay-check` (was `clewseau-gate`), preset `specassay`. The emitted file
  is a plain, vendor-neutral `trace-manifest.json` (was `clew.json`).
- **trace-manifest schema v4**: row field `debtTasks` → `carryingTasks`
  (semantics unchanged; readers alias v3 on load). A **v5 interop rev ships in
  beta** — explicit parent/child edges, portable `tier`, generalized ID
  `origin` (ledger-minted IDs), durable code anchors, emitter object, and an
  emitter-conformance checklist (`docs/trace-manifest-v5.md`, two samples in
  `samples/`).
- **Thread Report** (new): on every PR, CI posts one briefing — what moved on
  the thread, the touched story end to end, and the changed files that sit off
  the thread, all clickable. It illuminates and never blocks; a separate step
  refuses a broken Gate. Live demos: PR #1 (green), PR #2 (broken).
- **Intent Changed** (new report section): detects restated intent wording,
  grades the re-confirm hint into three tiers (pinpointed stale value / value
  changed / prose), and tells the two intent-PR shapes apart by whether the
  carriers moved in the same PR. Live demos: PR #4 (wording alone), PR #5
  (discovery — wording and proof together).
- **Affirm rung, enforced**: `offthread_ack` and `intent_ack`
  (`off | record | required`) render real checkboxes in the report;
  `required` sets a `specassay/ack` commit status that stays red until a human
  ticks (ack-gate workflow re-reads on comment edit).
- **The seam, made reviewable**: `.github/CODEOWNERS` puts the example app's
  registry under the product owner; doctrine in
  `docs/scope-and-pull-requests.md` §5a.
- **Preset 0.2.0**: the constitution template's vocabulary article is now
  self-sufficient (mark/`@covers`, `Carries:`, anointed backlog rows added).
- Docs: field guide, Thread Report reference, scope-and-pull-requests, and a
  designed walkthrough site at [specassay.com](https://www.specassay.com).

Components: bundle `specassay` 0.3.0 · extension `specassay-check` 0.3.0 ·
preset `specassay` 0.2.0.

## 0.2.0 — 2026-08-06

- Gate 2 emits the manifest (then `clew.json`) on every run, including
  failures, so a refusal leaves an evidence trail.
- Viewer (then *Panther*, now [Loupe](https://loupe.dryfoos.com)) consumes the
  emitted manifest; the Gate never visualizes.

Components: bundle 0.2.0 · extension (as `clewseau-gate`) 0.2.0 · preset 0.1.0.

## 0.1.0 — 2026-08-05

- Initial bundle (as *clewseau*): durable-ID templates over stock Spec Kit,
  Gate 2 refusal of silent acceptance-criterion gaps, exact-set registry
  checking.
