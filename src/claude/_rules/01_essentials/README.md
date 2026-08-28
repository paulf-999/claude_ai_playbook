# 01_essentials/

Foundational rules applied in every Claude session, regardless of task type or project.

## 📋 Contents

| File | Purpose | Type |
|------|---------|------|
| **authoring_rules.md** | Pre-creation checklist, directory placement, and testing requirements for rules | Instructional |
| **authoring_skills.md** | Standards for skill creation, naming, complexity scoring, and review | Instructional |
| **conventions/naming_standards.md** | Self-describing naming for files, directories, identifiers | Instructional |
| **conventions/writing_style.md** | Writing conventions for all content — responses, docs, tickets, rules | Instructional |
| **conventions/claude_directory_structure.md** | Directory organization and file structure conventions | Instructional |
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
- **`conventions/`** — Child files for naming standards, writing style, directory structure
- **`skill_authoring/`** — Child files for skill authoring standards
- **`03_lazy_load/`** — Domain-specific rules (SQL, Airflow, Terraform, etc.)
- **`02_claude_standards/`** — Quality gates and operational standards (includes behaviour/)
- **`02_claude_internal/`** — Claude Code operational rules (not for general audience)
