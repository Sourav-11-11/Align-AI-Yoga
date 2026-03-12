"""
conftest.py — auto-loaded by pytest before any test collection.

Adds the project root (FRONT END/) to sys.path so that both
  `import ml.*` and `import app.*` work from any test file without
  needing per-file sys.path manipulation.
"""

import sys
import os

# Insert FRONT END/ (the directory containing this file) at the front.
ROOT = os.path.dirname(__file__)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
