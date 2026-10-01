# Quality Scorecard — test_writing_style.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.4/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and every assertion names the clause that broke |
| **Complexity** | 9/10 | 2026-09-30 | • 🧮 **Raw complexity 1:** Concepts 1 (writing_style.md clauses) + Scope 0 + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** `writing_style.md` is imported every session and shapes every response |
| **Coverage** | 10/10 | 2026-10-01 | • 📊 **Counts:** 11 test functions and 23 assertions<br>• 🧩 **New:** one sentence per bullet, British spelling, underscore dates in file names and the multifile child |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 9/10 | 2026-10-01 | • 🛡️ **Dates:** fails if a hyphenated `YYYY-MM-DD_` file-name pattern creeps back in |
| **Overall** | **9.4/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Clarity, Complexity, Evidence of Need and Regression Value (9/10) |

## 🔗 Related files

- `src/claude/_tests/rules/01_essentials/test_writing_style.py` — the test being scored
- `src/claude/_rules/01_essentials/claude_usage_standards/writing_style.md` — what the test guards
