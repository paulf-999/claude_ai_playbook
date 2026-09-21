# Quality Scorecard — guiding_principles.md

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | Each principle has Description + Rationale + How-to-apply columns — actionable, not just aspirational. Table density is the only friction. |
| **Complexity** | 7/10 | Raw complexity 3: 10 principles covers the whole Concepts range (capped at 6+), but single file, no dependencies, no fixtures. |
| **Evidence of Need** | 9/10 | Actively cited by name across most other rules this session (`authoring_rules.md`, `_concurrent_sessions.md`, `_hooks_decision_framework.md`, etc.) — clearly in real use, not aspirational. |
| **Token Cost Justification** | 10/10 | Tier 1, always-on, foundational — governs decision-making for every other rule in the config. Cost is unambiguously earned. |
| **Structural Compliance** | 7/10 | Emoji header, Purpose statement, trailing newline, and table usage all correct per `writing_style.md` — but has no `## 🔗 Related` section, unlike almost every other rule file in this config. |
| **Currency** | 9/10 | No stale references found; content matches how the config actually operates today. |
| **Test Coverage** | 5/10 | `test_guiding_principles.py` exists and passes (3 behavioral tests), but self-rates 3/10 quality and hardcodes the `@~/.claude/` import prefix — a direct violation of `portable_paths.md`'s own rule against hardcoding that exact string. |
| **Overall** | **8.0/10** | Strong, actively-used foundational rule; the two real gaps are a missing Related section and a pre-existing, unrelated quality issue in its test file. |

---

## 🚩 Pre-existing issue disclosed, not fixed

`test_guiding_principles.py` (line 32, 81) hardcodes `@~/.claude/` when parsing `@import` lines — `portable_paths.md` explicitly forbids this ("Never hardcode the `@~/.claude/` or `@~/claude/` import-prefix string when parsing `@import` lines"). Confirmed via the test's own metadata header (`Test quality score: 3/10`). Out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
