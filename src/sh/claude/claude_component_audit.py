#!/usr/bin/env python3
"""Periodic health check for the Claude component library.

Scans all .md files under src/claude/ (skills, agents, rules, process, commands)
and produces a structured health report. Components with YAML frontmatter containing
a 'maturity' key are fully analysed for health signals. All others are counted as
untagged and grouped by directory.

Unlike the lint validator (claude_tag_lint.py), this script:
  - Is not a CI gate — always exits 0
  - Reports untagged components (agents, rules, process docs not yet on the schema)
  - Checks health signals: dormant+critical, untested+critical, stale/missing
    review dates, deprecated components, and broken depends-on chains

Usage:
    python3 src/sh/claude/claude_component_audit.py          # scan src/claude/
    python3 src/sh/claude/claude_component_audit.py <root>   # explicit root
    make audit_components                                      # via Makefile target
"""

import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

import frontmatter

# ── constants ─────────────────────────────────────────────────────────────────

SCAN_DIRS = ["skills", "agents", "rules", "process", "commands"]
EXCLUDE_DIRS = {"style_guide_standards", "skills_wip", "patches"}
EXCLUDE_NAMES = {"README.md"}
STALENESS_WARN_DAYS = 90

# Script lives at src/sh/claude/; repo root is three levels up.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_ROOT = _REPO_ROOT / "src" / "claude"


# ── file discovery ────────────────────────────────────────────────────────────


def find_all_components(root: Path) -> tuple[list[Path], list[Path]]:
    """Discover all component files under root, split into tagged and untagged.

    Tagged: any .md with a 'maturity' key in frontmatter.
    Untagged: all other .md files in scope.

    :param root: Root directory to search (e.g. src/claude/).
    :type root: Path
    :return: Tuple of (tagged_paths, untagged_paths), both sorted.
    :rtype: tuple[list[Path], list[Path]]
    """
    tagged: list[Path] = []
    untagged: list[Path] = []

    for scan_dir_name in SCAN_DIRS:
        scan_dir = root / scan_dir_name
        if not scan_dir.exists():
            continue
        for p in sorted(scan_dir.rglob("*.md")):
            if p.name in EXCLUDE_NAMES:
                continue
            if any(part in EXCLUDE_DIRS for part in p.parts):
                continue
            try:
                post = frontmatter.load(str(p))
                if "maturity" in post.metadata:
                    tagged.append(p)
                else:
                    untagged.append(p)
            except Exception:  # noqa: BLE001 — skip unreadable files silently
                untagged.append(p)

    return sorted(tagged), sorted(untagged)


def _collect_names(tagged: list[Path]) -> set[str]:
    """Build the set of known component names from tagged components' frontmatter.

    :param tagged: List of tagged component file paths.
    :type tagged: list[Path]
    :return: Set of name values declared in frontmatter.
    :rtype: set[str]
    """
    names: set[str] = set()
    for p in tagged:
        try:
            post = frontmatter.load(str(p))
            name = post.metadata.get("name")
            if name:
                names.add(str(name))
        except Exception:  # noqa: BLE001
            pass
    return names


# ── health checks ─────────────────────────────────────────────────────────────


def check_health(metadata: dict, known_names: set[str]) -> dict[str, str | None]:
    """Check a tagged component's metadata for health signals.

    :param metadata: Parsed YAML frontmatter as a plain dict.
    :type metadata: dict
    :param known_names: Set of all known component names for depends-on validation.
    :type known_names: set[str]
    :return: Dict mapping signal keys to detail strings, or None if signal absent.
             Keys: DORMANT, UNTESTED, NO_REVIEW, STALE, DEPRECATED, BROKEN_DEP
    :rtype: dict[str, str | None]
    """
    signals: dict[str, str | None] = {
        "DORMANT": None,
        "UNTESTED": None,
        "NO_REVIEW": None,
        "STALE": None,
        "DEPRECATED": None,
        "BROKEN_DEP": None,
    }

    tags: dict = metadata.get("tags") or {}
    criticality = tags.get("criticality", "")
    status = tags.get("status", "")
    tested_raw = tags.get("tested")
    last_reviewed = metadata.get("last-reviewed")
    depends_on = metadata.get("depends-on") or []

    # Dormant + high criticality
    if status == "dormant" and criticality in {"must", "should"}:
        signals["DORMANT"] = f"[criticality: {criticality}, status: dormant]"

    # Untested + high criticality
    if tested_raw is not None:
        tested = _normalise_bool(tested_raw)
        if tested is False and criticality in {"must", "should"}:
            signals["UNTESTED"] = f"[criticality: {criticality}, tested: false]"

    # Deprecated
    if status == "deprecated":
        signals["DEPRECATED"] = f"[criticality: {criticality or 'unset'}]"

    # Missing review date for high-criticality
    if last_reviewed is None and criticality in {"must", "should"}:
        signals["NO_REVIEW"] = f"[criticality: {criticality}]"

    # Stale review date
    if last_reviewed is not None:
        stale_msg = _check_staleness(last_reviewed)
        if stale_msg:
            signals["STALE"] = stale_msg

    # Broken depends-on
    if depends_on:
        broken = [dep for dep in depends_on if str(dep) not in known_names]
        if broken:
            signals["BROKEN_DEP"] = f"[unknown: {', '.join(str(d) for d in broken)}]"

    return signals


def _normalise_bool(value: object) -> bool | None:
    """Normalise a YAML bool field to Python bool, accepting string forms.

    :param value: Raw value from frontmatter (bool or string).
    :type value: object
    :return: True, False, or None if not a recognisable boolean.
    :rtype: bool | None
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return None


def _check_staleness(last_reviewed: object) -> str | None:
    """Return a stale warning string if last-reviewed exceeds STALENESS_WARN_DAYS.

    :param last_reviewed: Raw last-reviewed value from frontmatter.
    :type last_reviewed: object
    :return: Warning string if stale, None otherwise.
    :rtype: str | None
    """
    try:
        reviewed_date = (
            last_reviewed if isinstance(last_reviewed, date) else date.fromisoformat(str(last_reviewed))
        )
        age_days = (date.today() - reviewed_date).days
        if age_days > STALENESS_WARN_DAYS:
            return f"[last-reviewed: {last_reviewed}, {age_days}d ago]"
    except (ValueError, TypeError):
        return f"[last-reviewed: unparseable value '{last_reviewed}']"
    return None


# ── output helpers ────────────────────────────────────────────────────────────


def _rel(path: Path, root: Path) -> str:
    """Return a display-friendly relative path string.

    :param path: Absolute file path.
    :type path: Path
    :param root: Scan root for relativising.
    :type root: Path
    :return: Relative path string.
    :rtype: str
    """
    try:
        return str(path.relative_to(root.parent))
    except ValueError:
        return str(path)


def _top_dir(path: Path, root: Path) -> str:
    """Return the top-level SCAN_DIR name for a path under root.

    :param path: File path under root.
    :type path: Path
    :param root: Scan root.
    :type root: Path
    :return: Top-level directory name, e.g. 'agents', 'rules'.
    :rtype: str
    """
    try:
        rel = path.relative_to(root)
        return rel.parts[0]
    except (ValueError, IndexError):
        return "other"


# ── report ────────────────────────────────────────────────────────────────────


def build_report(root: Path) -> None:
    """Orchestrate scan, health checks, and printed report.

    :param root: Root directory to scan (e.g. src/claude/).
    :type root: Path
    """
    tagged, untagged = find_all_components(root)
    known_names = _collect_names(tagged)

    # Collect all health signals grouped by type
    signal_groups: dict[str, list[tuple[str, str]]] = defaultdict(list)

    for path in tagged:
        try:
            post = frontmatter.load(str(path))
            metadata = dict(post.metadata)
        except Exception:  # noqa: BLE001
            continue

        signals = check_health(metadata, known_names)
        display = _rel(path, root)

        for key, detail in signals.items():
            if detail is not None:
                signal_groups[key].append((display, detail))

    total_signals = sum(len(v) for v in signal_groups.values())

    # ── header ────────────────────────────────────────────────────────────────
    print(f"\n{'=' * 52}")
    print(f"  Claude Component Audit — {date.today()}")
    print(f"{'=' * 52}\n")

    # ── summary ───────────────────────────────────────────────────────────────
    print("SUMMARY")
    print(f"  Scanned:        {len(tagged) + len(untagged)} components")
    print(f"  Tagged:         {len(tagged)}  |  Untagged: {len(untagged)}")
    print(f"  Health signals: {total_signals}\n")

    # ── untagged breakdown ────────────────────────────────────────────────────
    if untagged:
        by_dir: dict[str, int] = defaultdict(int)
        for p in untagged:
            by_dir[_top_dir(p, root)] += 1

        print(f"UNTAGGED COMPONENTS ({len(untagged)})")
        for dir_name in SCAN_DIRS:
            count = by_dir.get(dir_name, 0)
            if count:
                print(f"  {dir_name + '/':<14}{count}")
        print()

    # ── health signals ────────────────────────────────────────────────────────
    print("HEALTH SIGNALS\n")

    _print_signal_section(signal_groups, "DORMANT", "⚠  DORMANT + must/should")
    _print_signal_section(signal_groups, "UNTESTED", "⚠  UNTESTED + must/should")
    _print_signal_section(signal_groups, "NO_REVIEW", "⚠  MISSING REVIEW DATE + must/should")
    _print_signal_section(signal_groups, "STALE", f"⚠  STALE REVIEW >{STALENESS_WARN_DAYS}d")
    _print_signal_section(signal_groups, "BROKEN_DEP", "⚠  BROKEN DEPENDS-ON")
    _print_signal_section(signal_groups, "DEPRECATED", "ℹ  DEPRECATED — ready for removal")


def _print_signal_section(
    signal_groups: dict[str, list[tuple[str, str]]],
    key: str,
    label: str,
) -> None:
    """Print one health signal section.

    :param signal_groups: Collected signals grouped by key.
    :type signal_groups: dict[str, list[tuple[str, str]]]
    :param key: Signal key to look up.
    :type key: str
    :param label: Display label for this signal type.
    :type label: str
    """
    entries = signal_groups.get(key, [])
    print(f"  {label} ({len(entries)})")
    for display_path, detail in entries:
        print(f"     {display_path}  {detail}")
    print()


# ── entry point ───────────────────────────────────────────────────────────────


def main() -> int:
    """Run the component audit and print the health report.

    :return: Always 0 — this tool is informational, not a CI gate.
    :rtype: int
    """
    root_arg = sys.argv[1] if len(sys.argv) > 1 else str(DEFAULT_ROOT)
    root = Path(root_arg).resolve()

    if not root.exists():
        print(f"error: root directory not found: {root}", file=sys.stderr)
        return 1

    build_report(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
