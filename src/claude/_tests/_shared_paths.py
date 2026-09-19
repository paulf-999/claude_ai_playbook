"""Shared Claude config path constants for the test suite.

Single source of truth for locating the Claude config directory under
test, plus the handful of path constants that were independently
redeclared with identical values across multiple test files. Override
CLAUDE_DIR via CLAUDE_CONFIG_DIR (e.g. CI points this at the repo's own
src/claude/ instead of a real ~/.claude install).

Test-specific paths used by only one test file (e.g. a single rule's
file path) stay declared locally in that file — centralizing them here
would add indirection without removing any duplication.
"""
import os
from pathlib import Path

CLAUDE_DIR = Path(os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude")))

CLAUDE_MD = CLAUDE_DIR / "CLAUDE.md"
ALIASES_FILE = CLAUDE_DIR / "aliases.md"
SETTINGS_FILE = CLAUDE_DIR / "settings.json"
SKILLS_DIR = CLAUDE_DIR / "skills"
HOOKS_DIR = CLAUDE_DIR / "hooks"
RULES_DIR = CLAUDE_DIR / "_rules"
