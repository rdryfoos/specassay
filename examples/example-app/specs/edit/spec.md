# Feature Spec — Inline Edit

Inherits registry IDs from `PRD.md`.

> Note: **the undo acceptance criterion was anointed backlog until this
> change.** It was minted in the registry and carried only by an open TODO in
> `specs/backlog/tasks.md`; naming it here is what pulls it out of the backlog
> altitude, which is the last step of picking it up (see the "Practice" section
> of the README).

## Story

- US-EDIT-01 — As a user, I can edit a list item inline.

## Behavior

- FR-EDIT-01 — Inline edit commits on blur and is undoable. Both halves are
  implemented in `src/edit.py`.
- AC-EDIT-01 — Undo restores the last committed value in one call, and discards
  any uncommitted draft with it.
