"""Shared pytest setup: puts the _tests/ folder on sys.path so tests can import helpers like _shared_paths."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
