# Quality Scorecard — test_file_structure_compliance.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 7.4/10

**Recommended improvements:**
- Update the header quality score from 5/10 to reflect the current counts
- Add test functions and assertions toward 10+ and 15+ (now 1 and 1)
- Complete the metadata header: add `Test complexity score` and `Python style compliant`
- Correct the docstring: it is one scanning function, not a parametrized test

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 8/10 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message<br>• ⚠️ **Docstring:** docstring says the test is parametrized, but it is one function that scans everything |
| **Complexity** | 10/10 | • 🧮 **Complexity:** estimated raw complexity 0 — the header has no complexity score |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 2/10 | • 📊 **Counts:** 1 test functions and 1 assertions<br>• ⚠️ **Header drift:** header quality score is 5/10, but the counts support 2/10 |
| **Structural Compliance** | 6/10 | • ✅ **Header:** header is missing `Test complexity score` and `Python style compliant` |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-28 |
| **Regression Value** | 8/10 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case<br>• ⚠️ **Finding:** runs the real scanner over the whole config, so any naming or placement violation fails it |
| **Overall** | **7.4/10** | • 💪 **Strongest:** Complexity (10/10)<br>• ⚠️ **Weakest:** Coverage (2/10) |

## 🔗 Related files

- `src/claude/_tests/test_file_structure_compliance.py` — the test being scored
- `src/claude/_rules/01_essentials/claude_usage_standards/claude_directory_structure.md` — what the test guards
