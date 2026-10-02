## CI is the property line

<!-- @covers FR-COLD-30, AC-COLD-30a -->

A local run is hygiene. The run that protects the thread is the one on the pull request, because the person who pushes unmarked work is the person who did not run it locally. One command installs it:

```bash
bash .specify/extensions/specassay-check/scripts/install-ci.sh
```

That copies [`ci/specassay.yml`](./ci/specassay.yml) to `.github/workflows/specassay.yml` at your repository root, and writes your project's own root into it if the project sits in a subdirectory. It refuses rather than overwrite a workflow that differs from the one your project should have, printing the `diff` command to look at first and the `--force` that replaces it.

The workflow is one file with two jobs, and needs no secrets:

- **On every pull request:** runs the Gate on the head and again on the base commit, works out which files changed, builds the Thread Report, and posts it as one comment that it updates in place rather than piling new ones up. Then, as a separate step, it fails the check if the Gate refused. The comment always posts, even on a broken thread, so a reviewer reads what broke in thread terms; the red check is the block and the comment never is.
- **When that comment is edited:** re-reads the tick boxes and updates the `specassay/ack` commit status. Inert unless your config sets `offthread_ack` or `intent_ack` to `required`. To make that status block a merge, add `specassay/ack` to the branch's required checks.

There is no path filter on the pull-request trigger, deliberately: a filter is a list somebody has to remember, and a pull request that produces no checks at all reads to a reviewer as "none required" rather than "none ran". Gating pushes to your protected branch as well means naming that branch in the `push:` trigger, which the workflow carries commented out rather than guessing what your branch is called.

**Why a command rather than the install doing it.** Spec Kit cannot place a file outside `.specify/extensions/<id>/`: its extension manifest provides commands, templates, scripts and config and deploys each of them under that directory, the only `.github` paths the CLI writes are Copilot prompts and `.github/hooks/speckit.json`, and hooks are agent-side events rather than install-time ones (read from Spec Kit 1.0.5's source, 2026-10-02). So the bundle ships the workflow and this command places it.

This repository runs a workflow of its own shape against its own registry, because it gates a bundle rather than a project: see [`.github/workflows/self-gate.yml`](https://github.com/rdryfoos/specassay/blob/main/.github/workflows/self-gate.yml) and [`.github/workflows/thread-report.yml`](https://github.com/rdryfoos/specassay/blob/main/.github/workflows/thread-report.yml). Those are ours, not a template: until today the only account of the plumbing a Thread Report needs was those files, named here by a relative link that resolved to nothing in anybody else's checkout.

# SpecAssay Check

You just installed this extension into a Spec Kit project. This page says what it is, what its config controls, what a run produces, and what green and red mean. Developer notes (running the test suite, building a release) live in [`DEVELOPING.md`](./DEVELOPING.md).

## What this extension is

SpecAssay Check is Gate 2 of the SpecAssay workflow: `scripts/check-traceability.sh`, which reads four things in your repo and refuses to pass work with a silent gap between them.

Two files, since 0.5.5, and you still only ever call the first: `scripts/check-traceability.sh` is a small launcher, and `scripts/check-traceability.impl.sh` is the Gate. The launcher parses the Gate before running it and refuses to let an exit 0 through unless a manifest was written, because 0.5.4 shipped a construct macOS's system bash cannot parse, and a checker that ran nothing read as green through a pipeline. The floor is **bash 3.2**, which is what a stock Mac has, and CI runs the suite on a macOS runner against `/bin/bash` as well as on Linux.

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
| `registry` | The file that holds your durable IDs. The Gate reads IDs only from definition-shaped lines (a bullet, the ID, a separator, a statement), and never from inside a fenced code block: a quoted row is an example, not a promise. | `PRD.md` |
| `target_name` | Display name written into the manifest | project directory name |
| `manifest_path` | Where `trace-manifest.json` is written | `trace-manifest.json` |
| `specs`, `tasks` | Globs for Spec Kit's spec and task files | `specs/**/spec.md`, `specs/**/tasks.md` |
| `src_globs` | Block list of globs scanned for `@covers` marks. Edit this for your layout. | `src/**` and an iOS example |
| `test_globs` | Block list of globs scanned for AC-named tests. Edit this too. | `tests/**` and an iOS example |
| `id_regex` | The ID grammar | `(FR\|NFR\|AC\|US)-<AREA>-<NN>[a-z]?` |
| `covers_regex`, `carries_regex`, `retires_regex`, `test_ac_regex` | How marks, task carries, retirement records, and test-name IDs are spelled | the shapes shown above |
| `test_results` | Optional JUnit XML from your own test run. When set, `proven` requires a passing test, not just a matching name. A report with **zero** test cases is refused (exit 2) rather than read as "nothing passed": some toolchains write one file per test framework and leave the others empty. | unset |
| `parent_derivation` | `heading-nesting` derives parent edges from the registry's own indentation; unset means no edges | unset |
| `block_uncovered_proof` | Turns the `uncovered-proof` diagnostic into a refusal. Flip only once your own backlog of these is zero, with a dated comment. | unset (report-only) |
| `matrix_md`, `matrix_svg`, `portfolio_md` | Output paths for `--matrix` and `--portfolio` | `coverage.md`, `coverage.svg`, `portfolio-snapshot.md` |

**Your grammar is consumed as configured.** `id_regex`, `test_ac_regex` and
the mark patterns are read as the project's own grammar everywhere, not just
at the front door. A test name cannot carry an ID's punctuation (most
languages forbid a dot or a hyphen in an identifier), so `AC-5.6.1a` is
written `test_AC_5_6_1_a`; the engine maps that back by looking the ID up in
your registry, not by substituting one character for another. Two IDs that
differ only in punctuation are refused rather than guessed between, and
`mint-id.sh` refuses to compose an ID your own `id_regex` would reject.

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
| 2 | Could not run. No usable Python 3, no config, a config key that would be misread, or a `test_results` report carrying no test cases. Not a verdict on your thread; nothing was scanned and no manifest was written. |

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
| `ambiguous IDs under proof matching` | Two minted IDs differ only in punctuation (`AC-1-2` and `AC-12`), so a test named for one cannot be told from a test named for the other. The registry has to settle it; the engine will not guess. |

The manifest is still written on red, with `gate.ok: false` and every refusal under `gate.failures[]`. Fix the named ID, rerun. Symptoms that have confused real users, each with what taught it: [`docs/troubleshooting.md`](../../docs/troubleshooting.md).

## First run on a fresh project

<!-- @covers FR-COLD-20, AC-COLD-20d -->

**Start with a registry.** Nothing in the install creates one, so the first command on a new project writes it from the seed this extension ships:

```bash
bash .specify/extensions/specassay-check/scripts/mint-id.sh --init
```

That writes the file your config's `registry:` key names, from [`templates/registry-seed.md`](./templates/registry-seed.md). The seed states the ID grammar in full, carries one example row of each of the four types with the `**Authorship**:` mark on it, and says what the four authorship words mean. It is the file a person reads to learn what a row looks like, so the grammar lives there rather than only inside a Gate refusal. Every example row sits inside a fenced block, which the Gate reads as a quotation, so the seed promises nothing and a first run on it is green with zero rows. `--init` never overwrites an existing registry; it refuses and names the file.

Brownfield repos usually want the other door: point `registry:` at the document that already holds your requirements, and mint one ID against a requirement in it.

Then, nothing being minted yet, the registry is empty and the Gate is green with nothing behind it. It says so:

```text
SpecAssay Check (Gate 2): OK, registry empty (0 IDs in PRD.md)
  Nothing is promised yet, so there is nothing to check. The Gate stays green until a first ID exists; this green proves nothing.
  Mint a first ID, either way:
    greenfield (new work): mint the IDs for a story before writing its spec; the SpecAssay preset makes each Spec Kit spec inherit IDs from PRD.md rather than invent them.
      bash .specify/extensions/specassay-check/scripts/mint-id.sh AC LOGIN --authorship case --append "Given a wrong password, when the user signs in, then the form shows an error and no session starts."
    brownfield (existing docs, no IDs yet): pick one requirement from a doc you already have and mint it with the same command, naming the doc in the statement. One is enough to start; do not backfill.
      bash .specify/extensions/specassay-check/scripts/mint-id.sh AC LOGIN --authorship case --append "Given a wrong password (docs/auth.md, Sign-in), when the user signs in, then the form shows an error."
  Then rerun this check. Expect a refusal: the new ID has no spec, task, or test yet, so the Gate reports it as drift and a silent gap. That first honest red is the tool working.
  Clear it either way. An open task line carrying "**Carries**: AC-LOGIN-10", and nothing else yet, is anointed backlog: green and honest.
  Or name the ID in a specs/*/spec.md and on a task line with **Carries**, then write a test named test_AC_LOGIN_10_...: proven. Spec and task without the test is tracked-debt, also green.
```

If the registry file itself does not exist, the run is red with `registry not found` and names both doors: `mint-id.sh --init`, or `registry:` pointed at the doc that already holds your requirements.

## The other commands

| Command | Does |
| --- | --- |
| `scripts/mint-id.sh --init` | Writes the registry from the shipped seed, which carries the grammar and one fenced example row of each type. Refuses rather than overwrite an existing registry. |
| `scripts/install-ci.sh` | Puts the shipped workflow at `.github/workflows/specassay.yml`, so every pull request runs the Gate and gets one Thread Report comment. Refuses rather than overwrite a workflow that differs; `--force` replaces it. |
| `scripts/mint-id.sh <PREFIX> <AREA> [--authorship <value>] [--append "statement"]` or `speckit.specassay-check.mint` | Mints the next ID for a prefix and area, always a multiple of ten, and prints the whole line to paste in the file's own style; `--append` also writes it. `--authorship` takes one of `case`, `design`, `retrospective`, `constitution` and puts the mark on the line; omitted, the row reads as unassigned, which is reported and not refused. `--resolve <ID>` resolves a duplicate. |
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
