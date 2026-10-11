# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-11
# Date updated:      2026-10-11
# Version:           1.1.0
# Test quality score: 10/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Fails when a test pins an instructional rule's wording instead of checking structure.

A wording-pinning test reads a real file and asserts a literal phrase is (or isn't) in it,
so it breaks on every legitimate rewording and never catches a real bug. 37 such tests
were deleted on 2026-10-11; this guard stops new ones, per ``_testing_anti_patterns.md``.

- **Flagged:** in a ``test_*`` function that reads a file, a literal string checked with
  ``in``/``not in`` or passed as the pattern to ``re.search``/``re.match``/``re.fullmatch``.
- **Prose only:** the literal must be two or more words, so a key, marker or file pointer
  (``permissions``, ``**Purpose:**``, ``_commits.md``) passes, as does a pattern using regex syntax.
- **Allowed:** a test that builds its input under ``tmp_path``, one that reads no file, and a
  line tagged ``# wording-check: <reason>``.

It also fails on a finished-migration check, ``assert not <path>.exists()`` (or ``is_file``/``is_dir``)
outside ``tmp_path``, which guards a move that already happened; tag a kept one ``# absence-check: <reason>``.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

from _shared_paths import CLAUDE_DIR

TESTS_DIR = CLAUDE_DIR / "_tests"
TAG = re.compile(r"#\s*wording-check:\s*\S")
ABSENCE_TAG = re.compile(r"#\s*absence-check:\s*\S")
PATH_CHECKS = {"exists", "is_file", "is_dir"}
REGEX_SYNTAX = re.compile(r"[\\^$*+?()\[\]{}|]")
READ_CALLS = {"read_text", "read_bytes", "open"}
PATTERN_CALLS = {"search", "match", "fullmatch"}


def _called_names(node: ast.AST) -> set[str]:
    """Return the bare or attribute name of every call inside a node."""
    names = set()
    for call in (n for n in ast.walk(node) if isinstance(n, ast.Call)):
        func = call.func
        names.add(func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", ""))
    return names


def _reader_helpers(tree: ast.Module) -> set[str]:
    """Return the module's helper functions that read a file, directly or through another helper."""
    helpers = {f.name: _called_names(f) for f in tree.body if isinstance(f, ast.FunctionDef)}
    readers: set[str] = set()
    while new := {name for name, calls in helpers.items() if name not in readers and calls & (READ_CALLS | readers)}:
        readers |= new
    return readers


def _is_wording(phrase: str, pattern: bool) -> bool:
    """Say whether a literal is prose wording rather than a key, marker, file pointer or regex.

    :param phrase: The literal string checked against file text.
    :param pattern: True when the literal is a ``re`` pattern rather than an ``in`` operand.
    :return: True for two or more words that, as a pattern, use no regex syntax.
    """
    words = phrase.strip()
    return bool(re.search(r"\s", words)) and not (pattern and REGEX_SYNTAX.search(words))


def _strings(node: ast.AST | None) -> list[str]:
    """Return the string constants a node is, or holds as a list or tuple."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return [e.value for e in node.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
    return []


def _literal_names(tree: ast.Module, test: ast.FunctionDef) -> dict[str, list[str]]:
    """Map each name in a test to the literal strings it holds.

    Covers module constants, local assignments and loop variables over literal lists.
    """
    names: dict[str, list[str]] = {}
    for scope in (tree.body, list(ast.walk(test))):
        for node in scope:
            if isinstance(node, ast.Assign) and _strings(node.value):
                names.update({t.id: _strings(node.value) for t in node.targets if isinstance(t, ast.Name)})
    for loop in (n for n in ast.walk(test) if isinstance(n, ast.For) and isinstance(n.target, ast.Name)):
        source = loop.iter
        values = names.get(source.id, []) if isinstance(source, ast.Name) else _strings(source)
        if values:
            names[loop.target.id] = values
    return names


def _phrases(node: ast.AST, literals: dict[str, list[str]]) -> list[str]:
    """Return the prose phrases a compare or pattern call checks, if any."""
    if isinstance(node, ast.Compare) and isinstance(node.ops[0], (ast.In, ast.NotIn)):
        left = node.left
        found = literals.get(left.id, []) if isinstance(left, ast.Name) else _strings(left)
        return [phrase for phrase in found if _is_wording(phrase, pattern=False)]
    func = getattr(node, "func", None)
    if isinstance(func, ast.Attribute) and func.attr in PATTERN_CALLS and getattr(func.value, "id", "") == "re":
        return [phrase for phrase in _strings(node.args[0]) if _is_wording(phrase, pattern=True)] if node.args else []
    return []


def pinned_phrases(source: str) -> list[str]:
    """Return ``"test_name:line: phrase"`` for every untagged wording check in a test file's source.

    :param source: A test module's Python source.
    :return: One entry per flagged phrase, empty when the file pins no wording.
    """
    tree = ast.parse(source)
    lines = source.splitlines()
    readers = _reader_helpers(tree)
    hits = []
    for test in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")):
        if "tmp_path" in {a.arg for a in test.args.args} or not _called_names(test) & (READ_CALLS | readers):
            continue
        literals = _literal_names(tree, test)
        for node in ast.walk(test):
            span = lines[getattr(node, "lineno", 1) - 1:getattr(node, "end_lineno", 0)]
            tagged = any(TAG.search(line) for line in span)
            hits += [f"{test.name}:{node.lineno}: {phrase!r}" for phrase in _phrases(node, literals) if not tagged]
    return hits


def absence_checks(source: str) -> list[str]:
    """Return ``"test_name:line: path"`` for every untagged check that a real config path stays absent.

    :param source: A test module's Python source.
    :return: One entry per ``assert not <path>.exists()``-style check outside ``tmp_path``.
    """
    lines = source.splitlines()
    hits = []
    for test in (n for n in ast.walk(ast.parse(source)) if isinstance(n, ast.FunctionDef)):
        if not test.name.startswith("test_") or "tmp_path" in {a.arg for a in test.args.args}:
            continue
        for node in (n for n in ast.walk(test) if isinstance(n, ast.Assert) and isinstance(n.test, ast.UnaryOp)):
            call = node.test.operand
            checks_path = isinstance(call, ast.Call) and getattr(call.func, "attr", "") in PATH_CHECKS
            span = lines[node.lineno - 1:node.end_lineno]
            if isinstance(node.test.op, ast.Not) and checks_path and not any(ABSENCE_TAG.search(x) for x in span):
                hits.append(f"{test.name}:{node.lineno}: {ast.unparse(call)}")
    return hits


def scan(root: Path, finder=pinned_phrases) -> dict[str, list[str]]:
    """Return a finder's hits for every test file under a folder, keyed by relative path.

    :param root: A tests folder, such as ``_tests/`` or a backup of it.
    :param finder: :func:`pinned_phrases` or :func:`absence_checks`.
    :return: Only files with at least one hit.
    """
    found = {}
    for path in sorted(root.rglob("test_*.py")):
        if "_archived" not in path.parts and (hits := finder(path.read_text())):
            found[path.relative_to(root).as_posix()] = hits
    return found


def test_no_test_pins_rule_wording():
    """No test in _tests/ pins a literal phrase from a real file without a wording-check tag."""
    assert len(list(TESTS_DIR.rglob("test_*.py"))) >= 40, f"expected the whole suite under {TESTS_DIR}"
    found = scan(TESTS_DIR)
    report = "\n  ".join(f"{name}: {hit}" for name, hits in found.items() for hit in hits)
    assert not found, (
        "These tests pin rule wording — delete them, check structure instead, or tag a kept "
        f"incident record with '# wording-check: <reason>' (see _testing_anti_patterns.md):\n  {report}"
    )


def test_no_test_guards_a_finished_migration():
    """No test in _tests/ asserts a real config path stays absent without an absence-check tag."""
    found = scan(TESTS_DIR, absence_checks)
    report = "\n  ".join(f"{name}: {hit}" for name, hits in found.items() for hit in hits)
    assert not found, (
        "These tests guard a migration that already finished — delete them, or tag a kept one "
        f"with '# absence-check: <reason>' (see _testing_anti_patterns.md):\n  {report}"
    )


READS = 'RULE = Path("rule.md")\n\n\ndef test_x():\n    content = RULE.read_text()\n'


def test_phrase_in_read_file_is_flagged():
    """A literal phrase checked against a real file's text is flagged, via in, not in, re.search or a loop."""
    for check in ('    assert "Detect early" in content\n', '    assert "a 70% threshold" not in content\n',
                  '    assert re.search(r"stop after each phase", content)\n',
                  '    for word in ("absolute requirement", "never skip"):\n        assert word not in content\n'):
        assert pinned_phrases(READS + check), f"wording check not flagged: {check.strip()}"


def test_tagged_phrase_is_allowed():
    """A wording check on a line tagged '# wording-check: <reason>' passes, but a bare tag does not."""
    tagged = READS + '    assert "Incident (2026-09-19)" in content  # wording-check: incident record\n'
    bare = READS + '    assert "Incident (2026-09-19)" in content  # wording-check:\n'
    assert pinned_phrases(tagged) == [], "a tagged incident check should be allowed"
    assert pinned_phrases(bare), "a tag with no reason should not exempt the check"


def test_single_tokens_and_regex_are_allowed():
    """Keys, markers, pointers and real regex patterns pass, but a sentence holding a pointer is flagged."""
    assert pinned_phrases(READS + '    assert "_concurrent_sessions.md" in content\n') == [], "file name flagged"
    assert pinned_phrases(READS + '    assert "/claude_usage_standards/x.md" in content\n') == [], "path flagged"
    assert pinned_phrases(READS + '    assert "`test_x.py` fails any file" in content\n'), "sentence missed"
    assert pinned_phrases(READS + '    assert "**Purpose:**" in content\n') == [], "a one-word marker was flagged"
    assert pinned_phrases(READS + '    assert re.search(r"^# (.+)", content)\n') == [], "a regex pattern was flagged"


def test_tmp_path_input_and_no_file_read_are_allowed():
    """A test that builds input under tmp_path, or reads no file at all, is never flagged."""
    tmp = READS.replace("def test_x():", "def test_x(tmp_path):") + '    assert "Missing" in content\n'
    no_read = 'def test_x():\n    errors = validate("bad")\n    assert "missing header" in errors[0]\n'
    assert pinned_phrases(tmp) == [], "a tmp_path test should be allowed"
    assert pinned_phrases(no_read) == [], "a validator unit test that reads no file should be allowed"


def test_finished_migration_check_is_flagged():
    """An absent-path assert on the real config is flagged, unless tagged or built under tmp_path."""
    check = '    assert not (RULES_DIR / "behaviour").is_dir()\n'
    assert absence_checks(f"def test_x():\n{check}"), "a finished-migration check was not flagged"
    tagged = f"def test_x():\n{check.rstrip()}  # absence-check: still possible\n"
    assert absence_checks(tagged) == [], "a tagged absence check should be allowed"
    assert absence_checks(f"def test_x(tmp_path):\n{check}") == [], "a tmp_path test should be allowed"
    assert absence_checks('def test_x():\n    assert RULE.exists(), "x"\n') == [], "a presence check was flagged"
