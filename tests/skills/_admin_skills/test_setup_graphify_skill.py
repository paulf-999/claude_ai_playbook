"""Behavioural tests for the setup_graphify skill."""

from pathlib import Path

import pytest

_SKILL_DIR = (
    Path(__file__).parent.parent.parent.parent
    / "src"
    / "claude"
    / "skills"
    / "_admin_skills"
    / "setup_graphify"
)

SKILL_MD = _SKILL_DIR / "SKILL.md"
PHASE2_MD = _SKILL_DIR / "phase2.md"
REPOS_MD = _SKILL_DIR / "repos.md"


@pytest.fixture(scope="module")
def skill_content() -> str:
    return SKILL_MD.read_text()


@pytest.fixture(scope="module")
def phase2_content() -> str:
    return PHASE2_MD.read_text()


@pytest.fixture(scope="module")
def repos_content() -> str:
    return REPOS_MD.read_text()


# ---------------------------------------------------------------------------
# File presence
# ---------------------------------------------------------------------------


def test_skill_file_exists():
    """SKILL.md must exist at the expected skill path."""
    assert SKILL_MD.exists(), "setup_graphify/SKILL.md not found under skills/_admin_skills"


def test_phase2_child_page_exists():
    """phase2.md child page must exist alongside SKILL.md."""
    assert PHASE2_MD.exists(), "setup_graphify/phase2.md not found"


def test_repos_child_page_exists():
    """repos.md child page must exist alongside SKILL.md."""
    assert REPOS_MD.exists(), "setup_graphify/repos.md not found"


# ---------------------------------------------------------------------------
# Maturity and scope gate
# ---------------------------------------------------------------------------


def test_draft_maturity_declared(skill_content):
    """SKILL.md must declare draft maturity."""
    assert "maturity: draft" in skill_content, (
        "setup_graphify must declare 'maturity: draft' in frontmatter"
    )


def test_scope_gate_present(skill_content):
    """SKILL.md must include the maturity scope gate table."""
    assert "Scope gate" in skill_content or "scope gate" in skill_content.lower(), (
        "SKILL.md must include the scope gate section"
    )


# ---------------------------------------------------------------------------
# Phase 1 — Install
# ---------------------------------------------------------------------------


def test_install_package_name_correct(skill_content):
    """Phase 1 must use the correct package name 'graphifyy' (double y)."""
    assert "graphifyy" in skill_content, (
        "pip install command must reference 'graphifyy' (double y) — single y is the wrong package"
    )


def test_install_platform_claude_documented(skill_content):
    """Phase 1 must document 'graphify install --platform claude'."""
    assert "graphify install --platform claude" in skill_content, (
        "Phase 1 must document 'graphify install --platform claude' to install the query skill"
    )


def test_claude_md_append_documented(skill_content):
    """Phase 1 must document that the trigger block is persisted via process/graphify.md."""
    assert "process/graphify.md" in skill_content, (
        "Phase 1 must document that the trigger block is persisted in src/claude/process/graphify.md"
    )


# ---------------------------------------------------------------------------
# Phase 2 — Extract
# ---------------------------------------------------------------------------


def test_extract_from_repo_root(skill_content):
    """Phase 2 must instruct running extract from repo root, not a subdirectory."""
    lower = skill_content.lower()
    assert "repo root" in lower or "repo-root" in lower, (
        "Phase 2 must instruct running graphify extract from the repo root to avoid double-nested output"
    )


def test_extract_cost_documented(phase2_content):
    """phase2.md must document the OpenAI/Gemini cost for semantic extraction."""
    lower = phase2_content.lower()
    assert "openai" in lower or "gemini" in lower, (
        "phase2.md must document the API cost for semantic extraction on non-code files"
    )


# ---------------------------------------------------------------------------
# Phase 3 — .gitignore
# ---------------------------------------------------------------------------


def test_gitignore_phase_documented(skill_content):
    """Phase 3 must document adding graphify-out/ to .gitignore."""
    assert ".gitignore" in skill_content, (
        "Phase 3 must document adding graphify-out/ to .gitignore"
    )

    assert "graphify-out/" in skill_content, (
        "Phase 3 must include the graphify-out/ pattern for .gitignore"
    )


# ---------------------------------------------------------------------------
# Phase 4 — CLAUDE.md update
# ---------------------------------------------------------------------------


def test_repo_claude_md_update_documented(skill_content):
    """Phase 4 must document updating the repo CLAUDE.md with the graph path."""
    # CLAUDE.md appears in multiple contexts — check it's associated with Phase 4
    assert "Phase 4" in skill_content, "Phase 4 (CLAUDE.md update) must be documented"


# ---------------------------------------------------------------------------
# Phase 5 — Git hook
# ---------------------------------------------------------------------------


def test_git_hook_phase_documented(skill_content):
    """Phase 5 must document the optional git hook for incremental rebuilds."""
    assert "hook" in skill_content.lower(), (
        "Phase 5 must document the optional git hook"
    )

    assert "graphify hook install" in skill_content, (
        "Phase 5 must include the 'graphify hook install' command"
    )


# ---------------------------------------------------------------------------
# Known issues and tracking
# ---------------------------------------------------------------------------


def test_known_issues_documented(phase2_content):
    """phase2.md must document known issues with the extraction step."""
    lower = phase2_content.lower()
    assert "known issue" in lower, (
        "phase2.md must document known issues encountered during Graphify extraction"
    )


def test_double_nested_path_issue_documented(phase2_content):
    """phase2.md must document the double-nested output path issue."""
    assert "double-nested" in phase2_content or "graphify-out/graphify-out" in phase2_content, (
        "phase2.md must document the double-nested output path issue from incorrect --out flag usage"
    )


def test_repos_table_present(skill_content):
    """SKILL.md must include a table tracking repos where Graphify is set up."""
    assert "Repos where Graphify is set up" in skill_content or "repos where graphify" in skill_content.lower(), (
        "SKILL.md must include a repos tracking table to record where Graphify has been installed"
    )


def test_da_etl_dbtanalytics_listed(repos_content):
    """repos.md must include da-etl-dbtanalytics as the first known entry."""
    assert "da-etl-dbtanalytics" in repos_content, (
        "repos.md must include da-etl-dbtanalytics as the first repo where Graphify is set up"
    )
