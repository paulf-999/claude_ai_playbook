"""Unit tests for src/claude/hooks/claude_prompt_reviewer.py.

Tests cover all check functions, output building, and the full emit_output
paths (pass, low severity, high severity).
"""

import json
import sys
from pathlib import Path

import pytest

# Add the hooks directory to the path so the module can be imported directly.
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "claude" / "hooks"))

from claude_prompt_reviewer import (  # noqa: E402
    CheckResult,
    _build_suggested_prompt,
    _build_tip_text,
    check_risky_actions,
    check_specific_context,
    check_verification,
    emit_output,
    read_prompt,
)


# ---------------------------------------------------------------------------
# check_specific_context
# ---------------------------------------------------------------------------


class TestCheckSpecificContext:
    """Tests for the specific-context check."""

    def test_passes_when_file_reference_present(self) -> None:
        """No issue raised when the prompt references a file path."""
        prompt = "fix the validation logic in src/auth/login.py"
        assert check_specific_context(prompt) is None

    def test_passes_when_at_mention_present(self) -> None:
        """No issue raised when the prompt uses an @file mention."""
        prompt = "update the error handling in @src/utils/helpers.py"
        assert check_specific_context(prompt) is None

    def test_passes_when_file_extension_present(self) -> None:
        """No issue raised when the prompt names a file with an extension."""
        prompt = "add a new column to the orders.sql staging model"
        assert check_specific_context(prompt) is None

    def test_passes_for_non_implementation_prompt(self) -> None:
        """No issue raised for prompts that are not implementation requests."""
        prompt = "what does the staging layer do in this project"
        assert check_specific_context(prompt) is None

    def test_passes_for_short_prompt(self) -> None:
        """No issue raised for prompts below the minimum word threshold."""
        prompt = "fix that"
        assert check_specific_context(prompt) is None

    def test_flags_implementation_prompt_without_reference(self) -> None:
        """Issue raised for an implementation prompt with no file reference."""
        prompt = "add a function to validate email addresses in the auth module"
        result = check_specific_context(prompt)
        assert result is not None
        assert result.severity == "low"
        assert result.check == "specific_context"

    def test_flags_fix_prompt_without_reference(self) -> None:
        """Issue raised for a fix prompt with no file or path reference."""
        prompt = "fix the login bug where session expires too quickly"
        result = check_specific_context(prompt)
        assert result is not None
        assert result.severity == "low"


# ---------------------------------------------------------------------------
# check_verification
# ---------------------------------------------------------------------------


class TestCheckVerification:
    """Tests for the verification-criteria check."""

    def test_passes_when_test_keyword_present(self) -> None:
        """No issue raised when the prompt mentions 'test'."""
        prompt = "add a validateEmail function and run the tests after"
        assert check_verification(prompt) is None

    def test_passes_when_verify_keyword_present(self) -> None:
        """No issue raised when the prompt includes 'verify'."""
        prompt = "implement the retry logic and verify it works with make test"
        assert check_verification(prompt) is None

    def test_passes_when_run_keyword_present(self) -> None:
        """No issue raised when the prompt says 'run' (e.g. run the tests)."""
        prompt = "add the endpoint and run pytest to check it passes"
        assert check_verification(prompt) is None

    def test_passes_for_non_implementation_prompt(self) -> None:
        """No issue raised for prompts that are not implementation requests."""
        prompt = "explain how the DAG scheduler works in Airflow"
        assert check_verification(prompt) is None

    def test_passes_for_short_prompt(self) -> None:
        """No issue raised for prompts below the minimum word threshold."""
        prompt = "create a helper"
        assert check_verification(prompt) is None

    def test_flags_implementation_prompt_without_verification(self) -> None:
        """Issue raised for an implementation prompt with no verification criteria."""
        prompt = "add a function to calculate the total order value including tax"
        result = check_verification(prompt)
        assert result is not None
        assert result.severity == "low"
        assert result.check == "verification"

    def test_flags_build_prompt_without_verification(self) -> None:
        """Issue raised for a build prompt with no success criteria."""
        prompt = "build a new staging model for the salesforce opportunity table"
        result = check_verification(prompt)
        assert result is not None
        assert result.severity == "low"


# ---------------------------------------------------------------------------
# check_risky_actions
# ---------------------------------------------------------------------------


class TestCheckRiskyActions:
    """Tests for the risky-action check."""

    @pytest.mark.parametrize("prompt,expected_label", [
        ("drop table dim_merchant", "DROP TABLE"),
        ("DROP TABLE staging.orders", "DROP TABLE"),
        ("drop the database entirely", "DROP DATABASE / SCHEMA"),
        ("drop the schema for dev environment", "DROP DATABASE / SCHEMA"),
        ("truncate orders_staging", "TRUNCATE"),
        ("rm -rf the temp directory", "rm -rf"),
        ("rm -r /tmp/data", "rm -rf"),
        ("git push origin main --force", "git --force"),
        ("git commit --no-verify", "git --no-verify"),
        ("delete all the records in the table", "bulk delete"),
        ("delete every entry in the staging table", "bulk delete"),
    ])
    def test_flags_risky_pattern(self, prompt: str, expected_label: str) -> None:
        """Each known risky pattern is detected and labelled correctly."""
        result = check_risky_actions(prompt)
        assert result is not None
        assert result.severity == "high"
        assert result.check == "risky_action"
        assert result.matched == expected_label

    @pytest.mark.parametrize("prompt", [
        "add a delete function for a single order by ID",
        "git push origin feature/my_branch",
        "update the merge logic in the dbt model",
        "remove the unused import from utils.py",
    ])
    def test_passes_safe_prompt(self, prompt: str) -> None:
        """Safe prompts are not flagged as risky."""
        assert check_risky_actions(prompt) is None


# ---------------------------------------------------------------------------
# _build_suggested_prompt
# ---------------------------------------------------------------------------


class TestBuildSuggestedPrompt:
    """Tests for the suggested prompt builder."""

    def test_adds_file_prefix_for_context_issue(self) -> None:
        """File prefix is prepended when specific_context check fails."""
        results = [CheckResult(severity="low", check="specific_context", tip="")]
        suggested = _build_suggested_prompt("fix the login bug", results)
        assert "specify file" in suggested
        assert "fix the login bug" in suggested

    def test_adds_verification_suffix_for_verification_issue(self) -> None:
        """Verification suffix is appended when verification check fails."""
        results = [CheckResult(severity="low", check="verification", tip="")]
        suggested = _build_suggested_prompt("add a validate function", results)
        assert "make test" in suggested
        assert "add a validate function" in suggested

    def test_combines_both_when_both_fail(self) -> None:
        """Both prefix and suffix are added when both checks fail."""
        results = [
            CheckResult(severity="low", check="specific_context", tip=""),
            CheckResult(severity="low", check="verification", tip=""),
        ]
        suggested = _build_suggested_prompt("add error handling", results)
        assert "specify file" in suggested
        assert "make test" in suggested


# ---------------------------------------------------------------------------
# _build_tip_text
# ---------------------------------------------------------------------------


class TestBuildTipText:
    """Tests for the full tip message builder."""

    def test_includes_issue_description(self) -> None:
        """The tip text includes the issue description from the check result."""
        results = [CheckResult(severity="low", check="verification", tip="No verification criteria detected.")]
        tip = _build_tip_text("add a function", results)
        assert "No verification criteria detected." in tip

    def test_includes_suggested_prompt(self) -> None:
        """The tip text includes a suggested prompt."""
        results = [CheckResult(severity="low", check="verification", tip="x")]
        tip = _build_tip_text("implement the retry logic", results)
        assert "Suggested prompt:" in tip
        assert "make test" in tip

    def test_includes_docs_link(self) -> None:
        """The tip text references the best-practices docs URL."""
        results = [CheckResult(severity="low", check="specific_context", tip="x")]
        tip = _build_tip_text("refactor the handler", results)
        assert "best-practices" in tip


# ---------------------------------------------------------------------------
# read_prompt
# ---------------------------------------------------------------------------


class TestReadPrompt:
    """Tests for stdin JSON parsing."""

    def test_reads_prompt_from_valid_json(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Prompt string is extracted from valid JSON input."""
        import io
        monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"prompt": "fix the bug"})))
        assert read_prompt() == "fix the bug"

    def test_returns_empty_string_on_invalid_json(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Empty string returned when stdin contains invalid JSON."""
        import io
        monkeypatch.setattr("sys.stdin", io.StringIO("not json"))
        assert read_prompt() == ""

    def test_returns_empty_string_on_missing_prompt_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Empty string returned when JSON has no 'prompt' key."""
        import io
        monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"session_id": "abc"})))
        assert read_prompt() == ""


# ---------------------------------------------------------------------------
# emit_output
# ---------------------------------------------------------------------------


class TestEmitOutput:
    """Tests for the JSON output emitter."""

    def test_exits_cleanly_with_no_results(self, capsys: pytest.CaptureFixture) -> None:
        """Exits 0 with no stdout output when there are no issues."""
        with pytest.raises(SystemExit) as exc:
            emit_output("a clean prompt", [])
        assert exc.value.code == 0
        assert capsys.readouterr().out == ""

    def test_emits_additional_context_for_low_severity(self, capsys: pytest.CaptureFixture) -> None:
        """Outputs additionalContext JSON for low-severity results."""
        results = [CheckResult(severity="low", check="verification", tip="No verification criteria detected.")]
        with pytest.raises(SystemExit) as exc:
            emit_output("add a helper function", results)
        assert exc.value.code == 0
        output = json.loads(capsys.readouterr().out)
        assert "additionalContext" in output
        assert "decision" not in output

    def test_emits_block_decision_for_high_severity(self, capsys: pytest.CaptureFixture) -> None:
        """Outputs block decision JSON for high-severity results."""
        results = [CheckResult(severity="high", check="risky_action", tip="Risky.", matched="DROP TABLE")]
        with pytest.raises(SystemExit) as exc:
            emit_output("drop table orders", results)
        assert exc.value.code == 0
        output = json.loads(capsys.readouterr().out)
        assert output["decision"] == "block"
        assert "DROP TABLE" in output["reason"]

    def test_high_severity_takes_precedence_over_low(self, capsys: pytest.CaptureFixture) -> None:
        """Block decision is emitted even when low-severity results are also present."""
        results = [
            CheckResult(severity="high", check="risky_action", tip="Risky.", matched="rm -rf"),
            CheckResult(severity="low", check="verification", tip="No verification."),
        ]
        with pytest.raises(SystemExit):
            emit_output("rm -rf /tmp and add a helper", results)
        output = json.loads(capsys.readouterr().out)
        assert output["decision"] == "block"
