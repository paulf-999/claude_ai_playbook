# 🧪 Tests

Tests verify that enforcement hooks and rule files behave as intended.
Run from within each subdirectory using `pytest`.

```bash
cd ~/.claude/_tests/hooks && pytest -v
cd ~/.claude/_tests/rules && pytest -v
```

Each table's **Quality**, **Created**, **Updated**, and **Version** columns are read directly from
the test file's own metadata header — see `testing.md`'s Test Metadata Standard section for the
format and scoring rubric.

**Utility (not a scored test):** `_skill_orphans.py` — pure detectors for orphaned skill files, broken `reference/` links and eager imports.

**Utility (not a scored test):** `_gate_fixtures.py` — loads the skill authoring gate linter and builds fake skills for its walk and run tests.

**Utility (not a scored test):** `_resolved_rule.py` — reads a parent rule with every child it imports or points to on demand inlined.

**Utility (not a scored test):** `_rule_reachability.py` — walks the `@import` chains from `CLAUDE.md` and reports broken imports and orphaned rule files.

**Utility (not a scored test):** `_file_structure_validator.py` — the file-structure scanner, and the `--check` mode the naming hook calls for one new path.

**Utility (not a scored test):** `_shared_paths.py` — resolves `CLAUDE_DIR` (via `CLAUDE_CONFIG_DIR`,
default `~/.claude`) plus the handful of path constants (`CLAUDE_MD`, `ALIASES_FILE`,
`SETTINGS_FILE`, `SKILLS_DIR`, `HOOKS_DIR`, `RULES_DIR`) that were independently redeclared with
identical values across multiple test files. Single-use, test-specific path constants stay local
to their own test file.

---

## 📁 `hooks/`

Tests for Claude Code hook scripts in `~/.claude/hooks/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_hook_registry_utils.py` | `settings.json` hook registry — known events, command hooks, no duplicates, every referenced hook file exists, and every hook file is registered or listed in `RESERVED_HOOKS` | 9/10 | 2026-08-28 | 2026-10-01 | 2.1.0 |

**Archived:** `test_auto_rotate_todo.py` moved to `_tests/_archived/` (2026-09-18) — `rotate_todo.sh` and `hook_auto_rotate_todo.sh` were never built despite a stale "Ready for production" claim in `TODO.md`; see the file's own archival note.

**Utility (not a scored test):** `hook_test_utils.py` — shared `run_hook()` helper, pipes a JSON payload to a hook and returns the result.

### `hooks/enforcement/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_enforcement_mcp_stale_settings.py` | `hook_enforcement_mcp_stale_settings.sh` — warns once when the disabled MCP servers change mid-session | 9/10 | 2026-09-18 | 2026-10-01 | 2.0.1 |
| `test_enforcement_naming_convention.py` | `hook_enforcement_naming_convention.sh` — denies new config files whose names break the compliance checks, and lets everything else through | 9/10 | 2026-08-28 | 2026-10-01 | 2.0.1 |
| `test_enforcement_writing_style.py` | `hook_enforcement_writing_style.sh` — flags stray markdown at the config root and badly named `_reference/` files, using the real stdin payload | 9/10 | 2026-08-28 | 2026-10-01 | 2.0.0 |

### `hooks/response_standards/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_style_guide_response_standards_flags.py` | `hook_style_guide_response_standards.sh` (reserved) — flags a missing Summary, offer line or timing footer, and text after the footer | 9/10 | 2026-10-01 | 2026-10-01 | 1.0.0 |
| `test_style_guide_response_standards_waivers.py` | `hook_style_guide_response_standards.sh` (reserved) — skips short answers, skill output, code blocks, errors and plan-mode output | 9/10 | 2026-10-01 | 2026-10-01 | 1.0.0 |
| `test_style_guide_response_standards_inject.py` | `hook_style_guide_response_standards_inject.sh` — per-turn salience injection, timestamp, waiver handling | 9/10 | 2026-09-07 | 2026-10-01 | 2.0.2 |

---

## 📁 `rules/`

Tests for structural properties and behavioral compliance of files in `~/.claude/_rules/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_rules_structure.py` | Per-file format across all `_rules/` files — line limits, H1 and H2 heading emoji, trailing newlines, and no Related or unearned Contents sections | 9/10 | 2026-08-28 | 2026-10-01 | 2.0.0 |
| `test_rules_structure_layout.py` | Where `_rules/` files live, every import in `CLAUDE.md` and `_rules/` resolves, tier order, and no import chain reaches `_reference/` | 9/10 | 2026-10-01 | 2026-10-01 | 1.0.0 |

### `rules/01_essentials/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_guiding_principles.py` | CLAUDE.md's imports follow guiding_principles.md — no lazy-load imports, a purpose comment on each, few, unique, always-on tiers in order | 9/10 | 2026-08-28 | 2026-10-01 | 2.0.0 |
| `test_rule_directory_organisation.py` | `01_essentials/` holds its expected files and folders, and tiers 01–04 follow the parent-and-children layout (`_` prefix, 2+ children, parent beside each folder) | 9/10 | 2026-08-28 | 2026-10-01 | 2.0.0 |
| `test_writing_style.py` | `writing_style.md` keeps its tables rule, one sentence per bullet, British spelling, underscore file-name dates and its multifile child | 9/10 | 2026-08-28 | 2026-10-01 | 1.1.0 |

### `rules/02_claude_standards/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_always_on_reachability.py` | Every always-on rule file in the real config is reachable from `CLAUDE.md`, and every `_lazy_load/` child has a 'Read on demand' pointer | 9/10 | 2026-09-18 | 2026-10-01 | 2.0.0 |
| `test_artefact_proposal_gates.py` | The three artefact proposal gates — naming, placement, duplication | 9/10 | 2026-08-28 | 2026-10-01 | 2.0.1 |
| `test_concurrent_sessions.py` | `git/_concurrent_sessions.md` keeps its incident record and shared-working-tree safety guidance | 9/10 | 2026-09-21 | 2026-10-01 | 1.2.1 |
| `test_decision_making.py` | `_decision_making.md` keeps each clause of the intentionality gate, and the rules it defers to still exist and agree | 9/10 | 2026-08-28 | 2026-10-01 | 2.0.0 |
| `test_git.py` | `git.md` keeps each git rule, imports its children, and its branch-name pattern matches its own examples | 9/10 | 2026-08-28 | 2026-10-01 | 2.0.0 |
| `test_plan_mode_phase_gates.py` | Mandatory plan-mode phase gates — blocking requirements, plan-type examples | 8/10 | 2026-09-16 | 2026-10-01 | 3.0.1 |
| `test_portable_paths_hooks.py` | Hooks resolve the config dir from their own location — no hardcoded `~/.claude/` file operations or guard substrings | 9/10 | 2026-09-18 | 2026-10-01 | 2.0.0 |
| `test_portable_paths_python.py` | Python test files use `CLAUDE_DIR` — no `.expanduser()` outside `_shared_paths.py`, home-directory constants or one-convention import prefixes | 9/10 | 2026-09-18 | 2026-10-01 | 2.0.0 |
| `test_security_guardrails.py` | `_security_guardrails.md` keeps each guardrail, and settings.json allows none of the wildcards it forbids | 9/10 | 2026-08-28 | 2026-10-01 | 2.0.0 |
| `test_test_metadata.py` | Every test's metadata header is complete, in order, well formed (banners, dates, semver, scores), and its quality score matches its own counts | 9/10 | 2026-10-01 | 2026-10-01 | 1.1.0 |
| `test_test_score_floor.py` | Every test meets quality 9, complexity 7 and style Yes, with no exemptions, and the minimums match `_test_metadata.md` | 9/10 | 2026-10-01 | 2026-10-01 | 2.0.0 |
| `test_testing.py` | Every enforcement hook has a test (aspect splits allowed), no orphaned hook tests, and testing.md's pointers exist | 9/10 | 2026-08-28 | 2026-10-01 | 1.2.0 |

### `rules/03_authoring_guidelines/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_authoring_rules.py` | `authoring_rules.md` keeps its checklist, steps and gates, and every file it points authors to exists | 9/10 | 2026-08-28 | 2026-10-01 | 2.0.0 |
| `test_authoring_agents.py` | `authoring_agents.md` is always-on and points to each of its 5 on-demand children, which are present and well-formed | 9/10 | 2026-09-28 | 2026-10-01 | 2.0.1 |
| `test_authoring_skills.py` | `authoring_skills.md` and its children: SKILL.md's six sections, the frontmatter example, contract fields matching the checklist, and trigger design | 9/10 | 2026-09-16 | 2026-10-01 | 4.1.0 |
| `test_authoring_skills_maturity.py` | `authoring_skills.md`'s maturity table matches the checklist and complexity formula, plus scope anti-patterns and low-maintenance principles | 9/10 | 2026-10-01 | 2026-10-01 | 1.0.0 |
| `test_claude_config_metadata.py` | Every rule opens with the three-line version, created and updated metadata header | 9/10 | 2026-09-28 | 2026-10-01 | 2.2.1 |

### `rules/04_claude_reference/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_claude_operational_efficiency.py` | `claude_operational_efficiency.md` keeps its 8 sections, imports exactly its 4 children with no orphans, and keeps its key phrases | 9/10 | 2026-09-30 | 2026-10-01 | 1.0.1 |

### `rules/05_lazy_load/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_claude_rule_loading_strategy.py` | The five-tier table matches the real `_rules/` folders, its example files exist, and CLAUDE.md imports match each tier's loading claim; placement uses measured usage, not 70% | 9/10 | 2026-09-30 | 2026-10-01 | 1.2.0 |
| `test_automation_controls.py` | Turn budgets and gates for `/loop`, `/batch`, `/goal` are documented and reasonable | 9/10 | 2026-09-16 | 2026-10-01 | 1.0.2 |
| `test_latency_optimisation.py` | `latency_optimisation.md` keeps effort as the lever, never gives a temperature above 1, and keeps its measure-first steps | 9/10 | 2026-09-17 | 2026-10-01 | 2.0.0 |
| `test_lazy_load_coverage.py` | Every `05_lazy_load/` file is reachable from at least one hook (direct or via a parent index file) | 3/10 | 2026-09-16 | 2026-10-01 | 1.5.1 |
| `test_lazy_load_rule_structure.py` | The 15 lazy-load rules once lacking a dedicated test keep their metadata header, Purpose line, key sections, linked child pages, working links and accurate Contents | 9/10 | 2026-10-01 | 2026-10-01 | 1.1.0 |
| `test_path_scoped_rules.py` | Path-scoped rules in `rules/` carry no `@` imports, and `rules/` holds only symlinks into `_rules/05_lazy_load/` | 9/10 | 2026-10-01 | 2026-10-01 | 1.0.0 |

---

## 📁 `settings/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_aliases.py` | Each `aliases.md` entry is complete, well formed and unique, its links and controls note stay in sync, and core aliases stay documented | 9/10 | 2026-08-28 | 2026-10-01 | 2.1.0 |
| `test_settings.py` | `settings.json` permission structure, security denies, no broad destructive allows and no real secrets | 9/10 | 2026-08-28 | 2026-10-01 | 1.1.0 |

**Merged (2026-10-01):** `rules/test_aliases_behavior.py` — its unique checks moved into `settings/test_aliases.py`, so one test covers `aliases.md`.

**Removed (2026-09-18):** `settings/test_aliases_behavior.py` — written to run as a standalone script (per its own docstring/README), not as native pytest: 3 of its 5 functions required positional arguments pytest couldn't supply (collection errors), and the other 2 used `print`/`return` instead of `assert`, so they never actually failed regardless of outcome. `rules/test_aliases_behavior.py` already covers "aliases are documented and functional" with real assertions. **Lost, not replaced:** the skill/command-existence and convention-documentation checks this file's logic described but never actually enforced as pytest.

---

## 📁 `skills/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_skill_structure_compliance.py` | Every installed skill passes the skill authoring gate's crawl checks, and each check is proven to fire | 9/10 | 2026-08-28 | 2026-10-01 | 2.0.1 |
| `test_no_orphaned_skill_files.py` | Every skill file is referenced somewhere in its skill, every `reference/` link in SKILL.md exists, and no SKILL.md @-imports a file | 9/10 | 2026-09-19 | 2026-10-01 | 2.0.0 |
| `test_skill_authoring_gate_walk.py` | The gate linter's walk checks (W1–W6) fail or warn as intended on fake skills | 9/10 | 2026-10-01 | 2026-10-01 | 1.0.0 |
| `test_skill_authoring_gate_run.py` | The gate linter's run checks (R2–R4) on fake skills, and failures block while judgement calls only warn | 9/10 | 2026-10-01 | 2026-10-01 | 1.0.0 |

### `skills/confluence_create_page/`

Behavioral tests for a code-backed skill — `confluence_create_page_handler.py` lives
alongside these tests and is imported directly via a relative import.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_confluence_create_page_handler.py` | The handler's title, space, pattern and section validators, including their boundaries | 9/10 | 2026-08-28 | 2026-10-01 | 2.0.0 |
| `test_confluence_create_page_phases.py` | The handler's publish phases, each failure mode's error, and the end-to-end flow, with Confluence mocked | 9/10 | 2026-10-01 | 2026-10-01 | 1.0.0 |
| `test_confluence_create_page_timeout.py` | The timeout wrapper on a live call — the dialog, each answer, draft preservation, the 6-minute cap, errors and closed input | 9/10 | 2026-08-28 | 2026-10-01 | 2.0.0 |
| `test_confluence_create_page_timeout_options.py` | Timeout argument parsing, the dialog's wording, how each answer resolves, and that drafts go to `~/_drafts/confluence/YYYY_MM_DD_<slug>.md` | 9/10 | 2026-10-01 | 2026-10-01 | 1.2.0 |

### `skills/jira_create/`

Behavioral tests for a code-backed skill — `jira_create_handler.py` lives alongside
these tests and is imported directly via a relative import.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_jira_create_handler.py` | Validation, phase orchestration, and mocked MCP error handling in the handler | 9/10 | 2026-09-19 | 2026-10-01 | 1.0.2 |

---

## 📁 Top level

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_file_structure_compliance.py` | Every file in the real Claude config passes the file-structure scan, checked area by area | 9/10 | 2026-08-28 | 2026-10-01 | 2.0.0 |
| `test_file_structure_validator.py` | The file-structure scanner flags bad names and skips auto-generated, hidden and exempt files | 9/10 | 2026-10-01 | 2026-10-01 | 1.1.2 |
| `test_rule_reachability.py` | The rule-reachability detector flags orphans and broken imports, and honours its exemptions, on fake rule trees | 9/10 | 2026-09-18 | 2026-10-01 | 2.0.0 |

---

## 📐 When to add a test

Per `_rules/02_claude_standards/behaviour.md` — adding or modifying an **enforcement hook** requires a corresponding test.
Instructional rules (files Claude reads but no mechanical hook fires) do not require tests; structural quality is covered by `test_rules_structure.py`.
