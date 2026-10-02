# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-02
# Date updated:      2026-10-02
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates that every test header's quality score matches the test it describes.

``_test_metadata.md`` scores quality by counting test functions and assertions. Each
header's score must sit within the band its own counts support (one below, up to one
above the band), so a header can't drift from the test it describes. Split out of
``test_test_metadata.py`` on 2026-10-02, which keeps the header-structure checks.
"""
from __future__ import annotations

import ast
import re

from test_test_metadata import HINT, ONE_TEST, VALID_HEADER, find_test_files, label


def count_tests(source: str) -> tuple[int, int]:
    """Count test functions and assert statements in a test file.

    :param source: Python source of the test file.
    :type source: str
    :return: Number of ``test_*`` functions and number of ``assert`` statements.
    :rtype: tuple[int, int]
    """
    tree = ast.parse(source)
    functions = sum(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    asserts = sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
    return functions, asserts


def band_floor(functions: int, asserts: int) -> int:
    """Return the lowest score of the quality band the counts support.

    The band is the lower of the assertion band and the function band in the
    ``_test_metadata.md`` table, so both counts must meet a band to reach it.

    :param functions: Number of test functions.
    :type functions: int
    :param asserts: Number of assert statements.
    :type asserts: int
    :return: 9, 7, 5 or 3 — the first score of the matching band.
    :rtype: int
    """
    assert_band = 9 if asserts >= 15 else 7 if asserts >= 10 else 5 if asserts >= 5 else 3
    function_band = 9 if functions >= 10 else 7 if functions >= 8 else 5 if functions >= 4 else 3
    return min(assert_band, function_band)


def quality_error(source: str) -> str | None:
    """Return why a header's quality score doesn't match the test's counts.

    :param source: Python source of the test file.
    :type source: str
    :return: A message when the score is missing or outside the band ±1, else ``None``.
    :rtype: str | None
    """
    match = re.search(r"^# Test quality score: (\d+)/10$", source, re.M)
    if not match:
        return "no quality score"
    score = int(match.group(1))
    functions, asserts = count_tests(source)
    floor = band_floor(functions, asserts)
    if not floor - 1 <= score <= floor + 2:
        return f"quality {score}/10, but {functions} functions and {asserts} asserts support {floor}–{floor + 1}"
    return None


def test_every_quality_score_matches_counts():
    """Every header's quality score sits within ±1 of the band its counts support."""
    failures = []
    for path in find_test_files():
        error = quality_error(path.read_text())
        if error:
            failures.append(f"{label(path)}: {error}")
    assert not failures, "Header quality scores have drifted " + HINT + ":\n  " + "\n  ".join(failures)


def test_counts_include_class_methods_only_for_tests():
    """Test methods inside classes count, helper functions don't."""
    source = (
        "def helper():\n    assert True\n\n"
        "class TestDemo:\n    def test_one(self):\n        assert 1\n        assert 2\n"
    )
    functions, asserts = count_tests(source)
    assert functions == 1, f"only test_one is a test function, counted {functions}"
    assert asserts == 3, f"all assert statements count, counted {asserts}"


def test_band_floor_matches_table():
    """The band floor follows the _test_metadata.md quality table."""
    assert band_floor(10, 15) == 9, "10+ functions and 15+ asserts is the 9–10 band"
    assert band_floor(8, 10) == 7, "8+ functions and 10–14 asserts is the 7–8 band"
    assert band_floor(4, 5) == 5, "4–7 functions and 5–9 asserts is the 5–6 band"
    assert band_floor(1, 1) == 3, "fewer than 4 functions or 5 asserts is the 3–4 band"


def test_band_floor_uses_lower_count():
    """Many asserts in few functions only reach the function band."""
    assert band_floor(3, 40) == 3, "3 functions cap the band at 3–4, whatever the assert count"


def test_inflated_quality_is_flagged():
    """A 10/10 header on a one-assert test is reported as drift."""
    source = VALID_HEADER.replace("quality score: 3/10", "quality score: 10/10") + ONE_TEST
    error = quality_error(source)
    assert error is not None, "10/10 on 1 function and 1 assert must be flagged"
    assert "support 3–4" in error, f"message should name the 3–4 band, got {error}"


def test_quality_within_one_of_band_passes():
    """Scores one either side of the band are allowed."""
    for score in (2, 3, 4, 5):
        source = VALID_HEADER.replace("quality score: 3/10", f"quality score: {score}/10") + ONE_TEST
        assert quality_error(source) is None, f"{score}/10 is within ±1 of the 3–4 band and should pass"


def test_missing_quality_score_is_flagged():
    """A header with no quality score is reported."""
    source = VALID_HEADER.replace("# Test quality score: 3/10\n", "") + ONE_TEST
    assert quality_error(source) == "no quality score", "a missing quality score must be reported"


def test_deflated_quality_is_flagged():
    """A score more than one below the band, such as 1/10 on the 3–4 band, is reported."""
    source = VALID_HEADER.replace("quality score: 3/10", "quality score: 1/10") + ONE_TEST
    assert quality_error(source) is not None, "1/10 is two below the 3–4 band and must be flagged"


def test_score_past_the_allowance_is_flagged():
    """6/10 on the 3–4 band is one past the allowed 5/10, so it's reported."""
    source = VALID_HEADER.replace("quality score: 3/10", "quality score: 6/10") + ONE_TEST
    assert quality_error(source) is not None, "6/10 on 1 function and 1 assert must be flagged"


def test_async_test_functions_count():
    """``async def test_*`` functions count as tests, like plain ones."""
    functions, asserts = count_tests("async def test_a():\n    assert 1\n\nasync def helper():\n    assert 2\n")
    assert functions == 1, f"only the async test_a is a test function, counted {functions}"
    assert asserts == 2, f"both assert statements count, counted {asserts}"


def test_malformed_score_line_counts_as_missing():
    """A score line in the wrong format, such as ``9 / 10``, is treated as no score."""
    source = VALID_HEADER.replace("quality score: 3/10", "quality score: 3 / 10") + ONE_TEST
    assert quality_error(source) == "no quality score", "a malformed score must not be read as valid"
