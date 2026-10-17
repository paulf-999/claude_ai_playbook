# 🧪 `_helpers/` shared helpers

**Purpose:** Shared helpers the whole suite imports; it holds no tests of its own.

| Helper | What it does |
|---|---|
| `_shared_paths.py` | Resolves `CLAUDE_DIR` (via `CLAUDE_CONFIG_DIR`, default `~/.claude`) and the path constants several tests share (`CLAUDE_MD`, `ALIASES_FILE`, `SETTINGS_FILE`, `SKILLS_DIR`, `HOOKS_DIR`, `RULES_DIR`); single-use constants stay in their own test file |
| `_file_structure_validator.py` | The file-structure scanner, and the `--check` mode the naming hook calls for one new path |
| `_metadata_header.py` | Validates the three-line version, created and updated header for rules, skills, agents and hooks |
| `_rule_reachability.py` | Reports files under `rules/` that would load wrongly (READMEs, `_lazy_load/` folders, `@import` lines, unscoped path-scoped files) and Read-on-demand pointers that lead nowhere |
| `_resolved_rule.py` | Reads a parent rule with every child it imports or points to on demand inlined |
| `_skill_orphans.py` | Detects orphaned skill files, broken `reference/` links and eager imports |
| `_gate_fixtures.py` | Loads the skill authoring gate linter and builds fake skills for its walk and run tests |

- **Whole-config tests:** the tests that span the whole config live in [`_whole_config/`](../_whole_config/README.md).

[← All tests](../README.md)
