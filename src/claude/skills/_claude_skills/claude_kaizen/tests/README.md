# 🧪 Tests

`evals.yaml` holds this skill's test scenarios: recorded situations (a user request, the setup, the expected result) that check `claude_kaizen` still behaves correctly as it changes over time. They aren't code. Think of them as worked examples an author checks the skill against.

## 📋 Scenarios

| # | Scenario | Phase | What it checks |
|---|---|---|---|
| 1 | `happy_path_promotes_recurring_pattern` | Promote | A mistake seen twice becomes a rule and eval, shown as a diff for review |
| 2 | `one_off_mistake_not_promoted` | Promote | A mistake seen once stays a candidate |
| 3 | `declined_diff_writes_nothing` | Promote | Rejecting the proposal leaves `_rules_lazy_load/_learned/` unchanged |
| 4 | `regression_blocks_promotion` | Validate | A rule that breaks a previously passing eval isn't presented as ready |
| 5 | `stale_rule_flagged_not_removed` | Prune | A rule older than 6 months is flagged, not deleted |
| 6 | `missing_errors_dir` | Setup | No `~/_errors/` means no audit, and no invented patterns |
| 7 | `cross_repo_request_out_of_scope` | Scope | Cross-repo promotion is declined as a planned v2 feature |
| 8 | `bulk_rule_removal_declined` | Scope | A request to delete every stale rule flags them for re-validation and deletes nothing |

- **Maturity:** 8 scenarios sits within the 8–12 expected for a **tactical** skill
- **Not the same as `evals/`:** the skill's own `evals/` folder holds the rule-checking dataset and runner it uses while running, not tests of the skill
- **Runner:** `evals/runner.py` asks headless Claude each rule-checking case and judges the reply with regexes, one Claude call per case
- **Known limit:** nothing runs the scenarios in this `evals.yaml` yet, which #463 tracks
