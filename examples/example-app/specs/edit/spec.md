# Feature Spec — Inline Edit

Inherits registry IDs from `PRD.md`.

> Note: **the undo acceptance criterion is intentionally absent from this
> spec.** It is *anointed backlog* — minted in the registry and carried only by
> an open TODO in `specs/backlog/tasks.md`. A learner picks it up end-to-end
> (see the "Practice" section of the README). Even naming its ID here would pull
> it out of the backlog altitude, so this spec deliberately does not.

## Story

- US-EDIT-01 — As a user, I can edit a list item inline.

## Behavior

- FR-EDIT-01 — Inline edit commits on blur and is undoable. The commit-on-blur
  half is implemented (`src/edit.py`); the undo half is the anointed backlog
  work item (its AC is carried only by the open TODO in `specs/backlog/`).
