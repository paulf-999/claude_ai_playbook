"""Adds the jira_create skill directory to sys.path.

jira_create_handler.py lives with the skill, not under _tests/,
so these tests' bare `from jira_create_handler import ...` needs
an explicit sys.path entry rather than relying on same-directory imports.
"""

import sys

from _shared_paths import CLAUDE_DIR

_SKILL_DIR = CLAUDE_DIR / "skills" / "_atlassian_skills" / "jira_create"
if str(_SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILL_DIR))
