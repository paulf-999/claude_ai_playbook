"""Adds the confluence_create_page skill directory to sys.path.

confluence_create_page_handler.py lives with the skill, not under _tests/,
so these tests' bare `from confluence_create_page_handler import ...` needs
an explicit sys.path entry rather than relying on same-directory imports.
"""

import sys

from _claude_dir import CLAUDE_DIR

_SKILL_DIR = CLAUDE_DIR / "skills" / "_atlassian_skills" / "confluence_create_page"
if str(_SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILL_DIR))
