#!/usr/bin/env python3
"""
claude_kaizen eval runner — before/after scorer.

Sends each eval case's prompt to headless Claude Code (``claude -p``, no tools,
empty working folder) with ``CLAUDE_CONFIG_DIR`` pointing at the rules under test, then checks the reply
against the case's ``must_match`` and ``must_not_match`` regex lists. Running it
once before and once after a proposed rule change shows whether the change helps.

Each case costs one Claude call, so run it deliberately rather than on every commit.

Usage:
  python runner.py evals/claude_ai_playbook.yaml
  python runner.py --before evals/claude_ai_playbook.yaml
  python runner.py --after --config-dir /path/to/patched/claude evals/claude_ai_playbook.yaml
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

DEFAULT_TIMEOUT_SECONDS = 300


def find_config_dir(start: Path) -> Path | None:
    """Return the config folder the rules live in.

    :param start: Where to begin looking, normally this script's own folder.
    :type start: Path
    :return: ``CLAUDE_CONFIG_DIR`` if set, else the nearest parent holding ``_rules/``, else None.
    :rtype: Path | None
    """
    if os.environ.get("CLAUDE_CONFIG_DIR"):
        return Path(os.environ["CLAUDE_CONFIG_DIR"])
    return next((p for p in [start, *start.parents] if (p / "_rules").is_dir()), None)


def judge(output: str, must_match: list[str], must_not_match: list[str]) -> tuple[str, str]:
    """Check Claude's reply against a case's patterns.

    :param output: Claude's reply.
    :type output: str
    :param must_match: Regexes that must all appear.
    :type must_match: list[str]
    :param must_not_match: Regexes that must not appear.
    :type must_not_match: list[str]
    :return: ``("PASS" | "FAIL", details)``.
    :rtype: tuple[str, str]
    """
    missing = [p for p in must_match if not re.search(p, output)]
    forbidden = [p for p in must_not_match if re.search(p, output)]
    if not missing and not forbidden:
        return "PASS", "all patterns as expected"
    problems = [f"missing {p!r}" for p in missing] + [f"found forbidden {p!r}" for p in forbidden]
    return "FAIL", "; ".join(problems)


class EvalRunner:
    """Runs eval cases against Claude and reports results."""

    def __init__(self, eval_file: Path, config_dir: Path | None = None, timeout: int = DEFAULT_TIMEOUT_SECONDS):
        """Load the eval cases and remember which rules to test against.

        :param eval_file: YAML file with a top-level ``evals`` list.
        :type eval_file: Path
        :param config_dir: Config folder whose rules Claude loads, or None to find one.
        :type config_dir: Path | None
        :param timeout: Seconds to allow each Claude call.
        :type timeout: int
        """
        self.eval_file = eval_file
        self.config_dir = config_dir or find_config_dir(Path(__file__).resolve().parent)
        self.timeout = timeout
        self.evals = self._load_evals()

    def _load_evals(self) -> list[dict[str, Any]]:
        """Load eval cases from the YAML file.

        :return: The cases, or an empty list if the file has none.
        :rtype: list[dict[str, Any]]
        """
        data = yaml.safe_load(self.eval_file.read_text(encoding="utf-8")) or {}
        return data.get("evals", [])

    def ask_claude(self, prompt: str) -> str:
        """Send one prompt to headless Claude Code and return its reply.

        :param prompt: The eval case's prompt.
        :type prompt: str
        :return: Claude's reply text.
        :rtype: str
        :raises RuntimeError: If the CLI is missing, times out or exits non-zero.
        """
        env = dict(os.environ)
        if self.config_dir:
            env["CLAUDE_CONFIG_DIR"] = str(self.config_dir)
        # No tools and an empty working folder: Claude answers from the rules alone and can't touch any files.
        # The prompt goes on stdin because --tools takes every following argument as a tool name.
        try:
            with tempfile.TemporaryDirectory() as workdir:
                done = subprocess.run(
                    ["claude", "-p", "--tools", ""], input=prompt,
                    capture_output=True, text=True, env=env, cwd=workdir, timeout=self.timeout, check=False,
                )
        except FileNotFoundError as exc:
            raise RuntimeError("the claude CLI isn't installed or on PATH") from exc
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"claude didn't answer within {self.timeout}s") from exc
        if done.returncode != 0:
            raise RuntimeError(f"claude exited {done.returncode}: {done.stderr.strip()[:200]}")
        return done.stdout

    def run(self, context: str = "current") -> dict[str, Any]:
        """Run every eval case.

        :param context: ``before``, ``after`` or ``current``, used only for reporting.
        :type context: str
        :return: Totals and a per-case ``results`` list of ``{name, status, details}``.
        :rtype: dict[str, Any]
        """
        results = [self._run_case(case) for case in self.evals]
        passed = sum(r["status"] == "PASS" for r in results)
        return {
            "context": context,
            "total": len(results),
            "passed": passed,
            "failed": len(results) - passed,
            "results": results,
        }

    def _run_case(self, eval_case: dict[str, Any]) -> dict[str, Any]:
        """Run a single eval case.

        :param eval_case: One entry from the ``evals`` list.
        :type eval_case: dict[str, Any]
        :return: ``{"name": str, "status": "PASS" | "FAIL", "details": str}``.
        :rtype: dict[str, Any]
        """
        name = eval_case.get("name")
        must_match = eval_case.get("must_match") or []
        must_not_match = eval_case.get("must_not_match") or []
        if not eval_case.get("prompt"):
            return {"name": name, "status": "FAIL", "details": "case has no prompt"}
        if not must_match and not must_not_match:
            return {"name": name, "status": "FAIL", "details": "case has no must_match or must_not_match patterns"}
        try:
            output = self.ask_claude(eval_case["prompt"])
        except RuntimeError as exc:
            return {"name": name, "status": "FAIL", "details": str(exc)}
        status, details = judge(output, must_match, must_not_match)
        return {"name": name, "status": status, "details": details}

    def print_results(self, results: dict[str, Any]) -> None:
        """Print results in a human-readable format.

        :param results: The dict returned by :meth:`run`.
        :type results: dict[str, Any]
        """
        print(f"\n{'=' * 60}")
        print(f"Eval Results — {results['context'].upper()}")
        print(f"{'=' * 60}")
        print(f"Total: {results['total']} | Passed: {results['passed']} | Failed: {results['failed']}")
        print()
        for result in results["results"]:
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_icon} {result['name']}")
            print(f"   {result['details']}")
            print()
        print(f"{'=' * 60}\n")


def parse_args(args: list[str]) -> tuple[str, Path | None, Path | None]:
    """Read the command-line arguments.

    :param args: Arguments after the script name.
    :type args: list[str]
    :return: ``(context, config_dir, eval_file)``.
    :rtype: tuple[str, Path | None, Path | None]
    """
    context, config_dir, eval_file = "current", None, None
    remaining = iter(args)
    for arg in remaining:
        if arg in ("--before", "--after"):
            context = arg[2:]
        elif arg == "--config-dir":
            config_dir = Path(next(remaining, ""))
        else:
            eval_file = Path(arg)
    return context, config_dir, eval_file


if __name__ == "__main__":
    context, config_dir, eval_file_path = parse_args(sys.argv[1:])
    if not eval_file_path or not eval_file_path.exists():
        print(f"Eval file not found: {eval_file_path}")
        print("Usage: python runner.py [--before|--after] [--config-dir DIR] <eval_file>")
        sys.exit(1)

    runner = EvalRunner(eval_file_path, config_dir=config_dir)
    results = runner.run(context=context)
    runner.print_results(results)

    # Exit with failure code if any evals failed
    sys.exit(0 if results["failed"] == 0 else 1)
