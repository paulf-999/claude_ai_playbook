# Quality Scorecard — security.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-11

**Overall score:** 8.1/10

**Recommended improvements:**
- Add a "Related rules" section cross-linking to `behaviour.md` and other rules touching conduct/injection concerns.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-09-28 | • 📋 **Purpose is clear:** two concerns cleanly separated (secure coding vs. Claude's own conduct)<br>• 🔍 **Very thin:** 30 lines, almost entirely Contents + 3 imports, little independent substance of its own |
| **Complexity** | 8/10 | 2026-09-28 | • 🧮 **Raw complexity 2:** pure 2-concept router (code security, guardrails) plus 1 reference doc |
| **Evidence of Need** | 8/10 | 2026-09-28 | • 🔗 **Self-evidently necessary:** security guidance for both generated code and Claude's own conduct<br>• 📉 **No in-file incident:** no specific past failure cited in this parent |
| **Token Cost Justification** | 9/10 | 2026-09-28 | • 🎯 **Scope:** Tier 2, always-on, safety-critical by nature |
| **Structural Compliance** | 6/10 | 2026-09-28 | • ✅ **Compliant:** emoji headers, Purpose statement, trailing newline<br>• ❌ **Gap:** no "Related rules" section at all — unlike every sibling in this tier, no cross-links to `behaviour.md` or other rules touching conduct/injection concerns |
| **Currency** | 8/10 | 2026-09-28 | • 🔍 **Check:** both children and the reference doc resolve; no stale references found |
| **Test Coverage** | 10/10 | 2026-10-11 | • 🧪 **Rubric met:** parent and children pass `test_rules_structure.py`, and none records an incident<br>• 🔗 **Settings check:** `test_rule_cross_references.py` fails if `settings.json` allows a wildcard the guardrails forbid |
| **Overall** | **8.1/10** | 2026-10-11 | • 💪 **Strength:** clean separation of concerns between the two children<br>• ⚠️ **Gap:** Structural Compliance (6/10) |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/security.md` — the rule being scored
- `src/claude/_tests/rules/test_rule_cross_references.py` — Test Coverage dimension
- `src/claude/rules/02_claude_standards/security/_code_security.md` — Test Coverage dimension (untested child)
