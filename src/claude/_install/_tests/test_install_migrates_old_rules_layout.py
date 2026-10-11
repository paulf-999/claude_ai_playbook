# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-03
# Date updated:      2026-10-11
# Version:           2.4.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates that ``make install`` clears what the old ``_rules/`` layout left behind.

Rules used to live in ``_rules/``, with path-scoped ones linked into ``rules/`` by the install.
They now ship in ``rules/`` and ``_rules_lazy_load/`` directly, so the install removes the old
links, removes any old file whose content the repo shipped (in ``_rules/`` or already moved into
``_rules_lazy_load/``), and moves any file you added under
``_rules/`` to the same place in ``_rules_lazy_load/`` (whose root was ``_rules/05_lazy_load/``),
never overwriting. Each test runs the real
``migrate_old_rules_layout`` step against a temp target.
"""

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
UTILS = REPO_ROOT / "src" / "claude" / "_install" / "helpers" / "claude_file_utils.sh"
INSTALL_SCRIPT = REPO_ROOT / "src" / "claude" / "_install" / "install_claude_files.sh"
WINDOWS_SCRIPT = REPO_ROOT / "src" / "claude" / "_install" / "install_claude_files_windows.sh"
LAZY = "_rules_lazy_load"


def write(target: Path, rel: str, text: str = "x\n"):
    """Write one file under the target, creating its folders."""
    (target / rel).parent.mkdir(parents=True, exist_ok=True)
    (target / rel).write_text(text)


def migrate(target: Path) -> str:
    """Run the real migration step against the target and return its output."""
    env = {**os.environ, "HOME": str(target.parent), "CLAUDE_CONFIG_DIR": str(target)}
    done = subprocess.run(
        ["bash", "-c", f'source "{UTILS}" && migrate_old_rules_layout'],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=60, check=True,
    )
    return done.stdout + done.stderr


def test_old_links_into_rules_are_removed(tmp_path: Path):
    """A link an earlier install made into ../_rules/ is removed, so nothing dangles in rules/."""
    (tmp_path / "rules").mkdir()
    (tmp_path / "rules" / "sql.md").symlink_to("../_rules/05_lazy_load/style_guide_standards/sql.md")
    output = migrate(tmp_path)
    assert not (tmp_path / "rules" / "sql.md").is_symlink(), "the old link survived"
    assert "Removed old rule link: rules/sql.md" in output, f"the removal should be logged: {output}"


def test_real_files_and_other_links_in_rules_are_kept(tmp_path: Path):
    """Only links into ../_rules/ go — shipped rule files and other links stay."""
    write(tmp_path, "rules/01_essentials/a.md", "# A\n")
    write(tmp_path, "notes.md")
    (tmp_path / "rules" / "mine.md").symlink_to("../notes.md")
    migrate(tmp_path)
    assert (tmp_path / "rules" / "01_essentials" / "a.md").read_text() == "# A\n", "a shipped rule was touched"
    assert (tmp_path / "rules" / "mine.md").is_symlink(), "a link that isn't into _rules/ was removed"


def test_your_lazy_files_move_to_the_lazy_folder(tmp_path: Path):
    """A file you added under _rules/05_lazy_load/ moves to the same place under _rules_lazy_load/."""
    write(tmp_path, "_rules/05_lazy_load/org/_naming.md", "# Org naming\n")
    output = migrate(tmp_path)
    moved = tmp_path / LAZY / "org" / "_naming.md"
    assert moved.read_text() == "# Org naming\n", "the org file didn't reach _rules_lazy_load/org/"
    assert "Moved your file: _rules/05_lazy_load/org/_naming.md -> _rules_lazy_load/org/_naming.md" in output


def test_other_files_keep_their_path_under_the_lazy_folder(tmp_path: Path):
    """A file outside 05_lazy_load/, e.g. a promoted kaizen rule, keeps its path under _rules_lazy_load/."""
    write(tmp_path, "_rules/learned/no_bare_except.md", "# Learned\n")
    migrate(tmp_path)
    assert (tmp_path / LAZY / "learned" / "no_bare_except.md").is_file(), "the learned rule didn't move"


def test_empty_old_folder_is_removed(tmp_path: Path):
    """Once everything has moved, the old _rules/ folder and its empty subfolders are gone."""
    write(tmp_path, "_rules/05_lazy_load/org/_naming.md")
    (tmp_path / "_rules" / "01_essentials").mkdir()
    migrate(tmp_path)
    assert not (tmp_path / "_rules").exists(), "the empty _rules/ folder was left behind"


def test_existing_file_is_never_overwritten(tmp_path: Path):
    """If the new path is taken, the old file stays in _rules/ and a warning names both."""
    write(tmp_path, "_rules/05_lazy_load/org.md", "# Old org index\n")
    write(tmp_path, f"{LAZY}/org.md", "# Shipped org index\n")
    output = migrate(tmp_path)
    assert (tmp_path / LAZY / "org.md").read_text() == "# Shipped org index\n", "the shipped file was overwritten"
    assert (tmp_path / "_rules" / "05_lazy_load" / "org.md").is_file(), "the clashing old file was lost"
    assert "Kept _rules/05_lazy_load/org.md: _rules_lazy_load/org.md already exists" in output, output
    assert "_rules/ still holds files" in output, f"the leftover folder should be flagged: {output}"


def test_target_without_old_layout_is_untouched(tmp_path: Path):
    """A fresh target with no _rules/ and no rules/ runs the step quietly."""
    output = migrate(tmp_path)
    assert not (tmp_path / "_rules").exists(), "the step must not create _rules/"
    assert "Moved" not in output and "Removed" not in output, f"nothing should change: {output}"


def test_rerun_is_a_no_op(tmp_path: Path):
    """Running the step twice moves nothing the second time."""
    write(tmp_path, "_rules/05_lazy_load/org/_naming.md")
    migrate(tmp_path)
    output = migrate(tmp_path)
    assert "Moved" not in output, f"a second run should have nothing to move: {output}"


def test_installers_run_the_step_after_pruning():
    """The step runs after prune_removed_files, so only your own files are left in _rules/ to move."""
    script = INSTALL_SCRIPT.read_text()
    assert "build_path_scoped_rules" not in script, "make install still builds rule links"
    assert script.index("prune_removed_files ") < script.index("migrate_old_rules_layout"), "must run after pruning"
    windows = WINDOWS_SCRIPT.read_text()
    assert "migrate_old_rules_layout" in windows, "the Windows sync should clear old rule links too"
    assert 'RETIRED_ITEMS=("_rules")' in windows, "the Windows sync should remove the retired _rules/ folder"


# --- Old copies the repo shipped ---

# Read from HEAD, not the working tree, so the repo stores this exact content even mid-edit
SHIPPED = subprocess.run(
    ["git", "show", f"HEAD:src/claude/rules/{LAZY}/README.md"],
    cwd=REPO_ROOT, capture_output=True, text=True, check=True,
).stdout


def test_shipped_copy_is_removed_not_merged(tmp_path: Path):
    """An old copy whose content the repo shipped is removed, even when the new path exists, with no merge prompt."""
    write(tmp_path, "_rules/README.md", SHIPPED)
    write(tmp_path, f"{LAZY}/README.md", "# Newer shipped index\n")
    output = migrate(tmp_path)
    assert not (tmp_path / "_rules").exists(), "the stale shipped copy was kept"
    assert "merge it by hand" not in output, f"a shipped copy must never ask for a merge: {output}"
    assert "Removed old shipped copies from _rules/: 1" in output, output
    assert (tmp_path / LAZY / "README.md").read_text() == "# Newer shipped index\n", "the new file was touched"


def test_shipped_copy_is_not_moved_into_the_lazy_folder(tmp_path: Path):
    """A shipped copy with no new counterpart is removed, so a retired rule never comes back as a lazy file."""
    write(tmp_path, "_rules/05_lazy_load/turn_budgets.md", SHIPPED)
    output = migrate(tmp_path)
    assert not (tmp_path / LAZY / "turn_budgets.md").exists(), "a retired shipped rule was moved in as yours"
    assert "Moved your file" not in output, f"a shipped copy must not be reported as yours: {output}"


def test_shipped_copies_get_one_summary_line(tmp_path: Path):
    """Many shipped copies give one count line, not a line per file, so the install output stays short."""
    for rel in ("_rules/README.md", "_rules/05_lazy_load/a.md", "_rules/05_lazy_load/org/b.md"):
        write(tmp_path, rel, SHIPPED)
    output = migrate(tmp_path)
    assert "Removed old shipped copies from _rules/: 3 (the backup keeps them)" in output, output
    assert output.count("_rules/05_lazy_load/") == 0, f"individual files were listed: {output}"


# --- Old shipped copies already moved into _rules_lazy_load/ ---


def test_stale_shipped_copy_in_lazy_folder_is_removed(tmp_path: Path):
    """A shipped copy the first migration moved into _rules_lazy_load/ is removed, with empty folders."""
    write(tmp_path, f"{LAZY}/01_essentials/guiding_principles.md", SHIPPED)
    output = migrate(tmp_path)
    assert not (tmp_path / LAZY / "01_essentials").exists(), "the stale shipped copy or its folder was kept"
    assert f"Removed old shipped copies from {LAZY}/: 1 (the backup keeps them)" in output, output


def test_lazy_file_the_install_ships_is_kept(tmp_path: Path):
    """A file this install ships stays, even though its content is in the repo's history."""
    write(tmp_path, f"{LAZY}/README.md", SHIPPED)
    output = migrate(tmp_path)
    assert (tmp_path / LAZY / "README.md").read_text() == SHIPPED, "a currently shipped lazy file was removed"
    assert "Removed old shipped copies" not in output, output


def test_your_own_lazy_file_is_kept(tmp_path: Path):
    """A file you wrote has content the repo never stored, so it stays where it is."""
    write(tmp_path, f"{LAZY}/_learned/my_rule.md", "# My own learned rule\n")
    output = migrate(tmp_path)
    assert (tmp_path / LAZY / "_learned" / "my_rule.md").is_file(), "your own lazy file was removed"
    assert "Removed old shipped copies" not in output, output


def test_empty_old_file_is_moved_not_removed(tmp_path: Path):
    """An empty file under _rules/ is treated as yours, since the repo storing an empty file proves nothing."""
    write(tmp_path, "_rules/05_lazy_load/placeholder.md", "")
    migrate(tmp_path)
    assert (tmp_path / LAZY / "placeholder.md").is_file(), "an empty file was taken for a shipped copy and removed"
