"""Finds rule files that CLAUDE.md never reaches through its ``@import`` chain.

``find_reachability_issues`` walks every ``@~/<config-dir>/...`` import from the entry
files and reports imports that point nowhere and rule files nothing imports. It skips
``05_lazy_load/`` and per-parent ``_lazy_load/`` folders, which are read on demand.

Tests: ``rules/02_claude_standards/test_always_on_reachability.py`` runs it over the
real config, and ``test_rule_reachability.py`` proves it on small fake rule trees.
"""
from __future__ import annotations

from pathlib import Path


def find_reachability_issues(rules_root: Path, entry_files: list[Path]) -> tuple[list[str], list[str]]:
    """Walk `@import` chains from the given entry files and report gaps.

    :param rules_root: The root directory whose .md tree is being audited.
    :type rules_root: Path
    :param entry_files: Files to start the import walk from (e.g. CLAUDE.md).
    :type entry_files: list[Path]
    :return: A tuple of (broken import targets, orphaned files never reached).
    :rtype: tuple[list[str], list[str]]
    """
    all_md = {
        p.resolve() for p in rules_root.rglob("*.md")
        if p.name != "README.md"
        # Match "template" only below rules_root: a checkout path such as
        # ~/git/repo_template/ must not hide every rule file from the scan.
        and "template" not in str(p.relative_to(rules_root)).lower()
        and "05_lazy_load" not in p.parts
        # A parent may keep on-demand children beside it in a `_lazy_load/`
        # folder — never imported by design, so never an orphan.
        and "_lazy_load" not in p.relative_to(rules_root).parts
    }
    visited: set[Path] = set()
    broken: list[str] = []
    queue = list(entry_files)

    while queue:
        current = queue.pop()
        if not current.exists():
            broken.append(str(current))
            continue
        resolved = current.resolve()
        if resolved in visited:
            continue
        visited.add(resolved)
        for line in current.read_text(errors="ignore").splitlines():
            stripped = line.strip()
            if not stripped.startswith("@~/") or "/" not in stripped[len("@~/"):]:
                continue
            # "@~/<config-dir-name>/rest" — the config-dir-name varies (.claude,
            # claude, a repo checkout); strip both segments, resolve against
            # rules_root.parent. Never assume which convention is in play.
            rest = stripped[len("@~/"):].split("/", 1)[1]
            target = rules_root.parent / rest
            if target.exists():
                queue.append(target)
            else:
                broken.append(f"{current} -> {target}")

    orphaned = sorted(str(p.relative_to(rules_root.parent)) for p in all_md if p not in visited)
    return broken, orphaned
