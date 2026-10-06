# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-02
# Date updated:      2026-10-06
# Version:           1.1.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates that every script under _scripts/ follows the script naming pattern.

The pattern lives in _claude_naming_patterns.md: each script sits in a
_<verb>_scripts/ folder and its filename starts with that verb, so the name
alone says what the script does.
"""

import re
from pathlib import Path

from _shared_paths import CLAUDE_DIR

SCRIPTS_DIR = CLAUDE_DIR / "_scripts"
NAMING_STANDARDS_DIR = CLAUDE_DIR / "rules" / "01_essentials" / "claude_usage_standards" / "naming_standards"
NAMING_RULE = NAMING_STANDARDS_DIR / "_claude_naming_patterns.md"

# A group folder is _<verb>_scripts/, where the verb is one snake_case word
GROUP_PATTERN = re.compile(r"^_([a-z]+)_scripts$")
SNAKE_CASE_PY = re.compile(r"^[a-z][a-z0-9_]*\.py$")
IGNORED_NAMES = {"__pycache__", ".DS_Store"}


def find_violations(scripts_dir: Path) -> list[str]:
    """List every way the scripts under scripts_dir break the naming pattern.

    :param scripts_dir: The _scripts/ folder to check.
    :type scripts_dir: Path
    :return: One message per violation, empty when everything complies.
    :rtype: list[str]
    """
    violations = []
    for entry in sorted(scripts_dir.iterdir()):
        if entry.name in IGNORED_NAMES:
            continue

        # Scripts must sit in a group folder, never loose at the top level
        if entry.is_file():
            violations.append(f"{entry.name}: loose in _scripts/ — move it into a _<verb>_scripts/ folder")
            continue

        match = GROUP_PATTERN.match(entry.name)
        if not match:
            violations.append(f"{entry.name}/: folder name must match _<verb>_scripts")
            continue

        verb = match.group(1)
        scripts = [child for child in entry.iterdir() if child.name not in IGNORED_NAMES]

        # A group earns its folder only once two scripts share the verb
        if len(scripts) < 2:
            violations.append(f"{entry.name}/: holds {len(scripts)} script(s) — a group needs at least 2")

        for script in scripts:
            if script.is_dir():
                violations.append(f"{entry.name}/{script.name}/: group folders must not be nested")
            elif not SNAKE_CASE_PY.match(script.name):
                violations.append(f"{entry.name}/{script.name}: must be a snake_case .py file")
            elif not script.name.startswith(f"{verb}_"):
                violations.append(f"{entry.name}/{script.name}: must start with '{verb}_'")
    return violations


def make_group(root: Path, folder: str, *names: str) -> Path:
    """Create a group folder holding empty files with the given names.

    :param root: The fake _scripts/ folder.
    :type root: Path
    :param folder: Name of the group folder to create.
    :type folder: str
    :param names: Filenames to create inside the folder.
    :type names: str
    :return: The created group folder.
    :rtype: Path
    """
    group = root / folder
    group.mkdir(parents=True)
    for name in names:
        (group / name).touch()
    return group


# ── live config ───────────────────────────────────────────────────────────────


def test_scripts_dir_exists():
    """The _scripts/ folder exists in the config under test."""
    assert SCRIPTS_DIR.is_dir(), f"Expected {SCRIPTS_DIR} to exist"


def test_live_scripts_follow_naming_pattern():
    """Every real script follows the pattern, with no violations."""
    violations = find_violations(SCRIPTS_DIR)
    assert violations == [], "Script naming violations:\n" + "\n".join(violations)


def test_live_has_no_loose_scripts():
    """No file sits directly in _scripts/."""
    loose = [path.name for path in SCRIPTS_DIR.iterdir() if path.is_file() and path.name not in IGNORED_NAMES]
    assert loose == [], f"Move these into a _<verb>_scripts/ folder: {loose}"


def test_live_expected_groups_present():
    """The audit, clean and lint groups all exist."""
    groups = {path.name for path in SCRIPTS_DIR.iterdir() if path.is_dir()}
    for folder in ("_audit_scripts", "_clean_scripts", "_lint_scripts"):
        assert folder in groups, f"Expected group folder {folder}/ in {SCRIPTS_DIR}"


def test_naming_rule_documents_pattern():
    """The naming rule still documents the script pattern and points at this test."""
    text = NAMING_RULE.read_text(encoding="utf-8")
    assert "## 🐍 Script naming" in text, "Script naming section missing from _claude_naming_patterns.md"
    assert "_scripts/_<verb>_scripts/<verb>_<subject>.py" in text, "Script pattern missing from the naming rule"
    assert "test_script_naming.py" in text, "Naming rule should name the test that enforces it"


# ── checker behaviour ─────────────────────────────────────────────────────────


def test_compliant_tree_passes(tmp_path):
    """A tree that follows the pattern reports no violations."""
    make_group(tmp_path, "_lint_scripts", "lint_tags.py", "lint_skills.py")
    make_group(tmp_path, "_clean_scripts", "clean_plans.py", "clean_backups.py")
    assert find_violations(tmp_path) == [], "A compliant tree should pass"


def test_loose_script_flagged(tmp_path):
    """A script directly in _scripts/ is flagged."""
    make_group(tmp_path, "_lint_scripts", "lint_tags.py", "lint_skills.py")
    (tmp_path / "score_things.py").touch()
    violations = find_violations(tmp_path)
    assert len(violations) == 1, f"Expected one violation, got {violations}"
    assert "loose in _scripts/" in violations[0], "Loose script message should say where it is"


def test_wrong_verb_prefix_flagged(tmp_path):
    """A script whose name doesn't start with its folder's verb is flagged."""
    make_group(tmp_path, "_audit_scripts", "audit_rules.py", "skill_scorer.py")
    violations = find_violations(tmp_path)
    assert violations == ["_audit_scripts/skill_scorer.py: must start with 'audit_'"], violations


def test_bad_folder_name_flagged(tmp_path):
    """A folder not shaped like _<verb>_scripts is flagged."""
    make_group(tmp_path, "lint_scripts", "lint_tags.py", "lint_skills.py")
    violations = find_violations(tmp_path)
    assert violations == ["lint_scripts/: folder name must match _<verb>_scripts"], violations


def test_single_script_group_flagged(tmp_path):
    """A group folder with only one script is flagged."""
    make_group(tmp_path, "_score_scripts", "score_skills.py")
    violations = find_violations(tmp_path)
    assert any("needs at least 2" in message for message in violations), violations


def test_non_snake_case_flagged(tmp_path):
    """A script name that isn't snake_case is flagged."""
    make_group(tmp_path, "_lint_scripts", "lint_tags.py", "lint-skills.py")
    violations = find_violations(tmp_path)
    assert violations == ["_lint_scripts/lint-skills.py: must be a snake_case .py file"], violations


def test_nested_folder_flagged(tmp_path):
    """A folder nested inside a group folder is flagged."""
    group = make_group(tmp_path, "_lint_scripts", "lint_tags.py")
    (group / "_extra").mkdir()
    violations = find_violations(tmp_path)
    assert any("must not be nested" in message for message in violations), violations


def test_pycache_ignored(tmp_path):
    """Python's __pycache__ folders are never reported."""
    group = make_group(tmp_path, "_lint_scripts", "lint_tags.py", "lint_skills.py")
    (group / "__pycache__").mkdir()
    (tmp_path / "__pycache__").mkdir()
    assert find_violations(tmp_path) == [], "__pycache__ should be ignored"
