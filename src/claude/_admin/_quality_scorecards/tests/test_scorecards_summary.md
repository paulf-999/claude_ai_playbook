# 📊 Test Scorecards Summary

**Purpose:** One-glance rollup of every test scorecard, showing where quality is weakest and what to fix first, without opening each file.

---

## 📋 Scores by folder

- **Overall:** the mean of every scorecard's Overall score in that folder.
- **Strongest and weakest:** the highest- and lowest-scoring file in that folder, by Overall score.
- **Date Updated:** the latest `Date Updated` among that folder's scorecards.

| Folder | Scored | Overall | Date Updated | Strengths and gaps |
|---|---|---|---|---|
| admin | 1 | 9.3/10 | 2026-10-01 | • 💪 **Only file:** `test_scorecard_dates.py` (9.3/10) |
| agents | 1 | 9.0/10 | 2026-09-30 | • 💪 **Only file:** `test_agent_metadata_header.py` (9.0/10) |
| hooks | 7 | 9.2/10 | 2026-10-01 | • 💪 **Strongest:** 5 files tied at 9.3/10, including `test_enforcement_writing_style.py`<br>• ⚠️ **Weakest:** `test_enforcement_mcp_stale_settings.py` (9.1/10) |
| rules | 30 | 9.0/10 | 2026-10-01 | • 💪 **Strongest:** `test_latency_optimisation.py` (9.6/10)<br>• ⚠️ **Weakest:** `test_skill_authoring_gate.py` (7.7/10) |
| settings | 2 | 9.5/10 | 2026-10-01 | • 💪 **Strongest:** `test_aliases.py` (9.6/10)<br>• ⚠️ **Weakest:** `test_settings.py` (9.3/10) |
| skills | 7 | 8.1/10 | 2026-10-01 | • 💪 **Strongest:** `test_skill_metadata_header.py` (9.1/10)<br>• ⚠️ **Weakest:** `test_confluence_create_page_timeout.py` (6.9/10) |
| _tests root | 4 | 9.2/10 | 2026-10-01 | • 💪 **Strongest:** `test_rule_reachability.py` (9.6/10)<br>• ⚠️ **Weakest:** `test_file_structure_compliance.py` (8.9/10) |

---

## 🚀 Recommended next actions

Ranked by impact, highest first.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 🔧 **`test_confluence_create_page_timeout.py`:** add failure messages that say how to fix each assertion (0% have one today) | • 🔻 **Score:** 6.9/10 | `skills/confluence_create_page/scorecard_test_confluence_create_page_timeout.md` |
| 2 | • 🔧 **`test_jira_create_handler.py`:** add failure messages that say how to fix each assertion (0% have one today) | • 🔻 **Score:** 7.4/10 | `skills/jira_create/scorecard_test_jira_create_handler.md` |
| 3 | • 🔧 **`test_skill_authoring_gate.py`:** split the test by concept to bring raw complexity (5) down to 3 or less | • 🔻 **Score:** 7.7/10 | `rules/01_essentials/scorecard_test_skill_authoring_gate.md` |

---

## 📄 All scorecards

Sorted by Overall score, highest first.

| Scorecard | Overall | Date Updated | Recommended improvements |
|---|---|---|---|
| `rules/05_lazy_load/scorecard_test_latency_optimisation.md` | 9.6/10 | 2026-10-01 | — (≥8.5) |
| `scorecard_test_rule_reachability.md` | 9.6/10 | 2026-10-01 | — (≥8.5) |
| `settings/scorecard_test_aliases.md` | 9.6/10 | 2026-10-01 | — (≥8.5) |
| `rules/01_essentials/scorecard_test_guiding_principles.md` | 9.4/10 | 2026-10-01 | — (≥8.5) |
| `rules/01_essentials/scorecard_test_writing_style.md` | 9.4/10 | 2026-10-01 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_portable_paths_hooks.md` | 9.4/10 | 2026-10-01 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_portable_paths_python.md` | 9.4/10 | 2026-10-01 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_authoring_skills_maturity.md` | 9.4/10 | 2026-10-01 | — (≥8.5) |
| `admin/scorecard_test_scorecard_dates.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `hooks/enforcement/scorecard_test_enforcement_writing_style.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `hooks/response_standards/scorecard_test_style_guide_response_standards_flags.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `hooks/response_standards/scorecard_test_style_guide_response_standards_inject.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `hooks/response_standards/scorecard_test_style_guide_response_standards_waivers.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `hooks/scorecard_test_hook_registry_utils.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `rules/01_essentials/scorecard_test_rule_directory_organisation.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_git.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_test_metadata.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_test_score_floor.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_authoring_skills.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `scorecard_test_file_structure_validator.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `settings/scorecard_test_settings.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `hooks/enforcement/scorecard_test_enforcement_mcp_stale_settings.md` | 9.1/10 | 2026-10-01 | — (≥8.5) |
| `hooks/enforcement/scorecard_test_enforcement_naming_convention.md` | 9.1/10 | 2026-10-01 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_always_on_reachability.md` | 9.1/10 | 2026-10-01 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_security_guardrails.md` | 9.1/10 | 2026-10-01 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_authoring_rules.md` | 9.1/10 | 2026-10-01 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_claude_config_metadata.md` | 9.1/10 | 2026-09-30 | — (≥8.5) |
| `skills/scorecard_test_skill_metadata_header.md` | 9.1/10 | 2026-09-30 | — (≥8.5) |
| `agents/scorecard_test_agent_metadata_header.md` | 9.0/10 | 2026-09-30 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_decision_making.md` | 9.0/10 | 2026-10-01 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_plan_mode_phase_gates.md` | 9.0/10 | 2026-09-30 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_testing.md` | 9.0/10 | 2026-10-01 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_skill_domains.md` | 9.0/10 | 2026-09-30 | — (≥8.5) |
| `rules/05_lazy_load/scorecard_test_lazy_load_rule_structure.md` | 9.0/10 | 2026-10-01 | — (≥8.5) |
| `rules/scorecard_test_rules_structure.md` | 9.0/10 | 2026-10-01 | — (≥8.5) |
| `rules/scorecard_test_rules_structure_layout.md` | 9.0/10 | 2026-10-01 | — (≥8.5) |
| `scorecard_test_hook_metadata_header.md` | 9.0/10 | 2026-09-30 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_artefact_proposal_gates.md` | 8.9/10 | 2026-09-30 | — (≥8.5) |
| `scorecard_test_file_structure_compliance.md` | 8.9/10 | 2026-10-01 | — (≥8.5) |
| `skills/scorecard_test_skill_structure_compliance.md` | 8.9/10 | 2026-09-30 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_concurrent_sessions.md` | 8.7/10 | 2026-09-30 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_authoring_agents.md` | 8.6/10 | 2026-09-30 | — (≥8.5) |
| `rules/04_claude_reference/scorecard_test_claude_operational_efficiency.md` | 8.6/10 | 2026-09-30 | — (≥8.5) |
| `rules/05_lazy_load/scorecard_test_automation_controls.md` | 8.6/10 | 2026-10-01 | — (≥8.5) |
| `rules/05_lazy_load/scorecard_test_claude_rule_loading_strategy.md` | 8.4/10 | 2026-10-01 | • Add a synthetic bad-input test that proves the check fails when it should |
| `rules/05_lazy_load/scorecard_test_lazy_load_coverage.md` | 8.3/10 | 2026-09-30 | • Add failure messages that say how to fix each assertion (27% have one today) |
| `skills/scorecard_test_no_orphaned_skill_files.md` | 8.3/10 | 2026-09-30 | • Add failure messages that say how to fix each assertion (16% have one today)<br>• Split the test by concept to bring raw complexity (5) down to 3 or less |
| `skills/claude_capture_session_prompts/scorecard_test_capture_session_prompts.md` | 8.1/10 | 2026-09-30 | • Add failure messages that say how to fix each assertion (14% have one today)<br>• Add a synthetic bad-input test that proves the check fails when it should |
| `rules/01_essentials/scorecard_test_skill_authoring_gate.md` | 7.7/10 | 2026-10-01 | • Split the test by concept to bring raw complexity (5) down to 3 or less<br>• Fix the style gaps and set `Python style compliant: Yes`<br>• Turn the manual-review skips into failures, or `xfail` with a tracked reason, so real gaps can't pass quietly |
| `skills/confluence_create_page/scorecard_test_confluence_create_page_handler.md` | 7.7/10 | 2026-09-30 | • Add failure messages that say how to fix each assertion (1% have one today)<br>• Split the test by concept to bring raw complexity (6) down to 3 or less<br>• Confirm the handler still mirrors what SKILL.md tells Claude to do, or move the handler into the skill so the test covers real behaviour |
| `skills/jira_create/scorecard_test_jira_create_handler.md` | 7.4/10 | 2026-10-01 | • Add failure messages that say how to fix each assertion (0% have one today)<br>• Fix the style gaps and set `Python style compliant: Yes`<br>• Confirm the handler still mirrors what SKILL.md tells Claude to do, or move the handler into the skill so the test covers real behaviour |
| `skills/confluence_create_page/scorecard_test_confluence_create_page_timeout.md` | 6.9/10 | 2026-09-30 | • Add failure messages that say how to fix each assertion (0% have one today)<br>• Split the test by concept to bring raw complexity (6) down to 3 or less<br>• Add test functions and assertions toward 10+ and 15+ (now 9 and 19)<br>• Add a synthetic bad-input test that proves the check fails when it should<br>• Confirm the handler still mirrors what SKILL.md tells Claude to do, or move the handler into the skill so the test covers real behaviour |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever a scorecard it covers is created or re-scored.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files.
- **Bump dates:** set a folder's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its scorecard no longer lists it.
- **Template:** this file follows `_templates/scorecard_summary.md.template`.
