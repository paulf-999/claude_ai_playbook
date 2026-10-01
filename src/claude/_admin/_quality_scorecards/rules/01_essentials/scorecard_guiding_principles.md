# Quality Scorecard — guiding_principles.md

**Date Created:** 2026-09-21
**Date Updated:** 2026-09-30

**Overall score:** 8.6/10

**Recommended improvements:**
- Raise `test_guiding_principles.py`'s assertion/function count — its self-rated 3/10 quality is the main drag on this file's Test Coverage score.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 10/10 | • 📋 **Structure:** each principle has Description + Rationale + How-to-apply columns — actionable, not just aspirational<br>• ✅ **Density resolved:** table cells now use bold-keyword bullets, one sentence each (issue #122) |
| **Complexity** | 7/10 | • 🧮 **Raw complexity 3:** 11 principles covers the whole Concepts range (capped at 6+)<br>• 📄 **Everything else 0:** single file, no dependencies, no fixtures |
| **Evidence of Need** | 9/10 | • 🔗 **Active use:** cited by name across most other rules this session (`authoring_rules.md`, `_concurrent_sessions.md`, `_hooks_decision_framework.md`, etc.)<br>• ✅ **Not aspirational:** clearly in real, ongoing use |
| **Token Cost Justification** | 10/10 | • 🎯 **Scope:** Tier 1, always-on, foundational — governs decision-making for every other rule in the config<br>• 💰 **Verdict:** cost is unambiguously earned |
| **Structural Compliance** | 9/10 | • ✅ **Compliant:** emoji header, Purpose statement, trailing newline, and table usage all correct per `writing_style.md`<br>• 🌳 **No Related section — correctly:** this rule is the dependency-graph root, nothing to link *up* to<br>• 🚫 **Would go stale:** linking *down* to consumers would drift as more rules cite it — exactly what this rule's own "False truth rots silently" warns against |
| **Currency** | 9/10 | • 🔍 **Check:** no stale references found<br>• ✅ **Result:** content matches how the config actually operates today<br>• 📚 **v1.1.0:** aligned with the Claude Code memory docs — 200-line size target, path-scoped rules, imports cost and hooks for enforcement (issue #157) |
| **Test Coverage** | 6/10 | • 🧪 **Exists:** `test_guiding_principles.py` has 3 behavioral tests, all passing<br>• 📉 **Self-rated:** the test file's own metadata still says 3/10 quality (low assertion count)<br>• ✅ **Fixed:** the `@~/.claude/` hardcoding violation is resolved in PR #88 |
| **Overall** | **8.6/10** | • 💪 **Strength:** a strong, actively-used foundational rule<br>• ⚠️ **Gap:** test file's own quality score (3/10) is the main drag on this dimension |

## 🔗 Related files

- `src/claude/_rules/01_essentials/guiding_principles.md` — the rule being scored
- `src/claude/_tests/rules/01_essentials/test_guiding_principles.py` — Test Coverage dimension
- `src/claude/_rules/03_authoring_guidelines/authoring_rules.md` — Evidence of Need dimension
- `src/claude/_rules/02_claude_standards/git/_concurrent_sessions.md` — Evidence of Need dimension
- `src/claude/_rules/05_lazy_load/hooks_decision_framework.md` — Evidence of Need dimension
- `src/claude/_rules/01_essentials/claude_usage_standards/writing_style.md` — Structural Compliance dimension
- `src/claude/_rules/02_claude_standards/portable_paths.md` — Test Coverage dimension (the disclosed violation)

---

## 🚩 Pre-existing issue — found here, fixed separately

- 🐛 **Violation found:** `test_guiding_principles.py` (lines 32, 81) hardcoded `@~/.claude/` when parsing `@import` lines.
- 🚫 **Rule broken:** `portable_paths.md` forbids this — "never hardcode the `@~/.claude/` or `@~/claude/` import-prefix string when parsing `@import` lines."
- ✅ **Resolved:** fixed in PR #88, on its own hotfix branch rather than bundled into this scorecard PR.
- 📋 **Disposition:** per this config's pre-existing-issue disclosure rule — flagged here, fixed separately, not silently absorbed into scope.
