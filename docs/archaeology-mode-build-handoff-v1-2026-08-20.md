# Archaeology Mode — Build Handoff v1.0 FROZEN 2026-08-20

For: the SpecAssay/Docs room. Receipt required naming this version line. Converts the archaeology-mode-brief-2026-08-20.md (drawer, vision-level) into a build-ready spec. That brief's law stands and governs every ruling below: inferred and attested are never conflated; the Gate never reads a dug row as governed; anointment is the only crossing; annotate, never erase.

## 0. Test site, with permission on record

David Vydra (SpecDriven) has offered `github.com/SpecDriven/insurance-java` as a test repo for this feature — permission granted verbally to Rik, recorded here for provenance. Use it as the first real dig target once the command exists. It is an EXTERNAL, real, ungoverned repo — treat it as a genuine stranger's-repo test (relevant to vision-brief §7's falsifiable test T-b), not a fixture. Do not commit any dig output back to SpecDriven's repo; the dig-report is written to a location under our own control (see §3) unless and until David asks otherwise.

## 1. Scope of this build

Build the NO-LLM FLOOR ONLY. This is rung (a) of the three-rung ladder the brief specified; rungs (b) local-model and (c) user-supplied-API-key are explicitly OUT OF SCOPE for this handoff and follow once the floor is proven. The no-LLM floor is not a placeholder — the brief's own finding is that a test suite is a latent registry, and static heuristics over test names, routes, and structure should produce a genuinely useful dig on their own.

## 2. Command surface

New command: `specassay dig [path]` (default path: cwd), packaged alongside specassay-check's existing extension machinery (same install/scaffold pattern, same config file conventions). Proposed flags, builder's discretion on exact names: `--out <path>` (default per §3), `--sources <list>` (which heuristic sources to run; default all), `--dry-run` (print counts, write nothing). No flag enables inference beyond the no-LLM floor in this version — there is nothing to gate yet, but the flag surface should anticipate rungs b/c (e.g. a future `--engine local|api` that doesn't exist yet but whose absence should be a deliberate omission, not an oversight).

## 3. Sources and heuristics (no-LLM floor)

In priority order (highest-signal first), each proposed row must cite the specific evidence that produced it:

1. Test names and bodies — parse test function/method names for criterion-shaped language (given/when/then patterns, assertion targets); a test name is treated as a candidate AC statement, the test's own file:line as its provenance.
2. Route and API surface — controller/endpoint declarations, CLI subcommands: candidate FR statements ("the system accepts X"), provenance the declaring file:line.
3. Module/directory structure — top-level packages or directories as candidate AREA groupings (mirrors MAP's own area-parsing spirit, applied to unfamiliar structure instead of registry IDs).
4. README/docs prose — headings and stated features as candidate US statements, lowest priority (highest paraphrase risk; keep citations tight, short excerpts only, never long reproductions per copyright discipline).
5. Commit history — used for stratigraphy/grouping signal only in this version (what changed together, roughly when), not for minting individual rows; full commit-driven mining is a candidate for a later rung, not this build.

## 4. Dig-report schema (draft — builder authors the real one, this is the shape)

A new artifact, NOT the trace-manifest, NOT the cube. Proposed name: `dig-report.json`, living at repo root or `.specify/dig-report.json` — builder's call, document the choice. Required shape per row: candidate id-shaped label (draft only, not a minted ID), statement text, type guess (US/FR/AC/NFR), epistemic class = `inferred` (constant, always present, never omitted), provenance (source kind from §3's list, file, line or range, and for test-derived rows the test's own name), confidence signal (builder's discretion on shape — even a simple high/medium/low is fine), suggested area grouping. Document-level: generator version, source repo path, generated-at timestamp, source commit if available. The report is FLAT DATA — it does not chain, cover, or gate anything; the Gate must not load it.

## 5. The one hard law, restated for the build

No dug row is ever written into the real registry, ever, by this command. `specassay dig` only ever produces `dig-report.json`. There is no `--anoint` flag on this command. Anointment (turning a proposed row into a real, dated, minted registry row) is future work per the brief — a separate, later capability, likely delivered as a generated PR per the brief's ratified §Q2 ruling — and is explicitly NOT part of this build. This build's Gate must be trivially provable to never touch the real registry: write a pinned test asserting the dig produces no writes outside dig-report.json.

## 6. Explicitly deferred (do not build)

- Rungs (b) local-model and (c) user-supplied-API-key inference.
- The anointment room / PR-generation flow.
- Any Tally-side ghost-layer rendering (held, per Rik, for a later combined session — Tally has more coming besides this).
- Commit-history row-minting (only grouping signal in this version, per §3.5).
- Secret-scrubbing pipeline: not yet load-bearing since no external call exists in the no-LLM floor, but note the requirement in code comments so rung (c) doesn't ship without it.

## 7. Sequencing

1. Receipt this document by version line.
2. Registry mint pass: propose the real FR/AC/US rows for the dig command itself (this handoff is prose, not registry law — the room mints as usual).
3. Build the no-LLM floor per §2–5.
4. Dry-run against a small local fixture first; confirm the no-write-outside-dig-report test passes.
5. Run for real against `github.com/SpecDriven/insurance-java` (clone read-only; do not push anything to that repo). Report back: row counts by type and source, a handful of representative proposed rows, and an honest assessment of whether the no-LLM floor produced something a human would find useful — that assessment is the actual test of this build, more than any unit test.
6. Pause-and-escalate stands throughout, as always.

Please edit this file as we go along; edits after crossing require re-delivery with a version bump.
