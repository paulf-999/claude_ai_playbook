# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-02
# Date updated:      2026-10-06
# Version:           1.2.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests for claude_kaizen's evals/runner.py, the before/after eval scorer.

The runner sends each eval prompt to ``claude -p`` and checks the reply against
the case's ``must_match`` and ``must_not_match`` regexes. Every test here swaps in
a fake ``subprocess.run``, so no test ever calls Claude or spends tokens.
"""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest
import yaml

from _shared_paths import SKILLS_DIR

# Grouped in the playbook repo (skills/_claude_skills/<name>/), flat in a live config (skills/<name>/)
RUNNER = next(
    (SKILLS_DIR / rel / "evals" / "runner.py" for rel in ("claude_kaizen", "_claude_skills/claude_kaizen")
     if (SKILLS_DIR / rel / "evals" / "runner.py").is_file()),
    SKILLS_DIR / "claude_kaizen" / "evals" / "runner.py",
)
SEEDS = RUNNER.parent / "claude_ai_playbook.yaml"

_spec = importlib.util.spec_from_file_location("kaizen_runner", RUNNER)
runner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(runner)


def fake_claude(
    monkeypatch, stdout: str = "", returncode: int = 0, error: Exception | None = None, stderr: str = "boom"
):
    """Replace ``subprocess.run`` with a fake ``claude -p`` and record each call.

    The isolated config folder is deleted after the call, so its links are captured while the call runs.

    :param monkeypatch: pytest's monkeypatch fixture.
    :param stdout: The reply the fake returns.
    :param returncode: The fake's exit code.
    :param error: An exception to raise instead of replying.
    :param stderr: The fake's error output.
    :return: A list that collects ``(command, prompt, env, cwd, links)`` for every call.
    """
    calls = []

    def run(command, **kwargs):
        config = Path(kwargs["env"].get("CLAUDE_CONFIG_DIR", ""))
        links = {e.name: e.resolve() for e in config.iterdir()} if config.is_dir() else {}
        calls.append((command, kwargs["input"], kwargs["env"], kwargs["cwd"], links))
        if error:
            raise error
        return subprocess.CompletedProcess(command, returncode, stdout=stdout, stderr=stderr)

    monkeypatch.setattr(runner.subprocess, "run", run)
    return calls


def write_evals(tmp_path: Path, *cases: dict) -> Path:
    """Write an eval file holding the given cases.

    :param tmp_path: Folder to write it in.
    :return: The eval file's path.
    """
    path = tmp_path / "evals.yaml"
    path.write_text(yaml.safe_dump({"evals": list(cases)}))
    return path


CASE = {"name": "no_bare_except", "prompt": "Write a try block", "must_match": [r"except \w+"],
        "must_not_match": [r"(?m)^\s*except\s*:"]}


def test_judge_passes_when_patterns_line_up():
    """A reply with every must_match and no must_not_match passes."""
    assert runner.judge("except ValueError:", [r"except \w+"], [r"except\s*:$"]) == ("PASS", "all patterns as expected")


def test_judge_names_every_problem():
    """A failing reply lists both the missing and the forbidden patterns."""
    status, details = runner.judge("except:\n", [r"except \w+"], [r"except\s*:"])
    assert status == "FAIL"
    assert "missing 'except \\\\w+'" in details, details
    assert "found forbidden" in details, details


def test_case_passes_on_a_good_reply(tmp_path, monkeypatch):
    """A good reply from Claude makes the case pass."""
    fake_claude(monkeypatch, stdout="try:\n    x()\nexcept ValueError as e:\n    log(e)\n")
    results = runner.EvalRunner(write_evals(tmp_path, CASE), config_dir=tmp_path).run()
    assert (results["total"], results["passed"], results["failed"]) == (1, 1, 0)


def test_case_fails_on_a_bad_reply(tmp_path, monkeypatch):
    """A reply containing a forbidden pattern fails, which a placeholder runner never did."""
    fake_claude(monkeypatch, stdout="try:\n    x()\nexcept:\n    pass\n")
    results = runner.EvalRunner(write_evals(tmp_path, CASE), config_dir=tmp_path).run("before")
    assert results["context"] == "before"
    assert results["results"][0]["status"] == "FAIL", results


def test_claude_gets_the_prompt_and_the_rules_under_test(tmp_path, monkeypatch):
    """The prompt goes to ``claude -p`` with no tools, from an empty folder, against the chosen rules."""
    patched = tmp_path / "patched"
    patched.mkdir()
    (patched / "CLAUDE.md").write_text("rules")
    calls = fake_claude(monkeypatch, stdout="except KeyError:")
    runner.EvalRunner(write_evals(tmp_path, CASE), config_dir=patched).run()
    command, prompt, env, cwd, links = calls[0]
    assert command == ["claude", "-p", "--tools", ""], "the prompt must not follow --tools, which would swallow it"
    assert prompt == "Write a try block"
    assert not Path(cwd).exists(), "Claude should run in a throwaway folder that's removed afterwards"
    assert links["CLAUDE.md"] == (patched / "CLAUDE.md").resolve(), "the isolated config must link the rules under test"


def test_case_without_patterns_fails_without_calling_claude(tmp_path, monkeypatch):
    """A case with nothing to check fails rather than passing by default, and costs no call."""
    calls = fake_claude(monkeypatch)
    results = runner.EvalRunner(write_evals(tmp_path, {"name": "empty", "prompt": "hi"}), config_dir=tmp_path).run()
    assert results["results"][0]["details"] == "case has no must_match or must_not_match patterns"
    assert calls == [], "a case with no patterns shouldn't spend a Claude call"


def test_case_without_prompt_fails(tmp_path, monkeypatch):
    """A case with no prompt fails."""
    fake_claude(monkeypatch)
    case = {"name": "no_prompt", "must_match": ["x"]}
    results = runner.EvalRunner(write_evals(tmp_path, case), config_dir=tmp_path).run()
    assert results["results"][0] == {"name": "no_prompt", "status": "FAIL", "details": "case has no prompt"}


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        ({"returncode": 2}, "claude exited 2: boom"),
        ({"error": FileNotFoundError()}, "the claude CLI isn't installed or on PATH"),
        ({"error": subprocess.TimeoutExpired("claude", 5)}, "claude didn't answer within 300s"),
    ],
)
def test_cli_problems_fail_the_case_with_a_reason(tmp_path, monkeypatch, kwargs, expected):
    """A missing CLI, a timeout or a non-zero exit fails the case and says why."""
    fake_claude(monkeypatch, **kwargs)
    results = runner.EvalRunner(write_evals(tmp_path, CASE), config_dir=tmp_path).run()
    assert results["results"][0]["details"] == expected


def test_config_dir_comes_from_the_environment_first(tmp_path, monkeypatch):
    """CLAUDE_CONFIG_DIR wins over searching the folders above."""
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "live"))
    assert runner.find_config_dir(tmp_path) == tmp_path / "live"


def test_config_dir_falls_back_to_the_folder_holding_rules(tmp_path, monkeypatch):
    """Without the variable, the nearest parent with a ``rules/`` folder is used."""
    monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
    (tmp_path / "rules").mkdir()
    nested = tmp_path / "skills" / "claude_kaizen" / "evals"
    nested.mkdir(parents=True)
    assert runner.find_config_dir(nested) == tmp_path
    assert runner.find_config_dir(tmp_path / "skills") == tmp_path, "a direct child should find it too"


def test_parse_args_reads_context_config_dir_and_file():
    """Flags set the context and config folder, and the remaining argument is the eval file."""
    parsed = runner.parse_args(["--after", "--config-dir", "/rules", "e.yaml"])
    assert parsed == ("after", Path("/rules"), Path("e.yaml"))
    assert runner.parse_args(["e.yaml"]) == ("current", None, Path("e.yaml"))


def test_seed_evals_use_valid_pass_patterns():
    """Every seed case has a prompt and at least one compilable pattern, and the old field is gone."""
    cases = yaml.safe_load(SEEDS.read_text())["evals"]
    assert cases, f"{SEEDS.name} has no eval cases"
    for case in cases:
        patterns = (case.get("must_match") or []) + (case.get("must_not_match") or [])
        assert case.get("prompt") and patterns, f"{case['name']} needs a prompt and a pattern"
        assert "pass_indicator" not in case, f"{case['name']} still uses pass_indicator — use must_match/must_not_match"
        for pattern in patterns:
            runner.re.compile(pattern)


# ── Isolated config and login (fixed 2026-10-06: a rules-only CLAUDE_CONFIG_DIR made Claude "Not logged in") ──


def rules_and_home(tmp_path, monkeypatch, creds_in: str | None = "home"):
    """Build a rules folder and a fake home, with credentials in one of them.

    :param creds_in: ``"home"``, ``"rules"`` or None for no credentials anywhere.
    :return: ``(rules folder, credentials path or None)``.
    """
    rules = tmp_path / "rules"
    (rules / "rules").mkdir(parents=True)
    (rules / "CLAUDE.md").write_text("rules")
    home = tmp_path / "home"
    (home / ".claude").mkdir(parents=True)
    monkeypatch.setattr(runner.Path, "home", lambda: home)
    monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
    creds = {"home": home / ".claude" / ".credentials.json", "rules": rules / ".credentials.json"}.get(creds_in)
    if creds:
        creds.write_text("{}")
    return rules, creds


def test_isolated_config_links_rules_and_home_credentials(tmp_path, monkeypatch):
    """The throwaway config links every rules entry plus the default login, so headless Claude is logged in."""
    rules, creds = rules_and_home(tmp_path, monkeypatch)
    isolated = runner.build_isolated_config(rules, tmp_path)
    assert (isolated / "CLAUDE.md").resolve() == (rules / "CLAUDE.md").resolve(), "rules not linked"
    assert (isolated / "rules").resolve() == (rules / "rules").resolve(), "rule folders not linked"
    linked_login = (isolated / ".credentials.json").resolve()
    assert linked_login == creds.resolve(), "login not linked — Claude reports Not logged in"


def test_credentials_are_symlinked_never_copied(tmp_path, monkeypatch):
    """The credentials file in the throwaway folder is a link, so no copy of the secret is ever written."""
    rules, _ = rules_and_home(tmp_path, monkeypatch)
    isolated = runner.build_isolated_config(rules, tmp_path)
    assert (isolated / ".credentials.json").is_symlink(), "credentials were copied instead of linked"
    assert oct(isolated.stat().st_mode & 0o777) == "0o700", "the isolated config must be private to the user"


def test_credentials_in_the_rules_folder_win(tmp_path, monkeypatch):
    """A rules folder that already holds a login, like a live config, uses its own."""
    rules, creds = rules_and_home(tmp_path, monkeypatch, creds_in="rules")
    assert runner.find_credentials(rules) == creds, "the rules folder's own login should be preferred"


def test_no_credentials_links_rules_only(tmp_path, monkeypatch):
    """With no credentials file (for example a keychain login), the rules are still linked and nothing fails."""
    rules, _ = rules_and_home(tmp_path, monkeypatch, creds_in=None)
    isolated = runner.build_isolated_config(rules, tmp_path)
    assert runner.find_credentials(rules) is None, "found credentials that don't exist"
    assert not (isolated / ".credentials.json").exists(), "linked a missing credentials file"
    assert (isolated / "CLAUDE.md").exists(), "rules should still be linked"


def test_missing_config_folder_fails_with_its_own_reason(tmp_path, monkeypatch):
    """A config folder that doesn't exist is reported as such, not as a missing claude CLI."""
    calls = fake_claude(monkeypatch)
    results = runner.EvalRunner(write_evals(tmp_path, CASE), config_dir=tmp_path / "nowhere").run()
    assert "doesn't exist" in results["results"][0]["details"], results["results"][0]["details"]
    assert calls == [], "no Claude call should be made without a config folder"


def test_error_shows_stdout_when_stderr_is_empty(tmp_path, monkeypatch):
    """Claude prints "Not logged in" to stdout, so the failure reason must include it."""
    fake_claude(monkeypatch, stdout="Not logged in · Please run /login", returncode=1, stderr="")
    results = runner.EvalRunner(write_evals(tmp_path, CASE), config_dir=tmp_path).run()
    assert results["results"][0]["details"] == "claude exited 1: Not logged in · Please run /login"


def test_state_folders_are_not_linked(tmp_path, monkeypatch):
    """Claude Code's state folders stay unlinked, so backups and caches land in the throwaway config."""
    rules, _ = rules_and_home(tmp_path, monkeypatch)
    for state in ("backups", "plugins", "projects"):
        (rules / state).mkdir()
    isolated = runner.build_isolated_config(rules, tmp_path)
    linked = sorted(entry.name for entry in isolated.iterdir())
    assert not {"backups", "plugins", "projects"} & set(linked), f"state folders were linked: {linked}"
    assert "rules" in linked and "CLAUDE.md" in linked, f"rules missing: {linked}"
