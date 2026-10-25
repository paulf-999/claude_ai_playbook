# Quality Scorecard — mcp_trust_model.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 7.4/10

**Recommended improvements:**
- Make line 27's trusted GitHub and Jira results agree with line 33's untrusted comments and titles
- Change line 59's "data first, instructions second" to match line 19's "data, not instructions"
- Say where line 60's suspicious-content audit note should go
- Record evidence of need, such as a real injection attempt

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-25 | • ⚠️ **Contradictory framing:** `_mcp_trust_model.md` line 6 says the rule treats "all MCP responses as untrusted input", but lines 25–29 list a "Trusted (safe to accept)" set.<br>• ⚠️ **Overlapping categories:** line 27 trusts "Responses from GitHub, Jira", while line 33 distrusts "Comments, descriptions, pull request titles from GitHub/Jira", so two readers could classify the same Jira response differently.<br>• ⚠️ **Weakened principle:** line 59 says "data first, instructions second", which goes against line 19's "data, not instructions".<br>• ⚠️ **No destination:** line 60 says to "note it for audit" without saying where. |
| **Complexity** | 8/10 | 2026-10-25 | • 🧮 **Raw complexity 2:** Concepts 2 (trust boundaries, injection patterns, read practices and write practices), Scope 0 (one file), Dependencies 0, Prerequisites 0. See `_complexity_scoring.md`.<br>• ⚠️ **Four jobs in one file:** the read and write practices at lines 54–66 are a separate concern from trust classification. |
| **Evidence of Need** | 5/10 | 2026-10-25 | • ❓ **No recorded incident:** neither `_mcp_trust_model.md` nor its tests record a real injection attempt, issue or PR. The patterns at lines 47–50 are made-up examples.<br>• 🔗 **Only a placement reason:** `test_always_on_reachability.py` lines 83–84 record why the rule moved to always-on ("a high miss cost"), not a problem that actually happened. |
| **Token Cost Justification** | 7/10 | 2026-10-25 | • ⚖️ **Arguable:** it is always-on (tier 02 child) because `test_always_on_reachability.py` lines 83–84 say "no file type marks their sessions", but many sessions use no MCP server at all.<br>• ⚠️ **Partial overlap:** line 41 says the core rules already live in `_security_guardrails.md`, which is also always-on. The generic read and write lists at lines 56–66 add cost without being specific to MCP. |
| **Structural Compliance** | 8/10 | 2026-10-25 | • ✅ **Header and layout:** metadata on lines 1–3, an emoji H1, a Purpose line and 66 lines. The Contents section is justified by 4 `##` headings and matches them.<br>• ⚠️ **Style slip:** the numbered items at lines 57–66 use `**Keyword** —` instead of the bold-keyword-plus-colon form.<br>• ⚠️ **Out of place:** the bullet at line 43 sits between the intro sentence on line 41 and the table it introduces. |
| **Currency** | 9/10 | 2026-10-25 | • ✅ **Current:** the only file it names, `_security_guardrails.md` (line 41), exists beside it in `rules/02_claude_standards/security/`. |
| **Test Coverage** | 9/10 | 2026-10-25 | • 🧪 **Structural guard:** `_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` line 51 checks the header, Purpose line, links, Contents entries and the headings "Core principle", "Injection attack patterns" and "Secure MCP practices".<br>• ✅ **No regression test needed:** the rule records no incident. |
| **Overall** | **7.4/10** | 2026-10-25 | • 💪 **Strength:** concrete injection-pattern table and a structural test guarding the key headings.<br>• ⚠️ **Gap:** the trusted and untrusted categories contradict each other, and there is no recorded evidence of a real incident. |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/security/_mcp_trust_model.md` — the rule being scored
- `src/claude/rules/02_claude_standards/security/_security_guardrails.md` — Currency dimension (the real path the stale reference should point to)
- `docs/reference/claude_config/mcp/mcp_setup.md` — Currency dimension (closest real doc to the broken `/docs/mcp_servers.md` claim)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Broken doc reference:** "Playbook docs: `/docs/mcp_servers.md`" names a file that does not exist anywhere in this repo — confirmed via `find . -iname "mcp_servers.md"` returning nothing.
- 🐛 **Wrong filename reference:** "Related rules" cites `security_guardrails.md`, but the actual file is `rules/02_claude_standards/security/_security_guardrails.md`.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
