# Rules overview

Documentation for the rule folders, `rules/` and `_rules_lazy_load/` — describes the tier system for how rules are organized by audience and purpose, and the distinction between instructional and enforcement rules.

## 🎯 Directory structure

Claude Code loads every `.md` under `rules/` by itself, so the folder decides how a rule loads. Rules are organized into four numbered tiers under `rules/`, plus a read-on-demand folder beside it:

- **`01_essentials/`** — Foundational principles and conventions meant for **user/stakeholder understanding** (behaviour, naming, writing standards)
- **`02_claude_standards/`** — Foundational quality gates and operational conduct that **Claude must apply** to all work (security, testing, efficiency) — NOT user-facing
- **`03_authoring_guidelines/`** — Meta-guidance for authoring **rules, skills, agents** (how to create and maintain config artifacts)
- **`04_path_scoped/`** — Domain-specific rules with `paths:` frontmatter, loaded only when a matching file is open (SQL, Airflow, dbt, Terraform, etc.)
- **`_rules_lazy_load/`** — Beside `rules/`: rules and bulky children read on demand, never loaded automatically, plus these tier READMEs

## 🎯 Design principle: Audience-based organization

Rules are organized by **who they're for and what they do**, not by enforcement mechanism:

| Tier | Audience | Purpose | Size (≈ tokens) |
|---|---|---|---|
| **01_essentials** | Users & stakeholders | Conventions and principles they need to understand | ≈10.7k every session (12 files) |
| **02_claude_standards** | Claude (internally) | Foundational quality gates and operational conduct Claude applies to all work | ≈16.4k every session (24 files) |
| **03_authoring_guidelines** | Claude (internally) | Meta-guidance for authoring rules, skills, agents | ≈4.2k every session (5 files) |
| **04_path_scoped** + **_rules_lazy_load** | Domain-specific | Rules loaded only when needed in that domain | 0 baseline (≈59k across both if all files were read) |

**Key insight:** 01, 02 and 03 are always-on, about 34.4k tokens together. 04 and `_rules_lazy_load/` load only when needed, to preserve context.

**Note:** sizes are characters ÷ 4, measured 2026-10-01 over the files that loaded every session (on-demand children don't count) — `make audit_rule_usage` reports the current total.

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

Files under `rules/` tiers 01–03 load every session, so every line in them costs always-on context. To keep that cost down:

- **Related links:** each file's parent, sibling and dependency links sit in its tier README in `_rules_lazy_load/_tier_readmes/` under "🔗 Related rules", one `###` per file, for tiers 02–05 only (`01_essentials/` keeps no links, #310) — never in a `## Related` section inside the rule (#121).
  - **Why:** READMEs live outside `rules/` and never load by themselves, so the links cost nothing until someone opens the README.
  - **`_reference/`:** follows the same pattern, with its links in `_reference/README.md`.
- **Contents sections:** add one only when the rule has 3 or more real `##` headings (#120).
- **Child indexes:** a lazy-loaded parent that is the only route to its children keeps those links in the rule, under a non-Related heading (e.g. `python.md`'s "📂 Child files").
- **Enforced by:** `test_rules_structure.py` — `test_no_related_section_outside_readmes` and `test_contents_section_only_with_three_real_headings`.

## 🏗️ Tier definitions

### **01_essentials/** — User-facing conventions and principles
- **Who it's for:** Users, stakeholders, teams reading/implementing these standards
- **Scope:** Naming conventions, behaviour principles, writing style, authoring guidance
- **Examples:** naming_standards.md, behaviour.md, writing_style.md, authoring_skills.md
- **Loaded:** Yes, always-on (≈10.7k tokens/session)

### **02_claude_standards/** — Foundational quality gates (Claude-facing)
- **Who it's for:** Claude's internal operation (not meant for stakeholder understanding)
- **Scope:** Security practices and git workflow — blocking standards Claude applies to all code
- **Examples:** security.md (secure coding + prompt injection defence), git.md (commits, branches and PRs)
- **Loaded:** Yes, always-on (≈13.7k tokens/session)

### **03_authoring_guidelines/** — Meta-guidance for authoring config artifacts
- **Who it's for:** Claude when creating or maintaining rules, skills, agents, hooks
- **Scope:** Standards for authoring; structure, naming, testing, maturity levels, and per-file metadata headers for artifacts
- **Examples:** authoring_rules.md (children: common mistakes, hard-gates checklist), authoring_skills.md, shared_standards/_claude_config_metadata.md (shared version/created/updated standard)
- **Loaded:** Yes, always-on (≈4.2k tokens/session), except `authoring_agents.md`, which has `paths:` and loads with agent files

### **04_path_scoped/** and **_rules_lazy_load/** — Domain-specific rules (lazy-loaded)
- **Who it's for:** Domain specialists (SQL, Airflow, dbt, Terraform, etc.)
- **Scope:** Rules specific to a single language, tool, or domain
- **Examples:** `04_path_scoped/style_guide_standards/sql.md` and `airflow.md` (with `paths:`), `_rules_lazy_load/latency_optimisation.md` and `turn_budgets.md` (pointers)
- **Loaded:** `04_path_scoped/` with matching files; `_rules_lazy_load/` only when Claude follows a pointer
- **Note:** if a rule applies in most sessions regardless of task type, it belongs in tier 01/02/03 — not here.
- **Hook required:** every lazy file should have a corresponding enforcement hook or be a pure reference document (consulted explicitly, not auto-triggered)

## 🎚️ Tier placement decision tree

Use this decision tree when deciding where a new rule belongs.

```
Is this rule domain-specific?
├─ YES  → rules/04_path_scoped/ (tied to a file type, with paths:) or _rules_lazy_load/ (read on demand)
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
         Is it a quality gate or operational conduct Claude applies to all work?
         ├─ YES → 02_claude_standards/
         │  (Security, testing, prompt injection defence, efficiency, delegation)
         │
         └─ NO  → _rules_lazy_load/
            (Read on demand: reference material and niche guidance)
```

**Default:** when in doubt, prefer lazy-load — every always-on file (01/02/03) adds its full size to every session.
