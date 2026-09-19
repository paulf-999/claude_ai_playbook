# 🛠️ Skill Authoring

**Purpose:** Create focused, well-documented, properly tested skills. One concept per skill.

---

## 🧭 Quick Navigation

**New skill author?** Start here in order:
1. **Core Standards** — Naming pattern, SKILL.md structure, specification fields, testing standards
2. **7-Step Process** — Workflow: name → specification → SKILL.md → reference/ → evals.yaml → score → submit
3. **Hard Gates Checklist** — Final validation before submitting

**Experienced author, need to refresh?** Jump to specific child files:
- **Scope Boundaries** — If designing what your skill does NOT do (`_scope_and_maintenance.md`)
- **Maturity Justification** — If choosing Draft vs. Tactical vs. Strategic maturity (`_maturity_justification.md`)
- **Low-Maintenance Design** — If updating an existing skill or preventing maintenance debt (`_scope_and_maintenance.md`)
- **Common Mistakes** — If you're stuck or uncertain about a choice (`_common_mistakes_and_security.md`)

**Reviewing someone else's skill?** Use these child files:
- **Hard Gates Checklist** (below) — Verify completeness and compliance
- **Common Mistakes** — Catch anti-patterns and design flaws
- **Maturity Justification** — Verify evidence-based maturity choice

---

## 📐 Core Standards

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_core_standards.md

## 🎯 Trigger Design & Testing Standards

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_trigger_design_and_testing.md

## 🚀 Creation Process

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_creation_process.md

## 🚪 Scope Boundaries & Low-Maintenance Design

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_scope_and_maintenance.md

## 🧹 No Orphaned Files

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_no_orphaned_files.md

## 📈 Maturity Justification

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_maturity_justification.md

## ⚠️ Common Mistakes & Security

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_common_mistakes_and_security.md

---

## ✅ Hard Gates Checklist

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_hard_gates_checklist.md

---

## 📚 Reference

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_skill_structure_contract.md

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_skill_quality_checklist.md

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_skill_review_framework.md

---

## 📁 File Organization

Minimal, focused structure. Each skill directory contains **only**:

```
skill_name/
├── SKILL.md               # User-facing overview (5 sections, ~60 lines)
├── skill.contract.yaml    # Machine-readable contract (scope, triggers, maturity)
├── evals.yaml             # Test scenarios (10–15, organized by phase)
├── _quality_scorecard.md  # Dimensions, maturity justification, design rationale
└── reference/             # Runtime docs Claude reads while executing (keep SKILL.md lean)
    ├── _implementation.md # Phases, logic, error handling
    └── _formats.md        # Standards, validation, examples (if applicable)
```

**`_quality_scorecard.md` lives at skill root, not in `reference/`** — it's an authoring/review artifact (assessed when the skill is created or audited), not something Claude reads while executing the skill. Everything in `reference/` is runtime behavioral documentation.

**Nothing else.** No `templates/`, `patterns/`, `references/`, or domain-specific subdirectories. Keep scope tight, keep structure clean.

---

## 🔗 Related Rules

- **naming_standards.md** — Foundational naming principles; skill naming patterns in child file
- **testing.md** — Skill testing requirements by maturity level
- **authoring_rules.md** — General rule authoring process (complementary to skill authoring)
