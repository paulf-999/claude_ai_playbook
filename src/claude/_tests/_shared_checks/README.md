# 🧪 `_shared_checks/` tests

**Purpose:** Tests for the checks every artefact type shares (file naming and structure, rule loading, the metadata header and the Python version check), plus the scan that runs them over the whole config.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_file_structure_compliance.py` | Every file in the real Claude config passes the file-structure scan, checked area by area | 7/10 | 2026-08-28 | 2026-10-17 | 3.0.4 |
| `test_file_structure_validator.py` | The file-structure scanner flags bad names and skips auto-generated, hidden and exempt files | 10/10 | 2026-10-01 | 2026-10-22 | 1.4.0 |
| `test_rule_reachability.py` | The native-load detector flags READMEs, `_lazy_load/` folders, imports, unscoped path-scoped files and broken pointers under `rules/`, on fake rule trees | 8/10 | 2026-09-18 | 2026-10-22 | 3.2.4 |
| `test_shared_paths.py` | The path helpers return the plain link when it climbs out of the config, and read `paths:` only from the opening frontmatter | 9/10 | 2026-10-22 | 2026-10-22 | 1.0.0 |
| `test_resolved_rule.py` | The resolved-rule reader still lists and inlines `@~/` imports, keeping missing ones as written | 10/10 | 2026-10-22 | 2026-10-22 | 1.0.0 |
| `test_metadata_header_format.py` | Format cases for the shared metadata-header validator, run once for rules, skills, agents and hooks: field order, values, placement, shell style and header after frontmatter | 10/10 | 2026-10-11 | 2026-10-11 | 1.0.0 |
| `test_python_version_guard.py` | Every playbook script in `scripts/`, `skills/`, `_install/helpers/` and `plugins/` exits early on Python older than 3.10, with the check placed before its other imports | 10/10 | 2026-10-22 | 2026-10-22 | 1.0.0 |

- **Helpers they use:** listed in [`_helpers/README.md`](../_helpers/README.md).

[← All tests](../README.md)
