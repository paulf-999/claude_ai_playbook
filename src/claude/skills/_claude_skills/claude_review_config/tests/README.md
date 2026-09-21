# 🧪 Tests

`evals.yaml` holds this skill's test scenarios — recorded situations (a user request, the setup, the expected result) that check `claude_review_config` still behaves correctly as it changes over time. They aren't code; think of them as worked examples an author checks the skill against.

## 📋 Scenarios

| # | Scenario | Phase | What it checks |
|---|---|---|---|
| 1 | `phase1_read_config` | Audit & score | Reads config files without parsing errors, identifies all imported rules |
| 2 | `phase1_score_dimensions` | Audit & score | Scores all 6 quality dimensions (1–10) with reasoning and an overall grade |
| 3 | `phase1_generate_scorecard` | Audit & score | Generates a complete scorecard table with per-dimension notes |
| 4 | `phase1_error_missing_claude_md` | Audit & score | Missing `CLAUDE.md` produces a clear error and a graceful exit, not a crash |
| 5 | `phase2_moscow_table` | Analyze gaps | Generates a MoSCoW (Must/Should) prioritization table of identified gaps |
| 6 | `phase2_recommendations_with_severity` | Analyze gaps | Produces severity-rated (Critical/High/Medium/Low) recommendations |
| 7 | `phase3_propose_fixes_for_must_items` | Offer fixes | Proposes a fix per Must item with a user approval prompt |
| 8 | `phase4_apply_fixes_to_config` | Apply fixes | Applies an approved fix to the config file and confirms |
| 9 | `phase4_sync_to_playbook_repo` | Apply fixes | Keeps `~/.claude/` and the playbook repo's `src/claude/` in sync after a fix |
| 10 | `error_malformed_yaml_in_rules` | Error handling | Malformed YAML in a rule file is caught, not a crash |
| 11 | `error_missing_rules_directory` | Error handling | A missing `_rules/` directory produces a clear error, not a crash |

- **No Python handler:** this skill has none
- **Only coverage:** `evals.yaml` is this skill's sole test coverage
