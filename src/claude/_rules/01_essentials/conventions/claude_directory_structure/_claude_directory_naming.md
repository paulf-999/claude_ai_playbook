# 🏷️ Naming — Directories and Files

**Purpose:** Establish conventions for naming directories and files in the Claude config, ensuring self-describing, unambiguous names that follow consistent patterns.

---

## 📝 Naming rules

- **snake_case only:** lowercase, words separated by underscores — no hyphens, spaces, or special characters
- **Prefix conventions:**
  - **User-created directories:** must start with underscore — `_rules/`, `_templates/`, `_reference/`
  - **Auto-generated directories:** no prefix — `backups/`, `memory/`, `sessions/`
  - **Child files (within a directory):** start with underscore to distinguish from top-level files — `_child_file.md`
- **Self-describing:** a name must be unambiguous without context
  - ❌ Bad: `rule_a.md` — doesn't explain what "a" is
  - ✅ Good: `naming_standards.md` — purpose is clear from the name
- **Name for scale:** choose a name that fits the likely higher grouping, not just today's problem
  - ❌ Bad: `hook_naming.md` — only hooks need naming; what about skills, rules, directories?
  - ✅ Good: `naming_standards.md` — all identifiers need naming conventions; scales to future domains

---

## 🏗️ Directory naming

| Type | Pattern | Example | Note |
|---|---|---|---|
| **User-created** | `_<name>/` | `_rules/`, `_templates/`, `_docs/` | Always underscore prefix |
| **Auto-generated** | `<name>/` | `backups/`, `memory/`, `sessions/` | Never touch these |
| **Child file** | `_<aspect>.md` | `_claude_directory_organization.md` | Prefix indicates child of parent |

---

## 🪝 Hook naming

**Pattern:** `hook_<type>_<domain>.sh`

- **Prefix:** all hook files must start with `hook_` — distinguishes them from other shell scripts
- **Type:** `enforcement` (blocks or injects a warning) or `style_guide` (injects domain-specific style context)
- **Domain:** the concern being enforced, e.g. `sql`, `dir_structure`, `naming_convention`
- **Dispatcher:** `hook_<type>_dispatch.sh` — fan-out hook that calls multiple same-type domain hooks

**Examples:**
- `hook_enforcement_sql.sh` — enforces SQL style rules
- `hook_enforcement_dir_structure.sh` — enforces directory structure compliance
- `hook_style_guide_dbt.sh` — injects dbt style guidance

---

## 🛠️ Skill naming

**Pattern:** `<domain>_<action>`

- **Domain prefix:** must match a domain ID from `skill_domains.yaml` (active) or `skill_domains_future.yaml` (roadmap)
- **Directory:** domain directory must exist and match the domain ID (e.g., `confluence_create_page` → `_confluence_skills/`)
- **Action:** lowercase imperative verb describing what the skill does

**Examples:**
- `confluence_create_page` — creates a Confluence page
- `jira_create` — creates a Jira issue
- `claude_review_config` — reviews Claude configuration

---

## 📄 Rule naming

**Pattern:** snake_case, descriptive of the concept being enforced

- **Format:** lowercase only, words separated by underscores (e.g. `naming_standards.md`, `security.md`)
- **Location:**
  - `01_essentials/` — blocking/safety rules (always-on imports)
  - `02_claude_standards/` — how Claude operates (always-on imports)
  - `04_lazy_load/` — domain-specific rules (lazy-loaded on-demand)
- **Name for scale:** `naming_standards.md` (applies to all identifiers) over `hook_naming.md` (only hooks)

---

## 🔗 Related rules

- **Parent:** `claude_directory_structure.md` — directory organization and naming overview
- **Sibling:** `_claude_directory_organization.md` — the full directory tree and auto-generated vs. user-created distinction
- **Related:** `naming_standards.md` → `_naming_principles.md` — foundational naming principles for all identifiers
- **Related:** `naming_standards.md` → `_claude_naming_patterns.md` — detailed patterns for hooks, skills, and rules
