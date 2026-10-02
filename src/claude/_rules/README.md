# _rules/

Documentation for the rules directory — describes the five-tier system for how rules are organized by audience and purpose, and the distinction between instructional and enforcement rules.

## 🎯 Directory structure

Rules are organized into five numbered tiers, each with a distinct purpose and audience:

- **`01_essentials/`** — Foundational principles and conventions meant for **user/stakeholder understanding** (behaviour, naming, writing standards)
- **`02_claude_standards/`** — Foundational quality gates that **Claude must apply** to all work (security, testing) — NOT user-facing
- **`03_authoring_guidelines/`** — Meta-guidance for authoring **rules, skills, agents** (how to create and maintain config artifacts)
- **`04_claude_reference/`** — Technical/meta-knowledge about **how the system works** (efficiency, loading strategy, external systems) — reference material
- **`05_lazy_load/`** — Domain-specific rules loaded on demand; never imported into the main context (SQL, Airflow, dbt, Terraform, etc.)

## 🎯 Design principle: Audience-based organization

Rules are organized by **who they're for and what they do**, not by enforcement mechanism:

| Tier | Audience | Purpose | Size (≈ tokens) |
|---|---|---|---|
| **01_essentials** | Users & stakeholders | Conventions and principles they need to understand | ≈10.7k every session (12 imported files) |
| **02_claude_standards** | Claude (internally) | Foundational quality gates Claude applies to all work | ≈13.7k every session (19 imported files) |
| **03_authoring_guidelines** | Claude (internally) | Meta-guidance for authoring rules, skills, agents | ≈4.2k every session (5 imported files) |
| **04_claude_reference** | Claude (internally) | Technical reference material about the system | ≈2.7k every session (5 imported files) |
| **05_lazy_load** | Domain-specific | Rules loaded only when needed in that domain | 0 baseline (≈59k if all 83 files were read) |

**Key insight:** 01, 02, 03, and 04 are always-on, about 34.4k tokens together before `_reference/` imports. 05 is lazy-loaded to preserve context.

**Note:** sizes are characters ÷ 4, measured 2026-10-01 over the files `CLAUDE.md` actually imports (a tier's `_lazy_load/` children don't count) — `make audit_rule_usage` reports the current total.

## 🔄 Instructional vs. Enforcement Rules

Not all rules have mechanical triggers. Understand the difference:

### Instructional rules
- **What:** Rules that Claude reads and follows — human guidance informing behavior
- **Examples:** behaviour.md, security.md, writing_style.md, guiding_principles.md
- **Testing:** Structure tests only (file quality, line limits) in `_tests/rules/`; intended behavior validated by behavior tests
- **Enforcement:** By Claude's reasoning — no automatic block

### Enforcement rules
- **What:** Rules with mechanical triggers — hooks, linters, validators that block or inject context
- **Examples:** naming_conventions (enforced by `hook_enforcement_naming_convention.sh`)
- **Testing:** Must have corresponding tests in `_tests/hooks/` — verify the hook works as documented
- **Enforcement:** Automatic — can block operations or force corrections
- **Per testing.md:** Adding or modifying an enforcement hook requires a corresponding test

## 🔗 Where Related links live

Rule files are `@import`ed every session, so every line in them costs always-on context. To keep that cost down:

- **Related links:** each file's parent, sibling and dependency links sit in its tier `README.md` under "🔗 Related rules", one `###` per file — never in a `## Related` section inside the rule (#121).
  - **Why:** READMEs aren't `@import`ed, so the links cost nothing until someone opens the README.
  - **`_reference/`:** follows the same pattern, with its links in `_reference/README.md`.
- **Contents sections:** add one only when the rule has 3 or more real `##` headings (#120).
- **Child indexes:** a lazy-loaded parent that is the only route to its children keeps those links in the rule, under a non-Related heading (e.g. `python.md`'s "📂 Child files").
- **Enforced by:** `test_rules_structure.py` — `test_no_related_section_outside_readmes` and `test_contents_section_only_with_three_real_headings`.

## 🏗️ Tier definitions

### **01_essentials/** — User-facing conventions and principles
- **Who it's for:** Users, stakeholders, teams reading/implementing these standards
- **Scope:** Naming conventions, behaviour principles, writing style, authoring guidance
- **Examples:** naming_standards.md, behaviour.md, writing_style.md, authoring_skills.md
- **Imported:** Yes, always-on (≈10.7k tokens/session)

### **02_claude_standards/** — Foundational quality gates (Claude-facing)
- **Who it's for:** Claude's internal operation (not meant for stakeholder understanding)
- **Scope:** Security practices and git workflow — blocking standards Claude applies to all code
- **Examples:** security.md (secure coding + prompt injection defence), git.md (commits, branches and PRs)
- **Imported:** Yes, always-on (≈13.7k tokens/session)

### **03_authoring_guidelines/** — Meta-guidance for authoring config artifacts
- **Who it's for:** Claude when creating or maintaining rules, skills, agents, hooks
- **Scope:** Standards for authoring; structure, naming, testing, maturity levels, and per-file metadata headers for artifacts
- **Examples:** authoring_rules.md (children: common mistakes, hard-gates checklist), authoring_skills.md, shared_standards/_claude_config_metadata.md (shared version/created/updated standard)
- **Imported:** Yes, always-on (≈4.2k tokens/session)

### **04_claude_reference/** — System/platform knowledge and reference material
- **Who it's for:** Claude's reference when implementing standards; understanding the system
- **Scope:** How the config system works, git workflow patterns, efficiency guidance, external system access
- **Examples:** loading_strategy_rules.md, git.md, external_system_access.md, claude_efficiency.md
- **Imported:** Yes, always-on (≈2.7k tokens/session)

### **05_lazy_load/** — Domain-specific rules (lazy-loaded)
- **Who it's for:** Domain specialists (SQL, Airflow, dbt, Terraform, etc.)
- **Scope:** Rules specific to a single language, tool, or domain
- **Examples:** style_guide_standards/sql.md, style_guide_standards/airflow.md, latency_optimisation.md, turn_budgets.md
- **Imported:** No, loaded on-demand only
- **Note:** if a rule applies in most sessions regardless of task type, it belongs in tier 01/02/03/04 — not here.
- **Hook required:** every file in 05_lazy_load/ should have a corresponding enforcement hook or be a pure reference document (consulted explicitly, not auto-triggered)

## 🎚️ Tier placement decision tree

Use this decision tree when deciding where a new rule belongs.

```
Is this rule domain-specific?
├─ YES  → 05_lazy_load/
│  (SQL, Airflow, dbt, Terraform, language-specific style guides)
│
└─ NO   → Continue...
   Is it meta-guidance for authoring artifacts (rules, skills, agents)?
   ├─ YES → 03_authoring_guidelines/
   │  (How to create/maintain rules, skills, agents, hooks)
   │
   └─ NO  → Continue...
      Is it meant for users/stakeholders to understand?
      ├─ YES → 01_essentials/
      │  (Naming conventions, behaviour principles, writing standards)
      │
      └─ NO  → Continue...
         Is it a foundational quality gate Claude must enforce?
         ├─ YES → 02_claude_standards/
         │  (Security, testing, prompt injection defence, code safety)
         │
         └─ NO  → 04_claude_reference/
            (System knowledge: how config works, efficiency patterns, workflow guidance)
```

**Default:** when in doubt, prefer lazy-load or 04_claude_reference — every always-on file (01/02/03/04) adds its full size to every session.
