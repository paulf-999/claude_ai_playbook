# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-03
# Date updated:      2026-10-03
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates that ``make install`` rebuilds ``rules/`` from the path-scoped rules in ``_rules/``.

Claude Code only reads path-scoped rules from a folder named exactly ``rules/``, so the repo keeps
every rule in ``_rules/`` and the install links each rule with ``paths:`` frontmatter into
``rules/``. Each test runs the real ``build_path_scoped_rules`` step against a temp target.
"""

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
UTILS = REPO_ROOT / "src" / "sh" / "claude" / "helpers" / "claude_file_utils.sh"
INSTALL_SCRIPT = REPO_ROOT / "src" / "sh" / "claude" / "install_claude_files.sh"
WINDOWS_SCRIPT = REPO_ROOT / "src" / "sh" / "claude" / "install_claude_files_windows.sh"
LAZY = "_rules/05_lazy_load"
SCOPED = '---\npaths:\n  - "**/*.sql"\n---\n# Rule\n'
UNSCOPED = "# Rule with no frontmatter\n"


def write(target: Path, rel: str, text: str):
    """Write one file under the target, creating its folders."""
    (target / rel).parent.mkdir(parents=True, exist_ok=True)
    (target / rel).write_text(text)


def build(target: Path) -> str:
    """Run the real build step against the target and return its output."""
    env = {**os.environ, "HOME": str(target.parent), "CLAUDE_CONFIG_DIR": str(target)}
    done = subprocess.run(
        ["bash", "-c", f'source "{UTILS}" && build_path_scoped_rules'],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=60, check=True,
    )
    return done.stdout + done.stderr


def links(target: Path) -> list[str]:
    """Return the names of the links in the target's rules/ folder."""
    return sorted(p.name for p in (target / "rules").iterdir() if p.is_symlink())


def test_links_each_path_scoped_rule(tmp_path: Path):
    """A rule with paths: frontmatter gets a link in rules/ that reads the rule's text."""
    write(tmp_path, f"{LAZY}/sql.md", SCOPED)
    build(tmp_path)
    link = tmp_path / "rules" / "sql.md"
    assert link.is_symlink(), "rules/sql.md should be a link"
    assert link.read_text() == SCOPED, "the link should read the rule in _rules/"


def test_links_are_relative_so_the_folder_can_move(tmp_path: Path):
    """Each link points at ../_rules/..., not an absolute path tied to one machine."""
    write(tmp_path, f"{LAZY}/style_guide_standards/sql.md", SCOPED)
    build(tmp_path)
    target = str((tmp_path / "rules" / "sql.md").readlink())
    assert target == f"../{LAZY}/style_guide_standards/sql.md", f"unexpected link target: {target}"
    assert not Path(target).is_absolute(), "links must be relative"


def test_nested_rules_are_linked_by_filename(tmp_path: Path):
    """Rules in subfolders are linked flat, under their own filename."""
    write(tmp_path, f"{LAZY}/style_guide_standards/infra/terraform.md", SCOPED)
    write(tmp_path, f"{LAZY}/testing.md", SCOPED)
    build(tmp_path)
    assert links(tmp_path) == ["terraform.md", "testing.md"], f"got {links(tmp_path)}"


def test_rule_without_paths_is_not_linked(tmp_path: Path):
    """A lazy rule with no frontmatter stays out of rules/, or it would load in every session."""
    write(tmp_path, f"{LAZY}/turn_budgets.md", UNSCOPED)
    write(tmp_path, f"{LAZY}/sql.md", SCOPED)
    build(tmp_path)
    assert links(tmp_path) == ["sql.md"], f"only the path-scoped rule should be linked, got {links(tmp_path)}"


def test_paths_after_another_frontmatter_key_is_linked(tmp_path: Path):
    """paths: counts wherever it sits in the frontmatter, not only on the second line."""
    write(tmp_path, f"{LAZY}/dbt.md", '---\ndescription: dbt\npaths:\n  - "**/*.sql"\n---\n# Rule\n')
    build(tmp_path)
    assert links(tmp_path) == ["dbt.md"], f"got {links(tmp_path)}"


def test_paths_outside_the_frontmatter_is_ignored(tmp_path: Path):
    """A paths: line in the body, or frontmatter that isn't on line 1, doesn't make a rule path-scoped."""
    write(tmp_path, f"{LAZY}/body.md", "# Rule\n\npaths:\n  - x\n")
    write(tmp_path, f"{LAZY}/late.md", "# Rule\n---\npaths:\n  - x\n---\n")
    write(tmp_path, f"{LAZY}/after.md", "---\nname: x\n---\npaths:\n  - x\n")
    build(tmp_path)
    assert links(tmp_path) == [], f"no rule should be linked, got {links(tmp_path)}"


def test_link_to_a_rule_that_lost_paths_is_removed(tmp_path: Path):
    """Rebuilding drops links for rules that are no longer path-scoped."""
    write(tmp_path, f"{LAZY}/sql.md", SCOPED)
    build(tmp_path)
    write(tmp_path, f"{LAZY}/sql.md", UNSCOPED)
    build(tmp_path)
    assert not (tmp_path / "rules" / "sql.md").exists(), "a stale link survived the rebuild"
    assert (tmp_path / LAZY / "sql.md").is_file(), "removing the link must not touch the rule"


def test_real_file_in_rules_is_kept(tmp_path: Path):
    """Only links are replaced, so a rule file the user wrote in rules/ survives."""
    write(tmp_path, "rules/mine.md", "# My own rule\n")
    write(tmp_path, f"{LAZY}/sql.md", SCOPED)
    build(tmp_path)
    assert (tmp_path / "rules" / "mine.md").read_text() == "# My own rule\n", "the user's file was changed"
    assert links(tmp_path) == ["sql.md"], f"got {links(tmp_path)}"


def test_duplicate_filename_keeps_the_first_and_warns(tmp_path: Path):
    """Two path-scoped rules can't share a filename, so the first wins and a warning names the second."""
    write(tmp_path, f"{LAZY}/a/sql.md", SCOPED)
    write(tmp_path, f"{LAZY}/b/sql.md", SCOPED.replace("# Rule", "# Other"))
    output = build(tmp_path)
    assert str((tmp_path / "rules" / "sql.md").readlink()) == f"../{LAZY}/a/sql.md", "the first rule should win"
    assert f"Skipped path-scoped rule with a duplicate name: {LAZY}/b/sql.md" in output, "no duplicate warning"


def test_rebuild_is_idempotent_and_logs_the_count(tmp_path: Path):
    """Running the step twice gives the same links and reports how many it made."""
    write(tmp_path, f"{LAZY}/sql.md", SCOPED)
    write(tmp_path, f"{LAZY}/bash.md", SCOPED)
    build(tmp_path)
    output = build(tmp_path)
    assert links(tmp_path) == ["bash.md", "sql.md"], f"got {links(tmp_path)}"
    assert "Linked 2 path-scoped rules" in output, f"count missing from output: {output}"


def test_missing_lazy_folder_leaves_an_empty_rules_folder(tmp_path: Path):
    """A target with no 05_lazy_load/ still gets rules/, with nothing linked and no error."""
    output = build(tmp_path)
    assert (tmp_path / "rules").is_dir(), "rules/ should be created"
    assert links(tmp_path) == [], "nothing should be linked"
    assert "Linked 0 path-scoped rules" in output, f"unexpected output: {output}"


def test_installers_run_the_step_after_pruning(tmp_path: Path):
    """The step runs after prune_removed_files, which would otherwise delete the new links, and Windows runs it too."""
    script = INSTALL_SCRIPT.read_text()
    assert "build_path_scoped_rules" in script, "make install no longer builds rules/"
    assert script.index("prune_removed_files ") < script.index("build_path_scoped_rules"), "must run after pruning"
    assert "build_path_scoped_rules" in WINDOWS_SCRIPT.read_text(), "the Windows install should build rules/ too"
