"""
Test suite for hook_style_guide_response_standards.sh

Validates response format compliance: Summary structure, offer line, timing footer.
"""

import subprocess
import pytest


class TestResponseStandardsHook:
    """Test response standards enforcement hook."""

    @staticmethod
    def run_hook(response: str) -> str:
        """Run the hook with given response content and return output."""
        hook_script = "/home/paul/.claude/hooks/hook_style_guide_response_standards.sh"
        result = subprocess.run(
            [hook_script],
            input=response,
            text=True,
            capture_output=True,
        )
        return result.stdout + result.stderr

    def test_valid_response_passes(self):
        """Valid response with all required elements should pass (no flags)."""
        response = """**Summary**
- 🎯 **First point:** detailed explanation here (15 words max)
- 📋 **Second point:** another key item (15 words max)
- ✅ **Third point:** final consideration (15 words max)

More detail? (Y/N)

Response time (post-reasoning): 2s"""

        output = self.run_hook(response)
        assert "🚩 Response Standards Check" not in output, \
            f"Valid response should not trigger flags. Output: {output}"

    def test_missing_summary_flagged(self):
        """Response missing Summary structure should be flagged."""
        response = """This is a substantive response that is definitely long enough to meet the minimum word count
requirement for validation. It contains enough words to be considered a real response but it is
missing the proper Summary structure that should be included at the beginning of any substantive response.
More detail? (Y/N)

Response time (post-reasoning): 1s"""

        output = self.run_hook(response)
        assert "Missing **Summary** block" in output, \
            f"Should flag missing Summary. Output: {output}"

    def test_missing_offer_line_flagged(self):
        """Response missing offer line should be flagged."""
        response = """**Summary**
- 🎯 **Point one:** This is a detailed explanation that provides comprehensive information about the topic
- ✅ **Point two:** More detail about the second point with sufficient elaboration to make it substantive

This is additional context content that extends this response to ensure it meets the minimum word count
requirement for validation to be triggered against the response standards.

Response time (post-reasoning): 1s"""

        output = self.run_hook(response)
        assert "Missing offer line" in output, \
            f"Should flag missing offer line. Output: {output}"

    def test_missing_timing_footer_flagged(self):
        """Response missing timing footer should be flagged."""
        response = """**Summary**
- 🎯 **Point one:** This is a detailed explanation that provides comprehensive information about the topic
- ✅ **Point two:** More detail about the second point with sufficient elaboration to make it substantive

This is additional context content that extends this response to ensure it meets the minimum word count
requirement for validation to be triggered against the response standards.

More detail? (Y/N)"""

        output = self.run_hook(response)
        assert "Missing response timing footer" in output, \
            f"Should flag missing timing footer. Output: {output}"

    def test_content_after_timing_flagged(self):
        """Response with content after timing footer should be flagged."""
        response = """**Summary**
- 🎯 **Point one:** This is a detailed explanation that provides comprehensive information about the topic
- ✅ **Point two:** More detail about the second point with sufficient elaboration to make it substantive

This is additional context content that extends this response to ensure it meets the minimum word count
requirement for validation to be triggered against the response standards.

More detail? (Y/N)

Response time (post-reasoning): 1s

Extra content here should not be present and this violates the standard."""

        output = self.run_hook(response)
        assert "Content found after timing footer" in output, \
            f"Should flag content after timing. Output: {output}"

    def test_short_answer_waived(self):
        """Short answer (<100 words) should be waived."""
        response = "This is a short answer. No flags expected."

        output = self.run_hook(response)
        assert "🚩 Response Standards Check" not in output, \
            f"Short answer should be waived. Output: {output}"

    def test_skill_output_waived(self):
        """Skill output (with skill markers) should be waived."""
        response = """⎿  Done (3 tool uses · 18.6k tokens · 8s)

This is skill output with extended content that would normally be flagged,
but skill markers indicate it's from a skill invocation and should be waived."""

        output = self.run_hook(response)
        assert "🚩 Response Standards Check" not in output, \
            f"Skill output should be waived. Output: {output}"

    def test_code_block_waived(self):
        """Code block (starting with triple backticks) should be waived."""
        response = """```python
def foo():
    return "This is a code block"
```

Long code output that would normally require Summary structure."""

        output = self.run_hook(response)
        assert "🚩 Response Standards Check" not in output, \
            f"Code block should be waived. Output: {output}"

    def test_error_message_waived(self):
        """Error message should be waived."""
        response = "Error: File not found"

        output = self.run_hook(response)
        assert "🚩 Response Standards Check" not in output, \
            f"Error message should be waived. Output: {output}"

    def test_plan_mode_waived(self):
        """Plan mode response (with plan file link) should be waived."""
        response = """Planning: /home/paul/.claude/plans/example.md

This is a plan mode response with extended content that would normally
be flagged, but the plan file link indicates plan mode and should be waived."""

        output = self.run_hook(response)
        assert "🚩 Response Standards Check" not in output, \
            f"Plan mode should be waived. Output: {output}"

    def test_multiple_violations_all_flagged(self):
        """Response with multiple violations should flag all of them."""
        response = """This is a long response without proper formatting. It has no summary structure,
no offer line, and no timing footer. It is definitely substantive enough to require
proper formatting according to the response standards, but it violates all three
requirements. This should result in multiple flags being raised by the validation hook.

The response needs to be long enough to be considered substantive, so I'm adding more content
here to ensure the word count is sufficient for the validation to trigger. This is intentional.
"""

        output = self.run_hook(response)
        assert "Missing **Summary** block" in output
        assert "Missing offer line" in output
        assert "Missing response timing footer" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
