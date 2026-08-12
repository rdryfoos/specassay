# Changelog

All notable changes to the SpecAssay bundle. Versions follow [semver](https://semver.org);
the bundle version leads, component versions are listed per release.

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
