"""Tests for all domain-specific style guide enforcement hooks.

Each hook injects a style guide reminder when Claude edits a file matching
its domain — by extension (e.g. .sql, .tf) or by path pattern (e.g. */dags/*).
All hooks share the same behaviour contract:
  - fires on Edit or Write to a matching path
  - passes through silently for non-matching paths
  - passes through silently for non-Edit/Write tools
"""
import json
from dataclasses import dataclass
from pathlib import Path

import pytest

from hook_test_utils import run_hook

HOOKS_DIR = Path.home() / ".claude/hooks/style_guides"


@dataclass
class StyleGuideCase:
    hook: str
    trigger_paths: list[str]
    nontrigger_paths: list[str]
    content_check: str


CASES = [
    StyleGuideCase(
        hook="hook_style_guide_sql.sh",
        trigger_paths=["/tmp/example.sql"],
        nontrigger_paths=["/tmp/example.md"],
        content_check="sql style",
    ),
    StyleGuideCase(
        hook="hook_style_guide_python.sh",
        trigger_paths=["/home/paul/.claude/_tests/rules/test_rules_structure.py"],
        nontrigger_paths=["/home/paul/.claude/_rules/behaviour.md"],
        content_check="python style",
    ),
    StyleGuideCase(
        hook="hook_style_guide_bash.sh",
        trigger_paths=["/home/paul/.claude/hooks/style_guides/hook_style_guide_bash.sh"],
        nontrigger_paths=["/home/paul/.claude/_rules/behaviour.md"],
        content_check="bash style",
    ),
    StyleGuideCase(
        hook="hook_style_guide_terraform.sh",
        trigger_paths=["/tmp/main.tf"],
        nontrigger_paths=["/home/paul/.claude/_rules/behaviour.md"],
        content_check="terraform style",
    ),
    StyleGuideCase(
        hook="hook_style_guide_dbt.sh",
        trigger_paths=[
            "/repo/da-etl-dbtanalytics/models/staging/stg_orders.sql",
            "/repo/dbt/models/schema.yml",
        ],
        nontrigger_paths=[
            "/tmp/ad_hoc_query.sql",
            "/repo/ci/pipeline.yml",
        ],
        content_check="dbt style",
    ),
    StyleGuideCase(
        hook="hook_style_guide_airflow.sh",
        trigger_paths=["/repo/dags/my_dag.py"],
        nontrigger_paths=["/repo/src/utils.py"],
        content_check="airflow style",
    ),
    StyleGuideCase(
        hook="hook_style_guide_ansible.sh",
        trigger_paths=[
            "/repo/pyrc-cac-ans/roles/docker/tasks/main.yml",
            "/repo/playbooks/deploy.yml",
        ],
        nontrigger_paths=["/repo/dbt/models/schema.yml"],
        content_check="ansible style",
    ),
    StyleGuideCase(
        hook="hook_style_guide_jira.sh",
        trigger_paths=[str(Path.home() / "_drafts/jira/2026-08-06_example_ticket.md")],
        nontrigger_paths=[str(Path.home() / "_drafts/confluence/2026-08-06_example_page.md")],
        content_check="jira style",
    ),
]

_IDS = [c.hook.removesuffix(".sh").removeprefix("hook_style_guide_") for c in CASES]


@pytest.mark.parametrize("case", CASES, ids=_IDS)
def test_injects_for_edit(case: StyleGuideCase):
    """Edit to a matching path — hook must inject a style reminder."""
    hook = HOOKS_DIR / case.hook
    for path in case.trigger_paths:
        result = run_hook(hook, {"tool_name": "Edit", "tool_input": {"file_path": path}})
        output = json.loads(result.stdout)
        assert "additionalContext" in output["hookSpecificOutput"], (
            f"{case.hook}: no additionalContext for path {path}"
        )
        assert case.content_check in output["hookSpecificOutput"]["additionalContext"].lower(), (
            f"{case.hook}: '{case.content_check}' missing from output for path {path}"
        )


@pytest.mark.parametrize("case", CASES, ids=_IDS)
def test_injects_for_write(case: StyleGuideCase):
    """Write to a matching path — hook must fire for Write as well as Edit."""
    hook = HOOKS_DIR / case.hook
    result = run_hook(hook, {"tool_name": "Write", "tool_input": {"file_path": case.trigger_paths[0]}})
    output = json.loads(result.stdout)
    assert "additionalContext" in output["hookSpecificOutput"], (
        f"{case.hook}: no additionalContext for Write on {case.trigger_paths[0]}"
    )


@pytest.mark.parametrize("case", CASES, ids=_IDS)
def test_ignores_nontrigger_paths(case: StyleGuideCase):
    """Edit to a non-matching path — hook must pass through silently."""
    hook = HOOKS_DIR / case.hook
    for path in case.nontrigger_paths:
        result = run_hook(hook, {"tool_name": "Edit", "tool_input": {"file_path": path}})
        assert result.stdout.strip() == "", (
            f"{case.hook}: unexpected output for non-trigger path {path}"
        )
        assert result.returncode == 0


@pytest.mark.parametrize("case", CASES, ids=_IDS)
def test_ignores_wrong_tool(case: StyleGuideCase):
    """Non-Edit/Write tool — hook must pass through silently regardless of path."""
    hook = HOOKS_DIR / case.hook
    result = run_hook(hook, {"tool_name": "Bash", "tool_input": {"command": "ls"}})
    assert result.stdout.strip() == ""
    assert result.returncode == 0
