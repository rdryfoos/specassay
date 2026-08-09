# SpecAssay vocabulary

Copy into the project glossary (e.g. `glossary.md`) when the repo keeps one. The same terms are appended to the constitution via the SpecAssay preset.

| Term                     | Meaning                                                      |
| ------------------------ | ------------------------------------------------------------ |
| **trace-manifest**       | The check-emitted traceability artifact (`format: "trace-manifest"`). Default filename `trace-manifest.json`. |
| **trace-manifest.json**  | Usual on-disk path for a trace-manifest (configurable via `manifest_path`). |
| **SpecAssay**            | Spec Kit overlay: durable IDs, Gate 2, trace-manifest emission. |
| **Loupe**                | Viewer that reads a trace-manifest only — no target re-scan. Reads any emitter's manifest. |
| **gilt**                 | Work dressed to gleam like done with nothing underneath: code with no intent behind it, "done" with no proof answering for it. The failure SpecAssay exists to catch. From the assay office: base metal gilded to pass as gold. |
| **proven**               | Named carrier exists (AC proof and/or `@covers` / proof for US/FR/NFR). A fact that a carrier exists, not a claim the code is correct. |
| **tracked-debt**         | Incomplete, but declared on an open task with `Carries:`. Visible, on the books. |
| **GAP**                  | Silent AC gap — neither proof nor open debt; the Golden Thread is broken; Gate refuses. |
| **backlog**              | US/FR/NFR with no own carrier, or an anointed ID — planning altitude, not a silent gap. |
| **anointed backlog**     | An ID minted ahead of its build: registry entry plus one open `Carries:` TODO. An honest "coming soon," not a broken thread. Anointing is how new scope enters without creating a GAP. |
| **Golden Thread**        | The intent → build → proof chain a trace-manifest records. Human-facing: the Golden Thread is intact or broken. Prefer this wording over "Gate passed/failed" except when naming the check script itself. The lineage is the [UK's "golden thread" of building-safety records](https://www.gov.uk/government/publications/building-regulations-advisory-committee-golden-thread-report/building-regulations-advisory-committee-golden-thread-report#golden-thread-definition) and Jonathan Smart's "golden thread" in *[Sooner Safer Happier](https://www.soonersaferhappier.com/)*. |
| **mark** / **`@covers`** | Leave a mark when you touch the work: a one-line comment in source naming the durable ID(s) that code serves. Greppable; author-written; Gate reads it; Loupe shows it under Build. The lineage is the maker's mark, struck by the maker before the assay office tests; the hallmark belongs to the trace-manifest. |
| **`Carries:`**           | Mark on a task checkbox naming the ID(s) that task carries — usually open debt or anointed backlog. |
| **Gate 2**               | Deterministic SpecAssay check + manifest emit (`speckit.specassay.check`). The mechanism that judges the Golden Thread; say "Gate" when you mean this script, "Golden Thread" when you mean what the human sees. Local runs are hygiene; **CI Gate is the property line** that protects the codebase. |
