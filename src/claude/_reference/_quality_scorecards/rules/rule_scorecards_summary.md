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
| 01_essentials | 3 | 7.4/10 | 2026-10-28 | • 💪 **Strongest:** 2 files tied at 7.6/10, `claude_response_standards.md` and `claude_usage_standards.md`<br>• ⚠️ **Weakest:** `guiding_principles.md` (6.9/10) |
| 02_claude_standards | 11 | 6.9/10 | 2026-10-28 | • 💪 **Strongest:** `claude_working_practices.md` (7.9/10)<br>• ⚠️ **Weakest:** `claude_operational_efficiency.md` (5.9/10) |
| 03_authoring_guidelines | 4 | 7.2/10 | 2026-10-28 | • 💪 **Strongest:** `claude_config_metadata.md` (7.7/10)<br>• ⚠️ **Weakest:** `authoring_agents.md` (6.7/10) |
| rules_lazy_load | 1 | 7.0/10 | 2026-10-25 | • 💪 **Only file:** `latency_optimisation.md` (7.0/10) |
| style_guide_standards | 11 | 6.2/10 | 2026-10-25 | • 💪 **Strongest:** `bash.md` (6.8/10)<br>• ⚠️ **Weakest:** `dbt.md` (5.5/10) |
| Non-tiered | 1 | 7.1/10 | 2026-10-25 | • 💪 **Only file:** `aliases.md` (7.1/10) |

---

## 🚀 Recommended next actions

Ranked by impact, highest first, with always-on rules before lazy-load rules.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 🔧 **`claude_operational_efficiency.md`:** add or stop naming the `make disable_mcp` target, and move TODO logging and MCP restarts out | • 🔻 **Score:** 5.9/10 | `02_claude_standards/scorecard_claude_operational_efficiency.md` |
| 2 | • 🔧 **`automation_controls.md`:** state the interval floor and turn cap once each, and confirm or remove `/stop_loop` | • 🔻 **Score:** 6.1/10 | `02_claude_standards/scorecard_automation_controls.md` |
| 3 | • 🔧 **`git.md`:** correct the `git -C` hook-safety claim in `_safe_patterns.md` | • 🔻 **Score:** 6.6/10 | `02_claude_standards/scorecard_git.md` |
| 4 | • 🔧 **`behaviour.md`:** make `_artefact_proposal_gates.md` and `_decision_making.md` agree on whether options follow passed gates | • 🔻 **Score:** 6.9/10 | `02_claude_standards/scorecard_behaviour.md` |
| 5 | • 🔧 **`testing.md`:** fix the dead relative links and the missing `test_aliases_behavior.py` name | • 🔻 **Score:** 6.7/10 | `02_claude_standards/scorecard_testing.md` |

---

## 📄 All scorecards

Sorted by Overall score, highest first.

| Scorecard | Overall | Date Updated | Recommended improvements |
|---|---|---|---|
| `02_claude_standards/scorecard_claude_working_practices.md` | 7.9/10 | 2026-10-25 | • Make the Contents summary on line 16 name all six operational-efficiency topics<br>• Add a test that the index's three pointers resolve and its Contents matches its headings<br>• Record why the index layer is needed |
| `03_authoring_guidelines/scorecard_claude_config_metadata.md` | 7.7/10 | 2026-10-25 | • Change line 60's "up to three more lines" to say which usage fields are required<br>• Update line 72's `path-scoped` definition to match `test_rule_headers.py` lines 345–346<br>• Add a test for line 24's bump-on-edit rule |
| `01_essentials/scorecard_claude_usage_standards.md` | 7.6/10 | 2026-10-25 | • Replace line 11's import-era reason with the file's current job, the directory-structure pointer<br>• Use one path base for the Contents "see" paths on lines 17–19<br>• Split line 11 into one-sentence bullets and give the Contents bullets bold keywords |
| `01_essentials/scorecard_claude_response_standards.md` | 7.6/10 | 2026-10-28 | • Move the Delivery Cadence section to `behaviour.md` or `claude_operational_efficiency.md`, because it governs how Claude works and the rule's own Scope line limits it to how replies look<br>• Define "substantive" inside the rule and make the skip criteria match `response_standards_enforcement.md`, including its under-50-words threshold and its skill-output waiver<br>• Say whether "Wait: get an explicit reply" applies in non-interactive runs (subagents, `/goal`, `/loop`)<br>• Split the semicolon-joined Human-readable format bullet into two child bullets |
| `02_claude_standards/scorecard_mcp_trust_model.md` | 7.4/10 | 2026-10-25 | • Make line 27's trusted GitHub and Jira results agree with line 33's untrusted comments and titles<br>• Change line 59's "data first, instructions second" to match line 19's "data, not instructions"<br>• Say where line 60's suspicious-content audit note should go<br>• Record evidence of need, such as a real injection attempt |
| `02_claude_standards/scorecard_portable_paths.md` | 7.3/10 | 2026-10-25 | • Correct line 23's "all three shipped", since four incidents follow<br>• Extend `test_portable_paths_python.py` to scan `scripts/` as well as `_tests/`<br>• Add a content-regression test for the incident record on lines 21–28<br>• Split line 38 into one-sentence bullets and use British "recognised" on line 28 |
| `03_authoring_guidelines/scorecard_authoring_skills.md` | 7.3/10 | 2026-10-25 | • Resolve line 45's `patterns/` ban against line 47's `reference/patterns/` exception<br>• Update line 31's "~60 lines" to match `_core_standards.md` line 20's instructions exemption<br>• Make the drafts-path guidance agree between `_core_standards.md` line 34 and the hard gates<br>• Add a content-regression test for the 2026-10-01 incident in `_core_standards.md` line 37 |
| `02_claude_standards/scorecard_security.md` | 7.3/10 | 2026-10-25 | • Resolve the trusted and untrusted overlap in `_mcp_trust_model.md` lines 27 and 33<br>• Add the fourth heading, "Reference", to the Contents in `security.md` lines 11–15<br>• Record evidence of need, such as an observed injection attempt or leaked secret<br>• Consider path-scoping `_code_security.md`, which only matters in coding sessions |
| `02_claude_standards/scorecard_claude_plans.md` | 7.3/10 | 2026-10-28 | • Replace the "Ready to proceed to Phase X?" step in `claude_plans.md` with the Next steps format the same section already requires, so the gate prompt has one form<br>• Add a "✅ Right" example next to the "❌ Wrong" one in `claude_plans.md`'s Example section<br>• Merge the two "wait for explicit approval" sentences in `plan_mode_phase_gates.md` (lines 8 and 17) into one<br>• Change "the parent `claude_plans.md`" in `plan_mode_phase_gates.md` and "the parent rule" in `plan_file_format.md` to name the sibling or caller file, since neither is a child of `claude_plans.md` any more |
| `scorecard_aliases.md` | 7.1/10 | 2026-10-25 | • Add the standard metadata header and `applies_to` / `miss_cost` fields to `aliases.md`<br>• Define what the `Ready` and `Testing` statuses mean<br>• Drop the controls-path repetition in lines 17–25, and use British "optimise" on line 10<br>• Add a test that checks `aliases.md` has a metadata header |
| `rules_lazy_load/scorecard_latency_optimisation.md` | 7.0/10 | 2026-10-25 | • Record evidence of need, such as a dated slow or costly run<br>• Replace the per-model catalogue on lines 39–44 with a pointer to the current model docs<br>• Split the prose on lines 14, 30 and 43 into one-sentence bullets, and drop the stray `---` on line 76 |
| `02_claude_standards/scorecard_claude_rule_loading_strategy.md` | 7.0/10 | 2026-10-25 | • Change line 71's `load:` to the real field name, `loading:`<br>• Update `HEADER_LINES` in `test_claude_rule_loading_strategy.py` lines 30–31 to the current 12-line header<br>• Record evidence of need for the placement rules<br>• Split the multi-sentence lines 17, 19 and 92, and give the numbered steps bold keywords |
| `03_authoring_guidelines/scorecard_authoring_rules.md` | 6.9/10 | 2026-10-28 | • Point Pre-Creation question 4 at the `rules/` tier folders and `_rules_lazy_load/`, not at a "full rule list" in `claude_rule_loading_strategy.md`<br>• Replace "~100–150 tokens/session cost" with a pointer to `make audit_rule_usage`, which measures tier sizes<br>• Say in question 2 that a rule in tiers 01–03 with `paths:` frontmatter loads only with matching files, as `authoring_agents.md` does<br>• Merge question 2's three-tier list into question 5's five-folder list, so tier placement is described only once |
| `01_essentials/scorecard_guiding_principles.md` | 6.9/10 | 2026-10-25 | • Align line 17's 200-line target with the 110-line rule limit, or say which files each applies to<br>• Record evidence of need, meeting the bar the rule sets on line 19<br>• Give the child `usage_evidence.md` emoji headings and bold-keyword bullets<br>• Spell out the ROI example on line 22 and what counts as "directly referenced" on line 15 |
| `02_claude_standards/scorecard_behaviour.md` | 6.9/10 | 2026-10-28 | • Make `_artefact_proposal_gates.md` line 12 and `_decision_making.md` line 23 give the same instruction on whether options follow passed gates<br>• Open the Risky actions section with the action to take, e.g. "Confirm before any of these, even on Trivial tasks"<br>• Add a dated incident to the parent or a child that shows each gate is needed<br>• Move the artefact proposal gates behind `paths:` or a read-on-demand pointer, since only authoring sessions need them |
| `style_guide_standards/scorecard_bash.md` | 6.8/10 | 2026-10-25 | • Say whether `local` variables are uppercase too (lines 72 and 78)<br>• Reconcile the relative `shell_utils.sh` path on line 47 with the absolute-path rule on line 87<br>• Replace the literal `~/.claude/` paths on lines 30 and 50, and say what "strict mode" means on line 8 |
| `style_guide_standards/utilities/scorecard_datetime.md` | 6.7/10 | 2026-10-25 | • Change line 44's "Frontmatter fields" to the HTML-comment metadata header<br>• Fix the Contents anchors on lines 18 and 20 so they match the em-dash headings<br>• Record evidence of need, and give the bullets on lines 44–49 and 63–68 bold keywords |
| `03_authoring_guidelines/scorecard_authoring_agents.md` | 6.7/10 | 2026-10-25 | • Update `_core_standards.md` lines 30–32 to the `agents/<group>/<name>/AGENT.md` layout<br>• Make `_decision_tree_and_process.md` line 55 agree with the 5–8 draft eval count<br>• Fix the naming examples in `_core_standards.md` lines 22–25 and the "(below)" pointer on line 30<br>• Add an `applies_to` header so `make audit_rule_usage` can measure it |
| `02_claude_standards/scorecard_testing.md` | 6.7/10 | 2026-10-25 | • Fix the relative links on lines 74–78, which point to a folder that doesn't exist<br>• Replace line 48's `test_aliases_behavior.py`, which isn't in the repo<br>• Extend `test_testing.py` to check link targets, not just the backticked path<br>• Swap the ML examples on lines 39–41 for config-test examples, and use British "behaviour" |
| `02_claude_standards/scorecard_git.md` | 6.6/10 | 2026-10-25 | • Correct `git/_safe_patterns.md` line 18, since `git -C <repo>` still runs that repo's hooks<br>• Make `_commits.md` line 25 and `_concurrent_sessions.md` line 24 agree on `git add -A`<br>• Convert the prose in `_safe_patterns.md` and `_concurrent_sessions.md` line 12 to one-sentence bullets<br>• Update `test_concurrent_sessions.py` line 27's stale `@import` message |
| `style_guide_standards/scorecard_python.md` | 6.5/10 | 2026-10-25 | • Move "Meaningful names" and "No history in names" (lines 35–36) out from under "Constants"<br>• Give the 6 children `_` prefixes, and add a Purpose line to `python/python_environment.md`<br>• Record evidence of need, and add an exception for top-level handlers to the `except` rule on line 50 |
| `style_guide_standards/infra/scorecard_ansible.md` | 6.3/10 | 2026-10-25 | • Make the example on line 84 match its `[provider]_[account/site]_[plugin].yml` pattern<br>• Stop skipping `var-naming[no-role-prefix]` on line 99, since lines 85 and `roles_and_tasks.md` line 71 require the prefix<br>• Remove or create the `secrets_and_inventory.md` that line 25 names, and reference or remove the two orphaned templates<br>• Give the children Purpose lines, and record evidence of need |
| `style_guide_standards/infra/scorecard_docker.md` | 6.3/10 | 2026-10-25 | • Make the multi-stage example in `docker/advanced.md` lines 99–104 switch to a non-root user, as line 51 requires<br>• Reconcile the Docker Hub base-image rule (`fundamentals.md` line 16) with the distroless advice on line 18<br>• Give the children `_` prefixes and Purpose lines, and record evidence of need |
| `style_guide_standards/infra/scorecard_terraform.md` | 6.2/10 | 2026-10-25 | • Split `terraform/structure.md` (145 lines) and `terraform/conventions.md` (142 lines) to fit the 110-line limit<br>• Resolve `conventions.md` line 82's "declare all three" against line 88's optional `default`<br>• Give the children `_` prefixes and Purpose lines, and record evidence of need |
| `style_guide_standards/utilities/scorecard_mermaid.md` | 6.2/10 | 2026-10-25 | • Widen the `paths:` trigger, or narrow the scope on line 16, so the guide loads with the files it governs<br>• Remove or add the "reference example" that line 21 says `advanced.md` holds<br>• Give the children `_` prefixes and Purpose lines, and record evidence of need |
| `style_guide_standards/utilities/scorecard_makefile.md` | 6.2/10 | 2026-10-25 | • Indent the recipe examples with tabs, since space-indented recipes fail with "missing separator"<br>• Resolve the echo ban (`variables_operators_and_commands.md` line 28) against the `@echo` example on lines 57–58<br>• Use `:=` in the `SHELL` example on line 21, as lines 40–44 recommend<br>• Give the children `_` prefixes, Purpose lines and emoji headings |
| `02_claude_standards/scorecard_automation_controls.md` | 6.1/10 | 2026-10-25 | • State the interval floor once on line 27, without the conflicting sub-minute clause<br>• State the 20-turn cap on line 48 once<br>• Confirm or remove `/stop_loop` on line 31<br>• Record the basis for the 5-minute, 2-hour, 30-minute and 12-item thresholds<br>• Consider path-scoping or lazy-loading it, since the commands never auto-trigger |
| `02_claude_standards/scorecard_claude_operational_efficiency.md` | 5.9/10 | 2026-10-25 | • Add the `make disable_mcp` target, or stop naming it in `_mcp_server_toggling.md` line 8<br>• Move TODO logging and MCP restarts out from under "operational efficiency"<br>• Record evidence of need, including a source for `_turn_budgets.md` line 12<br>• Path-scope or lazy-load the narrow children that load every session |
| `style_guide_standards/scorecard_airflow.md` | 5.7/10 | 2026-10-25 | • Make the parent and `airflow/best_practices.md` agree on Variables vs `config.yaml`, retries and retry delay<br>• Move callbacks to `includes/` or change `dag_design.md` line 18, so the two agree<br>• Replace the deprecated `schedule_interval` and `execution_date` with `schedule` and `logical_date`<br>• Replace the literal `~/.claude/` paths, and give the bullets bold keywords |
| `style_guide_standards/scorecard_sql.md` | 5.7/10 | 2026-10-25 | • Fix `sql.md` line 49's advice to quote Snowflake identifiers with backticks, since Snowflake uses double quotes<br>• Update the SQLFluff codes on lines 47–49 and in `sql/sqlfluff.md` to current, correctly described rules<br>• Bring the `sql/cte_style_guide.md` examples in line with `sql/formatting.md` (no `SELECT *`, trailing commas or bare `JOIN`)<br>• Remove the duplicate child index, and give the children Purpose lines |
| `style_guide_standards/scorecard_dbt.md` | 5.5/10 | 2026-10-25 | • Make the parent's model layers and name prefixes match `dbt/model_organisation.md` and `dbt/naming_conventions.md`<br>• Replace the non-existent `dbt lineage` (lines 38 and 124) and complete `dbt docs generate` (lines 105 and 126)<br>• Fix line 78's uniqueness advice, which names a column-order test<br>• Split the parent to fit 110 lines, remove the duplicate child index and the literal `~/.claude/` paths |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever a scorecard it covers is created or re-scored.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files.
- **Bump dates:** set a tier's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its scorecard no longer lists it.
- **Template:** this file follows `_templates/scorecard/scorecard_summary.md.template`.
