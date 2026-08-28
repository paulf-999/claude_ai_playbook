"""Shared utilities for enforcement hook tests."""
import json
import subprocess
from pathlib import Path
from typing import Any


def run_hook(hook: Path, payload: dict[str, Any]) -> subprocess.CompletedProcess[str]:
    """Run the given hook script with a JSON payload on stdin.

    :param hook: Path to the bash hook script to execute.
    :type hook: Path
    :param payload: The Claude Code hook payload to pass on stdin.
    :type payload: dict
    :return: The completed process result including stdout and returncode.
    :rtype: subprocess.CompletedProcess
    """
    return subprocess.run(
        ["bash", str(hook)],
        # simulates Claude's hook runtime JSON input on stdin
        input=json.dumps(payload),
        capture_output=True,
        text=True,
    )
