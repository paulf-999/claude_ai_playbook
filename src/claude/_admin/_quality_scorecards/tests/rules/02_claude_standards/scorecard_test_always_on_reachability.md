# Quality Scorecard — test_always_on_reachability.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.1/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 1 (reachability of always-on rules) + Scope 2 (`CLAUDE.md` and tiers 01–04) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 10/10 | 2026-10-01 | • 🔗 **Incident:** `naming_standards.md` described children it never imported (2026-09-17) |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 13 test functions and 15 assertions<br>• 🧩 **Checks:** each tier, broken imports, the lazy-load tier, `aliases.md`, and the `_lazy_load/` pointer contract |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 9/10 | 2026-10-01 | • 🛡️ **Exemption contract:** fails if a `_lazy_load/` child has no 'Read on demand' pointer, so the exemption can't hide a real orphan |
| **Overall** | **9.1/10** | 2026-10-01 | • 💪 **Strongest:** Evidence of Need, Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — the test being scored
- `src/claude/_tests/_rule_reachability.py` — the detector it runs
- `src/claude/_rules/03_authoring_guidelines/authoring_rules.md` — the "wire up every documented child" gate it enforces
