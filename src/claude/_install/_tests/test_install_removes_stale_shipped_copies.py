# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-11
# Date updated:      2026-10-11
# Version:           1.0.2
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates that ``make install`` removes old shipped copies the manifest never listed.

Installs from before the install manifest, and renames inside a folder, leave files behind that pruning
can't see. The install removes a file when it's in a folder the repo installs (or the last install filled),
this install doesn't ship it, and its exact content is something the repo stored. Each test runs the real
``remove_stale_shipped_copies`` step against a temp target.
"""

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
UTILS = REPO_ROOT / "src" / "claude" / "_install" / "helpers" / "claude_file_utils.sh"

# Read from HEAD, not the working tree, so the repo stores this exact content even mid-edit
SHIPPED = subprocess.run(
    ["git", "show", "HEAD:src/claude/rules/_rules_lazy_load/README.md"],
    cwd=REPO_ROOT, capture_output=True, text=True, check=True,
).stdout


def write(target: Path, rel: str, text: str = SHIPPED):
    """Write one file under the target, creating its folders."""
    (target / rel).parent.mkdir(parents=True, exist_ok=True)
    (target / rel).write_text(text)


def remove_stale(target: Path, previous_manifest: str = "") -> str:
    """Run the real step against the target, as if the last install's manifest held ``previous_manifest``."""
    env = {**os.environ, "HOME": str(target.parent), "CLAUDE_CONFIG_DIR": str(target),
           "PREVIOUS_MANIFEST": previous_manifest}
    done = subprocess.run(
        ["bash", "-c", f'source "{UTILS}" && remove_stale_shipped_copies'],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=60, check=True,
    )
    return done.stdout + done.stderr


def test_copy_in_a_retired_folder_is_removed(tmp_path: Path):
    """A shipped copy in a folder the repo renamed (e.g. _scripts/) goes, with the empty folder."""
    target = tmp_path / "cfg"
    write(target, "_scripts/claude_component_audit.py")
    output = remove_stale(target, previous_manifest="_scripts/_audit_scripts/audit_rule_usage.py\n")
    assert not (target / "_scripts").exists(), "the retired folder's stale copy or the folder itself was kept"
    assert "Removed old shipped copies from _scripts/: 1 (the backup keeps them)" in output, output


def test_retired_folder_not_on_the_manifest_is_untouched(tmp_path: Path):
    """A folder neither this install nor the last one filled is never checked, whatever its content."""
    target = tmp_path / "cfg"
    write(target, "_scripts/claude_component_audit.py")
    output = remove_stale(target)
    assert (target / "_scripts" / "claude_component_audit.py").is_file(), "a folder outside the install was touched"
    assert "Removed old shipped copies" not in output, output


def test_renamed_copy_in_a_current_folder_is_removed(tmp_path: Path):
    """An old name left in a folder the repo still installs goes, e.g. a template renamed since."""
    target = tmp_path / "cfg"
    write(target, "_templates/skills/old_name.md.template")
    output = remove_stale(target)
    assert not (target / "_templates").exists(), "the renamed template's old copy was kept"
    assert "Removed old shipped copies from _templates/: 1 (the backup keeps them)" in output, output


def test_copies_get_one_line_per_folder(tmp_path: Path):
    """Several copies give one count line per folder, not a line per file."""
    target = tmp_path / "cfg"
    for rel in ("_templates/a.md", "_templates/b/c.md", "hooks/old_hook.md"):
        write(target, rel)
    output = remove_stale(target)
    assert "Removed old shipped copies from _templates/: 2" in output, output
    assert "Removed old shipped copies from hooks/: 1" in output, output
    assert "b/c.md" not in output, f"individual files were listed: {output}"


def test_file_you_wrote_or_edited_is_kept(tmp_path: Path):
    """Content the repo never stored stays, even in a folder the install fills."""
    target = tmp_path / "cfg"
    write(target, "_templates/my_notes.md", "# My own notes\n")
    write(target, "hooks/edited_copy.md", SHIPPED + "my edit\n")
    output = remove_stale(target)
    assert (target / "_templates" / "my_notes.md").is_file(), "a file you wrote was removed"
    assert (target / "hooks" / "edited_copy.md").is_file(), "a file you edited was removed"
    assert "Removed old shipped copies" not in output, output


def test_empty_file_is_kept(tmp_path: Path):
    """An empty file stays: the repo stores an empty file, so an empty file proves nothing about its origin."""
    target = tmp_path / "cfg"
    write(target, "_rules_lazy_load/placeholder.md", "")
    remove_stale(target)
    assert (target / "_rules_lazy_load" / "placeholder.md").is_file(), "an empty file was taken for a shipped copy"


def test_runtime_and_user_owned_folders_are_untouched(tmp_path: Path):
    """Runtime folders and user-owned ones stay, even with shipped content and an old manifest naming them."""
    target = tmp_path / "cfg"
    write(target, "projects/session.md")
    write(target, "memory/note.md")
    write(target, "_plans/active/plan.md")
    remove_stale(target, previous_manifest="memory/MEMORY.md\n_plans/README.md\n")
    for rel in ("projects/session.md", "memory/note.md", "_plans/active/plan.md"):
        assert (target / rel).is_file(), f"{rel} was removed from a folder the install doesn't own"


def test_manifest_path_outside_the_target_is_ignored(tmp_path: Path):
    """A manifest line starting with ../ never makes the step look outside the target."""
    target = tmp_path / "cfg"
    target.mkdir()
    write(tmp_path, "outside.md")
    remove_stale(target, previous_manifest="../outside.md\n")
    assert (tmp_path / "outside.md").is_file(), "a file outside the target was removed"


def test_file_the_install_ships_is_kept(tmp_path: Path):
    """A file this install ships stays, even though its content is in the repo's history."""
    target = tmp_path / "cfg"
    write(target, "_rules_lazy_load/README.md")
    output = remove_stale(target)
    assert (target / "_rules_lazy_load" / "README.md").is_file(), "a currently shipped file was removed"
    assert "Removed old shipped copies" not in output, output
