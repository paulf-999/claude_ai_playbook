# Quality Scorecard — test_file_structure_compliance.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 7.0/10

**Recommended improvements:**
- Add test functions and assertions toward 10+ and 15+ (now 1 and 1)
- Convert `scan()`'s Google-style `Returns:` docstring to reST so the file is Python style compliant
- Correct the docstring: it is one scanning function, not a parametrized test

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 8/10 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message<br>• ⚠️ **Docstring:** docstring says the test is parametrized, but it is one function that scans everything |
| **Complexity** | 5/10 | • 🧮 **Complexity:** raw 5 — Concepts 2 (naming, placement) + Scope 3 (whole-config scan), matching the header's 5/10 |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 2/10 | • 📊 **Counts:** 1 test functions and 1 assertions |
| **Structural Compliance** | 8/10 | • ✅ **Header:** all 7 metadata lines present, in order<br>• ⚠️ **Style:** `Python style compliant: No` — `scan()` uses a Google-style docstring |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 8/10 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case<br>• ⚠️ **Finding:** runs the real scanner over the whole config, so any naming or placement violation fails it |
| **Overall** | **7.0/10** | • 💪 **Strongest:** Evidence of Need and Currency (9/10)<br>• ⚠️ **Weakest:** Coverage (2/10) |

## 🔗 Related files

- `src/claude/_tests/test_file_structure_compliance.py` — the test being scored
- `src/claude/_rules/01_essentials/claude_usage_standards/claude_directory_structure.md` — what the test guards
