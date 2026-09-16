"""Shared Claude config directory resolution for the test suite.

Single source of truth for locating the Claude config directory under
test. Override via CLAUDE_CONFIG_DIR (e.g. CI points this at the repo's
own src/claude/ instead of a real ~/.claude install).
"""
import os
from pathlib import Path

CLAUDE_DIR = Path(os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude")))
