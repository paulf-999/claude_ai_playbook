"""Shared Claude config path constants for the test suite.

Single source of truth for locating the Claude config directory under
test, plus the handful of path constants that were independently
redeclared with identical values across multiple test files. Override
CLAUDE_DIR via CLAUDE_CONFIG_DIR (e.g. CI points this at the repo's own
src/claude/ instead of a real ~/.claude install).

Test-specific paths used by only one test file (e.g. a single rule's
file path) stay declared locally in that file — centralizing them here
would add indirection without removing any duplication.
"""
from __future__ import annotations

import os
from pathlib import Path

CLAUDE_DIR = Path(os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude")))

CLAUDE_MD = CLAUDE_DIR / "CLAUDE.md"
ALIASES_FILE = CLAUDE_DIR / "aliases.md"
SETTINGS_FILE = CLAUDE_DIR / "settings.json"
SKILLS_DIR = CLAUDE_DIR / "skills"
HOOKS_DIR = CLAUDE_DIR / "hooks"
RULES_DIR = CLAUDE_DIR / "rules"  # loaded natively by Claude Code
LAZY_RULES_NAME = "_rules_lazy_load"  # read on demand only
# Every style guide, read on demand except entry files once installed
STYLE_GUIDES_NAME = "_reference/_style_guide_standards"
ON_DEMAND_ROOTS = (LAZY_RULES_NAME, STYLE_GUIDES_NAME)  # installed folders read only when a pointer is followed

# Installed path prefix -> repo path prefix. The repo keeps on-demand rules inside rules/ and style-guide
# entry files with the rest of their guide; the install moves both (see claude_file_utils.sh).
INSTALLED_TO_REPO = (
    ("rules/02_claude_standards/path_scoped_rules/style_guide_standards/", f"{STYLE_GUIDES_NAME}/"),
    (f"{LAZY_RULES_NAME}/", f"rules/{LAZY_RULES_NAME}/"),
)


def lazy_rules_dir(config_dir: Path) -> Path:
    """Find the on-demand rules folder: beside ``rules/`` once installed, inside it in the repo.

    :param config_dir: The Claude config directory, installed or the repo's ``src/claude``.
    :return: ``<config_dir>/_rules_lazy_load`` when it exists, else ``<config_dir>/rules/_rules_lazy_load``.
    """
    installed = config_dir / LAZY_RULES_NAME
    return installed if installed.is_dir() else config_dir / "rules" / LAZY_RULES_NAME


def to_repo_path(rel: str) -> str:
    """Map a path relative to the installed config to where the repo keeps it.

    :param rel: A path such as ``_rules_lazy_load/org.md``.
    :return: The repo path, e.g. ``rules/_rules_lazy_load/org.md``, or ``rel`` when nothing moves it.
    """
    for installed, repo in INSTALLED_TO_REPO:
        if rel.startswith(installed):
            return repo + rel[len(installed):]
    return rel


def resolve_config_path(config_dir: Path, rel: str) -> Path:
    """Turn a path relative to the installed config, e.g. from a pointer, into a real file path.

    :param config_dir: The Claude config directory, installed or the repo's ``src/claude``.
    :param rel: A path such as ``_rules_lazy_load/org.md`` or ``rules/01_essentials/x.md``.
    :return: ``<config_dir>/<rel>`` when it exists, else where the repo keeps that file.
    """
    direct = config_dir / rel
    return direct if direct.exists() else config_dir / to_repo_path(rel)


def _config_dir_of(source: Path) -> Path | None:
    """Return the config folder a rule file sits in: the nearest parent holding ``rules/``."""
    return next((p for p in source.parents if (p / "rules").is_dir()), None)


def resolve_link(source: Path, target: str) -> Path:
    """Resolve a relative markdown link, written for the repo layout, in either layout.

    Links follow the repo. In an installed config the source is placed where the repo keeps it,
    the link is followed there, and the result is mapped to wherever the install put that file.

    :param source: The file holding the link.
    :param target: The link target, without any ``#anchor``.
    :return: The absolute path the link reaches, existing or not.
    """
    direct = (source.parent / target).resolve()
    config_dir = _config_dir_of(source)
    if direct.exists() or config_dir is None:
        return direct
    config_dir = config_dir.resolve()
    repo_source = config_dir / to_repo_path(source.resolve().relative_to(config_dir).as_posix())
    reached = (repo_source.parent / target).resolve()
    if config_dir not in reached.parents:
        return direct
    rel = reached.relative_to(config_dir).as_posix()
    candidates = [config_dir / (inst + rel[len(repo):]) for inst, repo in INSTALLED_TO_REPO if rel.startswith(repo)]
    return next((c for c in [reached, *candidates] if c.exists()), direct)


def frontmatter_has_paths(text: str) -> bool:
    """Return True when a file's opening YAML frontmatter has a ``paths:`` key.

    :param text: Full file content.
    :return: Whether Claude Code loads the file only on matching files.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    for line in lines[1:]:
        if line.strip() == "---":
            return False
        if line.startswith("paths:"):
            return True
    return False


def native_rule_files(rules_dir: Path, pattern: str = "*.md") -> list[Path]:
    """List files under ``rules/`` that Claude Code loads natively, leaving out the repo's lazy folder.

    :param rules_dir: A ``rules/`` folder.
    :param pattern: Glob for ``rglob``.
    :return: Matching paths, sorted, outside ``rules/_rules_lazy_load/``.
    """
    lazy = rules_dir / LAZY_RULES_NAME
    return sorted(p for p in rules_dir.rglob(pattern) if lazy not in p.parents and p != lazy)


def path_scoped_rule_files(config_dir: Path) -> list[Path]:
    """List the rules Claude Code loads on matching files: those with ``paths:`` frontmatter.

    :param config_dir: The Claude config directory, installed or the repo's ``src/claude``.
    :return: Native rule files with ``paths:``, plus, in the repo, style-guide entry files; sorted.
    """
    candidates = native_rule_files(config_dir / "rules") + sorted((config_dir / STYLE_GUIDES_NAME).rglob("*.md"))
    return sorted(p for p in candidates if frontmatter_has_paths(p.read_text(encoding="utf-8")))


def installed_rule_files(config_dir: Path, pattern: str = "*.md") -> dict[str, Path]:
    """Map each rule file's installed path, relative to the config, to where it sits on disk, in either layout.

    :param config_dir: The Claude config directory, installed or the repo's ``src/claude``.
    :param pattern: Glob for ``rglob``.
    :return: e.g. ``_reference/_style_guide_standards/sql/formatting.md`` -> its path; sorted by key.
    """
    found = {p.relative_to(config_dir).as_posix(): p for p in native_rule_files(config_dir / "rules", pattern)}
    lazy = lazy_rules_dir(config_dir)
    found |= {f"{LAZY_RULES_NAME}/{p.relative_to(lazy).as_posix()}": p for p in lazy.rglob(pattern)}
    guides = config_dir / STYLE_GUIDES_NAME
    for path in guides.rglob(pattern):
        # The install moves entry files with paths: under rules/ (split_style_guides in claude_file_utils.sh)
        rel = path.relative_to(guides).as_posix()
        scoped = path.is_file() and frontmatter_has_paths(path.read_text(encoding="utf-8", errors="ignore"))
        found[f"rules/02_claude_standards/path_scoped_rules/style_guide_standards/{rel}" if scoped else f"{STYLE_GUIDES_NAME}/{rel}"] = path
    return {rel: found[rel] for rel in sorted(found) if found[rel].is_file()}


def on_demand_rule_files(config_dir: Path, pattern: str = "*.md") -> dict[str, Path]:
    """Map each file read only on demand, in ``_rules_lazy_load/`` or the style guides, to its path.

    :param config_dir: The Claude config directory, installed or the repo's ``src/claude``.
    :param pattern: Glob for ``rglob``.
    :return: Installed path, relative to the config, mapped to the file on disk; sorted by key.
    """
    files = installed_rule_files(config_dir, pattern)
    return {rel: path for rel, path in files.items() if rel.startswith(tuple(f"{root}/" for root in ON_DEMAND_ROOTS))}


LAZY_RULES_DIR = lazy_rules_dir(CLAUDE_DIR)
