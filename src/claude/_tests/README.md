# 🧪 Tests

**Purpose:** Check that every part of the Claude config (rules, skills, agents, hooks, settings and scripts) is well formed and behaves as intended, so a broken change fails here before it reaches a live session.

## 🎯 Summary

- **One suite:** run everything at once with `pytest`, and it checks whichever config `CLAUDE_CONFIG_DIR` points at.
- **Named after what they test:** each folder is named after the config folder or files it checks, apart from `_core/`.
- **`_core/` is the shared engine:** it holds the helpers every other folder imports and the few tests that span the whole config.
- **Scores come from the files:** each table's Quality, Created, Updated and Version columns are copied from that test's own metadata header.

## ▶️ Running the tests

```bash
# Playbook repo: from the repo root, where pytest.ini adds coverage and the install tests
CLAUDE_CONFIG_DIR=$PWD/src/claude python3 -m pytest src/claude/_tests

# Live config: from the config folder
cd ~/.claude && python3 -m pytest _tests
```

- **Why set `CLAUDE_CONFIG_DIR`:** without it, the suite may check your live config instead of the repo.

## 🗂️ What each folder tests

| Folder | Claude artefact | What it checks |
|---|---|---|
| `_core/` | None, it's shared infrastructure | Helpers used across the suite, plus whole-config checks like file naming |
| `_reference/` | Quality scorecards in `_reference/_quality_scorecards/` | Every artefact has a scorecard, and its dates are valid |
| `agents/` | Sub-agents | Agent headers and triggers |
| `docs/` | Repo docs | Local links in `README.md` and `docs/` |
| `hooks/` | Hooks | Hook headers, registration and each hook's behaviour |
| `rules/` | Rules | Rule structure, loading, headers and cross-references, by tier |
| `root_files/` | Single files at the config root | `settings.json` permissions and `aliases.md` entries |
| `scripts/` | Maintenance scripts | Each script's behaviour and naming |
| `skills/` | Skills | Skill structure, headers, references and each skill's own scripts |

## 🧩 Why `_core/` exists

Every other folder maps to one kind of artefact, but some code and checks belong to none of them.

- **Shared helpers:** path resolution, the file-structure scanner and the metadata-header validator are used by tests in several folders, so they live in one place.
- **Whole-config tests:** checks like "every file in the config is named correctly" cover all artefacts at once, so they sit beside the helpers they use.
- **How tests find it:** `conftest.py` puts `_core/` on `sys.path`, so tests import helpers by name, e.g. `from _shared_paths import CLAUDE_DIR`.
- **Why the `_` prefix:** it marks the folder as infrastructure rather than an artefact type, and sorts it first.

### 🔧 Shared helpers (not scored tests)

| Helper | What it does |
|---|---|
| `_shared_paths.py` | Resolves `CLAUDE_DIR` (via `CLAUDE_CONFIG_DIR`, default `~/.claude`) and the path constants several tests share (`CLAUDE_MD`, `ALIASES_FILE`, `SETTINGS_FILE`, `SKILLS_DIR`, `HOOKS_DIR`, `RULES_DIR`); single-use constants stay in their own test file |
| `_file_structure_validator.py` | The file-structure scanner, and the `--check` mode the naming hook calls for one new path |
| `_metadata_header.py` | Validates the three-line version, created and updated header for rules, skills, agents and hooks |
| `_rule_reachability.py` | Reports files under `rules/` that would load wrongly (READMEs, `_lazy_load/` folders, `@import` lines, unscoped path-scoped files) and Read-on-demand pointers that lead nowhere |
| `_resolved_rule.py` | Reads a parent rule with every child it imports or points to on demand inlined |
| `_skill_orphans.py` | Detects orphaned skill files, broken `reference/` links and eager imports |
| `_gate_fixtures.py` | Loads the skill authoring gate linter and builds fake skills for its walk and run tests |

---

## 📁 `_core/`

Suite-wide tests that span the whole config, kept beside the shared helpers listed above.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_file_structure_compliance.py` | Every file in the real Claude config passes the file-structure scan, checked area by area | 7/10 | 2026-08-28 | 2026-10-11 | 3.0.2 |
| `test_file_structure_validator.py` | The file-structure scanner flags bad names and skips auto-generated, hidden and exempt files | 10/10 | 2026-10-01 | 2026-10-11 | 1.3.3 |
| `test_rule_reachability.py` | The native-load detector flags READMEs, `_lazy_load/` folders, imports, unscoped path-scoped files and broken pointers under `rules/`, on fake rule trees | 8/10 | 2026-09-18 | 2026-10-11 | 3.2.3 |
| `test_metadata_header_format.py` | Format cases for the shared metadata-header validator, run once for rules, skills, agents and hooks: field order, values, placement, shell style and header after frontmatter | 10/10 | 2026-10-11 | 2026-10-11 | 1.0.0 |

---

## 📁 `_reference/`

Tests for the quality scorecards in `_reference/_quality_scorecards/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_scorecard_coverage.py` | Every hook, agent and skill has a scorecard on its folder's dimensions, and the summaries add up | 8/10 | 2026-10-01 | 2026-10-11 | 1.1.3 |
| `test_scorecard_dates.py` | Validates the per-row Date Updated column in every quality scorecard table | 10/10 | 2026-10-01 | 2026-10-11 | 1.0.3 |

---

## 📁 `agents/`

Tests for custom sub-agents in `agents/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_agent_metadata_header.py` | Every AGENT.md carries a valid header after its frontmatter, its major version matches its maturity, and the template models it | 9/10 | 2026-09-29 | 2026-10-11 | 2.0.0 |
| `test_agent_triggers.py` | No agent trigger competes with a skill for the same request | 9/10 | 2026-10-01 | 2026-10-11 | 2.0.0 |

---

## 📁 `docs/`

Tests for the playbook repo's own `README.md` and `docs/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_docs_local_links.py` | Checks every local link in README.md and docs/ points at a file that exists | 7/10 | 2026-10-04 | 2026-10-11 | 1.0.1 |

---

## 📁 `hooks/`

Tests for Claude Code hook scripts in `~/.claude/hooks/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_hook_metadata_header.py` | Every hook script carries a valid metadata header on lines 2–4, after its shebang | 9/10 | 2026-09-29 | 2026-10-11 | 2.0.0 |
| `test_hook_registry_utils.py` | `settings.json` hook registry — known events, command hooks, no duplicates, every referenced hook file exists, and every hook file is registered or listed in `RESERVED_HOOKS` | 8/10 | 2026-08-28 | 2026-10-11 | 2.3.4 |

**Utility (not a scored test):** `hook_test_utils.py` — shared `run_hook()` helper, pipes a JSON payload to a hook and returns the result.

### `hooks/enforcement/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_enforcement_mcp_stale_settings.py` | `hook_enforcement_mcp_stale_settings.sh` — warns once when the disabled MCP servers change mid-session | 10/10 | 2026-09-18 | 2026-10-11 | 2.0.4 |
| `test_enforcement_naming_convention.py` | `hook_enforcement_naming_convention.sh` — denies new config files whose names break the compliance checks, and lets everything else through | 10/10 | 2026-08-28 | 2026-10-11 | 2.1.2 |
| `test_enforcement_markdown_location.py` | `hook_enforcement_markdown_location.sh` — flags stray markdown at the config root and badly named `_reference/` files, using the real stdin payload | 10/10 | 2026-08-28 | 2026-10-11 | 3.1.2 |

### `hooks/response_standards/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_style_guide_response_standards_checker_flags.py` | `hook_style_guide_response_standards_checker.sh` (reserved) — flags a missing Summary, offer line or timing footer, and text after the footer | 10/10 | 2026-10-01 | 2026-10-11 | 1.0.2 |
| `test_style_guide_response_standards_checker_waivers.py` | `hook_style_guide_response_standards_checker.sh` (reserved) — skips short answers, skill output, code blocks, errors and plan-mode output | 10/10 | 2026-10-01 | 2026-10-11 | 1.0.2 |
| `test_style_guide_response_standards_reminder.py` | `hook_style_guide_response_standards_reminder.sh` — per-turn salience injection, timestamp, waiver handling | 10/10 | 2026-09-07 | 2026-10-11 | 2.1.2 |

---

## 📁 `rules/`

Tests for structural properties and behavioral compliance of files in `~/.claude/rules/` and `~/.claude/_rules_lazy_load/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_rules_structure.py` | Per-file format across all `rules/` files — line limits, H1 and H2 heading emoji, trailing newlines, and no Related or unearned Contents sections | 10/10 | 2026-08-28 | 2026-10-11 | 2.5.4 |
| `test_rules_structure_layout.py` | Where `rules/` files live, every import in `CLAUDE.md` and `rules/` resolves, and no import chain reaches `_reference/` | 7/10 | 2026-10-01 | 2026-10-11 | 5.0.0 |
| `test_rule_cross_references.py` | Rule files point at things that exist and agree with the files that repeat them, across six rules, including git.md's branch pattern and its examples | 10/10 | 2026-10-11 | 2026-10-11 | 2.0.1 |

### `rules/01_essentials/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_guiding_principles.py` | CLAUDE.md imports only memory and aliases, each with a purpose comment, unique and under the Imports heading | 9/10 | 2026-08-28 | 2026-10-11 | 3.0.3 |
| `test_rule_directory_organisation.py` | `01_essentials/` holds its expected files and folders, and tiers 01–03 follow the parent-and-children layout (`_` prefix, 2+ children, parent beside each folder) | 9/10 | 2026-08-28 | 2026-10-11 | 2.4.1 |

### `rules/02_claude_standards/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_always_on_reachability.py` | Every file under `rules/` loads the way its folder says — no README, `_lazy_load/` folder, `@import` or unscoped `02_claude_standards/path_scoped_rules/` file — and every 'Read on demand' pointer | 9/10 | 2026-09-18 | 2026-10-11 | 3.2.5 |
| `test_claude_rule_loading_strategy.py` | The five-folder table matches the real `rules/` and `_rules_lazy_load/` folders, and its example files exist, matching each tier's loading claim | 9/10 | 2026-09-30 | 2026-10-11 | 4.0.0 |
| `test_concurrent_sessions.py` | `git/_concurrent_sessions.md` stays reachable from `git.md` and keeps its 2026-09-21 incident record | 9/10 | 2026-09-21 | 2026-10-11 | 3.0.0 |
| `test_no_wording_pinning.py` | No test pins an instructional rule's prose (a multi-word literal checked against a real file's text) or guards a finished migration (`assert not <path>.exists()`), unless tagged `# wording-check:` or `# absence-check:` with a reason | 10/10 | 2026-10-11 | 2026-10-11 | 1.1.0 |
| `test_path_scoped_rules.py` | Path-scoped rules in `rules/` carry no `@` imports, `rules/` holds real files not links, and every `02_claude_standards/path_scoped_rules/` file has `paths:` | 7/10 | 2026-10-01 | 2026-10-11 | 2.3.2 |
| `test_path_scoped_rules_live.py` | Proves in a live session that a `paths:` rule loads when, and only when, a matching file is read | 9/10 | 2026-10-01 | 2026-10-11 | 1.2.3 |
| `test_plan_mode_phase_gates.py` | `_plan_mode_phase_gates.md` keeps its plan-persistence section and 2026-09-19 incident record | 9/10 | 2026-09-16 | 2026-10-11 | 4.0.0 |
| `test_portable_paths_hooks.py` | Hooks resolve the config dir from their own location — no hardcoded `~/.claude/` file operations or guard substrings | 10/10 | 2026-09-18 | 2026-10-11 | 2.0.3 |
| `test_portable_paths_python.py` | Python test files use `CLAUDE_DIR` — no `.expanduser()` outside `_shared_paths.py`, home-directory constants or one-convention import prefixes | 8/10 | 2026-09-18 | 2026-10-11 | 2.0.3 |
| `test_testing.py` | Every enforcement hook has a test (aspect splits allowed), no orphaned hook tests, and testing.md's pointers exist | 10/10 | 2026-08-28 | 2026-10-11 | 2.1.0 |

### `rules/03_authoring_guidelines/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_authoring_agents.py` | `authoring_agents.md` points to each of its 5 on-demand children, which are present and well-formed | 9/10 | 2026-09-28 | 2026-10-10 | 2.2.2 |
| `test_authoring_skills.py` | `authoring_skills.md` and its children: SKILL.md's six sections, the frontmatter example, contract fields matching the checklist, and the maturity table matching the checklist and complexity formula | 9/10 | 2026-09-16 | 2026-10-11 | 5.0.1 |
| `test_claude_config_metadata.py` | Every rule opens with the three-line version, created and updated metadata header | 9/10 | 2026-09-28 | 2026-10-11 | 3.0.0 |
| `test_rule_headers.py` | Validates the rule-only `applies_to`, `miss_cost` and `loading` headers defined in _claude_config_metadata.md | 8/10 | 2026-10-01 | 2026-10-11 | 1.9.6 |
| `test_skill_domains.py` | Keeps skill_domains.yaml and the real skills/ layout in step | 10/10 | 2026-09-30 | 2026-10-11 | 1.0.4 |

### `rules/rules_lazy_load/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_lazy_load_coverage.py` | Every `_rules_lazy_load/` file is reachable from at least one hook (direct or via a parent index file) | 8/10 | 2026-09-16 | 2026-10-11 | 2.5.8 |
| `test_lazy_load_rule_structure.py` | The 14 rules once lacking a dedicated test keep their metadata header, Purpose line, linked child pages, working links and accurate Contents | 10/10 | 2026-10-01 | 2026-10-11 | 2.0.0 |
| `test_lazy_load_triggers.py` | Validates that every lazy rule has something that makes Claude load it | 9/10 | 2026-10-01 | 2026-10-11 | 2.0.0 |
| `test_org.py` | Organisation-specific terms stay inside _rules_lazy_load/org/ and never leak into shared files | 8/10 | 2026-10-01 | 2026-10-11 | 1.3.6 |
| `test_test_metadata.py` | Every test's metadata header, in `_tests/` and the repo's `src/claude/_install/_tests/`, is complete, in order and well formed (banners, dates, semver, scores) | 10/10 | 2026-10-01 | 2026-10-11 | 1.3.2 |
| `test_test_quality_score.py` | Every test header's quality score is exactly what its file earns from four content checks: failure messages, docstrings, a non-vacuous scan and a test proven to fail | 10/10 | 2026-10-02 | 2026-10-11 | 2.0.0 |
| `test_test_score_floor.py` | Every test, in `_tests/` and the repo's `src/claude/_install/_tests/`, meets quality 7, complexity 7 and style Yes, and the minimums match `_test_metadata.md` | 8/10 | 2026-10-01 | 2026-10-11 | 4.0.0 |

---

## 📁 `scripts/`

Tests for the maintenance scripts in `scripts/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_audit_claude_component_root.py` | Validates how audit_claude_component.py chooses the folder it scans | 10/10 | 2026-10-01 | 2026-10-11 | 1.0.4 |
| `test_audit_plans.py` | `audit_plans.py` lists saved plans by status from `_plans/` and its status folders, flags stale Active plans, and counts plans and drafts to file | 9/10 | 2026-10-11 | 2026-10-11 | 2.0.1 |
| `test_audit_rule_usage.py` | Validates audit_rule_usage.py against small fixture rules and transcripts | 10/10 | 2026-10-01 | 2026-10-11 | 1.10.5 |
| `test_clean_plans.py` | `clean_plans.py` files saved plans into `_plans/<status>/` by their status line (or phase table), files drafts into `plans/draft/` or `plans/archive/` by age, never overwrites, and runs without asking during `make install` | 9/10 | 2026-10-02 | 2026-10-11 | 2.1.1 |
| `test_script_naming.py` | Validates that every script under scripts/ follows the script naming pattern | 10/10 | 2026-10-02 | 2026-10-11 | 1.1.3 |

---

## 📁 `root_files/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_aliases.py` | Each `aliases.md` entry is complete, well formed and unique, its links and controls note stay in sync, and core aliases stay documented | 10/10 | 2026-08-28 | 2026-10-11 | 2.2.7 |
| `test_settings.py` | `settings.json` permission structure, security denies, no broad destructive allows and no real secrets | 9/10 | 2026-08-28 | 2026-10-11 | 1.2.2 |

---

## 📁 `skills/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_skill_structure_compliance.py` | Every installed skill passes the skill authoring gate's crawl checks, and each check is proven to fire | 9/10 | 2026-08-28 | 2026-10-11 | 2.0.5 |
| `test_no_orphaned_skill_files.py` | Every skill file is referenced somewhere in its skill, every `reference/` link in SKILL.md exists, and no SKILL.md @-imports a file | 10/10 | 2026-09-19 | 2026-10-11 | 2.0.2 |
| `test_skill_authoring_gate_walk.py` | The gate linter's walk checks (W1–W6) fail or warn as intended on fake skills | 10/10 | 2026-10-01 | 2026-10-11 | 1.1.1 |
| `test_skill_authoring_gate_run.py` | The gate linter's run checks (R2–R4) on fake skills, and failures block while judgement calls only warn | 10/10 | 2026-10-01 | 2026-10-11 | 1.1.2 |
| `test_skill_index_versions.py` | Every skill group README lists each of its skills at the version in that skill's SKILL.md header | 10/10 | 2026-10-05 | 2026-10-11 | 1.0.1 |
| `test_skill_instructions_section.py` | Every SKILL.md must carry its own must-follow instructions for Claude | 8/10 | 2026-10-01 | 2026-10-11 | 2.2.4 |
| `test_skill_metadata_header.py` | Every SKILL.md carries a valid header after its frontmatter, matching its contract version, and the template models it | 9/10 | 2026-09-28 | 2026-10-11 | 2.0.0 |

### `skills/claude_capture_session_prompts/`

Tests for the skill's own script, `capture_session_prompts.py`, which lives in the skill folder.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_capture_session_prompts.py` | The history file resolves from `CLAUDE_CONFIG_DIR`, output goes to `~/_sessions/` with a date-first name, and the categories and markdown match the skill's docs | 7/10 | 2026-09-30 | 2026-10-11 | 1.1.1 |

### `skills/claude_kaizen/`

Tests for the skill's eval scorer, `evals/runner.py`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_claude_kaizen_runner.py` | Tests for claude_kaizen's evals/runner.py, the before/after eval scorer | 9/10 | 2026-10-02 | 2026-10-06 | 1.2.0 |

---

## 📐 When to add a test

- **Enforcement hooks:** adding or changing one needs a matching test, per `rules/02_claude_standards/behaviour.md`.
- **Instructional rules:** files Claude reads but no hook enforces need no test of their own, because `test_rules_structure.py` covers their structure.
