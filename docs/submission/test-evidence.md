# Test evidence — SpecAssay bundle v0.3.1

Clean-project installation test, per the Bundle Submission checklist. All runs
used the real Spec Kit CLI (`specify 0.16.3.dev0`) against the published v0.3.1 release
assets and this repository's hosted catalogs.

## Setup — clean Spec Kit project

```sh
mkdir testproj && cd testproj
specify init --here --integration claude --script sh --ignore-agent-tools

specify extension catalog add --name specassay --install-allowed \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/extensions.json
specify preset catalog add --name specassay --install-allowed \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/presets.json
specify bundle catalog add --id specassay --policy install-allowed \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/bundles.json
```

## Validate + build (from the clean project, against a pristine checkout)

```
$ specify bundle validate --path <repo>
✓ specassay is well-formed and valid.

$ specify bundle build --path <repo> --output dist
✓ Built specassay-0.3.1.zip
```

The released artifact is built by the same command in CI
(`.github/workflows/release.yml`) — the workflow resolves references through
these catalogs exactly as an adopter's project would.

## Install by bundle ID from the install-allowed catalog stack

```
$ specify bundle install specassay
Updated execute permissions on 1 script(s) recursively
✓ Installed 'specassay' (2 added, 0 already present).

$ specify bundle list

Installed bundles:

  specassay v0.3.1 (2 components, installed 2026-08-11T13:17:04Z)

$ specify extension list

Installed Extensions:

  ✓ SpecAssay Check (v0.3.1)
     specassay-check
     Gate 2 — refuse silent gaps and emit a trace-manifest 
(`trace-manifest.json`).
     Commands: 1 | Hooks: 1 | Priority: 10 | Status: Enabled


$ specify preset list

Installed Presets:

  SpecAssay (specassay) v0.2.0 — enabled — priority 10
    Appends durable-ID, Carries, and SpecAssay vocabulary onto Spec Kit spec, 
tasks, and constitution templates.
    Tags: traceability, durable-ids, governance, sdd
    Templates: 3
```

## Notes

- The v0.3.0 → v0.3.1 bump exists because Spec Kit's installer (correctly)
  refused v0.3.0: extension commands must follow
  `speckit.{extension-id}.{command}`. The command is now
  `speckit.specassay-check.gate`. The refusal was caught by running this
  exact install test — the checklist works.
