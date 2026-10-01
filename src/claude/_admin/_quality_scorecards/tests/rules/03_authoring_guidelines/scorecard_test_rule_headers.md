# Quality Scorecard — test_rule_headers.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 9.1/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Goal:** module docstring says what `applies_to` and `miss_cost` are and why the audit needs them<br>• 💬 **Messages:** the real-file scans name each rule and its problem |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 1 (`applies_to`, `miss_cost`, the trigger rule) + Scope 2 (`_rules/` and `hooks/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-10-01 | • 🔗 **Target:** `make audit_rule_usage` reads both headers<br>• 🔒 **Trigger rule:** a costly lazy rule that relies on recall can be missed silently |
| **Coverage** | 10/10 | 2026-10-01 | • 📊 **Counts:** 20 test functions and 30 assertions<br>• 🧩 **Cases:** parser accept and reject cases for both headers, trigger detection, and scans of all 36 entry points |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against all 14 always-on and 22 lazy entry points |
| **Regression Value** | 9/10 | 2026-10-01 | • 🔴 **Red first:** the `applies_to` and `miss_cost` scans each failed on the real rules before their backfill |
| **Overall** | **9.1/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10), from reading `hooks/` as well as `_rules/` |

## 🔗 Related files

- `src/claude/_tests/rules/03_authoring_guidelines/test_rule_headers.py` — the test being scored
- `src/claude/_rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md` — the standard it enforces
- `src/claude/_scripts/audit_rule_usage.py` — the script that reads the headers
