"""Behavioural tests for the create_pr skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- PR title format validation (conventional commits)
- PR title description cleanliness (no file extensions, path separators, or backticks)
- Label mapping (file paths, branch name, commit message → GitHub labels)
- Scope selection (changed file paths → scope string)

These tests serve as a living specification: when SKILL.md rules change, update
the constants and parametrize cases here to match.
"""

import re
from pathlib import Path

import pytest

# ─── PR title format ───────────────────────────────────────────────────────────

# Phase 3: title must match this regex.
TITLE_FORMAT_REGEX = re.compile(
    r"^(feat|fix|chore|docs|refactor|test|ci|perf|style|build|revert)"
    r"(\([^)]+\))?: [a-z]"
)

# File extensions that must not appear in the title description.
BANNED_EXTENSIONS_PATTERN = re.compile(
    r"\.(json|py|sql|yml|yaml|md|sh|tf)\b"
)


def _description(title: str) -> str:
    """Extract the description portion of a conventional commit title.

    Returns the text after the first ': '. Returns the full title if no
    separator is found (caller handles the invalid case).

    :param title: Full PR title string.
    :type title: str
    :return: Description substring.
    :rtype: str
    """
    if ": " in title:
        return title.split(": ", 1)[1]
    return title


def is_valid_title_format(title: str) -> bool:
    """Return True if the title matches the conventional commits format.

    :param title: Full PR title string.
    :type title: str
    :return: True if format is valid.
    :rtype: bool
    """
    return bool(TITLE_FORMAT_REGEX.match(title))


def is_clean_title_description(title: str) -> bool:
    """Return True if the title description contains no banned content.

    The description (text after ': ') must not contain:
    - File extensions (.json, .py, .sql, .yml, .yaml, .md, .sh, .tf)
    - Path separators (/)
    - Backticks

    The scope (text inside the parentheses) is excluded from this check —
    backticks and file extensions are valid there.

    :param title: Full PR title string.
    :type title: str
    :return: True if the description is clean.
    :rtype: bool
    """
    desc = _description(title)
    if BANNED_EXTENSIONS_PATTERN.search(desc):
        return False
    if "/" in desc:
        return False
    if "`" in desc:
        return False
    return True


# ─── Label mapping ─────────────────────────────────────────────────────────────

# Maps changed file path prefixes to GitHub label names.
FILE_PATH_LABEL_RULES: list[tuple[str, str]] = [
    ("src/claude/skills/", "claude-skill"),
    ("src/claude/rules/", "claude-rule"),
    ("src/claude/agents/", "claude-agent"),
    ("src/claude/hooks/", "claude-hook"),
    ("src/claude/process/", "claude-process"),
    ("src/claude/commands/", "claude-command"),
    ("src/claude/style_guide_standards/", "style-guide-and-standards"),
    ("src/sh/", "build scripts"),
    ("docs/", "documentation"),
]

# Commit message type → label.
COMMIT_TYPE_LABEL_RULES: dict[str, str] = {
    "refactor": "refactor",
}

# Commit message scope keyword → label.
COMMIT_SCOPE_LABEL_RULES: dict[str, str] = {
    "security": "security",
}


def get_labels(
    changed_files: list[str],
    branch: str = "",
    commit_message: str = "",
) -> set[str]:
    """Determine GitHub labels from changed files, branch name, and commit message.

    Implements the label mapping rules defined in create_pr/SKILL.md.

    :param changed_files: List of changed file paths relative to repo root.
    :type changed_files: list[str]
    :param branch: Current branch name.
    :type branch: str
    :param commit_message: Full commit message string.
    :type commit_message: str
    :return: Set of label names to apply.
    :rtype: set[str]
    """
    labels: set[str] = set()

    for path in changed_files:
        for prefix, label in FILE_PATH_LABEL_RULES:
            if path.startswith(prefix):
                labels.add(label)
                break

    if branch.startswith("hotfix/"):
        labels.add("hotfix")

    first_line = commit_message.splitlines()[0] if commit_message else ""
    type_match = re.match(r"^([a-z]+)(\(([^)]+)\))?[!]?:", first_line)
    if type_match:
        commit_type = type_match.group(1)
        commit_scope = type_match.group(3) or ""
        if commit_type in COMMIT_TYPE_LABEL_RULES:
            labels.add(COMMIT_TYPE_LABEL_RULES[commit_type])
        if any(kw in commit_scope for kw in COMMIT_SCOPE_LABEL_RULES):
            labels.add(COMMIT_SCOPE_LABEL_RULES["security"])

    if re.match(r"^[a-z]+(\([^)]+\))?!:", first_line) or "BREAKING CHANGE:" in commit_message:
        labels.add("breaking-change")

    return labels


# ─── Scope selection ───────────────────────────────────────────────────────────

_SKILLS_PREFIX = "src/claude/skills/"


def get_scope(changed_files: list[str]) -> str:
    """Determine the commit/PR title scope from changed file paths.

    Rules (applied in order):
    - Single file → filename in backticks, e.g. '`SKILL.md`'
    - Multiple files all within the same skill directory → skill name in backticks,
      e.g. '`create_pr`'
    - Multiple files within one non-skill area → area descriptor without backticks,
      e.g. 'rules', 'dependencies'
    - Multiple files across unrelated areas → empty string (omit scope)

    :param changed_files: List of changed file paths relative to repo root.
    :type changed_files: list[str]
    :return: Scope string (without parentheses), or '' to omit.
    :rtype: str
    """
    if not changed_files:
        return ""

    if len(changed_files) == 1:
        return f"`{changed_files[0].split('/')[-1]}`"

    # Check if all files that live inside a skill subdirectory belong to the same skill.
    # Files at the top level of skills/ (e.g. src/claude/skills/README.md) are excluded
    # from skill detection — they are index files, not part of a specific skill.
    skill_names = set()
    for path in changed_files:
        if path.startswith(_SKILLS_PREFIX):
            parts = path[len(_SKILLS_PREFIX):].split("/")
            if len(parts) >= 2:  # inside a skill subdirectory, not top-level skills/
                skill_names.add(parts[0])

    if len(skill_names) == 1:
        return f"`{next(iter(skill_names))}`"

    return ""


# ─── Tests: title format ───────────────────────────────────────────────────────

@pytest.mark.parametrize("title", [
    "feat(create_pr): improve PR creation workflow",
    "feat(`create_pr`): improve PR creation workflow",
    "fix: correct regression in label mapping",
    "chore: update dependencies",
    "docs: add usage examples",
    "refactor(rules): simplify scope selection logic",
    "test(`SKILL.md`): add behavioural tests for create pr skill",
    "ci: pin action versions",
])
def test_valid_title_format(title: str) -> None:
    """Titles in conventional commits format must pass the Phase 3 regex.

    :param title: PR title string to validate.
    :type title: str
    """
    assert is_valid_title_format(title), f"Expected valid format: {title!r}"


@pytest.mark.parametrize("title", [
    "Fix: something",                          # uppercase type
    "feat: Something",                         # uppercase description
    "update: something",                       # invalid type
    "feat(scope):something",                   # missing space after colon
    "Feat(scope): something",                  # uppercase type
    "feat scope: something",                   # missing parentheses around scope
])
def test_invalid_title_format(title: str) -> None:
    """Titles that violate the conventional commits format must fail the Phase 3 regex.

    :param title: PR title string to validate.
    :type title: str
    """
    assert not is_valid_title_format(title), f"Expected invalid format: {title!r}"


# ─── Tests: title cleanliness ──────────────────────────────────────────────────

@pytest.mark.parametrize("title", [
    "feat(`create_pr`): improve PR creation workflow",   # backtick in scope only — allowed
    "chore(`settings.json`): remove personal config",    # extension in scope only — allowed
    "fix: correct label mapping for hotfix branches",
    "feat(skills): add new skill for sprint planning",
])
def test_clean_title_description(title: str) -> None:
    """Titles with a clean description must pass the cleanliness check.

    :param title: PR title string to check.
    :type title: str
    """
    assert is_clean_title_description(title), f"Expected clean description: {title!r}"


@pytest.mark.parametrize("title", [
    "feat: update the settings.json file",       # extension in description
    "feat: update src/sh/ scripts",              # path separator in description
    "feat: update the `create_pr` skill",        # backtick in description
    "chore: pin requirements.yml versions",      # extension in description
    "fix: correct path in src/claude/rules/",    # path separator in description
])
def test_dirty_title_description(title: str) -> None:
    """Titles with banned content in the description must fail the cleanliness check.

    :param title: PR title string to check.
    :type title: str
    """
    assert not is_clean_title_description(title), f"Expected dirty description: {title!r}"


# ─── Tests: label mapping ──────────────────────────────────────────────────────

@pytest.mark.parametrize("changed_files,branch,commit_message,expected_labels", [
    (
        ["src/claude/skills/create_pr/SKILL.md"],
        "feature/update_create_pr_skill",
        "feat(`create_pr`): improve PR workflow",
        {"claude-skill"},
    ),
    (
        ["src/claude/rules/git.md"],
        "feature/update_git_rules",
        "docs(rules): update branch naming conventions",
        {"claude-rule"},
    ),
    (
        ["src/claude/skills/create_pr/SKILL.md", "docs/whats_installed.md"],
        "feature/update_create_pr_skill",
        "feat(`create_pr`): improve PR workflow",
        {"claude-skill", "documentation"},
    ),
    (
        ["src/claude/agents/core/architect.md"],
        "feature/update_architect_agent",
        "feat(agents): update architect scope",
        {"claude-agent"},
    ),
    (
        ["src/sh/some_script.sh"],
        "hotfix/fix_install_script",
        "fix(`some_script.sh`): correct install path",
        {"build scripts", "hotfix"},
    ),
    (
        ["src/claude/rules/security.md"],
        "feature/update_security_rules",
        "fix(security): tighten secret detection rules",
        {"claude-rule", "security"},
    ),
    (
        ["src/claude/skills/create_pr/SKILL.md"],
        "feature/breaking_change",
        "feat!: overhaul PR workflow",
        {"claude-skill", "breaking-change"},
    ),
])
def test_label_mapping(
    changed_files: list[str],
    branch: str,
    commit_message: str,
    expected_labels: set[str],
) -> None:
    """Label mapping must produce the correct set of labels for given inputs.

    :param changed_files: List of changed file paths.
    :type changed_files: list[str]
    :param branch: Branch name.
    :type branch: str
    :param commit_message: Commit message string.
    :type commit_message: str
    :param expected_labels: Expected set of label names.
    :type expected_labels: set[str]
    """
    assert get_labels(changed_files, branch, commit_message) == expected_labels


# ─── Tests: scope selection ────────────────────────────────────────────────────

@pytest.mark.parametrize("changed_files,expected_scope", [
    (
        ["src/claude/skills/create_pr/SKILL.md"],
        "`SKILL.md`",
    ),
    (
        ["src/claude/skills/create_pr/SKILL.md", "src/claude/skills/README.md"],
        "`create_pr`",
    ),
    (
        ["src/claude/rules/git.md"],
        "`git.md`",
    ),
    (
        [],
        "",
    ),
])
def test_scope_selection(changed_files: list[str], expected_scope: str) -> None:
    """Scope selection must derive the correct scope string from changed file paths.

    :param changed_files: List of changed file paths.
    :type changed_files: list[str]
    :param expected_scope: Expected scope string (without parentheses).
    :type expected_scope: str
    """
    assert get_scope(changed_files) == expected_scope


# ─── Tests: post-creation skill prompts ────────────────────────────────────────

SKILL_MD = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_git_skills" / "git_create_pr" / "SKILL.md"
)


def _skill_content() -> str:
    """Read the create_pr SKILL.md content.

    :return: Full file content as a string.
    :rtype: str
    """
    return SKILL_MD.read_text()


def test_skill_prompts_for_review_pr() -> None:
    """SKILL.md must prompt the user to run review_pr after the PR is created."""
    content = _skill_content()
    assert "review_pr" in content, (
        "create_pr/SKILL.md must prompt the user to run review_pr after PR creation"
    )


def test_skill_prompts_for_notify_pr() -> None:
    """SKILL.md must prompt the user to run notify_pr after the PR is created."""
    content = _skill_content()
    assert "notify_pr" in content, (
        "create_pr/SKILL.md must prompt the user to run notify_pr after PR creation"
    )


def test_skill_offers_both_prompts_together() -> None:
    """SKILL.md must offer review_pr and notify_pr in the same prompt block, not sequentially."""
    content = _skill_content()
    # Use rfind to find the last occurrence — earlier references may be examples or
    # path references elsewhere in the file, not the post-creation prompt block.
    review_pos = content.rfind("review_pr")
    notify_pos = content.rfind("notify_pr")
    assert review_pos != -1, "create_pr/SKILL.md must reference review_pr"
    assert notify_pos != -1, "create_pr/SKILL.md must reference notify_pr"
    # Both must appear within 500 characters of each other — same prompt block
    assert abs(review_pos - notify_pos) < 500, (
        "review_pr and notify_pr prompts must appear together in the same block, "
        f"but found them {abs(review_pos - notify_pos)} characters apart"
    )


def test_skill_instructs_parallel_execution() -> None:
    """SKILL.md must instruct Claude to run review_pr and notify_pr as parallel sub-agents."""
    content = _skill_content()
    assert "parallel" in content.lower(), (
        "create_pr/SKILL.md must instruct parallel execution when both review_pr and notify_pr are requested"
    )
