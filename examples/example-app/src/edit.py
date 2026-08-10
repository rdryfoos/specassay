"""Inline edit for list items.

FR-EDIT-01: inline edit commits on blur and is undoable. The commit-on-blur half
is implemented here. The *undo* half is intentionally left as anointed-backlog
practice work — see specs/backlog/tasks.md (T900) and the "Practice" section of
the README. This file deliberately carries no coverage mark and no test for the
undo criterion yet (its ID is left unwritten here on purpose).
"""


class InlineEditor:
    """A one-field inline editor: type into a draft, commit on blur."""

    def __init__(self, value=""):
        self.value = value
        self._draft = value

    def type(self, text):
        """Update the in-progress draft without committing."""
        self._draft = text
        return self._draft

    def blur(self):
        """Commit the draft to the committed value (commit-on-blur)."""
        self.value = self._draft
        return self.value

    # TODO(T900): undo() — restore the prior committed value within one step.
    # This is anointed-backlog practice work; add the coverage mark and proof
    # when you implement it (the undo AC's ID is left unwritten here on purpose).
