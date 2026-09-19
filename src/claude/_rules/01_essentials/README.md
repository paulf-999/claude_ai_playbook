# 01_essentials/

Foundational rules applied in every Claude session, regardless of task type or project.

## 📋 Contents

| File | Purpose | Type |
|------|---------|------|
| **claude_response_standards.md** | Response format, delivery cadence, timing measurement, and enforcement for substantive tasks | Instructional |
| **claude_usage_standards.md** | Usage standards: directory structure, naming, writing, editing conventions | Instructional |
| **guiding_principles.md** | Decision-making principles; prevents config bloat; establishes intentionality gates | Instructional |

## 🎯 Why essentials?

Every rule in this directory applies regardless of:
- **Project context** (works the same in all repos)
- **Task type** (safety, conduct, writing standards apply everywhere)
- **Removing it** would regularly produce wrong or unsafe behaviour

These rules form the foundation — violating them has broad impact.

## 📐 Structure

Each rule follows a consistent format:
- **Title** — descriptive, scans quickly
- **Purpose** — one sentence explaining the rule's existence
- **Scope** — which scenarios this rule covers
- **Guidance** — actionable advice (bullets, examples, decision trees)
- **Anti-patterns** — what NOT to do (flagged with ❌)

## 🔗 Related

- **`claude_usage_standards/`** — Child files for naming standards, writing style, directory structure
- **`behaviour/`** — Child files for implementation gates and behavioural guidance
- **`03_authoring_guidelines/`** — Meta-guidance for authoring rules, skills, and agents
- **`02_claude_standards/`** — Quality gates and operational standards (includes behaviour/, security.md, testing.md)
- **`04_claude_reference/`** — System knowledge and reference docs
- **`05_lazy_load/`** — Domain-specific rules (SQL, Airflow, Terraform, etc.)
