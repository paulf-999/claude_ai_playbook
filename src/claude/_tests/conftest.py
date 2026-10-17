"""Shared pytest setup: puts _tests/ and _tests/_helpers/ on sys.path so tests can import helpers like _shared_paths."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "_helpers"))
