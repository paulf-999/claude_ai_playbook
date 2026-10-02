# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-07
# Date updated:      2026-10-02
# Version:           2.1.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Test suite for hook_style_guide_response_standards_inject.sh.

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
import shutil
import subprocess
from pathlib import Path

import pytest

from _shared_paths import CLAUDE_DIR

HOOK_SCRIPT = str(CLAUDE_DIR / "hooks" / "hook_style_guide_response_standards_inject.sh")


class TestResponseStandardsInjectHook:
    """Test the response-standards injection hook."""

    @staticmethod
    def run_hook(env_override=None) -> subprocess.CompletedProcess:
        """Run the injection hook with empty stdin (mirrors UserPromptSubmit).

        :param env_override: Extra environment variables to set for this run.
        :type env_override: dict[str, str] | None
        :return: The completed hook run.
        :rtype: subprocess.CompletedProcess
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

    def test_directive_stays_short(self):
        """Every injection stays in the transcript, so the directive must stay a short reminder."""
        context = json.loads(self.run_hook().stdout)["hookSpecificOutput"]["additionalContext"]
        assert len(context) < 1200, \
            f"Directive is {len(context)} characters — keep it under 1,200 and leave detail to the rule"

    def test_falls_back_to_plain_text_without_jq(self, tmp_path):
        """Without jq the hook still injects, as plain text that Claude Code adds as context."""
        bin_dir = tmp_path / "bin"
        bin_dir.mkdir()
        for tool in ("bash", "cat", "date", "dirname", "grep"):
            (bin_dir / tool).symlink_to(shutil.which(tool))
        result = subprocess.run(
            ["bash", HOOK_SCRIPT], input='{"prompt": "hi"}', text=True, capture_output=True,
            env={"PATH": str(bin_dir)},
        )
        assert result.returncode == 0, f"Hook should exit 0 without jq. Stderr: {result.stderr}"
        assert result.stdout.startswith("RESPONSE STANDARDS"), \
            f"Without jq the hook should print the plain directive. Got: {result.stdout}"
        assert re.search(r"PROMPT_SUBMITTED_AT=\d{10}", result.stdout), \
            f"The plain directive should still carry the timestamp. Got: {result.stdout}"


class TestSkillWaiver:
    """The hook skips injection for /<skill> prompts whose contract waives the standard.

    Each test copies the hook into a temporary config dir with its own skills/,
    because the hook resolves skills relative to its own location.
    """

    @staticmethod
    def make_config(tmp_path: Path) -> Path:
        """Build a temp config dir holding the hook and three sample skills.

        :param tmp_path: pytest temporary directory.
        :return: Path to the copied hook script.
        """
        hooks = tmp_path / "hooks"
        hooks.mkdir()
        hook = hooks / Path(HOOK_SCRIPT).name
        shutil.copy(HOOK_SCRIPT, hook)
        contracts = {
            "skills/_demo_skills/waiving_skill": "name: waiving_skill\nwaives_response_standards: true  # own format\n",
            "skills/_demo_skills/normal_skill": "name: normal_skill\nwaives_response_standards: false\n",
            "skills/flat_skill": "name: flat_skill\nwaives_response_standards: true\n",
        }
        for rel, body in contracts.items():
            skill_dir = tmp_path / rel
            skill_dir.mkdir(parents=True)
            (skill_dir / "skill.contract.yaml").write_text(body)
        return hook

    @staticmethod
    def run(hook: Path, stdin: str, env_override=None) -> subprocess.CompletedProcess:
        """Run a copied hook with the given raw stdin.

        :param hook: Hook script path.
        :param stdin: Raw stdin text (normally a JSON payload).
        :param env_override: Extra environment variables.
        :return: Completed process.
        """
        env = os.environ.copy()
        env.pop("SKILL_WAIVES_RESPONSE_STANDARDS", None)
        env.update(env_override or {})
        return subprocess.run(["bash", str(hook)], input=stdin, text=True, capture_output=True, env=env)

    def run_prompt(self, hook: Path, prompt, env_override=None) -> subprocess.CompletedProcess:
        """Run a copied hook with a UserPromptSubmit payload.

        :param hook: Hook script path.
        :param prompt: Value for the payload's ``prompt`` field.
        :param env_override: Extra environment variables.
        :return: Completed process.
        """
        return self.run(hook, json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": prompt}), env_override)

    @staticmethod
    def injected(result: subprocess.CompletedProcess) -> bool:
        """Return whether the hook emitted the directive.

        :param result: Completed hook run.
        :return: True when stdout carries the Summary directive.
        """
        assert result.returncode == 0, f"Hook must exit 0. Stderr: {result.stderr}"
        return "**Summary**" in result.stdout

    def test_slash_command_for_waiving_skill_skips_injection(self, tmp_path):
        """/<skill> for a skill whose contract waives the standard emits nothing."""
        result = self.run_prompt(self.make_config(tmp_path), "/waiving_skill")
        assert result.returncode == 0, f"Hook must exit 0. Stderr: {result.stderr}"
        assert result.stdout.strip() == "", f"Waived skill should get no injection. Got: {result.stdout}"

    def test_slash_command_with_arguments_still_waives(self, tmp_path):
        """Arguments and leading whitespace after the slash command don't break the match."""
        assert not self.injected(self.run_prompt(self.make_config(tmp_path), "  /waiving_skill --date 2026-08-20")), (
            "arguments after a waiving skill's slash command should still skip injection"
        )

    def test_flat_skill_layout_is_found(self, tmp_path):
        """A contract at skills/<name>/ (no group folder) is honoured too."""
        assert not self.injected(self.run_prompt(self.make_config(tmp_path), "/flat_skill")), (
            "a waiving contract at skills/<name>/ should skip injection"
        )

    def test_non_waiving_skill_still_injects(self, tmp_path):
        """A skill whose contract says false gets the directive."""
        assert self.injected(self.run_prompt(self.make_config(tmp_path), "/normal_skill")), (
            "a contract with waives_response_standards: false should still inject"
        )

    def test_unknown_slash_command_injects(self, tmp_path):
        """A slash command with no matching skill contract gets the directive."""
        assert self.injected(self.run_prompt(self.make_config(tmp_path), "/no_such_skill")), (
            "an unknown slash command should still inject"
        )

    def test_natural_language_mention_injects(self, tmp_path):
        """Naming a waiving skill without a leading slash does not waive."""
        assert self.injected(self.run_prompt(self.make_config(tmp_path), "please run waiving_skill /waiving_skill")), (
            "only a leading slash command can waive injection"
        )

    def test_prefix_of_skill_name_does_not_match(self, tmp_path):
        """/waiving_skillx must not match waiving_skill."""
        assert self.injected(self.run_prompt(self.make_config(tmp_path), "/waiving_skillx")), (
            "a longer name must not match a waiving skill by prefix"
        )

    def test_path_traversal_name_is_rejected(self, tmp_path):
        """Names with path characters never reach the filesystem lookup."""
        assert self.injected(self.run_prompt(self.make_config(tmp_path), "/../skills/flat_skill")), (
            "names with path characters must never reach the skill lookup"
        )

    def test_malformed_or_empty_input_injects(self, tmp_path):
        """Bad JSON, empty stdin, or a non-string prompt fall back to normal injection."""
        hook = self.make_config(tmp_path)
        assert self.injected(self.run(hook, "{not json")), "bad JSON should fall back to injecting"
        assert self.injected(self.run(hook, "")), "empty stdin should fall back to injecting"
        assert self.injected(self.run(hook, "[1, 2]")), "a non-object payload should fall back to injecting"
        assert self.injected(self.run_prompt(hook, 42)), "a non-string prompt should fall back to injecting"

    def test_legacy_env_var_no_longer_waives(self, tmp_path):
        """SKILL_WAIVES_RESPONSE_STANDARDS was never set by anything and is no longer read."""
        result = self.run_prompt(self.make_config(tmp_path), "hello", {"SKILL_WAIVES_RESPONSE_STANDARDS": "true"})
        assert self.injected(result), "the retired env var must no longer waive injection"
        assert "SKILL_WAIVES_RESPONSE_STANDARDS" not in Path(HOOK_SCRIPT).read_text(), (
            "Hook should no longer reference the unused env var"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
