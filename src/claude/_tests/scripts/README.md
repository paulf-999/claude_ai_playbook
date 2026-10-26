# 🧪 `scripts/` tests

**Purpose:** Tests for the maintenance scripts in `scripts/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_audit_claude_component_root.py` | Validates how audit_claude_component.py chooses the folder it scans | 10/10 | 2026-10-01 | 2026-10-11 | 1.0.4 |
| `test_audit_claude_component_health.py` | Validates the health signals audit_claude_component.py raises for tagged components | 9/10 | 2026-10-22 | 2026-10-22 | 1.0.0 |
| `test_audit_agent_evals.py` | `audit_agent_evals.py` runs only evals with a prompt and patterns, calls `claude -p --agent <name>` through claude_kaizen's runner, reports pass rates, and makes no calls on `--dry-run` | 10/10 | 2026-10-22 | 2026-10-25 | 2.0.0 |
| `test_audit_plans.py` | `audit_plans.py` lists saved plans by status from `_plans/` and its status folders, flags stale Active plans, and counts plans and drafts to file | 9/10 | 2026-10-11 | 2026-10-11 | 2.0.1 |
| `test_audit_rule_usage.py` | Validates audit_rule_usage.py against small fixture rules and transcripts | 10/10 | 2026-10-01 | 2026-10-22 | 1.11.0 |
| `test_clean_plans.py` | `clean_plans.py` files saved plans into `_plans/<status>/` by their status line (or phase table), files drafts into `plans/draft/` or `plans/archive/` by age, never overwrites, and runs without asking during `make install` | 9/10 | 2026-10-02 | 2026-10-22 | 2.2.0 |
| `test_script_naming.py` | Validates that every script under scripts/ follows the script naming pattern | 10/10 | 2026-10-02 | 2026-10-11 | 1.1.3 |

[← All tests](../README.md)
