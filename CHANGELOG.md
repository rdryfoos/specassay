# Changelog

All notable changes to the SpecAssay bundle. Versions follow [semver](https://semver.org);
the bundle version leads, component versions are listed per release.

## 0.4.0 — 2026-08-14

Concurrent minting stops failing silently, and a new tool makes it cheap to
avoid failing at all.

- **`mint-id.sh`** (new): mints the next ID for a given prefix and area by
  scanning the registry for the highest existing number, rather than
  requiring a human or agent to eyeball the file and guess. Mints land on
  multiples of ten (`AC-HOME-10`, `AC-HOME-20`, ...); a brand-new area
  starts at 10. The step size does not reduce how often two branches
  collide on the same next number (both compute from the same
  last-observed state regardless of step size), but it reserves the `1`
  through `9` offset off every decade exclusively for resolving a
  collision, so fixing one is a purely local `+1` (`mint-id.sh --resolve
  AC-HOME-20` → `AC-HOME-21`) with no need to recompute the registry's
  current state. The ones digit doubles as a free collision counter for
  that slot. Reuses the same config discovery and registry conventions as
  `check-traceability.sh`.
- **`duplicate-id` Gate refusal** (new failure kind): two independent
  definition lines minting the same ID used to merge cleanly and vanish
  silently, because the exact-set check dedupes the registry with `sort
  -u` before looking at it, and the trace-manifest only ever kept the
  first matching line's statement. Gate 2 now detects any ID with more
  than one definition-shaped line and refuses, naming both line numbers.
  Detection is scoped to definition-shaped lines only (a shared pattern
  with `mint-id.sh`'s own style-detection, `lib-def-line.sh`) so a
  range-summary table using an ID as a range endpoint, or any other line
  that merely mentions an ID, is never mistaken for a second mint of it;
  verified against HomesFlow's real registry (0 false positives across 82
  IDs) and a new fixture, `samples/sample-duplicate-id.trace-manifest.json`.
- Registry-only for this release. Duplicate detection does not extend to
  specs or tasks referencing an ID more than once, which is repetition,
  not minting.
- `mint-id.sh` and the duplicate-id refusal are a matched pair: the decade
  scheme's payoff is a cheap resolution at the exact moment the Gate
  refuses a collision. Shipping the mint helper without the refusal would
  leave the collision-masking hole open; shipping the refusal without the
  helper would leave collision resolution as manual arithmetic.

Components: bundle 0.4.0 · extension `specassay-check` 0.4.0 · preset
`specassay` 0.4.0.

## 0.3.4 — 2026-08-13

- **The preset's own README pointed at a stale asset.** `presets/specassay/README.md`
  ships inside the preset zip, and its install command still named
  `v0.3.1/specassay-preset-0.2.0.zip` even after two version bumps, because
  neither sweep grepped that file. Found by Copilot review on the generated
  preset PR. Fixed, and since the file ships inside the artifact, the fix
  needed a real release rather than a docs-only push: republishing v0.3.3's
  assets under the same tag with different contents would have repeated the
  exact mismatch this bundle exists to catch.

Components: bundle 0.3.4 · extension `specassay-check` 0.3.4 · preset
`specassay` 0.3.4.

## 0.3.3 — 2026-08-13

Two findings from Spec Kit review, and a versioning rule to keep them from
recurring.

- **Required tools are declared.** `extension.yml` carried `tools: []` while
  the submission text promised `python3 (>=3.8)`, so the generated catalog
  entry reported every Python 3 as compatible. The extension now declares
  `bash` and `python3 >=3.8` in the schema the catalog uses. The constraint
  is conservative on purpose: the shipped code parses on 3.7, and 3.8 is what
  is supported and tested.
- **All three components share the bundle's version, from here on.** Spec
  Kit's preset workflow expects a release tag matching the preset's own
  version, and a preset at 0.2.1 riding in a v0.3.2 release cannot satisfy
  that. Component versions now move together with the bundle, so the release
  tag always matches every component.

Components: bundle 0.3.3 · extension `specassay-check` 0.3.3 · preset
`specassay` 0.3.3.

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
