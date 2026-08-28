# 🎯 Naming Principles — Foundational Concepts

**Purpose:** Establish the foundational principles that apply to ALL naming conventions — identifiers, files, directories, and artefacts.

---

## 📋 Core Principles

### 🎯 Self-describing

A name must be unambiguous without context. If it could apply to anything, it is too vague.

- **Standard:** Readers should understand the purpose of a file or identifier from its name alone, without needing to open it first
- **Example:** `naming_standards.md` (clear) vs. `standards.md` (ambiguous — standards for what?)

### 📋 Offer options

Before creating a new file or directory, propose 3–4 name candidates with a recommendation.

- **Standard:** Do not proceed unilaterally with naming decisions; naming is the user's call
- **When:** Any time you're naming a new file, directory, hook, skill, or rule
- **Format:** Present options with a recommendation marked (Recommended); explain trade-offs

### 🔤 snake_case

Lowercase only, words separated by underscores — no hyphens, spaces, or special characters.

- **Applies to:** all files, directories, identifiers, and artefacts
- **Examples:** `naming_standards.md`, `authoring_skills.md`, `hook_enforcement_sql.sh`, `api_key`, `user_profile`
- **Never:** `NamingStandards.md`, `naming-standards.md`, `Naming Standards.md`

### 📈 Name for scale

Choose a name that fits the likely higher grouping, not just today's problem.

- **Thinking:** What category does this belong to? Will other similar items need the same convention?
- **Example:** `naming_standards.md` (applies to all identifiers) over `hook_naming.md` (only hooks)
  - **Why:** Rules for naming will apply to skills, directories, agents, and other artefacts too; a single rule covers all of them
  - **Benefit:** Future additions (skills, directories) will reference the same rule instead of requiring separate files

---

## 📊 Quick reference

| Artefact | Pattern | Example | Details |
|---|---|---|---|
| **Hook files** | `hook_<type>_<domain>.sh` | `hook_enforcement_sql.sh` | See `_claude_naming_patterns.md` |
| **Skill** | `<domain>_<action>` | `confluence_create_page` | See `_claude_naming_patterns.md` |
| **Rule file** | `snake_case.md` | `naming_standards.md` | See `_claude_naming_patterns.md` |
| **Directory (user-created)** | `_<name>/` | `_rules/`, `_templates/` | See `claude_directory_structure.md` |
| **Directory (auto-generated)** | `<name>/` | `backups/`, `memory/` | See `claude_directory_structure.md` |

---

## 🔗 Related rules

- **Parent:** `naming_standards.md` — entry point; loads these principles + pattern details
- **Sibling:** `_claude_naming_patterns.md` — detailed naming patterns for hooks, skills, rules
- **Related:** `claude_directory_structure.md` → `_claude_directory_naming.md` — naming rules for directories and files
- **Related:** `claude_directory_structure.md` → `_claude_directory_organization.md` — directory structure and prefix conventions
