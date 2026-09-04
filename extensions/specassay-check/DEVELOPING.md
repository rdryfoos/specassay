# Developing SpecAssay Check

Notes for someone changing this extension, as opposed to using it. The user-facing page is [`README.md`](./README.md).

## Layout

| Path | Role |
| --- | --- |
| `scripts/check-traceability.sh` | The Gate. Bash, with Python 3 (standard library) for the JSON and SVG emit. |
| `scripts/mint-id.sh` | Mints the next ID for a prefix and area; resolves duplicates. |
| `scripts/lib-def-line.sh` | The one definition-line pattern both scripts above share, so they agree on what a real registry entry looks like. |
| `scripts/dig.py` | Archaeology mode. Pure Python, no dependencies. |
| `scripts/thread-report.py` | Builds the PR Thread Report from a base and head manifest. |
| `scripts/commit-advisory.sh` | The warn-only `commit-msg` hook. |
| `commands/*.md` | The agent-facing command files Spec Kit installs as skills. |
| `config-template.yml` | Scaffolded to `specassay-check-config.yml` on install. Every key commented. |
| `extension.yml` | Spec Kit extension manifest: version, required tools, provided commands and config. |
| `tests/` | The engine's own pytest suite. Every test builds a disposable project under `tmp_path` and runs the real script against it. |

## Running the tests

```bash
python3 -m pytest extensions/specassay-check/tests/ -q
```

Every Gate rule with a registry ID has a test named for its acceptance criterion (`test_AC_GATE_70a_…`), which is how this repo's own Self Gate counts that AC as proven (Rule 6a applies to us too). When you add a rule, mint its ID in `PRD.md`, name the test after the AC, and cite the test in `specs/self-gate-config/spec.md`. The suite is also the CI's first step, ahead of the self-gate.

Interpreter detection has tests of its own (`tests/test_gate_100_cold_install.py`): they put shim `python3` and `python` executables at the front of `PATH` to simulate a machine with only one of them, or neither.

## Dev install into a scratch project

```bash
specify init --here --integration claude --script sh --ignore-agent-tools --force
specify extension add --dev /path/to/specassay/extensions/specassay-check
specify preset add --dev /path/to/specassay/presets/specassay
```

`--dev` copies the directory; rerun `specify extension add --dev … --force` after editing a script to pick up the change.

## Config discovery, for anyone touching it

All three shell scripts resolve the same way: `SPECASSAY_PROJECT_ROOT` if set, else three levels up from this directory when installed under `.specify/extensions/`, else two levels up (this repo's own layout). Config is `SPECASSAY_CONFIG` if set, else `specassay-check-config.yml` here, else `config-template.yml` with a loud notice. Keep them in step; mint-id.sh's header says the same.

## Releasing

`scripts/build-release.sh` at the repo root zips the preset, this extension, and the bundle, and checks the zip names against what the catalogs point at. Versions live in `extension.yml`, `presets/specassay/preset.yml`, and `bundle.yml`; the changelog leads with the bundle version. The release runbook is [`RELEASE-HANDOFF.md`](../../RELEASE-HANDOFF.md).
