"""Make `src` importable as a package when running `python -m pytest` from
the example-app directory (or from the repo root via the documented command).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
