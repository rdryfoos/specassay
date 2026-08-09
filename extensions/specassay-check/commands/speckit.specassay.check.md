---
description: Run SpecAssay Check (Gate 2) — fail on silent gaps; emit trace-manifest.json
---

# SpecAssay Check (Gate 2)

Run the portable Gate 2 script shipped with this extension. It checks that:

- registry IDs ≡ IDs in specs ≡ IDs in tasks (**exact-set** drift),
- durable IDs are either proven (named proof) or tracked as debt (open task) for **ACs**,
- coverage annotations / test-encoded IDs are not orphans,
- checkbox tasks declare `Carries:`,

and **always writes a trace-manifest** (default `trace-manifest.json`, path configurable) — the SpecAssay matrix. The manifest is written even when the gate fails, so GAPs and `gate.failures` are visible.

`trace-manifest.json` is a portable, vendor-neutral matrix (`format: "trace-manifest"`, schemaVersion 4). It is not ReqIF/OSLC. Loupe (the viewer) consumes this file; it does not re-scan the target.

## Steps

1. Confirm `.specify/extensions/specassay-check/specassay-check-config.yml` exists (copy from `config-template.yml` if missing) and points at this project's registry, specs, tasks, and source/test trees. Set `manifest_path` if you do not want `trace-manifest.json` at the project root.
2. From the project root, run:

```bash
bash .specify/extensions/specassay-check/scripts/check-traceability.sh
```

3. Report the script's exit code, any `FAIL:` lines, and confirm `trace-manifest.json` (or configured `manifest_path`) was written.
4. Do **not** weaken the gate. If something is unfinished, it belongs as tracked debt (unchecked task with `Carries:`), not as a silenced gap.
5. Reminder: **proven** means a named proof exists — not that a full suite was asserted green by this script.
