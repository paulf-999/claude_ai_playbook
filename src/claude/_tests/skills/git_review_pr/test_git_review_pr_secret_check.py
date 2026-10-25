# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-22
# Date updated:      2026-10-22
# Version:           1.0.0
# Test quality score: 10/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""git_review_pr's secret check catches real secret shapes and lets ordinary review text through.

The check is a ``grep -nE`` pattern in ``reference/_implementation.md`` that runs on the comment
before it is saved. Issue #388 found it missed Anthropic, OpenAI, Google and Stripe keys and JSON
``"api_key": "..."`` pairs. Each test runs the pattern from the doc itself, so a change to the doc
is what gets tested.

Sample secrets are built by joining pieces, so this file never holds a literal that secret
scanners or the private-key pre-commit hook would flag.
"""
import re
import subprocess

import pytest

from _shared_paths import SKILLS_DIR

# Grouped in the playbook repo (skills/_git_skills/<name>/), flat in a live config (skills/<name>/)
IMPLEMENTATION = next(
    (SKILLS_DIR / rel / "reference" / "_implementation.md" for rel in ("git_review_pr", "_git_skills/git_review_pr")
     if (SKILLS_DIR / rel / "reference" / "_implementation.md").is_file()),
    None,
)
GREP_LINE = re.compile(r"^grep -nE '(?P<pattern>.+)' \"<temp file>\"$", re.M)

SECRETS = {
    "aws": "AKIA" + "ABCDEFGHIJKLMNOP",
    "pem": "-----BEGIN " + "RSA PRIVATE" + " KEY-----",
    "github": "gh" + "p_" + "a" * 36,
    "slack": "xo" + "xb-" + "1234-abcd",
    "anthropic": "sk" + "-ant-" + "api03-" + "b" * 24,
    "openai": "key is sk" + "-proj-" + "c" * 24,
    "google": "AI" + "za" + "d" * 35,
    "stripe": "sk" + "_live_" + "e" * 16,
    "key_value": "password = " + "hunter2hunter2",
    "json_pair": '{"api_key": "' + "f" * 12 + '"}',
}
SAFE = {
    "prose": "The token is read from an environment variable, never hard-coded.",
    "short_value": "password: abc",
    "hyphenated": "See task-runner-configuration-file-for-the-vm for details.",
    "live_word": "the disk_live_metrics_dashboard_panel is unchanged",
}


def secret_pattern():
    """Return the check's pattern exactly as the skill's doc gives it."""
    match = GREP_LINE.search(IMPLEMENTATION.read_text())
    assert match, f"no grep -nE line found in {IMPLEMENTATION}"
    return match["pattern"]


def flagged(text, tmp_path):
    """Tell whether the doc's grep command matches a comment holding this text."""
    comment = tmp_path / "comment.md"
    comment.write_text(f"**Claude review — PR #1**\n\n{text}\n")
    done = subprocess.run(["grep", "-nE", secret_pattern(), str(comment)], capture_output=True, text=True, check=False)
    assert done.returncode in (0, 1), f"grep failed: {done.stderr}"
    return done.returncode == 0


def test_skill_doc_is_found():
    """The checks below prove something only if the skill's implementation doc is found."""
    assert IMPLEMENTATION, f"git_review_pr's reference/_implementation.md not found under {SKILLS_DIR}"


@pytest.mark.parametrize("name", sorted(SECRETS))
def test_secret_is_flagged(name, tmp_path):
    """Every secret shape the doc says it catches is flagged."""
    assert flagged(SECRETS[name], tmp_path), f"{name} sample was not flagged"


@pytest.mark.parametrize("name", sorted(SAFE))
def test_safe_text_passes(name, tmp_path):
    """Ordinary review text, including hyphenated words and short values, is not flagged."""
    assert not flagged(SAFE[name], tmp_path), f"{name} text was wrongly flagged"


def test_check_runs_before_save():
    """Phase 4 lists the secret check before the save step, so a flagged comment never reaches _drafts/."""
    text = IMPLEMENTATION.read_text()
    assert text.index("- **Secret check:**") < text.index("- **Save:**"), "Save comes before the secret check"
