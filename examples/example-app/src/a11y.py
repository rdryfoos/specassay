# @covers AC-A11Y-01
"""Accessibility surface for list actions.

All list actions are reachable by keyboard and announced to assistive
tech. Modeled here as a keyboard map covering every action plus a
live-region announcement channel.
"""

ACTIONS = ("add", "edit", "delete", "toggle", "reorder")

KEYMAP = {
    "a": "add",
    "e": "edit",
    "Delete": "delete",
    " ": "toggle",
    "Control+ArrowUp": "reorder",
}


class ListView:
    """A minimal list view with keyboard dispatch and an announcement log."""

    def __init__(self):
        self.announcements = []  # stands in for an aria-live region

    def reachable_actions(self):
        """Actions reachable by keyboard (values of the key map)."""
        return set(KEYMAP.values())

    def invoke_by_key(self, key):
        """Dispatch a keypress to its action and announce it. Raises on unknown key."""
        action = KEYMAP.get(key)
        if action is None:
            raise KeyError(key)
        self.announce(action)
        return action

    def announce(self, action):
        """Push a message to the live region so assistive tech reads it out."""
        self.announcements.append(f"{action} performed")
        return self.announcements[-1]
