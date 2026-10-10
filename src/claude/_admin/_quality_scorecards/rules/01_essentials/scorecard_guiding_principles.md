# Quality Scorecard — guiding_principles.md

**Date Created:** 2026-09-21
**Date Updated:** 2026-10-01

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 10/10 | 2026-09-30 | • 📋 **Structure:** each principle has Description + Rationale + How-to-apply columns — actionable, not just aspirational<br>• ✅ **Density resolved:** table cells now use bold-keyword bullets, one sentence each (issue #122) |
| **Complexity** | 7/10 | 2026-09-28 | • 🧮 **Raw complexity 3:** 11 principles covers the whole Concepts range (capped at 6+)<br>• 📄 **Everything else 0:** single file, no dependencies, no fixtures |
| **Evidence of Need** | 9/10 | 2026-09-28 | • 🔗 **Active use:** cited by name across most other rules this session (`authoring_rules.md`, `_concurrent_sessions.md`, `_hooks_decision_framework.md`, etc.)<br>• ✅ **Not aspirational:** clearly in real, ongoing use |
| **Token Cost Justification** | 10/10 | 2026-09-28 | • 🎯 **Scope:** Tier 1, always-on, foundational — governs decision-making for every other rule in the config<br>• 💰 **Verdict:** cost is unambiguously earned |
| **Structural Compliance** | 9/10 | 2026-09-28 | • ✅ **Compliant:** emoji header, Purpose statement, trailing newline, and table usage all correct per `writing_style.md`<br>• 🌳 **No Related section — correctly:** this rule is the dependency-graph root, nothing to link *up* to<br>• 🚫 **Would go stale:** linking *down* to consumers would drift as more rules cite it — exactly what this rule's own "False truth rots silently" warns against |
| **Currency** | 9/10 | 2026-09-28 | • 🔍 **Check:** no stale references found<br>• ✅ **Result:** content matches how the config actually operates today<br>• 📚 **v1.1.0:** aligned with the Claude Code memory docs — 200-line size target, path-scoped rules, imports cost and hooks for enforcement (issue #157) |
| **Test Coverage** | 9/10 | 2026-10-01 | • 🧪 **Direct test exists:** `test_guiding_principles.py`, 13 functions, 9/10 — CLAUDE.md's imports follow the lazy-load, purpose-comment and tier rules<br>• ✅ **Fixed:** its lazy-load check used to look for a path that doesn't exist, so it could never fail |
| **Overall** | **9.0/10** | 2026-10-01 | • 💪 **Strength:** a strong, actively-used foundational rule<br>• ⚠️ **Gap:** Complexity (7/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/rules/01_essentials/guiding_principles.md` — the rule being scored
- `src/claude/_tests/rules/01_essentials/test_guiding_principles.py` — Test Coverage dimension
- `src/claude/rules/03_authoring_guidelines/authoring_rules.md` — Evidence of Need dimension
- `src/claude/rules/02_claude_standards/git/_concurrent_sessions.md` — Evidence of Need dimension
- `src/claude/rules/_rules_lazy_load/hooks_decision_framework.md` — Evidence of Need dimension
- `src/claude/rules/01_essentials/claude_usage_standards/writing_style.md` — Structural Compliance dimension
- `src/claude/rules/02_claude_standards/portable_paths.md` — Test Coverage dimension (the disclosed violation)

---

## 🚩 Pre-existing issue — found here, fixed separately

- 🐛 **Violation found:** `test_guiding_principles.py` (lines 32, 81) hardcoded `@~/.claude/` when parsing `@import` lines.
- 🚫 **Rule broken:** `portable_paths.md` forbids this — "never hardcode the `@~/.claude/` or `@~/claude/` import-prefix string when parsing `@import` lines."
- ✅ **Resolved:** fixed in PR #88, on its own hotfix branch rather than bundled into this scorecard PR.
- 📋 **Disposition:** per this config's pre-existing-issue disclosure rule — flagged here, fixed separately, not silently absorbed into scope.
