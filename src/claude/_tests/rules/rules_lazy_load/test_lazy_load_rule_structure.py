# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-28
# Version:           2.1.1
# Test quality score: 10/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Structural tests for the lazy-load rules that had no dedicated test.

Their scorecards average 4.9/10 for Test Coverage, the lowest dimension
anywhere (see ``quality_scorecards_summary.md``). This file guards five
things for each rule: its metadata header, its ``**Purpose:**`` line, that
every child page is linked, that every relative link resolves, and that each
Contents entry matches a real heading. It also checks every style-guide
child page, not just the parents, for a ``_`` prefix and a Purpose line.

One of them (MCP trust model) moved to rules/02_claude_standards/ on
2026-10-11 to load every session, and stays tracked here so its guard isn't lost.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from _shared_paths import (
    CLAUDE_DIR,
    LAZY_RULES_NAME,
    RULES_DIR,
    STYLE_GUIDES_NAME,
    installed_rule_files,
    resolve_config_path,
    resolve_link,
)

PATH_SCOPED_DIR = RULES_DIR / "02_claude_standards" / "path_scoped_rules"
STYLE_DIR = Path("style_guide_standards")

# Rule path (relative to rules/02_claude_standards/path_scoped_rules/, rules/02_claude_standards/ or _rules_lazy_load/,
# or style_guide_standards/ for any style guide)
# -> H2 headings it must keep, emoji stripped.
RULES: dict[Path, list[str]] = {
    Path("org.md"): ["Child pages", "Organisation facts", "Internal references"],
    STYLE_DIR / "airflow.md": ["Child pages", "Core Principles", "DAG Acceptance Checklist"],
    STYLE_DIR / "utilities" / "datetime.md": ["Standard formats", "Timezone", "Known exceptions"],
    STYLE_DIR / "infra" / "ansible.md": ["Child pages", "Repo structure", "Naming conventions", "Linting"],
    STYLE_DIR / "infra" / "terraform.md": ["Child pages", "Core principles"],
    STYLE_DIR / "python.md": ["Naming conventions", "Error handling", "Docstrings", "Child files"],
    Path("security/_mcp_trust_model.md"): ["Core principle", "Injection attack patterns", "Secure MCP practices"],
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
    :return: The text from its first letter, digit or bracket onwards.
    """
    return re.sub(r"^[^\w(]+", "", text).strip()


def _unfenced_lines(text: str) -> list[str]:
    """Return the lines of a markdown file that sit outside code fences.

    :param text: Full file content.
    :return: Lines outside ``` or ~~~ blocks.
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
    :return: The two dates, or ``None`` if the header is missing or malformed.
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
    :return: Whether the rule states its purpose on a line of its own.
    """
    return any(line.startswith("**Purpose:**") for line in _unfenced_lines(text))


def h2_headings(text: str) -> list[str]:
    """Return every H2 heading outside code fences, emoji stripped.

    :param text: Full file content.
    :return: Heading texts in file order.
    """
    return [_strip_emoji(line[3:]) for line in _unfenced_lines(text) if line.startswith("## ")]


def relative_links(text: str) -> list[str]:
    """Return every markdown link target that points at a local file.

    URLs, mailto links and in-page anchors are skipped, and any ``#anchor``
    suffix is dropped from a file link.

    :param text: Full file content.
    :return: Link targets relative to the file's own folder.
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
    :param stem: The parent's filename stem, which names its child folder.
    :param child_names: Filenames of the ``.md`` files in the child folder.
    :return: Child filenames with no link ending in ``<stem>/<child>``.
    """
    # A parent may link across folders, so match the link's tail
    linked = set(relative_links(text))
    return [
        name for name in child_names
        if not any(link == f"{stem}/{name}" or link.endswith(f"/{stem}/{name}") for link in linked)
    ]


def contents_mismatches(text: str) -> list[str]:
    """Return Contents entries whose text matches no H2 heading.

    :param text: Full file content.
    :return: Entry texts, emoji stripped, that have no matching heading.
    """
    headings = {heading.lower() for heading in h2_headings(text)}
    entries = [_strip_emoji(m.group(1)) for m in map(CONTENTS_ENTRY_PATTERN.match, _unfenced_lines(text)) if m]
    return [entry for entry in entries if entry.lower() not in headings]


def _child_names(rule: Path) -> list[str]:
    """Return the ``.md`` child pages sitting directly in a rule's child folder.

    :param rule: Absolute path to the parent rule.
    :return: Sorted child filenames, excluding README.md and nested folders.
    """
    folder = rule.parent / rule.stem
    if not folder.is_dir() and PATH_SCOPED_DIR / STYLE_DIR in rule.parents:
        # Installed, an entry file's children stay in _reference/_style_guide_standards/ so they don't auto-load
        folder = CLAUDE_DIR / STYLE_GUIDES_NAME / rule.relative_to(PATH_SCOPED_DIR / STYLE_DIR).with_suffix("")
    if not folder.is_dir():
        return []
    return sorted(p.name for p in folder.glob("*.md") if p.name != "README.md")


def _rule_texts() -> dict[Path, str]:
    """Return each tracked rule's absolute path mapped to its content."""
    return {rule_path(rel): rule_path(rel).read_text(encoding="utf-8") for rel in RULES}


@lru_cache(maxsize=1)
def _installed_files() -> dict[str, Path]:
    """Return every rule file keyed by installed path, read once per run."""
    return installed_rule_files(CLAUDE_DIR)


def rule_path(rel: Path) -> Path:
    """Return a tracked rule's absolute path wherever it installs, in either layout."""
    key = rel.as_posix()
    candidates = [f"rules/02_claude_standards/path_scoped_rules/{key}", f"rules/02_claude_standards/{key}",
                  f"{LAZY_RULES_NAME}/{key}"]
    if rel.parts[0] == STYLE_DIR.name:
        candidates.append(f"{STYLE_GUIDES_NAME}/{rel.relative_to(STYLE_DIR).as_posix()}")
    files = _installed_files()
    return next((files[c] for c in candidates if c in files), resolve_config_path(CLAUDE_DIR, candidates[-1]))


# ── Real config ─────────────────────────────────────────────────────────


def test_every_tracked_rule_exists():
    """Every tracked rule is still on disk under rules/02_claude_standards/path_scoped_rules/,
    rules/02_claude_standards/,
    _rules_lazy_load/ or the style guides."""
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
        missing = [target for target in relative_links(text) if not resolve_link(rule, target).exists()]
        broken += [f"{rule.name} -> {target}" for target in missing]
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


# ── Style-guide children ─────────────────────────────────────────────────

GUIDES_ROOT = CLAUDE_DIR / STYLE_GUIDES_NAME
INSTALLED_GUIDES = PATH_SCOPED_DIR / "style_guide_standards"
NOT_CHILD_FOLDERS = {"templates", "examples"}


def is_style_guide_child(path: Path, root: Path, installed_root: Path) -> bool:
    """Return True if a page sits in a guide's own folder, so it's a child of that guide.

    A folder belongs to a guide when the guide's parent page sits beside it, or at its installed
    path once the install has moved path-scoped parents. READMEs and anything under a
    ``templates/`` or ``examples/`` folder are support files, not children.

    :param path: A markdown file under the style-guides folder.
    :param root: The style-guides folder.
    :param installed_root: Where the install puts path-scoped parent guides.
    :return: Whether the file is a child page of a guide.
    """
    folder = path.parent
    if folder == root or path.name == "README.md" or NOT_CHILD_FOLDERS & set(path.relative_to(root).parts):
        return False
    rel_parent = folder.relative_to(root).with_suffix(".md")
    return (root / rel_parent).is_file() or (installed_root / rel_parent).is_file()


def is_nested_parent(path: Path) -> bool:
    """Return True if a child page is itself a parent, with a folder of its own children beside it."""
    return path.with_suffix("").is_dir()


@lru_cache(maxsize=None)
def style_guide_children() -> tuple[Path, ...]:
    """List every style-guide child page, skipping templates, examples and READMEs."""
    return tuple(p for p in sorted(GUIDES_ROOT.rglob("*.md")) if is_style_guide_child(p, GUIDES_ROOT, INSTALLED_GUIDES))


def test_style_guide_children_exist_to_check():
    """There are child pages to check, so the two checks below can't pass on an empty set."""
    assert style_guide_children(), f"no style-guide children found under {GUIDES_ROOT}"


def test_style_guide_children_start_with_underscore():
    """Every child page starts with ``_``, except a child that is itself a parent and names its folder."""
    bad = [str(p.relative_to(GUIDES_ROOT)) for p in style_guide_children()
           if not p.name.startswith("_") and not is_nested_parent(p)]
    assert not bad, f"Style-guide children without a _ prefix — rename them and their links: {bad}"


def test_style_guide_children_have_purpose_line():
    """Every child page states its purpose on a **Purpose:** line."""
    bad = [str(p.relative_to(GUIDES_ROOT)) for p in style_guide_children() if not has_purpose_line(p.read_text())]
    assert not bad, f"Style-guide children with no **Purpose:** line — add one under the H1: {bad}"


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


def test_is_style_guide_child_tells_children_from_support_files(tmp_path: Path):
    """Pages in a guide's folder are children, while the parent, READMEs, templates and unguided folders are not."""
    root, installed = tmp_path / "guides", tmp_path / "installed"
    for rel in ("sql.md", "sql/_formatting.md", "sql/README.md", "sql/templates/t.md", "loose/page.md",
                "infra/docker/_advanced.md"):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text("x")
    (installed / "infra").mkdir(parents=True)
    (installed / "infra" / "docker.md").write_text("x")
    children = {p.relative_to(root).as_posix() for p in root.rglob("*.md") if is_style_guide_child(p, root, installed)}
    assert children == {"sql/_formatting.md", "infra/docker/_advanced.md"}, f"wrong children found: {children}"


def test_is_nested_parent_needs_its_own_folder(tmp_path: Path):
    """A child with a same-named folder beside it is a nested parent, and one without is not."""
    (tmp_path / "testing").mkdir()
    assert is_nested_parent(tmp_path / "testing.md"), "a child with its own folder should count as a parent"
    assert not is_nested_parent(tmp_path / "comments.md"), "a child with no folder should not count as a parent"
