"""Make `src` importable as a package when running `python -m pytest` from
the example-app directory (or from the repo root via the documented command).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from src.edit import InlineEditor


@pytest.fixture
def editor():
    """An editor with one committed value, which is what undo goes back to."""
    return InlineEditor("old")
