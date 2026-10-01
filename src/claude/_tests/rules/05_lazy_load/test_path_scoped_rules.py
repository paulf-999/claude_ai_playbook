# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-01
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests for path-scoped rules in rules/.

Claude Code only loads a rule with ``paths:`` frontmatter when a matching
file is read, but any ``@`` import inside that rule still loads at session
start. That is how sql.md's four ``@./sql/*.md`` children loaded in every
session and pushed the always-on total over the 150k-char limit (fixed in
PR #184). This test fails if a path-scoped rule regains an ``@`` import.

Also verifies the rules/ folder convention from
``_claude_directory_organisation.md``: it holds only symlinks into
``_rules/05_lazy_load/``, never original files.
"""
import re
from pathlib import Path

from _shared_paths import CLAUDE_DIR, RULES_DIR

PATH_SCOPED_DIR = CLAUDE_DIR / "rules"
LAZY_LOAD_DIR = RULES_DIR / "05_lazy_load"
IMPORT_LINE_PATTERN = re.compile(r"^@\S")
FENCE_PATTERN = re.compile(r"^\s*(```|~~~)")


def frontmatter_paths(text: str) -> list[str]:
    """Return the globs listed under ``paths:`` in a file's YAML frontmatter.

    :param text: Full file content.
    :type text: str
    :return: The path globs, or an empty list if there is no ``paths:`` key.
    :rtype: list[str]
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return []
    globs: list[str] = []
    in_paths = False
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("paths:"):
            in_paths = True
            continue
        if in_paths and line.lstrip().startswith("- "):
            globs.append(line.lstrip()[2:].strip().strip("\"'"))
        elif in_paths:
            in_paths = False
    return globs


def find_import_lines(text: str) -> list[int]:
    """Return the 1-indexed line numbers of ``@`` imports outside code fences.

    :param text: Full file content.
    :type text: str
    :return: Line numbers of lines that Claude Code would treat as imports.
    :rtype: list[int]
    """
    hits = []
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        if FENCE_PATTERN.match(line):
            in_fence = not in_fence
            continue
        if not in_fence and IMPORT_LINE_PATTERN.match(line):
            hits.append(number)
    return hits


def find_violations(rules_dir: Path) -> list[str]:
    """Return ``file:line`` for every ``@`` import in a path-scoped rule.

    :param rules_dir: Folder of path-scoped rules to scan.
    :type rules_dir: Path
    :return: One entry per offending import line.
    :rtype: list[str]
    """
    violations = []
    for rule in sorted(rules_dir.glob("*.md")):
        text = rule.read_text(encoding="utf-8")
        if not frontmatter_paths(text):
            continue
        violations += [f"{rule.name}:{n}" for n in find_import_lines(text)]
    return violations


def _scoped_rules() -> list[Path]:
    """Return every .md file in rules/."""
    return sorted(PATH_SCOPED_DIR.glob("*.md"))


# ── Real config ─────────────────────────────────────────────────────────


def test_rules_folder_has_scoped_rules():
    """rules/ exists and holds at least one rule, so the checks below run."""
    assert PATH_SCOPED_DIR.is_dir(), f"Missing folder: {PATH_SCOPED_DIR}"
    assert _scoped_rules(), "rules/ is empty — nothing for the checks to verify"


def test_every_entry_is_a_markdown_symlink():
    """rules/ holds only .md symlinks, never original files."""
    for entry in PATH_SCOPED_DIR.iterdir():
        assert entry.suffix == ".md", f"Non-markdown entry in rules/: {entry.name}"
        assert entry.is_symlink(), (
            f"rules/{entry.name} is a real file — move it to _rules/05_lazy_load/ "
            "and symlink it here instead"
        )


def test_every_symlink_resolves_into_lazy_load():
    """Each symlink points at an existing file under _rules/05_lazy_load/."""
    for rule in _scoped_rules():
        target = rule.resolve()
        assert target.is_file(), f"rules/{rule.name} is a broken symlink"
        assert target.is_relative_to(LAZY_LOAD_DIR.resolve()), (
            f"rules/{rule.name} points outside _rules/05_lazy_load/: {target}"
        )


def test_every_rule_declares_paths():
    """Each rule in rules/ is path-scoped, or it would load every session."""
    for rule in _scoped_rules():
        assert frontmatter_paths(rule.read_text(encoding="utf-8")), (
            f"rules/{rule.name} has no `paths:` frontmatter, so it loads in every session"
        )


def test_no_imports_in_path_scoped_rules():
    """No path-scoped rule contains an ``@`` import, which would load at startup."""
    violations = find_violations(PATH_SCOPED_DIR)
    assert not violations, (
        "`@` imports in path-scoped rules load in every session regardless of "
        "`paths:` — replace them with `**Read on demand:**` pointers:\n  "
        + "\n  ".join(violations)
    )


# ── Detector behaviour ──────────────────────────────────────────────────


def test_frontmatter_paths_reads_globs():
    """Quoted and unquoted globs under ``paths:`` are both returned."""
    text = '---\npaths:\n  - "**/*.sql"\n  - models/**\n---\n# Rule\n'
    assert frontmatter_paths(text) == ["**/*.sql", "models/**"]


def test_frontmatter_paths_empty_without_frontmatter():
    """A file with no frontmatter, or none with ``paths:``, returns no globs."""
    assert frontmatter_paths("# Rule\n\n@./child.md\n") == []
    assert frontmatter_paths("---\nname: x\n---\n# Rule\n") == []


def test_frontmatter_paths_stops_at_next_key():
    """Globs end at the next frontmatter key."""
    text = "---\npaths:\n  - a/**\ndescription: b\n---\n"
    assert frontmatter_paths(text) == ["a/**"]


def test_find_import_lines_flags_relative_and_home_imports():
    """Both ``@./`` and ``@~/`` imports are flagged with their line numbers."""
    text = "# Rule\n@./sql/formatting.md\ntext\n@~/claude/x.md\n"
    assert find_import_lines(text) == [2, 4]


def test_find_import_lines_ignores_code_fences():
    """An ``@`` line inside a fenced code block is example text, not an import."""
    text = "# Rule\n```\n@./example.md\n```\n~~~\n@~/x.md\n~~~\n"
    assert find_import_lines(text) == []


def test_find_import_lines_ignores_mid_line_mentions():
    """``@`` that does not start a line (emails, prose) is not an import."""
    text = "Contact user@example.com\n- see @./child.md for details\n@ alone\n"
    assert find_import_lines(text) == []


def test_detector_flags_the_original_sql_regression(tmp_path):
    """Regression: the pre-#184 sql.md shape is caught."""
    (tmp_path / "sql.md").write_text(
        '---\npaths:\n  - "**/*.sql"\n---\n# SQL\n\n## Imports\n\n'
        "@./sql/formatting.md\n@./sql/sqlfluff.md\n"
    )
    assert find_violations(tmp_path) == ["sql.md:9", "sql.md:10"]


def test_detector_passes_read_on_demand_pointers(tmp_path):
    """The post-#184 shape, with read-on-demand pointers, passes."""
    (tmp_path / "sql.md").write_text(
        '---\npaths:\n  - "**/*.sql"\n---\n# SQL\n\n'
        "- **Read on demand:** `~/claude/_rules/.../sql/formatting.md` — formatting.\n"
    )
    assert find_violations(tmp_path) == []


def test_detector_skips_rules_without_paths(tmp_path):
    """Imports in an always-on rule are allowed, since it loads anyway."""
    (tmp_path / "always_on.md").write_text("# Always on\n@./child.md\n")
    assert find_violations(tmp_path) == []
