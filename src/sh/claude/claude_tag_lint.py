#!/usr/bin/env python3
"""Tier 1 tag lint validator for Claude components.

Scans SKILL.md files (and any other .md file that declares a maturity key) for
mandatory Tier 1 tags as defined in the Claude component tag schema. Run manually
before committing new or updated components.

Usage:
    python3 src/sh/claude/claude_tag_lint.py          # scan src/claude/ (default)
    python3 src/sh/claude/claude_tag_lint.py <root>   # scan an explicit root dir
    make lint_tags                                      # via Makefile target

Exit codes:
    0 — all components pass (warnings allowed)
    1 — one or more components have FAIL-level issues
"""

import argparse
import sys
from datetime import date
from pathlib import Path

import frontmatter

# ── valid values ──────────────────────────────────────────────────────────────

VALID_MATURITY = {"draft", "tactical", "strategic"}
VALID_CRITICALITY = {"must", "should", "could", "want"}
VALID_STATUS = {"active", "dormant", "deprecated", "wip"}
STALENESS_WARN_DAYS = 90

# ── script location ───────────────────────────────────────────────────────────

# Script lives at src/sh/claude/; repo root is three levels up.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_ROOT = _REPO_ROOT / "src" / "claude"


# ── validation logic ──────────────────────────────────────────────────────────


def validate_component(metadata: dict) -> tuple[list[str], list[str]]:
    """Validate Tier 1 tags in a component's frontmatter metadata.

    Checks for presence and valid values of: maturity, tags.criticality,
    tags.status, and tags.tested. Also emits warnings for untested must/should
    components and stale or absent last-reviewed dates.

    :param metadata: Parsed YAML frontmatter as a plain dict.
    :type metadata: dict
    :return: Tuple of (failures, warnings). Failures block; warnings are advisory.
    :rtype: tuple[list[str], list[str]]
    """
    failures: list[str] = []
    warnings: list[str] = []

    # ── maturity ──────────────────────────────────────────────────────────────
    maturity = metadata.get("maturity")
    if maturity is None:
        failures.append("maturity: missing")
    elif maturity not in VALID_MATURITY:
        failures.append(f"maturity: invalid value '{maturity}' (expected: draft | tactical | strategic)")

    # ── tags block ────────────────────────────────────────────────────────────
    tags_raw = metadata.get("tags")
    tags: dict = tags_raw if isinstance(tags_raw, dict) else {}

    # criticality
    criticality = tags.get("criticality")
    if criticality is None:
        failures.append("tags.criticality: missing")
    elif criticality not in VALID_CRITICALITY:
        failures.append(
            f"tags.criticality: invalid value '{criticality}' (expected: must | should | could | want)"
        )

    # status
    status = tags.get("status")
    if status is None:
        failures.append("tags.status: missing")
    elif status not in VALID_STATUS:
        failures.append(
            f"tags.status: invalid value '{status}' (expected: active | dormant | deprecated | wip)"
        )

    # tested — YAML parses `false`/`true` as Python bool; accept both bool and string form
    tested_raw = tags.get("tested")
    if tested_raw is None:
        failures.append("tags.tested: missing")
    else:
        tested = _normalise_bool(tested_raw)
        if tested is None:
            failures.append(f"tags.tested: invalid value '{tested_raw}' (expected: true | false)")
        else:
            if criticality in {"must", "should"} and not tested:
                warnings.append(
                    f"tags.tested is false for criticality:{criticality} — consider adding test coverage"
                )

    # ── last-reviewed ─────────────────────────────────────────────────────────
    last_reviewed = metadata.get("last-reviewed")
    if last_reviewed is None:
        if criticality in {"must", "should"}:
            warnings.append("last-reviewed: not set (recommended for must/should components)")
    else:
        _check_staleness(last_reviewed, warnings)

    return failures, warnings


def _normalise_bool(value: object) -> bool | None:
    """Normalise a YAML bool field to Python bool, accepting string forms.

    :param value: Raw value from frontmatter (bool or string).
    :type value: object
    :return: True, False, or None if the value is not a recognisable boolean.
    :rtype: bool | None
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return None


def _check_staleness(last_reviewed: object, warnings: list[str]) -> None:
    """Append a warning if last-reviewed is older than STALENESS_WARN_DAYS.

    :param last_reviewed: Raw last-reviewed value from frontmatter.
    :type last_reviewed: object
    :param warnings: List to append any warning messages to.
    :type warnings: list[str]
    """
    try:
        reviewed_date = last_reviewed if isinstance(last_reviewed, date) else date.fromisoformat(str(last_reviewed))
        age_days = (date.today() - reviewed_date).days
        if age_days > STALENESS_WARN_DAYS:
            warnings.append(f"last-reviewed: {last_reviewed} is {age_days} days ago (>{STALENESS_WARN_DAYS} days)")
    except (ValueError, TypeError):
        warnings.append(f"last-reviewed: could not parse date '{last_reviewed}'")


# ── file discovery ────────────────────────────────────────────────────────────


def find_components(root: Path) -> list[Path]:
    """Discover components to validate under root.

    Always includes every SKILL.md found at any depth. Also includes any other
    .md file (excluding READMEs) that declares a maturity key in its frontmatter
    — this picks up agents, rules, and process files once they adopt the schema.

    :param root: Root directory to search.
    :type root: Path
    :return: Sorted list of component file paths.
    :rtype: list[Path]
    """
    skill_files: set[Path] = set(root.rglob("SKILL.md"))
    other_tagged: set[Path] = set()

    for p in root.rglob("*.md"):
        if p in skill_files or p.name == "README.md":
            continue
        try:
            post = frontmatter.load(str(p))
            if "maturity" in post.metadata:
                other_tagged.add(p)
        except Exception:  # noqa: BLE001 — skip unreadable files silently
            pass

    return sorted(skill_files | other_tagged)


# ── output helpers ────────────────────────────────────────────────────────────


def _rel(path: Path, root: Path) -> str:
    """Return a display-friendly relative path string.

    :param path: Absolute path to the component file.
    :type path: Path
    :param root: Root used for the scan (to make paths relative to).
    :type root: Path
    :return: Relative path string, falling back to the full path on failure.
    :rtype: str
    """
    try:
        return str(path.relative_to(root.parent))
    except ValueError:
        return str(path)


# ── entry point ───────────────────────────────────────────────────────────────


def main() -> int:
    """Run the tag lint scan and print a summary report.

    :return: Exit code — 0 if all components pass, 1 if any FAILs found.
    :rtype: int
    """
    parser = argparse.ArgumentParser(
        description="Validate Tier 1 tags on Claude components.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=str(DEFAULT_ROOT),
        help=f"Root directory to scan (default: {DEFAULT_ROOT})",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"error: root directory not found: {root}", file=sys.stderr)
        return 1

    components = find_components(root)
    if not components:
        print(f"No components found under {root}")
        return 0

    print(f"Scanning {len(components)} component(s) under {_rel(root, root)}...\n")

    n_clean = 0
    n_warn_only = 0
    n_fail = 0

    for path in components:
        try:
            post = frontmatter.load(str(path))
            metadata = dict(post.metadata)
        except Exception as exc:
            print(f"{_rel(path, root)}")
            print(f"  FAIL  could not parse frontmatter: {exc}\n")
            n_fail += 1
            continue

        failures, warnings = validate_component(metadata)

        if not failures and not warnings:
            n_clean += 1
            continue

        print(_rel(path, root))
        for msg in failures:
            print(f"  FAIL  {msg}")
        for msg in warnings:
            print(f"  WARN  {msg}")
        print()

        if failures:
            n_fail += 1
        else:
            n_warn_only += 1

    # summary
    print(f"{'─' * 60}")
    print(f"  Scanned   {len(components)} component(s)")
    print(f"  Clean     {n_clean}")
    if n_warn_only:
        print(f"  Warnings  {n_warn_only} component(s) — advisory only")
    if n_fail:
        print(f"  Failures  {n_fail} component(s) — must be fixed\n")
        print("Exit: 1 — fix FAILs before merging")
        return 1

    print()
    print("Exit: 0 — all components pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
