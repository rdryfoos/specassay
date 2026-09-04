# Test evidence: SpecAssay bundle v0.4.13

Clean-project installation test, per the Bundle Submission checklist, run
fresh against the tagged, published release on 2026-09-04 with the real Spec
Kit CLI (`specify 0.15.3.dev0`) on macOS (Python 3.9.6). The release tag
`v0.4.13` is commit `105c4845f8ae88f1af361d56c0de458089b50fad`; the Self Gate
run on that commit is
<https://github.com/rdryfoos/specassay/actions/runs/33883414322> (81 tests
passed, Gate 2 OK, 55 registry IDs) and the Release run that built and
published the assets is
<https://github.com/rdryfoos/specassay/actions/runs/33883485224>.

**Standing rule (2026-09-04):** every test-evidence entry names the Spec Kit
CLI version it ran on (`specify --version`), in its first paragraph. The
v0.4.13 evidence above ran on 0.15.3.dev0 two days after Spec Kit 1.0.4
shipped and nobody could tell from the file; that gap class dies here, the
way the stale-version-link class did.

New this time, and worth reading first: an **upgrade-path** section at the
end. A tester who installed v0.4.12 through the catalogs yesterday is waiting
on this release, so the update commands were run for real from a project at
v0.4.12, not assumed from the CLI's help text.

## Digest verification: downloaded bytes match the published release

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

## Inside the artifacts, not the source tree

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

## Validate and build from the pristine tagged checkout

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

## Clean Spec Kit project, install by bundle ID from the catalog stack

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

## Gate run on the untouched fresh project

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

## Upgrade path: a project installed at v0.4.12 through the catalogs

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

## Upgrade path: a git-clone install

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

## One measured friction, new this release

`raw.githubusercontent.com` serves the catalogs with `cache-control:
max-age=300`. A catalog fetched by anyone in the five minutes before a
version-bump push keeps serving the old version until that window expires:
observed here as a fresh install resolving 0.4.12 two minutes after the
0.4.13 catalogs were on `main` (`x-cache: HIT`, `source-age: 285`), and
0.4.13 four minutes later with no other change. Nothing to fix on our side;
recorded in `docs/migration.md` so the next release does not read it as a
broken push.

## Spec Kit 1.0.4 validation, 2026-09-04

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
