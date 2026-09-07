# 01_essentials/

Foundational rules applied in every Claude session, regardless of task type or project.

## 📋 Contents

| File | Purpose | Type |
|------|---------|------|
| **authoring_rules.md** | Pre-creation checklist, directory placement, and testing requirements for rules | Instructional |
| **authoring_skills.md** | Standards for skill creation, naming, complexity scoring, and review | Instructional |
| **claude_response_standards.md** | Response format, delivery cadence, timing measurement, and enforcement for substantive tasks | Instructional |
| **claude_usage_standards.md** | Usage standards: directory structure, naming, writing, editing conventions | Instructional |
| **guiding_principles.md** | Decision-making principles; prevents config bloat; establishes intentionality gates | Instructional |
| **security.md** | Secure coding standards — secrets, auth, input validation, dependencies | Instructional |
| **testing.md** | When tests are required; what to validate; test design patterns | Instructional |

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

- **`testing/`** — Child files for testing standards
- **`claude_usage_standards/`** — Child files for naming standards, writing style, directory structure, editing standards
- **`authoring_skills/`** — Child files for skill authoring standards
- **`03_lazy_load/`** — Domain-specific rules (SQL, Airflow, Terraform, etc.)
- **`02_claude_standards/`** — Quality gates and operational standards (includes behaviour/)
- **`02_claude_internal/`** — Claude Code operational rules (not for general audience)
