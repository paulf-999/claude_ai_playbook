# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-21
# Date updated:      2026-10-01
# Version:           1.2.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Content-regression tests for git/_concurrent_sessions.md.

Goal: not to prove Claude follows this rule (not mechanically testable
without a live-session eval harness), but to catch silent loss of its
key guidance in a future edit or merge — the exact failure mode this
rule itself documents (2026-09-21 concurrent-session incident).

Single file, no external dependencies, no fixtures: deliberately kept
structurally simple (complexity score 7) while covering 15+ assertions
across every major section, per _test_metadata_complexity_scoring.md's
"thoroughness and simplicity aren't opposed" principle.
"""
from pathlib import Path

from _shared_paths import CLAUDE_DIR

RULE_FILE = CLAUDE_DIR / "_rules" / "02_claude_standards" / "git" / "_concurrent_sessions.md"
GIT_MD = CLAUDE_DIR / "_rules" / "02_claude_standards" / "git.md"
TIER_README = CLAUDE_DIR / "_rules" / "02_claude_standards" / "README.md"


def readme_related_entry(readme: Path, rel_path: str) -> str:
    """Return one file's block from a tier README's "🔗 Related rules" section.

    Related links moved out of rule files into tier READMEs (#121), so each
    file's parent/sibling links now live under a ``### `<rel_path>` `` heading.

    :param readme: The tier README holding the Related rules section.
    :type readme: Path
    :param rel_path: The rule's path relative to the README's directory.
    :type rel_path: str
    :return: The block's text, or an empty string if the heading is absent.
    :rtype: str
    """
    lines = readme.read_text().splitlines()
    heading = f"### `{rel_path}`"
    if heading not in lines:
        return ""
    start = lines.index(heading) + 1
    end = next(
        (idx for idx in range(start, len(lines)) if lines[idx].startswith(("### ", "## "))),
        len(lines),
    )
    return "\n".join(lines[start:end])


def test_concurrent_sessions_file_exists():
    """_concurrent_sessions.md must be present at the expected path."""
    assert RULE_FILE.exists(), f"_concurrent_sessions.md missing: {RULE_FILE}"


def test_concurrent_sessions_imported_from_git_md():
    """git.md must import _concurrent_sessions.md, or it's unreachable."""
    content = GIT_MD.read_text()
    assert "_concurrent_sessions.md" in content, (
        "git.md does not @import _concurrent_sessions.md — rule is orphaned"
    )


def test_concurrent_sessions_has_purpose_statement():
    """File must open with a Purpose statement, per writing_style.md."""
    content = RULE_FILE.read_text()
    assert "**Purpose:**" in content, "_concurrent_sessions.md missing a Purpose statement"


def test_concurrent_sessions_documents_real_incident():
    """The real 2026-09-21 incident must stay documented, not just the abstract rule."""
    content = RULE_FILE.read_text()
    assert "2026-09-21" in content, "Incident date missing"
    assert "confluence_create_page_handler.py" in content, (
        "Specific incident detail (contaminated commit) missing"
    )


def test_concurrent_sessions_covers_detect_early():
    """'Detect early, don't assume' guidance must survive edits."""
    content = RULE_FILE.read_text()
    assert "Detect early" in content, "Detect-early section missing"
    assert "don't assume" in content.lower(), "Core 'don't assume' framing missing"


def test_concurrent_sessions_covers_never_blind_stage():
    """Stage-by-name guidance (the single control that prevented catastrophe) must survive."""
    content = RULE_FILE.read_text()
    assert "blind-stage" in content.lower(), "Blind-stage anti-pattern section missing"
    assert "git add -A" in content, "Explicit git add -A warning missing"


def test_concurrent_sessions_covers_index_reset():
    """Reset-before-each-commit guidance must survive."""
    content = RULE_FILE.read_text()
    assert "git reset" in content, "git reset guidance missing"
    assert "unstages only" in content.lower() or "never touches file content" in content.lower(), (
        "Safety clarification for git reset missing"
    )


def test_concurrent_sessions_covers_stash_operations():
    """Stash-conflict guidance must survive."""
    content = RULE_FILE.read_text()
    assert "git stash pop" in content, "git stash pop guidance missing"
    assert "git stash list" in content, "Never-drop-another-session's-stash guidance missing"


def test_concurrent_sessions_covers_precommit_isolation():
    """Pre-commit isolation caveat and its diagnostic command must survive."""
    content = RULE_FILE.read_text()
    assert "pre-commit" in content.lower(), "Pre-commit isolation section missing"
    assert "git stash push --keep-index --include-untracked" in content, (
        "Manual isolation-replication command missing"
    )


def test_concurrent_sessions_covers_worktree_preference():
    """git worktree recommendation, for both sessions and sub-agents, must survive."""
    content = RULE_FILE.read_text()
    assert "git worktree" in content, "git worktree guidance missing"
    assert "isolation" in content.lower(), "Sub-agent isolation guidance missing"


def test_concurrent_sessions_related_section_links_siblings():
    """The tier README's Related entry must still link to git.md and its siblings."""
    entry = readme_related_entry(TIER_README, "git/_concurrent_sessions.md")
    assert entry, "02_claude_standards/README.md has no Related entry for git/_concurrent_sessions.md"
    for target in ["git.md", "_safe_patterns.md", "_commits.md", "behaviour.md"]:
        assert target in entry, f"README Related entry missing link to {target}"


def test_concurrent_sessions_line_limit():
    """_concurrent_sessions.md must not exceed 110 lines."""
    lines = RULE_FILE.read_text().splitlines()
    assert len(lines) <= 110, f"_concurrent_sessions.md: {len(lines)} lines exceeds 110-line limit"


def test_concurrent_sessions_ends_with_newline():
    """_concurrent_sessions.md must end with exactly one newline."""
    raw = RULE_FILE.read_bytes()
    assert raw.endswith(b"\n"), "_concurrent_sessions.md does not end with a newline"
    assert not raw.endswith(b"\n\n"), "_concurrent_sessions.md ends with multiple newlines"
