# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-22
# Date updated:      2026-10-26
# Version:           1.1.0
# Test quality score: 10/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""git_review_pr's secret check catches real secret shapes and lets ordinary review text through.

The check is a ``grep`` pattern in ``reference/_implementation.md`` that runs on the comment
before it is saved. Issue #388 found it missed Anthropic, OpenAI, Google and Stripe keys and JSON
``"api_key": "..."`` pairs, and issue #394 added fine-grained GitHub tokens, single-quoted pairs,
any letter case and line-numbers-only output. Each test runs the pattern from the doc itself, so a change to the doc
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
GREP_LINE = re.compile(r"^grep -(?P<flags>[a-zA-Z]+) '(?P<pattern>.+)' \"<temp file>\"(?P<pipe>.*)$", re.M)

SECRETS = {
    "aws": "AKIA" + "ABCDEFGHIJKLMNOP",
    "pem": "-----BEGIN " + "RSA PRIVATE" + " KEY-----",
    "github": "gh" + "p_" + "a" * 36,
    "github_fine_grained": "github" + "_pat_" + "g" * 30,
    "slack": "xo" + "xb-" + "1234-abcd",
    "anthropic": "sk" + "-ant-" + "api03-" + "b" * 24,
    "openai": "key is sk" + "-proj-" + "c" * 24,
    "google": "AI" + "za" + "d" * 35,
    "stripe": "sk" + "_live_" + "e" * 16,
    "key_value": "password = " + "hunter2hunter2",
    "json_pair": '{"api_key": "' + "f" * 12 + '"}',
    "single_quoted_pair": "{'api_key': '" + "h" * 12 + "'}",
    "upper_case_key": "PASSWORD=" + "hunter2hunter2",
}
SAFE = {
    "prose": "The token is read from an environment variable, never hard-coded.",
    "short_value": "password: abc",
    "hyphenated": "See task-runner-configuration-file-for-the-vm for details.",
    "live_word": "the disk_live_metrics_dashboard_panel is unchanged",
}


def grep_line():
    """Return the check's grep command, split into flags, pattern and pipe, exactly as the doc gives it."""
    match = GREP_LINE.search(IMPLEMENTATION.read_text())
    assert match, f"no grep line found in {IMPLEMENTATION}"
    return match


def flagged(text, tmp_path):
    """Tell whether the doc's grep command matches a comment holding this text."""
    comment = tmp_path / "comment.md"
    comment.write_text(f"**Claude review — PR #1**\n\n{text}\n")
    line = grep_line()
    command = ["grep", f"-{line['flags']}", line["pattern"], str(comment)]
    done = subprocess.run(command, capture_output=True, text=True, check=False)
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


def test_check_ignores_case():
    """The grep runs with -i, so upper-case keywords such as PASSWORD= are caught."""
    assert "i" in grep_line()["flags"], "the secret check's grep is missing -i"


def test_check_prints_line_numbers_only():
    """The grep output goes through cut, so only line numbers print and the secret never shows."""
    assert grep_line()["pipe"].strip() == "| cut -d: -f1", "the secret check doesn't pipe through cut -d: -f1"


def test_check_runs_before_save():
    """Phase 5 lists the secret check before the save step, so a flagged comment never reaches _drafts/."""
    text = IMPLEMENTATION.read_text()
    assert text.index("- **Secret check:**") < text.index("- **Save:**"), "Save comes before the secret check"
