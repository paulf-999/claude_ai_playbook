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

---

## 🔗 Related rules

Parent, sibling and dependency links for each file in this tier — kept here, not in the file, because READMEs aren't `@import`ed (#121).

### `claude_response_standards.md`

- `writing_style.md` — Writing conventions and progressive disclosure
- `behaviour.md` — Safe defaults and decision-making patterns
- `guiding_principles.md` — Intentionality and efficiency principles
- On demand: `05_lazy_load/response_standards_enforcement.md` — how this standard is enforced turn-to-turn

### `claude_usage_standards/claude_directory_structure/_claude_directory_naming.md`

- **Parent:** `claude_directory_structure.md` — directory organization and naming overview
- **Sibling:** `_claude_directory_organisation.md` — the full directory tree and auto-generated vs. user-created distinction
- **Related:** `naming_standards.md` → `_naming_principles.md` — foundational naming principles for all identifiers
- **Related:** `naming_standards.md` → `_claude_naming_patterns.md` — detailed patterns for hooks, skills, and rules

### `claude_usage_standards/claude_directory_structure/_claude_directory_organisation.md`

- **Parent:** `claude_directory_structure.md` — entry point; organisation and naming overview
- **Sibling:** `_claude_directory_naming.md` — naming patterns for files and directories
- **Related:** `writing_style.md` → `_multifile_document_organisation.md` — when to split documents into parent + child files
- **Related:** `authoring_rules.md` — directory placement for new rules (01_essentials, 02_claude_standards, 03_authoring_guidelines, 04_claude_reference, 05_lazy_load)

### `claude_usage_standards/claude_directory_structure/_file_structure_validation.md`

- `claude_directory_structure.md` — Authoritative naming and placement rules
- `naming_standards.md` — Foundational naming principles
- `behaviour.md` → "Before acting" → "Plan approval" — validate structure before proceeding with complex changes

### `claude_usage_standards/claude_directory_structure.md`

- `naming_standards.md` — General naming principles for all identifiers; see child file `_naming_principles.md` for foundational concepts
- `authoring_rules.md` — Directory placement rules for new rules (01_essentials, 02_claude_standards, 03_authoring_guidelines, 04_claude_reference, 05_lazy_load)
- `writing_style.md` → `_multifile_document_organisation.md` — When to create subdirectories for multi-file documents

### `claude_usage_standards/naming_standards/_claude_naming_patterns.md`

**Parent & siblings:**
- **Parent:** `naming_standards.md` — entry point for all naming conventions
- **Sibling:** `_naming_principles.md` — foundational naming principles (self-describing, offer options, snake_case, name for scale)
- **Related:** `claude_directory_structure.md` → `_claude_directory_naming.md` — directory and file naming conventions

**Detailed authoring guides:**
- **authoring_skills.md** — Full skill naming convention, domain list, examples
- **authoring_rules.md** — Rule naming standards, directory placement (01_essentials, 02_claude_standards, 03_authoring_guidelines, 04_claude_reference, 05_lazy_load), pre-creation checklist

### `claude_usage_standards/naming_standards/_naming_principles.md`

- **Parent:** `naming_standards.md` — entry point; loads these principles + pattern details
- **Sibling:** `_claude_naming_patterns.md` — detailed naming patterns for hooks, skills, rules
- **Related:** `claude_directory_structure.md` → `_claude_directory_naming.md` — naming rules for directories and files
- **Related:** `claude_directory_structure.md` → `_claude_directory_organisation.md` — directory structure and prefix conventions

### `claude_usage_standards/naming_standards.md`

- `claude_directory_structure.md` — Directory organization and naming conventions for `~/.claude/`
- `authoring_rules.md` — Rule naming standards and directory placement (01_essentials, 02_claude_standards, 03_authoring_guidelines, 04_claude_reference, 05_lazy_load)
- `writing_style.md` → `_multifile_document_organisation.md` — File organization conventions; when to split into parent + child files

### `claude_usage_standards.md`

- `guiding_principles.md` — foundational decision-making principles
- `authoring_rules.md`, `authoring_skills.md` — apply these conventions when creating new rules/skills
