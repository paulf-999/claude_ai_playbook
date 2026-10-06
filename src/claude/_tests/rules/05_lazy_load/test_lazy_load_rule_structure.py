# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-06
# Version:           1.2.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Structural tests for the lazy-load rules that had no dedicated test.

Their scorecards average 4.9/10 for Test Coverage, the lowest dimension
anywhere (see ``quality_scorecards_summary.md``). This file guards six
things for each rule: its metadata header, its ``**Purpose:**`` line, its
key sections, that every child page is linked, that every relative link
resolves, and that each Contents entry matches a real heading.
"""
from __future__ import annotations

import re
from pathlib import Path

from _shared_paths import LAZY_RULES_DIR, RULES_DIR

PATH_SCOPED_DIR = RULES_DIR / "05_path_scoped"
STYLE_DIR = Path("style_guide_standards")

# Rule path (relative to rules/05_path_scoped/ or _rules_lazy_load/) -> H2 headings it must keep, emoji stripped.
RULES: dict[Path, list[str]] = {
    Path("org.md"): ["Child pages", "Organisation facts", "Internal references"],
    STYLE_DIR / "airflow.md": ["Child pages", "Core Principles", "DAG Acceptance Checklist"],
    STYLE_DIR / "utilities" / "datetime.md": ["Standard formats", "Timezone", "Known exceptions"],
    STYLE_DIR / "infra" / "ansible.md": ["Child pages", "Repo structure", "Naming conventions", "Linting"],
    STYLE_DIR / "infra" / "terraform.md": ["Child pages", "Core principles"],
    STYLE_DIR / "python.md": ["Naming conventions", "Error handling", "Docstrings", "Child files"],
    Path("mcp_trust_model.md"): ["Core principle", "Injection attack patterns", "Secure MCP practices"],
    STYLE_DIR / "dbt.md": ["Child pages", "Core Principles", "Model Acceptance Checklist"],
    STYLE_DIR / "utilities" / "mermaid.md": ["Structure"],
    STYLE_DIR / "infra" / "docker.md": ["Structure"],
    STYLE_DIR / "bash.md": ["Safety flags", "Naming conventions"],
    STYLE_DIR / "sql.md": ["Child pages", "Core Principles", "Cost guardrails", "Pre-commit Validation"],
    STYLE_DIR / "jira.md": ["Child pages", "Core principles"],
    STYLE_DIR / "utilities" / "makefile.md": ["Structure"],
}

FENCE_PATTERN = re.compile(r"^\s*(```|~~~)")
HEADER_PATTERNS = (
    re.compile(r"^<!-- version: \d+\.\d+\.\d+ -->$"),
    re.compile(r"^<!-- created: (\d{4}-\d{2}-\d{2}) -->$"),
    re.compile(r"^<!-- updated: (\d{4}-\d{2}-\d{2}) -->$"),
)
LINK_PATTERN = re.compile(r"\]\(([^)\s]+)\)")
CONTENTS_ENTRY_PATTERN = re.compile(r"^\s*-\s*\[([^\]]+)\]\(#[^)]*\)")


def _strip_emoji(text: str) -> str:
    """Drop any leading emoji, variation selectors and spaces from a heading.

    :param text: Heading or link text.
    :type text: str
    :return: The text from its first letter, digit or bracket onwards.
    :rtype: str
    """
    return re.sub(r"^[^\w(]+", "", text).strip()


def _unfenced_lines(text: str) -> list[str]:
    """Return the lines of a markdown file that sit outside code fences.

    :param text: Full file content.
    :type text: str
    :return: Lines outside ``` or ~~~ blocks.
    :rtype: list[str]
    """
    lines, in_fence = [], False
    for line in text.splitlines():
        if FENCE_PATTERN.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return lines


def read_header(text: str) -> tuple[str, str] | None:
    """Return the (created, updated) dates from a rule's three-line metadata header.

    The header sits on lines 1–3, or straight after ``paths:`` frontmatter.

    :param text: Full file content.
    :type text: str
    :return: The two dates, or ``None`` if the header is missing or malformed.
    :rtype: tuple[str, str] | None
    """
    lines = text.splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        closing = [i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---"]
        if not closing:
            return None
        start = closing[0] + 1
    block = lines[start:start + 3]
    if len(block) < 3:
        return None
    matches = [pattern.match(line) for pattern, line in zip(HEADER_PATTERNS, block)]
    if not all(matches):
        return None
    return matches[1].group(1), matches[2].group(1)


def has_purpose_line(text: str) -> bool:
    """Return True if a line outside code fences opens with ``**Purpose:**``.

    :param text: Full file content.
    :type text: str
    :return: Whether the rule states its purpose on a line of its own.
    :rtype: bool
    """
    return any(line.startswith("**Purpose:**") for line in _unfenced_lines(text))


def h2_headings(text: str) -> list[str]:
    """Return every H2 heading outside code fences, emoji stripped.

    :param text: Full file content.
    :type text: str
    :return: Heading texts in file order.
    :rtype: list[str]
    """
    return [_strip_emoji(line[3:]) for line in _unfenced_lines(text) if line.startswith("## ")]


def relative_links(text: str) -> list[str]:
    """Return every markdown link target that points at a local file.

    URLs, mailto links and in-page anchors are skipped, and any ``#anchor``
    suffix is dropped from a file link.

    :param text: Full file content.
    :type text: str
    :return: Link targets relative to the file's own folder.
    :rtype: list[str]
    """
    targets = []
    for line in _unfenced_lines(text):
        for target in LINK_PATTERN.findall(line):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            targets.append(target.split("#", 1)[0])
    return targets


def unlinked_children(text: str, stem: str, child_names: list[str]) -> list[str]:
    """Return child pages that the parent rule never links to.

    :param text: The parent rule's content.
    :type text: str
    :param stem: The parent's filename stem, which names its child folder.
    :type stem: str
    :param child_names: Filenames of the ``.md`` files in the child folder.
    :type child_names: list[str]
    :return: Child filenames with no link ending in ``<stem>/<child>``.
    :rtype: list[str]
    """
    # A path-scoped parent links across to _rules_lazy_load/, so match the link's tail
    linked = set(relative_links(text))
    return [
        name for name in child_names
        if not any(link == f"{stem}/{name}" or link.endswith(f"/{stem}/{name}") for link in linked)
    ]


def contents_mismatches(text: str) -> list[str]:
    """Return Contents entries whose text matches no H2 heading.

    :param text: Full file content.
    :type text: str
    :return: Entry texts, emoji stripped, that have no matching heading.
    :rtype: list[str]
    """
    headings = {heading.lower() for heading in h2_headings(text)}
    entries = [_strip_emoji(m.group(1)) for m in map(CONTENTS_ENTRY_PATTERN.match, _unfenced_lines(text)) if m]
    return [entry for entry in entries if entry.lower() not in headings]


def _child_names(rule: Path) -> list[str]:
    """Return the ``.md`` child pages sitting directly in a rule's child folder.

    :param rule: Absolute path to the parent rule.
    :type rule: Path
    :return: Sorted child filenames, excluding README.md and nested folders.
    :rtype: list[str]
    """
    folder = rule.parent / rule.stem
    if not folder.is_dir() and PATH_SCOPED_DIR in rule.parents:
        # A path-scoped parent's children live in _rules_lazy_load/ so they don't auto-load
        folder = LAZY_RULES_DIR / rule.relative_to(PATH_SCOPED_DIR).with_suffix("")
    if not folder.is_dir():
        return []
    return sorted(p.name for p in folder.glob("*.md") if p.name != "README.md")


def _rule_texts() -> dict[Path, str]:
    """Return each tracked rule's absolute path mapped to its content."""
    return {rule_path(rel): rule_path(rel).read_text(encoding="utf-8") for rel in RULES}


def rule_path(rel: Path) -> Path:
    """Return a tracked rule's absolute path, in rules/05_path_scoped/ or else _rules_lazy_load/."""
    scoped = PATH_SCOPED_DIR / rel
    return scoped if scoped.is_file() else LAZY_RULES_DIR / rel


# ── Real config ─────────────────────────────────────────────────────────


def test_rule_table_tracks_fourteen_distinct_rules():
    """The table covers the 14 rules whose scorecards asked for a dedicated test (ohmyzsh_setup.md is archived)."""
    assert len(RULES) == 14, f"Expected 14 tracked rules, found {len(RULES)} — update RULES"
    stems = [rel.stem for rel in RULES]
    assert len(set(stems)) == len(stems), f"Duplicate rule stems in RULES: {stems}"


def test_every_tracked_rule_exists():
    """Every rule in the table is still on disk under rules/05_path_scoped/ or _rules_lazy_load/."""
    missing = [str(rel) for rel in RULES if not rule_path(rel).is_file()]
    assert not missing, f"Tracked rules missing from both rule folders — fix the path in RULES or restore: {missing}"


def test_every_rule_has_metadata_header():
    """Each rule opens with the version, created and updated comment lines."""
    bad = [rule.name for rule, text in _rule_texts().items() if read_header(text) is None]
    assert not bad, f"Missing or malformed metadata header (see _claude_config_metadata.md): {bad}"


def test_header_updated_is_not_before_created():
    """Each rule's updated date is on or after its created date."""
    bad = []
    for rule, text in _rule_texts().items():
        header = read_header(text)
        if header and header[1] < header[0]:
            bad.append(f"{rule.name}: created {header[0]}, updated {header[1]}")
    assert not bad, f"updated date is earlier than created — fix the header: {bad}"


def test_key_sections_survive():
    """Each rule keeps the H2 headings that carry its core guidance."""
    missing = []
    for rel, sections in RULES.items():
        headings = h2_headings(rule_path(rel).read_text(encoding="utf-8"))
        missing += [f"{rel.name}: '{section}'" for section in sections if section not in headings]
    assert not missing, f"Key sections missing — restore them or update RULES if renamed on purpose: {missing}"


def test_every_child_page_is_linked():
    """Every .md file in a rule's child folder is linked from the parent."""
    bad = []
    for rule, text in _rule_texts().items():
        bad += [f"{rule.name} -> {child}" for child in unlinked_children(text, rule.stem, _child_names(rule))]
    assert not bad, f"Child pages not linked from their parent — add a link so they can be found: {bad}"


def test_rules_with_child_folders_have_children():
    """The rules split into parent and children still have at least two children."""
    split = [rule for rule in _rule_texts() if _child_names(rule)]
    assert len(split) >= 10, f"Expected 10+ split rules, found {len(split)} — was a child folder removed?"
    thin = [rule.name for rule in split if len(_child_names(rule)) < 2]
    assert not thin, (
        f"Child folders with fewer than 2 pages — flatten them per multifile_document_organisation.md: {thin}"
    )


def test_every_relative_link_resolves():
    """Every link to a local file points at a file that exists."""
    broken = []
    for rule, text in _rule_texts().items():
        broken += [f"{rule.name} -> {target}" for target in relative_links(text) if not (rule.parent / target).exists()]
    assert not broken, f"Broken relative links — fix the path or restore the file: {broken}"


def test_contents_entries_match_headings():
    """Every Contents entry names a real H2 heading in the same file."""
    bad = []
    for rule, text in _rule_texts().items():
        bad += [f"{rule.name}: '{entry}'" for entry in contents_mismatches(text)]
    assert not bad, f"Contents entries with no matching heading — rename the entry or the heading: {bad}"


def test_every_rule_has_purpose_line():
    """Every tracked rule states its purpose on a **Purpose:** line."""
    missing = sorted(rule.name for rule, text in _rule_texts().items() if not has_purpose_line(text))
    assert not missing, f"Rules with no **Purpose:** line — add one under the H1: {missing}"


# ── Synthetic cases: prove each detector fails when it should ────────────


def test_read_header_rejects_missing_or_malformed_header():
    """A file with no header, or a non-semver version, has no valid header."""
    assert read_header("# 🧪 Title\n") is None, "A file with no header should be rejected"
    bad_version = "<!-- version: 1.0 -->\n<!-- created: 2026-01-01 -->\n<!-- updated: 2026-01-02 -->\n"
    assert read_header(bad_version) is None, "A two-part version should be rejected as non-semver"


def test_read_header_finds_header_after_frontmatter():
    """A path-scoped rule's header is read from just below its frontmatter."""
    text = (
        '---\npaths:\n  - "**/*.sql"\n---\n'
        "<!-- version: 1.0.0 -->\n<!-- created: 2026-01-01 -->\n<!-- updated: 2026-02-01 -->\n"
    )
    assert read_header(text) == ("2026-01-01", "2026-02-01"), "Header after frontmatter should be parsed"
    assert read_header("---\npaths: []\n") is None, "Unclosed frontmatter should be rejected"


def test_has_purpose_line_needs_its_own_unfenced_line():
    """A Purpose mid-sentence or inside a code fence doesn't count."""
    assert has_purpose_line("# 🧪 Title\n\n**Purpose:** Explain things.\n"), "A real Purpose line was missed"
    assert not has_purpose_line("See the **Purpose:** line below.\n"), "A mid-sentence Purpose was counted"
    assert not has_purpose_line("```\n**Purpose:** example\n```\n"), "A fenced Purpose was counted"


def test_h2_headings_strip_emoji_and_skip_fences():
    """Headings lose their emoji, and ## lines inside code fences are ignored."""
    text = "## ⚠️ Known exceptions\n```\n## not a heading\n```\n## 📂 Model Layers (Architecture)\n"
    assert h2_headings(text) == ["Known exceptions", "Model Layers (Architecture)"], "Emoji or fenced lines leaked"


def test_relative_links_skip_urls_and_anchors():
    """URLs, mailto and in-page anchors are skipped, and file anchors are dropped."""
    text = "[a](https://x.io) [b](#top) [c](mailto:a@b.c) [d](dbt/macros.md#usage)"
    assert relative_links(text) == ["dbt/macros.md"], "Only the local file link should remain"


def test_unlinked_children_detects_missing_link():
    """A child page with no link from its parent is reported."""
    text = "| [`dbt/macros.md`](dbt/macros.md) | Macros |"
    assert unlinked_children(text, "dbt", ["macros.md", "snapshots.md"]) == ["snapshots.md"], "Unlinked child missed"
    assert unlinked_children(text, "dbt", ["macros.md"]) == [], "A linked child was wrongly reported"


def test_contents_mismatches_detects_stale_entry():
    """A Contents entry with no matching heading is reported, and a matching one is not."""
    text = "## 📋 Contents\n- [🎨 Theme](#-theme)\n- [🔌 Plugins](#-plugins)\n## 🎨 Theme\n"
    assert contents_mismatches(text) == ["Plugins"], "Stale Contents entry missed"
    assert contents_mismatches("## 🎨 Theme\n") == [], "A file without Contents should report nothing"
