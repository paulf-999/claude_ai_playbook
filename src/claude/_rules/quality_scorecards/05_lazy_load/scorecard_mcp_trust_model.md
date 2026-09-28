# Quality Scorecard — mcp_trust_model.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 6.8/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Fix the "Playbook docs: `/docs/mcp_servers.md`" reference — no such file exists anywhere in this repo; point to a real doc (e.g. `docs/reference/claude_config/mcp/mcp_setup.md`) or remove the claim.
- Fix the `security_guardrails.md` reference to its real path and filename: `_rules/02_claude_standards/security/_security_guardrails.md`.
- Add a dedicated structural test for this file — it's security-relevant and currently has zero coverage.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 10/10 | • 📋 **Excellent:** explicit trusted/untrusted boundary lists, a table of concrete injection patterns with example + response, a clear "flag and ask" escalation path |
| **Complexity** | 8/10 | • 🧮 **Raw complexity 2:** 5 concepts (core principle, trust boundaries, what-not-to-do, injection patterns, secure practices), single file, no dependencies |
| **Evidence of Need** | 8/10 | • 🔗 **Load-bearing:** MCP prompt injection is a real, actively-guarded-against risk class, cross-referenced by `security_guardrails.md` and `external_system_access.md` |
| **Token Cost Justification** | N/A | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | • ✅ **Compliant:** emoji headers throughout, Purpose statement, Contents section, trailing newline, well within the line limit |
| **Currency** | 4/10 | • 🐛 **Broken reference:** "Playbook docs: `/docs/mcp_servers.md`" — confirmed via `find`, no such file exists anywhere in the repo<br>• 🐛 **Wrong filename:** "Related rules" cites `security_guardrails.md`, but the real file is `_rules/02_claude_standards/security/_security_guardrails.md` (missing underscore, missing path) |
| **Test Coverage** | 2/10 | • 🧪 **Gap:** confirmed via `find` — zero test files reference `mcp_trust_model` by name |
| **Overall** | **6.8/10** | • 💪 **Strength:** the clearest injection-pattern documentation in this survey<br>• ⚠️ **Gap:** two stale references and no dedicated test, for a security-relevant rule |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/mcp_trust_model.md` — the rule being scored
- `src/claude/_rules/02_claude_standards/security/_security_guardrails.md` — Currency dimension (the real path the stale reference should point to)
- `docs/reference/claude_config/mcp/mcp_setup.md` — Currency dimension (closest real doc to the broken `/docs/mcp_servers.md` claim)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Broken doc reference:** "Playbook docs: `/docs/mcp_servers.md`" names a file that does not exist anywhere in this repo — confirmed via `find . -iname "mcp_servers.md"` returning nothing.
- 🐛 **Wrong filename reference:** "Related rules" cites `security_guardrails.md`, but the actual file is `_rules/02_claude_standards/security/_security_guardrails.md`.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
