"""The proof the criterion is read by name, and a real passing test."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from walk import speak_turn  # noqa: E402


def test_AC_WALK_01_speaks_the_turn_once():
    assert speak_turn(50, "turn left") == "In 50 metres, turn left."
    assert speak_turn(120, "turn left") is None
