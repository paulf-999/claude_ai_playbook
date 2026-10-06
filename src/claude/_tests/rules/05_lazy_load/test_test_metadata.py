# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-06
# Version:           1.3.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates every test's metadata header against _test_metadata.md.

Each test file, in the config's ``_tests/`` and the repo's ``src/sh/claude/_tests/``,
must open with the full header: banners, fields in order and well-formed values.
Whether the quality score matches the test's own counts is checked by
``test_test_quality_score.py``.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from _shared_paths import CLAUDE_DIR

TESTS_DIR = CLAUDE_DIR / "_tests"
# The repo's shell tooling tests sit beside the config in src/sh/; a live install has none, so this is skipped there
SH_TESTS_DIR = CLAUDE_DIR.parent / "sh" / "claude" / "_tests"
HINT = "— see _rules_lazy_load/testing/_test_metadata.md"
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
    """Return every pytest file under the config's tests directory and, in the repo, the shell tooling tests.

    :return: Paths of ``test_*.py`` files, skipping ``_archived`` folders.
    :rtype: list[Path]
    """
    folders = [TESTS_DIR] + ([SH_TESTS_DIR] if SH_TESTS_DIR.is_dir() else [])
    return sorted(p for folder in folders for p in folder.rglob("test_*.py") if "_archived" not in p.parts)


def label(path: Path) -> str:
    """Name a test file for failure messages, relative to whichever tests folder holds it.

    :param path: A path from :func:`find_test_files`.
    :type path: Path
    :return: The path under ``_tests/``, or under ``src/`` for the shell tooling tests.
    :rtype: str
    """
    base = TESTS_DIR if path.is_relative_to(TESTS_DIR) else CLAUDE_DIR.parent
    return path.relative_to(base).as_posix()


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


def test_scan_finds_find_test_files():
    """The scan finds this file, so a broken glob can't pass silently."""
    files = find_test_files()
    assert len(files) >= 10, f"expected many test files under {TESTS_DIR}, found {len(files)}"
    assert Path(__file__).resolve() in [p.resolve() for p in files], "the scan must include this file"


def test_every_test_file_has_complete_header():
    """Every test file opens with the full metadata header, in order."""
    failures = [f"{label(p)}: {e}" for p in find_test_files() for e in header_errors(p.read_text())]
    assert not failures, "Incomplete metadata headers " + HINT + ":\n  " + "\n  ".join(failures)


def test_valid_header_has_no_errors():
    """A complete, ordered header gives no errors."""
    assert header_errors(VALID_HEADER + ONE_TEST) == [], "the reference header must be valid"


def test_missing_title_is_flagged():
    """A header without the title line is flagged."""
    errors = header_errors(VALID_HEADER.replace(TITLE, "# Metadata") + ONE_TEST)
    assert errors == [f"line 1 must be '{TITLE}'"], f"missing title should be the only error, got {errors}"


def test_missing_field_is_flagged():
    """A header missing the complexity line names that field."""
    source = VALID_HEADER.replace("# Test complexity score: 9/10\n", "") + ONE_TEST
    errors = header_errors(source)
    assert errors == ["missing '# Test complexity score:'"], f"expected one missing-field error, got {errors}"


def test_out_of_order_fields_are_flagged():
    """Swapping two fields is reported as out of order."""
    swapped = VALID_HEADER.replace(
        "# Date created:      2026-10-01\n# Date updated:      2026-10-01\n",
        "# Date updated:      2026-10-01\n# Date created:      2026-10-01\n",
    )
    errors = header_errors(swapped + ONE_TEST)
    assert len(errors) == 1, f"expected one ordering error, got {errors}"
    assert "out of order" in errors[0], f"error should say out of order, got {errors[0]}"


def test_old_field_order_is_flagged():
    """The pre-2026-10-01 order, scores first, is reported as out of order."""
    lines = VALID_HEADER.splitlines()
    old_order = lines[:2] + lines[5:8] + [lines[2], lines[4], lines[3]] + lines[8:]
    errors = header_errors("\n".join(old_order) + ONE_TEST)
    assert errors == [f"fields out of order — expected {', '.join(FIELDS)}"], f"got {errors}"


def test_placeholder_date_is_flagged():
    """``[placeholder]`` is no longer a valid Date updated."""
    source = VALID_HEADER.replace("updated:      2026-10-01", "updated:      [placeholder]") + ONE_TEST
    errors = header_errors(source)
    assert len(errors) == 1, f"expected one value error, got {errors}"
    assert "'Date updated' value '[placeholder]'" in errors[0], f"error should name the field, got {errors[0]}"


def test_bad_values_are_flagged():
    """Two-part versions, out-of-range scores and non Yes/No style values fail."""
    cases = {
        "# Version:           1.0.0": "# Version:           1.0",
        "# Test quality score: 3/10": "# Test quality score: 11/10",
        "# Python style compliant: Yes": "# Python style compliant: Partly",
    }
    for good, bad in cases.items():
        errors = header_errors(VALID_HEADER.replace(good, bad) + ONE_TEST)
        assert len(errors) == 1, f"'{bad}' should give one error, got {errors}"


def test_wrong_banner_is_flagged():
    """A closing banner of hyphens instead of ─ fails."""
    lines = VALID_HEADER.splitlines()
    lines[8] = "# -----"
    errors = header_errors("\n".join(lines) + ONE_TEST)
    assert errors == ["lines 2 and 9 must be '# ─…' banners"], f"got {errors}"


def test_updated_before_created_is_flagged():
    """A Date updated earlier than Date created fails."""
    source = VALID_HEADER.replace("updated:      2026-10-01", "updated:      2026-09-01") + ONE_TEST
    errors = header_errors(source)
    assert errors == ["Date updated 2026-09-01 is earlier than Date created 2026-10-01"], f"got {errors}"


def test_impossible_date_is_flagged():
    """A well-shaped but impossible date fails."""
    errors = date_errors("2026-13-40", "2026-10-01")
    assert len(errors) == 1, f"expected one date error, got {errors}"
    assert errors[0].startswith("invalid date"), f"error should say invalid date, got {errors[0]}"
