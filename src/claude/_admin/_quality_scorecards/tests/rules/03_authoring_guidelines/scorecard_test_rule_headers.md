# Quality Scorecard — test_rule_headers.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 9.3/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Goal:** module docstring says what `applies_to` is and why the audit needs it<br>• 💬 **Messages:** the real-file scan names each rule and its problem |
| **Complexity** | 8/10 | 2026-10-01 | • 🧮 **Raw complexity 2:** Concepts 1 (the `applies_to` header) + Scope 1 (the always-on tiers of `_rules/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-10-01 | • 🔗 **Target:** `make audit_rule_usage` reads the header, so a missing or malformed one skews applied % |
| **Coverage** | 10/10 | 2026-10-01 | • 📊 **Counts:** 13 test functions and 16 assertions<br>• 🧩 **Cases:** one glob, several globs, `*`, missing, duplicate, misplaced, mixed `*`, prose, empty entry, children and body examples |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against all 14 always-on entry points |
| **Regression Value** | 9/10 | 2026-10-01 | • 🔴 **Red first:** failed on the real rules before the backfill, and passed after |
| **Overall** | **9.3/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/rules/03_authoring_guidelines/test_rule_headers.py` — the test being scored
- `src/claude/_rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md` — the standard it enforces
- `src/claude/_scripts/audit_rule_usage.py` — the script that reads the header
