# Quality Scorecard — test_hook_metadata_header.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-17

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 9/10 | 2026-10-11 | • 🧮 **Raw complexity 1:** Concepts 0 (every hook's header) + Scope 1 (`hooks/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 9/10 | 2026-10-11 | • 📊 **Counts:** 2 test functions and 2 assertions<br>• 🔀 **Split:** every hook is scanned here, while the format cases moved to `_helpers/test_metadata_header_format.py` on 2026-10-11 |
| **Structural Compliance** | 9/10 | 2026-10-11 | • ✅ **Header:** full metadata header, marked Python style compliant<br>• 📁 **Location:** moved to `_tests/hooks/` on 2026-10-11 |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current config, header version 2.0.0 updated 2026-10-11 |
| **Regression Value** | 8/10 | 2026-10-11 | • 🛡️ **Failure cases:** fails on any bad hook header, with the bad-input proofs in the shared format test |
| **Overall** | **9.0/10** | 2026-10-11 | • 💪 **Strongest:** Currency (10/10)<br>• ⚠️ **Weakest:** Regression Value (8/10) |

## 🔗 Related files

- `src/claude/_tests/hooks/test_hook_metadata_header.py` — the test being scored
- `src/claude/hooks/` — what the test guards
- `src/claude/rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md` — what the test guards
