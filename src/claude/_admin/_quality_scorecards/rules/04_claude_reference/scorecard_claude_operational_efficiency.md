# Quality Scorecard — claude_operational_efficiency.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 7.1/10

**Recommended improvements:**
- Add dedicated structural tests for the parent and its imported children (`claude_when_to_delegate.md`, `turn_budgets.md`, `external_system_access.md`, `task_request_conventions.md`, `mcp_server_toggling.md`), rather than relying on adjacent hook/automation tests.
- Cite a specific incident or recurring problem that motivated this rule.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-09-28 | • 📋 **Concrete pattern:** "Flag, don't block" comes with a worked example ("Flagging: this read duplicates one already in context") |
| **Complexity** | 7/10 | 2026-09-28 | • 🧮 **Raw complexity 3:** 3 inline concepts (token awareness, default behaviours, intervention mode) plus 4 imported children |
| **Evidence of Need** | 7/10 | 2026-09-28 | • 🔗 **Reasonable but uncited:** no specific incident referenced, and no test exists for the parent or any of its 4 children by name |
| **Token Cost Justification** | 8/10 | 2026-09-28 | • 🎯 **Scope:** Tier 4, always-on — token/turn discipline applies broadly, though less safety-critical than Tier 1/2 rules |
| **Structural Compliance** | 8/10 | 2026-09-28 | • ✅ **Compliant:** Contents matches headings, emoji headers, trailing newline, 78 lines |
| **Currency** | 8/10 | 2026-09-28 | • 🔍 **Check:** no stale references spotted in the parent's own inline content |
| **Test Coverage** | 4/10 | 2026-09-28 | • 🧪 **No direct match:** no test file references this rule's own children (`claude_when_to_delegate.md`, `turn_budgets.md`, `external_system_access.md`, `task_request_conventions.md`, `mcp_server_toggling.md`) by name<br>• 🔍 **Closest hits are adjacent, not this rule:** `test_enforcement_mcp_stale_settings.py` and `test_automation_controls.py` test related hook/automation mechanisms, not this rule's content directly |
| **Overall** | **7.1/10** | 2026-09-28 | • 💪 **Strength:** clear, concrete operational guidance<br>• ⚠️ **Gap:** none of its 4 children have a dedicated test |

## 🔗 Related files

- `src/claude/_rules/04_claude_reference/claude_operational_efficiency.md` — the rule being scored
- `src/claude/_rules/04_claude_reference/claude_operational_efficiency/_claude_when_to_delegate.md` — Test Coverage dimension (untested child)
- `src/claude/_rules/05_lazy_load/turn_budgets.md` — Test Coverage dimension (untested, read on demand)
- `src/claude/_rules/04_claude_reference/claude_operational_efficiency/_task_request_conventions.md` — Test Coverage dimension (untested child)
- `src/claude/_tests/hooks/enforcement/test_enforcement_mcp_stale_settings.py` — Test Coverage dimension (adjacent, not direct)
- `src/claude/_tests/rules/05_lazy_load/test_automation_controls.py` — Test Coverage dimension (adjacent, not direct)
