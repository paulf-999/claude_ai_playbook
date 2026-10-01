# Quality Scorecard — test_security_guardrails.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.1/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and every assertion names the clause that broke |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 1 (the guardrails) + Scope 2 (`security/` and `settings.json`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** Claude's own prompt-injection and secret-handling guardrails |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 12 test functions and 15 assertions<br>• 🧩 **Checks:** each injection, secret and permission clause, and the bad/good examples |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🐛 **Bug fixed:** the old checks matched words like "read" that any text contains, so they could never fail<br>• 🛡️ **Cross-check:** settings.json must allow none of the wildcards the rule calls too broad |
| **Overall** | **9.1/10** | 2026-10-01 | • 💪 **Strongest:** Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_security_guardrails.py` — the test being scored
- `src/claude/_rules/02_claude_standards/security/_security_guardrails.md` — what the test guards
