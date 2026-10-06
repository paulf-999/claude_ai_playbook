# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-06
# Version:           2.2.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Enforces the score minimum in _test_metadata.md on every test file.

A test must score quality ≥9, complexity ≥7 and ``Python style compliant: Yes``.
There are no exemptions: every test met the minimum on 2026-10-01, when the
``BASELINE`` list of older tests was retired. The minimums here must match the
numbers the rule states, so the rule and its enforcer can't drift apart.
"""
from __future__ import annotations

import re
from pathlib import Path

from _shared_paths import LAZY_RULES_DIR
from test_test_metadata import HINT, VALID_HEADER, find_test_files, label

QUALITY_FLOOR = 9
COMPLEXITY_FLOOR = 7
RULE_FILE = LAZY_RULES_DIR / "testing" / "_test_metadata.md"
SCORE_PATTERN = re.compile(
    r"^# Test quality score: (\d+)/10\n"
    r"# Test complexity score: (\d+)/10\n"
    r"# Python style compliant: (Yes|No)$",
    re.M,
)


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


def floor_errors(source: str) -> list[str]:
    """Return how a test file's scores fall short of the minimum.

    :param source: Python source of the test file.
    :type source: str
    :return: One message per missed minimum — empty when the file passes.
    :rtype: list[str]
    """
    found = scores(source)
    if found is None:
        return ["no quality, complexity and style lines to check"]
    quality, complexity, style = found
    errors = []
    if quality < QUALITY_FLOOR:
        errors.append(f"quality {quality}/10 is below the minimum {QUALITY_FLOOR}/10")
    if complexity < COMPLEXITY_FLOOR:
        errors.append(f"complexity {complexity}/10 is below the minimum {COMPLEXITY_FLOOR}/10")
    if style != "Yes":
        errors.append("Python style compliant must be Yes")
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


def test_every_test_meets_the_minimum():
    """Every test file scores quality 9, complexity 7 and style Yes or better."""
    failures = [
        f"{label(path)}: {e}"
        for path in find_test_files()
        for e in floor_errors(path.read_text())
    ]
    assert not failures, "Tests below the score minimum " + HINT + ":\n  " + "\n  ".join(failures)


def test_scan_finds_this_file():
    """The scan covers many test files, including this one, so it can't pass on nothing."""
    files = [p.resolve() for p in find_test_files()]
    assert len(files) >= 40, f"expected the whole test suite, found {len(files)} files"
    assert Path(__file__).resolve() in files, "the scan must include this file"


def test_minimums_match_the_rule():
    """The minimums enforced here are the ones _test_metadata.md states."""
    rule = RULE_FILE.read_text()
    assert f"quality ≥{QUALITY_FLOOR}/10 AND complexity score ≥{COMPLEXITY_FLOOR}/10" in rule, (
        f"_test_metadata.md should require quality ≥{QUALITY_FLOOR} and complexity ≥{COMPLEXITY_FLOOR}"
    )
    assert "`test_test_score_floor.py` fails any test file below quality" in rule, "the rule should name this test"


def test_rule_has_no_exemption_list():
    """The rule no longer describes a BASELINE list of exempt tests."""
    assert "BASELINE" not in RULE_FILE.read_text(), "_test_metadata.md still describes the retired BASELINE list"


def test_scores_reads_header():
    """The three scores are read from the header, and a file with no header has none."""
    assert scores(header(8, 6, "No")) == (8, 6, "No"), "scores should read quality, complexity and style"
    assert scores("print('no header')") is None, "a file with no header has no scores"


def test_file_at_the_minimum_passes():
    """A file at exactly the minimum, or above it, passes."""
    assert floor_errors(header(9, 7, "Yes")) == [], "9/10, 7/10 and Yes meet every minimum"
    assert floor_errors(header(10, 10, "Yes")) == [], "top scores meet every minimum"


def test_low_quality_fails():
    """A file with quality 8 fails."""
    errors = floor_errors(header(8, 9, "Yes"))
    assert errors == ["quality 8/10 is below the minimum 9/10"], f"got {errors}"


def test_low_complexity_fails():
    """A file with complexity 6 fails."""
    errors = floor_errors(header(9, 6, "Yes"))
    assert errors == ["complexity 6/10 is below the minimum 7/10"], f"got {errors}"


def test_style_no_fails():
    """A file that isn't style compliant fails."""
    errors = floor_errors(header(9, 7, "No"))
    assert errors == ["Python style compliant must be Yes"], f"got {errors}"


def test_every_miss_is_reported():
    """A file missing all three minimums gets one message for each."""
    errors = floor_errors(header(5, 3, "No"))
    assert len(errors) == 3, f"expected three errors, got {errors}"


def test_missing_scores_are_reported():
    """A file with no score lines is reported rather than passed."""
    assert floor_errors("x = 1\n") == ["no quality, complexity and style lines to check"], "missing scores must fail"
