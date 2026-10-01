# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-01
# Version:           1.1.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates every test's metadata header against _test_metadata.md.

Each test file must open with the full header — banners, fields in order,
well-formed values — and its quality score must sit within ±1 of the band
its own test-function and assertion counts support, so a header can't drift
from the test it describes.
"""
from __future__ import annotations

import ast
import re
from datetime import date
from pathlib import Path

from _shared_paths import CLAUDE_DIR

TESTS_DIR = CLAUDE_DIR / "_tests"
HINT = "— see _rules/02_claude_standards/testing/_test_metadata.md"
TITLE = "# Test Metadata"
FIELDS = [
    "Date created",
    "Date updated",
    "Version",
    "Test quality score",
    "Test complexity score",
    "Python style compliant",
]
VALUE_PATTERNS = {
    "Date created": r"\d{4}-\d{2}-\d{2}",
    "Date updated": r"\d{4}-\d{2}-\d{2}",
    "Version": r"\d+\.\d+\.\d+",
    "Test quality score": r"(?:10|[1-9])/10",
    "Test complexity score": r"(?:10|[0-9])/10",
    "Python style compliant": r"Yes|No",
}
BANNER = re.compile(r"# ─+")
HEADER_LINES = 9
VALID_HEADER = (
    "# Test Metadata\n"
    "# ─────\n"
    "# Date created:      2026-10-01\n"
    "# Date updated:      2026-10-01\n"
    "# Version:           1.0.0\n"
    "# Test quality score: 3/10\n"
    "# Test complexity score: 9/10\n"
    "# Python style compliant: Yes\n"
    "# ─────\n"
)
ONE_TEST = '\n\ndef test_demo():\n    """Demo."""\n    assert True\n'


def find_test_files() -> list[Path]:
    """Return every pytest file under the tests directory.

    :return: Paths of ``test_*.py`` files, skipping ``_archived`` folders.
    :rtype: list[Path]
    """
    return sorted(p for p in TESTS_DIR.rglob("test_*.py") if "_archived" not in p.parts)


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


def header_errors(source: str) -> list[str]:
    """Return what is wrong with a test file's metadata header.

    :param source: Python source of the test file.
    :type source: str
    :return: One message per problem — empty when the header is complete, in order and well formed.
    :rtype: list[str]
    """
    head = source.splitlines()[:HEADER_LINES]
    if not head or head[0] != TITLE:
        return [f"line 1 must be '{TITLE}'"]
    positions = []
    values = {}
    errors = []
    for field in FIELDS:
        position = next((i for i, line in enumerate(head) if line.startswith(f"# {field}:")), None)
        if position is None:
            errors.append(f"missing '# {field}:'")
            continue
        positions.append(position)
        value = head[position].split(":", 1)[1].strip()
        if re.fullmatch(VALUE_PATTERNS[field], value):
            values[field] = value
        else:
            errors.append(f"'{field}' value '{value}' must match {VALUE_PATTERNS[field]}")
    if positions != sorted(positions):
        errors.append(f"fields out of order — expected {', '.join(FIELDS)}")
    if not errors:
        if not (BANNER.fullmatch(head[1]) and BANNER.fullmatch(head[8])):
            errors.append("lines 2 and 9 must be '# ─…' banners")
        errors.extend(date_errors(values["Date created"], values["Date updated"]))
    return errors


def date_errors(created: str, updated: str) -> list[str]:
    """Return what is wrong with a header's two dates.

    :param created: The ``Date created`` value.
    :type created: str
    :param updated: The ``Date updated`` value.
    :type updated: str
    :return: A message for an impossible date or an update before creation, else empty.
    :rtype: list[str]
    """
    try:
        if date.fromisoformat(updated) < date.fromisoformat(created):
            return [f"Date updated {updated} is earlier than Date created {created}"]
    except ValueError as error:
        return [f"invalid date: {error}"]
    return []


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


def test_scan_finds_find_test_files() -> None:
    """The scan finds this file, so a broken glob can't pass silently."""
    files = find_test_files()
    assert len(files) >= 10, f"expected many test files under {TESTS_DIR}, found {len(files)}"
    assert Path(__file__).resolve() in [p.resolve() for p in files], "the scan must include this file"


def test_every_test_file_has_complete_header() -> None:
    """Every test file opens with the full metadata header, in order."""
    failures = [f"{p.relative_to(TESTS_DIR)}: {e}" for p in find_test_files() for e in header_errors(p.read_text())]
    assert not failures, "Incomplete metadata headers " + HINT + ":\n  " + "\n  ".join(failures)


def test_every_quality_score_matches_counts() -> None:
    """Every header's quality score sits within ±1 of the band its counts support."""
    failures = []
    for path in find_test_files():
        error = quality_error(path.read_text())
        if error:
            failures.append(f"{path.relative_to(TESTS_DIR)}: {error}")
    assert not failures, "Header quality scores have drifted " + HINT + ":\n  " + "\n  ".join(failures)


def test_valid_header_has_no_errors() -> None:
    """A complete, ordered header gives no errors."""
    assert header_errors(VALID_HEADER + ONE_TEST) == [], "the reference header must be valid"


def test_missing_title_is_flagged() -> None:
    """A header without the title line is flagged."""
    errors = header_errors(VALID_HEADER.replace(TITLE, "# Metadata") + ONE_TEST)
    assert errors == [f"line 1 must be '{TITLE}'"], f"missing title should be the only error, got {errors}"


def test_missing_field_is_flagged() -> None:
    """A header missing the complexity line names that field."""
    source = VALID_HEADER.replace("# Test complexity score: 9/10\n", "") + ONE_TEST
    errors = header_errors(source)
    assert errors == ["missing '# Test complexity score:'"], f"expected one missing-field error, got {errors}"


def test_out_of_order_fields_are_flagged() -> None:
    """Swapping two fields is reported as out of order."""
    swapped = VALID_HEADER.replace(
        "# Date created:      2026-10-01\n# Date updated:      2026-10-01\n",
        "# Date updated:      2026-10-01\n# Date created:      2026-10-01\n",
    )
    errors = header_errors(swapped + ONE_TEST)
    assert len(errors) == 1, f"expected one ordering error, got {errors}"
    assert "out of order" in errors[0], f"error should say out of order, got {errors[0]}"


def test_counts_include_class_methods_only_for_tests() -> None:
    """Test methods inside classes count, helper functions don't."""
    source = (
        "def helper():\n    assert True\n\n"
        "class TestDemo:\n    def test_one(self):\n        assert 1\n        assert 2\n"
    )
    functions, asserts = count_tests(source)
    assert functions == 1, f"only test_one is a test function, counted {functions}"
    assert asserts == 3, f"all assert statements count, counted {asserts}"


def test_band_floor_matches_table() -> None:
    """The band floor follows the _test_metadata.md quality table."""
    assert band_floor(10, 15) == 9, "10+ functions and 15+ asserts is the 9–10 band"
    assert band_floor(8, 10) == 7, "8+ functions and 10–14 asserts is the 7–8 band"
    assert band_floor(4, 5) == 5, "4–7 functions and 5–9 asserts is the 5–6 band"
    assert band_floor(1, 1) == 3, "fewer than 4 functions or 5 asserts is the 3–4 band"


def test_band_floor_uses_lower_count() -> None:
    """Many asserts in few functions only reach the function band."""
    assert band_floor(3, 40) == 3, "3 functions cap the band at 3–4, whatever the assert count"


def test_inflated_quality_is_flagged() -> None:
    """A 10/10 header on a one-assert test is reported as drift."""
    source = VALID_HEADER.replace("quality score: 3/10", "quality score: 10/10") + ONE_TEST
    error = quality_error(source)
    assert error is not None, "10/10 on 1 function and 1 assert must be flagged"
    assert "support 3–4" in error, f"message should name the 3–4 band, got {error}"


def test_quality_within_one_of_band_passes() -> None:
    """Scores one either side of the band are allowed."""
    for score in (2, 3, 4, 5):
        source = VALID_HEADER.replace("quality score: 3/10", f"quality score: {score}/10") + ONE_TEST
        assert quality_error(source) is None, f"{score}/10 is within ±1 of the 3–4 band and should pass"


def test_missing_quality_score_is_flagged() -> None:
    """A header with no quality score is reported."""
    source = VALID_HEADER.replace("# Test quality score: 3/10\n", "") + ONE_TEST
    assert quality_error(source) == "no quality score", "a missing quality score must be reported"


def test_old_field_order_is_flagged() -> None:
    """The pre-2026-10-01 order, scores first, is reported as out of order."""
    lines = VALID_HEADER.splitlines()
    old_order = lines[:2] + lines[5:8] + [lines[2], lines[4], lines[3]] + lines[8:]
    errors = header_errors("\n".join(old_order) + ONE_TEST)
    assert errors == [f"fields out of order — expected {', '.join(FIELDS)}"], f"got {errors}"


def test_placeholder_date_is_flagged() -> None:
    """``[placeholder]`` is no longer a valid Date updated."""
    source = VALID_HEADER.replace("updated:      2026-10-01", "updated:      [placeholder]") + ONE_TEST
    errors = header_errors(source)
    assert len(errors) == 1, f"expected one value error, got {errors}"
    assert "'Date updated' value '[placeholder]'" in errors[0], f"error should name the field, got {errors[0]}"


def test_bad_values_are_flagged() -> None:
    """Two-part versions, out-of-range scores and non Yes/No style values fail."""
    cases = {
        "# Version:           1.0.0": "# Version:           1.0",
        "# Test quality score: 3/10": "# Test quality score: 11/10",
        "# Python style compliant: Yes": "# Python style compliant: Partly",
    }
    for good, bad in cases.items():
        errors = header_errors(VALID_HEADER.replace(good, bad) + ONE_TEST)
        assert len(errors) == 1, f"'{bad}' should give one error, got {errors}"


def test_wrong_banner_is_flagged() -> None:
    """A closing banner of hyphens instead of ─ fails."""
    lines = VALID_HEADER.splitlines()
    lines[8] = "# -----"
    errors = header_errors("\n".join(lines) + ONE_TEST)
    assert errors == ["lines 2 and 9 must be '# ─…' banners"], f"got {errors}"


def test_updated_before_created_is_flagged() -> None:
    """A Date updated earlier than Date created fails."""
    source = VALID_HEADER.replace("updated:      2026-10-01", "updated:      2026-09-01") + ONE_TEST
    errors = header_errors(source)
    assert errors == ["Date updated 2026-09-01 is earlier than Date created 2026-10-01"], f"got {errors}"


def test_impossible_date_is_flagged() -> None:
    """A well-shaped but impossible date fails."""
    errors = date_errors("2026-13-40", "2026-10-01")
    assert len(errors) == 1, f"expected one date error, got {errors}"
    assert errors[0].startswith("invalid date"), f"error should say invalid date, got {errors[0]}"
