<!-- version: 3.2.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-09-30 -->
# 🛠️ Skill Authoring

**Purpose:** Create focused, well-documented, properly tested skills. One concept per skill.

Before creating or reviewing a skill, read the children below in order, and finish with the Hard Gates Checklist before submitting.

---

## 📚 Read on demand

- **Read on demand:** `~/.claude/_rules/03_authoring_guidelines/authoring_skills/_lazy_load/_core_standards.md` — naming, SKILL.md structure, contract fields and maturity levels.
- **Read on demand:** `~/.claude/_rules/03_authoring_guidelines/authoring_skills/_lazy_load/_trigger_design.md` — how to write trigger phrases so the skill runs when users ask for it.
- **Read on demand:** `~/.claude/_rules/03_authoring_guidelines/authoring_skills/_lazy_load/_scope_and_maintenance.md` — declaring `not_for` boundaries and designing for stability.
- **Read on demand:** `~/.claude/_rules/03_authoring_guidelines/authoring_skills/_lazy_load/_no_orphaned_files.md` — making sure every file in the skill is referenced.
- **Read on demand:** `~/.claude/_rules/03_authoring_guidelines/authoring_skills/_lazy_load/_hard_gates_checklist.md` — the final checklist before submitting a skill.

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

- **Exception — a skill's own script:** a skill that runs code may keep that one script at skill root, named for what it does (e.g. `capture_session_prompts.py`) and referenced from SKILL.md; its pytest file lives in `_tests/skills/<skill_name>/`.

**Naming applies going forward:** existing skills created before this naming change keep their `quality_scorecard.md` filename — rename to `scorecard_<skill_name>.md` only when that skill is next touched, not as a standalone rename-only pass.
