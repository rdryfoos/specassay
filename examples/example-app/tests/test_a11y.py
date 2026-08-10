"""Proof for AC-A11Y-01: every list action is reachable by keyboard and
announced to assistive tech.
"""

import pytest

from src.a11y import ACTIONS, KEYMAP, ListView


def test_AC_A11Y_01_keyboard_reachable_and_announced():
    view = ListView()

    # Every declared action is reachable by some key.
    assert view.reachable_actions() == set(ACTIONS)

    # Invoking each key dispatches the action and announces it.
    for key, action in KEYMAP.items():
        assert view.invoke_by_key(key) == action

    announced = {msg.split(" ", 1)[0] for msg in view.announcements}
    assert announced == set(ACTIONS)

    # Unknown keys do not silently no-op.
    with pytest.raises(KeyError):
        view.invoke_by_key("Q")
