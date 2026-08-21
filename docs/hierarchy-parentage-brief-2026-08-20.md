# Hierarchy & Parentage Edges — Drawer Brief, 2026-08-20

Design-room document, not a build handoff. This is the item previously flagged 3+ times and never commissioned — this session finally supplies its concrete demonstration and its acceptance criterion. Rulings here need ratification before minting.

## The demonstration that forced this

Live comparison, same repo, two surfaces: StoriesOnBoard's story map shows US-BIND-10 as a parent card with FR-BIND-10, FR-BIND-20, AC-BIND-10 nested beneath it — a real, readable composition. Loupe's descent on the sibling row US-UNBIND-10 shows INTENT → BUILD → PROOF and dead-ends at "No proof" — technically correct (US rows carry no direct test by design, per the FR-LEDGER-40 finding) and practically a lie by omission: real proof exists three levels down, on AC-UNBIND-10/20/30, and the descent has no way to reach it. Rik's own words, elevated to the acceptance criterion for this brief: "if I can't find code and test from intent, then this whole system does not really help me."

## The actual gap, precisely

Two different relationships are currently conflated:

- COVERAGE (real, built, many-to-many, build-artifact-to-spec): "also covers" — one file can cover several sibling IDs. Horizontal axis.
- COMPOSITION (absent from the data model, spec-to-spec): "US-BIND-10 decomposes into FR-BIND-10, AC-BIND-10." Vertical axis. Currently exists ONLY as an inference the story map draws from PRD document nesting order — never as a field in trace-manifest.json. Loupe cannot walk what the data doesn't contain.

## Why it's genuinely hard, not just unbuilt (Rik's point 2, confirmed)

Spec structure varies across projects: not every repo nests a clean US→FR→AC three tier; orphan FRs with no parent US are legitimate; nesting depth isn't uniform; this repo's PRD-ordering convention is a local habit, not a portable rule. Any fix has to be an OPTIONAL, EXPLICIT, gracefully-degrading contract — never an assumed structure, never an invented edge. Same em-dash law as everywhere else: absence of a declared parent renders as absence, not as a guess.

## Proposed shape

1. Schema: an optional `parent` field on a registry row, pointing at another ID. Populated at mint time IF the source document expresses it (e.g., PRD nesting) or left absent otherwise — never inferred after the fact by the viewer, never guessed from naming convention alone (ID prefixes are not a reliable parent signal across projects).
2. A new descent card type, COMPOSITION, rendered when a row has children: lists them with a rolled-up status summary (X proven / Y debt / Z backlog / W GAP among descendants), each child one click to its own descent. Replaces a bare "No proof" dead-end for parent-shaped rows.
3. Leaf rows (typically AC-type, no children) render exactly as today — INTENT/BUILD/PROOF unchanged. This is additive, not a replacement of the existing descent.
4. Stretch, not core: the thread field could eventually nest child strands under a parent strand visually — deferred, the descent-level fix is the one that actually answers Rik's acceptance criterion.

## Resolution on population (added 2026-08-20, late — supersedes "Proposed shape" item 1)

Rik's instinct, ratified in discussion: instructions in Spec Kit would be legislation without a gate, and a separately-authored `parent:` field would be a second source of truth that can drift from the document's actual structure. The right mechanism is the family's own deepest rule — DERIVE, never declare:

- The Gate derives parent edges at EMIT time from the registry document's own structure (heading/section nesting) — the same move as status deriving from evidence. The manifest carries the edge with provenance: parent + derivation method. Deterministic, regenerated every run, cannot drift from the document because it IS the document.
- Per-project variation handled by config, not assumption: specassay-check-config.yml names the convention (e.g. parent_derivation: heading-nesting | none). Flat specs emit no edges; absence renders as absence, em-dash law.
- Spec Kit's role is the paved road, not instructions: templates whose natural output nests correctly make the honest path the shortest path. No compliance asked of anyone.
- This resolves open question 1 (derivation, not authoring or dig-style proposal) and question 2 (document structure yields a tree by construction — single-parent v1 for free; DAG deferred until a real cross-cutting case demands it).

## Open questions for ruling

1. Is `parent` populated only via explicit per-project authoring, or can mint tooling propose it from PRD structure with the human confirming (dig-adjacent pattern from the archaeology-mode brief — worth checking these two briefs for shared machinery when both are eventually built).
2. Multiple parents (an FR serving two USs) — allow, and if so does roll-up double-count, or is composition strictly single-parent (a tree, not a DAG)?
3. Does composition depth stop at declared edges, or does the roll-up recurse arbitrarily deep?
4. Sequencing: this is real UI/schema build work, not a quick rendering fix like the PROOF-card branch. Where does it sit against T905/T906/T907, T914, and everything else currently queued?

## Standing citation

Em-dash law (absence renders as absence, never invented) — the same discipline that governs every other field in this family now governs the one relationship it never had.
