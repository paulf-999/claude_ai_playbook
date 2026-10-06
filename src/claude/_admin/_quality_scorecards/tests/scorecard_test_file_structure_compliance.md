# Quality Scorecard — test_file_structure_compliance.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 8.9/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Goal:** module docstring says what the scan covers and why each area has its own test<br>• 🔍 **Messages:** every assertion names the folder and lists each error |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 0 (the real config passes the scan) + Scope 3 (whole-config scan) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards the naming conventions in `claude_directory_structure.md` on the real config |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 11 test functions and 20 assertions<br>• 🧩 **Areas:** root files, `_rules/`, `_tests/`, `_templates/`, `_reference/`, `hooks/`, `skills/`, `agents/`, `rules/` and a whole-config catch-all |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 8/10 | 2026-09-30 | • 🛡️ **Missing folders:** each area test fails if its folder is gone, so a move can't pass silently<br>• ⚠️ **Bad cases:** proven in `test_file_structure_validator.py`, not here |
| **Overall** | **8.9/10** | 2026-10-01 | • 💪 **Strongest:** Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10), held at the minimum by the whole-config scan |

## 🔗 Related files

- `src/claude/_tests/test_file_structure_compliance.py` — the test being scored
- `src/claude/_tests/_file_structure_validator.py` — the scanner it runs
- `src/claude/_tests/test_file_structure_validator.py` — proves the scanner on fake config trees
- `src/claude/_rules/05_lazy_load/claude_directory_structure.md` — what the test guards
