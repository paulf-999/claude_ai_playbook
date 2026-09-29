# 🧪 Tests

`evals.yaml` holds this skill's test scenarios: recorded situations (a user request, the setup, the expected result) that check `claude_kaizen` still behaves correctly as it changes over time. They aren't code. Think of them as worked examples an author checks the skill against.

## 📋 Scenarios

| # | Scenario | Phase | What it checks |
|---|---|---|---|
| 1 | `happy_path_promotes_recurring_pattern` | Promote | A mistake seen twice becomes a rule and eval, shown as a diff for review |
| 2 | `one_off_mistake_not_promoted` | Promote | A mistake seen once stays a candidate |
| 3 | `declined_diff_writes_nothing` | Promote | Rejecting the proposal leaves `_rules/learned/` unchanged |
| 4 | `regression_blocks_promotion` | Validate | A rule that breaks a previously passing eval isn't presented as ready |
| 5 | `stale_rule_flagged_not_removed` | Prune | A rule older than 6 months is flagged, not deleted |
| 6 | `missing_errors_dir` | Setup | No `~/_errors/` means no audit, and no invented patterns |
| 7 | `cross_repo_request_out_of_scope` | Scope | Cross-repo promotion is declined as a planned v2 feature |

- **Maturity:** 7 scenarios sits within the 5–8 expected for a **draft** skill
- **Not the same as `evals/`:** the skill's own `evals/` folder holds the rule-checking dataset and runner it uses while running, not tests of the skill
- **Known limit:** `evals/runner.py` is still a placeholder that marks every case as passed, so scenario 4 can't pass until a real eval harness replaces it (see `reference/_roadmap.md`)
