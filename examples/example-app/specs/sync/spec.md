# Feature Spec — Cross-device Sync

Inherits registry IDs from `PRD.md`. This spec references (does not re-mint) the
durable IDs it delivers, so the exact-set rule holds.

## Story

- US-SYNC-01 — As a user, I keep my lists in sync across devices.

## Behavior

- FR-SYNC-01 — Two-way sync reconciles list changes across devices. Each device
  keeps a local op queue; a central hub receives queued ops on reconnect and
  fans the merged log back out to every device.

## Acceptance criteria

- AC-SYNC-01 — A change made offline appears on a second device within 5s of
  reconnect. Reconciliation is timestamp-ordered and runs on the reconnect edge.
- AC-SYNC-02 — Disjoint field edits on two devices merge without conflict.
  Field-level merge keeps both edits; same-field collisions are last-write-wins.
- AC-OFFL-01 — The app is fully usable with no network; edits queue locally and
  apply optimistically until the next reconcile.

## Cross-cutting (referenced here so the registry set stays closed)

- NFR-PERF-01 — List view renders 1,000 items at 60fps on a mid-range device.
- AC-A11Y-01 — All list actions are reachable by keyboard and announced to
  assistive tech.
