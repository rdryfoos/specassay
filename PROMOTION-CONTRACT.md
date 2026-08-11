# SpecAssay Promotion Contract

This document defines the rules of promotion: what counts as covered, what counts as debt, what gets refused. The contract is the spec; SpecAssay carries it into your templates and enforces it at the Gate. Any tool honoring these rules can enforce them; prior art is thick (see [Lineage](#lineage-name-prior-art-first)). SpecAssay's contribution is economic: the tracing that only regulated work could once afford now costs a mark, a name, and a TODO. That makes honesty cheaper than hiding, and work that cannot hide cannot be gilt.

## One sentence

Mint durable IDs at intent; refuse silent gaps; allow tracked debt to stay visible.

## Rules

1. **Mint at intent.** IDs are assigned once in the authoritative registry (usually the PRD), not inferred from code later. Feature specs inherit; they do not mint.

2. **Immutability.** Never renumber. Never reuse. Retire in place (tombstone), do not recycle.

3. **Atomic ACs.** One acceptance criterion, one independently testable assertion. Split compounds before Spec Kit ingests them.

4. **Propagation.** Every task declares `Carries:` with the ID(s) it serves. Source that serves an intent carries an `@covers` mark (or language equivalent). Every verifying test names the AC in its identifier. **Exact-set:** registry ≡ specs ≡ tasks. No unclaimed registry IDs, no invented feature IDs. One deliberate exception: anointed backlog (rule 5a).

5. **Coverage altitude.** An intent counts as covered when its acceptance criteria are covered, or explicitly tracked as debt. **AC is the atomic unit of "covered"** and the only altitude where silent-gap refusal applies. US/FR/NFR are planning altitude: without a carrier of their own they are `backlog`, never `GAP`. An ID sitting quietly in the PRD with no claim at all is not allowed; that is exact-set drift, not a spec switch.

   **5a. Anointed backlog.** Minting an ID is a promise, and the Gate holds you to it immediately. To mint ahead of the work: mint the ID *and* write one open `Carries:` TODO for it (conventionally in `specs/backlog/tasks.md`). The TODO is the claim; it proves intent and names who carries the item. The ID rides as `backlog`, ACs included: an anointed AC is not a *silent* gap. The moment a spec claims the ID, the anointment expires and normal rules apply. A typo'd ID in a spec never comes with a matching TODO, so drift still fails exact-set.

6. **Honest states.** Prefer named states over a false green:

   - **proven**: a named carrier exists (an AC proof, or `@covers`/proof for US/FR/NFR). A fact that a carrier exists, not a claim the code is correct.
   - **tracked-debt**: work started, proof missing, but declared on an open task with `Carries:`. Visible, on the books.
   - **backlog**: US/FR/NFR with no own carrier, or any ID anointed into backlog (registry entry plus open `Carries:` TODO and nothing else). Planning altitude, not a broken thread.
   - **GAP**: a silent AC gap, neither proof nor open debt. The Golden Thread is broken; the Gate refuses.

7. **Refusal.** Gate 1 (judgment, e.g. `/speckit.analyze`) and Gate 2 (deterministic check) fail closed on silent AC gaps, untraced scope, and registry↔spec↔tasks drift. Passing does not mean zero unfinished work; it means zero *hidden* unfinished work at AC altitude, and zero abandoned or invented IDs in the planning layer.

   **7a. CI is the property line.** A Gate on a compliant laptop is courtesy and fast feedback. A cowboy (or a cold agent) with no local SpecAssay install can still push unmarked work. Gate 2 must run in CI on every PR and every commit to a protected branch, and must fail the build when the Golden Thread breaks. Local Gate is optional hygiene; the CI Gate protects the thread. The trace-manifest emitted on that run is the refusal's evidence trail.

8. **Trace-manifest.** Gate 2 emits a **trace-manifest** (default path `trace-manifest.json`): a portable, vendor-neutral matrix (`format: "trace-manifest"`) with a top-level `gate: { ok, failures[] }` so non-row refusals (orphans, missing `Carries:`, drift) are visible to viewers. The file is written even when the Gate fails. It is not ReqIF/OSLC; see [`docs/trace-manifest-schema.md`](./docs/trace-manifest-schema.md).

9. **Attribution is not authentication.** Optional operator stamps record claimed provenance in an already-trusted context. They enforce nothing about who may act.

10. **Viewer invariant.** Gate PASS ⇔ contiguous braid in Loupe; Gate FAIL ⇔ fray, the Golden Thread broken. Excused incompleteness carries its own color without fray: amber for tracked debt, blue for not-yet backlog. Red is reserved for fray and refusal only.

## What SpecAssay is not

- Not a fork of Spec Kit, and not a replacement: a bundle that overlays the stock workflow.
- Not Thorsten Schlathölter's [`clew`](https://ariadne-thread.io) (an inner-loop, code-anchored constructor). SpecAssay is complementary altitude — promotion and refusal on the outer loop — and cites `clew` as prior art.
- Not agent kanban or human-lane orchestration (a separate concern).
- Not a visualizer. [Loupe](https://loupe.dryfoos.com) (or any viewer) may read `trace-manifest.json`; viewers never mint IDs or re-scan the target.

## Paste-ready constitution article

Add to `.specify/memory/constitution.md` (or feed `/speckit.constitution`):

> ### Article: End-to-End Traceability (NON-NEGOTIABLE)
>
> Every functional requirement, non-functional requirement, and acceptance criterion carries a durable unique ID of the form `<TYPE>-<DOMAIN>-<NN>` (e.g. `FR-LOG-01`, `AC-OFFL-03`). IDs are assigned once at the PRD level and are never reused or renumbered; retired IDs are tombstoned, not recycled.
>
> 1. Each acceptance criterion is **atomic**, one independently testable assertion, and maps to at least one automated test *or* an explicitly tracked debt entry. Silent-gap refusal is at **AC altitude**; US/FR/NFR IDs are planning labels (trace-manifest status `backlog`), not silent-gap candidates.
> 2. Every task in `tasks.md` MUST declare the ID(s) it implements via a `Carries:` field.
> 3. Every verifying test MUST encode the AC ID it answers for. Every intent-bearing source module MUST carry a coverage annotation naming the ID.
> 4. Coverage is **bidirectional** and machine-checked: no silent AC gaps, no untraced scope, and **exact-set** registry ≡ specs ≡ tasks (no abandoned PRD IDs, no invented feature IDs). CI fails the build on any of these; local Gate is hygiene, the CI Gate is the property line.
> 5. `/speckit.analyze` MUST report zero SpecAssay traceability violations before `/speckit.implement` runs.
>
> ### Article: SpecAssay vocabulary
>
> Terms are minted once in `GLOSSARY.md`; this article restates them so the constitution is self-contained. When they disagree, the glossary wins. Use these terms; do not invent synonyms (especially not "dossier").
>
> | Term                     | Meaning                                                      |
> | ------------------------ | ------------------------------------------------------------ |
> | **trace-manifest**       | The check-emitted traceability artifact (`format: "trace-manifest"`). Default filename `trace-manifest.json`. |
> | **trace-manifest.json**  | Usual on-disk path for a trace-manifest (configurable via `manifest_path`). |
> | **SpecAssay**            | Spec Kit overlay: durable IDs, Gate 2, trace-manifest emission. |
> | **Loupe**                | Viewer that reads a trace-manifest only — no target re-scan. Reads any emitter's manifest. |
> | **gilt**                 | Work dressed to gleam like done with nothing underneath: code with no intent behind it, "done" with no proof answering for it. The failure SpecAssay exists to catch. From the assay office: base metal gilded to pass as gold. |
> | **proven**               | Named carrier exists (AC proof and/or `@covers` / proof for US/FR/NFR). A fact that a carrier exists, not a claim the code is correct. |
> | **tracked-debt**         | Incomplete, but declared on an open task with `Carries:`. Visible, on the books. |
> | **GAP**                  | Silent AC gap — neither proof nor open debt; the Golden Thread is broken; Gate refuses. |
> | **backlog**              | US/FR/NFR with no own carrier, or an anointed ID — planning altitude, not a silent gap. |
> | **anointed backlog**     | An ID minted ahead of its build: registry entry plus one open `Carries:` TODO. An honest "coming soon," not a broken thread. Anointing is how new scope enters without creating a GAP. |
> | **Golden Thread**        | The intent → build → proof chain a trace-manifest records. Human-facing: the Golden Thread is intact or broken. Prefer this wording over "Gate passed/failed" except when naming the check script itself. The lineage is the [UK's "golden thread" of building-safety records](https://www.gov.uk/government/publications/building-regulations-advisory-committee-golden-thread-report/building-regulations-advisory-committee-golden-thread-report#golden-thread-definition) and Jonathan Smart's "golden thread" in *[Sooner Safer Happier](https://www.soonersaferhappier.com/)*. |
> | **mark** / **`@covers`** | Leave a mark when you touch the work: a one-line comment in source naming the durable ID(s) that code serves. Greppable; author-written; Gate reads it; Loupe shows it under Build. The lineage is the maker's mark, struck by the maker before the assay office tests; the hallmark belongs to the trace-manifest. |
> | **`Carries:`**           | Mark on a task checkbox naming the ID(s) that task carries — usually open debt or anointed backlog. |
> | **Gate 2**               | Deterministic SpecAssay check + manifest emit (`speckit.specassay-check.gate`). The mechanism that judges the Golden Thread; say "Gate" when you mean this script, "Golden Thread" when you mean what the human sees. Local runs are hygiene; **CI Gate is the property line** that protects the thread. |

## Lineage (name prior art first)

- Business and programme "golden thread" usage; Jonathan Smart, *Sooner Safer Happier*
- The UK golden thread of building-safety information (Hackitt review; Building Safety Act 2022)
- Safety-critical requirements traceability matrices (avionics, medical, rail practice)
- [GitHub Spec Kit](https://github.com/github/spec-kit) (the stock SDD workflow SpecAssay overlays)
- Thorsten Schlathölter, [CAS-DD and open-source `clew`](https://ariadne-thread.io) (inner-loop, code-anchored specs); complementary altitude to SpecAssay's promotion and refusal focus
