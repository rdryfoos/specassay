# Archaeology Mode — Drawer Brief, 2026-08-20

Design-room document, not a build handoff. Captures the concept fully so it can be commissioned when sequencing allows. Origin: the 2026-08-20 competitive scan (unified-viewer vision brief §8), where the synthesis emerged that the competitors' inference architecture is not a threat to answer but an onboarding feature to absorb. Rulings proposed here need Rik's ratification before any row mints.

## The one-paragraph shape

An ungoverned repo opens in the viewer as an empty field, and that emptiness is the product's adoption threshold: govern from day one or see nothing. Archaeology mode digs instead. Inference over what already exists (structure, tests, commits, docs) proposes a DRAFT registry: statements of intent the repo appears to embody, rendered as ghost threads in the same familiar field. Every proposed row is born marked inferred, never attested; the Gate never reads it as governed; statuses stay honest-gray until a human anoints, amends, or rejects each one. Inference bootstraps; governance takes over; the two are never conflated. The pitch collapses from "adopt a methodology" to "see your product as-built in twenty minutes, unsigned, then start signing it."

## The problem it solves

1. Cold start (vision brief §7, condition 1): the killer-app coupling is only killer above the adoption threshold, and today the threshold is a founded registry. Archaeology mode is the direct answer.
2. The stranger's-repo demo (falsifiable test T-b): the briefing-on-their-own-PR moment currently requires the stranger to have governed something. With a dig, the demo runs on any repo: their map renders gray, and gray is visceral. Nobody feels the absence of proof until they see their own product rendered honestly unsigned.
3. Migration: every existing codebase on earth is ungoverned by this methodology. The dig is the on-ramp from all of them.

## The core law: inferred versus attested, never conflated

This is the brief's spine and the part that must survive every design iteration:

- Every dug row carries epistemic class INFERRED, permanently visible, with per-row provenance (which files, tests, commits, or docs suggested it).
- The Gate does not read inferred rows. No inferred row can be proven, carry debt, or gate anything. Statuses derive only after anointment, from evidence, per Rule 6a, exactly as for any born-governed row.
- The viewer renders inferred threads in the family's existing epistemic grammar: texture equals epistemic class. Ghost strands: reduced opacity, distinct texture, no status hues anywhere on them. A dug field looks like what it is, a proposal.
- Anointment is the only crossing. Anoint (mint the real ID, dated, coverage basis stated as recovered-not-newly-attributed), amend-then-anoint, or reject. Rejections are recorded in the dig report, never deleted: annotate, never erase.
- No silent promotion, ever. No batch auto-anoint. Speed comes from good review ergonomics, not from removing the human.

## How the dig works (proposed pipeline)

1. Sources, roughly in order of signal quality: existing test names and bodies (a test suite is a latent registry: test names often state criteria verbatim); README and docs; API routes and CLI surfaces; module and directory structure; commit message history (stratigraphy: what themes recur, what changed together).
2. Synthesis: LLM-assisted drafting of candidate US/FR/AC rows in the registry's own grammar, each citing its provenance. Statements must quote or point at the evidence that suggested them; a row with no citable provenance does not get proposed.
3. Output: a dig report (draft-registry artifact) living BESIDE the real registry, never inside it. The viewer loads it as a ghost layer.
4. Candidate proofs: where an existing passing test plausibly answers a proposed criterion, the dig records a candidate binding. On anointment, the candidate becomes a suggested @covers mark for the human or build process to strike; it is never struck automatically, and status still derives only from actual runs.

## The anointment room (workflow sketch)

The review surface is the field itself: ghost strands, click to read the proposed row with its provenance inline, one gesture each for anoint / amend / reject, running tally of the dig's disposition. Small batches by area, not one heroic session. The ceremony matters: anointment is the moment a guess becomes a commitment, and the UI should make that weight felt without making it slow.

## Honest risks

1. Gilt, inverted: a confident wrong draft registry is worse than an empty field, because plausible-looking rows get rubber-stamped. Mitigations: provenance rendered on every row, statements that must cite evidence, small-batch review, and the ghost rendering itself (nothing looks settled).
2. Anchoring: the dig's framing becomes the team's framing even where the team would have framed better. Mitigation: amend-then-anoint as a first-class equal gesture, not a buried edit.
3. Privacy posture: LLM inference over repo content raises the NFR-SPOOL-20 question in new clothing. If inference calls an external API, that is repo content leaving the machine and requires explicit consent; a local-model path should be evaluated. This is a ruling, not a default.
4. Overpromise: "see your map in twenty minutes" must mean a ghost map. Marketing that blurs inferred into attested would spend the exact trust the product exists to create.

## What this is NOT

Not auto-governance. Not a spec generator that writes truth. Not a replacement for founding a registry on a greenfield repo (born-governed remains the paved road). Not a competitor feature copied: the competitors stop at the guess; this system is the only one with somewhere attested for the guess to go.

## Open questions — ANSWERED, ratified by Rik 2026-08-20

1. Name — RULED: "the dig" for the command (specassay dig), "archaeology mode" in prose.
2. Placement — RULED: the dig is open-source and necessarily a command (it writes; the viewer never writes), producing a dig-report file the viewer renders as the ghost layer. The paid line stays where the collapse ruling drew it: structure free, cost illumination (SpecCost) paid. Two ratified consequences: (a) guided excavation is a Dryfoos Consulting service offering — tool free, facilitation billable; (b) ANOINTMENT SHIPS AS A PR — the anointment room's output is a generated pull request of selected/amended rows, signed in the forge, refused by the Gate until signed. The onboarding ritual IS the PR-for-Intent ritual: the dig teaches the §7 coupling on day one.
3. LLM path — RULED: federation and inference are unrelated (federation is artifact exchange between sovereign machines; no LLM, no third party, transport can be git). The dig's synthesis ships as a three-rung ladder, defaulting to the most private engine available: (a) no-LLM floor, static heuristics led by test-name parsing (a test suite is a latent registry); (b) local model, nothing leaves the machine; (c) user-supplied API key — their provider, their agreement, explicit path preview, hard scrub of secrets/env before anything crosses. Dryfoos infrastructure never touches repo content; the dig is a tool, not a service.
4. Dig report home and schema — RULED: builder discretion at commission time.
5. Sequencing — RULED as leaned: after the quickstart proves the governed path; star of the first external demo cycle. Not before.

## Standing citations

Texture equals epistemic class · Rule 6a (status derives, never declared) · annotate never erase · coverage basis stated at mint · NFR-SPOOL-20 (nothing leaves the machine without consent) · the em-dash law's spirit (absence of attestation renders as absence, never as a lighter shade of yes) · purpose clause (no dark patterns: the ghost map is honest about being a guess).
