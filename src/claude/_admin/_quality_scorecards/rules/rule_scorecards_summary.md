# 📊 Rule Scorecards Summary

**Purpose:** One-glance rollup of every rule scorecard's Overall score and whether it has Recommended improvements — see which rules need attention without opening each file individually.

---

## 📋 Current scores

Each tier is its own table, sorted descending by Overall score within the tier.

### 01_essentials

| File | Overall | Recommended improvements |
|---|---|---|
| `scorecard_claude_usage_standards.md` | 8.9/10 | — (≥8.5) |
| `scorecard_guiding_principles.md` | 8.4/10 | • Raise `test_guiding_principles.py`'s assertion/function count |
| `scorecard_claude_response_standards.md` | 7.9/10 | • Add a dedicated `test_claude_response_standards.py` structural test<br>• Cite a specific past incident that motivated this rule |

### 02_claude_standards

| File | Overall | Recommended improvements |
|---|---|---|
| `scorecard_portable_paths.md` | 9.4/10 | — (≥8.5) |
| `scorecard_git.md` | 8.1/10 | • Fix the stale `_rules/claude_internal/git.md` reference in `test_git.py`'s docstring |
| `scorecard_behaviour.md` | 7.7/10 | • Add structural tests for the 5 untested children<br>• Document when a behavioral concept becomes its own child file vs. staying inline |
| `scorecard_security.md` | 7.6/10 | • Add a "Related rules" section cross-linking to `behaviour.md`<br>• Add dedicated tests for `_code_security.md` and the parent file |
| `scorecard_testing.md` | 7.6/10 | • Verify the content-regression-test recommendation this file makes is itself followed in the suite |
| `scorecard_claude_plans.md` | 7.6/10 | • Add a "Right" example alongside the existing "Wrong" example<br>• Add a Contents section, matching sibling tier files<br>• Add a dedicated test for `_plan_file_format.md` and the parent's own format |

### 03_authoring_guidelines

| File | Overall | Recommended improvements |
|---|---|---|
| `scorecard_authoring_skills.md` | 8.7/10 | — (≥8.5) |
| `scorecard_claude_config_metadata.md` | 8.4/10 | • Re-score Evidence of Need after one audit cycle has used the backfilled `updated` dates<br>• Decide whether shared authoring standards should stay always-on or move behind a reachability exemption, to recover the ~400 tokens/session |
| `scorecard_authoring_agents.md` | 7.9/10 | • Cite a specific incident or usage evidence justifying always-on placement |
| `scorecard_authoring_rules.md` | 7.1/10 | • Extend `test_authoring_rules.py` to check tier names against the real directory structure |

### 04_claude_reference

| File | Overall | Recommended improvements |
|---|---|---|
| `scorecard_claude_operational_efficiency.md` | 7.1/10 | • Add structural tests for the parent and its 5 imported children<br>• Cite a specific incident that motivated this rule |
| `scorecard_claude_rule_loading_strategy.md` | 6.4/10 | • Extend `test_rules_structure.py`'s emoji check to cover all `##` subheadings |

### 05_lazy_load

| File | Overall | Recommended improvements |
|---|---|---|
| `scorecard_latency_optimisation.md` | 9.2/10 | — (≥8.5) |
| `scorecard_payroc_engineering_naming_standards.md` | 7.8/10 | • Add a dedicated structural test for this file and its 3 children |
| `scorecard_automation_controls.md` | 7.5/10 | • Split into parent + child files — 162 lines with no children |
| `scorecard_airflow.md` | 7.5/10 | • Add a dedicated structural test<br>• Delete or reconcile the orphaned duplicate `airflow/airflow.md` |
| `scorecard_datetime.md` | 7.3/10 | • Add a `**Purpose:**` statement<br>• Add a dedicated structural test |
| `scorecard_ohmyzsh_setup.md` | 7.2/10 | • Add a `**Purpose:**` statement<br>• Add a lightweight structural test |
| `scorecard_ansible.md` | 7.2/10 | • Add a `**Purpose:**` statement<br>• Add a dedicated structural test |
| `scorecard_terraform.md` | 7.0/10 | • Add a `**Purpose:**` statement<br>• Add a dedicated structural test |
| `scorecard_python.md` | 6.8/10 | • Add a dedicated structural test |
| `scorecard_mcp_trust_model.md` | 6.8/10 | • Add a dedicated structural test |
| `scorecard_dbt.md` | 6.7/10 | • Reconcile the redundant Child-pages-table + `@./` imports<br>• Delete or reconcile the orphaned duplicate `dbt/dbt.md`<br>• Add a dedicated structural test |
| `scorecard_mermaid.md` | 6.5/10 | • Add a `**Purpose:**` statement<br>• Add a dedicated structural test |
| `scorecard_docker.md` | 6.5/10 | • Add a `**Purpose:**` statement<br>• Expand beyond a bare 2-item routing list<br>• Add a dedicated structural test |
| `scorecard_bash.md` | 6.5/10 | • Add a dedicated structural test |
| `scorecard_sql.md` | 6.3/10 | • Add an emoji to the "Imports" heading<br>• Reconcile the redundant Child-pages-table + `@./` imports<br>• Delete or reconcile the orphaned duplicate `sql/sql.md`<br>• Add a dedicated structural test |
| `scorecard_jira.md` | 6.3/10 | • Add a `**Purpose:**` statement<br>• Delete or reconcile the orphaned duplicate `jira/jira.md`<br>• Add a dedicated structural test |
| `scorecard_makefile.md` | 5.2/10 | • Add a `**Purpose:**` statement<br>• Add a dedicated structural test |

### Non-tiered

| File | Overall | Recommended improvements |
|---|---|---|
| `scorecard_aliases.md` | 8.6/10 | — (≥8.5) |

---

## 🔄 Keeping this current

- **Update on every scorecard change** — when a scorecard is created or re-scored (per `README.md`'s "When to score" cadence), update this file's row in the same commit. A summary that drifts from the underlying scorecards is worse than no summary — per `guiding_principles.md`'s own "False truth rots silently."
- **Sort order:** each tier's table is sorted descending by Overall score — the rules needing the most attention are at the bottom of their tier.
- **Tier tables mirror `_rules/`'s own tier structure** — a new tier only appears here once it has at least one scored rule.
- **Bullets are copied verbatim** from each file's own `**Recommended improvements:**` section (lightly trimmed for table width) — if you edit a bullet in one place, update the other.

---

## 🔗 Related

- `README.md` — the scorecard convention, template, and per-dimension criteria this file summarizes
- Individual `scorecard_*.md` files — full detail behind each row above
