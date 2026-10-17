# 🧪 `_shared_checks/` tests

**Purpose:** Tests for the checks every artefact type shares (file naming and structure, rule loading and the metadata header), plus the scan that runs them over the whole config.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_file_structure_compliance.py` | Every file in the real Claude config passes the file-structure scan, checked area by area | 7/10 | 2026-08-28 | 2026-10-17 | 3.0.4 |
| `test_file_structure_validator.py` | The file-structure scanner flags bad names and skips auto-generated, hidden and exempt files | 10/10 | 2026-10-01 | 2026-10-11 | 1.3.3 |
| `test_rule_reachability.py` | The native-load detector flags READMEs, `_lazy_load/` folders, imports, unscoped path-scoped files and broken pointers under `rules/`, on fake rule trees | 8/10 | 2026-09-18 | 2026-10-11 | 3.2.3 |
| `test_metadata_header_format.py` | Format cases for the shared metadata-header validator, run once for rules, skills, agents and hooks: field order, values, placement, shell style and header after frontmatter | 10/10 | 2026-10-11 | 2026-10-11 | 1.0.0 |

- **Helpers they use:** listed in [`_helpers/README.md`](../_helpers/README.md).

[← All tests](../README.md)
