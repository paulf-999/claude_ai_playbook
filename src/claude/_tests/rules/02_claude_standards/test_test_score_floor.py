# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-01
# Version:           1.0.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Enforces the score minimum in _test_metadata.md on every test file.

A test must score quality ≥9, complexity ≥7 and ``Python style compliant: Yes``.
Files written before the minimum was enforced sit on ``BASELINE`` with their
recorded scores: they may improve but never get worse, and leave the list once
they meet every minimum.
"""
from __future__ import annotations

import re

from test_test_metadata import HINT
from test_test_metadata import TESTS_DIR
from test_test_metadata import VALID_HEADER
from test_test_metadata import find_test_files

QUALITY_FLOOR = 9
COMPLEXITY_FLOOR = 7
SCORE_PATTERN = re.compile(
    r"^# Test quality score: (\d+)/10\n"
    r"# Test complexity score: (\d+)/10\n"
    r"# Python style compliant: (Yes|No)$",
    re.M,
)

# Files below the minimum when it was first enforced, keyed by path under _tests/,
# with their recorded (quality, complexity, style) — remove each as it's fixed
BASELINE = {
    "hooks/enforcement/test_enforcement_writing_style.py": (9, 5, "No"),
    "hooks/response_standards/test_style_guide_response_standards.py": (7, 5, "No"),
    "hooks/response_standards/test_style_guide_response_standards_inject.py": (9, 8, "No"),
    "hooks/test_hook_registry_utils.py": (3, 10, "Yes"),
    "rules/01_essentials/test_guiding_principles.py": (3, 10, "Yes"),
    "rules/01_essentials/test_rule_directory_organisation.py": (7, 6, "Yes"),
    "rules/01_essentials/test_skill_authoring_gate.py": (9, 5, "No"),
    "rules/01_essentials/test_writing_style.py": (5, 9, "Yes"),
    "rules/02_claude_standards/test_always_on_reachability.py": (9, 3, "Yes"),
    "rules/02_claude_standards/test_decision_making.py": (5, 9, "Yes"),
    "rules/02_claude_standards/test_git.py": (5, 9, "Yes"),
    "rules/02_claude_standards/test_portable_paths.py": (9, 3, "Yes"),
    "rules/02_claude_standards/test_security_guardrails.py": (5, 9, "Yes"),
    "rules/02_claude_standards/test_testing.py": (5, 7, "No"),
    "rules/03_authoring_guidelines/test_authoring_rules.py": (5, 9, "Yes"),
    "rules/03_authoring_guidelines/test_authoring_skills.py": (9, 6, "Yes"),
    "rules/05_lazy_load/test_latency_optimisation.py": (5, 9, "Yes"),
    "rules/test_aliases_behavior.py": (5, 9, "Yes"),
    "rules/test_rules_structure.py": (9, 4, "Yes"),
    "settings/test_aliases.py": (5, 9, "No"),
    "settings/test_settings.py": (7, 9, "Yes"),
    "skills/confluence_create_page/test_confluence_create_page_handler.py": (9, 4, "Yes"),
    "skills/confluence_create_page/test_confluence_create_page_timeout.py": (8, 4, "Yes"),
    "skills/jira_create/test_jira_create_handler.py": (9, 7, "No"),
    "skills/test_no_orphaned_skill_files.py": (9, 5, "Yes"),
}


def scores(source: str) -> tuple[int, int, str] | None:
    """Read the three scores from a test file's metadata header.

    :param source: Python source of the test file.
    :type source: str
    :return: ``(quality, complexity, style)``, or ``None`` when the score lines are missing.
    :rtype: tuple[int, int, str] | None
    """
    match = SCORE_PATTERN.search(source)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2)), match.group(3)


def meets_floor(quality: int, complexity: int, style: str) -> bool:
    """Say whether a set of scores meets every minimum.

    :param quality: Test quality score.
    :type quality: int
    :param complexity: Test complexity score.
    :type complexity: int
    :param style: ``Yes`` or ``No``.
    :type style: str
    :return: ``True`` when quality, complexity and style all meet the minimum.
    :rtype: bool
    """
    return quality >= QUALITY_FLOOR and complexity >= COMPLEXITY_FLOOR and style == "Yes"


def floor_errors(source: str, baseline: tuple[int, int, str] | None = None) -> list[str]:
    """Return how a test file's scores break the minimum or its baseline.

    :param source: Python source of the test file.
    :type source: str
    :param baseline: The file's ``BASELINE`` entry, or ``None`` when it isn't listed.
    :type baseline: tuple[int, int, str] | None
    :return: One message per problem — empty when the file passes.
    :rtype: list[str]
    """
    found = scores(source)
    if found is None:
        return ["no quality, complexity and style lines to check"]
    quality, complexity, style = found
    if baseline is None:
        errors = []
        if quality < QUALITY_FLOOR:
            errors.append(f"quality {quality}/10 is below the minimum {QUALITY_FLOOR}/10")
        if complexity < COMPLEXITY_FLOOR:
            errors.append(f"complexity {complexity}/10 is below the minimum {COMPLEXITY_FLOOR}/10")
        if style != "Yes":
            errors.append("Python style compliant must be Yes")
        return errors
    # A listed file that now meets every minimum must leave the list, so it can't slip back
    if meets_floor(quality, complexity, style):
        return ["meets every minimum — remove it from BASELINE"]
    base_quality, base_complexity, base_style = baseline
    errors = []
    if quality < base_quality:
        errors.append(f"quality fell from {base_quality}/10 to {quality}/10")
    if complexity < base_complexity:
        errors.append(f"complexity fell from {base_complexity}/10 to {complexity}/10")
    if base_style == "Yes" and style == "No":
        errors.append("Python style compliant fell from Yes to No")
    return errors


def header(quality: int, complexity: int, style: str) -> str:
    """Build a metadata header with the given scores.

    :param quality: Test quality score.
    :type quality: int
    :param complexity: Test complexity score.
    :type complexity: int
    :param style: ``Yes`` or ``No``.
    :type style: str
    :return: The reference header from ``test_test_metadata`` with these scores swapped in.
    :rtype: str
    """
    return (
        VALID_HEADER.replace("quality score: 3/10", f"quality score: {quality}/10")
        .replace("complexity score: 9/10", f"complexity score: {complexity}/10")
        .replace("compliant: Yes", f"compliant: {style}")
    )


def test_every_test_meets_floor_or_baseline():
    """Every test file meets the minimum, or holds its BASELINE scores."""
    failures = []
    for path in find_test_files():
        key = path.relative_to(TESTS_DIR).as_posix()
        failures.extend(f"{key}: {e}" for e in floor_errors(path.read_text(), BASELINE.get(key)))
    assert not failures, "Tests below the score minimum " + HINT + ":\n  " + "\n  ".join(failures)


def test_every_baseline_path_exists():
    """Every BASELINE path is a real test file, so deleted or renamed files leave the list."""
    found = {p.relative_to(TESTS_DIR).as_posix() for p in find_test_files()}
    missing = sorted(set(BASELINE) - found)
    assert not missing, "BASELINE lists files that no longer exist — remove them:\n  " + "\n  ".join(missing)


def test_baseline_entries_are_below_floor():
    """Every BASELINE entry misses at least one minimum, so the list holds no free passes."""
    free = [key for key, entry in BASELINE.items() if meets_floor(*entry)]
    assert not free, f"BASELINE entries already meet the minimum: {free}"


def test_scores_reads_header():
    """The three scores are read from the header."""
    assert scores(header(8, 6, "No")) == (8, 6, "No"), "scores should read quality, complexity and style"
    assert scores("print('no header')") is None, "a file with no header has no scores"


def test_unlisted_file_at_floor_passes():
    """An unlisted file at exactly the minimum passes."""
    assert floor_errors(header(9, 7, "Yes")) == [], "9/10, 7/10 and Yes meet every minimum"
    assert floor_errors(header(10, 10, "Yes")) == [], "top scores meet every minimum"


def test_unlisted_low_quality_fails():
    """An unlisted file with quality 8 fails."""
    errors = floor_errors(header(8, 9, "Yes"))
    assert errors == ["quality 8/10 is below the minimum 9/10"], f"got {errors}"


def test_unlisted_low_complexity_fails():
    """An unlisted file with complexity 6 fails."""
    errors = floor_errors(header(9, 6, "Yes"))
    assert errors == ["complexity 6/10 is below the minimum 7/10"], f"got {errors}"


def test_unlisted_style_no_fails():
    """An unlisted file that isn't style compliant fails."""
    errors = floor_errors(header(9, 7, "No"))
    assert errors == ["Python style compliant must be Yes"], f"got {errors}"


def test_unlisted_file_reports_every_miss():
    """An unlisted file missing all three minimums gets one message for each."""
    errors = floor_errors(header(5, 3, "No"))
    assert len(errors) == 3, f"expected three errors, got {errors}"


def test_listed_file_at_baseline_passes():
    """A listed file holding its recorded scores passes."""
    assert floor_errors(header(5, 9, "No"), (5, 9, "No")) == [], "unchanged scores must pass"


def test_listed_file_improving_but_below_floor_passes():
    """A listed file that improves but still misses a minimum passes."""
    assert floor_errors(header(7, 9, "No"), (5, 9, "No")) == [], "a higher quality is allowed"
    assert floor_errors(header(5, 9, "Yes"), (5, 6, "No")) == [], "better style and complexity are allowed"


def test_listed_quality_regression_fails():
    """A listed file whose quality drops below its baseline fails."""
    errors = floor_errors(header(4, 9, "Yes"), (5, 9, "Yes"))
    assert errors == ["quality fell from 5/10 to 4/10"], f"got {errors}"


def test_listed_complexity_regression_fails():
    """A listed file whose complexity drops below its baseline fails."""
    errors = floor_errors(header(9, 4, "Yes"), (9, 5, "Yes"))
    assert errors == ["complexity fell from 5/10 to 4/10"], f"got {errors}"


def test_listed_style_regression_fails():
    """A listed file whose style falls from Yes to No fails."""
    errors = floor_errors(header(5, 9, "No"), (5, 9, "Yes"))
    assert errors == ["Python style compliant fell from Yes to No"], f"got {errors}"


def test_stale_entry_fails():
    """A listed file that now meets every minimum must be removed from BASELINE."""
    errors = floor_errors(header(9, 7, "Yes"), (5, 9, "No"))
    assert errors == ["meets every minimum — remove it from BASELINE"], f"got {errors}"


def test_missing_scores_are_reported():
    """A file with no score lines is reported whether or not it's listed."""
    assert floor_errors("x = 1\n") == ["no quality, complexity and style lines to check"], "unlisted"
    assert floor_errors("x = 1\n", (5, 9, "No")) == ["no quality, complexity and style lines to check"], "listed"
