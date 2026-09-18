# 📐 Rule Directory Tier Classification

**Purpose:** Explain how Claude rules are organized into five directory tiers (01_essentials through 05_lazy_load), each representing a distinct purpose and scope. Tier assignment determines loading strategy (always-on import vs. lazy-loaded on-demand).

**Scope:** Rules in `~/.claude/_rules/` are organized into five tiers. Directory placement determines whether a rule is always-on (imported in CLAUDE.md) or lazy-loaded (in `_rules/05_lazy_load/`), and defines the rule's scope and application.

---

## 📜 Historical Note

This document has been through two reorganizations: an original five-tier classification (Tier 1–5), a four-tier directory-based structure (Q3 2026), and the current five-tier structure that split authoring guidance (rules/skills/agents) out into its own `03_authoring_guidelines/` tier. Always trust the current directory structure over any prose description — see `claude_directory_structure.md`.

---

## 📁 Tier Definitions

@~/.claude/_rules/04_claude_reference/claude_rule_system/claude_rule_classification/_tier_definitions.md

---

## 📊 Distribution Summary

| Tier | Directory | Scope | Loading |
|---|---|---|---|
| **1** | `01_essentials/` | User-facing conventions, foundational principles | Always-on (non-negotiable) |
| **2** | `02_claude_standards/` | Blocking standards, enforcement, operational conduct | Always-on (non-negotiable) |
| **3** | `03_authoring_guidelines/` | Meta-guidance for authoring rules, skills, agents | Always-on |
| **4** | `04_claude_reference/` | System knowledge, platform guidance, architecture | Mostly always-on; some candidates for lazy-load |
| **5** | `05_lazy_load/` | Domain-specific style guides, niche tools | Lazy-loaded (on-demand only) |

---

## 🔄 Loading Decision Framework

**Always-on (imported in CLAUDE.md):**
- Safety-critical (behaviour, guiding_principles)
- Quality gates (testing, security)
- High session coverage (>70%)
- Foundational for all work (naming, writing style)

**Lazy-load (in `05_lazy_load/`):**
- Domain-specific (style guides for SQL, Airflow, dbt, etc.)
- Session coverage <70%
- Clear trigger (command invocation, tool use)
- No safety cost if omitted in irrelevant sessions

**See also:** `claude_rule_loading_strategy.md` for the detailed always-on vs. lazy-load decision tree.

---

## 🔗 Related References

- **Loading strategy decision tree:** `claude_rule_loading_strategy.md` — Authoritative guide for always-on vs. lazy-load placement
- **Tier-specific guidance:**
  - `01_essentials/` — Foundational rules (safety, user-facing, quality)
  - `02_claude_standards/` — Standard enforcement and quality gates
  - `03_authoring_guidelines/` — Rule/skill/agent authoring standards
  - `04_claude_reference/` — This directory; system knowledge and platform guidance
  - `05_lazy_load/` — Domain-specific rules (load on-demand)
