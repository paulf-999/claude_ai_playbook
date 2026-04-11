"""Structural tests for Claude process files.

Validates that required process files exist and contain expected structural
elements that the session startup logic depends on.
"""

import json
from pathlib import Path

import pytest

PROCESS_DIR = Path(__file__).parent.parent / "src" / "claude" / "process"
SETTINGS_PATH = Path(__file__).parent.parent / "src" / "claude" / "settings.json"

REQUIRED_FILES = [
    "session.md",
    "planning.md",
    "environment.md",
    "session_input.md",
]


@pytest.mark.parametrize("filename", REQUIRED_FILES)
def test_required_process_file_exists(filename: str) -> None:
    """Each required process file must exist in src/claude/process/.

    :param filename: Name of the required process file.
    :type filename: str
    """
    path = PROCESS_DIR / filename
    assert path.exists(), f"Required process file not found: src/claude/process/{filename}"


def test_settings_has_plan_mode_default() -> None:
    """settings.json must set defaultMode to plan — replaces explicit EnterPlanMode calls."""
    settings = json.loads(SETTINGS_PATH.read_text())
    assert settings.get("permissions", {}).get("defaultMode") == "plan", (
        "settings.json must set permissions.defaultMode to 'plan'"
    )


def test_session_input_has_sub_agent_section() -> None:
    """session_input.md must contain a ## Sub-agent section for pre-populating agent selection."""
    content = (PROCESS_DIR / "session_input.md").read_text()
    assert "## Sub-agent" in content, (
        "session_input.md must contain a '## Sub-agent' section"
    )


def test_session_input_has_task_section() -> None:
    """session_input.md must contain a ## Task section for pre-populating session tasks."""
    content = (PROCESS_DIR / "session_input.md").read_text()
    assert "## Task" in content, (
        "session_input.md must contain a '## Task' section"
    )
