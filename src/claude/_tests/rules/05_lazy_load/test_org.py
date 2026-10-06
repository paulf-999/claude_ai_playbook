# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-01
# Version:           1.1.2
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Organisation-specific terms stay inside 05_lazy_load/org/ and never leak into shared files.

``org.md`` and ``org/`` hold one organisation's names, links and IDs. Every other config
file is shared, so a term from ``org/_shared_file_terms.txt`` appearing there is a leak.
The term list lives inside ``org/`` itself, so this test never names a term. Where the
list is absent, as in a config with no organisation content, the real-file check skips.
"""
from pathlib import Path

import pytest

from _shared_paths import CLAUDE_DIR

TERMS_FILE = CLAUDE_DIR / "_rules" / "05_lazy_load" / "org" / "_shared_file_terms.txt"
SHARED_DIRS = (
    "_rules", "_templates", "_reference", "_tests", "_scripts", "_admin", "agents", "hooks", "skills", "rules",
)
SHARED_TOP_FILES = ("CLAUDE.md", "aliases.md", "README.md", "settings.json", "settings_json_readme.md", "TODO.md")
EXCLUDED_PREFIXES = ("_rules/05_lazy_load/org/", "_admin/_audits/")
EXCLUDED_FILES = {"_rules/05_lazy_load/org.md"}
ORG_PATH_MARKER = "05_lazy_load/org/"
# Shared files known to hold organisation terms, awaiting a decision. Shrink-only.
KNOWN_EXCEPTIONS = {"TODO.md"}


def load_terms(path: Path) -> list[str]:
    """Read lower-cased terms from a list file, skipping comments and blank lines.

    :param path: The term list.
    :type path: Path
    :return: The terms, or an empty list when the file is missing.
    :rtype: list[str]
    """
    if not path.is_file():
        return []
    lines = (line.strip() for line in path.read_text(encoding="utf-8").splitlines())
    return [line.lower() for line in lines if line and not line.startswith("#")]


def is_excluded(rel: str) -> bool:
    """Tell whether a config-relative path is organisation content or generated data.

    :param rel: Path relative to the config directory.
    :type rel: str
    :return: True for org files, their scorecards and audit output.
    :rtype: bool
    """
    if rel in EXCLUDED_FILES or rel.startswith(EXCLUDED_PREFIXES):
        return True
    return rel.startswith("_admin/_quality_scorecards/") and "/org/" in rel


def shared_files(root: Path) -> list[str]:
    """List the shared config files to scan, relative to ``root``.

    :param root: The config directory.
    :type root: Path
    :return: Sorted relative paths of real files, symlinks and caches excluded.
    :rtype: list[str]
    """
    found = [name for name in SHARED_TOP_FILES if (root / name).is_file()]
    for folder in SHARED_DIRS:
        for path in (root / folder).rglob("*"):
            if path.is_file() and not path.is_symlink() and "__pycache__" not in path.parts:
                found.append(path.relative_to(root).as_posix())
    return sorted(rel for rel in found if not is_excluded(rel))


def leaked_terms(text: str, terms: list[str]) -> list[str]:
    """Return the terms found in a file, ignoring lines that only reference org/ paths.

    :param text: File content.
    :type text: str
    :param terms: Lower-cased terms.
    :type terms: list[str]
    :return: Sorted terms present outside org/ path references.
    :rtype: list[str]
    """
    lines = [line.lower() for line in text.splitlines() if ORG_PATH_MARKER not in line]
    body = "\n".join(lines)
    return sorted({term for term in terms if term in body})


# ── helpers ──────────────────────────────────────────────────────────────────


def test_terms_skip_comments_and_blanks(tmp_path):
    """Comment and blank lines aren't terms, and terms are lower-cased."""
    terms_file = tmp_path / "terms.txt"
    terms_file.write_text("# a comment\n\nAcme\n  widgets  \n")
    assert load_terms(terms_file) == ["acme", "widgets"]


def test_missing_terms_file_gives_no_terms(tmp_path):
    """A config with no organisation content has no term list, and that's fine."""
    assert load_terms(tmp_path / "absent.txt") == []


def test_org_content_and_audits_are_excluded():
    """org.md, org/, org scorecards and generated audits are never scanned."""
    assert is_excluded("_rules/05_lazy_load/org.md")
    assert is_excluded("_rules/05_lazy_load/org/jira.md")
    assert is_excluded("_admin/_quality_scorecards/rules/05_lazy_load/org/scorecard_jira.md")
    assert is_excluded("_admin/_audits/rule_usage_history.csv")
    assert not is_excluded("_rules/05_lazy_load/style_guide_standards/sql.md"), "a shared rule must be scanned"


def test_leak_found_case_insensitively():
    """A term is found whatever its case."""
    assert leaked_terms("Built for ACME engineers", ["acme"]) == ["acme"]


def test_line_referencing_org_path_is_allowed():
    """A line that only points at an org/ file may name it, for example a scorecard summary row."""
    text = "| `05_lazy_load/org/scorecard_acme_naming.md` | 9/10 |\nother text\n"
    assert leaked_terms(text, ["acme"]) == []


def test_clean_text_has_no_leaks():
    """Text without any term reports nothing."""
    assert leaked_terms("neutral placeholder <your-org>", ["acme", "widgets"]) == []


def test_scan_skips_symlinks_caches_and_runtime_folders(tmp_path):
    """Only real files in shared config folders are scanned, never runtime data like projects/."""
    (tmp_path / "_rules" / "05_lazy_load" / "org").mkdir(parents=True)
    (tmp_path / "_rules" / "shared.md").write_text("x")
    (tmp_path / "_rules" / "05_lazy_load" / "org" / "secret.md").write_text("x")
    (tmp_path / "_tests" / "__pycache__").mkdir(parents=True)
    (tmp_path / "_tests" / "__pycache__" / "x.pyc").write_text("x")
    (tmp_path / "projects").mkdir()
    (tmp_path / "projects" / "log.json").write_text("x")
    (tmp_path / "rules").mkdir()
    (tmp_path / "rules" / "link.md").symlink_to(tmp_path / "_rules" / "shared.md")
    (tmp_path / "CLAUDE.md").write_text("x")
    assert shared_files(tmp_path) == ["CLAUDE.md", "_rules/shared.md"]


# ── the real config ──────────────────────────────────────────────────────────


def test_shared_files_are_found():
    """The scan finds the shared config, or every leak check would pass vacuously."""
    files = shared_files(CLAUDE_DIR)
    assert "CLAUDE.md" in files, "CLAUDE.md is missing from the scan"
    assert len(files) > 100, f"expected over 100 shared files, found {len(files)}"


def test_no_organisation_terms_in_shared_files():
    """No shared config file names a term from org/_shared_file_terms.txt."""
    terms = load_terms(TERMS_FILE)
    if not terms:
        pytest.skip("no organisation term list, so there is nothing to leak")
    leaks = {}
    for rel in shared_files(CLAUDE_DIR):
        if rel in KNOWN_EXCEPTIONS:
            continue
        found = leaked_terms((CLAUDE_DIR / rel).read_text(encoding="utf-8", errors="ignore"), terms)
        if found:
            leaks[rel] = found
    assert not leaks, (
        "organisation terms in shared files — move the content into 05_lazy_load/org/ or use a placeholder:\n  "
        + "\n  ".join(f"{rel}: {found}" for rel, found in sorted(leaks.items()))
    )


def test_known_exceptions_still_need_their_place():
    """A known exception that no longer holds any term must leave KNOWN_EXCEPTIONS, so the list only shrinks."""
    terms = load_terms(TERMS_FILE)
    if not terms:
        pytest.skip("no organisation term list")
    for rel in KNOWN_EXCEPTIONS:
        path = CLAUDE_DIR / rel
        if path.is_file():
            assert leaked_terms(path.read_text(encoding="utf-8", errors="ignore"), terms), (
                f"{rel} is clean now — remove it from KNOWN_EXCEPTIONS"
            )


# ── org.md stays a complete index ────────────────────────────────────────────

ORG_INDEX = CLAUDE_DIR / "_rules" / "05_lazy_load" / "org.md"
ORG_DIR = ORG_INDEX.with_suffix("")
ORG_POINTER = "05_lazy_load/org.md"
POINTING_FILES = (
    ("_rules", "01_essentials/claude_usage_standards/naming_standards.md"),
    ("skills", "jira_create/SKILL.md"),
    ("skills", "git_create_pr/reference/_phase1_gather.md"),
)


def find_config_file(folder, tail):
    """Find a config file by its path tail, so repo and installed layouts both resolve."""
    matches = [p for p in (CLAUDE_DIR / folder).rglob(Path(tail).name) if p.as_posix().endswith(tail)]
    assert matches, f"{folder}/**/{tail} not found"
    return matches[0]


def unlisted_org_rules(index_text: str, org_dir: Path) -> list[str]:
    """Return top-level org/ rules that the index's child table doesn't link to.

    :param index_text: org.md content.
    :type index_text: str
    :param org_dir: The org/ folder.
    :type org_dir: Path
    :return: Sorted file names missing from the index.
    :rtype: list[str]
    """
    if not org_dir.is_dir():
        return []
    rules = [p.name for p in org_dir.glob("*.md") if not p.name.startswith("_")]
    return sorted(name for name in rules if f"(org/{name})" not in index_text)


def test_unlisted_org_rule_is_caught(tmp_path):
    """An org/ rule with no row in the index is reported, and a linked one isn't."""
    (tmp_path / "org").mkdir()
    (tmp_path / "org" / "listed.md").write_text("# L\n")
    (tmp_path / "org" / "missing.md").write_text("# M\n")
    (tmp_path / "org" / "_terms.txt").write_text("x\n")
    assert unlisted_org_rules("| [`org/listed.md`](org/listed.md) |", tmp_path / "org") == ["missing.md"]


def test_no_org_folder_means_nothing_unlisted(tmp_path):
    """A config with no org/ folder, such as a fresh install, has nothing to index."""
    assert unlisted_org_rules("", tmp_path / "org") == []


def test_org_index_lists_every_org_rule():
    """Every rule moved into org/ has a row in org.md, so the index never hides one."""
    assert ORG_INDEX.is_file(), "org.md is missing"
    missing = unlisted_org_rules(ORG_INDEX.read_text(), ORG_DIR)
    assert not missing, f"org/ rules with no row in org.md: {missing}"


def test_shared_files_point_at_the_org_index():
    """naming_standards.md and the Jira and PR skills keep their pointer to org.md."""
    for folder, tail in POINTING_FILES:
        text = find_config_file(folder, tail).read_text()
        assert ORG_POINTER in text, f"{tail} lost its pointer to {ORG_POINTER}"
