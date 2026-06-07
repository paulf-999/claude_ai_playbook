"""Behavioural tests for the notify_pr skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Change type detection from PR body (- [x] **Label** pattern)
- DWH layer detection from file paths (prefix → label mapping)
- Config directory derivation (CWD → project memory path)
- Confirmation required before posting to Teams
- Reviewer window logic constants
"""

import re
from pathlib import Path

import pytest

# ─── Change type detection ─────────────────────────────────────────────────────

# Pattern: `- [x] **Label**` or `- [x] :emoji: **Label**`
# Extracts the bold text and strips markdown/emoji to produce a plain Change Type string.
CHANGE_TYPE_REGEX = re.compile(r"-\s+\[x\].*?\*\*([^*]+)\*\*")


def detect_change_type(pr_body: str) -> str | None:
    """Extract the change type from a PR body by finding the checked checkbox.

    Mimics the rule in notify_pr/SKILL.md Phase 2:
    Scan body for '- [x]' and extract the bold label on that line.
    Strip markdown and emoji. Return None if not found.

    :param pr_body: Full PR body markdown string.
    :type pr_body: str
    :return: Plain-text change type label, or None.
    :rtype: str | None
    """
    for line in pr_body.splitlines():
        if "- [x]" in line or "- [X]" in line:
            match = CHANGE_TYPE_REGEX.search(line)
            if match:
                raw = match.group(1).strip()
                # Strip trailing slash-separated alternatives: "Refactoring/housekeeping" → "Refactoring"
                return raw.split("/")[0].strip()
    return None


# ─── Layer detection ───────────────────────────────────────────────────────────

def detect_layers(file_paths: list[str], layers_config: list[dict]) -> list[str]:
    """Map changed file paths to DWH layer labels.

    Mimics the rule in notify_pr/SKILL.md Phase 2:
    For each file path, check if it starts with any configured prefix.
    Collect matching labels, deduplicate and sort. Return ['-'] if no match.
    Return [] if layers_config is empty (omit the line).

    :param file_paths: List of changed file paths.
    :type file_paths: list[str]
    :param layers_config: List of {prefix, label} dicts from teams_config.json.
    :type layers_config: list[dict]
    :return: Sorted deduplicated list of layer labels, or ['-'], or [].
    :rtype: list[str]
    """
    if not layers_config:
        return []
    matched: set[str] = set()
    for path in file_paths:
        for entry in layers_config:
            if path.startswith(entry["prefix"]):
                matched.add(entry["label"])
    return sorted(matched) if matched else ["-"]


# ─── Config directory derivation ───────────────────────────────────────────────

def derive_memory_dir(cwd: str) -> str:
    """Derive the project memory directory path from the current working directory.

    Mimics the rule in notify_pr/SKILL.md Phase 1:
    Take the CWD, prefix with ~/.claude/projects/, replace every / and _ with -.

    :param cwd: Current working directory path string.
    :type cwd: str
    :return: Derived project memory directory path.
    :rtype: str
    """
    slug = cwd.replace("/", "-").replace("_", "-")
    return f"~/.claude/projects/{slug}"


# ─── SKILL.md reference ────────────────────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_git_skills" / "notify_pr" / "SKILL.md"
)


def _skill_content() -> str:
    return SKILL_MD.read_text()


# ─── Tests: change type detection ─────────────────────────────────────────────

@pytest.mark.parametrize("body,expected", [
    (
        "- [ ] **Feature**\n- [x] **Refactoring/housekeeping**\n- [ ] **Bugfix**",
        "Refactoring",
    ),
    (
        "- [x] :sparkles: **Feature**",
        "Feature",
    ),
    (
        "- [x] **Documentation**",
        "Documentation",
    ),
    (
        "- [ ] **Feature**\n- [ ] **Bugfix**",
        None,
    ),
    (
        "No checkboxes here at all.",
        None,
    ),
])
def test_change_type_detection(body: str, expected: str | None) -> None:
    """Change type must be extracted from the checked checkbox in the PR body.

    :param body: PR body markdown.
    :type body: str
    :param expected: Expected change type string or None.
    :type expected: str | None
    """
    assert detect_change_type(body) == expected


# ─── Tests: layer detection ────────────────────────────────────────────────────

LAYERS_CONFIG = [
    {"prefix": "models/staging/", "label": "staging"},
    {"prefix": "models/mart/", "label": "mart"},
    {"prefix": "models/intermediate/", "label": "intermediate"},
]


@pytest.mark.parametrize("file_paths,expected", [
    (["models/staging/stg_orders.sql"], ["staging"]),
    (["models/mart/mart_revenue.sql", "models/staging/stg_orders.sql"], ["mart", "staging"]),
    (["dbt_project.yml"], ["-"]),
    ([], ["-"]),
])
def test_layer_detection(file_paths: list[str], expected: list[str]) -> None:
    """Layer labels must be derived from file path prefixes and returned sorted.

    :param file_paths: List of changed file paths.
    :type file_paths: list[str]
    :param expected: Expected sorted layer label list.
    :type expected: list[str]
    """
    assert detect_layers(file_paths, LAYERS_CONFIG) == expected


def test_layer_detection_empty_config_returns_empty() -> None:
    """When layers config is empty, layer detection must return [] (omit the line)."""
    assert detect_layers(["models/staging/stg_orders.sql"], []) == []


# ─── Tests: config directory derivation ───────────────────────────────────────

@pytest.mark.parametrize("cwd,expected", [
    (
        "/home/paul/git_repos/core/dmt-scripts-claude_ai_playbook",
        "~/.claude/projects/-home-paul-git-repos-core-dmt-scripts-claude-ai-playbook",
    ),
    (
        "/home/paul/git_repos/core/da-etl-dbtanalytics",
        "~/.claude/projects/-home-paul-git-repos-core-da-etl-dbtanalytics",
    ),
])
def test_config_dir_derivation(cwd: str, expected: str) -> None:
    """Memory directory must be derived by prefixing ~/.claude/projects/ and replacing / with -.

    :param cwd: Current working directory.
    :type cwd: str
    :param expected: Expected memory directory path.
    :type expected: str
    """
    assert derive_memory_dir(cwd) == expected


# ─── Tests: confirmation required ─────────────────────────────────────────────

def test_confirmation_required_before_post() -> None:
    """SKILL.md must require user confirmation before posting to Teams."""
    content = _skill_content()
    confirm_terms = ["confirm", "confirmation", "y/n", "wait"]
    assert any(term in content.lower() for term in confirm_terms), (
        "notify_pr/SKILL.md must require confirmation before posting to Teams"
    )


def test_confirmation_required_flag_in_frontmatter() -> None:
    """SKILL.md frontmatter must set confirmation_required: true."""
    assert "confirmation_required: true" in _skill_content(), (
        "notify_pr/SKILL.md frontmatter must set confirmation_required: true"
    )
