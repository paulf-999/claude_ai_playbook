# Quality Scorecard — test_script_naming.py

**Date Created:** 2026-10-02
**Date Updated:** 2026-10-02

**Overall score:** 9.3/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-02 | • 🔍 **Goal:** module docstring names the pattern and the rule it comes from<br>• 💬 **Messages:** every assertion says what to rename or move |
| **Complexity** | 8/10 | 2026-10-02 | • 🧮 **Raw complexity 2:** Concepts 1 (script naming) + Scope 0 (one folder) + Dependencies 0 + Prerequisites 1 (small `tmp_path` trees) |
| **Evidence of Need** | 9/10 | 2026-10-02 | • 🔗 **Target:** scripts were moved and renamed into verb groups on 2026-10-02, and nothing stopped new ones drifting |
| **Coverage** | 10/10 | 2026-10-02 | • 📊 **Counts:** 13 test functions and 16 assert statements, on the live config and on fake trees |
| **Structural Compliance** | 10/10 | 2026-10-02 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 10/10 | 2026-10-02 | • 🔍 **References:** passes against the current config |
| **Regression Value** | 9/10 | 2026-10-02 | • 🛡️ **Guard:** fails on a loose script, a wrong verb, a badly named folder or a one-script group |
| **Overall** | **9.3/10** | 2026-10-02 | • 💪 **Strongest:** Coverage, Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** none below 8/10 |

## 🔗 Related files

- `src/claude/_tests/scripts/test_script_naming.py` — the test being scored
- `src/claude/_rules/01_essentials/claude_usage_standards/naming_standards/_claude_naming_patterns.md` — the pattern it enforces
