# 📈 Rule usage history

**Generated:** 2026-10-01 by `make audit_rule_usage` · **Sessions recorded:** 115 (2026-08-31 to 2026-10-01) · **Runs:** 1

Each session counts once per rule, however many runs saw it. Sessions stay in the record after Claude Code deletes their logs, so these totals keep growing past the 90-day log limit.

## 📖 How to read this

- **Applied / Loaded / Misses:** sessions, all time — the same meaning as in `audit_rule_usage.md`.
- **Miss rate:** misses as a share of applied sessions.
- **Runs:** distinct days `make audit_rule_usage` measured the rule.
- **First seen / Last used:** the earliest and latest session where the rule applied or loaded.
- **Removed:** a rule in the record that no longer exists, usually after a rename.

## 🔎 Key insights

### 🔥 Highest miss rates (at least 10 applied sessions)

1. `05_lazy_load/claude_rule_loading_strategy.md` — missed 35 of 35 sessions (100%)
2. `05_lazy_load/testing_guidance.md` — missed 28 of 28 sessions (100%)
3. `05_lazy_load/style_guide_standards/python.md` — missed 29 of 30 sessions (97%)
4. `05_lazy_load/style_guide_standards/bash.md` — missed 10 of 11 sessions (91%)
5. `01_essentials/claude_usage_standards.md` — missed 28 of 115 sessions (24%)

- **Too few sessions to rank:** 5 more rules have misses but under 10 applied sessions.

### ⭐ Most used

- **Every-session rules:** 7 rules apply to every session (`applies_to: *`), loaded in 87–104 sessions each.
- **Most needed of the rest, by sessions applied:**

1. `01_essentials/guiding_principles.md` — applied in 88 sessions, loaded in 104
2. `02_claude_standards/testing.md` — applied in 37 sessions, loaded in 104
3. `05_lazy_load/claude_rule_loading_strategy.md` — applied in 35 sessions, loaded in 0
4. `03_authoring_guidelines/authoring_rules.md` — applied in 32 sessions, loaded in 87
5. `05_lazy_load/style_guide_standards/python.md` — applied in 30 sessions, loaded in 1

## 📋 Rules by tier

### 🧭 01 Essentials

| Rule | Applied | Loaded | Misses | Miss rate | Runs | First seen | Last used |
|---|---|---|---|---|---|---|---|
| `01_essentials/claude_response_standards.md` | 115 | 104 | 11 | 10% | 1 | 2026-08-31 | 2026-10-01 |
| `01_essentials/claude_usage_standards.md` | 115 | 87 | 28 | 24% | 1 | 2026-08-31 | 2026-10-01 |
| `01_essentials/guiding_principles.md` | 88 | 104 | 5 | 6% | 1 | 2026-08-31 | 2026-10-01 |

### 🛡️ 02 Claude standards

| Rule | Applied | Loaded | Misses | Miss rate | Runs | First seen | Last used |
|---|---|---|---|---|---|---|---|
| `02_claude_standards/behaviour.md` | 115 | 104 | 11 | 10% | 1 | 2026-08-31 | 2026-10-01 |
| `02_claude_standards/claude_plans.md` | 115 | 87 | 28 | 24% | 1 | 2026-08-31 | 2026-10-01 |
| `02_claude_standards/git.md` | 115 | 104 | 11 | 10% | 1 | 2026-08-31 | 2026-10-01 |
| `02_claude_standards/portable_paths.md` | 27 | 87 | 2 | 7% | 1 | 2026-08-31 | 2026-10-01 |
| `02_claude_standards/security.md` | 115 | 104 | 11 | 10% | 1 | 2026-08-31 | 2026-10-01 |
| `02_claude_standards/testing.md` | 37 | 104 | 1 | 3% | 1 | 2026-08-31 | 2026-10-01 |

### 🛠️ 03 Authoring guidelines

| Rule | Applied | Loaded | Misses | Miss rate | Runs | First seen | Last used |
|---|---|---|---|---|---|---|---|
| `03_authoring_guidelines/authoring_agents.md` | 2 | 81 | 1 | 50% | 1 | 2026-09-07 | 2026-10-01 |
| `03_authoring_guidelines/authoring_rules.md` | 32 | 87 | 5 | 16% | 1 | 2026-09-16 | 2026-10-01 |
| `03_authoring_guidelines/authoring_skills.md` | 17 | 87 | 4 | 24% | 1 | 2026-09-07 | 2026-10-01 |

### 📚 04 Claude reference

| Rule | Applied | Loaded | Misses | Miss rate | Runs | First seen | Last used |
|---|---|---|---|---|---|---|---|
| `04_claude_reference/claude_operational_efficiency.md` | 115 | 87 | 28 | 24% | 1 | 2026-08-31 | 2026-10-01 |

### 💤 05 Lazy load

| Rule | Applied | Loaded | Misses | Miss rate | Runs | First seen | Last used |
|---|---|---|---|---|---|---|---|
| `05_lazy_load/automation_controls.md` | 0 | 0 | 0 | — | 1 | — | — |
| `05_lazy_load/claude_rule_loading_strategy.md` | 35 | 0 | 35 | 100% | 1 | 2026-08-31 | 2026-10-01 |
| `05_lazy_load/delegating_to_subagent.md` | 0 | 0 | 0 | — | 1 | — | — |
| `05_lazy_load/hooks_decision_framework.md` | 3 | 0 | 3 | 100% | 1 | 2026-09-19 | 2026-09-30 |
| `05_lazy_load/latency_optimisation.md` | 0 | 3 | 0 | — | 1 | 2026-09-19 | 2026-10-01 |
| `05_lazy_load/mcp_trust_model.md` | 0 | 0 | 0 | — | 1 | — | — |
| `05_lazy_load/response_standards_enforcement.md` | 2 | 1 | 1 | 50% | 1 | 2026-09-19 | 2026-09-30 |
| `05_lazy_load/style_guide_standards/airflow.md` | 0 | 0 | 0 | — | 1 | — | — |
| `05_lazy_load/style_guide_standards/bash.md` | 11 | 1 | 10 | 91% | 1 | 2026-08-31 | 2026-10-01 |
| `05_lazy_load/style_guide_standards/dbt.md` | 0 | 0 | 0 | — | 1 | — | — |
| `05_lazy_load/style_guide_standards/infra/ansible.md` | 0 | 0 | 0 | — | 1 | — | — |
| `05_lazy_load/style_guide_standards/infra/docker.md` | 0 | 0 | 0 | — | 1 | — | — |
| `05_lazy_load/style_guide_standards/infra/terraform.md` | 0 | 0 | 0 | — | 1 | — | — |
| `05_lazy_load/style_guide_standards/jira.md` | 0 | 0 | 0 | — | 1 | — | — |
| `05_lazy_load/style_guide_standards/org_naming_standards.md` | 0 | 0 | 0 | — | 1 | — | — |
| `05_lazy_load/style_guide_standards/python.md` | 30 | 1 | 29 | 97% | 1 | 2026-08-31 | 2026-10-01 |
| `05_lazy_load/style_guide_standards/sql.md` | 5 | 4 | 1 | 20% | 1 | 2026-09-09 | 2026-10-01 |
| `05_lazy_load/style_guide_standards/utilities/datetime.md` | 0 | 0 | 0 | — | 1 | — | — |
| `05_lazy_load/style_guide_standards/utilities/makefile.md` | 5 | 1 | 5 | 100% | 1 | 2026-09-09 | 2026-10-01 |
| `05_lazy_load/style_guide_standards/utilities/mermaid.md` | 0 | 0 | 0 | — | 1 | — | — |
| `05_lazy_load/testing_guidance.md` | 28 | 0 | 28 | 100% | 1 | 2026-08-31 | 2026-10-01 |
| `05_lazy_load/turn_budgets.md` | 0 | 0 | 0 | — | 1 | — | — |

## ⚠️ Limits

- **Always-on misses:** usually sessions that ran before the file was added or renamed, not times Claude skipped it.
- **Globs at measure time:** a session's applied value uses the rule's globs from the last run that still had its log, so changing a rule's `applies_to` doesn't rewrite older sessions.
- **Starts at the first run:** sessions deleted before 2026-10-01 were never recorded.
