"""
Test suite for hook_style_guide_response_standards_inject.sh

Validates the per-turn salience-injection hook: it must exit 0 and emit valid
JSON whose hookSpecificOutput.additionalContext carries the response-standards
directive markers. This is the "crawl" enforcement path that mirrors the
Desktop/Cowork experience (salient re-injection each turn).

The hook also injects the true submission timestamp (PROMPT_SUBMITTED_AT) so the
timing footer can span reasoning time, and instructs the footer to apply in all
modes including plan mode.
"""

import json
import os
import re
import subprocess

HOOK_SCRIPT = "/home/paul/.claude/hooks/hook_style_guide_response_standards_inject.sh"


class TestResponseStandardsInjectHook:
    """Test the response-standards injection hook."""

    @staticmethod
    def run_hook(env_override=None) -> subprocess.CompletedProcess:
        """Run the injection hook with empty stdin (mirrors UserPromptSubmit).

        Args:
            env_override: Optional dict of environment variables to set for this run.
        """
        env = os.environ.copy()
        if env_override:
            env.update(env_override)

        return subprocess.run(
            [HOOK_SCRIPT],
            input="",
            text=True,
            capture_output=True,
            env=env,
        )

    def test_exits_zero(self):
        """Hook must exit 0 so it never blocks prompt submission."""
        result = self.run_hook()
        assert result.returncode == 0, \
            f"Hook should exit 0, got {result.returncode}. Stderr: {result.stderr}"

    def test_emits_valid_json(self):
        """Hook stdout must be valid JSON with the UserPromptSubmit envelope."""
        result = self.run_hook()
        data = json.loads(result.stdout)
        assert data["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit", \
            f"Expected UserPromptSubmit envelope. Got: {result.stdout}"
        assert "additionalContext" in data["hookSpecificOutput"], \
            f"Missing additionalContext. Got: {result.stdout}"

    def test_context_contains_summary_marker(self):
        """Directive must instruct the **Summary** block."""
        context = json.loads(self.run_hook().stdout)["hookSpecificOutput"]["additionalContext"]
        assert "**Summary**" in context, \
            f"Directive missing **Summary** marker. Got: {context}"

    def test_context_uses_theme_headings(self):
        """Directive must instruct themes as heading lines (not bullets), with points as bullets."""
        context = json.loads(self.run_hook().stdout)["hookSpecificOutput"]["additionalContext"]
        assert "heading" in context.lower(), \
            f"Directive should format themes as headings. Got: {context}"

    def test_context_contains_offer_line(self):
        """Directive must instruct the offer line phrasing."""
        context = json.loads(self.run_hook().stdout)["hookSpecificOutput"]["additionalContext"]
        assert "More detail? (Y/N)" in context, \
            f"Directive missing offer-line phrasing. Got: {context}"

    def test_context_contains_timing_footer(self):
        """Directive must instruct the timing footer."""
        context = json.loads(self.run_hook().stdout)["hookSpecificOutput"]["additionalContext"]
        assert "Response time:" in context, \
            f"Directive missing timing-footer phrasing. Got: {context}"

    def test_context_humanizes_duration(self):
        """Directive must instruct a human-readable duration (e.g. '1min 15s' for >=60s)."""
        context = json.loads(self.run_hook().stdout)["hookSpecificOutput"]["additionalContext"]
        assert "1min 15s" in context, \
            f"Directive should show the human-readable minutes format. Got: {context}"

    def test_context_requests_next_steps_block(self):
        """Directive must instruct a numbered Next steps block for actionable answers."""
        context = json.loads(self.run_hook().stdout)["hookSpecificOutput"]["additionalContext"]
        assert "**Next steps:**" in context, \
            f"Directive missing Next steps block. Got: {context}"
        assert "pick a next step" in context.lower(), \
            f"Directive should offer picking a numbered next step. Got: {context}"
        assert "child bullet" in context.lower(), \
            f"Next steps options should carry a child-bullet description. Got: {context}"

    def test_context_injects_submission_timestamp(self):
        """Directive must inject a real Unix-epoch submission timestamp for the timer start."""
        context = json.loads(self.run_hook().stdout)["hookSpecificOutput"]["additionalContext"]
        assert "__START__" not in context, \
            f"Placeholder was not substituted. Got: {context}"
        assert re.search(r"PROMPT_SUBMITTED_AT=\d{10}", context), \
            f"Directive missing real epoch start timestamp. Got: {context}"

    def test_context_applies_in_plan_mode(self):
        """Directive must state it applies in all modes, including plan mode."""
        context = json.loads(self.run_hook().stdout)["hookSpecificOutput"]["additionalContext"]
        assert "including plan mode" in context.lower(), \
            f"Directive should assert plan-mode coverage. Got: {context}"

    def test_context_bans_timing_placeholder(self):
        """Directive must forbid placeholder footers (e.g. 'checking...') so the number is real."""
        context = json.loads(self.run_hook().stdout)["hookSpecificOutput"]["additionalContext"]
        assert "placeholder" in context.lower(), \
            f"Directive should ban placeholder footers. Got: {context}"
        assert "last tool call" in context.lower(), \
            f"Directive should order the timestamp as the last tool call. Got: {context}"

    # ═════════════════════════════════════════════════════════════════════════════════
    # SKILL WAIVER TESTS — Phase 2 conditional logic
    # ═════════════════════════════════════════════════════════════════════════════════

    def test_skips_injection_when_skill_waives_standards(self):
        """Hook must skip injection when SKILL_WAIVES_RESPONSE_STANDARDS=true.

        Skills that use custom output formats (e.g. multi-phase interactive workflows)
        declare waives_response_standards: true in their contract. The hook checks this
        env var and exits cleanly without injecting the response-standards directive.
        """
        result = self.run_hook(env_override={"SKILL_WAIVES_RESPONSE_STANDARDS": "true"})

        # Must exit 0 (clean, non-blocking exit)
        assert result.returncode == 0, \
            f"Hook should exit 0 when waiver is true. Got {result.returncode}. Stderr: {result.stderr}"

        # Must NOT emit JSON (waiver suppresses injection entirely)
        assert result.stdout.strip() == "", \
            f"Hook should emit no output when waiver is true. Got: {result.stdout}"

    def test_injects_normally_when_waiver_unset(self):
        """Hook must inject directive when waiver is not set (backward compatibility).

        If SKILL_WAIVES_RESPONSE_STANDARDS is unset or false, the hook proceeds with
        normal injection. This ensures existing skills and non-skill responses continue
        to receive the response-standards directive.
        """
        # Test with unset env var (default case)
        result = self.run_hook(env_override={"SKILL_WAIVES_RESPONSE_STANDARDS": "false"})

        # Must exit 0 and emit JSON with directive
        assert result.returncode == 0, \
            f"Hook should exit 0 when waiver is false. Got {result.returncode}. Stderr: {result.stderr}"

        data = json.loads(result.stdout)
        assert "hookSpecificOutput" in data, \
            f"Hook should emit JSON when waiver is false. Got: {result.stdout}"
        assert "**Summary**" in data["hookSpecificOutput"]["additionalContext"], \
            f"Directive should be injected when waiver is false. Got: {result.stdout}"

    def test_honors_waiver_precedence_over_directive(self):
        """Hook must check waiver FIRST, before building the directive.

        This is both a performance and correctness requirement: the waiver check
        should occur at the earliest point, preventing unnecessary processing.
        """
        # When waiver is true, hook exits immediately without reading the directive block
        result_waived = self.run_hook(env_override={"SKILL_WAIVES_RESPONSE_STANDARDS": "true"})

        # When waiver is false or unset, hook proceeds to emit directive
        result_normal = self.run_hook(env_override={"SKILL_WAIVES_RESPONSE_STANDARDS": "false"})

        # Waived: empty output
        assert result_waived.stdout.strip() == "", \
            f"Waived response should have no output. Got: {result_waived.stdout}"

        # Normal: directive output
        assert len(result_normal.stdout) > 0, \
            f"Normal response should have directive output. Got empty string"

        # Verify they're different (waiver genuinely changes behavior)
        assert result_waived.stdout != result_normal.stdout, \
            "Waived and normal responses should differ"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
