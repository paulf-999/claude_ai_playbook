# Quality Scorecard — mcp_trust_model.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 8.0/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Fix the broken `/docs/mcp_servers.md` reference.
- Point the `security_guardrails.md` reference at `rules/02_claude_standards/security/_security_guardrails.md`.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 10/10 | 2026-09-28 | • 📋 **Excellent:** explicit trusted/untrusted boundary lists, a table of concrete injection patterns with example + response, a clear "flag and ask" escalation path |
| **Complexity** | 8/10 | 2026-09-28 | • 🧮 **Raw complexity 2:** 5 concepts (core principle, trust boundaries, what-not-to-do, injection patterns, secure practices), single file, no dependencies |
| **Evidence of Need** | 8/10 | 2026-09-28 | • 🔗 **Load-bearing:** MCP prompt injection is a real, actively-guarded-against risk class, cross-referenced by `security_guardrails.md` and `external_system_access.md` |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | 2026-09-28 | • ✅ **Compliant:** emoji headers throughout, Purpose statement, Contents section, trailing newline, well within the line limit |
| **Currency** | 4/10 | 2026-09-28 | • 🐛 **Broken reference:** "Playbook docs: `/docs/mcp_servers.md`" — confirmed via `find`, no such file exists anywhere in the repo<br>• 🐛 **Wrong filename:** "Related rules" cites `security_guardrails.md`, but the real file is `rules/02_claude_standards/security/_security_guardrails.md` (missing underscore, missing path) |
| **Test Coverage** | 9/10 | 2026-10-01 | • 🧪 **Dedicated test:** `test_lazy_load_rule_structure.py` checks its header, Purpose line, key sections, child links, relative links and Contents<br>• ✅ **Generic checks:** also passes `test_rules_structure.py` |
| **Overall** | **8.0/10** | 2026-10-01 | • 💪 **Strength:** the clearest injection-pattern documentation in this survey<br>• ⚠️ **Gap:** Currency (4/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/rules/_rules_lazy_load/mcp_trust_model.md` — the rule being scored
- `src/claude/rules/02_claude_standards/security/_security_guardrails.md` — Currency dimension (the real path the stale reference should point to)
- `docs/reference/claude_config/mcp/mcp_setup.md` — Currency dimension (closest real doc to the broken `/docs/mcp_servers.md` claim)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Broken doc reference:** "Playbook docs: `/docs/mcp_servers.md`" names a file that does not exist anywhere in this repo — confirmed via `find . -iname "mcp_servers.md"` returning nothing.
- 🐛 **Wrong filename reference:** "Related rules" cites `security_guardrails.md`, but the actual file is `rules/02_claude_standards/security/_security_guardrails.md`.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
