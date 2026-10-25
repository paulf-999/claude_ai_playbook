#!/usr/bin/env python3
"""Run each agent's runnable evals through headless Claude and report a pass rate per agent.

An eval is runnable when it has a ``run`` block holding a ``prompt`` and at least one ``must_match``
or ``must_not_match`` regex. Each one runs ``claude -p`` with no tools, through claude_kaizen's eval
runner, and costs one Claude call. Evals without a ``run`` block, such as routing checks that need a
full session to pick the agent, are skipped and counted.

The agent's instructions come from its ``AGENT.md`` in the config this script sits in (or
``--config-dir``), passed with ``--agents``, so the version under test is the one on disk. Claude
itself runs with the caller's own ``$CLAUDE_CONFIG_DIR`` and login, not an isolated copy, because an
isolated copy can't reach a login kept in the macOS Keychain. That config's ``CLAUDE.md`` and rules
load alongside the agent, as in real use, so results can shift when that config changes.

Usage:
    python3 src/claude/scripts/_audit_scripts/audit_agent_evals.py --dry-run
    python3 src/claude/scripts/_audit_scripts/audit_agent_evals.py code_reviewer
    python3 src/claude/scripts/_audit_scripts/audit_agent_evals.py --config-dir <folder> code_reviewer

Exits 1 when any eval fails or a named agent has no evals, and 0 otherwise.
"""

from __future__ import annotations

import sys

if sys.version_info < (3, 10):  # pragma: no cover
    sys.exit("This script needs Python 3.10 or newer — you're running " + sys.version.split()[0] + ".")

import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml

# Grouped in the playbook repo (skills/_claude_skills/<name>/), flat in a live config (skills/<name>/)
KAIZEN_RUNNER = ("claude_kaizen/evals/runner.py", "_claude_skills/claude_kaizen/evals/runner.py")
SCRIPT_CONFIG = Path(__file__).resolve().parents[2]


def load_kaizen_runner(config: Path):
    """Import claude_kaizen's eval runner, which owns the ``claude -p`` call and the regex judge.

    :raises FileNotFoundError: If the config holds no claude_kaizen runner.
    """
    path = next((config / "skills" / rel for rel in KAIZEN_RUNNER if (config / "skills" / rel).is_file()), None)
    if path is None:
        raise FileNotFoundError(f"claude_kaizen's evals/runner.py not found under {config / 'skills'}")
    spec = importlib.util.spec_from_file_location("kaizen_runner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def agent_eval_files(config: Path) -> dict[str, Path]:
    """Map each agent with an ``evals.yaml`` beside its ``AGENT.md`` to that file, sorted by name."""
    found = {p.parent.name: p.parent / "evals.yaml" for p in (config / "agents").rglob("AGENT.md")}
    return {name: path for name, path in sorted(found.items()) if path.is_file()}


def agent_definition(agent_file: Path) -> dict[str, str]:
    """Return the ``--agents`` entry for an agent: its frontmatter description and its body as the prompt."""
    _, frontmatter, body = agent_file.read_text().split("---\n", 2)
    return {"description": yaml.safe_load(frontmatter)["description"], "prompt": body.strip()}


def runnable_cases(eval_file: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Split an agent's evals into runner cases and the names of the ones skipped.

    :return: Cases in the kaizen runner's shape (name, prompt, must_match, must_not_match), and skipped names.
    """
    cases, skipped = [], []
    for case in (yaml.safe_load(eval_file.read_text()) or {}).get("evals", []):
        run = case.get("run") or {}
        if run.get("prompt") and (run.get("must_match") or run.get("must_not_match")):
            cases.append({"name": case["name"], "prompt": run["prompt"], "must_match": run.get("must_match", []),
                          "must_not_match": run.get("must_not_match", [])})
        else:
            skipped.append(case["name"])
    return cases, skipped


def run_agent(kaizen, name: str, eval_file: Path) -> dict[str, Any]:
    """Run one agent's runnable evals and return the kaizen runner's results plus the skipped names."""
    cases, skipped = runnable_cases(eval_file)
    agents = json.dumps({name: agent_definition(eval_file.parent / "AGENT.md")})
    runner = kaizen.EvalRunner(eval_file, cli_args=["--agents", agents, "--agent", name], isolate=False)
    runner.evals = cases
    results = runner.run(context=name)
    results["skipped"] = skipped
    runner.print_results(results)
    return results


def summary_line(name: str, results: dict[str, Any]) -> str:
    """Return one agent's pass rate, for example ``code_reviewer: 5/6 passed (83%), 2 skipped``."""
    total, passed = results["total"], results["passed"]
    rate = f"{round(100 * passed / total)}%" if total else "n/a"
    return f"{name}: {passed}/{total} passed ({rate}), {len(results['skipped'])} skipped"


def parse_args(args: list[str]) -> tuple[Path, bool, list[str]]:
    """Read ``--config-dir <folder>``, ``--dry-run`` and agent names from the command line."""
    config, dry_run, names = SCRIPT_CONFIG, False, []
    remaining = iter(args)
    for arg in remaining:
        if arg == "--config-dir":
            config = Path(next(remaining, ""))
        elif arg == "--dry-run":
            dry_run = True
        else:
            names.append(arg)
    return config, dry_run, names


def main(argv: list[str] | None = None) -> int:
    """Run the evals for the named agents, or every agent, and return the exit code."""
    config, dry_run, names = parse_args(list(sys.argv[1:] if argv is None else argv))
    files = agent_eval_files(config)
    missing = [n for n in names if n not in files]
    if missing:
        print(f"No evals.yaml found for: {', '.join(missing)}")
        return 1
    chosen = {n: files[n] for n in names} if names else files
    if dry_run:
        for name, path in chosen.items():
            cases, skipped = runnable_cases(path)
            print(f"{name}: {len(cases)} runnable ({', '.join(c['name'] for c in cases) or 'none'}), "
                  f"{len(skipped)} skipped — no Claude calls made")
        return 0
    kaizen = load_kaizen_runner(config)
    results = {name: run_agent(kaizen, name, path) for name, path in chosen.items()}
    for name, result in results.items():
        print(summary_line(name, result))
    return 1 if any(r["failed"] for r in results.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
