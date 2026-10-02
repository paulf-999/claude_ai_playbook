# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-02
# Version:           2.0.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Proves every file in the real Claude config passes the file-structure scan.

The scan comes from ``_file_structure_validator.py``: snake_case names and the
``_rules/`` tiers. Each main area of the config gets its own test, so a failure
names the area at fault, and each test first checks its area exists, so a moved or
missing folder can't pass by being skipped.

``test_file_structure_validator.py`` proves the scanner itself on fake config trees.
"""
from functools import cache

import pytest

from _file_structure_validator import CLAUDE_HOME, FileStructureValidator

HINT = "— see _rules/01_essentials/claude_usage_standards/claude_directory_structure.md"


@cache
def scan_errors() -> tuple[dict, ...]:
    """Scan the real config once and keep only the error-level violations.

    :return: Error violations, each a dict with keys path, rule, severity and message.
    :rtype: tuple[dict, ...]
    """
    return tuple(v for v in FileStructureValidator().scan() if v["severity"] == "error")


def errors_under(area: str) -> list[str]:
    """List the scan errors for files under one top-level folder.

    :param area: Top-level folder name, e.g. ``_rules``.
    :type area: str
    :return: One ``path: message`` line per error under that folder.
    :rtype: list[str]
    """
    return [f"{v['path']}: {v['message']}" for v in scan_errors() if v["path"].split("/")[0] == area]


def missing_area(area: str) -> str:
    """Build the failure message for a top-level folder that isn't there.

    :param area: Top-level folder name, e.g. ``hooks``.
    :type area: str
    :return: A message saying the folder can't be scanned.
    :rtype: str
    """
    return f"{area}/ is missing from {CLAUDE_HOME}, so it can't be scanned"


def error_report(area: str, errors: list[str]) -> str:
    """Build the failure message listing one folder's naming errors.

    :param area: Top-level folder name, e.g. ``hooks``.
    :type area: str
    :param errors: ``path: message`` lines from ``errors_under``.
    :type errors: list[str]
    :return: A message naming the folder and every error in it.
    :rtype: str
    """
    return f"Naming errors in {area}/ {HINT}:\n  " + "\n  ".join(errors)


def test_config_dir_exists():
    """The config directory is there to scan."""
    assert CLAUDE_HOME.is_dir(), f"config directory not found: {CLAUDE_HOME} — check CLAUDE_CONFIG_DIR"


def test_root_files_are_compliant():
    """Files at the top of the config directory pass the scan."""
    assert (CLAUDE_HOME / "CLAUDE.md").is_file(), f"CLAUDE.md is missing from {CLAUDE_HOME}"
    errors = [f"{v['path']}: {v['message']}" for v in scan_errors() if "/" not in v["path"]]
    assert not errors, f"Naming errors at the config root {HINT}:\n  " + "\n  ".join(errors)


def test_rules_are_compliant():
    """Every file under _rules/ passes the scan."""
    assert (CLAUDE_HOME / "_rules").is_dir(), missing_area("_rules")
    errors = errors_under("_rules")
    assert not errors, error_report("_rules", errors)


def test_tests_are_compliant():
    """Every file under _tests/ passes the scan."""
    assert (CLAUDE_HOME / "_tests").is_dir(), missing_area("_tests")
    errors = errors_under("_tests")
    assert not errors, error_report("_tests", errors)


def test_templates_are_compliant():
    """Every file under _templates/ passes the scan."""
    assert (CLAUDE_HOME / "_templates").is_dir(), missing_area("_templates")
    errors = errors_under("_templates")
    assert not errors, error_report("_templates", errors)


def test_reference_is_compliant():
    """Every file under _reference/ passes the scan."""
    assert (CLAUDE_HOME / "_reference").is_dir(), missing_area("_reference")
    errors = errors_under("_reference")
    assert not errors, error_report("_reference", errors)


def test_hooks_are_compliant():
    """Every file under hooks/ passes the scan."""
    assert (CLAUDE_HOME / "hooks").is_dir(), missing_area("hooks")
    errors = errors_under("hooks")
    assert not errors, error_report("hooks", errors)


def test_skills_are_compliant():
    """Every file under skills/ passes the scan."""
    assert (CLAUDE_HOME / "skills").is_dir(), missing_area("skills")
    errors = errors_under("skills")
    assert not errors, error_report("skills", errors)


def test_agents_are_compliant():
    """Every file under agents/ passes the scan."""
    assert (CLAUDE_HOME / "agents").is_dir(), missing_area("agents")
    errors = errors_under("agents")
    assert not errors, error_report("agents", errors)


def test_rule_links_are_compliant():
    """Every path-scoped rule link under rules/ passes the scan."""
    assert (CLAUDE_HOME / "rules").is_dir(), missing_area("rules")
    errors = errors_under("rules")
    assert not errors, error_report("rules", errors)


def test_whole_config_has_no_errors():
    """The full scan has no errors, including folders no area test names."""
    errors = [f"{v['path']}: {v['message']}" for v in scan_errors()]
    assert not errors, f"File structure errors {HINT}:\n  " + "\n  ".join(errors)


if __name__ == "__main__":
    # Kept so `python3 _tests/test_file_structure_compliance.py` still runs the scan
    # (see claude_directory_structure/_file_structure_validation.md)
    raise SystemExit(pytest.main([__file__, "-q"]))
