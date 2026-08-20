# Test evidence — SpecAssay bundle v0.4.12

Clean-project installation test, per the Bundle Submission checklist, run fresh
against the tagged, published release — not a version-bumped edit of an older
trial. All runs used the real Spec Kit CLI (`specify 0.15.3.dev0`) against the
published `v0.4.12` release assets and this repository's hosted catalogs, on
2026-08-20. The published release tag is exactly `HEAD` of this repo at the
time of the trial (`8f964996d983494458d6fcc1cdadec97d30c1e64`, `git describe
--tags --exact-match HEAD` → `v0.4.12`), so `bundle validate`/`bundle build`
below ran against the pristine tagged tree, not a working copy that might
have drifted from what shipped.

## Digest verification — installed bytes match the published release

Before installing anything, the three release assets were downloaded directly
and hashed locally, then compared against the digests GitHub's own API
reports for the same release (`gh api repos/rdryfoos/specassay/releases/tags/v0.4.12`):

```
$ shasum -a 256 specassay-0.4.12.zip specassay-check-0.4.12.zip specassay-preset-0.4.12.zip
4716129a1c5fef94fd310401c68ebd76104e3c7af5b3124f0af7d6118e5752fd  specassay-0.4.12.zip
6d449e8d755f038100f759667d91801655c768d5446c46cbda69fc31b330a976  specassay-check-0.4.12.zip
58bb4ed34ad725b51ba3dece242022250b1741588ef6ed9e6df841d1c77f8b2a  specassay-preset-0.4.12.zip

$ gh api repos/rdryfoos/specassay/releases/tags/v0.4.12 --jq '.assets[] | "\(.name): \(.digest)"'
specassay-0.4.12.zip: sha256:4716129a1c5fef94fd310401c68ebd76104e3c7af5b3124f0af7d6118e5752fd
specassay-check-0.4.12.zip: sha256:6d449e8d755f038100f759667d91801655c768d5446c46cbda69fc31b330a976
specassay-preset-0.4.12.zip: sha256:58bb4ed34ad725b51ba3dece242022250b1741588ef6ed9e6df841d1c77f8b2a
```

All three match exactly.

## Setup — clean Spec Kit project

```sh
mkdir testproj && cd testproj
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

## Validate + build (from a pristine v0.4.12 checkout)

```
$ git describe --tags --exact-match HEAD
v0.4.12

$ specify bundle validate --path /Users/spudnik/specassay
✓ specassay is well-formed and valid.

$ specify bundle build --path /Users/spudnik/specassay --output dist
✓ Built specassay-0.4.12.zip (110 files) → dist/specassay-0.4.12.zip
```

The released artifact is built by the same command in CI
(`.github/workflows/release.yml`) — the workflow resolves references through
these catalogs exactly as an adopter's project would.

## Install by bundle ID from the install-allowed catalog stack

```
$ specify bundle install specassay
Updated execute permissions on 4 script(s) recursively
✓ Installed 'specassay' (2 added, 0 already present).

$ specify bundle list

Installed bundles:

  specassay v0.4.12 (2 components, installed 2026-08-20T16:30:32Z)

$ specify preset list

Installed Presets:

  SpecAssay (specassay) v0.4.12 — enabled — priority 10
    Appends durable-ID, Carries, and SpecAssay vocabulary onto Spec Kit spec,
tasks, and constitution templates.
    Tags: traceability, durable-ids, governance, sdd
    Templates: 3

$ specify extension list

Installed Extensions:

  ✓ SpecAssay Check (v0.4.12)
     specassay-check
     Gate 2 refuses silent gaps and emits a trace-manifest
(`trace-manifest.json`).
     Commands: 2 | Hooks: 1 | Priority: 10 | Status: Enabled
```

## Gate run, real refusal on a fresh install

The Gate config did not auto-scaffold in this trial, so the README's documented
fallback was used, then the Gate was run for real against the untouched fresh
project (no registry minted yet):

```
$ cp .specify/extensions/specassay-check/config-template.yml \
     .specify/extensions/specassay-check/specassay-check-config.yml

$ bash .specify/extensions/specassay-check/scripts/check-traceability.sh
FAIL: registry not found: PRD.md
Wrote trace-manifest.v5beta.json (0 rows, schemaVersion 5, beta)
Wrote trace-manifest.json (0 rows) gate.ok=False
SpecAssay Check (Gate 2): FAILED
```

Honest behavior on a genuinely empty project: no registry yet is a loud,
named `FAIL`, not a silent pass — and both `trace-manifest.json` and
`trace-manifest.v5beta.json` are still written (0 rows), matching Rule 4a's
promise that the refusal is always recorded, never hidden. This closes the
gap in the prior trial for this release (`docs/testing/completed/
evidence-cold-agent-trial-observed-2026-08-19.md`), which ran against
pre-tag `main` before `v0.4.12` existed; this one ran against the tagged,
published release itself.

## Notes

- Digest verification (above) is new to this evidence file — added per the
  design room's ruling that a submission's linked evidence should trace to
  the exact bytes a maintainer or adopter would actually download, not just
  "it installed."
- `specify` version in this trial is `0.15.3.dev0`, the CLI actually
  installed locally at trial time; the v0.3.1 evidence this file replaces
  recorded `0.16.3.dev0` from an earlier local environment. Neither number
  is asserted as a compatibility floor — `requires.speckit_version:
  ">=0.14.0"` in the catalogs is the actual constraint.
