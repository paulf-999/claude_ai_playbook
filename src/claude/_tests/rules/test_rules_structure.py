# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-02
# Version:           2.0.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests that every _rules/ file meets the per-file format standards.

- **Size:** at most 110 lines (the 3-line metadata header doesn't count) and one trailing newline.
- **Headings:** an H1 and every ``##`` heading carry an emoji, per writing_style.md.
- **Context budget:** no Related section, and a Contents section only with 3+ real headings,
  in ``_rules/`` and ``_reference/`` (#120, #121).

``test_rules_structure_layout.py`` covers where files live and how they import each other.
"""
from __future__ import annotations

import re
from pathlib import Path

from _shared_paths import CLAUDE_DIR, RULES_DIR

REFERENCE_DIR = CLAUDE_DIR / "_reference"
RELATED_HEADING = re.compile(r"^## .*Related", re.MULTILINE)
REFERENCES_SECTION = re.compile(r"^## .*References.*\n(?:(?!## ).*\n?)*", re.MULTILINE)
H2_HEADING = re.compile(r"^## (.+)$", re.MULTILINE)
CONTENTS_MIN_HEADINGS = 3
LINE_LIMIT = 110


def rule_files() -> list[Path]:
    """Return all .md files in _rules/ eligible for quality checks.

    Excludes README.md (documentation, not a rule file) and anything
    under 05_lazy_load/ (different standards apply there).

    :return: List of rule markdown files to validate.
    :rtype: list[Path]
    """
    return [
        rule_file for rule_file in RULES_DIR.rglob("*.md")
        if rule_file.name != "README.md" and "05_lazy_load" not in rule_file.parts
    ]


def body_lines(text: str) -> list[str]:
    """Return a rule's lines without its 3-line metadata header.

    :param text: Full file content.
    :type text: str
    :return: The lines that count toward the line limit.
    :rtype: list[str]
    """
    lines = text.splitlines()
    return lines[3:] if lines and lines[0].startswith("<!-- version:") else lines


def h2_headings_without_emoji(text: str) -> list[str]:
    """Return the ``##`` headings outside code fences that carry no emoji.

    :param text: Full file content.
    :type text: str
    :return: Offending heading lines, in file order.
    :rtype: list[str]
    """
    missing, in_fence = [], False
    for line in text.splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            continue
        if not in_fence and line.startswith("## ") and not any(ord(char) > 127 for char in line[3:]):
            missing.append(line)
    return missing


def has_internal_link_section(text: str) -> bool:
    """Return True for a Related section, or a References section that lists config files.

    A References section of external URLs (e.g. vendor docs) is legitimate
    content; one that names other .md files is a Related section by another name.

    :param text: The markdown file's content.
    :type text: str
    :return: Whether the file carries parent/sibling links that belong in a README.
    :rtype: bool
    """
    if RELATED_HEADING.search(text):
        return True
    return any(".md" in section for section in REFERENCES_SECTION.findall(text))


def imported_content_files() -> list[Path]:
    """Return every .md file under _rules/ and _reference/ that can be @import-ed.

    Wider than rule_files(): includes 05_lazy_load/ and _reference/, since a
    lazy-loaded rule costs the same context once it is read. Excludes READMEs
    (never imported — they are where Related links now live).

    :return: Markdown files subject to the context-budget checks.
    :rtype: list[Path]
    """
    return [
        md_file
        for base in (RULES_DIR, REFERENCE_DIR)
        for md_file in base.rglob("*.md")
        if md_file.name != "README.md"
    ]


def test_rule_files_found():
    """The scan finds rule files and skips READMEs and 05_lazy_load/."""
    files = rule_files()
    assert files, f"no rule files found under {RULES_DIR}"
    leaked = [f for f in files if f.name == "README.md" or "05_lazy_load" in f.parts]
    assert not leaked, f"READMEs or lazy-load files leaked into the scan: {leaked}"


def test_line_limits():
    """No _rules/ file (excluding README and 05_lazy_load) exceeds 110 lines, header aside."""
    counts = {f.name: len(body_lines(f.read_text())) for f in rule_files()}
    over = [f"{name}: {count}" for name, count in counts.items() if count > LINE_LIMIT]
    assert not over, f"files over {LINE_LIMIT} lines — split into a parent and children: {over}"


def test_metadata_header_is_not_counted():
    """The 3-line metadata header is left out of the line count."""
    text = "<!-- version: 1.0.0 -->\n<!-- created: x -->\n<!-- updated: x -->\n# 🧪 Title\nbody\n"
    assert body_lines(text) == ["# 🧪 Title", "body"], f"got {body_lines(text)}"


def test_files_end_with_single_newline():
    """Every _rules/ file ends with exactly one newline."""
    for rule_file in rule_files():
        raw = rule_file.read_bytes()
        assert raw.endswith(b"\n"), f"{rule_file.name}: does not end with a newline"
        assert not raw.endswith(b"\n\n"), f"{rule_file.name}: ends with multiple newlines"


def test_h1_heading_present():
    """Every _rules/ file has an H1 heading."""
    missing = [f.name for f in rule_files() if not re.search(r"^# .+", f.read_text(), re.MULTILINE)]
    assert not missing, f"files with no H1 heading: {missing}"


def test_h1_heading_has_emoji():
    """Every _rules/ file's H1 heading includes an emoji."""
    bare = []
    for rule_file in rule_files():
        h1 = re.search(r"^# (.+)", rule_file.read_text(), re.MULTILINE)
        if h1 and not any(ord(char) > 127 for char in h1.group(1)):
            bare.append(f"{rule_file.name}: '# {h1.group(1)}'")
    assert not bare, f"H1 headings with no emoji: {bare}"


def test_h2_headings_have_emoji():
    """Every ``##`` heading in a _rules/ file includes an emoji, per writing_style.md."""
    bad = [
        f"{rule_file.relative_to(RULES_DIR)}: '{heading}'"
        for rule_file in rule_files()
        for heading in h2_headings_without_emoji(rule_file.read_text())
    ]
    assert not bad, f"## headings with no emoji — add one at the start of each: {bad}"


def test_h2_emoji_check_flags_bare_headings_and_skips_fences():
    """The detector flags a bare ## heading but ignores emoji headings and fenced examples."""
    text = "## 🎯 Good\n## Bad\n```\n## Fenced example\n```\n"
    assert h2_headings_without_emoji(text) == ["## Bad"], "Detector missed a bare heading or flagged a fenced one"


def test_h2_emoji_check_handles_tilde_fences():
    """Headings inside ~~~ fences are skipped too, and checking resumes after the fence."""
    text = "~~~\n## Fenced\n~~~\n## After\n"
    assert h2_headings_without_emoji(text) == ["## After"], f"got {h2_headings_without_emoji(text)}"


def test_no_related_section_outside_readmes():
    """Related links live in the tier README, not the always-on rule file (#121)."""
    offenders = [
        str(md_file.relative_to(CLAUDE_DIR))
        for md_file in imported_content_files()
        if has_internal_link_section(md_file.read_text())
    ]
    assert not offenders, (
        f"{len(offenders)} file(s) have a Related section (or a References section of .md links) — "
        f"move the links to the tier README under '🔗 Related rules': {sorted(offenders)}"
    )


def test_contents_section_only_with_three_real_headings():
    """A Contents section must only appear when the file has 3+ other ## headings (#120)."""
    offenders = []
    for md_file in imported_content_files():
        headings = H2_HEADING.findall(md_file.read_text())
        if not any("Contents" in heading for heading in headings):
            continue
        real = [h for h in headings if "Contents" not in h and "Related" not in h]
        if len(real) < CONTENTS_MIN_HEADINGS:
            offenders.append(f"{md_file.relative_to(CLAUDE_DIR)} ({len(real)} headings)")
    assert not offenders, (
        f"Contents section on file(s) with fewer than {CONTENTS_MIN_HEADINGS} real ## headings "
        f"— drop the Contents block: {sorted(offenders)}"
    )


def test_link_section_check_allows_external_references():
    """A References section of URLs is content, but one listing .md files or a Related heading is not."""
    assert not has_internal_link_section("## 📚 References\n- https://example.com\n"), "URL references are allowed"
    assert has_internal_link_section("## 📚 References\n- `git.md`\n"), (
        "a References list of .md files is a Related section"
    )
    assert has_internal_link_section("## 🔗 Related rules\n- anything\n"), "a Related heading must be flagged"
