# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# Date created:      2026-10-01
# Version:           1.1.0
# Date updated:      2026-10-01
# ─────────────────────────────────────────────────────────

"""Proves the file-structure scanner flags bad names and skips what it should.

``test_file_structure_compliance.py`` runs the scanner over the real config, so it
only shows the config is clean today. These tests build small fake config trees in
a temp directory and check the scanner catches each kind of bad case — so a change
that silences it fails here.
"""
from pathlib import Path

from test_file_structure_compliance import FileStructureValidator

HINT = "— see claude_directory_structure/_claude_directory_naming.md"


def make_files(root: Path, *relative_paths: str) -> None:
    """Create empty files under a fake config root.

    :param root: Root of the fake config tree.
    :type root: Path
    :param relative_paths: File paths relative to ``root``.
    :type relative_paths: str
    """
    for relative_path in relative_paths:
        file_path = root / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()


def scan(root: Path) -> list[dict]:
    """Run the scanner over a fake config root.

    :param root: Root of the fake config tree.
    :type root: Path
    :return: Violation dicts found by the scanner.
    :rtype: list[dict]
    """
    return FileStructureValidator(root).scan()


def errors_for(violations: list[dict], filename: str) -> list[dict]:
    """Return the error-severity violations whose path ends with ``filename``.

    :param violations: Violation dicts from the scanner.
    :type violations: list[dict]
    :param filename: File name to match against each violation's path.
    :type filename: str
    :return: Matching error violations.
    :rtype: list[dict]
    """
    return [v for v in violations if v["severity"] == "error" and Path(v["path"]).name == filename]


def test_hyphenated_markdown_is_an_error(tmp_path: Path) -> None:
    """A hyphenated .md file name is reported as a snake_case error."""
    make_files(tmp_path, "bad-name.md")
    errors = errors_for(scan(tmp_path), "bad-name.md")
    assert len(errors) == 1, f"bad-name.md should give exactly one error {HINT}"
    assert errors[0]["rule"] == "Invalid naming: not snake_case", f"wrong rule: {errors[0]['rule']}"


def test_camel_case_python_is_an_error(tmp_path: Path) -> None:
    """A CamelCase .py file name is reported as a snake_case error."""
    make_files(tmp_path, "BadName.py")
    errors = errors_for(scan(tmp_path), "BadName.py")
    assert len(errors) == 1, f"BadName.py should give exactly one error {HINT}"
    assert "snake_case" in errors[0]["message"], f"message should name snake_case: {errors[0]['message']}"


def test_snake_case_file_gives_no_violations(tmp_path: Path) -> None:
    """A snake_case file at the root gives no violations at all."""
    make_files(tmp_path, "good_name.md", "helper_script.py")
    violations = scan(tmp_path)
    assert violations == [], f"valid names should be clean, got {violations}"


def test_child_prefix_passes_snake_case(tmp_path: Path) -> None:
    """A leading-underscore child file is valid snake_case and needs no rename."""
    make_files(tmp_path, "_rules/01_essentials/topic/_child_aspect.md")
    violations = [v for v in scan(tmp_path) if Path(v["path"]).name == "_child_aspect.md"]
    assert violations == [], f"_child_aspect.md should be clean {HINT}, got {violations}"


def test_exact_name_exceptions_are_exempt(tmp_path: Path) -> None:
    """CLAUDE.md, SKILL.md and skill.contract.yaml are exempt from snake_case."""
    make_files(tmp_path, "CLAUDE.md", "skills/demo_skill/SKILL.md", "skills/demo_skill/skill.contract.yaml")
    violations = scan(tmp_path)
    for name in ["CLAUDE.md", "SKILL.md", "skill.contract.yaml"]:
        flagged = [v for v in violations if Path(v["path"]).name == name]
        assert flagged == [], f"{name} is a required exact name and must be exempt, got {flagged}"


def test_dotfiles_are_ignored(tmp_path: Path) -> None:
    """Tooling dotfiles such as .gitkeep are never flagged."""
    make_files(tmp_path, ".gitkeep", "_docs/.gitkeep")
    violations = scan(tmp_path)
    assert violations == [], f"dotfiles should be ignored, got {violations}"


def test_valid_template_is_exempt(tmp_path: Path) -> None:
    """A template named after an exact-name target, like AGENT.md.template, is exempt."""
    make_files(tmp_path, "_templates/AGENT.md.template")
    violations = scan(tmp_path)
    assert violations == [], f"AGENT.md.template should be exempt, got {violations}"


def test_bad_template_is_flagged(tmp_path: Path) -> None:
    """A template whose target name breaks snake_case is still flagged."""
    make_files(tmp_path, "_templates/Bad-Name.md.template")
    errors = errors_for(scan(tmp_path), "Bad-Name.md.template")
    assert len(errors) == 1, f"Bad-Name.md.template should be flagged {HINT}"
    assert "Bad-Name.md" in errors[0]["message"], f"message should name the target: {errors[0]['message']}"


def test_auto_generated_dir_is_skipped(tmp_path: Path) -> None:
    """A bad name inside an auto-generated directory like memory/ is not scanned."""
    make_files(tmp_path, "memory/Bad-Name.md", "memory/nested/Other-Bad.py")
    violations = scan(tmp_path)
    assert violations == [], f"memory/ is auto-generated and must be skipped, got {violations}"


def test_hidden_dir_is_skipped(tmp_path: Path) -> None:
    """A bad name inside a hidden directory like .cache/ is not scanned."""
    make_files(tmp_path, ".cache/Bad-Name.md")
    violations = scan(tmp_path)
    assert violations == [], f".cache/ is hidden and must be skipped, got {violations}"


def test_unprefixed_nested_markdown_is_info(tmp_path: Path) -> None:
    """An un-prefixed nested .md file gets an info nudge, not an error."""
    make_files(tmp_path, "_reference/topic/guide.md")
    violations = scan(tmp_path)
    assert len(violations) == 1, f"expected one child-prefix nudge, got {violations}"
    assert violations[0]["severity"] == "info", f"child-prefix nudge must be info, not {violations[0]['severity']}"
    assert violations[0]["rule"] == "Child files should start with underscore", f"wrong rule: {violations[0]['rule']}"


def test_rules_missing_tier_is_warning(tmp_path: Path) -> None:
    """A _rules/ directory missing a tier subdirectory gives a warning."""
    (tmp_path / "_rules" / "01_essentials").mkdir(parents=True)
    violations = scan(tmp_path)
    missing = {v["rule"] for v in violations if v["severity"] == "warning"}
    assert "Missing subdirectory: 05_lazy_load" in missing, f"missing tier should warn, got {missing}"
    assert "Missing subdirectory: 03_authoring_guidelines" in missing, f"tier 03 must be expected too, got {missing}"
    assert "Missing subdirectory: 01_essentials" not in missing, "a tier that exists must not be reported"


def test_missing_config_dir_is_an_error(tmp_path: Path) -> None:
    """A config directory that doesn't exist gives a 'Directory exists' error."""
    violations = scan(tmp_path / "does_not_exist")
    assert len(violations) == 1, f"expected one error, got {violations}"
    assert violations[0]["rule"] == "Directory exists", f"wrong rule: {violations[0]['rule']}"
    assert violations[0]["severity"] == "error", "a missing config dir must be an error"


def test_every_violation_has_required_keys(tmp_path: Path) -> None:
    """Every violation dict carries path, rule, severity and message."""
    make_files(tmp_path, "bad-name.md", "_reference/topic/guide.md")
    (tmp_path / "_rules").mkdir()
    violations = scan(tmp_path)
    assert len(violations) >= 3, f"fixture should produce error, info and warning cases, got {violations}"
    for violation in violations:
        missing = {"path", "rule", "severity", "message"} - violation.keys()
        assert not missing, f"violation {violation} is missing keys {missing}"
        assert violation["severity"] in {"error", "warning", "info"}, f"unknown severity {violation['severity']}"
