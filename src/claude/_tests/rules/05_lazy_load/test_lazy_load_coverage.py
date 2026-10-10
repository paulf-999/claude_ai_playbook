# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-16
# Date updated:      2026-10-10
# Version:           2.4.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests for lazy_load/ discoverability coverage.

Verifies the design constraint that every file in _rules_lazy_load/ is
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
from __future__ import annotations

import re
from pathlib import Path

from _shared_paths import (
    CLAUDE_DIR,
    HOOKS_DIR,
    LAZY_RULES_DIR,
    LAZY_RULES_NAME,
    RULES_DIR,
    STYLE_GUIDES_NAME,
    installed_rule_files,
    native_rule_files,
    on_demand_rule_files,
    path_scoped_rule_files,
    resolve_config_path,
    resolve_link,
)

LAZY_LOAD_DIR = LAZY_RULES_DIR
# Folders under _rules_lazy_load/ that hold indexes or ledgers rather than rules
NON_RULE_FOLDERS = {"_tier_readmes", "_learned"}
README_FILE = LAZY_LOAD_DIR / "README.md"


def lazy_files() -> dict[str, Path]:
    """Return each on-demand file's path inside the installed _rules_lazy_load/, mapped to where it is on disk."""
    prefix = f"{LAZY_RULES_NAME}/"
    return {rel[len(prefix):]: p for rel, p in installed_rule_files(CLAUDE_DIR).items() if rel.startswith(prefix)}


def _hook_lazy_load_refs() -> set[str]:
    """Return the lazy_load .md paths referenced across all hook scripts.

    :return: Paths inside _rules_lazy_load/ mentioned in any hook.
    :rtype: set[str]
    """
    refs = set()
    for hook in HOOKS_DIR.glob("*.sh"):
        refs |= set(re.findall(r"lazy_load/([\w/.-]+\.md)", hook.read_text()))
    return refs


def _readme_covered_files_and_dirs() -> tuple[set[str], set[str]]:
    """Return lazy_load files and directories named in README.md's index table.

    :return: (covered file paths, covered directory paths) inside _rules_lazy_load/, mentioned by name.
    :rtype: tuple[set[str], set[str]]
    """
    if not README_FILE.exists():
        return set(), set()
    content = README_FILE.read_text()
    return set(re.findall(r"\b([\w-]+\.md)\b", content)), set(re.findall(r"\b([\w-]+)/", content))


def _has_covered_ancestor(rel: str, covered: set[str], covered_dirs: set[str]) -> bool:
    """Return True if any ancestor directory is covered by a hook index or README entry.

    A directory foo/bar/ is covered when foo/bar.md is hook-referenced (index
    convention), or when "bar/" itself is named in README.md's table.

    :param rel: The file's path inside _rules_lazy_load/.
    :type rel: str
    :param covered: Lazy_load files directly referenced by hooks or README.md.
    :type covered: set[str]
    :param covered_dirs: Lazy_load directories named in README.md.
    :type covered_dirs: set[str]
    :return: Whether the file is transitively reachable via a covered ancestor.
    :rtype: bool
    """
    # The index for directory foo/bar/ is foo/bar.md
    return any(folder.as_posix() in covered_dirs or f"{folder.as_posix()}.md" in covered
               for folder in list(Path(rel).parents)[:-1])


def test_hook_references_resolve():
    """Every lazy_load/ path referenced by a hook must exist on disk."""
    for rel in _hook_lazy_load_refs():
        assert resolve_config_path(CLAUDE_DIR, f"{LAZY_RULES_NAME}/{rel}").exists(), (
            f"Hook references non-existent file: {LAZY_RULES_NAME}/{rel}"
        )


def test_no_orphaned_lazy_load_files():
    """Every .md in lazy_load/ must be covered by a hook or named in README.md."""
    covered = _hook_lazy_load_refs()
    readme_files, readme_dirs = _readme_covered_files_and_dirs()
    covered |= readme_files
    for rel in lazy_files():
        if Path(rel).parts[0] in NON_RULE_FOLDERS or Path(rel).name == "README.md" or rel in covered:
            continue
        assert _has_covered_ancestor(rel, covered, readme_dirs), (
            f"Orphaned lazy_load file — no hook, no README.md entry, and no covered ancestor: {rel}"
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

# Path-scoped entry points (sql.md, testing.md, ...) live in rules/04_path_scoped/ and load through paths:,
# so only the on-demand entry points are listed here, by installed path.
ENTRY_POINT_RELATIVE_PATHS = {
    "_rules_lazy_load/automation_lazy_load/automation_controls.md",
    "_rules_lazy_load/efficiency_lazy_load/delegating_to_subagent.md",
    "_rules_lazy_load/automation_lazy_load/hooks_decision_framework.md",
    "_rules_lazy_load/efficiency_lazy_load/latency_optimisation.md",
    "_rules_lazy_load/mcp_trust_model.md",
    "_rules_lazy_load/efficiency_lazy_load/response_standards_enforcement.md",
    "_rules_lazy_load/automation_lazy_load/turn_budgets.md",
    "_rules_lazy_load/org.md",
    "_style_guide_standards/jira.md",
    "_style_guide_standards/utilities/datetime.md",
}

MARKDOWN_LINK_PATTERN = re.compile(r"\]\(([^)#]+\.md)\)")
# Two relative @import spellings are in real use: "@./child.md" and the
# bare "@child.md" / "@dir/child.md" (no "./" prefix) — both resolve
# relative to the importing file's own directory. Neither "@~/..."
# (absolute, handled by test_always_on_reachability.py) nor a bare "@word:"
# prose marker (e.g. "@brief:", no .md suffix) should match here.
RELATIVE_IMPORT_PATTERN = re.compile(r"@(?!~)\.?/?([\w][\w/-]*\.md)")
# "**Read on demand:**" pointers name a child by its full config path, e.g.
# `~/.claude/_rules_lazy_load/x/_child.md` — the convention for on-demand children.
READ_ON_DEMAND_PATTERN = re.compile(r"`~/[^/`\s]+/((?:rules|_rules_lazy_load)/[^`\s]+\.md)`")
ROOT_NAMES = ("rules", LAZY_RULES_NAME, STYLE_GUIDES_NAME)


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
            targets.add(resolve_link(md_file, match.group(1)))
    # The config folder: above rules/, or above a _rules_lazy_load/ that sits beside it
    roots = [p for p in md_file.parents if p.name in ROOT_NAMES]
    if roots:
        config_dir = roots[-1].parent
        for match in READ_ON_DEMAND_PATTERN.finditer(text):
            targets.add(resolve_config_path(config_dir, match.group(1)).resolve())
    return targets


def find_unreferenced_content_files(
    lazy_load_dir: Path, other_sources: tuple[Path, ...] = (), files: dict[str, Path] | None = None
) -> list[Path]:
    """Return non-entry-point .md files never targeted by a link or import.

    :param lazy_load_dir: The _rules_lazy_load/ root to scan.
    :type lazy_load_dir: Path
    :param other_sources: More files whose links count, e.g. path-scoped parents in rules/.
    :type other_sources: tuple[Path, ...]
    :param files: The on-demand files keyed by installed path, when they don't all sit under one folder.
    :type files: dict[str, Path] | None
    :return: Files that are neither an entry point nor referenced by anything.
    :rtype: list[Path]
    """
    if files is None:
        files = {f.relative_to(lazy_load_dir).as_posix(): f for f in lazy_load_dir.rglob("*.md")}
    candidates = {
        rel: f for rel, f in files.items()
        if f.name != "README.md" and "templates" not in Path(rel).parts and not NON_RULE_FOLDERS & set(Path(rel).parts)
    }
    referenced: set[Path] = set()
    for f in [*candidates.values(), *other_sources]:
        referenced |= _outgoing_references(f)

    return [
        f for rel, f in candidates.items()
        if f.resolve() not in referenced and rel not in ENTRY_POINT_RELATIVE_PATHS
    ]


def test_no_unreferenced_content_files_in_lazy_load():
    """Every non-entry-point lazy_load/ file must be the target of a real link.

    Stricter than test_no_orphaned_lazy_load_files above — catches files
    that are technically "under a covered directory" but that nothing
    actually links to (the exact shape of the 2026-09-28 finding).
    """
    sources = tuple(native_rule_files(RULES_DIR)) + tuple(path_scoped_rule_files(CLAUDE_DIR))
    orphans = find_unreferenced_content_files(LAZY_LOAD_DIR, sources, on_demand_rule_files(CLAUDE_DIR))
    assert not orphans, (
        "Unreferenced lazy_load files — not an entry point, and no markdown "
        "link or @./ import anywhere targets them (check whether they're "
        "dead duplicates or just missing a link):\n  "
        + "\n  ".join(str(p.relative_to(CLAUDE_DIR)) for p in orphans)
    )


def test_detector_flags_a_duplicate_named_like_its_parent(tmp_path):
    """Regression: reproduces the exact jira/jira.md orphan pattern."""
    sgs = tmp_path / "_style_guide_standards"
    sgs.mkdir()
    (sgs / "jira.md").write_text("# Jira\n\n- [dag_design.md](jira/dag_design.md)\n")
    child_dir = sgs / "jira"
    child_dir.mkdir()
    (child_dir / "dag_design.md").write_text("# DAG design\n")
    (child_dir / "jira.md").write_text("# Jira (stale duplicate)\n")

    orphans = find_unreferenced_content_files(tmp_path)

    assert [p.name for p in orphans] == ["jira.md"]
    assert orphans[0].parent.name == "jira"


def test_detector_does_not_flag_a_referenced_child(tmp_path):
    """Regression: a child page linked from its parent is not flagged."""
    sgs = tmp_path / "_style_guide_standards"
    sgs.mkdir()
    (sgs / "jira.md").write_text("# SQL\n\n@./jira/formatting.md\n")
    child_dir = sgs / "jira"
    child_dir.mkdir()
    (child_dir / "formatting.md").write_text("# Formatting\n")

    orphans = find_unreferenced_content_files(tmp_path)

    assert orphans == []


def test_detector_exempts_entry_point_files(tmp_path):
    """Regression: a known entry point needs no incoming reference at all."""
    sgs = tmp_path / "_style_guide_standards"
    sgs.mkdir()
    (sgs / "jira.md").write_text("# Jira\n\nNo inbound links to this file exist anywhere.\n")

    orphans = find_unreferenced_content_files(tmp_path)

    assert orphans == []


def test_detector_exempts_files_under_templates_dir(tmp_path):
    """Regression: templates are copied via prose instruction, not linked — exempt."""
    sgs = tmp_path / "_style_guide_standards" / "airflow"
    sgs.mkdir(parents=True)
    templates = sgs / "templates"
    templates.mkdir()
    (templates / "template_dag_readme.md").write_text("# Template\nNever linked to directly.\n")

    orphans = find_unreferenced_content_files(tmp_path)

    assert orphans == []


def test_detector_resolves_relative_import_syntax(tmp_path):
    """Regression: `@./child.md` import syntax is correctly resolved and counted."""
    sgs = tmp_path / "_style_guide_standards"
    sgs.mkdir()
    (sgs / "sql.md").write_text("@./sql/cte_style_guide.md\n")
    child_dir = sgs / "sql"
    child_dir.mkdir()
    (child_dir / "cte_style_guide.md").write_text("# CTEs\n")

    refs = _outgoing_references(sgs / "sql.md")

    assert (child_dir / "cte_style_guide.md").resolve() in refs


def test_detector_resolves_markdown_link_syntax(tmp_path):
    """Regression: `[text](child.md)` markdown-link syntax is correctly resolved."""
    sgs = tmp_path / "_style_guide_standards"
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
    sgs = tmp_path / "_style_guide_standards"
    sgs.mkdir()
    (sgs / "jira.md").write_text("# jira\n\nSome other doc mentions `jira.md` in prose.\n")
    child_dir = sgs / "jira"
    child_dir.mkdir()
    (child_dir / "jira.md").write_text("# jira (stale duplicate)\n")

    orphans = find_unreferenced_content_files(tmp_path)

    assert [p.parent.name for p in orphans] == ["jira"]


def test_read_on_demand_pointer_counts_as_a_reference(tmp_path):
    """A child named by a parent's Read on demand pointer is referenced, even without a markdown link."""
    lazy = tmp_path / "_rules_lazy_load"
    (lazy / "guide").mkdir(parents=True)
    child = lazy / "guide" / "_child.md"
    child.write_text("# Child\n")
    parent = tmp_path / "rules" / "01_essentials" / "guide.md"
    parent.parent.mkdir(parents=True)
    parent.write_text("- **Read on demand:** `~/.claude/_rules_lazy_load/guide/_child.md` — detail\n")
    assert child.resolve() in _outgoing_references(parent), "the pointer's target was not recognised"
    assert (lazy / "x.md").resolve() not in _outgoing_references(parent), "an unnamed file must not count"
