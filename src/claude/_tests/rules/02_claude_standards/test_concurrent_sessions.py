# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-21
# Date updated:      2026-10-28
# Version:           3.0.1
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests for git/_concurrent_sessions.md: it stays reachable and keeps its incident record.

The rule's guidance is instructional and free to change, so its wording isn't pinned.
The 2026-09-21 concurrent-session incident is the exception: ``testing.md`` allows a
content-regression check for an incident record, tagged ``# wording-check:``.
"""
from _shared_paths import CLAUDE_DIR

RULE_FILE = CLAUDE_DIR / "rules" / "02_claude_standards" / "git" / "_concurrent_sessions.md"
GIT_MD = CLAUDE_DIR / "rules" / "02_claude_standards" / "git.md"


def test_concurrent_sessions_imported_from_git_md():
    """git.md must point to _concurrent_sessions.md, or it's unreachable."""
    content = GIT_MD.read_text()
    assert "_concurrent_sessions.md" in content, (
        "git.md does not point to _concurrent_sessions.md — rule is orphaned"
    )


def test_concurrent_sessions_has_purpose_statement():
    """File must open with a Purpose statement, per writing_style.md."""
    content = RULE_FILE.read_text()
    assert "**Purpose:**" in content, "_concurrent_sessions.md missing a Purpose statement"


def test_concurrent_sessions_documents_real_incident():
    """The real 2026-09-21 incident must stay documented, not just the abstract rule."""
    content = RULE_FILE.read_text()
    assert "2026-09-21" in content, "Incident date missing"  # wording-check: incident record
    assert "confluence_create_page_handler.py" in content, (  # wording-check: incident record
        "Specific incident detail (contaminated commit) missing"
    )
