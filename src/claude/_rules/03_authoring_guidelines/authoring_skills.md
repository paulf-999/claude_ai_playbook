<!-- version: 3.0.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-09-29 -->
# 🛠️ Skill Authoring

**Purpose:** Create focused, well-documented, properly tested skills. One concept per skill.

Work through the children in order, and finish with the Hard Gates Checklist before submitting.

---

## 📐 Core Standards

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_core_standards.md

## 🎯 Trigger Design

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_trigger_design.md

## 🚪 Scope Boundaries & Low-Maintenance Design

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_scope_and_maintenance.md

## 🧹 No Orphaned Files

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_no_orphaned_files.md

---

## ✅ Hard Gates Checklist

@~/.claude/_rules/03_authoring_guidelines/authoring_skills/_hard_gates_checklist.md

---

## 📁 File Organization

Minimal, focused structure. Each skill directory contains **only**:

```
skill_name/
├── SKILL.md               # User-facing overview (5 sections, ~60 lines)
├── skill.contract.yaml    # Machine-readable contract (scope, triggers, maturity)
├── scorecard_skill_name.md # 7-dimension table only — justification goes in SKILL.md
├── reference/             # Runtime docs Claude reads while executing (keep SKILL.md lean)
│   ├── _implementation.md # Phases, logic, error handling
│   └── _formats.md        # Standards, validation, examples (if applicable)
└── tests/                 # Test scenarios — kept out of the skill root so a
    ├── evals.yaml          # non-technical reader isn't met with "evals.yaml" first
    └── README.md           # Plain-language: what evals.yaml is, how many scenarios, why
```

**`scorecard_<skill_name>.md` lives at skill root, not in `reference/`** — it's an authoring/review artifact (assessed when the skill is created or audited), not something Claude reads while executing the skill. Everything in `reference/` is runtime behavioral documentation.

**`evals.yaml` always lives in `tests/`, never at skill root** — "evals" is jargon; a `tests/` folder reads as familiar to a non-technical browser of the skill directory. `tests/README.md` is mandatory alongside it, in plain language, so anyone who does open the folder isn't left guessing what the file is.

**Nothing else.** No `templates/`, `patterns/`, `references/`, or domain-specific subdirectories. Keep scope tight, keep structure clean.

**Naming applies going forward:** existing skills created before this naming change keep their `quality_scorecard.md` filename — rename to `scorecard_<skill_name>.md` only when that skill is next touched, not as a standalone rename-only pass.
