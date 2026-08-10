# Tasks — Cross-device Sync

Every checkbox task carries its registry ID(s) via a **Carries** mark (Gate 2
requires it). Open `- [ ]` tasks that carry an AC are *tracked debt*; the AC is
excused from the silent-gap check while the TODO stays open.

## Completed

- [x] T001 Reconcile queued ops on reconnect and fan the merged log out — **Carries**: FR-SYNC-01, AC-SYNC-01
- [x] T002 Queue edits locally while offline and apply them optimistically — **Carries**: AC-OFFL-01
- [x] T013 Keyboard reachability + assistive-tech announcements for list actions — **Carries**: AC-A11Y-01

## Tracked debt

- [ ] T005 Field-level merge test for disjoint edits — **Carries**: AC-SYNC-02 — deferred to the sync milestone

## Planning altitude (backlog — referenced so the registry set stays closed)

- US-SYNC-01 parent story (decomposed into the tasks above)
- NFR-PERF-01 virtualized 1,000-item render at 60fps — not yet scheduled
