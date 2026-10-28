# Quality Scorecard — security.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 7.7/10

**Recommended improvements:**
- Change the Purpose line from "two concerns" to the three areas the rule now covers: secure coding, Claude's guardrails and MCP trust.
- Turn the two-sentence prose line under "Secure coding practices" into one bold-keyword bullet, or delete it, so every section matches the pointer-only style of the others.
- Give the "Claude's security guardrails" heading its own emoji, since 🔐 is also used on the H1 and on "Secure coding practices".
- Add a dated incident or usage record (for example, a prompt-injection attempt or a near-miss secret commit) to back the `miss_cost: high` claim.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-27 | • 🔍 **Clear index:** each section names one child and a one-line description of what it covers<br>• ⚠️ **Purpose mismatch:** line 9 says "two concerns", but the rule points to three children (coding, guardrails, MCP trust) |
| **Complexity** | 7/10 | 2026-10-27 | • 🧮 **Raw complexity 3:** Concepts 1 (three areas) + Scope 2 (`security/` plus `_rules_lazy_load/`) + Dependencies 0 + Prerequisites 0<br>• ✅ **Thin parent:** the content lives in the children, and the parent is a 42-line index |
| **Evidence of Need** | 6/10 | 2026-10-25 | • ⚠️ **No recorded incident:** the `miss_cost: high` header on line 5 states a cost, but this file names no dated incident, issue or usage record<br>• 🔗 **Indirect guard:** `test_rule_cross_references.py` checks that `settings.json` allows none of the wildcards the guardrails forbid, which is a guard, not evidence of past failures |
| **Token Cost Justification** | 9/10 | 2026-10-27 | • 🎯 **Justified always-on:** `applies_to: *` and the `loading:` header give a reason (secrets and injection can come up in any session)<br>• ✅ **Low cost:** the parent is only pointers, and the children load on their own |
| **Structural Compliance** | 8/10 | 2026-10-27 | • ✅ **Header and length:** has the version/created/updated header, a Purpose line, emoji headings, 42 lines, and a Contents section earned by 4 headings<br>• ⚠️ **Prose slip:** line 21 is two sentences of prose rather than bold-keyword bullets<br>• ⚠️ **Repeated emoji:** 🔐 is used on the H1 and on two `##` headings (lines 19 and 27) |
| **Currency** | 8/10 | 2026-10-27 | • ✅ **Pointers resolve:** all three `security/_*.md` children and `_rules_lazy_load/security_design.md` exist at commit 1705887<br>• ⚠️ **Description drift:** the "two concerns" Purpose was not updated when MCP trust became a third child |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Structural:** covered by `test_rules_structure.py` and `test_rule_headers.py`<br>• 🧪 **Pointers:** `test_rule_reachability.py` fails on a broken `Read on demand` pointer<br>• ⚠️ **Not run:** this review did not execute the suite, so passing is assumed from the files, not observed |
| **Overall** | **7.7/10** | 2026-10-27 | • 💪 **Lean index:** a cheap, safety-critical always-on parent whose pointers are checked by tests<br>• ⚠️ **Gaps:** the Purpose line no longer matches the rule, and no recorded incident backs the need |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/security.md` — the rule being scored
- `src/claude/rules/02_claude_standards/security/_code_security.md` — child named in the index (Clarity, Currency)
- `src/claude/rules/02_claude_standards/security/_security_guardrails.md` — child named in the index (Clarity, Currency)
- `src/claude/rules/02_claude_standards/security/_mcp_trust_model.md` — the third child the Purpose line leaves out (Clarity, Currency)
- `src/claude/rules/_rules_lazy_load/security_design.md` — on-demand pointer target (Complexity, Currency)
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — complexity formula (Complexity)
- `src/claude/_tests/rules/test_rule_cross_references.py` — guardrail wildcard check (Evidence of Need)
- `src/claude/_tests/rules/test_rules_structure.py` — structural test (Test Coverage)
- `src/claude/_tests/rules/03_authoring_guidelines/test_rule_headers.py` — header test (Test Coverage)
- `src/claude/_tests/_shared_checks/test_rule_reachability.py` — broken-pointer check (Test Coverage)
