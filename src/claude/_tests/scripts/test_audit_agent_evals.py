# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-22
# Date updated:      2026-10-25
# Version:           2.0.0
# Test quality score: 10/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""audit_agent_evals.py runs each agent's runnable evals through claude_kaizen's runner and reports pass rates.

Issue #387 found that no agent eval ever ran, so Test Coverage could never honestly score above 7. The
agent's prompt comes from the AGENT.md on disk, while Claude runs with the caller's own config and login,
because an isolated config copy can't reach a login kept in the macOS Keychain. These tests use fake
agents in a temporary config and a fake ``subprocess.run``, so none of them calls Claude.
"""
import importlib.util
import json
import re
import subprocess
import textwrap

import pytest

from _shared_paths import CLAUDE_DIR

SCRIPT = CLAUDE_DIR / "scripts" / "_audit_scripts" / "audit_agent_evals.py"
_spec = importlib.util.spec_from_file_location("audit_agent_evals", SCRIPT)
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)

EVALS = textwrap.dedent("""\
    evals:
      - name: routing_case
        input:
          prompt: pick the agent
      - name: approves_clean_diff
        run:
          prompt: Review this diff
          must_match: ["(?i)approve"]
          must_not_match: ["(?i)request changes"]
      - name: prompt_without_patterns
        run:
          prompt: Review this
    """)
CALLER_CONFIG = "/caller/own/config"


def make_config(tmp_path, agents=("code_reviewer",), with_evals=True, with_kaizen=True):
    """Build a fake config folder holding agents, their evals and, optionally, the real kaizen runner."""
    for name in agents:
        folder = tmp_path / "agents" / "core" / name
        folder.mkdir(parents=True)
        (folder / "AGENT.md").write_text(f"---\nname: {name}\ndescription: Reviews things\n---\n# {name}\n\nBe fair.\n")
        if with_evals:
            (folder / "evals.yaml").write_text(EVALS)
    if with_kaizen:
        candidates = (CLAUDE_DIR / "skills" / rel for rel in audit.KAIZEN_RUNNER)
        real = next(path for path in candidates if path.is_file())
        target = tmp_path / "skills" / "claude_kaizen" / "evals" / "runner.py"
        target.parent.mkdir(parents=True)
        target.write_text(real.read_text())
    return tmp_path


def fake_claude(monkeypatch, stdout):
    """Make every ``claude`` call return this reply, and record each command and its CLAUDE_CONFIG_DIR."""
    calls = []
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", CALLER_CONFIG)

    def run(command, **kwargs):
        calls.append((command, kwargs["env"].get("CLAUDE_CONFIG_DIR")))
        return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")

    monkeypatch.setattr(subprocess, "run", run)
    return calls


# --- Finding things ---


def test_parse_args_reads_config_dir_dry_run_and_names(tmp_path):
    """--config-dir and --dry-run are read in any order, the rest are agent names, defaulting to the script's config."""
    assert audit.parse_args([]) == (audit.SCRIPT_CONFIG, False, []), "defaults should be the script's config, live run"
    parsed = audit.parse_args(["a", "--dry-run", "--config-dir", str(tmp_path), "b"])
    assert parsed == (tmp_path, True, ["a", "b"]), parsed
    expected = SCRIPT.resolve().parents[2]
    assert audit.SCRIPT_CONFIG == expected, "the default config should be the folder holding scripts/"


def test_agents_without_evals_are_left_out(tmp_path):
    """Only agents with an evals.yaml beside their AGENT.md are listed, by name."""
    make_config(tmp_path, agents=("b_agent", "a_agent"), with_kaizen=False)
    (tmp_path / "agents" / "core" / "b_agent" / "evals.yaml").unlink()
    assert list(audit.agent_eval_files(tmp_path)) == ["a_agent"], "only agents with evals.yaml should be listed"


def test_missing_kaizen_runner_is_reported(tmp_path):
    """Without claude_kaizen's runner the script names where it looked, instead of failing obscurely."""
    with pytest.raises(FileNotFoundError, match="claude_kaizen"):
        audit.load_kaizen_runner(tmp_path)


def test_agent_definition_uses_description_and_body(tmp_path):
    """The --agents entry is the frontmatter description plus the body below the frontmatter."""
    make_config(tmp_path, with_kaizen=False)
    definition = audit.agent_definition(tmp_path / "agents" / "core" / "code_reviewer" / "AGENT.md")
    assert definition == {"description": "Reviews things", "prompt": "# code_reviewer\n\nBe fair."}, definition


# --- Choosing cases ---


def test_only_cases_with_a_prompt_and_patterns_run(tmp_path):
    """A case runs only with a run block holding a prompt and a pattern, and the rest are skipped by name."""
    make_config(tmp_path, with_kaizen=False)
    cases, skipped = audit.runnable_cases(tmp_path / "agents" / "core" / "code_reviewer" / "evals.yaml")
    assert [c["name"] for c in cases] == ["approves_clean_diff"], cases
    assert cases[0] == {"name": "approves_clean_diff", "prompt": "Review this diff", "must_match": ["(?i)approve"],
                        "must_not_match": ["(?i)request changes"]}, "case not converted to the kaizen shape"
    assert skipped == ["routing_case", "prompt_without_patterns"], skipped


def test_empty_eval_file_has_nothing_to_run(tmp_path):
    """An empty evals.yaml gives no cases and no skips, rather than an error."""
    path = tmp_path / "evals.yaml"
    path.write_text("")
    assert audit.runnable_cases(path) == ([], []), "an empty file should give nothing to run"


def test_summary_line_shows_the_pass_rate():
    """The summary gives passed over runnable, the rate, and the skip count, or n/a with nothing to run."""
    assert audit.summary_line("x", {"total": 6, "passed": 5, "skipped": ["a", "b"]}) == "x: 5/6 passed (83%), 2 skipped"
    assert audit.summary_line("x", {"total": 0, "passed": 0, "skipped": ["a"]}) == "x: 0/0 passed (n/a), 1 skipped"


# --- Running ---


def test_dry_run_makes_no_claude_calls(tmp_path, monkeypatch, capsys):
    """--dry-run lists what would run and exits 0 without calling Claude."""
    calls = fake_claude(monkeypatch, "Approve")
    assert audit.main(["--config-dir", str(make_config(tmp_path)), "--dry-run"]) == 0, "a dry run should exit 0"
    assert calls == [], "a dry run must not call Claude"
    out = capsys.readouterr().out
    assert "code_reviewer: 1 runnable (approves_clean_diff), 2 skipped" in out, out


def test_dry_run_with_nothing_runnable_says_none(tmp_path, capsys):
    """An agent whose evals are all prose shows 'none' in the dry run."""
    make_config(tmp_path, with_kaizen=False)
    (tmp_path / "agents" / "core" / "code_reviewer" / "evals.yaml").write_text("evals:\n  - name: prose\n")
    assert audit.main(["--config-dir", str(tmp_path), "--dry-run"]) == 0, "a dry run should exit 0"
    out = capsys.readouterr().out
    assert "0 runnable (none), 1 skipped" in out, out


def test_passing_agent_runs_with_its_definition_and_the_callers_login(tmp_path, monkeypatch, capsys):
    """Each case passes the AGENT.md as --agents before --tools, and keeps the caller's own CLAUDE_CONFIG_DIR."""
    calls = fake_claude(monkeypatch, "Verdict: Approve")
    config = make_config(tmp_path)
    assert audit.main(["--config-dir", str(config), "code_reviewer"]) == 0, "a passing agent should exit 0"
    (command, claude_config), = calls
    expected = json.dumps({"code_reviewer": {"description": "Reviews things", "prompt": "# code_reviewer\n\nBe fair."}})
    assert command == ["claude", "-p", "--agents", expected, "--agent", "code_reviewer", "--tools", ""], command
    assert claude_config == CALLER_CONFIG, f"Claude should run with the caller's own config: {claude_config}"
    out = capsys.readouterr().out
    assert "code_reviewer: 1/1 passed (100%), 2 skipped" in out, out


def test_failing_eval_exits_one(tmp_path, monkeypatch, capsys):
    """A reply that breaks a pattern fails the case, and the script exits 1."""
    fake_claude(monkeypatch, "Request changes")
    monkeypatch.setattr(audit.sys, "argv", ["audit_agent_evals.py", "--config-dir", str(make_config(tmp_path))])
    assert audit.main() == 1, "a failing eval should exit 1"
    out = capsys.readouterr().out
    assert "code_reviewer: 0/1 passed (0%), 2 skipped" in out, out


def test_unknown_agent_exits_one(tmp_path, monkeypatch, capsys):
    """Naming an agent with no evals exits 1 and says which one, before any Claude call."""
    calls = fake_claude(monkeypatch, "Approve")
    config = make_config(tmp_path)
    assert audit.main(["--config-dir", str(config), "no_such_agent"]) == 1, "an unknown agent should exit 1"
    assert calls == [], "no Claude call should run for an unknown agent"
    out = capsys.readouterr().out
    assert "No evals.yaml found for: no_such_agent" in out, out


def test_real_agent_evals_are_well_formed():
    """code_reviewer's run blocks compile and its AGENT.md yields a definition, so a live run can't break on setup."""
    files = audit.agent_eval_files(CLAUDE_DIR)
    assert "code_reviewer" in files, "code_reviewer's evals should be found"
    cases, _ = audit.runnable_cases(files["code_reviewer"])
    assert len(cases) >= 6, f"expected code_reviewer's 6 runnable evals, found {len(cases)}"
    for case in cases:
        for pattern in case["must_match"] + case["must_not_match"]:
            re.compile(pattern)
    definition = audit.agent_definition(files["code_reviewer"].parent / "AGENT.md")
    assert definition["description"], "AGENT.md should yield a description"
    assert "\n# " in definition["prompt"], "AGENT.md should yield a prompt that includes its H1"
