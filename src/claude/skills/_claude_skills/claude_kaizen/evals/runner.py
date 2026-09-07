#!/usr/bin/env python3
"""
claude_kaizen eval runner — pytest-based before/after scorer.

Runs eval cases against the current _rules/ state and reports pass/fail,
enabling before/after comparisons when a proposed patch is added.

Usage:
  python runner.py evals/dmt-scripts-claude_ai_playbook.yaml
  python runner.py --before evals/dmt-scripts-claude_ai_playbook.yaml
  python runner.py --after evals/dmt-scripts-claude_ai_playbook.yaml
"""

import sys
import yaml
import re
from pathlib import Path
from typing import Dict, List, Any


class EvalRunner:
    """Runs eval cases and reports results."""

    def __init__(self, eval_file: Path):
        self.eval_file = eval_file
        self.evals = self._load_evals()

    def _load_evals(self) -> List[Dict[str, Any]]:
        """Load eval cases from YAML file."""
        with open(self.eval_file, 'r') as f:
            data = yaml.safe_load(f)
        return data.get('evals', [])

    def run(self, context: str = "current") -> Dict[str, Any]:
        """
        Run all eval cases.

        Args:
            context: "before" | "after" | "current" (for reporting)

        Returns:
            {
              "context": "before|after|current",
              "total": int,
              "passed": int,
              "failed": int,
              "results": [{"name": str, "status": "PASS|FAIL", "details": str}, ...]
            }
        """
        results = {
            "context": context,
            "total": len(self.evals),
            "passed": 0,
            "failed": 0,
            "results": []
        }

        for eval_case in self.evals:
            result = self._run_case(eval_case)
            results["results"].append(result)
            if result["status"] == "PASS":
                results["passed"] += 1
            else:
                results["failed"] += 1

        return results

    def _run_case(self, eval_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single eval case.

        Returns: {"name": str, "status": "PASS|FAIL", "details": str}
        """
        name = eval_case.get('name')
        description = eval_case.get('description', '')
        pass_indicator = eval_case.get('pass_indicator', '')

        # Placeholder: in real implementation, this would:
        # 1. Extract the prompt
        # 2. Run Claude against current _rules/ state
        # 3. Check output against pass_indicator (regex or substring match)
        # 4. Return PASS/FAIL with details

        # For now: dummy implementation that always passes
        # (will be replaced with real eval harness)
        status = "PASS"
        details = f"Placeholder eval: {description}"

        return {
            "name": name,
            "status": status,
            "details": details
        }

    def print_results(self, results: Dict[str, Any]) -> None:
        """Print results in human-readable format."""
        context = results["context"]
        total = results["total"]
        passed = results["passed"]
        failed = results["failed"]

        print(f"\n{'='*60}")
        print(f"Eval Results — {context.upper()}")
        print(f"{'='*60}")
        print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
        print()

        for result in results["results"]:
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_icon} {result['name']}")
            print(f"   {result['details']}")
            print()

        print(f"{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python runner.py [--before|--after] <eval_file>")
        sys.exit(1)

    # Parse args
    args = sys.argv[1:]
    context = "current"
    eval_file_path = None

    for arg in args:
        if arg == "--before":
            context = "before"
        elif arg == "--after":
            context = "after"
        else:
            eval_file_path = Path(arg)

    if not eval_file_path or not eval_file_path.exists():
        print(f"Error: eval file not found: {eval_file_path}")
        sys.exit(1)

    # Run
    runner = EvalRunner(eval_file_path)
    results = runner.run(context=context)
    runner.print_results(results)

    # Exit with failure code if any evals failed
    sys.exit(0 if results["failed"] == 0 else 1)
