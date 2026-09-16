# Test evidence: SpecAssay bundle

Entries are per release, newest first. **Standing rule (2026-09-04):** every
test-evidence entry names the Spec Kit CLI version it ran on (`specify
--version`), in its first paragraph. An entry that does not is not evidence of
compatibility with anything.

## v0.5.0 — released 2026-09-16

Everything here ran on Linux with the real Spec Kit CLI (`specify 1.0.4`),
Python 3.11.15, bash 5.2.21. The entry is in two halves and says which is which,
because they were written on either side of the tag: **pre-tag** evidence came
from the source tree and from zips built locally by `scripts/build-release.sh`,
while the **post-tag** section below ran against the published assets. The tag
is `v0.5.0` at `899420356a4b0fa89366034787d793b561ee1e0a`.

### Pre-tag: the suite, under both awks

`python3 -m pytest extensions/specassay-check/tests/ -q` passes 92 tests. The
same 92 pass with `awk` resolving to GNU Awk 5.2.1 instead of the container's
mawk: the 0.5.0 fix includes an `awk -v` escape-processing divergence that CI
(gawk) caught and the container (mawk) could not see, so the suite is now run
under both rather than one.

### Pre-tag: the regression tests fail against the version they were written for

Ten of the eleven new tests in
`extensions/specassay-check/tests/test_gate_110_nonstock_grammar.py` fail when
copied into a worktree checked out at the literal `v0.4.13` tag, and pass after
(`10 failed, 1 passed`). The eleventh is the static `awk -v` guard, and it passes
there for a real reason rather than a lucky one: at v0.4.13 the configured
retirement mark was interpolated into `sed`, not passed through an
escape-processed `awk -v` assignment. The `awk -v` shape was introduced by the
first repair in this release and caught by CI, so that test guards against
reintroducing a regression made while fixing v0.4.13, not against v0.4.13
itself. A release that fixed these without tests that would have caught them
would repeat the original error.

### Pre-tag: this repo's own Gate, at 65 rows

`SPECASSAY_PROJECT_ROOT="$PWD" SPECASSAY_CONFIG="$PWD/specassay-check-config.yml"
bash extensions/specassay-check/scripts/check-traceability.sh` exits 0:
`OK (65 registry IDs)`, `gate.ok=True`, 59 proven / 1 tracked-debt / 0 GAP /
5 backlog. Two `uncovered proof` diagnostics (`AC-LOGIN-10`, `AC-ZK9Q-01`) are
unchanged from v0.4.13 and come from fixture ID strings inside the suite's own
files. The six IDs minted for this release (`FR-GATE-110`/`AC-GATE-110`,
`FR-GATE-120`/`AC-GATE-120`, `FR-GATE-130`/`AC-GATE-130`) all land `proven`,
each AC by a named test and each FR by an `@covers` mark in the script that
implements it.

### Pre-tag: the manifests agree and the artifacts build

`specify bundle validate` in the repo root: `specassay is well-formed and
valid.` `bash scripts/build-release.sh`: `Versions: bundle 0.5.0 · extension
0.5.0 · preset 0.5.0`, three zips built, and its own closing check reports
`Artifacts and catalog download URLs agree.`

### Pre-tag: a clean project, installed from the locally built zip

`specify init --here --force --non-interactive --ignore-agent-tools
--integration claude --script sh` in an empty directory, then `specify extension
add <path-to-repo>/extensions/specassay-check --dev`. `specify extension list`
reports `SpecAssay Check (v0.5.0)`, `Commands: 5 | Hooks: 1`, and the install
scaffolds `.specify/extensions/specassay-check/specassay-check-config.yml`. The
first Gate run there refuses honestly, naming the missing registry and both ways
to fix it. A stock thread (one ID in `PRD.md`, named in a spec, carried by an
open task, proven by `test_AC_LOGIN_10_wrong_password_shows_error`) then runs
`OK (1 registry IDs)`.

### Pre-tag: the headline fix, end to end in that clean project

With the scaffolded config's `id_regex` changed to
`(AC|FR)-[0-9]+(\.[0-9]+)*[a-z]?` and `test_ac_regex` to
`AC_[0-9]+(_[0-9]+)*(_[a-z])?`, a dotted ID `AC-5.6.1a` proven by
`test_AC_5_6_1_a_replays_queued_cards` emits as `proven` with that test named in
its `proofs[]`. On v0.4.13 the same thread was unreachable by any test, because
the proof scan rewrote the test's token by a hardcoded rule instead of resolving
it against the registry the config produced. This is a real install of the built
extension, not a fixture.

### Post-tag: the published release, 2026-09-16

The tag `v0.5.0` is commit `899420356a4b0fa89366034787d793b561ee1e0a` (the merge
of PR #14). The Self Gate on that commit is
<https://github.com/rdryfoos/specassay/actions/runs/35151718593> and the Release
run that built and published the assets is
<https://github.com/rdryfoos/specassay/actions/runs/35151943499>. Everything
below was run against the published assets on `specify 1.0.4`, Python 3.11.15,
Linux, the same day.

#### Digest verification, three ways

```
# 1. from the release itself
$ gh api repos/rdryfoos/specassay/releases/tags/v0.5.0 --jq '.assets[] | "\(.name) \(.digest)"'
specassay-0.5.0.zip         sha256:737c1963ec86e83a0a312bf1addb70069e177398f3d0be4f99dfdccd51dd9464
specassay-check-0.5.0.zip   sha256:0aa651a6fe7a44e1030b555a55b94d415b2f10d0ab722d81dae4520019407394
specassay-preset-0.5.0.zip  sha256:d5e4e75b3f07c0555ffb2fc318a6a5c308126ef73a4df1f0b8241b3da9fc2a8b

# 2. the downloaded bytes, hashed locally
$ sha256sum *.zip
737c1963ec86e83a0a312bf1addb70069e177398f3d0be4f99dfdccd51dd9464  specassay-0.5.0.zip
0aa651a6fe7a44e1030b555a55b94d415b2f10d0ab722d81dae4520019407394  specassay-check-0.5.0.zip
d5e4e75b3f07c0555ffb2fc318a6a5c308126ef73a4df1f0b8241b3da9fc2a8b  specassay-preset-0.5.0.zip
```

Third way, inside the artifacts rather than the source tree: `bundle.yml`,
`extension.yml`, and `preset.yml` unzipped from the published zips each declare
`version: "0.5.0"`, and the bundle's `requires.speckit_version` reads
`>=0.14.0,<2.0.0`. The preset README that ships inside its own zip installs from
the version-agnostic `releases/latest/download/specassay-preset.zip`, so round
3's stale-install-line class cannot recur there. No scratch output leaked in:
no `trace-manifest.json`, `coverage.*`, or `portfolio-snapshot.md` at the bundle
root (the `samples/*.trace-manifest.json` files that a naive grep catches are
committed fixtures, not build residue). The extension zip's
`scripts/check-traceability.sh` really carries the fix: `id_for_test_token`,
`ambiguous-id-key`, and `ENVIRON[` all appear, and `mint-id.sh` carries its
refusal.

The unversioned aliases (`specassay.zip`, `specassay-check.zip`,
`specassay-preset.zip`) are byte-identical to their versioned twins, same
digests, which is what makes the `releases/latest/download/…` install lines
honest.

#### Clean project, installed by bundle ID from the catalog stack

`specify init --here --force --non-interactive --ignore-agent-tools
--integration claude --script sh`, then the three `catalog add` commands against
`raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/…`.

```
$ specify bundle install specassay
✓ Installed 'specassay' (2 added, 0 already present).

$ specify bundle list
  specassay v0.5.0 (2 components, installed 2026-09-16T22:27:16Z)

$ specify preset list
  SpecAssay (specassay) v0.5.0 — enabled — priority 10

$ specify extension list
  ✓ SpecAssay Check (v0.5.0)
     Commands: 5 | Hooks: 1 | Priority: 10 | Status: Enabled
```

No raw-catalog lag this time: the install resolved 0.5.0 on the first try, about
an hour after the catalogs were on `main`, well past the five-minute
`max-age` window `docs/migration.md` §4 describes.

#### The Gate on that fresh project, all the way to proven

A missing `PRD.md` refuses and names both ways out. `touch PRD.md` gives the
empty-registry on-ramp (`OK, registry empty (0 IDs in PRD.md)` with both mint
commands printed). The printed `mint-id.sh` command works and appends
`AC-LOGIN-10`. The next run refuses exactly as the on-ramp promised — missing
from specs, missing from tasks, silent gap — and a spec mention, one open
`**Carries**` line, and `test_AC_LOGIN_10_wrong_password_shows_error` turn it
`proven`.

#### The headline fix, on the published bits

With the scaffolded config's `id_regex` set to
`(AC|FR)-[0-9]+(\.[0-9]+)*[a-z]?` and `test_ac_regex` to
`AC_[0-9]+(_[0-9]+)*(_[a-z])?`, a dotted `AC-5.6.1a` proven by
`test_AC_5_6_1_a_replays_queued_cards` emits `proven` with that test named in
its `proofs[]`.

And the new refusal, on the same install, with `id_regex: "AC-[0-9-]+"`:

```
FAIL: ambiguous IDs under proof matching: AC-1-2 AC-12 differ only in
punctuation, so a test named for one cannot be told from a test named for another
SpecAssay Check (Gate 2): FAILED
```

That is `FR-GATE-120`, the upgrade-blocker, reading as intended for someone who
meets it cold.

#### Upgrade path, from a real v0.4.13 install

A second clean project installed `specassay v0.4.13` by bundle ID from the
catalogs at the `v0.4.13` ref, then got the same dotted thread: `PRD.md`,
`specs/cards/spec.md`, an open task carrying the ID, and
`test_AC_5_6_1_a_replays_queued_cards`, with the config's grammar keys edited to
match.

```
# BEFORE, on the real published v0.4.13
SpecAssay Check (Gate 2): OK (1 registry IDs)
[('AC-5.6.1a', 'tracked-debt', [])]
```

Green, with a named passing test present and `proofs[]` empty. That is the
defect this release exists for, reproduced on the shipped v0.4.13 bits rather
than on a fixture: the criterion can never become `proven`, and nothing says so.
(The row reads `tracked-debt` here because the ID is named in a spec; carried by
a task alone it would read `backlog`. Both are legal passing states, which is
what makes the failure silent either way.)

Then the documented upgrade, exactly as `docs/migration.md` gives it:

```
$ rm -rf .specify/extensions/.cache .specify/presets/.cache
$ specify bundle update specassay
✓ Updated 'specassay' to v0.5.0.

$ specify bundle list
  specassay v0.5.0 (2 components, installed 2026-09-16T22:28:05Z)
$ specify extension list
  ✓ SpecAssay Check (v0.5.0)
$ specify preset list
  SpecAssay (specassay) v0.5.0 — enabled — priority 10
```

The edited `specassay-check-config.yml` survived the update untouched, both
grammar keys intact. Same project, same files, same config, one command apart:

```
# AFTER
SpecAssay Check (Gate 2): OK (1 registry IDs)
[('AC-5.6.1a', 'proven', ['test_AC_5_6_1_a_replays_queued_cards'])]
```

The cache clear is still required, as it was for 0.4.12 → 0.4.13: without it the
update reports the old version. That friction is unchanged and already
documented.

#### One setup artefact, named so nobody reads it as a finding

The first `specify bundle update` in the upgrade project returned `Updated
'specassay' to v0.4.13` — no move at all. Cause was this test's own scaffolding,
not the tool: to install v0.4.13 after the catalogs had already moved, the
project had catalogs pinned at the `v0.4.13` ref, and adding the `main` ones
under a second name left both in the stack at the same priority, where the
alphabetically earlier pinned entry won. A real adopter has one catalog entry
pointing at `main` and never sees this. Removing the pinned entries and rerunning
the documented command moved both components in one go, as shown above.

#### Still owed

- The site's hero pin moved to the `v0.5.0` README anchor, per
  `docs/submission/CHEATSHEET.md`. That is the sites room's file, not this repo's.
- The three submission-form issues upstream, which now carry two versions' worth
  of change.
- `ONBOARD.md`'s receipts re-captured on v0.5.0 by a cold operator
  (`docs/docs-gaps.md` item 11).

## v0.4.13 — published release, 2026-09-04

Clean-project installation test, per the Bundle Submission checklist, run
fresh against the tagged, published release on 2026-09-04 with the real Spec
Kit CLI (`specify 0.15.3.dev0`) on macOS (Python 3.9.6). The release tag
`v0.4.13` is commit `105c4845f8ae88f1af361d56c0de458089b50fad`; the Self Gate
run on that commit is
<https://github.com/rdryfoos/specassay/actions/runs/33883414322> (81 tests
passed, Gate 2 OK, 55 registry IDs) and the Release run that built and
published the assets is
<https://github.com/rdryfoos/specassay/actions/runs/33883485224>.

Where the standing rule at the top of this file came from: this entry ran on
`specify 0.15.3.dev0`, two days after Spec Kit 1.0.4 shipped, and nobody could
tell from the file. That gap class died here, the way the stale-version-link
class did.

New that release, and worth reading first: an **upgrade-path** section at the
end. A tester who installed v0.4.12 through the catalogs the day before was
waiting on it, so the update commands were run for real from a project at
v0.4.12, not assumed from the CLI's help text.

### Digest verification: downloaded bytes match the published release

```
$ shasum -a 256 specassay-0.4.13.zip specassay-check-0.4.13.zip specassay-preset-0.4.13.zip
8529e8b7542a712542321856368b4f3d7f2f820f98350f7c7f7115670005f18d  specassay-0.4.13.zip
d7ac14c271b99aff0b649def9c3444b6e03090649df43ea2b9c3949ded91ed9f  specassay-check-0.4.13.zip
ed4298d72b80f083400c0ac7bcbf9a3eb5d5950eb50abd542e8fc4b5b77d8a58  specassay-preset-0.4.13.zip

$ gh api repos/rdryfoos/specassay/releases/tags/v0.4.13 --jq '.assets[] | "\(.name): \(.digest)"'
specassay-0.4.13.zip: sha256:8529e8b7542a712542321856368b4f3d7f2f820f98350f7c7f7115670005f18d
specassay-check-0.4.13.zip: sha256:d7ac14c271b99aff0b649def9c3444b6e03090649df43ea2b9c3949ded91ed9f
specassay-preset-0.4.13.zip: sha256:ed4298d72b80f083400c0ac7bcbf9a3eb5d5950eb50abd542e8fc4b5b77d8a58
```

All three match. A local `specify bundle build` from the pristine tagged
checkout (below) produced a bundle zip with the same digest as the published
one, so the CI build is reproducible byte for byte.

### Inside the artifacts, not the source tree

Per the cheat sheet's round-3 scar, the published zips were unzipped and
checked directly:

```
$ unzip -qo specassay-check-0.4.13.zip -d ext
$ grep -c resolve_python ext/scripts/check-traceability.sh
2
$ grep -m1 'registry empty' ext/README.md
SpecAssay Check (Gate 2): OK, registry empty (0 IDs in PRD.md)
$ ls ext
commands  config-template.yml  DEVELOPING.md  extension.yml  README.md  scripts  tests

$ unzip -qo specassay-preset-0.4.13.zip -d pre
$ grep -n releases/download pre/README.md
8:specify preset add --from https://github.com/rdryfoos/specassay/releases/download/v0.4.13/specassay-preset-0.4.13.zip
```

The extension zip carries the interpreter detection and the empty-registry
on-ramp; the preset zip's own README names the v0.4.13 asset.

### Validate and build from the pristine tagged checkout

```
$ git clone --branch v0.4.13 https://github.com/rdryfoos/specassay.git clone
$ cd clone && git describe --tags --exact-match HEAD
v0.4.13

$ specify bundle validate --path ./clone
✓ specassay is well-formed and valid.

$ specify bundle build --path ./clone --output dist
✓ Built specassay-0.4.13.zip → dist/specassay-0.4.13.zip
$ shasum -a 256 dist/specassay-0.4.13.zip
8529e8b7542a712542321856368b4f3d7f2f820f98350f7c7f7115670005f18d  dist/specassay-0.4.13.zip
```

### Clean Spec Kit project, install by bundle ID from the catalog stack

```sh
mkdir evproj && cd evproj
specify init --here --integration claude --script sh --ignore-agent-tools

specify preset catalog add \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/presets.json \
  --name specassay --install-allowed
specify extension catalog add \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/extensions.json \
  --name specassay --install-allowed
specify bundle catalog add \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/bundles.json \
  --id specassay --policy install-allowed
```

```
$ specify bundle install specassay
Updated execute permissions on 4 script(s) recursively
✓ Installed 'specassay' (2 added, 0 already present).

$ specify bundle list
Installed bundles:
  specassay v0.4.13 (2 components, installed 2026-09-04T14:27:58Z)

$ specify preset list
Installed Presets:
  SpecAssay (specassay) v0.4.13 — enabled — priority 10

$ specify extension list
Installed Extensions:
  ✓ SpecAssay Check (v0.4.13)
     specassay-check
     Commands: 5 | Hooks: 1 | Priority: 10 | Status: Enabled
```

### Gate run on the untouched fresh project

`specify bundle install` does not scaffold `specassay-check-config.yml`
(`specify extension add` does). As of this release the Gate says so itself
on its first lines, with the one command that fixes it, and the missing
registry gets its own next step:

```
$ bash .specify/extensions/specassay-check/scripts/check-traceability.sh
SpecAssay Check (Gate 2) starting
  python: python3 (3.9.6)
  config: MISSING at .specify/extensions/specassay-check/specassay-check-config.yml (looked via specassay-check-config.yml)
          running on config-template.yml defaults for now (registry PRD.md, specs/**, src/**, tests/**)
          scaffold it once: cp .specify/extensions/specassay-check/config-template.yml .specify/extensions/specassay-check/specassay-check-config.yml
          then edit registry, src_globs, and test_globs in that file for this repo
FAIL: registry not found: PRD.md
  The config's registry: key names the file that holds your durable IDs. Either create it (touch PRD.md) and mint a first ID into it, or point registry: at the doc that already holds your requirements. Then rerun.
Wrote trace-manifest.v5beta.json (0 rows, schemaVersion 5, beta)
Wrote trace-manifest.json (0 rows) gate.ok=False
SpecAssay Check (Gate 2): FAILED
```

Loud, named, nonzero, manifest still written. With an empty `PRD.md` in
place the run is green and prints the on-ramp to a first ID instead of a
bare OK (full text in `extensions/specassay-check/README.md`, "First run
on a fresh project").

### Upgrade path: a project installed at v0.4.12 through the catalogs

Set up the way the README installs (bundle by ID), while the hosted
catalogs still said 0.4.12, then upgraded after the 0.4.13 catalogs went
live. The user's own edited config (`target_name: "upgproj-edited"`) was in
place before the upgrade.

The plain update commands do not see the new version, because the
project's catalog cache is stale (`docs/migration.md`, friction 3):

```
$ specify extension update specassay-check
🔄 Checking for updates...
✓ specassay-check: Up to date (v0.4.12)

$ specify bundle update specassay
Error: Extension 'specassay-check' is pinned to version 0.4.13 in the bundle
manifest, but the resolved version is 0.4.12. Update the bundle's pinned version
or the source before installing.
```

Clearing the cache first is what works, and it is the command handed to the
waiting tester verbatim:

```
$ rm -rf .specify/extensions/.cache .specify/presets/.cache
$ specify bundle update specassay
Updated execute permissions on 4 script(s) recursively
✓ Updated 'specassay' to v0.4.13.

$ specify extension list
  ✓ SpecAssay Check (v0.4.13)
$ specify preset list
  SpecAssay (specassay) v0.4.13 — enabled — priority 10

$ grep -n '^target_name' .specify/extensions/specassay-check/specassay-check-config.yml
7:target_name: "upgproj-edited"

$ bash .specify/extensions/specassay-check/scripts/check-traceability.sh
SpecAssay Check (Gate 2) starting
  python: python3 (3.9.6)
  config: .specify/extensions/specassay-check/specassay-check-config.yml (from specassay-check-config.yml)
Wrote trace-manifest.v5beta.json (0 rows, schemaVersion 5, beta)
Wrote trace-manifest.json (0 rows) gate.ok=True
SpecAssay Check (Gate 2): OK, registry empty (0 IDs in PRD.md)
  ...
```

The edited config survived, and both new behaviors (interpreter line,
empty-registry on-ramp) arrived. `specify extension update specassay-check`
after the same cache clear also finds `0.4.12 → 0.4.13`, but prompts
`Update these extensions? [y/N]` and so needs a terminal; `bundle update`
does not prompt.

### Upgrade path: a git-clone install

```
$ git clone --branch v0.4.13 https://github.com/rdryfoos/specassay.git clone
$ specify extension add --dev ./clone/extensions/specassay-check --force
  ✓ SpecAssay Check (v0.4.13)
$ bash .specify/extensions/specassay-check/scripts/check-traceability.sh
  python: python3 (3.9.6)
SpecAssay Check (Gate 2): OK, registry empty (0 IDs in PRD.md)
```

`--force` re-copies the scripts and reports `Config files already exist
(preserved)`.

### One measured friction, new this release

`raw.githubusercontent.com` serves the catalogs with `cache-control:
max-age=300`. A catalog fetched by anyone in the five minutes before a
version-bump push keeps serving the old version until that window expires:
observed here as a fresh install resolving 0.4.12 two minutes after the
0.4.13 catalogs were on `main` (`x-cache: HIT`, `source-age: 285`), and
0.4.13 four minutes later with no other change. Nothing to fix on our side;
recorded in `docs/migration.md` so the next release does not read it as a
broken push.

### Spec Kit 1.0.4 validation, 2026-09-04

Same v0.4.13 artifacts, run again on **Spec Kit 1.0.4** (the CLI pinned to
the `v1.0.4` tag, commit `cb610277`; previously 0.15.3.dev0). Spec Kit
1.0.0 shipped 2026-08-21 and 1.0.4 on 2026-09-02; the 1.0.x line tightened
bundler and preset validation in exactly the paths SpecAssay installs
through, so this is the first evidence that the >=0.14.0 claim holds past
1.0. Everything below passed; one behavior change and one non-result are
called out where they happened.

```
$ uv tool install --force --from "git+https://github.com/github/spec-kit.git@v1.0.4" specify-cli
 + specify-cli==1.0.4 (from git+https://github.com/github/spec-kit.git@cb610277fdea781fcfa83d20522c2db37c94068d)
$ specify --version
specify 1.0.4
```

**Digests** of the downloaded assets matched the release API byte for byte
(same three sha256 values as the section above; the unversioned aliases
`specassay.zip`, `specassay-check.zip`, `specassay-preset.zip` report the
same digests as their versioned twins).

**Pristine tagged checkout under the 1.0.4 bundler:**

```
$ git clone --branch v0.4.13 https://github.com/rdryfoos/specassay.git clone
$ specify bundle validate --path ./clone
✓ specassay is well-formed and valid.
$ specify bundle build --path ./clone --output dist && shasum -a 256 dist/specassay-0.4.13.zip
8529e8b7542a712542321856368b4f3d7f2f820f98350f7c7f7115670005f18d  dist/specassay-0.4.13.zip
```

Reproducible on 1.0.4 as on 0.15.3.dev0.

**Catalog path, clean project** (the README's install commands, verbatim):

```
$ specify init --here --integration claude --script sh --ignore-agent-tools
$ specify preset catalog add .../main/catalogs/presets.json --name specassay --install-allowed
$ specify extension catalog add .../main/catalogs/extensions.json --name specassay --install-allowed
$ specify bundle catalog add .../main/catalogs/bundles.json --id specassay --policy install-allowed
$ specify bundle install specassay
✓ Installed 'specassay' (2 added, 0 already present).
$ specify bundle list
  specassay v0.4.13 (2 components, installed 2026-09-04T18:14:55Z)
$ specify preset list
  SpecAssay (specassay) v0.4.13 — enabled — priority 10
$ specify extension list
  ✓ SpecAssay Check (v0.4.13)
     Commands: 5 | Hooks: 1 | Priority: 10 | Status: Enabled
$ ls .specify/extensions/specassay-check/
commands  config-template.yml  DEVELOPING.md  extension.yml  README.md  scripts  specassay-check-config.yml  tests
```

**Behavior change, not a break:** on 1.0.4 `specify bundle install`
scaffolds `specassay-check-config.yml`. On 0.15.3.dev0 it did not (recorded
above). Cause: github/spec-kit#4285, "scaffold extension config when
installing via bundler", merged 2026-09-01, shipped in 1.0.3. The Gate's
first lines report which case it is in either way, so no adopter has to
know which CLI they have. The root README sentence that said bundle install
does not scaffold is corrected in this same commit.

**Gate on the untouched project** (no `PRD.md`): config found, then
`FAIL: registry not found: PRD.md`, manifest written with 0 rows,
`gate.ok=False`, exit 1. Same words as the 0.15.3.dev0 run.

**Direct-download path, second clean project** (the README's `--from
.../releases/latest/download/...` commands, verbatim; the CLI's per-URL
confirmation answered with `yes |`):

```
$ specify extension add specassay-check --from https://github.com/rdryfoos/specassay/releases/latest/download/specassay-check.zip
Config scaffolded:
  • .specify/extensions/specassay-check/specassay-check-config.yml
$ specify preset add --from https://github.com/rdryfoos/specassay/releases/latest/download/specassay-preset.zip
✓ Preset 'SpecAssay' v0.4.13 installed (priority 10)
$ specify extension list
  ✓ SpecAssay Check (v0.4.13)
$ specify preset list
  SpecAssay (specassay) v0.4.13 — enabled — priority 10
```

Gate on that project without `PRD.md`: the same `registry not found`
refusal.

**The on-ramp, end to end** (first project, `touch PRD.md`):

```
$ bash .specify/extensions/specassay-check/scripts/check-traceability.sh
SpecAssay Check (Gate 2): OK, registry empty (0 IDs in PRD.md)
  Nothing is promised yet, so there is nothing to check. ...
      bash .specify/extensions/specassay-check/scripts/mint-id.sh AC LOGIN --append "Given a wrong password, when the user signs in, then the form shows an error and no session starts."
  ...
$ bash .specify/extensions/specassay-check/scripts/mint-id.sh AC LOGIN --append "Given a wrong password, when the user signs in, then the form shows an error and no session starts."
AC-LOGIN-10
appended to PRD.md
$ bash .specify/extensions/specassay-check/scripts/check-traceability.sh
FAIL: registry ID missing from specs: AC-LOGIN-10
FAIL: registry ID missing from tasks: AC-LOGIN-10
FAIL: silent gap: AC-LOGIN-10 has no test and no open tracked-debt task
SpecAssay Check (Gate 2): FAILED
```

The printed command ran unchanged; the next run refused on all three counts
the on-ramp said it would. Cleared both ways the on-ramp names:

```
$ printf -- '- [ ] T001 Wrong-password sign-in shows an error. **Carries**: AC-LOGIN-10\n' > specs/001-login/tasks.md
$ bash .specify/extensions/specassay-check/scripts/check-traceability.sh
SpecAssay Check (Gate 2): OK (1 registry IDs)

$ printf 'AC-LOGIN-10: wrong password shows an error and no session starts.\n' > specs/001-login/spec.md
$ printf 'def test_AC_LOGIN_10_wrong_password_shows_error():\n    assert True\n' > tests/test_login.py
$ bash .specify/extensions/specassay-check/scripts/check-traceability.sh
DIAGNOSTIC: uncovered proof: AC-LOGIN-10 has a passing test but no file's @covers line names it
SpecAssay Check (Gate 2): OK (1 registry IDs)
$ python3 -c "import json;m=json.load(open('trace-manifest.json'));print(m['rows'][0]['status'])"
proven
```

Anointed backlog is green; spec plus task plus a named test is proven, with
the report-only uncovered-proof diagnostic firing as shipped (the test had
no `@covers` line).

**Upgrade path, v0.4.12 to v0.4.13 under the 1.0.4 bundler** (third clean
project, catalogs first pointed at the `v0.4.12` tag's files, then swapped
to `main`):

```
$ specify bundle install specassay
$ specify bundle list
  specassay v0.4.12 (2 components, installed 2026-09-04T18:16:10Z)
$ sed -i '' 's/^target_name:.*/target_name: "upgproj-edited"/' .specify/extensions/specassay-check/specassay-check-config.yml
$ specify {preset,extension,bundle} catalog remove specassay   # then re-add pointing at main
$ specify bundle update specassay
✓ Updated 'specassay' to v0.4.13.
$ specify extension list
  ✓ SpecAssay Check (v0.4.13)
$ specify preset list
  SpecAssay (specassay) v0.4.13 — enabled — priority 10
$ grep -n '^target_name' .specify/extensions/specassay-check/specassay-check-config.yml
7:target_name: "upgproj-edited"
$ bash .specify/extensions/specassay-check/scripts/check-traceability.sh
SpecAssay Check (Gate 2): OK, registry empty (0 IDs in PRD.md)
```

Edited config survived, both components moved together, Gate green after.

**Non-result, stated so it is not misread:** the update found 0.4.13
*without* the cache clear that friction 3 (`docs/migration.md`) requires
on 0.15.3.dev0. That is not evidence the friction is gone on 1.0.x: this
replay swapped catalog sources (remove, re-add), which fetches fresh,
whereas the friction is about an unchanged source whose content moved. The
first attempt here, with the sources left in place, was refused as a
duplicate name and never exercised the stale case. Friction 3 stays as
written until someone reproduces its exact shape on 1.0.x.

**What this proves and what it changes.** v0.4.13 installs, validates,
rebuilds byte-identical, gates, mints, refuses, and upgrades on Spec Kit
0.14.0 (cold trials), 0.15.3.dev0 (the entries above), and 1.0.4 (this
entry). Spec Kit enforces `requires.speckit_version` as a hard
`CompatibilityError` at install (`extensions/__init__.py`,
`check_compatibility`, PEP 440 `SpecifierSet`) and has no field for
"tested on", so the manifests now say `>=0.14.0,<2.0.0`: the proven major
line, in the one field the resolver reads. A literal `<=1.0.4` would have
refused every adopter on the next Spec Kit patch (1.0.2, 1.0.3, and 1.0.4
landed on three consecutive days), which is the staleness class this repo
just retired, reintroduced by hand. The exact proven versions live in this
file and in the README's "Before you install". The manifest change ships
with the next release per the versioning law; the catalogs and the
paste-from docs keep saying what the v0.4.13 zips actually say until then.
