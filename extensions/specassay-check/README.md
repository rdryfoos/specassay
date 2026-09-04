# SpecAssay Check

You just installed this extension into a Spec Kit project. This page says what it is, what its config controls, what a run produces, and what green and red mean. Developer notes (running the test suite, building a release) live in [`DEVELOPING.md`](./DEVELOPING.md).

## What this extension is

SpecAssay Check is Gate 2 of the SpecAssay workflow: one bash script, `scripts/check-traceability.sh`, that reads four things in your repo and refuses to pass work with a silent gap between them.

| It reads | Looking for |
| --- | --- |
| Your ID registry (usually `PRD.md`) | Durable IDs: `US-…`, `FR-…`, `NFR-…`, `AC-…`, one line each |
| Your Spec Kit specs and tasks (`specs/**/spec.md`, `specs/**/tasks.md`) | The same IDs, and `**Carries**:` on every task |
| Your source tree | `@covers ID` marks on the code that serves each intent |
| Your test tree | Test names that carry an acceptance criterion's ID (`test_AC_SYNC_04_…`) |

Every run writes `trace-manifest.json`, the portable record of what it found, whether the Gate passed or not. [Loupe](https://loupe.dryfoos.com/) and any other viewer read that file; nothing re-scans your repo. The rules are written down once, in [`PROMOTION-CONTRACT.md`](../../PROMOTION-CONTRACT.md); the script enforces them.

## What you need

- **bash.** macOS and Linux are first-class. Windows needs Git Bash or WSL; PowerShell alone will not run it.
- **Python 3.8 or newer**, standard library only. The script finds it as `python3` or `python`, whichever you have, and says which one it used on its first lines. Set `SPECASSAY_PYTHON=/path/to/python3` to force a specific interpreter. With no usable Python 3 it stops at once with an install hint and exit 2.
- **Spec Kit 0.14 or newer**, with `specify init` already done in the project.

## Install

From the public catalogs, see the [root README](../../README.md#install-catalog-path). From a checkout of this repo:

```bash
specify extension add --dev /path/to/specassay/extensions/specassay-check
```

Install scaffolds `specassay-check-config.yml` next to this file from `config-template.yml`. You do not have to check whether that happened: every run reports it (next section).

## The config: `specassay-check-config.yml`

One YAML file, in this directory. Paths and globs are relative to your project root. The template has a comment on every key; the short version:

| Key | What it controls | Default |
| --- | --- | --- |
| `registry` | The file that holds your durable IDs. The Gate reads IDs only from definition-shaped lines (a bullet, the ID, a separator, a statement). | `PRD.md` |
| `target_name` | Display name written into the manifest | project directory name |
| `manifest_path` | Where `trace-manifest.json` is written | `trace-manifest.json` |
| `specs`, `tasks` | Globs for Spec Kit's spec and task files | `specs/**/spec.md`, `specs/**/tasks.md` |
| `src_globs` | Block list of globs scanned for `@covers` marks. Edit this for your layout. | `src/**` and an iOS example |
| `test_globs` | Block list of globs scanned for AC-named tests. Edit this too. | `tests/**` and an iOS example |
| `id_regex` | The ID grammar | `(FR\|NFR\|AC\|US)-<AREA>-<NN>[a-z]?` |
| `covers_regex`, `carries_regex`, `retires_regex`, `test_ac_regex` | How marks, task carries, retirement records, and test-name IDs are spelled | the shapes shown above |
| `test_results` | Optional JUnit XML from your own test run. When set, `proven` requires a passing test, not just a matching name. | unset |
| `parent_derivation` | `heading-nesting` derives parent edges from the registry's own indentation; unset means no edges | unset |
| `block_uncovered_proof` | Turns the `uncovered-proof` diagnostic into a refusal. Flip only once your own backlog of these is zero, with a dated comment. | unset (report-only) |
| `matrix_md`, `matrix_svg`, `portfolio_md` | Output paths for `--matrix` and `--portfolio` | `coverage.md`, `coverage.svg`, `portfolio-snapshot.md` |

The two list keys (`src_globs`, `test_globs`) must be block lists, one `- "glob"` per line. An inline array (`src_globs: ["src/**"]`) is refused before any scanning, on purpose: it used to parse as an empty list and silently mark everything backlog.

## Running it

From the project root:

```bash
bash .specify/extensions/specassay-check/scripts/check-traceability.sh
```

or the agent command `speckit.specassay-check.gate`, which runs the same script. Flags: `--matrix` also writes `coverage.md` and `coverage.svg`; `--portfolio` also writes `portfolio-snapshot.md`. Both re-present the same run, never a second scan.

The first lines of every run state how it is set up:

```text
SpecAssay Check (Gate 2) starting
  python: python3 (3.9.6)
  config: .specify/extensions/specassay-check/specassay-check-config.yml (from specassay-check-config.yml)
```

If the config file is missing, that line reads `config: MISSING at <path>`, followed by the exact `cp` command that scaffolds it. The run continues on the template's defaults so you still get output, but scaffold it before relying on the result.

## What a run produces

**On the console.** Setup lines (above), then zero or more `FAIL:` lines (each one a refusal, with the ID and the reason), zero or more `DIAGNOSTIC:` lines (real findings that do not fail the Gate on their own), then the write confirmations and a verdict:

```text
Wrote trace-manifest.v5beta.json (10 rows, schemaVersion 5, beta)
Wrote trace-manifest.json (10 rows) gate.ok=True
SpecAssay Check (Gate 2): OK (10 registry IDs)
```

**On disk.** `trace-manifest.json` (schema v4, the frozen four-status file) and `trace-manifest.v5beta.json` (schema v5, adds `retired` and parent edges), both written even when the Gate refuses, so the break is recorded rather than hidden. Format reference: [`docs/trace-manifest-schema.md`](../../docs/trace-manifest-schema.md).

**Exit code.**

| Exit | Meaning |
| --- | --- |
| 0 | Green. Nothing unfinished is hidden at acceptance-criterion altitude. |
| 1 | Red. At least one refusal; read the `FAIL:` lines. The manifest was still written. |
| 2 | Could not run. No usable Python 3, no config, or a config key that would be misread. Not a verdict on your thread; nothing was scanned and no manifest was written. |

## What green means

Green does not mean everything is done. It means every acceptance criterion in the registry is either proven or openly admitted as debt, and the registry, specs, and tasks agree on which IDs exist. Each row in the manifest carries one of these states:

| State | Meaning |
| --- | --- |
| `proven` | A named carrier exists: an AC-named test, or a `@covers` mark for a US/FR/NFR. A fact that a carrier exists, not a claim the code is correct. |
| `tracked-debt` | Started, proof missing, admitted on an open task with `**Carries**:`. Visible, on the books. |
| `backlog` | A US/FR/NFR with no carrier yet, or any ID carried only by an open task TODO. Planning altitude, not a gap. |
| `GAP` | An AC with neither proof nor open debt. The Gate refuses. |
| `retired` | Withdrawn on purpose, recorded in a dated `**Retires**:` line on an open task. v5beta only. |

**Green on an empty registry proves nothing.** With zero IDs there is nothing to check, so the Gate exits 0, says the registry is empty, and prints the on-ramp to a first mint (next section) instead of a bare OK.

## What red means

Each `FAIL:` line names one of these:

| Refusal | What it means |
| --- | --- |
| `silent gap: AC-X has no test and no open tracked-debt task` | An acceptance criterion nobody has proven or admitted. The core refusal. |
| `registry ID missing from specs` / `from tasks` | The registry promises an ID that no spec or task mentions (unless an open task carries it as backlog). |
| `spec references ID not in registry` / `tasks reference ID not in registry` | A spec or task invented an ID. Mint it in the registry, or fix the typo. |
| `untraced scope (@covers)` / `(test name)` | A mark or test name cites an ID that does not exist in the registry. |
| `duplicate definition line(s)` | The same ID minted twice, usually two branches. `scripts/mint-id.sh --resolve <ID>` hands back the next free offset. |
| `task without Carries` | A checkbox task that does not say which ID it serves. |
| `registry not found` | The config's `registry:` names a file that is not there. |

The manifest is still written on red, with `gate.ok: false` and every refusal under `gate.failures[]`. Fix the named ID, rerun. Symptoms that have confused real users, each with what taught it: [`docs/troubleshooting.md`](../../docs/troubleshooting.md).

## First run on a fresh project

Nothing is minted yet, so the registry is empty and the Gate is green with nothing behind it. It says so:

```text
SpecAssay Check (Gate 2): OK, registry empty (0 IDs in PRD.md)
  Nothing is promised yet, so there is nothing to check. The Gate stays green until a first ID exists; this green proves nothing.
  Mint a first ID, either way:
    greenfield (new work): mint the IDs for a story before writing its spec; the SpecAssay preset makes each Spec Kit spec inherit IDs from PRD.md rather than invent them.
      bash .specify/extensions/specassay-check/scripts/mint-id.sh AC LOGIN --append "Given a wrong password, when the user signs in, then the form shows an error and no session starts."
    brownfield (existing docs, no IDs yet): pick one requirement from a doc you already have and mint it with the same command, naming the doc in the statement. One is enough to start; do not backfill.
      bash .specify/extensions/specassay-check/scripts/mint-id.sh AC LOGIN --append "Given a wrong password (docs/auth.md, Sign-in), when the user signs in, then the form shows an error."
  Then rerun this check. Expect a refusal: the new ID has no spec, task, or test yet, so the Gate reports it as drift and a silent gap. That first honest red is the tool working.
  Clear it either way. An open task line carrying "**Carries**: AC-LOGIN-10", and nothing else yet, is anointed backlog: green and honest.
  Or name the ID in a specs/*/spec.md and on a task line with **Carries**, then write a test named test_AC_LOGIN_10_...: proven. Spec and task without the test is tracked-debt, also green.
```

If the registry file itself does not exist, the run is red with `registry not found` and tells you to either create it (`touch PRD.md`) or point `registry:` at the doc that already holds your requirements. Brownfield repos usually want the second.

## The other commands

| Command | Does |
| --- | --- |
| `scripts/mint-id.sh <PREFIX> <AREA> [--append "statement"]` or `speckit.specassay-check.mint` | Mints the next ID for a prefix and area, always a multiple of ten; `--append` also writes the registry line in the file's own style. `--resolve <ID>` resolves a duplicate. |
| `scripts/dig.py` or `speckit.specassay-check.dig` | Archaeology mode for an unfamiliar repo: proposes a candidate registry from tests, routes, and README tables, written only to `dig-report.json`. Deterministic, no LLM. |
| `check-traceability.sh --matrix` or `speckit.specassay-check.matrix` | `coverage.md` and `coverage.svg` for a PR or README. |
| `check-traceability.sh --portfolio` or `speckit.specassay-check.portfolio` | `portfolio-snapshot.md`, a plain-prose snapshot for a reader with no context. |
| `scripts/commit-advisory.sh` as a `commit-msg` hook | Warns, never blocks, when a commit message names an ID but no staged file carries its `@covers` mark. Install: `ln -sf ../../.specify/extensions/specassay-check/scripts/commit-advisory.sh .git/hooks/commit-msg` |

## CI is the property line

A local run is hygiene. The run that protects the thread is the one in CI, on every pull request and every push to a protected branch, failing the build on a non-zero exit. Keep the emitted `trace-manifest.json` from that run as evidence. A minimal GitHub Actions step:

```yaml
- name: SpecAssay Check (Gate 2)
  run: |
    set -euo pipefail
    SPECASSAY_PROJECT_ROOT="$PWD" \
    SPECASSAY_CONFIG="$PWD/.specify/extensions/specassay-check/specassay-check-config.yml" \
      bash .specify/extensions/specassay-check/scripts/check-traceability.sh
```

This repo runs exactly that against its own registry: [`.github/workflows/self-gate.yml`](../../.github/workflows/self-gate.yml).
