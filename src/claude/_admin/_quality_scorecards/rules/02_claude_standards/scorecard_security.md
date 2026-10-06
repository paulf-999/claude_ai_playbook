# Quality Scorecard — security.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 7.7/10

**Recommended improvements:**
- Add a "Related rules" section cross-linking to `behaviour.md` and other rules touching conduct/injection concerns.
- Add dedicated tests for the `_code_security.md` child and the `security.md` parent file itself.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-09-28 | • 📋 **Purpose is clear:** two concerns cleanly separated (secure coding vs. Claude's own conduct)<br>• 🔍 **Very thin:** 30 lines, almost entirely Contents + 3 imports, little independent substance of its own |
| **Complexity** | 8/10 | 2026-09-28 | • 🧮 **Raw complexity 2:** pure 2-concept router (code security, guardrails) plus 1 reference doc |
| **Evidence of Need** | 8/10 | 2026-09-28 | • 🔗 **Self-evidently necessary:** security guidance for both generated code and Claude's own conduct<br>• 📉 **No in-file incident:** no specific past failure cited in this parent |
| **Token Cost Justification** | 9/10 | 2026-09-28 | • 🎯 **Scope:** Tier 2, always-on, safety-critical by nature |
| **Structural Compliance** | 6/10 | 2026-09-28 | • ✅ **Compliant:** emoji headers, Purpose statement, trailing newline<br>• ❌ **Gap:** no "Related rules" section at all — unlike every sibling in this tier, no cross-links to `behaviour.md` or other rules touching conduct/injection concerns |
| **Currency** | 8/10 | 2026-09-28 | • 🔍 **Check:** both children and the reference doc resolve; no stale references found |
| **Test Coverage** | 7/10 | 2026-10-01 | • 🧪 **Partial:** `test_security_guardrails.py` (12 functions) checks each guardrail in `_security_guardrails.md` and that `settings.json` allows no forbidden wildcard<br>• ⚠️ **Untested:** `_code_security.md` child and the parent itself have no dedicated test |
| **Overall** | **7.7/10** | 2026-10-01 | • 💪 **Strength:** clean separation of concerns between the two children<br>• ⚠️ **Gap:** missing Related section and half the children untested |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/security.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_security_guardrails.py` — Test Coverage dimension
- `src/claude/rules/02_claude_standards/security/_code_security.md` — Test Coverage dimension (untested child)
