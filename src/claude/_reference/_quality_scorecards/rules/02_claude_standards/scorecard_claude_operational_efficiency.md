# Quality Scorecard — claude_operational_efficiency.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-11

**Overall score:** 8.0/10

**Recommended improvements:**
- Cite a specific incident or recurring problem that motivated this rule.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-09-28 | • 📋 **Concrete pattern:** "Flag, don't block" comes with a worked example ("Flagging: this read duplicates one already in context") |
| **Complexity** | 7/10 | 2026-09-28 | • 🧮 **Raw complexity 3:** 3 inline concepts (token awareness, default behaviours, intervention mode) plus 4 imported children |
| **Evidence of Need** | 7/10 | 2026-09-28 | • 🔗 **Reasonable but uncited:** no specific incident referenced, and no test exists for the parent or any of its 4 children by name |
| **Token Cost Justification** | 8/10 | 2026-09-28 | • 🎯 **Scope:** Tier 4, always-on — token/turn discipline applies broadly, though less safety-critical than Tier 1/2 rules |
| **Structural Compliance** | 8/10 | 2026-09-28 | • ✅ **Compliant:** Contents matches headings, emoji headers, trailing newline, 78 lines |
| **Currency** | 8/10 | 2026-09-28 | • 🔍 **Check:** no stale references spotted in the parent's own inline content |
| **Test Coverage** | 10/10 | 2026-10-11 | • 🧪 **Rubric met:** parent and children pass `test_rules_structure.py`, and none records an incident<br>• 🔗 **Children:** `test_rule_cross_references.py` checks every named child resolves, none is orphaned and Contents match headings |
| **Overall** | **8.0/10** | 2026-10-11 | • 💪 **Strength:** clear, concrete operational guidance<br>• ⚠️ **Gap:** Evidence of Need (7/10), with no cited incident |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency.md` — the rule being scored
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_claude_when_to_delegate.md` — Test Coverage dimension (untested child)
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_turn_budgets.md` — Test Coverage dimension (untested child)
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_task_request_conventions.md` — Test Coverage dimension (untested child)
- `src/claude/_tests/hooks/enforcement/test_enforcement_mcp_stale_settings.py` — Test Coverage dimension (adjacent, not direct)
