# 🧪 `_helpers/` tests

**Purpose:** Shared helpers the whole suite imports, plus the tests that span the whole config rather than one artefact.

## 📋 Tests

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_file_structure_compliance.py` | Every file in the real Claude config passes the file-structure scan, checked area by area | 7/10 | 2026-08-28 | 2026-10-11 | 3.0.2 |
| `test_file_structure_validator.py` | The file-structure scanner flags bad names and skips auto-generated, hidden and exempt files | 10/10 | 2026-10-01 | 2026-10-11 | 1.3.3 |
| `test_rule_reachability.py` | The native-load detector flags READMEs, `_lazy_load/` folders, imports, unscoped path-scoped files and broken pointers under `rules/`, on fake rule trees | 8/10 | 2026-09-18 | 2026-10-11 | 3.2.3 |
| `test_metadata_header_format.py` | Format cases for the shared metadata-header validator, run once for rules, skills, agents and hooks: field order, values, placement, shell style and header after frontmatter | 10/10 | 2026-10-11 | 2026-10-11 | 1.0.0 |

## 🔧 Shared helpers (not scored tests)

| Helper | What it does |
|---|---|
| `_shared_paths.py` | Resolves `CLAUDE_DIR` (via `CLAUDE_CONFIG_DIR`, default `~/.claude`) and the path constants several tests share (`CLAUDE_MD`, `ALIASES_FILE`, `SETTINGS_FILE`, `SKILLS_DIR`, `HOOKS_DIR`, `RULES_DIR`); single-use constants stay in their own test file |
| `_file_structure_validator.py` | The file-structure scanner, and the `--check` mode the naming hook calls for one new path |
| `_metadata_header.py` | Validates the three-line version, created and updated header for rules, skills, agents and hooks |
| `_rule_reachability.py` | Reports files under `rules/` that would load wrongly (READMEs, `_lazy_load/` folders, `@import` lines, unscoped path-scoped files) and Read-on-demand pointers that lead nowhere |
| `_resolved_rule.py` | Reads a parent rule with every child it imports or points to on demand inlined |
| `_skill_orphans.py` | Detects orphaned skill files, broken `reference/` links and eager imports |
| `_gate_fixtures.py` | Loads the skill authoring gate linter and builds fake skills for its walk and run tests |

[← All tests](../README.md)
