"""Finds orphaned files, broken reference links and eager imports in a skill.

Each detector is a pure function over a skill's files, given as a map of path
(relative to the skill, in ``/`` form) to text, so it can be proven on a small
in-memory example. ``read_skill`` builds that map from disk for the real scan.

A file counts as referenced when its stem appears in another of the skill's content
files, or in the skill's out-of-tree tests at ``_tests/skills/<skill_name>/`` — a
handler moved out of the skill (the confluence_create_page precedent, 2026-09-19) is
still referenced by the test that imports it.
"""
from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

EXEMPT_NAMES = {"SKILL.md", "skill.contract.yaml", "README.md", "__init__.py", "conftest.py", "evals.yaml", ".coverage"}
EXEMPT_DIR_NAMES = {"__pycache__", ".pytest_cache"}
EXEMPT_SUFFIXES = {".pyc"}
CONTENT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json"}
REFERENCE_LINK = re.compile(r"`(reference/[\w./-]+\.md)`")


def skill_dirs(skills_dir: Path) -> list[Path]:
    """Return every skill directory (any directory holding a SKILL.md), flat or grouped.

    Skips dot-prefixed folders such as ``.trash/`` — Claude Code's own sync artefacts.

    :param skills_dir: The skills folder to search.
    :type skills_dir: Path
    :return: Sorted skill directories.
    :rtype: list[Path]
    """
    if not skills_dir.exists():
        return []
    return sorted(
        {
            p.parent for p in skills_dir.rglob("SKILL.md")
            if not any(part.startswith(".") for part in p.relative_to(skills_dir).parts)
        }
    )


def read_skill(skill_root: Path) -> dict[str, str]:
    """Read a skill's files into a path-to-text map.

    :param skill_root: The skill directory.
    :type skill_root: Path
    :return: Every file's ``/``-form relative path, mapped to its text (empty for non-content files).
    :rtype: dict[str, str]
    """
    return {
        f.relative_to(skill_root).as_posix(): (
            f.read_text(encoding="utf-8", errors="ignore") if f.suffix in CONTENT_SUFFIXES else ""
        )
        for f in sorted(skill_root.rglob("*")) if f.is_file()
    }


def read_external_tests(skill_root: Path, tests_dir: Path) -> list[str]:
    """Read the content of a skill's out-of-tree test folder, if it has one.

    :param skill_root: The skill directory.
    :type skill_root: Path
    :param tests_dir: The folder holding per-skill test folders, e.g. ``_tests/skills/``.
    :type tests_dir: Path
    :return: The text of each content file in ``<tests_dir>/<skill_name>/``.
    :rtype: list[str]
    """
    external = tests_dir / skill_root.name
    if not external.is_dir():
        return []
    return [text for path, text in read_skill(external).items() if is_content(path)]


def is_content(path: str) -> bool:
    """Say whether a skill file is readable content rather than a build artefact.

    :param path: ``/``-form path relative to the skill.
    :type path: str
    :return: True for .md/.py/.yaml/.yml/.json files outside ``__pycache__``.
    :rtype: bool
    """
    parts = PurePosixPath(path).parts
    return PurePosixPath(path).suffix in CONTENT_SUFFIXES and "__pycache__" not in parts


def is_exempt(path: str) -> bool:
    """Say whether a skill file is structural or generated, so it needs no reference.

    :param path: ``/``-form path relative to the skill.
    :type path: str
    :return: True for structural names, test files, ``.pyc`` files and anything in a cache folder.
    :rtype: bool
    """
    pure = PurePosixPath(path)
    return (
        pure.name in EXEMPT_NAMES
        or pure.suffix in EXEMPT_SUFFIXES
        or any(part in EXEMPT_DIR_NAMES for part in pure.parts[:-1])
        or (pure.name.startswith("test_") and pure.suffix == ".py")
    )


def find_orphans(files: dict[str, str], external_texts: list[str] | None = None) -> list[str]:
    """Return the non-exempt files whose stem appears in none of the skill's other content.

    :param files: The skill's ``/``-form paths mapped to their text.
    :type files: dict[str, str]
    :param external_texts: Text of the skill's out-of-tree tests, if any.
    :type external_texts: list[str] | None
    :return: Orphaned paths, sorted.
    :rtype: list[str]
    """
    contents = {path: text for path, text in files.items() if is_content(path)}
    extra = "\n".join(external_texts or [])
    orphans = []
    for path in sorted(p for p in files if not is_exempt(p) and "__pycache__" not in PurePosixPath(p).parts):
        others = "\n".join(text for other, text in contents.items() if other != path) + "\n" + extra
        if PurePosixPath(path).stem not in others:
            orphans.append(path)
    return orphans


def find_broken_links(files: dict[str, str]) -> list[str]:
    """Return the ``reference/`` paths SKILL.md names that aren't among the skill's files.

    :param files: The skill's ``/``-form paths mapped to their text.
    :type files: dict[str, str]
    :return: Broken reference paths, in the order SKILL.md names them.
    :rtype: list[str]
    """
    return [link for link in REFERENCE_LINK.findall(files.get("SKILL.md", "")) if link not in files]


def find_eager_imports(skill_md: str) -> list[str]:
    """Return SKILL.md's ``@``-import lines, ignoring fenced code blocks.

    :param skill_md: SKILL.md's text.
    :type skill_md: str
    :return: The stripped lines that would load a file on every run.
    :rtype: list[str]
    """
    imports, in_fence = [], False
    for line in skill_md.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if not in_fence and re.match(r"^\s*@\S", line):
            imports.append(line.strip())
    return imports
