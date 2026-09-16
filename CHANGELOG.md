# Changelog

All notable changes to the SpecAssay bundle. Versions follow [semver](https://semver.org);
the bundle version leads, component versions are listed per release.

## Unreleased

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
