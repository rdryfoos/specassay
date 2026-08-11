# Bundle Submission draft — SpecAssay

Paste-ready answers for Spec Kit's **Bundle Submission** issue form
(`https://github.com/github/spec-kit/issues/new?template=bundle_submission.yml`).
File the [extension](extension-submission.md) and [preset](preset-submission.md)
submissions alongside it so the component catalogs graduate too.

---

**Bundle ID:** `specassay`

**Bundle Name:** SpecAssay

**Version:** 0.3.1

**Role or Team:** developer

**Description:**
Durable-ID traceability for stock Spec Kit: intent → build → proof, checked on
every push. Templates mint durable IDs (US/FR/NFR/AC); a deterministic Gate
refuses silent acceptance-criterion gaps and emits a vendor-neutral
`trace-manifest.json`; CI posts a Thread Report briefing on every PR.

**Author:** Rik Dryfoos / Dryfoos Consulting

**Repository URL:** https://github.com/rdryfoos/specassay

**Download URL:**
https://github.com/rdryfoos/specassay/releases/download/v0.3.1/specassay-0.3.1.zip
*(built by `specify bundle build`)*

**Documentation URL:** https://github.com/rdryfoos/specassay#readme
*(walkthroughs: https://www.specassay.com — field guide, Thread Report, PR for Intent)*

**License:** MIT

**Required Spec Kit Version:** >=0.14.0

**Integration Target:** *(empty — integration-agnostic)*

**Components Provided:**
- Extension `specassay-check` 0.3.1 — the Gate (`speckit.specassay-check.gate`
  command + `after_implement` hook): refuses silent AC gaps, invented IDs, and
  registry↔specs↔tasks drift; emits `trace-manifest.json` on every run,
  including failures. Ships the Thread Report CI tooling (PR briefing comment,
  Intent Changed detection, `offthread_ack`/`intent_ack` human-tick gates).
- Preset `specassay` 0.2.0 — appends durable-ID, `Carries:`, and SpecAssay
  vocabulary onto the stock spec, tasks, and constitution templates
  (append strategy; stock Spec Kit stays intact).

**Required Component Catalogs:**
- Extensions: `https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/extensions.json`
- Presets: `https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/presets.json`

Both hosted in the bundle repository; add with `--install-allowed`.

**Tags:** traceability, governance, durable-ids, gate, sdd

**Key Features:**
- Durable IDs minted at intent (never renumbered), `@covers` marks in source,
  proofs named to acceptance criteria — the Golden Thread, machine-checked.
- A deterministic Gate that refuses **silent** gaps only: honest debt
  (`tracked-debt`) and planned work (`backlog`) pass and stay visible.
- `trace-manifest.json` emitted on every run, including refusals — a
  vendor-neutral record any viewer can read (reference viewer:
  https://loupe.dryfoos.com, upload or `?manifest=` URL).
- Thread Report: one CI comment per PR — what moved on the thread, the touched
  story end to end, changed files that sit off the thread, and restated-intent
  detection with a three-tier re-confirm hint. Illuminates; never blocks.
  Live demos: [PR #1](https://github.com/rdryfoos/specassay/pull/1) (green),
  [PR #2](https://github.com/rdryfoos/specassay/pull/2) (broken),
  [PR #4](https://github.com/rdryfoos/specassay/pull/4) /
  [PR #5](https://github.com/rdryfoos/specassay/pull/5) (intent moved).
- Public evidence: HomesFlow, a real iOS app run under the practice
  (82-row manifest shipped as a sample).

**Testing Details:**
Validated and built with the real CLI (`specify 0.16.3.dev0`) from a clean
`specify init` project with the repo's catalogs added (`--install-allowed`):
`specify bundle validate --path <repo>` → *"specassay is well-formed and
valid"*; `specify bundle build` → the submitted artifact. Full transcript:
[test-evidence.md](test-evidence.md). Install was exercised end to end from
the built artifact and from the catalog stack in the same clean project.

**Example Usage:**
```sh
# In your Spec Kit project
specify extension catalog add --name specassay --install-allowed \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/extensions.json
specify preset catalog add --name specassay --install-allowed \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/presets.json
specify bundle catalog add --name specassay --install-allowed \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/bundles.json

specify bundle install specassay

# Configure the Gate (registry path, globs, ID grammar), then:
#   /speckit.specassay-check.gate   — run Gate 2; emits trace-manifest.json
# CI: run the Gate on every PR; see .github/workflows/thread-report.yml
# in the bundle repo for the Thread Report wiring.
```

**Proposed Catalog Entry:**
*(the `specassay` object from
[`catalogs/bundles.json`](../../catalogs/bundles.json) — paste it verbatim
under the top-level `bundles` object)*

**Additional Context:**
The trace-manifest format is deliberately vendor-neutral (`format` +
`schemaVersion` are the contract); a v5 interop revision is in beta with a
second emitter (docs/trace-manifest-v5.md). The walkthrough site
(https://www.specassay.com) shows the Thread Report and intent-PR behavior on
live PRs in this repository.
