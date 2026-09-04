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
   **Done** (already, commit `280a079`; reverified 2026-08-18 by the
   docs room: `examples/example-app`'s Gate run, `gate.diagnostics: []`).
2. **Report-only is the shipped default; blocking is earned.** The
   design-room ruling (2026-08-18): `uncovered-proof` ships as a
   diagnostic; `block_uncovered_proof` is documented as a per-project
   ratchet — clear your backlog, then flip, never a global flag day,
   never reversed. Check: config template default + a README section
   stating the ratchet in exactly these terms.
   **Done** 2026-08-19: `config-template.yml`'s `block_uncovered_proof`
   ships commented out (verified); README's new "Uncovered proof:
   report-only is the shipped default; blocking is earned" section
   states the ratchet in these terms.
3. **Cold-install proof, attached.** A fresh scratch repo, the README
   followed verbatim, ending in a real Gate run and a real emitted
   trace-manifest. The transcript and the manifest ship with the
   release notes. Never hand-author a sample artifact — every shipped
   sample comes out of the real tool.
   **Done** 2026-08-19, and then some: a real cold-agent trial (not
   just a scratch repo the docs room drove itself), independently
   reverified command-by-command — `docs/testing/completed/
   evidence-cold-agent-trial-observed-2026-08-19.md`, manifest at
   `samples/cold-trial-imei.trace-manifest.json`.
4. **The migration guide is part of the release.** Existing adopters
   carry vendored copies measured 0–3 releases behind, and the upgrade
   frictions are known and documented in the survey (presets have no
   update command; pinned-tag catalogs can mask new versions; the
   local catalog cache has no documented refresh). Write the upgrade
   path for a 0.3.x or 0.4.x adopter honestly: what works, the
   workaround where it doesn't, no gilding. Check: the guide names
   each measured friction and its current answer.
   **Done** 2026-08-19: `docs/migration.md`. All three frictions
   reverified directly against the real CLI (0.15.3.dev0), not carried
   over from the survey unchecked — the cache-refresh one turned out
   more stubborn than described (a full `preset remove`+`add` cycle
   still didn't bust it; only deleting `.cache/` did), and the guide
   says so.
5. **Changelog from history, not memory.** The community-facing notes
   are written from `CHANGELOG.md` and the actual commits. Check:
   every release-note claim traces to a changelog entry or commit.
6. **Version and tag discipline** per the recorded law (components
   move together; tag matches). Check: the repo's own release
   verification steps, run, output kept.
   **Not started.** Before running `scripts/build-release.sh`, read
   `docs/submission/CHEATSHEET.md`'s "Updating to a new version"
   section — it carries real scars from the last submission (2026-08-13
   – 08-14), not generic advice, and it was just updated 2026-08-19 to
   name a gap it previously only recorded as history: grep
   `presets/specassay/README.md` and `extensions/specassay-check/
   README.md` for stale version strings too, not just the manifests
   and catalogs — that's specifically what got missed for two version
   bumps running last time. `scripts/build-release.sh`'s own header
   comment was found stale in the same pass (it argued for independent
   per-component versions, a policy round 2 explicitly reversed) and
   has been corrected.
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

**Deviation, recorded 2026-08-20 (design-room ruling, not relitigated):**
`v0.4.12` was tagged and published before the design room's independent
verification ran — the wall's ordering was not followed. Exposure is
judged ~zero: the tag was never announced and nothing public links to
it. Remedy is a freeze, not a re-cut: nothing files to `spec-kit` and
nothing on the live site links to the `v0.4.12` release until the wall
actually passes (the design room's own cold install, in its own
environment, against the published assets, verified against the
release digests).

**Wall passed, 2026-08-20.** Design room's independent verification: a
Linux container (Python 3.12.3), network path and tooling fully
disjoint from the Mac trial. All three release assets downloaded
directly and hashed — byte-identical to the Mac run's digests and to
GitHub's own API, three-way agreement. Fresh cold install via the
documented `https --from` path installed and enabled cleanly. The Gate,
run cold on the untouched project: honest loud `FAIL: registry not
found: PRD.md`, nonzero exit, `trace-manifest.json` still written (0
rows, `gate.ok=false`, `executionVerified=false`) — matching the Mac
evidence exactly, on a second OS. Freeze lifts. Four non-blocking
findings logged to `docs/docs-gaps.md` (open): real CLI version skew
between the two trials' `specify` versions, `--from`'s https-only
restriction, the "20 minutes" claim not accounting for interactive
prompts/first-fetch latency, and confirmation that the v4/v5beta dual
emit is intentional (documented since the 0.4.5 changelog entry).

**Done, 2026-08-20:** `specassay.com`'s hero install CTA now points at
`github.com/rdryfoos/specassay/blob/v0.4.12/README.md#install-catalog-path`
(`dryfoos-sites` commit `5a0d718`) — pinned to the exact tag the wall
just verified, not the unpinned `main`-tracking anchor it used before.

**v0.4.13, 2026-09-04: same deviation, on commission.** The tag was cut
before any independent verification because a real outside tester was
waiting on the cold-install fixes it carries. This room's own
verification is attached (`docs/submission/test-evidence.md`: digests
three ways, in-zip checks, fresh catalog install, and a real v0.4.12 to
v0.4.13 upgrade). The design room's separate-environment pass is still
owed and nothing is filed to `spec-kit` until it runs.

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
