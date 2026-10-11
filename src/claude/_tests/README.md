# 🧪 Tests

Tests verify that enforcement hooks and rule files behave as intended.
Run the whole suite at once — the tests check whichever config `CLAUDE_CONFIG_DIR` points at.

```bash
# Playbook repo: from the repo root, where pytest.ini adds coverage and the install tests
CLAUDE_CONFIG_DIR=$PWD/src/claude python3 -m pytest src/claude/_tests

# Live config: from the config folder
cd ~/.claude && python3 -m pytest _tests
```

Each table's **Quality**, **Created**, **Updated**, and **Version** columns are read directly from
the test file's own metadata header — see `testing.md`'s Test Metadata Standard section for the
format and scoring rubric.

**Utility (not a scored test):** `_skill_orphans.py` — pure detectors for orphaned skill files, broken `reference/` links and eager imports.

**Utility (not a scored test):** `_gate_fixtures.py` — loads the skill authoring gate linter and builds fake skills for its walk and run tests.

**Utility (not a scored test):** `_resolved_rule.py` — reads a parent rule with every child it imports or points to on demand inlined.

**Utility (not a scored test):** `_rule_reachability.py` — reports files under `rules/` that would load wrongly (READMEs, `_lazy_load/` folders, `@import` lines, unscoped `04_path_scoped/` files) and Read-on-demand pointers that lead nowhere.

**Utility (not a scored test):** `_file_structure_validator.py` — the file-structure scanner, and the `--check` mode the naming hook calls for one new path.

**Utility (not a scored test):** `_shared_paths.py` — resolves `CLAUDE_DIR` (via `CLAUDE_CONFIG_DIR`,
default `~/.claude`) plus the handful of path constants (`CLAUDE_MD`, `ALIASES_FILE`,
`SETTINGS_FILE`, `SKILLS_DIR`, `HOOKS_DIR`, `RULES_DIR`) that were independently redeclared with
identical values across multiple test files. Single-use, test-specific path constants stay local
to their own test file.

---

## 📁 `admin/`

Tests for the quality scorecards in `_admin/_quality_scorecards/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_scorecard_coverage.py` | Every hook, agent and skill has a scorecard on its folder's dimensions, and the summaries add up | 9/10 | 2026-10-01 | 2026-10-06 | 1.1.0 |
| `test_scorecard_dates.py` | Validates the per-row Date Updated column in every quality scorecard table | 9/10 | 2026-10-01 | 2026-10-02 | 1.0.1 |

---

## 📁 `agents/`

Tests for custom sub-agents in `agents/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_agent_metadata_header.py` | Validates the agent metadata header defined in _claude_config_metadata.md | 9/10 | 2026-09-29 | 2026-10-02 | 1.0.2 |
| `test_agent_triggers.py` | No agent trigger competes with a skill for the same request | 9/10 | 2026-10-01 | 2026-10-10 | 1.0.1 |

---

## 📁 `docs/`

Tests for the playbook repo's own `README.md` and `docs/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_docs_local_links.py` | Checks every local link in README.md and docs/ points at a file that exists | 9/10 | 2026-10-04 | 2026-10-04 | 1.0.0 |

---

## 📁 `hooks/`

Tests for Claude Code hook scripts in `~/.claude/hooks/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_hook_registry_utils.py` | `settings.json` hook registry — known events, command hooks, no duplicates, every referenced hook file exists, and every hook file is registered or listed in `RESERVED_HOOKS` | 9/10 | 2026-08-28 | 2026-10-10 | 2.3.3 |

**Archived:** `test_auto_rotate_todo.py` moved to `_tests/_archived/` (2026-09-18) — `rotate_todo.sh` and `hook_auto_rotate_todo.sh` were never built despite a stale "Ready for production" claim in `TODO.md`; see the file's own archival note.

**Utility (not a scored test):** `hook_test_utils.py` — shared `run_hook()` helper, pipes a JSON payload to a hook and returns the result.

### `hooks/enforcement/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_enforcement_mcp_stale_settings.py` | `hook_enforcement_mcp_stale_settings.sh` — warns once when the disabled MCP servers change mid-session | 9/10 | 2026-09-18 | 2026-10-01 | 2.0.3 |
| `test_enforcement_naming_convention.py` | `hook_enforcement_naming_convention.sh` — denies new config files whose names break the compliance checks, and lets everything else through | 9/10 | 2026-08-28 | 2026-10-10 | 2.1.1 |
| `test_enforcement_markdown_location.py` | `hook_enforcement_markdown_location.sh` — flags stray markdown at the config root, using the real stdin payload | 9/10 | 2026-08-28 | 2026-10-10 | 3.0.0 |

### `hooks/response_standards/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_style_guide_response_standards_flags.py` | `hook_style_guide_response_standards.sh` (reserved) — flags a missing Summary, offer line or timing footer, and text after the footer | 9/10 | 2026-10-01 | 2026-10-01 | 1.0.0 |
| `test_style_guide_response_standards_waivers.py` | `hook_style_guide_response_standards.sh` (reserved) — skips short answers, skill output, code blocks, errors and plan-mode output | 9/10 | 2026-10-01 | 2026-10-01 | 1.0.0 |
| `test_style_guide_response_standards_inject.py` | `hook_style_guide_response_standards_inject.sh` — per-turn salience injection, timestamp, waiver handling | 9/10 | 2026-09-07 | 2026-10-02 | 2.1.0 |

---

## 📁 `rules/`

Tests for structural properties and behavioral compliance of files in `~/.claude/rules/` and `~/.claude/_rules_lazy_load/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_rules_structure.py` | Per-file format across all `rules/` files — line limits, H1 and H2 heading emoji, trailing newlines, and no Related or unearned Contents sections | 9/10 | 2026-08-28 | 2026-10-10 | 2.5.2 |
| `test_rules_structure_layout.py` | Where `rules/` files live, every import in `CLAUDE.md` and `rules/` resolves | 9/10 | 2026-10-01 | 2026-10-10 | 3.0.0 |

### `rules/01_essentials/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_guiding_principles.py` | CLAUDE.md's imports follow guiding_principles.md — no lazy-load imports, a purpose comment on each, few, unique, always-on tiers in order | 9/10 | 2026-08-28 | 2026-10-06 | 2.2.0 |
| `test_rule_directory_organisation.py` | `01_essentials/` holds its expected files and folders, and tiers 01–03 follow the parent-and-children layout (`_` prefix, 2+ children, parent beside each folder) | 9/10 | 2026-08-28 | 2026-10-06 | 2.3.0 |
| `test_writing_style.py` | `writing_style.md` keeps its tables rule, one sentence per bullet, British spelling, underscore file-name dates and its multifile child | 9/10 | 2026-08-28 | 2026-10-06 | 2.1.0 |

### `rules/02_claude_standards/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_always_on_reachability.py` | Every file under `rules/` loads the way its folder says — no README, `_lazy_load/` folder, `@import` or unscoped `04_path_scoped/` file — and every 'Read on demand' pointer | 9/10 | 2026-09-18 | 2026-10-11 | 3.2.2 |
| `test_artefact_proposal_gates.py` | The three artefact proposal gates — naming, placement, duplication | 9/10 | 2026-08-28 | 2026-10-06 | 2.2.0 |
| `test_automation_controls.py` | Turn budgets and gates for `/loop`, `/batch`, `/goal` in `_automation_controls.md` are documented and reasonable | 9/10 | 2026-09-16 | 2026-10-11 | 1.2.0 |
| `test_concurrent_sessions.py` | `git/_concurrent_sessions.md` keeps its incident record and shared-working-tree safety guidance | 9/10 | 2026-09-21 | 2026-10-10 | 2.0.0 |
| `test_decision_making.py` | `_decision_making.md` keeps each clause of the intentionality gate, and the rules it defers to still exist and agree | 9/10 | 2026-08-28 | 2026-10-06 | 2.1.0 |
| `test_git.py` | `git.md` keeps each git rule, imports its children, and its branch-name pattern matches its own examples | 9/10 | 2026-08-28 | 2026-10-06 | 2.1.0 |
| `test_plan_mode_phase_gates.py` | Plan-mode phase gates, plan-approval exceptions, saving each approved plan as Active, and the four plan statuses with who sets each | 9/10 | 2026-09-16 | 2026-10-11 | 3.4.0 |
| `test_portable_paths_hooks.py` | Hooks resolve the config dir from their own location — no hardcoded `~/.claude/` file operations or guard substrings | 9/10 | 2026-09-18 | 2026-10-02 | 2.0.1 |
| `test_portable_paths_python.py` | Python test files use `CLAUDE_DIR` — no `.expanduser()` outside `_shared_paths.py`, home-directory constants or one-convention import prefixes | 9/10 | 2026-09-18 | 2026-10-02 | 2.0.1 |
| `test_security_guardrails.py` | `_security_guardrails.md` keeps each guardrail, and settings.json allows none of the wildcards it forbids | 9/10 | 2026-08-28 | 2026-10-06 | 2.1.0 |
| `test_claude_operational_efficiency.py` | `claude_operational_efficiency.md` keeps its 9 sections, loads exactly its 6 children with no orphans, leaves no stale lazy copies, and keeps its key phrases | 9/10 | 2026-09-30 | 2026-10-11 | 1.3.0 |

### `rules/03_authoring_guidelines/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_authoring_rules.py` | `authoring_rules.md` keeps its checklist, steps and gates, and every file it points authors to exists | 9/10 | 2026-08-28 | 2026-10-10 | 2.3.0 |
| `test_authoring_skills.py` | `authoring_skills.md` and its children: SKILL.md's six sections, the frontmatter example, contract fields matching the checklist, and trigger design | 9/10 | 2026-09-16 | 2026-10-10 | 4.2.2 |
| `test_authoring_skills_maturity.py` | `authoring_skills.md`'s maturity table matches the checklist and complexity formula, plus scope anti-patterns and low-maintenance principles | 9/10 | 2026-10-01 | 2026-10-10 | 1.1.2 |
| `test_claude_config_metadata.py` | Every rule opens with the three-line version, created and updated metadata header | 9/10 | 2026-09-28 | 2026-10-10 | 2.4.0 |
| `test_rule_headers.py` | Validates the rule-only `applies_to`, `miss_cost` and `loading` headers defined in _claude_config_metadata.md | 9/10 | 2026-10-01 | 2026-10-10 | 1.9.1 |
| `test_skill_domains.py` | Keeps skill_domains.yaml and the real skills/ layout in step | 9/10 | 2026-09-30 | 2026-10-02 | 1.0.3 |

### `rules/05_lazy_load/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_claude_rule_loading_strategy.py` | The five-folder table matches the real `rules/` and `_rules_lazy_load/` folders, its example files exist, and CLAUDE.md imports no rules, matching each tier's loading claim; placement uses measured usage, not 70% | 9/10 | 2026-09-30 | 2026-10-10 | 2.1.5 |
| `test_latency_optimisation.py` | `latency_optimisation.md` keeps effort as the lever, never gives a temperature above 1, and keeps its measure-first steps | 9/10 | 2026-09-17 | 2026-10-10 | 2.1.2 |
| `test_lazy_load_coverage.py` | Every `_rules_lazy_load/` file is reachable from at least one hook (direct or via a parent index file) | 9/10 | 2026-09-16 | 2026-10-11 | 2.5.3 |
| `test_lazy_load_rule_structure.py` | The 14 rules once lacking a dedicated test keep their metadata header, Purpose line, key sections, linked child pages, working links and accurate Contents | 9/10 | 2026-10-01 | 2026-10-11 | 1.6.0 |
| `test_path_scoped_rules.py` | Path-scoped rules in `rules/` carry no `@` imports, `rules/` holds real files not links, and every `04_path_scoped/` file has `paths:` | 9/10 | 2026-10-01 | 2026-10-10 | 2.3.0 |
| `test_authoring_agents.py` | `authoring_agents.md` is always-on and points to each of its 5 on-demand children, which are present and well-formed | 9/10 | 2026-09-28 | 2026-10-10 | 2.2.2 |
| `test_lazy_load_triggers.py` | Validates that every lazy rule has something that makes Claude load it | 9/10 | 2026-10-01 | 2026-10-10 | 1.7.2 |
| `test_org.py` | Organisation-specific terms stay inside _rules_lazy_load/org/ and never leak into shared files | 9/10 | 2026-10-01 | 2026-10-10 | 1.3.2 |
| `test_path_scoped_rules_live.py` | Proves in a live session that a `paths:` rule loads when, and only when, a matching file is read | 9/10 | 2026-10-01 | 2026-10-10 | 1.2.1 |
| `test_test_metadata.py` | Every test's metadata header, in `_tests/` and the repo's `src/sh/claude/_tests/`, is complete, in order and well formed (banners, dates, semver, scores) | 9/10 | 2026-10-01 | 2026-10-10 | 1.3.1 |
| `test_test_quality_score.py` | Every test header's quality score matches the band its own test-function and assertion counts support | 9/10 | 2026-10-02 | 2026-10-02 | 1.0.0 |
| `test_test_score_floor.py` | Every test, in `_tests/` and the repo's `src/sh/claude/_tests/`, meets quality 9, complexity 7 and style Yes, with no exemptions, and the minimums match `_test_metadata.md` | 9/10 | 2026-10-01 | 2026-10-10 | 2.2.1 |
| `test_testing.py` | Every enforcement hook has a test (aspect splits allowed), no orphaned hook tests, and testing.md's pointers exist | 9/10 | 2026-08-28 | 2026-10-10 | 1.4.2 |

---

## 📁 `scripts/`

Tests for the maintenance scripts in `_scripts/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_audit_claude_component_root.py` | Validates how audit_claude_component.py chooses the folder it scans | 9/10 | 2026-10-01 | 2026-10-02 | 1.0.2 |
| `test_audit_plans.py` | `audit_plans.py` lists saved plans by status from `_plans/` and its status folders, flags stale Active plans, and counts plans and drafts to file | 9/10 | 2026-10-11 | 2026-10-11 | 2.0.0 |
| `test_audit_rule_usage.py` | Validates audit_rule_usage.py against small fixture rules and transcripts | 9/10 | 2026-10-01 | 2026-10-10 | 1.10.1 |
| `test_clean_plans.py` | `clean_plans.py` files saved plans into `_plans/<status>/` by their status line (or phase table), files drafts into `plans/draft/` or `plans/archive/` by age, never overwrites, and runs without asking during `make install` | 9/10 | 2026-10-02 | 2026-10-11 | 2.1.0 |
| `test_script_naming.py` | Validates that every script under _scripts/ follows the script naming pattern | 9/10 | 2026-10-02 | 2026-10-06 | 1.1.0 |

---

## 📁 `settings/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_aliases.py` | Each `aliases.md` entry is complete, well formed and unique, its links and controls note stay in sync, and core aliases stay documented | 9/10 | 2026-08-28 | 2026-10-11 | 2.2.3 |
| `test_settings.py` | `settings.json` permission structure, security denies, no broad destructive allows and no real secrets | 9/10 | 2026-08-28 | 2026-10-02 | 1.2.1 |

**Merged (2026-10-01):** `rules/test_aliases_behavior.py` — its unique checks moved into `settings/test_aliases.py`, so one test covers `aliases.md`.

**Removed (2026-09-18):** `settings/test_aliases_behavior.py` — written to run as a standalone script (per its own docstring/README), not as native pytest: 3 of its 5 functions required positional arguments pytest couldn't supply (collection errors), and the other 2 used `print`/`return` instead of `assert`, so they never actually failed regardless of outcome. `rules/test_aliases_behavior.py` already covers "aliases are documented and functional" with real assertions. **Lost, not replaced:** the skill/command-existence and convention-documentation checks this file's logic described but never actually enforced as pytest.

---

## 📁 `skills/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_skill_structure_compliance.py` | Every installed skill passes the skill authoring gate's crawl checks, and each check is proven to fire | 9/10 | 2026-08-28 | 2026-10-10 | 2.0.4 |
| `test_no_orphaned_skill_files.py` | Every skill file is referenced somewhere in its skill, every `reference/` link in SKILL.md exists, and no SKILL.md @-imports a file | 9/10 | 2026-09-19 | 2026-10-02 | 2.0.1 |
| `test_skill_authoring_gate_walk.py` | The gate linter's walk checks (W1–W6) fail or warn as intended on fake skills | 9/10 | 2026-10-01 | 2026-10-02 | 1.1.0 |
| `test_skill_authoring_gate_run.py` | The gate linter's run checks (R2–R4) on fake skills, and failures block while judgement calls only warn | 9/10 | 2026-10-01 | 2026-10-05 | 1.1.1 |
| `test_skill_index_versions.py` | Every skill group README lists each of its skills at the version in that skill's SKILL.md header | 9/10 | 2026-10-05 | 2026-10-05 | 1.0.0 |
| `test_skill_instructions_section.py` | Every SKILL.md must carry its own must-follow instructions for Claude | 9/10 | 2026-10-01 | 2026-10-10 | 2.2.3 |
| `test_skill_metadata_header.py` | Validates the skill metadata header defined in _claude_config_metadata.md | 9/10 | 2026-09-28 | 2026-10-02 | 1.0.3 |

### `skills/claude_capture_session_prompts/`

Tests for the skill's own script, `capture_session_prompts.py`, which lives in the skill folder.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_capture_session_prompts.py` | The history file resolves from `CLAUDE_CONFIG_DIR`, output goes to `~/_sessions/` with a date-first name, and the categories and markdown match the skill's docs | 9/10 | 2026-09-30 | 2026-10-06 | 1.1.0 |

### `skills/claude_kaizen/`

Tests for the skill's eval scorer, `evals/runner.py`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_claude_kaizen_runner.py` | Tests for claude_kaizen's evals/runner.py, the before/after eval scorer | 9/10 | 2026-10-02 | 2026-10-06 | 1.2.0 |

### `skills/confluence_create_page/`

Behavioral tests for a code-backed skill — `confluence_create_page_handler.py` lives
alongside these tests and is imported directly via a relative import.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_confluence_create_page_handler.py` | The handler's title, space, pattern and section validators, including their boundaries | 9/10 | 2026-08-28 | 2026-10-02 | 2.0.2 |
| `test_confluence_create_page_phases.py` | The handler's publish phases, each failure mode's error, and the end-to-end flow, with Confluence mocked | 9/10 | 2026-10-01 | 2026-10-02 | 1.0.2 |
| `test_confluence_create_page_timeout.py` | The timeout wrapper on a live call — the dialog, each answer, draft preservation, the 6-minute cap, errors and closed input | 9/10 | 2026-08-28 | 2026-10-06 | 2.0.3 |
| `test_confluence_create_page_timeout_options.py` | Timeout argument parsing, the dialog's wording, how each answer resolves, and that drafts go to `~/claude/_drafts/confluence/YYYY_MM_DD_<slug>.md` | 9/10 | 2026-10-01 | 2026-10-06 | 2.0.0 |

### `skills/jira_create/`

Behavioral tests for a code-backed skill — `jira_create_handler.py` lives alongside
these tests and is imported directly via a relative import.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_jira_create_handler.py` | Validation, phase orchestration, and mocked MCP error handling in the handler | 9/10 | 2026-09-19 | 2026-10-02 | 1.0.3 |

---

## 📁 Top level

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_file_structure_compliance.py` | Every file in the real Claude config passes the file-structure scan, checked area by area | 9/10 | 2026-08-28 | 2026-10-10 | 3.0.0 |
| `test_file_structure_validator.py` | The file-structure scanner flags bad names and skips auto-generated, hidden and exempt files | 9/10 | 2026-10-01 | 2026-10-10 | 1.3.1 |
| `test_rule_reachability.py` | The native-load detector flags READMEs, `_lazy_load/` folders, imports, unscoped path-scoped files and broken pointers under `rules/`, on fake rule trees | 9/10 | 2026-09-18 | 2026-10-10 | 3.2.0 |
| `test_hook_metadata_header.py` | Validates the hook metadata header defined in _claude_config_metadata.md | 9/10 | 2026-09-29 | 2026-09-30 | 1.0.0 |

---

## 📐 When to add a test

Per `rules/02_claude_standards/behaviour.md` — adding or modifying an **enforcement hook** requires a corresponding test.
Instructional rules (files Claude reads but no mechanical hook fires) do not require tests; structural quality is covered by `test_rules_structure.py`.
