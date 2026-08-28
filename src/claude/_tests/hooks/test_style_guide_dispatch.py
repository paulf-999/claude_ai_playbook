"""Tests for hook_style_guide_dispatch.sh.

Verifies the dispatcher correctly routes to individual style_guide hooks and
aggregates injected context. Individual hook trigger/nontrigger contract is
tested exhaustively in test_style_guides.py — this file tests dispatcher
behaviour only.
"""
import json
from pathlib import Path

from hook_test_utils import run_hook

HOOK = Path.home() / ".claude/hooks/hook_style_guide_dispatch.sh"


def test_dispatches_sql_for_sql_file():
    """SQL file — dispatcher must inject SQL style context."""
    result = run_hook(HOOK, {"tool_name": "Edit", "tool_input": {"file_path": "/tmp/query.sql"}})
    output = json.loads(result.stdout)
    assert "additionalContext" in output["hookSpecificOutput"]
    assert "sql style" in output["hookSpecificOutput"]["additionalContext"].lower()


def test_dispatches_python_for_python_file():
    """Python file — dispatcher must inject Python style context."""
    result = run_hook(HOOK, {"tool_name": "Edit", "tool_input": {"file_path": "/tmp/script.py"}})
    output = json.loads(result.stdout)
    assert "additionalContext" in output["hookSpecificOutput"]
    assert "python style" in output["hookSpecificOutput"]["additionalContext"].lower()


def test_no_output_for_unmatched_file():
    """Markdown file matching no style guide — dispatcher must produce no output."""
    result = run_hook(HOOK, {"tool_name": "Edit", "tool_input": {"file_path": "/tmp/notes.md"}})
    assert result.stdout.strip() == ""
    assert result.returncode == 0


def test_aggregates_multiple_matching_guides():
    """dbt SQL file — both dbt and sql hooks match; output must contain both."""
    path = "/repo/da-etl-dbtanalytics/models/staging/stg_orders.sql"
    result = run_hook(HOOK, {"tool_name": "Edit", "tool_input": {"file_path": path}})
    output = json.loads(result.stdout)
    context = output["hookSpecificOutput"]["additionalContext"].lower()
    assert "dbt style" in context
    assert "sql style" in context
