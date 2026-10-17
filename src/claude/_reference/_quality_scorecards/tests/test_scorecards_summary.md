# 📊 Test Scorecards Summary

**Purpose:** One-glance rollup of every test scorecard, showing where quality is weakest and what to fix first, without opening each file.

---

## 📋 Scores by folder

- **Overall:** the mean of every scorecard's Overall score in that folder.
- **Strongest and weakest:** the highest- and lowest-scoring file in that folder, by Overall score.
- **Date Updated:** the latest `Date Updated` among that folder's scorecards.

| Folder | Scored | Overall | Date Updated | Strengths and gaps |
|---|---|---|---|---|
| admin | 2 | 9.0/10 | 2026-10-11 | • 💪 **Strongest:** `test_scorecard_dates.py` (9.3/10)<br>• ⚠️ **Weakest:** `test_scorecard_coverage.py` (8.7/10) |
| agents | 2 | 9.2/10 | 2026-10-11 | • 💪 **Strongest:** `test_agent_triggers.py` (9.3/10)<br>• ⚠️ **Weakest:** `test_agent_metadata_header.py` (9.0/10) |
| docs | 1 | 9.0/10 | 2026-10-11 | • 💪 **Only file:** `test_docs_local_links.py` (9.0/10) |
| hooks | 8 | 9.2/10 | 2026-10-11 | • 💪 **Strongest:** 5 files tied at 9.3/10, including `test_enforcement_markdown_location.py`<br>• ⚠️ **Weakest:** `test_hook_metadata_header.py` (9.0/10) |
| rules | 27 | 9.0/10 | 2026-10-11 | • 💪 **Strongest:** 3 files tied at 9.4/10, including `test_no_wording_pinning.py`<br>• ⚠️ **Weakest:** `test_lazy_load_coverage.py` (8.3/10) |
| scripts | 5 | 9.2/10 | 2026-10-11 | • 💪 **Strongest:** 3 files tied at 9.3/10, including `test_audit_claude_component_root.py`<br>• ⚠️ **Weakest:** `test_audit_plans.py` (9.0/10) |
| settings | 2 | 9.4/10 | 2026-10-01 | • 💪 **Strongest:** `test_aliases.py` (9.6/10)<br>• ⚠️ **Weakest:** `test_settings.py` (9.3/10) |
| skills | 9 | 9.0/10 | 2026-10-11 | • 💪 **Strongest:** 3 files tied at 9.4/10, including `test_no_orphaned_skill_files.py`<br>• ⚠️ **Weakest:** `test_capture_session_prompts.py` (8.1/10) |
| _core | 4 | 9.3/10 | 2026-10-11 | • 💪 **Strongest:** `test_rule_reachability.py` (9.6/10)<br>• ⚠️ **Weakest:** `test_file_structure_compliance.py` (8.9/10) |

---

## 🚀 Recommended next actions

Ranked by impact, highest first.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 🔧 **`test_capture_session_prompts.py`:** add failure messages that say how to fix each assertion (14% have one today) | • 🔻 **Score:** 8.1/10 | `skills/claude_capture_session_prompts/scorecard_test_capture_session_prompts.md` |
| 2 | • 🔧 **`test_lazy_load_coverage.py`:** add failure messages that say how to fix each assertion (27% have one today) | • 🔻 **Score:** 8.3/10 | `rules/rules_lazy_load/scorecard_test_lazy_load_coverage.md` |

---

## 📄 All scorecards

Sorted by Overall score, highest first.

| Scorecard | Overall | Date Updated | Recommended improvements |
|---|---|---|---|
| `_helpers/scorecard_test_rule_reachability.md` | 9.6/10 | 2026-10-11 | — (≥8.5) |
| `settings/scorecard_test_aliases.md` | 9.6/10 | 2026-10-01 | — (≥8.5) |
| `_helpers/scorecard_test_metadata_header_format.md` | 9.4/10 | 2026-10-11 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_no_wording_pinning.md` | 9.4/10 | 2026-10-11 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_portable_paths_hooks.md` | 9.4/10 | 2026-10-01 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_portable_paths_python.md` | 9.4/10 | 2026-10-01 | — (≥8.5) |
| `skills/scorecard_test_no_orphaned_skill_files.md` | 9.4/10 | 2026-10-01 | — (≥8.5) |
| `skills/scorecard_test_skill_authoring_gate_run.md` | 9.4/10 | 2026-10-01 | — (≥8.5) |
| `skills/scorecard_test_skill_authoring_gate_walk.md` | 9.4/10 | 2026-10-01 | — (≥8.5) |
| `_helpers/scorecard_test_file_structure_validator.md` | 9.3/10 | 2026-10-11 | — (≥8.5) |
| `admin/scorecard_test_scorecard_dates.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `agents/scorecard_test_agent_triggers.md` | 9.3/10 | 2026-10-11 | — (≥8.5) |
| `hooks/enforcement/scorecard_test_enforcement_markdown_location.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `hooks/response_standards/scorecard_test_style_guide_response_standards_checker_flags.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `hooks/response_standards/scorecard_test_style_guide_response_standards_checker_waivers.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `hooks/response_standards/scorecard_test_style_guide_response_standards_reminder.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `hooks/scorecard_test_hook_registry_utils.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `rules/01_essentials/scorecard_test_guiding_principles.md` | 9.3/10 | 2026-10-11 | — (≥8.5) |
| `rules/01_essentials/scorecard_test_rule_directory_organisation.md` | 9.3/10 | 2026-10-11 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_authoring_skills.md` | 9.3/10 | 2026-10-11 | — (≥8.5) |
| `rules/rules_lazy_load/scorecard_test_test_quality_score.md` | 9.3/10 | 2026-10-11 | — (≥8.5) |
| `scripts/scorecard_test_audit_claude_component_root.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `scripts/scorecard_test_clean_plans.md` | 9.3/10 | 2026-10-02 | — (≥8.5) |
| `scripts/scorecard_test_script_naming.md` | 9.3/10 | 2026-10-02 | — (≥8.5) |
| `settings/scorecard_test_settings.md` | 9.3/10 | 2026-10-01 | — (≥8.5) |
| `hooks/enforcement/scorecard_test_enforcement_mcp_stale_settings.md` | 9.1/10 | 2026-10-01 | — (≥8.5) |
| `hooks/enforcement/scorecard_test_enforcement_naming_convention.md` | 9.1/10 | 2026-10-01 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_always_on_reachability.md` | 9.1/10 | 2026-10-11 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_plan_mode_phase_gates.md` | 9.1/10 | 2026-10-11 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_rule_headers.md` | 9.1/10 | 2026-10-01 | — (≥8.5) |
| `rules/rules_lazy_load/scorecard_test_lazy_load_triggers.md` | 9.1/10 | 2026-10-11 | — (≥8.5) |
| `rules/rules_lazy_load/scorecard_test_test_metadata.md` | 9.1/10 | 2026-10-02 | — (≥8.5) |
| `rules/rules_lazy_load/scorecard_test_test_score_floor.md` | 9.1/10 | 2026-10-11 | — (≥8.5) |
| `scripts/scorecard_test_audit_rule_usage.md` | 9.1/10 | 2026-10-01 | — (≥8.5) |
| `skills/scorecard_test_skill_index_versions.md` | 9.1/10 | 2026-10-05 | — (≥8.5) |
| `agents/scorecard_test_agent_metadata_header.md` | 9.0/10 | 2026-10-11 | — (≥8.5) |
| `docs/scorecard_test_docs_local_links.md` | 9.0/10 | 2026-10-11 | — (≥8.5) |
| `hooks/scorecard_test_hook_metadata_header.md` | 9.0/10 | 2026-10-11 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_path_scoped_rules.md` | 9.0/10 | 2026-10-11 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_claude_config_metadata.md` | 9.0/10 | 2026-10-11 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_skill_domains.md` | 9.0/10 | 2026-09-30 | — (≥8.5) |
| `rules/rules_lazy_load/scorecard_test_lazy_load_rule_structure.md` | 9.0/10 | 2026-10-11 | — (≥8.5) |
| `rules/scorecard_test_rules_structure.md` | 9.0/10 | 2026-10-11 | — (≥8.5) |
| `rules/scorecard_test_rules_structure_layout.md` | 9.0/10 | 2026-10-11 | — (≥8.5) |
| `scripts/scorecard_test_audit_plans.md` | 9.0/10 | 2026-10-11 | — (≥8.5) |
| `skills/scorecard_test_skill_instructions_section.md` | 9.0/10 | 2026-10-02 | — (≥8.5) |
| `_helpers/scorecard_test_file_structure_compliance.md` | 8.9/10 | 2026-10-11 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_concurrent_sessions.md` | 8.9/10 | 2026-10-11 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_testing.md` | 8.9/10 | 2026-10-11 | — (≥8.5) |
| `rules/rules_lazy_load/scorecard_test_org.md` | 8.9/10 | 2026-10-11 | — (≥8.5) |
| `rules/scorecard_test_rule_cross_references.md` | 8.9/10 | 2026-10-11 | — (≥8.5) |
| `skills/claude_kaizen/scorecard_test_claude_kaizen_runner.md` | 8.9/10 | 2026-10-06 | — (≥8.5) |
| `skills/scorecard_test_skill_metadata_header.md` | 8.9/10 | 2026-10-11 | — (≥8.5) |
| `skills/scorecard_test_skill_structure_compliance.md` | 8.9/10 | 2026-09-30 | — (≥8.5) |
| `admin/scorecard_test_scorecard_coverage.md` | 8.7/10 | 2026-10-11 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_path_scoped_rules_live.md` | 8.7/10 | 2026-10-11 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_claude_rule_loading_strategy.md` | 8.6/10 | 2026-10-11 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_authoring_agents.md` | 8.4/10 | 2026-10-11 | — (≥8.5) |
| `rules/rules_lazy_load/scorecard_test_lazy_load_coverage.md` | 8.3/10 | 2026-10-11 | • Add failure messages that say how to fix each assertion (27% have one today) |
| `skills/claude_capture_session_prompts/scorecard_test_capture_session_prompts.md` | 8.1/10 | 2026-09-30 | • Add failure messages that say how to fix each assertion (14% have one today)<br>• Add a synthetic bad-input test that proves the check fails when it should |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever a scorecard it covers is created or re-scored.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files.
- **Bump dates:** set a folder's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its scorecard no longer lists it.
- **Template:** this file follows `_templates/scorecard/scorecard_summary.md.template`.
