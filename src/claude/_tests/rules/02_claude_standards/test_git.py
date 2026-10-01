# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-01
# Version:           2.0.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Content tests for _rules/02_claude_standards/git.md.

Each test guards one rule the file sets — protected main, branch naming, PR
standards, complex-operation care and its three imported children — so a
lost clause fails by name. The branch-name pattern is also run against the
file's own examples, so the regex and its examples can't drift apart.
"""
from __future__ import annotations

import re

from _shared_paths import RULES_DIR

GIT_RULES = RULES_DIR / "02_claude_standards" / "git.md"
CHILDREN = ("_safe_patterns.md", "_commits.md", "_concurrent_sessions.md")


def content() -> str:
    """Read git.md.

    :return: The rule's text.
    :rtype: str
    """
    return GIT_RULES.read_text()


def branch_pattern() -> re.Pattern[str]:
    """Compile the branch-name pattern git.md documents.

    :return: The compiled ``**Pattern:**`` regex.
    :rtype: re.Pattern[str]
    """
    match = re.search(r"\*\*Pattern:\*\* `([^`]+)`", content())
    assert match, "git.md must document its branch-name regex as **Pattern:** `...`"
    return re.compile(match.group(1))


def test_imports_every_child():
    """git.md imports each child file, so none is silently unloaded."""
    for child in CHILDREN:
        assert re.search(rf"^@~/[^/]+/_rules/02_claude_standards/git/{child}$", content(), re.M), (
            f"git.md must @import git/{child}"
        )


def test_children_exist():
    """Each imported child is on disk."""
    missing = [c for c in CHILDREN if not (GIT_RULES.parent / "git" / c).is_file()]
    assert not missing, f"git.md imports children that don't exist: {missing}"


def test_main_is_protected():
    """git.md forbids committing straight to main."""
    assert "Never commit to main" in content(), "git.md must keep the 'Never commit to main' rule"


def test_branch_pattern_accepts_its_examples():
    """Every example branch git.md gives matches its own pattern."""
    examples_line = content().split("**Examples:**", 1)[1].split("\n")[0]
    examples = re.findall(r"`((?:feature|hotfix|release)/[^`]+)`", examples_line)
    assert len(examples) >= 3, f"expected an example for each prefix, found {examples}"
    bad = [e for e in examples if not branch_pattern().fullmatch(e)]
    assert not bad, f"git.md's own examples break its pattern: {bad}"


def test_branch_pattern_rejects_bad_names():
    """Hyphens, capitals, a missing prefix or an unknown prefix all fail the pattern."""
    for name in ("feature/add-pr-template", "feature/AddTemplate", "add_pr_template", "bugfix/x"):
        assert not branch_pattern().fullmatch(name), f"'{name}' should not match the branch pattern"


def test_pr_size_limit():
    """PRs stay under 20 files."""
    assert "fewer than 20 files" in content(), "git.md must keep the under-20-files PR limit"


def test_pr_template_required():
    """PRs use the repo's PR template."""
    assert ".github/pull_request_template.md" in content(), "git.md must require the PR template"


def test_pr_titles_use_conventional_commits():
    """PR titles follow Conventional Commits."""
    assert "Conventional Commits — `type(scope): description`" in content(), (
        "git.md must keep the Conventional Commits title format"
    )


def test_prs_use_gh_cli():
    """PR operations go through the gh CLI."""
    assert "use the `gh` CLI for all GitHub PR operations" in content(), "git.md must keep the gh CLI rule"


def test_stash_is_never_resolved_silently():
    """A stash made mid-task is surfaced, never dropped or popped unilaterally."""
    assert "Never silently resolve a stash" in content(), "git.md must keep the stash rule"


def test_complex_operations_are_flagged_first():
    """Complex git operations are flagged before acting, preferring the simplest option."""
    assert "Flag before acting" in content(), "git.md must keep 'Flag before acting'"
    assert "Simplest over proper" in content(), "git.md must keep 'Simplest over proper'"


def test_line_limit():
    """git.md stays within the 110-line rule limit."""
    lines = len(content().splitlines())
    assert lines <= 110, f"git.md has {lines} lines — split it into a parent and children"
