#!/usr/bin/env python3
"""Sync the real HomesFlow twin sample from a Gate emit.

This refreshes ONLY `samples/homesflow.trace-manifest.json` (and, if a Loupe
checkout is reachable, its copy there). It never touches
`samples/sample.trace-manifest.json` — that synthetic `example-app` demo is
curated by hand, not synced (see samples/README.md).

Paths are resolved from the environment so nothing machine-specific is baked
in. Regenerate the real emit first, then run this:

  SPECASSAY_HOMESFLOW=/path/to/HomesFlow \
    bash extensions/specassay-check/scripts/check-traceability.sh
  SPECASSAY_HOMESFLOW=/path/to/HomesFlow \
    LOUPE_SAMPLES=/path/to/loupe/samples \
    python3 scripts/build-sample-manifest.py

Environment:
  SPECASSAY_HOMESFLOW  HomesFlow checkout whose trace-manifest.json to read
                       (defaults to a sibling ../HomesFlow if present).
  LOUPE_SAMPLES        Loupe samples/ dir to mirror the twin into (optional).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TWIN = ROOT / "samples" / "homesflow.trace-manifest.json"

ACCEPTED_FORMATS = {"trace-manifest", "clew"}  # accept pre-rename emits too


def _homesflow_manifest() -> Path | None:
    env = os.environ.get("SPECASSAY_HOMESFLOW")
    candidates = []
    if env:
        candidates.append(Path(env) / "trace-manifest.json")
    candidates.append(ROOT.parent / "HomesFlow" / "trace-manifest.json")
    for c in candidates:
        if c.exists():
            return c
    return None


def main() -> None:
    src = _homesflow_manifest()
    if src is None:
        raise SystemExit(
            "no HomesFlow emit found; set SPECASSAY_HOMESFLOW=/path/to/HomesFlow "
            "(and run the Gate there first)"
        )
    doc = json.loads(src.read_text(encoding="utf-8"))
    if doc.get("schemaVersion") not in (3, 4) or doc.get("format") not in ACCEPTED_FORMATS:
        raise SystemExit("not a schema v3/v4 trace-manifest")

    text = json.dumps(doc, indent=2) + "\n"
    TWIN.parent.mkdir(parents=True, exist_ok=True)
    TWIN.write_text(text, encoding="utf-8")
    print(
        f"Wrote {TWIN} ({len(doc.get('rows', []))} rows) "
        f"gate.ok={doc.get('gate', {}).get('ok')} counts={doc.get('statusCounts')}"
    )

    loupe_samples = os.environ.get("LOUPE_SAMPLES")
    if loupe_samples:
        dest = Path(loupe_samples) / "homesflow.trace-manifest.json"
        if dest.parent.exists():
            # Samples are honest emits — copy verbatim, never doctor fields.
            dest.write_text(text, encoding="utf-8")
            print(f"Synced {dest}")


if __name__ == "__main__":
    main()
