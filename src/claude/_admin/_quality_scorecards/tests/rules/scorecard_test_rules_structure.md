# Quality Scorecard — test_rules_structure.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 1 (file size, emoji headings, context-budget sections) + Scope 2 (`_rules/` and `_reference/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** every rule loads into every session, so its size and shape matter |
| **Coverage** | 9/10 | 2026-09-30 | • 📊 **Counts:** 12 test functions and 16 assertions<br>• 🧩 **Detectors:** the header exemption, `~~~` fences and URL-only References are proven on samples |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 9/10 | 2026-10-01 | • 🛡️ **Non-vacuous:** fails if the scan finds no rule files or lets READMEs and lazy-load files in |
| **Overall** | **9.0/10** | 2026-10-01 | • 💪 **Strongest:** Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/test_rules_structure.py` — the test being scored
- `src/claude/_rules/01_essentials/claude_usage_standards/writing_style.md` — the format rules it guards
- `src/claude/_tests/rules/test_rules_structure_layout.py` — the layout and import half of the old test
