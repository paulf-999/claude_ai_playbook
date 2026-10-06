"""Finds files under ``rules/`` that would load wrongly, and on-demand pointers that lead nowhere.

Claude Code loads every ``.md`` under ``rules/`` on its own — in every session, or only
when a matching file is open if the file has ``paths:`` frontmatter. So the folder, not an
``@import`` chain, decides what loads. ``find_native_load_issues`` reports what breaks that:

- **readme:** a ``README.md`` under ``rules/``, which would load every session.
- **lazy_folder:** a ``_lazy_load/`` folder under ``rules/``, whose on-demand children would load anyway.
- **import:** an ``@~/...`` import line under ``rules/``, which the native loader makes redundant.
- **unscoped:** a file in ``rules/05_path_scoped/`` without ``paths:``, which would load every session.
- **pointer:** a ``**Read on demand:**`` pointer under ``rules/`` naming a file that doesn't exist.

Tests: ``rules/02_claude_standards/test_always_on_reachability.py`` runs it over the
real config, and ``test_rule_reachability.py`` proves it on small fake rule trees.
"""
from __future__ import annotations

import re
from pathlib import Path

PATH_SCOPED_DIR = "05_path_scoped"
POINTER = re.compile(r"\*\*Read on demand:\*\*\s*\[?`~/[^/`]+/([^`]+\.md)`")


def has_paths_frontmatter(text: str) -> bool:
    """Say whether a file opens with a frontmatter block containing ``paths:``.

    :param text: The file's full text.
    :type text: str
    :return: True when the opening ``---`` block has a ``paths:`` key.
    :rtype: bool
    """
    lines = text.split("\n")
    if not lines or lines[0] != "---":
        return False
    for line in lines[1:]:
        if line == "---":
            return False
        if line.startswith("paths:"):
            return True
    return False


def find_native_load_issues(rules_root: Path) -> dict[str, list[str]]:
    """Scan a ``rules/`` folder for files that would load wrongly and pointers that lead nowhere.

    :param rules_root: The ``rules/`` folder; its parent is the config directory pointers resolve against.
    :type rules_root: Path
    :return: Problem paths by kind: readme, lazy_folder, import, unscoped, pointer.
    :rtype: dict[str, list[str]]
    """
    issues: dict[str, list[str]] = {k: [] for k in ("readme", "lazy_folder", "import", "unscoped", "pointer")}
    config_dir = rules_root.parent
    for path in sorted(rules_root.rglob("*")):
        rel = path.relative_to(config_dir).as_posix()
        if path.is_dir():
            if path.name == "_lazy_load":
                issues["lazy_folder"].append(rel)
            continue
        if path.suffix != ".md":
            continue
        if path.name == "README.md":
            issues["readme"].append(rel)
        text = path.read_text(errors="ignore")
        if re.search(r"^@~/\S+", text, re.M):
            issues["import"].append(rel)
        if PATH_SCOPED_DIR in path.relative_to(rules_root).parts and not has_paths_frontmatter(text):
            issues["unscoped"].append(rel)
        issues["pointer"] += [f"{rel} -> {t}" for t in POINTER.findall(text) if not (config_dir / t).is_file()]
    return issues
