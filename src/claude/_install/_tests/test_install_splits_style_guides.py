# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-10
# Date updated:      2026-10-10
# Version:           2.0.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────
"""Validates that ``make install`` moves the style guides' entry files under ``rules/`` and leaves the rest.

The repo keeps every style guide in ``_style_guide_standards/``, and so does the install, except that
entry files (those with ``paths:`` frontmatter) must sit under ``rules/04_path_scoped/`` so Claude Code
loads them on matching files. Each test runs the real copy, flatten, relocate, split and prune steps
from ``claude_file_utils.sh`` against a fake source and a temp target.
"""

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
UTILS = REPO_ROOT / "src" / "sh" / "claude" / "helpers" / "claude_file_utils.sh"
INSTALL_SCRIPT = REPO_ROOT / "src" / "sh" / "claude" / "install_claude_files.sh"
WINDOWS_SCRIPT = REPO_ROOT / "src" / "sh" / "claude" / "install_claude_files_windows.sh"
GUIDES = "_style_guide_standards"
PATH_SCOPED = "rules/04_path_scoped/style_guide_standards"
ON_DEMAND = GUIDES  # every file without paths: stays where the repo keeps it

ENTRY = '---\npaths:\n  - "**/*.sql"\n---\n# SQL\n'
SOURCE_FILES = {
    "rules/01_essentials/core.md": "core\n",
    "rules/_rules_lazy_load/org.md": "org\n",
    f"{GUIDES}/sql.md": ENTRY,
    f"{GUIDES}/infra/terraform.md": ENTRY,
    f"{GUIDES}/sql/formatting.md": "# Formatting\n",
    f"{GUIDES}/sql/templates/template_cte.sql": "select 1\n",
    f"{GUIDES}/README.md": "# Style guides\n",
    f"{GUIDES}/later_paths.md": "# Title\n\npaths: mentioned in prose, not frontmatter\n",
    f"{GUIDES}/other_key.md": "---\ndescription: no paths here\n---\n# Other\n",
}


def make_tree(root: Path, files: dict[str, str]):
    """Write a dict of relative paths and contents under a folder.

    :param root: Folder to write into.
    :param files: Relative path to file content.
    """
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)


def install(tmp_path: Path) -> str:
    """Run the install's copy, flatten, relocate, split and prune steps from the fake source into the target.

    :param tmp_path: Test folder holding ``src/``, ``target/`` and ``home/``.
    :return: The steps' combined output.
    """
    env = {**os.environ, "HOME": str(tmp_path / "home"), "CLAUDE_CONFIG_DIR": str(tmp_path / "target")}
    steps = (f'source "{UTILS}" && SOURCE_DIR="{tmp_path / "src"}" && copy_claude_files && flatten_skills'
             " && relocate_lazy_rules && split_style_guides && prune_removed_files")
    done = subprocess.run(["bash", "-c", steps], cwd=REPO_ROOT, env=env,
                          capture_output=True, text=True, timeout=60, check=True)
    return done.stdout + done.stderr


def setup(tmp_path: Path) -> Path:
    """Create the fake source and an empty target, and run a first install.

    :param tmp_path: pytest's temp folder.
    :return: The target folder.
    """
    make_tree(tmp_path / "src", SOURCE_FILES)
    (tmp_path / "home").mkdir()
    (tmp_path / "target").mkdir()
    install(tmp_path)
    return tmp_path / "target"


def test_entry_files_land_in_path_scoped_rules(tmp_path: Path):
    """Files with paths: frontmatter install under rules/, unchanged, so they still load on matching files."""
    target = setup(tmp_path)
    assert (target / PATH_SCOPED / "sql.md").read_text() == ENTRY, "sql.md missing or changed"
    assert (target / PATH_SCOPED / "infra/terraform.md").is_file(), "nested entry file missing"


def test_other_files_stay_in_the_style_guide_folder(tmp_path: Path):
    """Detail files, templates and the README stay in _style_guide_standards/, keeping their relative paths."""
    target = setup(tmp_path)
    for rel in ("sql/formatting.md", "sql/templates/template_cte.sql", "README.md"):
        assert (target / ON_DEMAND / rel).is_file(), f"{rel} missing from the on-demand folder"
        assert not (target / PATH_SCOPED / rel).exists(), f"{rel} also landed in the path-scoped folder"


def test_only_opening_frontmatter_counts(tmp_path: Path):
    """A paths: line outside the opening frontmatter, or frontmatter without one, doesn't make a file path-scoped."""
    target = setup(tmp_path)
    for rel in ("later_paths.md", "other_key.md"):
        assert (target / ON_DEMAND / rel).is_file(), f"{rel} wasn't treated as on-demand"


def test_no_entry_file_is_left_behind(tmp_path: Path):
    """No paths: file stays in the top-level folder, where it would never load, and no empty folder is left."""
    target = setup(tmp_path)
    assert not (target / GUIDES / "sql.md").exists(), "an entry file was left where it can't load"
    assert not (target / GUIDES / "infra").exists(), "the empty folder of a moved entry file was left behind"


def test_move_is_logged_and_no_op_without_guides(tmp_path: Path):
    """The install says how many entry files it moved, and with no style guides it creates nothing."""
    make_tree(tmp_path / "src", SOURCE_FILES)
    (tmp_path / "home").mkdir()
    (tmp_path / "target").mkdir()
    assert f"Moved 2 style-guide entry files into {PATH_SCOPED}/" in install(tmp_path)
    bare = tmp_path / "bare"
    make_tree(bare / "src", {"rules/01_essentials/core.md": "core\n"})
    (bare / "home").mkdir()
    (bare / "target").mkdir()
    assert "style-guide entry files" not in install(bare), "the step claimed a move with nothing to move"
    assert not (bare / "target" / PATH_SCOPED).exists(), "an empty style-guide folder was created"


def test_manifest_lists_installed_paths(tmp_path: Path):
    """The manifest names style guides where the install leaves them, not where the repo keeps them."""
    lines = (setup(tmp_path) / ".install_manifest").read_text().splitlines()
    assert f"{PATH_SCOPED}/sql.md" in lines, f"installed entry path missing: {lines}"
    assert f"{ON_DEMAND}/sql/formatting.md" in lines, f"installed detail path missing: {lines}"
    assert f"{GUIDES}/sql.md" not in lines, "an entry file is listed where the repo keeps it"


def test_reinstall_prunes_nothing_and_updates_content(tmp_path: Path):
    """A second install removes nothing the repo still ships, and replaces the last install's copy."""
    target = setup(tmp_path)
    (tmp_path / f"src/{GUIDES}/sql/formatting.md").write_text("# Formatting v2\n")
    output = install(tmp_path)
    assert "Removed (no longer in the repo)" not in output, output
    assert (target / ON_DEMAND / "sql/formatting.md").read_text() == "# Formatting v2\n", "content wasn't updated"
    assert (target / PATH_SCOPED / "sql.md").is_file(), "a re-install removed an entry file"


def test_guide_removed_from_repo_is_pruned(tmp_path: Path):
    """Deleting a style guide in the repo removes it from its installed path."""
    target = setup(tmp_path)
    (tmp_path / f"src/{GUIDES}/sql.md").unlink()
    (tmp_path / f"src/{GUIDES}/sql/formatting.md").unlink()
    install(tmp_path)
    assert not (target / PATH_SCOPED / "sql.md").exists(), "a deleted entry file is still installed"
    assert not (target / ON_DEMAND / "sql/formatting.md").exists(), "a deleted detail file is still installed"


def test_installs_split_after_relocating_and_before_pruning():
    """Both installs split once the lazy folder is in place, and the Mac one before pruning reads the layout."""
    script = INSTALL_SCRIPT.read_text()
    relocate, split, prune = (script.index(f"    {step}") for step in
                              ("relocate_lazy_rules", "split_style_guides", "prune_removed_files"))
    assert relocate < split < prune, "split_style_guides must run between relocate_lazy_rules and prune_removed_files"
    windows = WINDOWS_SCRIPT.read_text()
    assert windows.index("    relocate_lazy_rules") < windows.index("    split_style_guides"), \
        "the Windows install must split style guides after relocating the lazy folder"
