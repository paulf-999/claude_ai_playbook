# _rules/

Documentation for the rules directory — describes the four-tier system for how rules are organized by audience and purpose, and the distinction between instructional and enforcement rules.

## 🎯 Directory structure

Rules are organized into four numbered tiers, each with a distinct purpose and audience:

- **`01_essentials/`** — Foundational principles and conventions meant for **user/stakeholder understanding** (behaviour, naming, writing standards, authoring skills/rules)
- **`02_claude_standards/`** — Foundational quality gates that **Claude must apply** to all work (security, testing) — NOT user-facing
- **`03_claude_reference/`** — Technical/meta-knowledge about **how the system works** (efficiency, git workflow, loading strategy, external systems) — reference material
- **`04_lazy_load/`** — Domain-specific rules loaded on demand; never imported into the main context (SQL, Airflow, dbt, Terraform, etc.)

## 🎯 Design principle: Audience-based organization

Rules are organized by **who they're for and what they do**, not by enforcement mechanism:

| Tier | Audience | Purpose | Token cost |
|---|---|---|---|
| **01_essentials** | Users & stakeholders | Conventions and principles they need to understand | ~150/session |
| **02_claude_standards** | Claude (internally) | Foundational quality gates Claude applies to all work | ~150/session |
| **03_claude_reference** | Claude (internally) | Technical reference material about the system | ~150/session |
| **04_lazy_load** | Domain-specific | Rules loaded only when needed in that domain | ~0 baseline |

**Key insight:** 01, 02, and 03 are always-on (justifiable baseline cost). 04 is lazy-loaded to preserve context.

## 🔄 Instructional vs. Enforcement Rules

Not all rules have mechanical triggers. Understand the difference:

### Instructional rules
- **What:** Rules that Claude reads and follows — human guidance informing behavior
- **Examples:** behaviour.md, security.md, writing_style.md, guiding_principles.md, testing.md
- **Testing:** Structure tests only (file quality, line limits) in `_tests/rules/`; intended behavior validated by behavior tests
- **Enforcement:** By Claude's reasoning — no automatic block

### Enforcement rules
- **What:** Rules with mechanical triggers — hooks, linters, validators that block or inject context
- **Examples:** naming_conventions (enforced by `hook_enforcement_naming_convention.sh`), dir_structure validation
- **Testing:** Must have corresponding tests in `_tests/hooks/` — verify the hook works as documented
- **Enforcement:** Automatic — can block operations or force corrections
- **Per testing.md:** Adding or modifying an enforcement hook requires a corresponding test

## 🏗️ Tier definitions

### **01_essentials/** — User-facing conventions and principles
- **Who it's for:** Users, stakeholders, teams reading/implementing these standards
- **Scope:** Naming conventions, behaviour principles, writing style, authoring guidance
- **Examples:** naming_standards.md, behaviour.md, writing_style.md, authoring_skills.md
- **Imported:** Yes, always-on (~150 tokens/session)

### **02_claude_standards/** — Foundational quality gates (Claude-facing)
- **Who it's for:** Claude's internal operation (not meant for stakeholder understanding)
- **Scope:** Security practices, testing requirements — blocking standards Claude applies to all code
- **Examples:** security.md (secure coding + prompt injection defence), testing.md (test requirements)
- **Imported:** Yes, always-on (~150 tokens/session)

### **03_claude_reference/** — System/platform knowledge and reference material
- **Who it's for:** Claude's reference when implementing standards; understanding the system
- **Scope:** How the config system works, git workflow patterns, efficiency guidance, external system access
- **Examples:** loading_strategy_rules.md, git.md, external_system_access.md, claude_efficiency.md
- **Imported:** Yes, always-on (~150 tokens/session)

### **04_lazy_load/** — Domain-specific rules (lazy-loaded)
- **Who it's for:** Domain specialists (SQL, Airflow, dbt, Terraform, etc.)
- **Scope:** Rules specific to a single language, tool, or domain
- **Examples:** style_guide_standards/sql.md, style_guide_standards/airflow.md, latency_optimization.md
- **Imported:** No, loaded on-demand only
- **Note:** if a rule applies in most sessions regardless of task type, it belongs in tier 01/02/03 — not here.
- **Hook required:** every file in 04_lazy_load/ should have a corresponding enforcement hook or be a pure reference document (consulted explicitly, not auto-triggered)

## 🎚️ Tier placement decision tree

Use this decision tree when deciding where a new rule belongs.

```
Is this rule domain-specific?
├─ YES  → 04_lazy_load/
│  (SQL, Airflow, dbt, Terraform, language-specific style guides)
│
└─ NO   → Continue...
   Is it meant for users/stakeholders to understand?
   ├─ YES → 01_essentials/
   │  (Naming conventions, behaviour principles, writing standards, authoring guidance)
   │
   └─ NO  → Continue...
      Is it a foundational quality gate Claude must enforce?
      ├─ YES → 02_claude_standards/
      │  (Security, testing, prompt injection defence, code safety)
      │
      └─ NO  → 03_claude_reference/
         (System knowledge: how config works, efficiency patterns, workflow guidance)
```

**Default:** when in doubt, prefer lazy-load or 03_claude_reference — every always-on file (01/02/03) grows the base context (~150 tokens/session).
