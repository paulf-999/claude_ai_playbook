# 03_authoring_guidelines/

Meta-guidance for authoring and maintaining Claude config artifacts — rules that guide the creation and maintenance of rules, skills, agents, hooks, and other foundational artifacts.

## 📋 Contents

| File | Purpose | Type |
|------|---------|------|
| **authoring_agents.md** | Standards for agent creation: naming, structure, maturity levels, testing, scope boundaries | Instructional |
| **authoring_rules.md** | Standards for rule creation: naming, structure, directory placement, testing, scope boundaries | Instructional |
| **authoring_skills.md** | Standards for skill creation: naming, contract fields, structure, complexity scoring, testing, maturity levels | Instructional |

## 🎯 Why authoring_guidelines?

These rules guide the creation of other rules, skills, agents, and artifacts. They establish:
- **Consistent structure** across all config artifacts
- **Quality gates** before artifacts are proposed or finalized
- **Testing requirements** for enforcement artifacts
- **Maturity frameworks** for evaluating completeness and stability
- **Scope boundaries** to prevent feature creep and bloat

---

## 📐 Structure & Maturity

Authoring guidelines follow a **progressive maturity model**:

| Level | Artifact Status | Characteristics |
|-------|---|---|
| **Draft** | Speculative or one-time use | New concept; 5–8 evals; explores design space |
| **Tactical** | Battle-tested, recurring use | Solves real, recurring problem; 8–12 evals; used in 5+ sessions |
| **Strategic** | Core workflow, stable | Production-ready; 12+ evals; clear scope; <1 update/year |

---

## 🔗 Related

- **`01_essentials/`** — Foundational rules applied every session (guiding principles, behaviour, security, testing)
- **`02_claude_standards/`** — Quality gates and operational standards (behaviour, git, testing, security guardrails)
- **`04_claude_reference/`** — System knowledge and reference docs (design patterns, efficiency, MCP trust model)
- **`05_lazy_load/`** — Domain-specific rules (SQL, Airflow, Terraform, etc.); loaded on-demand only

---
