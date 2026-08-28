# 📋 Rules Loading Strategy

**Principle:** Lazy-load by default. Always-on rules must block or apply everywhere.

Every import costs ~100-200 tokens/session. Only rules that justify this cost stay always-on.

---

## Source of Truth

Don't rely on a separate decision document. Check these directly:

- **CLAUDE.md** — which rules are actually imported (always-on)
- **Filesystem structure:**
  - `01_essentials/` — foundational, user-facing, safety-critical rules
  - `02_claude_standards/` — quality gates and enforcement rules
  - `03_claude_reference/` — system knowledge and platform guidance
  - `04_lazy_load/` — domain-specific rules (loaded on-demand)
- **Individual rule files** — each rule's `Purpose` statement explains why it's placed where it is

---

## When Adding a Rule

1. Read CLAUDE.md to see what's currently imported
2. Check the directory structure to understand the tier system
3. Assess: Does this rule apply to >70% of sessions? Is it blocking/safety-critical?
4. Decision on placement involves context (session coverage, criticality, token cost) that requires human judgment — not a flowchart

If unsure, lazy-load it. Always-on rules are the exception, not the default.

---

## Related References

- **Tier classification:** `claude_rule_classification.md` — explains the four-tier directory structure
- **CLAUDE.md** — authoritative source of always-on imports and their rationale

---
