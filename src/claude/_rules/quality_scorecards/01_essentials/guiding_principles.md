# Quality Scorecard — guiding_principles.md

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 📋 **Structure:** each principle has Description + Rationale + How-to-apply columns — actionable, not just aspirational<br>• 🔍 **Friction:** table density is the only drawback |
| **Complexity** | 7/10 | • 🧮 **Raw complexity 3:** 10 principles covers the whole Concepts range (capped at 6+)<br>• 📄 **Everything else 0:** single file, no dependencies, no fixtures |
| **Evidence of Need** | 9/10 | • 🔗 **Active use:** cited by name across most other rules this session (`authoring_rules.md`, `_concurrent_sessions.md`, `_hooks_decision_framework.md`, etc.)<br>• ✅ **Not aspirational:** clearly in real, ongoing use |
| **Token Cost Justification** | 10/10 | • 🎯 **Scope:** Tier 1, always-on, foundational — governs decision-making for every other rule in the config<br>• 💰 **Verdict:** cost is unambiguously earned |
| **Structural Compliance** | 7/10 | • ✅ **Compliant:** emoji header, Purpose statement, trailing newline, and table usage all correct per `writing_style.md`<br>• ❌ **Gap:** no `## 🔗 Related` section, unlike almost every other rule file in this config |
| **Currency** | 9/10 | • 🔍 **Check:** no stale references found<br>• ✅ **Result:** content matches how the config actually operates today |
| **Test Coverage** | 5/10 | • 🧪 **Exists:** `test_guiding_principles.py` has 3 behavioral tests, all passing<br>• 📉 **Self-rated:** the test file's own metadata says 3/10 quality<br>• 🚩 **Violation:** hardcodes the `@~/.claude/` import prefix, against `portable_paths.md`'s own rule |
| **Overall** | **8.0/10** | • 💪 **Strength:** a strong, actively-used foundational rule<br>• ⚠️ **Gaps:** missing Related section, plus a pre-existing, unrelated quality issue in its test file |

## 🔗 Related files

- `src/claude/_rules/01_essentials/guiding_principles.md` — the rule being scored
- `src/claude/_tests/rules/01_essentials/test_guiding_principles.py` — Test Coverage dimension
- `src/claude/_rules/03_authoring_guidelines/authoring_rules.md` — Evidence of Need dimension
- `src/claude/_rules/02_claude_standards/git/_concurrent_sessions.md` — Evidence of Need dimension
- `src/claude/_rules/04_claude_reference/claude_conduct/task_request_conventions/_hooks_decision_framework.md` — Evidence of Need dimension
- `src/claude/_rules/01_essentials/claude_usage_standards/writing_style.md` — Structural Compliance dimension
- `src/claude/_rules/02_claude_standards/portable_paths.md` — Test Coverage dimension (the disclosed violation)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Violation:** `test_guiding_principles.py` (lines 32, 81) hardcodes `@~/.claude/` when parsing `@import` lines.
- 🚫 **Rule broken:** `portable_paths.md` explicitly forbids this — "never hardcode the `@~/.claude/` or `@~/claude/` import-prefix string when parsing `@import` lines."
- ✅ **Confirmed:** the test's own metadata header self-reports `Test quality score: 3/10`.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
