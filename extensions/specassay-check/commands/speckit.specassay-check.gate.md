---
description: Run SpecAssay Check (Gate 2) — fail on silent gaps; emit trace-manifest.json
---

# SpecAssay Check (Gate 2)

1. Run the portable Gate 2 script shipped with SpecAssay. It checks that:

   * registry IDs ≡ IDs in specs ≡ IDs in tasks (exact-set drift),
   * durable IDs are either proven (named proof) or tracked as debt (open task) for ACs,
   * marks / test-encoded IDs are not orphans,
   * checkbox tasks declare `Carries:`,

   and always writes a trace-manifest (default `trace-manifest.json`, path configurable). The manifest is written even when the Gate fails, so GAPs and `gate.failures` are visible.
   `trace-manifest.json` is a portable, vendor-neutral artifact (`format: "trace-manifest"`, schemaVersion 4). It is not ReqIF/OSLC. Loupe (the viewer) consumes this file; it does not re-scan the target.

   ## Steps

   1. The script reports its own config state on its first lines: `config: <path> (from ...)` when found, or `config: MISSING at <path>` followed by the exact `cp` command that scaffolds it from `config-template.yml`. If it reports MISSING, run that command once, then make sure the new file points at this project's registry, specs, tasks, and source/test trees. Set `manifest_path` if you do not want `trace-manifest.json` at the project root.
   2. From the project root, run:

      ```sh
      SPECASSAY_PROJECT_ROOT="$PWD" \
      SPECASSAY_CONFIG="$PWD/.specify/extensions/specassay-check/specassay-check-config.yml" \
        bash .specify/extensions/specassay-check/scripts/check-traceability.sh
      ```

      The script writes `trace-manifest.json` (or the `manifest_path` from the
      config) and exits non-zero if the Gate refuses. Exit 2 means it could
      not run at all (no usable Python 3, no config); the message says what
      to install or create. A registry with zero IDs exits 0 and prints the
      on-ramp to a first mint instead of a bare OK; relay that text to the
      user, it is the next step.
