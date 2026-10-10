# Quality Scorecard — test_latency_optimisation.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.6/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and every assertion names the clause that broke |
| **Complexity** | 9/10 | 2026-09-30 | • 🧮 **Raw complexity 1:** Concepts 1 (the latency rule's guidance) + Scope 0 + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Incident:** the rule recommended temperatures of 1.5–2.0, but the API only accepts 0–1 and current models reject temperature |
| **Coverage** | 10/10 | 2026-10-01 | • 📊 **Counts:** 13 test functions and 18 assertions<br>• 🧩 **Checks:** effort table, the Opus 5.5 default, temperature warning, `max_tokens`, streaming and the measure-first steps |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** matches the API's effort and temperature behaviour as of 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🛡️ **Mutation check:** the old rule fails the no-temperature-above-1 check on `[1.5, 2.0]` |
| **Overall** | **9.6/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Clarity, Complexity and Evidence of Need (9/10) |

## 🔗 Related files

- `src/claude/_tests/rules/05_lazy_load/test_latency_optimisation.py` — the test being scored
- `src/claude/rules/_rules_lazy_load/latency_optimisation.md` — what the test guards
