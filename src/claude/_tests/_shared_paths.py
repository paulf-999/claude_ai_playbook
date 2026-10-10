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


def lazy_rules_dir(config_dir: Path) -> Path:
    """Find the on-demand rules folder: beside ``rules/`` once installed, inside it in the repo.

    :param config_dir: The Claude config directory, installed or the repo's ``src/claude``.
    :return: ``<config_dir>/_rules_lazy_load`` when it exists, else ``<config_dir>/rules/_rules_lazy_load``.
    """
    installed = config_dir / LAZY_RULES_NAME
    return installed if installed.is_dir() else config_dir / "rules" / LAZY_RULES_NAME


def resolve_config_path(config_dir: Path, rel: str) -> Path:
    """Turn a path relative to the installed config, e.g. from a pointer, into a real file path.

    :param config_dir: The Claude config directory.
    :param rel: A path such as ``_rules_lazy_load/org.md`` or ``rules/01_essentials/x.md``.
    :return: The path on disk, with ``_rules_lazy_load/`` mapped to wherever that folder sits.
    """
    head, _, rest = rel.partition("/")
    return lazy_rules_dir(config_dir) / rest if head == LAZY_RULES_NAME else config_dir / rel


def resolve_link(source: Path, target: str) -> Path:
    """Resolve a relative markdown link, written for the repo layout, in either layout.

    Links follow the repo, where ``_rules_lazy_load/`` sits inside ``rules/``. In an installed
    config the folder sits beside ``rules/``, so the source is placed where the repo keeps it,
    the link is followed there, and the result is mapped back.

    :param source: The file holding the link.
    :param target: The link target, without any ``#anchor``.
    :return: The absolute path the link reaches, existing or not.
    """
    direct = (source.parent / target).resolve()
    beside = (p.parent for p in source.parents if p.name == LAZY_RULES_NAME and p.parent.name != "rules")
    config_dir = next(beside, None)
    config_dir = config_dir or next((p.parent for p in source.parents if p.name == "rules"), None)
    if direct.exists() or config_dir is None or not (config_dir / LAZY_RULES_NAME).is_dir():
        return direct
    installed, repo = (config_dir / LAZY_RULES_NAME).resolve(), (config_dir / "rules" / LAZY_RULES_NAME).resolve()
    src = source.resolve()
    repo_source = repo / src.relative_to(installed) if installed in src.parents else src
    reached = (repo_source.parent / target).resolve()
    return installed / reached.relative_to(repo) if repo in reached.parents else reached


def native_rule_files(rules_dir: Path, pattern: str = "*.md") -> list[Path]:
    """List files under ``rules/`` that Claude Code loads natively, leaving out the repo's lazy folder.

    :param rules_dir: A ``rules/`` folder.
    :param pattern: Glob for ``rglob``.
    :return: Matching paths, sorted, outside ``rules/_rules_lazy_load/``.
    """
    lazy = rules_dir / LAZY_RULES_NAME
    return sorted(p for p in rules_dir.rglob(pattern) if lazy not in p.parents and p != lazy)


LAZY_RULES_DIR = lazy_rules_dir(CLAUDE_DIR)
