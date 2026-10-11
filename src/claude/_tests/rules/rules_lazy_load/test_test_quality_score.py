# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-02
# Date updated:      2026-10-11
# Version:           2.0.0
# Test quality score: 10/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates that every test header's quality score is the score its file earns.

``_test_metadata.md`` scores quality from four content checks — failure messages,
docstrings, a non-vacuous scan and a test proven to fail — never from how many
tests a file has. Each header must state exactly the score its file earns, so a
header can't drift from the test it describes. Rewritten on 2026-10-11, when the
count-based bands were dropped for rewarding padding.
"""
from __future__ import annotations

import ast
import re

from .test_test_metadata import HINT, ONE_TEST, VALID_HEADER, find_test_files, label

# A failing-input test is named for what it catches, e.g. ``test_missing_title_is_flagged``.
CATCHES = re.compile(r"(flag|reject|fail|catch|detect|missing|invalid|broken|orphan|stale|malformed|bad)")
# A test that walks the real config, as opposed to one fed made-up input through tmp_path.
SCANS = re.compile(r"\.(rglob|glob|iterdir)\(|\b(find|scan)_\w*\(|_files\(|_refs\(")
FIXTURE_ARGS = {"tmp_path", "monkeypatch", "capsys"}


def scans_real_config(test: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Tell whether a test walks the real config rather than made-up input."""
    if FIXTURE_ARGS & {a.arg for a in test.args.args}:
        return False
    return bool(SCANS.search(ast.unparse(test)))


def is_guard(node: ast.Assert) -> bool:
    """Tell whether an assert proves a scan found something.

    Counts ``assert len(x) >= n`` (or ``>``), ``assert any(...)`` and a bare
    ``assert found, "..."`` on a name.
    """
    test = node.test
    if isinstance(test, ast.Compare):
        sized = isinstance(test.left, ast.Call) and getattr(test.left.func, "id", "") == "len"
        return sized and any(isinstance(op, (ast.Gt, ast.GtE)) for op in test.ops)
    if isinstance(test, ast.Call):
        return getattr(test.func, "id", "") == "any"
    return isinstance(test, ast.Name) and node.msg is not None


def content_checks(source: str) -> dict[str, float | bool]:
    """Work out the four quality checks for a test file's source."""
    tree = ast.parse(source)
    tests = [
        n for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test_")
    ]
    asserts = [n for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    return {
        "messages": sum(a.msg is not None for a in asserts) / len(asserts) if asserts else 0.0,
        "docstrings": sum(ast.get_docstring(t) is not None for t in tests) / len(tests) if tests else 0.0,
        "guard": any(is_guard(a) for a in asserts) or not any(scans_real_config(t) for t in tests),
        "fails": any(CATCHES.search(t.name) for t in tests) or "pytest.raises" in source,
    }


def quality_score(source: str) -> int:
    """Return the quality score a test file earns: messages 4, docstrings 3, guard 2, proven to fail 1."""
    checks = content_checks(source)
    earned = int(4 * checks["messages"] + 3 * checks["docstrings"] + 0.5)  # round half up, not to even
    return earned + 2 * checks["guard"] + checks["fails"]


def quality_error(source: str) -> str | None:
    """Return why a header's quality score differs from what its file earns, or ``None`` when it matches."""
    match = re.search(r"^# Test quality score: (\d+)/10$", source, re.M)
    if not match:
        return "no quality score"
    stated, earned = int(match.group(1)), quality_score(source)
    if stated != earned:
        return f"header says {stated}/10, but the file earns {earned}/10 ({content_checks(source)})"
    return None


def test_every_quality_score_matches_what_the_file_earns():
    """Every header states exactly the quality score its file earns."""
    files = find_test_files()
    assert len(files) >= 40, f"expected the whole test suite, found {len(files)} files"
    failures = [f"{label(path)}: {error}" for path in files if (error := quality_error(path.read_text()))]
    assert not failures, "Header quality scores have drifted " + HINT + ":\n  " + "\n  ".join(failures)


def test_full_marks_need_no_minimum_test_count():
    """A file of one clear test that guards a scan and catches bad input earns 10."""
    source = (
        "def test_missing_rule_is_flagged():\n"
        '    """A missing rule is reported."""\n'
        '    assert len(found) >= 1, "scan found nothing"\n'
    )
    assert quality_score(source) == 10, f"one complete test should earn 10, got {content_checks(source)}"


def test_assertions_without_messages_lose_points():
    """Asserts with no failure message cost up to 4 points."""
    source = 'def test_a():\n    """Doc."""\n    assert x\n    assert y\n'
    assert content_checks(source)["messages"] == 0.0, "neither assert carries a message"
    assert quality_score(source) == 5, f"3 for docstrings and 2 for scanning nothing real, got {content_checks(source)}"


def test_missing_docstrings_lose_points():
    """Tests with no docstring cost up to 3 points."""
    source = 'def test_a():\n    assert x == 1, "m"\n\ndef test_b():\n    """Doc."""\n    assert y == 2, "m"\n'
    assert content_checks(source)["docstrings"] == 0.5, "one of two tests has a docstring"
    assert quality_score(source) == 8, (
        f"4 + 1.5 rounds to 6, plus 2 for scanning nothing real, got {content_checks(source)}"
    )


def test_guard_forms_are_recognised():
    """len() >= n, any(...) and a named result with a message all prove a scan found something."""
    for body in ('assert len(files) >= 3, "m"', 'assert any(f.exists() for f in fs), "m"', 'assert files, "m"'):
        source = f"def test_a():\n    files = find_rules()\n    {body}\n"
        assert content_checks(source)["guard"], f"'{body}' should count as a guard"


def test_file_without_a_real_scan_earns_the_guard():
    """Unit tests fed made-up input scan nothing real, so they don't need a non-vacuity guard."""
    source = 'def test_a(tmp_path):\n    """Doc."""\n    assert parse(tmp_path) == [], "m"\n'
    assert content_checks(source)["guard"], "a file with no real-config scan should earn the guard points"


def test_scan_without_a_guard_is_flagged():
    """A test that walks the real config but never proves it found something misses the guard."""
    source = 'def test_a():\n    """Doc."""\n    for f in RULES.rglob("*.md"):\n        assert f.read_text(), "m"\n'
    assert not content_checks(source)["guard"], "an unguarded real scan should not earn the guard points"


def test_bare_truthy_assert_is_not_a_guard():
    """``assert x`` with no message, or ``assert not x``, doesn't prove anything was found."""
    for body in ("assert files", 'assert not failures, "m"', 'assert len(x) == 0, "m"'):
        source = f"def test_a():\n    for f in find_rules():\n        {body}\n"
        assert not content_checks(source)["guard"], f"'{body}' should not count as a guard"


def test_failing_input_is_recognised_by_name_or_raises():
    """A test named for what it catches, or one using pytest.raises, proves the check can fail."""
    assert content_checks("def test_bad_value_is_rejected():\n    pass\n")["fails"], "a '_rejected' name should count"
    assert content_checks("def test_a():\n    with pytest.raises(ValueError):\n        f()\n")["fails"], (
        "pytest.raises should count"
    )
    assert not content_checks("def test_valid_header_accepted():\n    pass\n")["fails"], (
        "a happy-path name shouldn't count"
    )


def test_drifted_header_is_flagged():
    """A header claiming more than its file earns is reported."""
    source = VALID_HEADER.replace("quality score: 3/10", "quality score: 9/10") + ONE_TEST
    error = quality_error(source)
    assert error is not None, "9/10 on a test that earns 5 must be flagged"
    assert "earns 5/10" in error, f"message should name the earned score, got {error}"


def test_matching_header_passes():
    """ONE_TEST earns 5/10: a docstring, no message, nothing real scanned and no failing case."""
    source = VALID_HEADER.replace("quality score: 3/10", "quality score: 5/10") + ONE_TEST
    assert quality_error(source) is None, "a header of 5/10 should match what ONE_TEST earns"


def test_missing_or_malformed_score_is_flagged():
    """A header with no score, or one written as ``3 / 10``, is reported as missing."""
    missing = VALID_HEADER.replace("# Test quality score: 3/10\n", "") + ONE_TEST
    malformed = VALID_HEADER.replace("quality score: 3/10", "quality score: 3 / 10") + ONE_TEST
    assert quality_error(missing) == "no quality score", "a missing score must be reported"
    assert quality_error(malformed) == "no quality score", "a malformed score must not be read as valid"
