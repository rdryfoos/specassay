"""Behavioral tests for inline edit: commit-on-blur, and undo.

The undo test is named for the criterion it answers, which is how the Gate
knows which test stands for which promise. Before this change undo was
anointed backlog, minted and carried by an open TODO with nothing built.
"""

from src.edit import InlineEditor


def test_commit_on_blur_sets_value():
    ed = InlineEditor("old")
    ed.type("new")
    assert ed.value == "old"  # not committed until blur
    assert ed.blur() == "new"
    assert ed.value == "new"


def test_AC_EDIT_01_undo_restores_prior_value(editor):
    editor.type("new")
    editor.blur()
    assert editor.value == "new"
    assert editor.undo() == "old"
    assert editor.value == "old"


def test_AC_EDIT_01_undo_discards_an_uncommitted_draft(editor):
    """The half the restatement is about: a draft must not survive the undo.

    Without this, undo would put the old value back on screen and the next
    blur would commit the draft the user had just undone.
    """
    editor.type("new")
    editor.blur()
    editor.type("half-typed")
    assert editor.undo() == "old"
    assert editor.blur() == "old"


def test_undo_with_nothing_committed_leaves_the_value_alone(editor):
    assert editor.undo() == "old"
    assert editor.value == "old"
