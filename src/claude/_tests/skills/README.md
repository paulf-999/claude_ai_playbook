# 🧪 `skills/` tests

**Purpose:** Tests for skills in `skills/`, plus the scripts some skills carry.

## 📁 `_all_skills/`

Tests that every skill must pass.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_skill_structure_compliance.py` | Every installed skill passes the skill authoring gate's crawl checks, and each check is proven to fire | 9/10 | 2026-08-28 | 2026-10-11 | 2.0.5 |
| `test_no_orphaned_skill_files.py` | Every skill file is referenced somewhere in its skill, every `reference/` link in SKILL.md exists, and no SKILL.md @-imports a file | 10/10 | 2026-09-19 | 2026-10-11 | 2.0.2 |
| `test_skill_authoring_gate_walk.py` | The gate linter's walk checks (W1–W6) fail or warn as intended on fake skills | 10/10 | 2026-10-01 | 2026-10-11 | 1.1.1 |
| `test_skill_authoring_gate_run.py` | The gate linter's run checks (R2–R4) on fake skills, and failures block while judgement calls only warn | 10/10 | 2026-10-01 | 2026-10-11 | 1.1.2 |
| `test_skill_authoring_gate_cli.py` | The gate linter's command line exits 1 on a failing skill or missing folder, and 0 on clean, warning-only or empty folders | 10/10 | 2026-10-17 | 2026-10-17 | 1.0.0 |
| `test_skill_index_versions.py` | Every skill group README lists each of its skills at the version in that skill's SKILL.md header | 10/10 | 2026-10-05 | 2026-10-11 | 1.0.1 |
| `test_skill_instructions_section.py` | Every SKILL.md must carry its own must-follow instructions for Claude | 8/10 | 2026-10-01 | 2026-10-11 | 2.2.4 |
| `test_skill_metadata_header.py` | Every SKILL.md carries a valid header after its frontmatter, matching its contract version, and the template models it | 9/10 | 2026-09-28 | 2026-10-17 | 2.0.2 |

## 📁 `claude_capture_session_prompts/`

Tests for the skill's own script, `capture_session_prompts.py`, which lives in the skill folder.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_capture_session_prompts.py` | The history file resolves from `CLAUDE_CONFIG_DIR`, output goes to `~/_sessions/` with a date-first name, and the categories and markdown match the skill's docs | 7/10 | 2026-09-30 | 2026-10-11 | 1.1.1 |

## 📁 `claude_kaizen/`

Tests for the skill's eval scorer, `evals/runner.py`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_claude_kaizen_runner.py` | Tests for claude_kaizen's evals/runner.py, the before/after eval scorer | 9/10 | 2026-10-02 | 2026-10-06 | 1.2.0 |

[← All tests](../README.md)
