"""Behavioural tests for the sync_playbook skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- WSL environment pre-check (command -v powershell.exe)
- Repo path resolution order: $CLAUDE_PLAYBOOK_DIR first, then fallback
- Make command used for sync
- Step sequencing (pull before sync)
"""

from pathlib import Path

# ─── Constants ─────────────────────────────────────────────────────────────────

WSL_CHECK_COMMAND = "powershell.exe"
REPO_PATH_ENV_VAR = "CLAUDE_PLAYBOOK_DIR"
REPO_PATH_FALLBACK = "~/git_repos/dmt-scripts-claude_ai_playbook"
SYNC_MAKE_TARGET = "make sync"
PULL_COMMAND = "git pull"

# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_admin_skills" / "sync_playbook" / "SKILL.md"
)


def _skill_content() -> str:
    return SKILL_MD.read_text()


# ─── Tests: WSL pre-check ──────────────────────────────────────────────────────

def test_wsl_precheck_uses_powershell() -> None:
    """SKILL.md must check for powershell.exe to detect a WSL environment."""
    assert WSL_CHECK_COMMAND in _skill_content(), (
        "sync_playbook/SKILL.md must verify WSL by checking for powershell.exe"
    )


def test_wsl_precheck_stops_if_not_wsl() -> None:
    """SKILL.md must instruct Claude to stop if not running in WSL."""
    content = _skill_content()
    stop_terms = ["stop", "halt", "do not proceed"]
    assert any(term in content.lower() for term in stop_terms), (
        "sync_playbook/SKILL.md must stop execution if powershell.exe is not found (not WSL)"
    )


# ─── Tests: repo path resolution ───────────────────────────────────────────────

def test_env_var_checked_first() -> None:
    """SKILL.md must check $CLAUDE_PLAYBOOK_DIR before the fallback path."""
    content = _skill_content()
    assert REPO_PATH_ENV_VAR in content, (
        "sync_playbook/SKILL.md must check the CLAUDE_PLAYBOOK_DIR env var for the repo path"
    )
    env_pos = content.find(REPO_PATH_ENV_VAR)
    fallback_pos = content.find(REPO_PATH_FALLBACK)
    assert env_pos < fallback_pos, (
        "sync_playbook/SKILL.md must check $CLAUDE_PLAYBOOK_DIR before the fallback path"
    )


def test_fallback_path_documented() -> None:
    """SKILL.md must document the fallback repo path."""
    assert REPO_PATH_FALLBACK in _skill_content(), (
        f"sync_playbook/SKILL.md must document fallback path: {REPO_PATH_FALLBACK}"
    )


# ─── Tests: sync command ───────────────────────────────────────────────────────

def test_uses_make_sync() -> None:
    """SKILL.md must use 'make sync' to perform the sync step."""
    assert SYNC_MAKE_TARGET in _skill_content(), (
        "sync_playbook/SKILL.md must use 'make sync' as the sync command"
    )


# ─── Tests: step order ─────────────────────────────────────────────────────────

def test_pull_before_sync() -> None:
    """SKILL.md must pull latest changes before running make sync."""
    content = _skill_content()
    pull_pos = content.find(PULL_COMMAND)
    sync_pos = content.find(SYNC_MAKE_TARGET)
    assert pull_pos != -1, "sync_playbook/SKILL.md must include a git pull step"
    assert sync_pos != -1, "sync_playbook/SKILL.md must include a make sync step"
    assert pull_pos < sync_pos, (
        "sync_playbook/SKILL.md must pull before syncing — git pull must appear before make sync"
    )
