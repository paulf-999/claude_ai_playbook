# 📊 Test Scorecards Summary

**Purpose:** One-glance rollup of every test scorecard's Overall score — see which tests need attention without opening each file.

---

## 📋 Current scores

- **Scored:** 49 test files, average 8.6/10.
- **Below 8.5:** 21 tests, each with recommended improvements.
- **Order:** one table per `_tests/` folder, sorted by Overall score, highest first.

### admin

| Scorecard | Overall | Recommended improvements |
|---|---|---|
| `admin/scorecard_test_scorecard_dates.md` | 9.3/10 | — (≥8.5) |

### agents

| Scorecard | Overall | Recommended improvements |
|---|---|---|
| `agents/scorecard_test_agent_metadata_header.md` | 9.0/10 | — (≥8.5) |

### hooks

| Scorecard | Overall | Recommended improvements |
|---|---|---|
| `hooks/response_standards/scorecard_test_style_guide_response_standards_flags.md` | 9.3/10 | — (≥8.5) |
| `hooks/response_standards/scorecard_test_style_guide_response_standards_inject.md` | 9.3/10 | — (≥8.5) |
| `hooks/response_standards/scorecard_test_style_guide_response_standards_waivers.md` | 9.3/10 | — (≥8.5) |
| `hooks/scorecard_test_hook_registry_utils.md` | 9.3/10 | — (≥8.5) |
| `hooks/enforcement/scorecard_test_enforcement_writing_style.md` | 9.3/10 | — (≥8.5) |
| `hooks/enforcement/scorecard_test_enforcement_mcp_stale_settings.md` | 9.1/10 | • None blocking |
| `hooks/enforcement/scorecard_test_enforcement_naming_convention.md` | 9.1/10 | • None blocking |

### rules

| Scorecard | Overall | Recommended improvements |
|---|---|---|
| `rules/02_claude_standards/scorecard_test_test_metadata.md` | 9.3/10 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_test_score_floor.md` | 9.3/10 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_claude_config_metadata.md` | 9.1/10 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_plan_mode_phase_gates.md` | 9.0/10 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_skill_domains.md` | 9.0/10 | — (≥8.5) |
| `rules/05_lazy_load/scorecard_test_lazy_load_rule_structure.md` | 9.0/10 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_artefact_proposal_gates.md` | 8.9/10 | — (≥8.5) |
| `rules/02_claude_standards/scorecard_test_concurrent_sessions.md` | 8.7/10 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_authoring_agents.md` | 8.6/10 | — (≥8.5) |
| `rules/03_authoring_guidelines/scorecard_test_authoring_skills.md` | 8.6/10 | — (≥8.5) |
| `rules/04_claude_reference/scorecard_test_claude_operational_efficiency.md` | 8.6/10 | — (≥8.5) |
| `rules/05_lazy_load/scorecard_test_automation_controls.md` | 8.6/10 | — (≥8.5) |
| `rules/04_claude_reference/scorecard_test_claude_rule_loading_strategy.md` | 8.4/10 | • Add a synthetic bad-input test that proves the check fails when it should |
| `rules/02_claude_standards/scorecard_test_always_on_reachability.md` | 8.3/10 | • Split the test by concept to bring raw complexity (7) down to 3 or less |
| `rules/05_lazy_load/scorecard_test_lazy_load_coverage.md` | 8.3/10 | • Add failure messages that say how to fix each assertion (27% have one today) |
| `rules/01_essentials/scorecard_test_writing_style.md` | 8.3/10 | • Add test functions and assertions toward 10+ and 15+ (now 7 and 14)<br>• Add a synthetic bad-input test that proves the check fails when it should |
| `rules/scorecard_test_rules_structure.md` | 8.3/10 | • Split the test by concept to bring raw complexity (6) down to 3 or less |
| `rules/02_claude_standards/scorecard_test_git.md` | 8.1/10 | • Add test functions and assertions toward 10+ and 15+ (now 5 and 6)<br>• Add a synthetic bad-input test that proves the check fails when it should |
| `rules/02_claude_standards/scorecard_test_security_guardrails.md` | 8.1/10 | • Add test functions and assertions toward 10+ and 15+ (now 6 and 6)<br>• Add a synthetic bad-input test that proves the check fails when it should |
| `rules/03_authoring_guidelines/scorecard_test_authoring_rules.md` | 8.1/10 | • Add test functions and assertions toward 10+ and 15+ (now 5 and 6)<br>• Add a synthetic bad-input test that proves the check fails when it should |
| `rules/05_lazy_load/scorecard_test_latency_optimisation.md` | 8.1/10 | • Add test functions and assertions toward 10+ and 15+ (now 4 and 6)<br>• Add a synthetic bad-input test that proves the check fails when it should |
| `rules/scorecard_test_aliases_behavior.md` | 8.1/10 | • Add test functions and assertions toward 10+ and 15+ (now 5 and 7)<br>• Add a synthetic bad-input test that proves the check fails when it should |
| `rules/01_essentials/scorecard_test_rule_directory_organisation.md` | 8.0/10 | • Split the test by concept to bring raw complexity (4) down to 3 or less<br>• Add test functions and assertions toward 10+ and 15+ (now 11 and 13)<br>• Add a synthetic bad-input test that proves the check fails when it should |
| `rules/02_claude_standards/scorecard_test_portable_paths.md` | 7.7/10 | • Split the test by concept to bring raw complexity (7) down to 3 or less<br>• Update the header quality score from 9/10 to reflect the current counts<br>• Add test functions and assertions toward 10+ and 15+ (now 9 and 13) |
| `rules/01_essentials/scorecard_test_skill_authoring_gate.md` | 7.7/10 | • Split the test by concept to bring raw complexity (5) down to 3 or less<br>• Fix the style gaps and set `Python style compliant: Yes`<br>• Turn the manual-review skips into failures, or `xfail` with a tracked reason, so real gaps can't pass quietly |
| `rules/02_claude_standards/scorecard_test_decision_making.md` | 7.7/10 | • Add test functions and assertions toward 10+ and 15+ (now 5 and 6)<br>• Add a synthetic bad-input test that proves the check fails when it should<br>• Fix the module docstring to name `02_claude_standards/behaviour/_decision_making.md` |
| `rules/02_claude_standards/scorecard_test_testing.md` | 7.6/10 | • Add test functions and assertions toward 10+ and 15+ (now 5 and 7)<br>• Fix the style gaps and set `Python style compliant: Yes`<br>• Add a synthetic bad-input test that proves the check fails when it should |
| `rules/01_essentials/scorecard_test_guiding_principles.md` | 7.6/10 | • Add test functions and assertions toward 10+ and 15+ (now 3 and 3)<br>• Replace the `< 20 imports` limit with a check tied to a documented budget |

### settings

| Scorecard | Overall | Recommended improvements |
|---|---|---|
| `settings/scorecard_test_settings.md` | 9.3/10 | — (≥8.5) |
| `settings/scorecard_test_aliases.md` | 9.1/10 | — (≥8.5) |

### skills

| Scorecard | Overall | Recommended improvements |
|---|---|---|
| `skills/scorecard_test_skill_metadata_header.md` | 9.1/10 | — (≥8.5) |
| `skills/scorecard_test_skill_structure_compliance.md` | 8.9/10 | — (≥8.5) |
| `skills/scorecard_test_no_orphaned_skill_files.md` | 8.3/10 | • Add failure messages that say how to fix each assertion (16% have one today)<br>• Split the test by concept to bring raw complexity (5) down to 3 or less |
| `skills/claude_capture_session_prompts/scorecard_test_capture_session_prompts.md` | 8.1/10 | • Add failure messages that say how to fix each assertion (14% have one today)<br>• Add a synthetic bad-input test that proves the check fails when it should |
| `skills/confluence_create_page/scorecard_test_confluence_create_page_handler.md` | 7.7/10 | • Add failure messages that say how to fix each assertion (1% have one today)<br>• Split the test by concept to bring raw complexity (6) down to 3 or less<br>• Confirm the handler still mirrors what SKILL.md tells Claude to do, or move the handler into the skill so the test covers real behaviour |
| `skills/jira_create/scorecard_test_jira_create_handler.md` | 7.4/10 | • Add failure messages that say how to fix each assertion (0% have one today)<br>• Fix the style gaps and set `Python style compliant: Yes`<br>• Confirm the handler still mirrors what SKILL.md tells Claude to do, or move the handler into the skill so the test covers real behaviour |
| `skills/confluence_create_page/scorecard_test_confluence_create_page_timeout.md` | 6.9/10 | • Add failure messages that say how to fix each assertion (0% have one today)<br>• Split the test by concept to bring raw complexity (6) down to 3 or less<br>• Add test functions and assertions toward 10+ and 15+ (now 9 and 19)<br>• Add a synthetic bad-input test that proves the check fails when it should<br>• Confirm the handler still mirrors what SKILL.md tells Claude to do, or move the handler into the skill so the test covers real behaviour |

### _tests root

| Scorecard | Overall | Recommended improvements |
|---|---|---|
| `scorecard_test_file_structure_validator.md` | 9.3/10 | — (≥8.5) |
| `scorecard_test_hook_metadata_header.md` | 9.0/10 | — (≥8.5) |
| `scorecard_test_file_structure_compliance.md` | 8.9/10 | — (≥8.5) |

---

## 🔄 Keeping this current

- **Update in the same commit:** whenever a test scorecard is created or re-scored, update its row here.
- **Improvements:** copied from each scorecard's own **Recommended improvements** list — edit both together.
