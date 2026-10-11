# 📊 Rule Scorecards Summary

**Purpose:** One-glance rollup of every rule scorecard, showing where quality is weakest and what to fix first, without opening each file.

---

## 📋 Scores by tier

- **Overall:** the mean of every scorecard's Overall score in that tier.
- **Strongest and weakest:** the highest- and lowest-scoring file in that tier, by Overall score.
- **Date Updated:** the latest `Date Updated` among that tier's scorecards.
- **Priority:** the tiers that load every session (01–03 and Non-tiered `aliases.md`) rank above `rules_lazy_load` and `style_guide_standards`, which load only on demand or with matching files.

| Tier | Scored | Overall | Date Updated | Strengths and gaps |
|---|---|---|---|---|
| 01_essentials | 3 | 8.7/10 | 2026-10-11 | • 💪 **Strongest:** `claude_usage_standards.md` (9.1/10)<br>• ⚠️ **Weakest:** `claude_response_standards.md` (8.1/10) |
| 02_claude_standards | 11 | 8.2/10 | 2026-10-11 | • 💪 **Strongest:** `portable_paths.md` (9.4/10)<br>• ⚠️ **Weakest:** `automation_controls.md` (7.5/10) |
| 03_authoring_guidelines | 4 | 8.4/10 | 2026-10-11 | • 💪 **Strongest:** `authoring_skills.md` (8.7/10)<br>• ⚠️ **Weakest:** `authoring_agents.md` (7.9/10) |
| rules_lazy_load | 1 | 9.2/10 | 2026-10-11 | • 💪 **Only file:** `latency_optimisation.md` (9.2/10) |
| style_guide_standards | 11 | 8.4/10 | 2026-10-01 | • 💪 **Strongest:** 2 files tied at 9.0/10, including `airflow.md`<br>• ⚠️ **Weakest:** `makefile.md` (6.8/10) |
| Non-tiered | 1 | 8.6/10 | 2026-09-28 | • 💪 **Only file:** `aliases.md` (8.6/10) |

---

## 🚀 Recommended next actions

Ranked by impact, highest first, with always-on rules before lazy-load rules.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 🔧 **`automation_controls.md`:** split into parent and child files, since at 162 lines it is well past the ~100-line limit | • 🔻 **Score:** 7.5/10 | `02_claude_standards/scorecard_automation_controls.md` |
| 2 | • 🔧 **`claude_plans.md`:** add a "Right" example alongside the existing "Wrong" example in the Example section | • 🔻 **Score:** 7.6/10 | `02_claude_standards/scorecard_claude_plans.md` |
| 3 | • 🔧 **`claude_operational_efficiency.md`:** cite a specific incident or recurring problem that motivated this rule | • 🔻 **Score:** 8.0/10 | `02_claude_standards/scorecard_claude_operational_efficiency.md` |
| 4 | • 🔧 **`claude_response_standards.md`:** cite a specific past incident or failure that motivated this rule | • 🔻 **Score:** 8.1/10 | `01_essentials/scorecard_claude_response_standards.md` |
| 5 | • 🔧 **`security.md`:** add a "Related rules" section cross-linking to `behaviour.md` and other conduct rules | • 🔻 **Score:** 8.1/10 | `02_claude_standards/scorecard_security.md` |

---

## 📄 All scorecards

Sorted by Overall score, highest first.

| Scorecard | Overall | Date Updated | Recommended improvements |
|---|---|---|---|
| `02_claude_standards/scorecard_portable_paths.md` | 9.4/10 | 2026-10-01 | — (≥8.5) |
| `rules_lazy_load/scorecard_latency_optimisation.md` | 9.2/10 | 2026-10-11 | — (≥8.5) |
| `01_essentials/scorecard_claude_usage_standards.md` | 9.1/10 | 2026-10-11 | — (≥8.5) |
| `01_essentials/scorecard_guiding_principles.md` | 9.0/10 | 2026-10-01 | — (≥8.5) |
| `style_guide_standards/scorecard_airflow.md` | 9.0/10 | 2026-10-01 | — (≥8.5) |
| `style_guide_standards/utilities/scorecard_datetime.md` | 9.0/10 | 2026-10-01 | — (≥8.5) |
| `02_claude_standards/scorecard_claude_rule_loading_strategy.md` | 8.9/10 | 2026-10-01 | — (≥8.5) |
| `style_guide_standards/infra/scorecard_ansible.md` | 8.8/10 | 2026-10-01 | — (≥8.5) |
| `style_guide_standards/scorecard_sql.md` | 8.8/10 | 2026-10-01 | — (≥8.5) |
| `03_authoring_guidelines/scorecard_authoring_skills.md` | 8.7/10 | 2026-09-29 | — (≥8.5) |
| `style_guide_standards/infra/scorecard_terraform.md` | 8.7/10 | 2026-10-01 | — (≥8.5) |
| `02_claude_standards/scorecard_git.md` | 8.7/10 | 2026-10-11 | — (≥8.5) |
| `scorecard_aliases.md` | 8.6/10 | 2026-09-28 | — (≥8.5) |
| `style_guide_standards/scorecard_python.md` | 8.5/10 | 2026-10-01 | — (≥8.5) |
| `03_authoring_guidelines/scorecard_claude_config_metadata.md` | 8.4/10 | 2026-09-28 | • Re-score Evidence of Need after one audit cycle has used the backfilled `updated` dates<br>• Decide whether shared authoring standards should stay always-on or move behind a reachability exemption, to recover the ~400 tokens/session |
| `03_authoring_guidelines/scorecard_authoring_rules.md` | 8.4/10 | 2026-10-11 | • Lower the guide's complexity (6/10), its weakest dimension, by moving detail into its on-demand children. |
| `02_claude_standards/scorecard_claude_working_practices.md` | 8.3/10 | 2026-10-11 | • Add a content test for the index, or drop it if the extra startup file isn't worth it |
| `02_claude_standards/scorecard_behaviour.md` | 8.3/10 | 2026-10-11 | • Document a clear criterion for when a behavioral concept is promoted to its own child file versus kept inline in the parent. |
| `style_guide_standards/infra/scorecard_docker.md` | 8.2/10 | 2026-10-01 | • Add some inline content (principles, examples, or a "when to load" column) |
| `style_guide_standards/scorecard_dbt.md` | 8.2/10 | 2026-10-01 | • Reconcile the redundant `@./dbt/*.md` imports block with the "Child pages" markdown-link table above it |
| `style_guide_standards/utilities/scorecard_mermaid.md` | 8.2/10 | 2026-10-01 | • Add inline principles or a short example, so the file is more than a 2-item routing list |
| `02_claude_standards/scorecard_security.md` | 8.1/10 | 2026-10-11 | • Add a "Related rules" section cross-linking to `behaviour.md` and other rules touching conduct/injection concerns. |
| `01_essentials/scorecard_claude_response_standards.md` | 8.1/10 | 2026-10-11 | • Cite a specific past incident or failure that motivated this rule, similar to how `portable_paths.md` documents its incidents. |
| `02_claude_standards/scorecard_mcp_trust_model.md` | 8.0/10 | 2026-10-01 | • Fix the broken `/docs/mcp_servers.md` reference<br>• Point the `security_guardrails.md` reference at `rules/02_claude_standards/security/_security_guardrails.md` |
| `02_claude_standards/scorecard_claude_operational_efficiency.md` | 8.0/10 | 2026-10-11 | • Cite a specific incident or recurring problem that motivated this rule. |
| `03_authoring_guidelines/scorecard_authoring_agents.md` | 7.9/10 | 2026-09-30 | • Cite a specific incident or usage evidence justifying this file's always-on, Tier 3 placement |
| `02_claude_standards/scorecard_testing.md` | 7.7/10 | 2026-10-01 | • Add a check to `test_testing.py` that verifies the content-regression-test recommendation this file makes is itself followed somewhere in the test suite |
| `style_guide_standards/scorecard_bash.md` | 7.7/10 | 2026-10-01 | • Fix the template path so it reads `_templates/utils/template_bash_script.sh` |
| `02_claude_standards/scorecard_claude_plans.md` | 7.6/10 | 2026-09-28 | • Add a "Right" example alongside the existing "Wrong" example in the Example section, per the heading's implied pairing<br>• Add a Contents section, matching the sibling files in this tier (`behaviour.md`, `git.md`, `testing.md`)<br>• Add a dedicated test for the `_plan_file_format.md` child and the parent's own inline "How to apply" format |
| `02_claude_standards/scorecard_automation_controls.md` | 7.5/10 | 2026-10-11 | • Split into parent + child files — at 162 lines it's well past the ~100-line limit, with no children to absorb the detail. |
| `style_guide_standards/utilities/scorecard_makefile.md` | 6.8/10 | 2026-10-01 | • Fix or remove the broken `~/.claude/templates/makefile/` templates reference<br>• Add inline principles beyond the 2-item routing list |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever a scorecard it covers is created or re-scored.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files.
- **Bump dates:** set a tier's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its scorecard no longer lists it.
- **Template:** this file follows `_templates/scorecard/scorecard_summary.md.template`.
