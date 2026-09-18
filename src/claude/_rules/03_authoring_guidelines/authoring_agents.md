# 🛠️ Agent Authoring

**Purpose:** Establish standardized process for creating agents that ensures clarity, consistency, and intentionality. One concept per agent.

---

## 🧭 Quick Navigation

**New agent author?** Start here in order:
1. **Core Standards** — Naming pattern, structure, maturity levels, testing requirements
2. **Decision Tree** — When to create an agent vs. rule vs. skill
3. **5-Step Creation Process** — Workflow: name → contract → AGENT.md → evals → score
4. **Hard Gates Checklist** — Final validation before finalizing

**Experienced author, need to refresh?** Jump to specific child files:
- **Scope Boundaries** — Defining what your agent does NOT do (`_scope_and_maturity.md`)
- **Maturity Justification** — Choosing Draft vs. Tactical vs. Strategic (`_scope_and_maturity.md`)
- **Common Mistakes** — Catch anti-patterns (`_common_mistakes.md`)

**Reviewing someone else's agent?** Use these child files:
- **Hard Gates Checklist** (below) — Verify completeness
- **Common Mistakes** — Catch anti-patterns
- **Maturity Justification** — Verify evidence-based maturity

---

## 📐 Core Standards

@~/.claude/_rules/03_authoring_guidelines/authoring_agents/_core_standards.md

## 🎯 Decision Tree & Creation Process

@~/.claude/_rules/03_authoring_guidelines/authoring_agents/_decision_tree_and_process.md

## 🚪 Scope Boundaries & Maturity Justification

@~/.claude/_rules/03_authoring_guidelines/authoring_agents/_scope_and_maturity.md

---

## ✅ Hard Gates Checklist

@~/.claude/_rules/03_authoring_guidelines/authoring_agents/_hard_gates_checklist.md

---

## 🚫 Common Mistakes & Anti-Patterns

@~/.claude/_rules/03_authoring_guidelines/authoring_agents/_common_mistakes.md

---

## 📚 References & Related Rules

**Naming & placement:**
- `naming_standards.md` — Self-describing naming principles
- `claude_directory_structure.md` — Directory organization patterns

**Authoring & testing:**
- `~/.claude/_templates/AGENT.md.template` — Agent template with examples
- `testing.md` — When tests are required; evals.yaml patterns

**Principles & maintenance:**
- `guiding_principles.md` — Intentionality principle; evidence-gathering methods
- `behaviour.md` — Safe defaults and decision-making patterns
- `claude_plans.md` — Review/approval gates during implementation

**Related agent standards:**
- `authoring_rules.md` — Rule creation standards (model for some agent patterns)
- `authoring_skills.md` — Skill creation standards (model for maturity levels, testing)

---

## 🔗 Related rules

- `claude_plans.md` — Review gates after each implementation phase
- `guiding_principles.md` — Intentionality; when to create new agents vs. enhance existing ones
- `testing.md` — Testing requirements for all artifacts including agents
