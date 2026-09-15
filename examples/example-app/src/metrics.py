"""Lightweight in-process event counters.

Incidental plumbing — counts a few sync/edit events for local debugging. It
serves no acceptance criterion on its own (no `@covers`), so the Thread Report
will list it as "far from the thread." That's the point of including it here:
a real PR usually carries some scaffolding that touches no intent, and SpecAssay
should surface it for a glance rather than pretend it isn't there.
"""

from collections import Counter

_counts: Counter = Counter()


def bump(event: str, n: int = 1) -> None:
    """Increment a named counter."""
    _counts[event] += n


def snapshot() -> dict:
    """Return a copy of the current counts."""
    return dict(_counts)


def reset() -> None:
    _counts.clear()
