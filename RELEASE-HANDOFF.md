# SpecAssay community release — handoff from the design room

Date: 2026-08-18. You are the **release room**: one mission, ship the
next public SpecAssay bundle to the GitHub community, then this room
archives. You are not a production line — SpecCost, Tally, and Loupe
each have their own rooms and none of their repos are yours to touch.
This repo — the real `specassay` — is where you work.

## Read first, in this order

1. `CHANGELOG.md` — the whole 0.4.x line. The versioning law is
   recorded in its own entries and is binding: all three components
   (bundle, extension `specassay-check`, preset `specassay`) share the
   bundle's version and move together; the release tag matches the
   preset's version; anything shipped *inside* an artifact can only be
   fixed by a real release, never a docs push.
2. `PROMOTION-CONTRACT.md` — the law the bundle enforces.
3. The survey: `docs/field-notes/2026-08-17-uncovered-proof.md` in the
   `dryfoos-sites` repo (github.com/rdryfoos/dryfoos-sites) — the
   five-project uncovered-proof numbers, the vendored-copy lag
   measurements, and the adopter-upgrade frictions. This is the
   release's evidence base and its best story.
4. This repo's own release-mechanics notes wherever the previous
   releases recorded them — follow the mechanics the repo documents,
   not memory.

## The story this release tells

The last public line stopped at 0.3.x. Since then the bundle grew its
first **omission-side check**: `uncovered-proof` (v0.4.7) — a real,
tested, proven ID absent from every `@covers` line is now a named
finding — and its opt-in hard-fail `block_uncovered_proof` (v0.4.8).
The headline is honest and strong: *the Gate always caught false
claims; now it also catches true work nobody declared — and when we
ran it on our own five projects it found 34 instances, including two
in our own reference app.* Lead with that. The 0.4.10 paved roads
(pre-written `@covers` lines in task templates, the warn-only
commit-advisory hook, the mint-time coverage reminder) are the
supporting cast: the check finds the debt, the paved roads stop it
accruing.

## Musts, each with its check (constitution style — no unnamed vows)

1. **The reference app models the law.** Both example-app
   uncovered-proof findings (`AC-A11Y-01`, `AC-OFFL-01`) are fixed in
   this release. Check: a Gate run on the shipped example-app reports
   zero uncovered-proof diagnostics, output attached to the release
   evidence.
2. **Report-only is the shipped default; blocking is earned.** The
   design-room ruling (2026-08-18): `uncovered-proof` ships as a
   diagnostic; `block_uncovered_proof` is documented as a per-project
   ratchet — clear your backlog, then flip, never a global flag day,
   never reversed. Check: config template default + a README section
   stating the ratchet in exactly these terms.
3. **Cold-install proof, attached.** A fresh scratch repo, the README
   followed verbatim, ending in a real Gate run and a real emitted
   trace-manifest. The transcript and the manifest ship with the
   release notes. Never hand-author a sample artifact — every shipped
   sample comes out of the real tool.
4. **The migration guide is part of the release.** Existing adopters
   carry vendored copies measured 0–3 releases behind, and the upgrade
   frictions are known and documented in the survey (presets have no
   update command; pinned-tag catalogs can mask new versions; the
   local catalog cache has no documented refresh). Write the upgrade
   path for a 0.3.x or 0.4.x adopter honestly: what works, the
   workaround where it doesn't, no gilding. Check: the guide names
   each measured friction and its current answer.
5. **Changelog from history, not memory.** The community-facing notes
   are written from `CHANGELOG.md` and the actual commits. Check:
   every release-note claim traces to a changelog entry or commit.
6. **Version and tag discipline** per the recorded law (components
   move together; tag matches). Check: the repo's own release
   verification steps, run, output kept.
7. **Shipped docs meet the taught-by bar** (family standard,
   2026-08-19 — see `docs/field-notes/2026-08-19-taught-by-standard.md`
   in `dryfoos-sites`): every troubleshooting/how-to entry cites the
   real incident that taught it; visual symptoms carry real,
   self-dating screenshots of the actual tool on real data (never
   mockups); pointer files are plumbing, never the answer to a
   question. Check: each shipped doc entry has its "Taught by:" line,
   and each visually-manifesting entry has its capture.

## The wall

Before anything public goes live: hand the release candidate across —
a draft release (or RC branch) plus the evidence from musts 1, 3, and
6. The design room verifies independently, including its own cold
install in a separate environment — the second honest lens is standing
family practice, and a release is exactly the artifact that deserves
one. The tag goes public after that verification, not before. The
owner (Rik) confirms the exact community submission venue at that
checkpoint; the prior submission's channel is the default assumption.

## Boundaries

- **Yours**: this repo — code only as release polish requires (the
  example-app fixes are in scope; new checks and features are not),
  docs, packaging, evidence.
- **Not yours**: SpecCost's 30-instance backlog cleanup (its own
  room's work, on its own clock — the ratchet ruling means the
  release does not wait for it); the other product repos; the family
  canon; anything that adds registry-governed behavior mid-release.
- Found a real defect while packaging? Fix-and-release is allowed if
  it is release-blocking; otherwise record it and ship. Say which you
  did and why in the notes.

## Working agreement

Same as every room: verified artifacts cross the wall, say-so doesn't.
When something in this handoff conflicts with what the repo actually
contains, the repo is the evidence — flag the conflict with receipts
and a proposed correction rather than silently working around it.
