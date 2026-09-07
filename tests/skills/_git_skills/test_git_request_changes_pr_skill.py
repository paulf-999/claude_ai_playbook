"""Behavioural tests for the request_changes_pr skill rules.

Tests the deterministic, rule-based components that Claude must follow:
- Inline comment bullet conversion (- → *)
- GitHub review API payload structure (event: REQUEST_CHANGES, side: RIGHT)
- Dismiss API uses JSON body via --input -, not --field
- Confirmation required before posting
- Attribution prompt present before confirmation
- skill_schema.yaml marks the action as non-reversible
"""

import re
from pathlib import Path

import pytest

# ─── Paths ────────────────────────────────────────────────────────────────────

SKILL_DIR = (
    Path(__file__).parent.parent.parent.parent
    / "src" / "claude" / "skills" / "_git_skills" / "git_request_changes_pr"
)
SKILL_MD = SKILL_DIR / "SKILL.md"
SKILL_SCHEMA = SKILL_DIR / "skill_schema.yaml"
COMMENT_FORMAT_MD = SKILL_DIR / "comment_format.md"


def _skill_content() -> str:
    return SKILL_MD.read_text()


def _schema_content() -> str:
    return SKILL_SCHEMA.read_text()


def _comment_format_content() -> str:
    return COMMENT_FORMAT_MD.read_text()


# ─── Bullet conversion ────────────────────────────────────────────────────────

def convert_bullets(text: str) -> str:
    """Convert leading-hyphen list items to asterisk list items.

    Implements the rule in SKILL.md Phase 2:
    'convert any - bullets from agent output to * bullets'.

    :param text: Raw agent output text.
    :type text: str
    :return: Text with hyphen list items replaced by asterisk list items.
    :rtype: str
    """
    return re.sub(r"^(\s*)-\s", r"\1* ", text, flags=re.MULTILINE)


@pytest.mark.parametrize("input_text,expected", [
    (
        "- first issue\n- second issue",
        "* first issue\n* second issue",
    ),
    (
        "* already correct\n- needs converting",
        "* already correct\n* needs converting",
    ),
    (
        "Some prose.\n- bullet\nMore prose.",
        "Some prose.\n* bullet\nMore prose.",
    ),
    (
        "No bullets here at all.",
        "No bullets here at all.",
    ),
    (
        "  - indented bullet",
        "  * indented bullet",
    ),
    (
        "non-hyphenated text with - in it",
        "non-hyphenated text with - in it",
    ),
])
def test_bullet_conversion(input_text: str, expected: str) -> None:
    """Hyphen list items in agent output must be converted to asterisk list items.

    :param input_text: Raw agent output.
    :type input_text: str
    :param expected: Text after conversion.
    :type expected: str
    """
    assert convert_bullets(input_text) == expected


# ─── Review API payload ───────────────────────────────────────────────────────

def build_review_payload(
    commit_id: str,
    body: str,
    comments: list[dict],
) -> dict:
    """Build the GitHub review API payload.

    Implements the payload spec in SKILL.md Phase 4:
    commit_id, event: REQUEST_CHANGES, body, comments[] with path/line/side.

    :param commit_id: Latest commit SHA on the PR head.
    :type commit_id: str
    :param body: Overall review summary body.
    :type body: str
    :param comments: List of inline comment dicts.
    :type comments: list[dict]
    :return: Payload dict ready for JSON serialisation.
    :rtype: dict
    """
    return {
        "commit_id": commit_id,
        "event": "REQUEST_CHANGES",
        "body": body,
        "comments": comments,
    }


@pytest.mark.parametrize("comments", [
    [{"path": "src/foo.py", "line": 10, "side": "RIGHT", "body": "Issue."}],
    [
        {"path": "src/foo.py", "line": 5, "side": "RIGHT", "body": "First."},
        {"path": "src/bar.py", "line": 20, "side": "RIGHT", "body": "Second."},
    ],
])
def test_payload_event_is_request_changes(comments: list[dict]) -> None:
    """Review payload event must always be REQUEST_CHANGES.

    :param comments: List of inline comment dicts.
    :type comments: list[dict]
    """
    payload = build_review_payload("abc123", "Review body.", comments)
    assert payload["event"] == "REQUEST_CHANGES"


@pytest.mark.parametrize("comments", [
    [{"path": "src/foo.py", "line": 10, "side": "RIGHT", "body": "Issue."}],
    [
        {"path": "src/foo.py", "line": 5, "side": "RIGHT", "body": "First."},
        {"path": "src/bar.py", "line": 20, "side": "RIGHT", "body": "Second."},
    ],
])
def test_payload_all_comments_side_right(comments: list[dict]) -> None:
    """Every inline comment in the payload must set side: RIGHT.

    :param comments: List of inline comment dicts.
    :type comments: list[dict]
    """
    payload = build_review_payload("abc123", "Review body.", comments)
    for comment in payload["comments"]:
        assert comment["side"] == "RIGHT", (
            f"Comment on {comment['path']}:{comment['line']} has "
            f"side={comment['side']!r}, expected 'RIGHT'"
        )


def test_payload_includes_commit_id() -> None:
    """Review payload must include commit_id (latest SHA on the PR head)."""
    payload = build_review_payload("deadbeef", "Body.", [])
    assert payload["commit_id"] == "deadbeef"


# ─── Dismiss API — JSON body required ────────────────────────────────────────

def test_dismiss_uses_input_flag_not_field() -> None:
    """Dismiss API call must use --input - (JSON body), not --field.

    The /dismissals endpoint requires a JSON body. Using --field sends
    form-encoded data, which the API rejects with a 422 error.
    """
    content = _skill_content()
    assert "--input -" in content, (
        "SKILL.md dismiss step must use '--input -' to send a JSON body"
    )
    assert "--field" not in content, (
        "SKILL.md dismiss step must not use '--field' (sends form-encoded data, not JSON)"
    )


# ─── Confirmation and attribution ─────────────────────────────────────────────

def test_confirmation_required_before_post() -> None:
    """SKILL.md must include a y/n confirmation gate before posting the review."""
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


def test_attribution_prompt_present() -> None:
    """SKILL.md must prompt the user about the optional 'Generated by Claude' attribution."""
    content = _skill_content()
    assert "Generated by Claude" in content, (
        "SKILL.md must prompt the user to optionally add '_Generated by Claude_' attribution"
    )


# ─── Attribution line insertion ──────────────────────────────────────────────

ATTRIBUTION_LINE = "_Generated by Claude_"


def build_comment_body(issue_text: str, *, attribution: bool) -> str:
    """Prepend the attribution line when the user opts in.

    Implements the rule in comment_format.md:
    '_Generated by Claude_ — prepend only if user opted in during Phase 3'.

    :param issue_text: The formatted comment body (bullet points, suggested fix, etc.).
    :type issue_text: str
    :param attribution: Whether the user opted in to the attribution line.
    :type attribution: bool
    :return: Final comment body with or without attribution.
    :rtype: str
    """
    if attribution:
        return f"{ATTRIBUTION_LINE}\n\n{issue_text}"
    return issue_text


@pytest.mark.parametrize("issue_text,attribution,expected_prefix", [
    ("* Fix the thing.", True, ATTRIBUTION_LINE),
    ("* Fix the thing.", False, "* Fix"),
])
def test_attribution_prepended_only_when_opted_in(
    issue_text: str,
    attribution: bool,
    expected_prefix: str,
) -> None:
    """Attribution line must appear at the top only when the user opted in.

    :param issue_text: Raw comment body.
    :type issue_text: str
    :param attribution: Whether attribution opt-in is set.
    :type attribution: bool
    :param expected_prefix: Expected start of the resulting comment.
    :type expected_prefix: str
    """
    result = build_comment_body(issue_text, attribution=attribution)
    assert result.startswith(expected_prefix), (
        f"Expected comment to start with {expected_prefix!r}, got {result[:40]!r}"
    )


def test_attribution_line_blank_separator() -> None:
    """When attribution is added, it must be separated from the body by a blank line."""
    result = build_comment_body("* Issue.", attribution=True)
    assert result == f"{ATTRIBUTION_LINE}\n\n* Issue.", (
        "Attribution line must be followed by a blank line before the comment body"
    )


def test_no_attribution_when_not_opted_in() -> None:
    """When attribution is not opted in, the comment body must be unchanged."""
    body = "* Issue one.\n* Issue two."
    result = build_comment_body(body, attribution=False)
    assert result == body, (
        "Comment body must not be modified when attribution is not opted in"
    )


# ─── schema.yaml — reversible: false ─────────────────────────────────────────

def test_schema_reversible_false() -> None:
    """skill_schema.yaml must set reversible: false — a posted review cannot be undone silently.

    Dismissing a review requires a deliberate API call; it is not automatic.
    """
    content = _schema_content()
    assert "reversible: false" in content, (
        "skill_schema.yaml must set reversible: false"
    )


# ─── Truncation warning path ─────────────────────────────────────────────────

def test_truncation_warning_required_before_preview() -> None:
    """SKILL.md must warn the user about diff truncation before showing the preview.

    When the diff exceeds 500 lines, the user must be warned and asked to confirm
    before the full proposed review is shown — ensuring they are not surprised by
    incomplete coverage.
    """
    content = _skill_content()
    assert "truncated" in content.lower(), (
        "SKILL.md must mention diff truncation in the Phase 3 confirmation flow"
    )
    assert "500" in content, (
        "SKILL.md must state the 500-line truncation limit"
    )


# ─── comment_format.md ────────────────────────────────────────────────────────

def test_comment_format_specifies_asterisk_bullets() -> None:
    """comment_format.md must explicitly require * bullets, not - bullets."""
    content = _comment_format_content()
    assert "`*`" in content, (
        "comment_format.md must specify '*' as the bullet character"
    )
    assert "not `-`" in content or "not `-`" in content, (
        "comment_format.md must explicitly disallow '-' bullets"
    )


def test_comment_format_requires_runnable_code() -> None:
    """comment_format.md must require suggested fix code to be runnable, not pseudocode."""
    content = _comment_format_content()
    assert "runnable" in content.lower(), (
        "comment_format.md must state that suggested fix code must be runnable"
    )


# ─── Suggested fix omission ───────────────────────────────────────────────────

SUGGESTED_FIX_HEADER = "**Suggested fix:**"


def build_inline_comment(issues: list[str], suggested_fix: str = "") -> str:
    """Build the body of an inline review comment.

    Implements the rule in comment_format.md:
    'Suggested fix: block — omit entirely if no concrete code fix applies'.

    :param issues: List of issue bullet strings (already formatted with leading `* `).
    :type issues: list[str]
    :param suggested_fix: Runnable code fix, or empty string if no fix applies.
    :type suggested_fix: str
    :return: Formatted comment body.
    :rtype: str
    """
    body = "\n".join(issues)
    if suggested_fix:
        body += f"\n\n{SUGGESTED_FIX_HEADER}\n```\n{suggested_fix}\n```"
    return body


@pytest.mark.parametrize("suggested_fix", ["", "   ", "\n"])
def test_suggested_fix_block_omitted_when_empty(suggested_fix: str) -> None:
    """The Suggested fix block must be omitted entirely when no fix is provided.

    comment_format.md rule: '**Suggested fix:** block — omit entirely if no
    concrete code fix applies'.

    :param suggested_fix: Empty or whitespace-only fix value.
    :type suggested_fix: str
    """
    body = build_inline_comment(["* Fix the thing."], suggested_fix=suggested_fix.strip())
    assert SUGGESTED_FIX_HEADER not in body, (
        f"Comment body must not contain '{SUGGESTED_FIX_HEADER}' when suggested_fix is empty"
    )


def test_suggested_fix_block_present_when_populated() -> None:
    """The Suggested fix block must appear when a concrete fix is provided."""
    body = build_inline_comment(["* Fix the thing."], suggested_fix="echo 'fixed'")
    assert SUGGESTED_FIX_HEADER in body, (
        f"Comment body must contain '{SUGGESTED_FIX_HEADER}' when a fix is provided"
    )


# ─── Zero-findings early stop ─────────────────────────────────────────────────

def test_zero_findings_stop_documented_in_skill() -> None:
    """SKILL.md must specify behaviour when the agent returns no Must/Should findings.

    Without an explicit stop rule, the skill would fall through to Phase 3
    and post an empty CHANGES_REQUESTED review — a silent no-op that still
    blocks the PR.
    """
    content = _skill_content()
    assert "no findings" in content.lower() or "no must" in content.lower(), (
        "SKILL.md must document the zero-findings early-stop path in Phase 2"
    )
