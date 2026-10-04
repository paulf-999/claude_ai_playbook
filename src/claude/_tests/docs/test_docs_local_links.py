# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-04
# Date updated:      2026-10-04
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Checks every local link in README.md and docs/ points at a file that exists.

Web links, mailto links and same-page anchors are skipped, and any #fragment is
dropped before the path is resolved relative to the linking file. Issue #292
found 52 links left broken by folder moves, because nothing checked them.
"""

import re
from pathlib import Path

import pytest

# repo/src/claude/_tests/docs/<this file> → parents[4] is the repo root
REPO_ROOT = Path(__file__).resolve().parents[4]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")


def broken_local_links(root: Path) -> list[str]:
    """Return 'file:line: target' for each local link under root whose target is missing."""
    files = [root / "README.md", *sorted((root / "docs").rglob("*.md"))]
    broken = []
    for md_file in files:
        if not md_file.is_file():
            continue
        for line_no, line in enumerate(md_file.read_text(encoding="utf-8").splitlines(), 1):
            for target in LINK.findall(line):
                if target.startswith(SKIP_PREFIXES):
                    continue
                path = target.split("#", 1)[0]
                if not (md_file.parent / path).exists():
                    broken.append(f"{md_file.relative_to(root)}:{line_no}: {target}")
    return broken


def make_repo(tmp_path: Path, readme: str) -> Path:
    """Build a tiny repo with docs/real.md, docs/guides/ and the given README text."""
    (tmp_path / "docs" / "guides").mkdir(parents=True)
    (tmp_path / "docs" / "real.md").write_text("# Real\n", encoding="utf-8")
    (tmp_path / "README.md").write_text(readme, encoding="utf-8")
    return tmp_path


def test_existing_file_passes(tmp_path):
    """A link to a file that exists is not reported."""
    assert broken_local_links(make_repo(tmp_path, "[ok](docs/real.md)\n")) == []


def test_missing_file_reported_with_line(tmp_path):
    """A missing target is reported as file:line: target."""
    root = make_repo(tmp_path, "intro\n[gone](docs/missing.md)\n")
    assert broken_local_links(root) == ["README.md:2: docs/missing.md"]


def test_web_and_mailto_links_skipped(tmp_path):
    """http, https and mailto links are never checked on disk."""
    root = make_repo(tmp_path, "[a](http://x.io) [b](https://x.io/y.md) [c](mailto:a@b.c)\n")
    assert broken_local_links(root) == []


def test_same_page_anchor_skipped(tmp_path):
    """A pure #anchor link points within the page, so it is skipped."""
    assert broken_local_links(make_repo(tmp_path, "[top](#intro)\n")) == []


def test_fragment_stripped_before_resolving(tmp_path):
    """file.md#section resolves to file.md, and the fragment does not matter."""
    root = make_repo(tmp_path, "[ok](docs/real.md#section) [bad](docs/nope.md#section)\n")
    assert broken_local_links(root) == ["README.md:1: docs/nope.md#section"]


def test_directory_target_passes(tmp_path):
    """A link to an existing folder counts as valid."""
    assert broken_local_links(make_repo(tmp_path, "[dir](docs/guides/)\n")) == []


def test_link_resolved_relative_to_linking_file(tmp_path):
    """A docs page's ../ link resolves from that page's folder, not the repo root."""
    root = make_repo(tmp_path, "")
    (root / "docs" / "guides" / "page.md").write_text("[up](../real.md)\n[root](../../README.md)\n", encoding="utf-8")
    assert broken_local_links(root) == []
    (root / "docs" / "guides" / "page.md").write_text("[wrong depth](../README.md)\n", encoding="utf-8")
    assert broken_local_links(root) == ["docs/guides/page.md:1: ../README.md"]


def test_link_title_ignored(tmp_path):
    """A link title after the path is not treated as part of the target."""
    root = make_repo(tmp_path, '[ok](docs/real.md "Real page") [bad](docs/x.md "X")\n')
    assert broken_local_links(root) == ["README.md:1: docs/x.md"]


def test_every_broken_link_on_a_line_reported(tmp_path):
    """Two broken links on one line are both reported, in order."""
    broken = broken_local_links(make_repo(tmp_path, "[a](a.md) and [b](b.md)\n"))
    assert broken == ["README.md:1: a.md", "README.md:1: b.md"]


def test_missing_readme_tolerated(tmp_path):
    """A tree without README.md still scans docs/ instead of crashing."""
    root = make_repo(tmp_path, "")
    (root / "README.md").unlink()
    (root / "docs" / "real.md").write_text("[gone](missing.md)\n", encoding="utf-8")
    assert broken_local_links(root) == ["docs/real.md:1: missing.md"]


def test_link_text_with_brackets_and_images(tmp_path):
    """Image links and link text holding code are checked like any other link."""
    root = make_repo(tmp_path, "![logo](img/logo.png) [`code`](docs/real.md)\n")
    assert broken_local_links(root) == ["README.md:1: img/logo.png"]
    assert len(LINK.findall("[`code`](docs/real.md)")) == 1, "code-styled link text not matched"


def test_docs_have_no_broken_local_links():
    """Every local link in the repo's README.md and docs/ resolves to a real file."""
    if not (REPO_ROOT / "docs").is_dir() or not (REPO_ROOT / "src" / "claude").is_dir():
        pytest.skip("no docs/ here — running against a live install, not the repo")
    broken = broken_local_links(REPO_ROOT)
    assert not broken, "broken local links:\n" + "\n".join(broken)
