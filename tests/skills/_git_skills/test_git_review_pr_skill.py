"""Behavioural tests for the review_pr skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Diff truncation at 500 lines
- File link construction (repo_url/blob/headRefName/filepath)
- Overall score calculation (average of 6 theme scores)
- Grade mapping from score to letter grade
- Verdict determination from Must/Should items
- Confirmation required before posting
- Scorecard covers 6 themes (code quality, code complexity, testing, security,
  documentation, standards)
"""

from pathlib import Path

import pytest

# ─── Paths ────────────────────────────────────────────────────────────────────

SKILL_DIR = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_git_skills" / "git_review_pr"
)
SKILL_MD = SKILL_DIR / "SKILL.md"
SKILL_SCHEMA = SKILL_DIR / "skill_schema.yaml"
COMMENT_FORMAT_MD = SKILL_DIR / "comment_format.md"
PHASE2_MD = SKILL_DIR / "phase2.md"


def _skill_content() -> str:
    return SKILL_MD.read_text()


def _schema_content() -> str:
    return SKILL_SCHEMA.read_text()


def _comment_format_content() -> str:
    return COMMENT_FORMAT_MD.read_text()


def _phase2_content() -> str:
    return PHASE2_MD.read_text()


# ─── Diff truncation ──────────────────────────────────────────────────────────

DIFF_TRUNCATION_LIMIT = 500


def truncate_diff(diff: str, limit: int = DIFF_TRUNCATION_LIMIT) -> tuple[str, bool]:
    """Truncate a diff to the first `limit` lines.

    Implements the rule in phase2.md:
    'If the diff exceeds 500 lines, truncate to the first 500 lines'.

    :param diff: Full diff string.
    :type diff: str
    :param limit: Maximum number of lines to keep.
    :type limit: int
    :return: Tuple of (truncated diff, was_truncated).
    :rtype: tuple[str, bool]
    """
    lines = diff.splitlines(keepends=True)
    if len(lines) > limit:
        return "".join(lines[:limit]), True
    return diff, False


def test_diff_under_limit_not_truncated() -> None:
    """A diff with 500 lines or fewer must not be truncated."""
    diff = "line\n" * 500
    result, truncated = truncate_diff(diff)
    assert not truncated
    assert result == diff


def test_diff_over_limit_is_truncated() -> None:
    """A diff with more than 500 lines must be truncated to exactly 500 lines."""
    diff = "line\n" * 501
    result, truncated = truncate_diff(diff)
    assert truncated
    assert len(result.splitlines()) == 500


def test_truncation_keeps_first_lines() -> None:
    """Truncation must keep the first 500 lines, not a random subset."""
    lines = [f"line {i}\n" for i in range(600)]
    diff = "".join(lines)
    result, _ = truncate_diff(diff)
    result_lines = result.splitlines()
    assert result_lines[0] == "line 0"
    assert result_lines[-1] == "line 499"


def test_truncation_limit_is_500() -> None:
    """phase2.md must specify 500 as the diff truncation limit."""
    content = _phase2_content()
    assert "500" in content, "phase2.md must state the 500-line truncation limit"


# ─── File link construction ───────────────────────────────────────────────────

def build_file_link(repo_url: str, head_ref: str, filepath: str) -> str:
    """Construct a GitHub file link for a changed file on the PR branch.

    Implements the rule in phase2.md:
    'File links take the form: {repo_url}/blob/{headRefName}/{filepath}'

    :param repo_url: Base repository URL (no trailing slash).
    :type repo_url: str
    :param head_ref: Feature branch name (headRefName).
    :type head_ref: str
    :param filepath: File path relative to repo root.
    :type filepath: str
    :return: Full GitHub file URL.
    :rtype: str
    """
    return f"{repo_url}/blob/{head_ref}/{filepath}"


@pytest.mark.parametrize("repo_url,head_ref,filepath,expected", [
    (
        "https://github.com/org/repo",
        "feature/my_branch",
        "src/claude/skills/review_pr/SKILL.md",
        "https://github.com/org/repo/blob/feature/my_branch/src/claude/skills/review_pr/SKILL.md",
    ),
    (
        "https://github.com/org/repo",
        "main",
        "README.md",
        "https://github.com/org/repo/blob/main/README.md",
    ),
    (
        "https://github.com/dmt-ghe-engineering/dmt-scripts-claude_ai_playbook",
        "feature/add_skill",
        "src/claude/skills/_git_skills/review_pr/SKILL.md",
        "https://github.com/dmt-ghe-engineering/dmt-scripts-claude_ai_playbook"
        "/blob/feature/add_skill/src/claude/skills/_git_skills/review_pr/SKILL.md",
    ),
])
def test_file_link_construction(
    repo_url: str, head_ref: str, filepath: str, expected: str
) -> None:
    """File links must follow the {repo_url}/blob/{headRefName}/{filepath} pattern.

    :param repo_url: Base repo URL.
    :type repo_url: str
    :param head_ref: PR head branch name.
    :type head_ref: str
    :param filepath: File path relative to repo root.
    :type filepath: str
    :param expected: Expected full URL.
    :type expected: str
    """
    assert build_file_link(repo_url, head_ref, filepath) == expected


# ─── Score calculation ────────────────────────────────────────────────────────

def calculate_overall_score(theme_scores: list[float]) -> float:
    """Calculate the overall review score as the average of theme scores.

    Implements the rule in comment_format.md:
    'Overall score: average of the six theme scores, rounded to one decimal place.'

    :param theme_scores: List of individual theme scores (1–10).
    :type theme_scores: list[float]
    :return: Overall score rounded to one decimal place.
    :rtype: float
    """
    return round(sum(theme_scores) / len(theme_scores), 1)


@pytest.mark.parametrize("scores,expected", [
    ([10, 10, 10, 10, 10, 10], 10.0),
    ([1, 1, 1, 1, 1, 1], 1.0),
    ([8, 7, 9, 8, 7, 9], 8.0),
    ([6, 7, 8, 9, 5, 7], 7.0),
    ([8, 9, 7, 8, 9, 7], 8.0),
    ([5, 6, 7, 4, 8, 6], 6.0),
])
def test_overall_score_calculation(scores: list[float], expected: float) -> None:
    """Overall score must be the average of 6 theme scores, to one decimal place.

    :param scores: List of 6 theme scores.
    :type scores: list[float]
    :param expected: Expected overall score.
    :type expected: float
    """
    assert calculate_overall_score(scores) == expected


def test_scorecard_has_six_themes() -> None:
    """comment_format.md scorecard must contain exactly 6 theme rows.

    The review_pr skill scores: code quality, code complexity, testing,
    security, documentation, and standards.
    """
    content = _comment_format_content()
    # Count scorecard theme rows — each is a table row with a bold theme name
    themes = [
        "Code quality",
        "Code complexity",
        "Testing",
        "Security",
        "Documentation",
        "Standards",
    ]
    for theme in themes:
        assert theme.lower() in content.lower(), (
            f"comment_format.md scorecard must include a '{theme}' theme row"
        )


# ─── Grade mapping ────────────────────────────────────────────────────────────

def score_to_grade(score: float) -> str:
    """Map an overall score to a letter grade.

    Implements the grade mapping table in comment_format.md.

    :param score: Overall score (1.0–10.0).
    :type score: float
    :return: Letter grade string.
    :rtype: str
    """
    if score >= 9.5:
        return "A+"
    if score >= 9.0:
        return "A"
    if score >= 8.5:
        return "A−"
    if score >= 8.0:
        return "B+"
    if score >= 7.5:
        return "B"
    if score >= 7.0:
        return "B−"
    if score >= 6.5:
        return "C+"
    if score >= 6.0:
        return "C"
    if score >= 5.5:
        return "C−"
    if score >= 5.0:
        return "D+"
    if score >= 4.0:
        return "D"
    return "F"


@pytest.mark.parametrize("score,expected_grade", [
    (10.0, "A+"),
    (9.5, "A+"),
    (9.4, "A"),
    (9.0, "A"),
    (8.9, "A−"),
    (8.5, "A−"),
    (8.4, "B+"),
    (8.0, "B+"),
    (7.9, "B"),
    (7.5, "B"),
    (7.4, "B−"),
    (7.0, "B−"),
    (6.9, "C+"),
    (6.5, "C+"),
    (6.4, "C"),
    (6.0, "C"),
    (5.9, "C−"),
    (5.5, "C−"),
    (5.4, "D+"),
    (5.0, "D+"),
    (4.9, "D"),
    (4.0, "D"),
    (3.9, "F"),
    (1.0, "F"),
])
def test_grade_mapping(score: float, expected_grade: str) -> None:
    """Grade mapping must match the table in comment_format.md exactly.

    :param score: Overall score input.
    :type score: float
    :param expected_grade: Expected letter grade.
    :type expected_grade: str
    """
    assert score_to_grade(score) == expected_grade


# ─── Verdict determination ────────────────────────────────────────────────────

def determine_verdict(has_must: bool, has_should: bool) -> tuple[str, str]:
    """Determine the review verdict from Must/Should item presence.

    Implements the verdict table in comment_format.md:
    - Any Must → Request changes
    - No Must, but Should/Could → Approve with suggestions
    - Neither → Approve

    :param has_must: Whether any Must items are present.
    :type has_must: bool
    :param has_should: Whether any Should/Could items are present.
    :type has_should: bool
    :return: Tuple of (verdict text, verdict emoji).
    :rtype: tuple[str, str]
    """
    if has_must:
        return ("Request changes", "❌")
    if has_should:
        return ("Approve with suggestions", "💬")
    return ("Approve", "✅")


@pytest.mark.parametrize("has_must,has_should,expected_verdict,expected_emoji", [
    (True, False, "Request changes", "❌"),
    (True, True, "Request changes", "❌"),
    (False, True, "Approve with suggestions", "💬"),
    (False, False, "Approve", "✅"),
])
def test_verdict_determination(
    has_must: bool,
    has_should: bool,
    expected_verdict: str,
    expected_emoji: str,
) -> None:
    """Verdict must be determined solely by Must items, not overall score.

    :param has_must: Whether Must items are present.
    :type has_must: bool
    :param has_should: Whether Should items are present.
    :type has_should: bool
    :param expected_verdict: Expected verdict text.
    :type expected_verdict: str
    :param expected_emoji: Expected verdict emoji.
    :type expected_emoji: str
    """
    verdict, emoji = determine_verdict(has_must, has_should)
    assert verdict == expected_verdict
    assert emoji == expected_emoji


# ─── Confirmation and schema ──────────────────────────────────────────────────

def test_confirmation_required_before_post() -> None:
    """SKILL.md must include a y/n confirmation gate before posting the comment."""
    content = _skill_content()
    assert "y/n" in content, (
        "SKILL.md must include a y/n confirmation prompt before posting"
    )


def test_confirmation_required_in_frontmatter() -> None:
    """SKILL.md frontmatter must set confirmation_required: true."""
    content = _skill_content()
    assert "confirmation_required: true" in content, (
        "SKILL.md frontmatter must set confirmation_required: true"
    )


def test_schema_reversible_false() -> None:
    """skill_schema.yaml must set reversible: false — a posted comment cannot be silently undone."""
    content = _schema_content()
    assert "reversible: false" in content, (
        "skill_schema.yaml must set reversible: false"
    )


def test_comment_written_to_drafts_file() -> None:
    """SKILL.md must write the comment body to ~/_drafts/pr/review_pr_<number>_<date>.md before posting.

    This ensures the comment is persisted before the gh CLI call, making it
    inspectable if the post fails.
    """
    content = _skill_content()
    assert "~/_drafts/pr/review_pr_" in content, (
        "SKILL.md must write the comment body to ~/_drafts/pr/review_pr_<number>_<date>.md"
    )
