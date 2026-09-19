# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 5/10
# Python style compliant: Yes
# Date created:      2026-09-19
# Version:           1.1.0
# Date updated:      2026-09-19
# ─────────────────────────────────────────────────────────

"""Generic orphaned-file detection for every skill under src/claude/skills/.

Applies to all current and future skills, not any one skill by name.
Validates the design constraint that every non-structural file in a skill
directory is discoverable from somewhere else in that same skill:
- Content coverage: the file's stem name (e.g. "general_page" for
  general_page.md) appears somewhere in the skill's other files —
  SKILL.md, skill.contract.yaml, the handler, evals, or another
  reference/pattern file. This is how confluence_create_page's dead
  templates/ directory and several unused pattern files were found and
  removed (2026-09-19).

Also verifies the inverse: every reference/ path SKILL.md points at
resolves to a real file, so a skill's docs can't silently link to
nothing (this is how git_create_pr's three broken reference/ links to
nonexistent files were found).

Structural files (SKILL.md, skill.contract.yaml, README.md, __init__.py,
conftest.py, evals.yaml, test_*.py, and auto-generated artifacts) are
exempt — they don't need to be "referenced by name" to be legitimate.
"""
import re
import sys
from pathlib import Path

from _shared_paths import CLAUDE_DIR, SKILLS_DIR

EXEMPT_NAMES = {
    "SKILL.md",
    "skill.contract.yaml",
    "README.md",
    "__init__.py",
    "conftest.py",
    "evals.yaml",
    ".coverage",
}
EXEMPT_DIR_NAMES = {"__pycache__", "evals", ".pytest_cache"}
EXEMPT_SUFFIXES = {".pyc"}
CONTENT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json"}


def _skill_dirs() -> list[Path]:
    """Return every skill directory (any directory containing a SKILL.md).

    Skips dot-prefixed directories (e.g. ``.trash/``) — Claude Code's own
    auto-managed sync/cleanup artifacts, not authored skills.

    :return: Sorted list of skill directory paths.
    :rtype: list[Path]
    """
    if not SKILLS_DIR.exists():
        return []
    return sorted(
        {
            p.parent
            for p in SKILLS_DIR.rglob("SKILL.md")
            if not any(part.startswith(".") for part in p.relative_to(SKILLS_DIR).parts)
        }
    )


def _is_exempt(file_path: Path, skill_root: Path) -> bool:
    """Return True if file_path is a structural/auto-generated file, not content.

    :param file_path: Candidate file to check.
    :type file_path: Path
    :param skill_root: The skill directory file_path lives under.
    :type skill_root: Path
    :return: Whether the file is exempt from needing a cross-reference.
    :rtype: bool
    """
    rel_parts = file_path.relative_to(skill_root).parts
    if file_path.name in EXEMPT_NAMES or file_path.suffix in EXEMPT_SUFFIXES:
        return True
    if any(part in EXEMPT_DIR_NAMES for part in rel_parts[:-1]):
        return True
    if file_path.name.startswith("test_") and file_path.suffix == ".py":
        return True
    return False


def _combined_text(skill_root: Path) -> str:
    """Concatenate every content file's text under a skill directory.

    Also includes the skill's out-of-tree test directory, if one exists at
    _tests/skills/<skill_dir_name>/ — a handler.py moved out of the skill
    directory (per the confluence_create_page precedent) is still clearly
    referenced by the test file that imports it, even though that test no
    longer lives inside skill_root.

    :param skill_root: The skill directory to scan.
    :type skill_root: Path
    :return: Combined text of all .md/.py/.yaml/.yml/.json files.
    :rtype: str
    """
    roots = [skill_root]
    external_tests = CLAUDE_DIR / "_tests" / "skills" / skill_root.name
    if external_tests.is_dir():
        roots.append(external_tests)

    combined = []
    for root in roots:
        for f in root.rglob("*"):
            if f.is_file() and f.suffix in CONTENT_SUFFIXES and "__pycache__" not in f.parts:
                try:
                    combined.append(f.read_text(encoding="utf-8", errors="ignore"))
                except OSError:
                    pass
    return "\n".join(combined)


def find_orphaned_files(skill_root: Path) -> list[Path]:
    """Return non-exempt files in skill_root never mentioned by name elsewhere.

    :param skill_root: The skill directory to scan.
    :type skill_root: Path
    :return: Files whose stem doesn't appear in any of the skill's other content.
    :rtype: list[Path]
    """
    candidates = [
        f for f in skill_root.rglob("*")
        if f.is_file() and "__pycache__" not in f.parts and not _is_exempt(f, skill_root)
    ]
    combined = _combined_text(skill_root)

    orphans = []
    for f in candidates:
        own_text = ""
        if f.suffix in CONTENT_SUFFIXES:
            try:
                own_text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                pass
        other_text = combined.replace(own_text, "", 1) if own_text else combined
        if f.stem not in other_text:
            orphans.append(f)
    return orphans


def find_broken_reference_links(skill_root: Path) -> list[str]:
    """Return reference/-prefixed paths mentioned in SKILL.md that don't exist.

    :param skill_root: The skill directory to scan.
    :type skill_root: Path
    :return: Reference paths named in SKILL.md with no file on disk.
    :rtype: list[str]
    """
    skill_md = skill_root / "SKILL.md"
    if not skill_md.exists():
        return []
    content = skill_md.read_text(encoding="utf-8", errors="ignore")
    broken = []
    for match in re.finditer(r"`(reference/[\w./-]+\.md)`", content):
        rel = match.group(1)
        if not (skill_root / rel).exists():
            broken.append(rel)
    return broken


def test_no_orphaned_files_in_any_skill():
    """Every content file in every skill must be referenced from elsewhere in that skill."""
    failures = []
    for skill_root in _skill_dirs():
        orphans = find_orphaned_files(skill_root)
        for orphan in orphans:
            failures.append(str(orphan.relative_to(SKILLS_DIR)))

    assert not failures, (
        "Orphaned skill files — never mentioned anywhere else in their skill "
        "(check whether they're dead content or just missing a link):\n  "
        + "\n  ".join(failures)
    )


def test_no_broken_reference_links_in_any_skill():
    """Every reference/ path a SKILL.md names must point at a real file."""
    failures = []
    for skill_root in _skill_dirs():
        for broken in find_broken_reference_links(skill_root):
            failures.append(f"{skill_root.relative_to(SKILLS_DIR)}: {broken}")

    assert not failures, (
        "SKILL.md files reference paths that don't exist on disk:\n  "
        + "\n  ".join(failures)
    )


def test_detector_flags_a_synthetic_orphan(tmp_path):
    """Regression: a file mentioned nowhere else is correctly flagged."""
    skill = tmp_path / "fake_skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text("# Fake skill\nNo mention of the orphan here.")
    (skill / "skill.contract.yaml").write_text("name: fake_skill")
    (skill / "orphaned_pattern.md").write_text("# Orphaned\nNever linked from anywhere.")

    orphans = find_orphaned_files(skill)

    assert len(orphans) == 1
    assert orphans[0].name == "orphaned_pattern.md"


def test_detector_passes_when_file_is_referenced(tmp_path):
    """Regression: a file named in SKILL.md is not flagged."""
    skill = tmp_path / "fake_skill"
    skill.mkdir()
    (skill / "skill.contract.yaml").write_text("name: fake_skill")
    (skill / "used_pattern.md").write_text("# Used pattern\nSome content.")
    (skill / "SKILL.md").write_text("# Fake skill\nSee `used_pattern.md` for details.")

    orphans = find_orphaned_files(skill)

    assert orphans == []


def test_detector_exempts_structural_and_test_files(tmp_path):
    """Regression: SKILL.md, skill.contract.yaml, README.md, and test_*.py never need a link."""
    skill = tmp_path / "fake_skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text("# Fake skill")
    (skill / "skill.contract.yaml").write_text("name: fake_skill")
    (skill / "README.md").write_text("# Notes")
    (skill / "test_fake_skill.py").write_text("def test_x(): pass")

    orphans = find_orphaned_files(skill)

    assert orphans == []


def test_detector_exempts_auto_generated_artifacts(tmp_path):
    """Regression: __pycache__ and .coverage are never flagged."""
    skill = tmp_path / "fake_skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text("# Fake skill")
    (skill / "skill.contract.yaml").write_text("name: fake_skill")
    (skill / ".coverage").write_text("binary-ish coverage data")
    pycache = skill / "__pycache__"
    pycache.mkdir()
    (pycache / "handler.cpython-39.pyc").write_bytes(b"\x00\x01")

    orphans = find_orphaned_files(skill)

    assert orphans == []


def test_detector_catches_confluence_create_page_bug_pattern(tmp_path):
    """Regression: reproduces the exact 2026-09-19 finding — a templates/ dir
    duplicating patterns/ content, referenced nowhere, must be flagged."""
    skill = tmp_path / "fake_skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text("# Fake skill\nUses `patterns/real.md`.")
    (skill / "skill.contract.yaml").write_text("name: fake_skill")
    patterns = skill / "patterns"
    patterns.mkdir()
    (patterns / "real.md").write_text("Real, referenced pattern.")
    templates = skill / "templates"
    templates.mkdir()
    (templates / "stale_duplicate.md").write_text("A stale, unreferenced duplicate.")

    orphans = find_orphaned_files(skill)

    assert [o.name for o in orphans] == ["stale_duplicate.md"]


def test_broken_link_detector_flags_nonexistent_reference(tmp_path):
    """Regression: reproduces the exact 2026-09-19 git_create_pr finding — a
    SKILL.md linking to a reference/ file that was never created."""
    skill = tmp_path / "fake_skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        "# Fake skill\nSee `reference/_implementation.md` for details."
    )

    broken = find_broken_reference_links(skill)

    assert broken == ["reference/_implementation.md"]


def test_broken_link_detector_passes_when_file_exists(tmp_path):
    """Regression: a reference/ link to a file that actually exists is not flagged."""
    skill = tmp_path / "fake_skill"
    skill.mkdir()
    reference = skill / "reference"
    reference.mkdir()
    (reference / "_implementation.md").write_text("Real content.")
    (skill / "SKILL.md").write_text(
        "# Fake skill\nSee `reference/_implementation.md` for details."
    )

    broken = find_broken_reference_links(skill)

    assert broken == []


def test_skill_dirs_discovery_finds_nested_skills(tmp_path, monkeypatch):
    """Regression: skill discovery works for both flat and group-nested skills."""
    monkeypatch.setattr(sys.modules[__name__], "SKILLS_DIR", tmp_path)
    (tmp_path / "flat_skill").mkdir()
    (tmp_path / "flat_skill" / "SKILL.md").write_text("# Flat")
    group = tmp_path / "_a_group" / "grouped_skill"
    group.mkdir(parents=True)
    (group / "SKILL.md").write_text("# Grouped")

    found = _skill_dirs()

    assert (tmp_path / "flat_skill") in found
    assert group in found
    assert len(found) == 2


def test_handler_referenced_only_by_external_test_is_not_orphaned(tmp_path, monkeypatch):
    """Regression: reproduces the exact 2026-09-19 confluence_create_page finding —
    a handler.py only imported by a test file that lives in _tests/skills/<name>/
    (moved out of the skill directory, per that same precedent) must not be
    flagged as orphaned just because nothing inside the skill directory itself
    mentions its name."""
    monkeypatch.setattr(sys.modules[__name__], "CLAUDE_DIR", tmp_path)
    skill_root = tmp_path / "skills" / "fake_skill"
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text("# Fake skill\nNo mention of the handler here.")
    (skill_root / "skill.contract.yaml").write_text("name: fake_skill")
    (skill_root / "fake_skill_handler.py").write_text("def do_thing():\n    pass\n")

    external_tests = tmp_path / "_tests" / "skills" / "fake_skill"
    external_tests.mkdir(parents=True)
    (external_tests / "test_fake_skill_handler.py").write_text(
        "from fake_skill_handler import do_thing\n"
    )

    orphans = find_orphaned_files(skill_root)

    assert orphans == []
