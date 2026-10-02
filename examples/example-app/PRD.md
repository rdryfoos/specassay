# Collaborative Lists — Product Requirements (ID Registry)

This PRD is the **authoritative ID registry** for the example app. Every durable
intent gets a stable ID here; specs, tasks, source `@covers` marks, and
`test_AC_*` proofs all trace back to these IDs. SpecAssay Gate 2 enforces the
exact-set rule: the IDs defined here must equal the IDs referenced in `specs/`
and `tasks.md` (the one exception is *anointed backlog* — an ID carried only by
an open `- [ ] … **Carries**:` TODO).

## Sync

- US-SYNC-01 — As a user, I keep my lists in sync across devices.
- FR-SYNC-01 — Two-way sync reconciles list changes across devices.
- AC-SYNC-01 — A change made offline appears on a second device within 3s of reconnect.
- AC-SYNC-02 — Disjoint field edits on two devices merge without conflict.
- AC-OFFL-01 — The app is fully usable with no network; edits queue locally.

## Inline edit

- US-EDIT-01 — As a user, I can edit a list item inline.
- FR-EDIT-01 — Inline edit commits on blur and is undoable.
- AC-EDIT-01 — Undo restores the prior value within one step after an inline edit.

## Cross-cutting

- NFR-PERF-01 — List view renders 1,000 items at 60fps on a mid-range device.
- AC-A11Y-01 — All list actions are reachable by keyboard and announced to assistive tech.
