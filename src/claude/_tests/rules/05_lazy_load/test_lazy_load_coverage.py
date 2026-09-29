# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# Date created:      2026-09-16
# Version:           1.3.0
# Date updated:      2026-09-29
# ─────────────────────────────────────────────────────────

"""Tests for lazy_load/ discoverability coverage.

Verifies the design constraint that every file in _rules/05_lazy_load/ is
reachable through at least one documented discovery path, per README.md's
own stated design ("Discoverable — included in this README and referenced
from related rules"):
- Hook coverage: the file is explicitly referenced in a hook script.
- README coverage: the file (or an ancestor directory) is named in
  README.md's "What's in this directory" table — the primary discovery
  path for files with no dedicated enforcement hook.
- Transitive coverage: the file lives inside a directory whose index file
  (e.g. dbt/macros.md → dbt.md) is directly referenced by a hook.

Also verifies the inverse: every lazy_load/ path referenced by a hook
resolves to a real file on disk, so hooks cannot silently load nothing.
"""
import re
from pathlib import Path

from _shared_paths import CLAUDE_DIR, HOOKS_DIR
LAZY_LOAD_DIR = CLAUDE_DIR / "_rules" / "05_lazy_load"
README_FILE = LAZY_LOAD_DIR / "README.md"


def _hook_lazy_load_refs() -> set[Path]:
    """Return the set of lazy_load .md paths referenced across all hook scripts.

    :return: Absolute paths to lazy_load .md files mentioned in any hook.
    :rtype: set[Path]
    """
    refs = set()
    for hook in HOOKS_DIR.glob("*.sh"):
        for match in re.finditer(r"lazy_load/([\w/.-]+\.md)", hook.read_text()):
            refs.add(LAZY_LOAD_DIR / match.group(1))
    return refs


def _readme_covered_files_and_dirs() -> tuple[set[Path], set[Path]]:
    """Return lazy_load files and directories named in README.md's index table.

    :return: (covered file paths, covered directory paths) mentioned by name.
    :rtype: tuple[set[Path], set[Path]]
    """
    if not README_FILE.exists():
        return set(), set()
    content = README_FILE.read_text()
    files = {LAZY_LOAD_DIR / m for m in re.findall(r"\b([\w-]+\.md)\b", content)}
    dirs = {LAZY_LOAD_DIR / m for m in re.findall(r"\b([\w-]+)/", content)}
    return files, dirs


def _has_covered_ancestor(file_path: Path, covered: set[Path], covered_dirs: set[Path]) -> bool:
    """Return True if any ancestor directory is covered by a hook index or README entry.

    A directory foo/bar/ is covered when foo/bar.md is hook-referenced (index
    convention), or when "bar/" itself is named in README.md's table.

    :param file_path: The lazy_load .md file to check.
    :type file_path: Path
    :param covered: Set of lazy_load files directly referenced by hooks.
    :type covered: set[Path]
    :param covered_dirs: Set of lazy_load directories named in README.md.
    :type covered_dirs: set[Path]
    :return: Whether the file is transitively reachable via a covered ancestor.
    :rtype: bool
    """
    current = file_path.parent
    while current != LAZY_LOAD_DIR.parent:
        if current in covered_dirs:
            return True
        # The index for directory foo/bar/ is foo/bar.md
        candidate = current.parent / f"{current.name}.md"
        if candidate in covered:
            return True
        current = current.parent
    return False


def test_hook_references_resolve():
    """Every lazy_load/ path referenced by a hook must exist on disk."""
    for path in _hook_lazy_load_refs():
        assert path.exists(), (
            f"Hook references non-existent file: {path.relative_to(CLAUDE_DIR)}"
        )


def test_no_orphaned_lazy_load_files():
    """Every .md in lazy_load/ must be covered by a hook or named in README.md."""
    covered = _hook_lazy_load_refs()
    readme_files, readme_dirs = _readme_covered_files_and_dirs()
    covered |= readme_files
    for md_file in LAZY_LOAD_DIR.rglob("*.md"):
        if md_file.name == "README.md" or md_file in covered:
            continue
        assert _has_covered_ancestor(md_file, covered, readme_dirs), (
            f"Orphaned lazy_load file — no hook, no README.md entry, and no "
            f"covered ancestor: {md_file.relative_to(CLAUDE_DIR)}"
        )


# ── Content-reference orphan detection ──────────────────────────────────
#
# The coverage check above catches files with no *documentation* path
# (hook/README), but has a blind spot: any file inside a directory whose
# top-level index is hook-referenced counts as "covered", even if nothing
# ever actually links to that specific file. That blind spot is exactly
# how 6 near-duplicate orphan files (airflow/airflow.md, dbt/dbt.md,
# jira/jira.md, sql/sql.md, python/python.md, python/python_standards.md)
# went unnoticed until a 2026-09-28 manual audit found and removed them.
# This section adds a stricter, complementary check: every non-entry-point
# .md file must be the actual target of a markdown link or `@./` import
# from some other file in the tree — not just live under a covered folder.

ENTRY_POINT_RELATIVE_PATHS = {
    "authoring_agents.md",
    "automation_controls.md",
    "delegating_to_subagent.md",
    "hooks_decision_framework.md",
    "latency_optimisation.md",
    "mcp_trust_model.md",
    "turn_budgets.md",
    "environment_setup/ohmyzsh_setup.md",
    "style_guide_standards/airflow.md",
    "style_guide_standards/bash.md",
    "style_guide_standards/dbt.md",
    "style_guide_standards/jira.md",
    "style_guide_standards/payroc_engineering_naming_standards.md",
    "style_guide_standards/python.md",
    "style_guide_standards/sql.md",
    "style_guide_standards/infra/ansible.md",
    "style_guide_standards/infra/docker.md",
    "style_guide_standards/infra/terraform.md",
    "style_guide_standards/utilities/datetime.md",
    "style_guide_standards/utilities/makefile.md",
    "style_guide_standards/utilities/mermaid.md",
}

MARKDOWN_LINK_PATTERN = re.compile(r"\]\(([^)#]+\.md)\)")
# Two relative @import spellings are in real use: "@./child.md" and the
# bare "@child.md" / "@dir/child.md" (no "./" prefix) — both resolve
# relative to the importing file's own directory. Neither "@~/..."
# (absolute, handled by test_always_on_reachability.py) nor a bare "@word:"
# prose marker (e.g. "@brief:", no .md suffix) should match here.
RELATIVE_IMPORT_PATTERN = re.compile(r"@(?!~)\.?/?([\w][\w/-]*\.md)")


def _is_entry_point(md_file: Path, lazy_load_dir: Path) -> bool:
    """Return True if md_file is a top-level, on-demand entry point.

    Entry points are loaded by name (like a skill's SKILL.md) rather than
    linked from elsewhere, so they're exempt from needing an incoming
    reference.

    :param md_file: The candidate file.
    :type md_file: Path
    :param lazy_load_dir: The 05_lazy_load/ root.
    :type lazy_load_dir: Path
    :return: Whether md_file is a known entry point.
    :rtype: bool
    """
    try:
        rel = md_file.relative_to(lazy_load_dir).as_posix()
    except ValueError:
        return False
    return rel in ENTRY_POINT_RELATIVE_PATHS


def _outgoing_references(md_file: Path) -> set[Path]:
    """Return the resolved targets of every markdown link and `@./` import in md_file.

    :param md_file: The file to scan for outgoing references.
    :type md_file: Path
    :return: Resolved absolute paths this file links or imports.
    :rtype: set[Path]
    """
    text = md_file.read_text(encoding="utf-8", errors="ignore")
    targets = set()
    for pattern in (MARKDOWN_LINK_PATTERN, RELATIVE_IMPORT_PATTERN):
        for match in pattern.finditer(text):
            candidate = (md_file.parent / match.group(1)).resolve()
            targets.add(candidate)
    return targets


def find_unreferenced_content_files(lazy_load_dir: Path) -> list[Path]:
    """Return non-entry-point .md files never targeted by a link or import.

    :param lazy_load_dir: The 05_lazy_load/ root to scan.
    :type lazy_load_dir: Path
    :return: Files that are neither an entry point nor referenced by anything.
    :rtype: list[Path]
    """
    all_files = [
        f for f in lazy_load_dir.rglob("*.md")
        if f.name != "README.md" and "templates" not in f.relative_to(lazy_load_dir).parts
    ]
    referenced: set[Path] = set()
    for f in all_files:
        referenced |= _outgoing_references(f)

    return [
        f for f in all_files
        if f.resolve() not in referenced and not _is_entry_point(f, lazy_load_dir)
    ]


def test_no_unreferenced_content_files_in_lazy_load():
    """Every non-entry-point lazy_load/ file must be the target of a real link.

    Stricter than test_no_orphaned_lazy_load_files above — catches files
    that are technically "under a covered directory" but that nothing
    actually links to (the exact shape of the 2026-09-28 finding).
    """
    orphans = find_unreferenced_content_files(LAZY_LOAD_DIR)
    assert not orphans, (
        "Unreferenced lazy_load files — not an entry point, and no markdown "
        "link or @./ import anywhere targets them (check whether they're "
        "dead duplicates or just missing a link):\n  "
        + "\n  ".join(str(p.relative_to(CLAUDE_DIR)) for p in orphans)
    )


def test_detector_flags_a_duplicate_named_like_its_parent(tmp_path):
    """Regression: reproduces the exact airflow/airflow.md orphan pattern."""
    sgs = tmp_path / "style_guide_standards"
    sgs.mkdir()
    (sgs / "airflow.md").write_text("# Airflow\n\n- [dag_design.md](airflow/dag_design.md)\n")
    child_dir = sgs / "airflow"
    child_dir.mkdir()
    (child_dir / "dag_design.md").write_text("# DAG design\n")
    (child_dir / "airflow.md").write_text("# Airflow (stale duplicate)\n")

    orphans = find_unreferenced_content_files(tmp_path)

    assert [p.name for p in orphans] == ["airflow.md"]
    assert orphans[0].parent.name == "airflow"


def test_detector_does_not_flag_a_referenced_child(tmp_path):
    """Regression: a child page linked from its parent is not flagged."""
    sgs = tmp_path / "style_guide_standards"
    sgs.mkdir()
    (sgs / "sql.md").write_text("# SQL\n\n@./sql/formatting.md\n")
    child_dir = sgs / "sql"
    child_dir.mkdir()
    (child_dir / "formatting.md").write_text("# Formatting\n")

    orphans = find_unreferenced_content_files(tmp_path)

    assert orphans == []


def test_detector_exempts_entry_point_files(tmp_path):
    """Regression: a known entry point needs no incoming reference at all."""
    sgs = tmp_path / "style_guide_standards"
    sgs.mkdir()
    (sgs / "bash.md").write_text("# Bash\n\nNo inbound links to this file exist anywhere.\n")

    orphans = find_unreferenced_content_files(tmp_path)

    assert orphans == []


def test_detector_exempts_files_under_templates_dir(tmp_path):
    """Regression: templates are copied via prose instruction, not linked — exempt."""
    sgs = tmp_path / "style_guide_standards" / "airflow"
    sgs.mkdir(parents=True)
    templates = sgs / "templates"
    templates.mkdir()
    (templates / "template_dag_readme.md").write_text("# Template\nNever linked to directly.\n")

    orphans = find_unreferenced_content_files(tmp_path)

    assert orphans == []


def test_detector_resolves_relative_import_syntax(tmp_path):
    """Regression: `@./child.md` import syntax is correctly resolved and counted."""
    sgs = tmp_path / "style_guide_standards"
    sgs.mkdir()
    (sgs / "sql.md").write_text("@./sql/cte_style_guide.md\n")
    child_dir = sgs / "sql"
    child_dir.mkdir()
    (child_dir / "cte_style_guide.md").write_text("# CTEs\n")

    refs = _outgoing_references(sgs / "sql.md")

    assert (child_dir / "cte_style_guide.md").resolve() in refs


def test_detector_resolves_markdown_link_syntax(tmp_path):
    """Regression: `[text](child.md)` markdown-link syntax is correctly resolved."""
    sgs = tmp_path / "style_guide_standards"
    sgs.mkdir()
    (sgs / "jira.md").write_text("- [`jira/ticket_conventions.md`](jira/ticket_conventions.md)\n")
    child_dir = sgs / "jira"
    child_dir.mkdir()
    (child_dir / "ticket_conventions.md").write_text("# Tickets\n")

    refs = _outgoing_references(sgs / "jira.md")

    assert (child_dir / "ticket_conventions.md").resolve() in refs


def test_detector_ignores_a_same_named_sibling_when_parent_is_exempt(tmp_path):
    """Regression: parent+orphan sharing a filename doesn't create a false negative.

    The real airflow.md and its orphaned airflow/airflow.md copy share a
    filename — a naive "is this filename referenced anywhere" check would
    wrongly clear the orphan just because its own name matches something
    real elsewhere. Path-based resolution must not make this mistake.
    """
    sgs = tmp_path / "style_guide_standards"
    sgs.mkdir()
    (sgs / "dbt.md").write_text("# dbt\n\nSome other doc mentions `dbt.md` in prose.\n")
    child_dir = sgs / "dbt"
    child_dir.mkdir()
    (child_dir / "dbt.md").write_text("# dbt (stale duplicate)\n")

    orphans = find_unreferenced_content_files(tmp_path)

    assert [p.parent.name for p in orphans] == ["dbt"]
