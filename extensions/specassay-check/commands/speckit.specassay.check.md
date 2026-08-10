---
description: Run SpecAssay Check (Gate 2) — fail on silent gaps; emit trace-manifest.json
---

# SpecAssay Check (Gate 2)

3. Run the portable Gate 2 script shipped with SpecAssay. It checks that:

   * registry IDs ≡ IDs in specs ≡ IDs in tasks (exact-set drift),
   * durable IDs are either proven (named proof) or tracked as debt (open task) for ACs,
   * marks / test-encoded IDs are not orphans,
   * checkbox tasks declare `Carries:`,

   and always writes a trace-manifest (default `trace-manifest.json`, path configurable). The manifest is written even when the Gate fails, so GAPs and `gate.failures` are visible.
   `trace-manifest.json` is a portable, vendor-neutral artifact (`format: "trace-manifest"`, schemaVersion 4). It is not ReqIF/OSLC. Loupe (the viewer) consumes this file; it does not re-scan the target.

   ## Steps

   1. Confirm `.specify/extensions/specassay-check/specassay-check-config.yml` exists (copy from `config-template.yml` if missing) and points at this project's registry, specs, tasks, and source/test trees. Set `manifest_path` if you do not want `trace-manifest.json` at the project root.
   2. From the project root, run:
