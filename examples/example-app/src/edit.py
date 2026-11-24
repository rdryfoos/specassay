"""Inline edit for list items.

FR-EDIT-01: inline edit commits on blur and is undoable. Both halves are
implemented here: the draft commits on blur, and one call to undo() puts the
last committed value back.
"""


class InlineEditor:
    """A one-field inline editor: type into a draft, commit on blur."""

    def __init__(self, value=""):
        self.value = value
        self._draft = value
        self._prior = None   # the value before the last commit, if there was one

    def type(self, text):
        """Update the in-progress draft without committing."""
        self._draft = text
        return self._draft

    def blur(self):
        """Commit the draft to the committed value (commit-on-blur)."""
        self._prior = self.value
        self.value = self._draft
        return self.value

    # @covers AC-EDIT-01 — one call puts the last committed value back, and
    # takes any uncommitted draft with it, so undo cannot leave a half-typed
    # edit behind to be committed by the next blur.
    def undo(self):
        """Restore the last committed value, discarding any draft.

        Returns the restored value. With nothing committed yet there is nothing
        to go back to, so the value is left alone and the draft is still reset:
        undo always leaves the editor showing what it has committed.
        """
        if self._prior is not None:
            self.value = self._prior
            self._prior = None
        self._draft = self.value
        return self.value
