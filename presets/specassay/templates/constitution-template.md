
<!-- SpecAssay (append) — constitution article -->

### Article: End-to-End Traceability (NON-NEGOTIABLE)

Every functional requirement, non-functional requirement, and acceptance criterion carries a durable unique ID of the form `<TYPE>-<DOMAIN>-<NN>` (e.g. `FR-LOG-01`, `AC-OFFL-03`). IDs are assigned once at the PRD level and are never reused or renumbered; retired IDs are tombstoned, not recycled.

1. Each acceptance criterion is **atomic** — one independently testable assertion — and maps to at least one automated test *or* an explicitly tracked debt entry. Silent-gap refusal is at **AC altitude**; US/FR/NFR IDs are planning labels (manifest status `backlog`), not silent-gap candidates.
2. Every task in `tasks.md` MUST declare the ID(s) it implements via a `Carries:` field.
3. Every verifying test MUST encode the AC ID it answers for. Every intent-bearing source module MUST carry a coverage annotation (a **mark** / `@covers`) naming the ID.
4. Coverage is **bidirectional** and machine-checked: no silent AC gaps, no untraced scope, and exact-set registry ≡ specs ≡ tasks. **CI fails the build on any of these** — local Gate is hygiene; CI Gate is the property line.
5. `/speckit.analyze` MUST report zero SpecAssay traceability violations before `/speckit.implement` runs.

### Article: SpecAssay vocabulary

Terms are minted once in `GLOSSARY.md`; this article restates them so the constitution is **self-contained** (agents follow it without fetching the glossary). When they disagree, the glossary wins. Use these terms; do not invent synonyms (especially not “dossier”).

| Term | Meaning |
|------|---------|
| **trace-manifest** | The check-emitted traceability artifact (`format: "trace-manifest"`). Default filename `trace-manifest.json`. |
| **trace-manifest.json** | Usual on-disk path for a trace-manifest (configurable via `manifest_path`). |
| **SpecAssay** | Spec Kit overlay: durable IDs, Gate 2, trace-manifest emission. |
| **Loupe** | Viewer that reads a trace-manifest only — no target re-scan. Reads any emitter's manifest. |
| **proven** | Named carrier exists (AC proof and/or `@covers` / proof for US/FR/NFR). A fact that a carrier exists, not a claim the code is correct. |
| **tracked-debt** | Incomplete, but declared on an open task with `Carries:`. |
| **GAP** | Silent AC gap — neither proof nor open debt; Gate refuses; the Golden Thread frays. |
| **backlog** | US/FR/NFR with no own carrier, or an anointed ID — planning altitude, not a silent gap. |
| **anointed backlog** | An ID minted ahead of its build: registry entry plus one open `Carries:` TODO. An honest “coming soon,” not a broken thread — how new scope enters without creating a GAP. |
| **mark** / **`@covers`** | A one-line comment in source naming the durable ID(s) that code serves. Greppable; author-written; the Gate reads it; Loupe shows it under Build. |
| **`Carries:`** | Mark on a task checkbox naming the ID(s) that task carries — usually open debt or anointed backlog. |
| **Gate 2** | Deterministic SpecAssay check + manifest emit (`speckit.specassay-check.gate`). |
