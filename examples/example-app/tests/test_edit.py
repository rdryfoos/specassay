"""Behavioral test for inline edit's commit-on-blur half of FR-EDIT-01.

This test is deliberately NOT named after the undo AC: undo (AC-EDIT-01) is
anointed backlog and has no proof yet. The first Practice exercise is to add a
proof named for that AC (plus a matching source mark) and watch the status flip
to proven. (The proof/mark tokens are intentionally left out of this file so the
Gate does not count them prematurely.)
"""

from src.edit import InlineEditor


def test_commit_on_blur_sets_value():
    ed = InlineEditor("old")
    ed.type("new")
    assert ed.value == "old"  # not committed until blur
    assert ed.blur() == "new"
    assert ed.value == "new"
