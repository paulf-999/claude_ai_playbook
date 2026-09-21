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
| `test_hook_registry_utils.py` | `settings.json` hook registry — every referenced hook file must exist on disk | 3/10 | 2026-08-28 | 2026-09-18 | 1.0.0 |

**Archived:** `test_auto_rotate_todo.py` moved to `_tests/_archived/` (2026-09-18) — `rotate_todo.sh` and `hook_auto_rotate_todo.sh` were never built despite a stale "Ready for production" claim in `TODO.md`; see the file's own archival note.

**Utility (not a scored test):** `hook_test_utils.py` — shared `run_hook()` helper, pipes a JSON payload to a hook and returns the result.

### `hooks/enforcement/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_enforcement_dir_structure.py` | `hook_enforcement_dir_structure.sh` — injects dir structure rules for `mkdir` under `~/.claude/` | 5/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |
| `test_enforcement_naming_convention.py` | `hook_enforcement_naming_convention.sh` — blocks new files under `~/.claude/` | 5/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |
| `test_enforcement_writing_style.py` | `hook_enforcement_writing_style.sh` — validates markdown file locations against writing_style.md | 9/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |

### `hooks/response_standards/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_style_guide_response_standards.py` | `hook_style_guide_response_standards.sh` — response-format compliance (Summary, offer line, timing footer) | 7/10 | 2026-09-07 | 2026-09-18 | 1.0.0 |
| `test_style_guide_response_standards_inject.py` | `hook_style_guide_response_standards_inject.sh` — per-turn salience injection, timestamp, waiver handling | 9/10 | 2026-09-07 | 2026-09-18 | 1.0.0 |

### `hooks/session_start/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_session_start_mcp_stale_settings.py` | `hook_session_start_mcp_stale_settings.sh` — stale-settings restart reminder, once-per-session dedup, portable path resolution | 9/10 | 2026-09-18 | 2026-09-18 | 1.0.0 |

---

## 📁 `rules/`

Tests for structural properties and behavioral compliance of files in `~/.claude/_rules/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_rules_structure.py` | File quality across all `_rules/` files — line limits, trailing newlines, import resolution, expected file set | 9/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |
| `test_aliases_behavior.py` | Aliases are documented, properly formatted, and validated as functional (spot-check representative aliases) | 5/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |

### `rules/01_essentials/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_guiding_principles.py` | Lazy-load and context-efficiency principles — no `05_lazy_load/` imports in CLAUDE.md, all imports documented | 3/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |
| `test_rule_directory_organisation.py` | Rule directory organization patterns — expected top-level files per tier | 7/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |
| `test_skill_authoring_gate.py` | Skills meet the authoring gate's quality (walk) and comprehensive (run) criteria | 9/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |
| `test_writing_style.py` | `writing_style.md` behavioral rules and documentation completeness | 5/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |

### `rules/02_claude_standards/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_artefact_proposal_gates.py` | The three artefact proposal gates — naming, placement, duplication | 9/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |
| `test_decision_making.py` | `_decision_making.md` is present, well-formed, and contains the intentionality-gate sections | 5/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |
| `test_git.py` | `git.md` is present, well-formed, and contains its expected section headings | 5/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |
| `test_plan_mode_phase_gates.py` | Mandatory plan-mode phase gates — blocking requirements, plan-type examples | 8/10 | 2026-09-16 | — | 1.0.0 |
| `test_security_guardrails.py` | Claude never recommends wildcard permissions for destructive commands, and related security guardrails | 5/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |
| `test_testing.py` | Self-consistency: enforcement hooks have tests, and testing.md documents the enforcement pattern | 5/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |

### `rules/03_authoring_guidelines/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_authoring_rules.py` | The rule authoring guide's pre-creation checklist and quality gate sections | — *(no metadata header)* | — | — | — |
| `test_authoring_skills.py` | `authoring_skills.md` contains its 7 required improvements | 5/10 | 2026-09-16 | — | 1.0.0 |

### `rules/05_lazy_load/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_automation_controls.py` | Turn budgets and gates for `/loop`, `/batch`, `/goal` are documented and reasonable | 9/10 | 2026-09-16 | 2026-09-17 | 1.0.0 |
| `test_latency_optimisation.py` | `latency_optimisation.md` exists under its correct (British) name, frontmatter, and key sections | 5/10 | 2026-09-17 | — | 1.0.0 |
| `test_lazy_load_coverage.py` | Every `05_lazy_load/` file is reachable from at least one hook (direct or via a parent index file) | 3/10 | 2026-09-16 | 2026-09-17 | 1.0.0 |

---

## 📁 `settings/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_aliases.py` | Each `aliases.md` entry is documented, formatted, and structurally valid | 5/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |
| `test_settings.py` | `settings.json` permission structure, hook registration, and principle compliance | 7/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |

**Removed (2026-09-18):** `settings/test_aliases_behavior.py` — written to run as a standalone script (per its own docstring/README), not as native pytest: 3 of its 5 functions required positional arguments pytest couldn't supply (collection errors), and the other 2 used `print`/`return` instead of `assert`, so they never actually failed regardless of outcome. `rules/test_aliases_behavior.py` already covers "aliases are documented and functional" with real assertions. **Lost, not replaced:** the skill/command-existence and convention-documentation checks this file's logic described but never actually enforced as pytest.

---

## 📁 `skills/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_skill_structure_compliance.py` | All installed skills follow the skill template structure | 3/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |

### `skills/confluence_create_page/`

Behavioral tests for a code-backed skill — `confluence_create_page_handler.py` lives
alongside these tests and is imported directly via a relative import.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_confluence_create_page_handler.py` | Validation, phase orchestration, and error handling in the handler | 9/10 | 2026-08-28 | 2026-09-19 | 1.0.0 |
| `test_confluence_create_page_timeout.py` | The publish-timeout mechanism — trigger, abort/retry/continue, draft preservation, 6-minute cap | 8/10 | 2026-08-28 | 2026-09-19 | 1.1.0 |

---

## 📁 Top level

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_file_structure_compliance.py` | All files and directories in the Claude config follow naming and placement conventions | 3/10 | 2026-08-28 | 2026-09-17 | 1.0.0 |

---

## 📐 When to add a test

Per `_rules/02_claude_standards/behaviour.md` — adding or modifying an **enforcement hook** requires a corresponding test.
Instructional rules (files Claude reads but no mechanical hook fires) do not require tests; structural quality is covered by `test_rules_structure.py`.
