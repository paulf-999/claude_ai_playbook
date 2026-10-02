# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-19
# Date updated:      2026-10-02
# Version:           2.0.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Generic orphaned-file detection for every skill under src/claude/skills/.

Every non-structural file in a skill must be named somewhere else in that skill, or in
its out-of-tree tests — how confluence_create_page's dead ``templates/`` folder and
unused pattern files were found (2026-09-19). Every ``reference/`` path SKILL.md names
must exist — how git_create_pr's three broken links were found — and no SKILL.md may
``@``-import a file, so reference files load on demand.

The detectors in ``_skill_orphans.py`` are pure functions over a ``{path: text}`` map,
so each case below is proven on a small in-memory skill with no fixtures.
"""
from __future__ import annotations

from _shared_paths import CLAUDE_DIR, SKILLS_DIR
from _skill_orphans import (
    find_broken_links,
    find_eager_imports,
    find_orphans,
    read_external_tests,
    read_skill,
    skill_dirs,
)

TESTS_DIR = CLAUDE_DIR / "_tests" / "skills"


def test_skills_are_discovered_flat_and_grouped():
    """Discovery finds the real skills, including ones inside a _<group>_skills/ folder."""
    found = skill_dirs(SKILLS_DIR)
    assert found, f"no skills found under {SKILLS_DIR}"
    dotted = [d for d in found if any(p.startswith(".") for p in d.relative_to(SKILLS_DIR).parts)]
    assert not dotted, f"dot folders leaked into discovery: {dotted}"


def test_no_orphaned_files_in_any_skill():
    """Every content file in every real skill is referenced from elsewhere in that skill."""
    failures = [
        f"{root.relative_to(SKILLS_DIR)}/{path}"
        for root in skill_dirs(SKILLS_DIR)
        for path in find_orphans(read_skill(root), read_external_tests(root, TESTS_DIR))
    ]
    assert not failures, "Orphaned skill files — dead content, or just missing a link:\n  " + "\n  ".join(failures)


def test_no_broken_reference_links_in_any_skill():
    """Every reference/ path a real SKILL.md names points at a real file."""
    failures = [
        f"{root.relative_to(SKILLS_DIR)}: {link}"
        for root in skill_dirs(SKILLS_DIR)
        for link in find_broken_links(read_skill(root))
    ]
    assert not failures, "SKILL.md files reference paths that don't exist:\n  " + "\n  ".join(failures)


def test_no_eager_imports_in_any_skill():
    """No real SKILL.md @-imports a file, so reference/ files load on demand."""
    failures = [
        f"{root.relative_to(SKILLS_DIR)}: {line}"
        for root in skill_dirs(SKILLS_DIR)
        for line in find_eager_imports(read_skill(root).get("SKILL.md", ""))
    ]
    assert not failures, "SKILL.md files @-import files — use plain `reference/...` paths:\n  " + "\n  ".join(failures)


def test_detector_flags_an_unreferenced_file():
    """A file named nowhere else is flagged."""
    files = {"SKILL.md": "# Fake\nNo mention here.", "skill.contract.yaml": "name: fake", "orphan_pattern.md": "x"}
    assert find_orphans(files) == ["orphan_pattern.md"], f"got {find_orphans(files)}"


def test_detector_passes_a_referenced_file():
    """A file named in SKILL.md is not flagged."""
    files = {"SKILL.md": "See `used_pattern.md`.", "skill.contract.yaml": "name: fake", "used_pattern.md": "# Used"}
    assert find_orphans(files) == [], f"a referenced file should pass, got {find_orphans(files)}"


def test_detector_exempts_structural_test_and_generated_files():
    """SKILL.md, the contract, README.md, test_*.py, .coverage and __pycache__ never need a link."""
    files = {
        "SKILL.md": "# Fake",
        "skill.contract.yaml": "name: fake",
        "README.md": "# Notes",
        "test_fake_skill.py": "def test_x(): pass",
        ".coverage": "",
        "__pycache__/handler.cpython-39.pyc": "",
    }
    assert find_orphans(files) == [], f"exempt files were flagged: {find_orphans(files)}"


def test_detector_catches_stale_duplicate_folder():
    """The 2026-09-19 finding: a templates/ copy of patterns/ that nothing names is flagged."""
    files = {
        "SKILL.md": "Uses `patterns/real.md`.",
        "skill.contract.yaml": "name: fake",
        "patterns/real.md": "Real pattern.",
        "templates/stale_duplicate.md": "A stale copy.",
    }
    assert find_orphans(files) == ["templates/stale_duplicate.md"], f"got {find_orphans(files)}"


def test_handler_named_only_by_external_test_is_not_orphaned():
    """A handler named only by a test in _tests/skills/<skill>/ still counts as referenced."""
    files = {"SKILL.md": "# Fake", "skill.contract.yaml": "name: fake", "fake_skill_handler.py": "def run(): pass"}
    assert find_orphans(files) == ["fake_skill_handler.py"], "without the external test the handler is an orphan"
    assert find_orphans(files, ["from fake_skill_handler import run"]) == [], "the external test should count"


def test_file_does_not_reference_itself():
    """A file whose stem appears only in its own text is still an orphan."""
    files = {"SKILL.md": "# Fake", "lonely_note.md": "This is lonely_note."}
    assert find_orphans(files) == ["lonely_note.md"], f"self-mention shouldn't count, got {find_orphans(files)}"


def test_broken_link_detector_flags_missing_reference():
    """The 2026-09-19 git_create_pr finding: SKILL.md naming a reference/ file that doesn't exist."""
    files = {"SKILL.md": "See `reference/_implementation.md`."}
    assert find_broken_links(files) == ["reference/_implementation.md"], f"got {find_broken_links(files)}"


def test_broken_link_detector_passes_existing_reference():
    """A reference/ link to a file the skill has is not flagged."""
    files = {"SKILL.md": "See `reference/_implementation.md`.", "reference/_implementation.md": "Real."}
    assert find_broken_links(files) == [], f"an existing reference should pass, got {find_broken_links(files)}"


def test_eager_import_detector_flags_reference_import():
    """An @-import of a reference/ file is flagged, while a plain backticked path is not."""
    assert find_eager_imports("# Fake\n@reference/_x.md\n") == ["@reference/_x.md"], "an @-import should be flagged"
    assert find_eager_imports("See `reference/_x.md`.\n") == [], "a plain path loads on demand and should pass"


def test_eager_import_detector_ignores_fences_and_prose():
    """An @ line in a fenced example, or an email address in prose, isn't an import."""
    assert find_eager_imports("```\n@reference/_x.md\n```\n") == [], "fenced examples must be ignored"
    assert find_eager_imports("~~~\n@reference/_x.md\n~~~\n") == [], "tilde fences must be ignored"
    assert find_eager_imports("Contact team@example.com.\n") == [], "a mid-line @ must be ignored"
