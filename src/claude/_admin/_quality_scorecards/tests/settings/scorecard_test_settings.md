# Quality Scorecard — test_settings.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.3/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message that says what to fix |
| **Complexity** | 9/10 | 2026-09-30 | • 🧮 **Raw complexity 1:** Concepts 1 (permissions and secrets in `settings.json`) + Scope 0 (one file) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards `settings.json` against the rules in `security.md` |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 12 test functions and 19 assertions<br>• 🧩 **New:** over-broad destructive allows, entries in both allow and deny, and the 90-day transcript retention |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 9/10 | 2026-10-01 | • 🛡️ **Secrets:** the secrets check now matches real key shapes, where the old one asserted nothing |
| **Overall** | **9.3/10** | 2026-10-01 | • 💪 **Strongest:** Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** none below 9/10 |

## 🔗 Related files

- `src/claude/_tests/settings/test_settings.py` — the test being scored
- `src/claude/settings.json` — what the test guards
- `src/claude/_rules/02_claude_standards/security/_security_guardrails.md` — the permission guidance it enforces
