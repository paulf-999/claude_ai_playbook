# Quality Scorecard — test_rule_reachability.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 9.6/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message |
| **Complexity** | 8/10 | 2026-10-01 | • 🧮 **Raw complexity 2:** Concepts 1 (the detector and its exemptions) + Scope 0 (temp trees) + Dependencies 0 + Prerequisites 1 (`tmp_path`) |
| **Evidence of Need** | 10/10 | 2026-10-01 | • 🔗 **Incident:** proves the detector that caught the `naming_standards.md` orphan bug |
| **Coverage** | 10/10 | 2000-01-01 | • 📊 **Counts:** 12 test functions and 20 assertions<br>• 🧩 **Edge cases:** nesting, broken imports, READMEs, templates, both config-dir names and the `_lazy_load/` segment match |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 10/10 | 2000-01-01 | • 🛡️ **Synthetic trees:** every exemption is proven on a fake tree, not just on today's config |
| **Overall** | **9.6/10** | 2026-10-01 | • 💪 **Strongest:** Evidence of Need, Coverage, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/test_rule_reachability.py` — the test being scored
- `src/claude/_tests/_rule_reachability.py` — the detector under test
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — runs the detector on the real config
