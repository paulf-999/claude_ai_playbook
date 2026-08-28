# 🏷️ Naming patterns — files, objects, and artefacts

**Purpose:** Establish self-describing naming patterns for hooks, skills, rules, and other Claude config artefacts.

## 🪝 Hook naming

**Pattern:** `hook_<type>_<domain>.sh`

- **Prefix:** all hook files must start with `hook_` — distinguishes them from other shell scripts
- **Type:** `enforcement` (blocks or injects a warning) or `style_guide` (injects domain-specific style context)
- **Domain:** the concern being enforced, e.g. `sql`, `dir_structure`, `naming_convention`
- **Dispatcher:** `hook_<type>_dispatch.sh` — fan-out hook that calls multiple same-type domain hooks and aggregates their output

**Examples:**
- `hook_enforcement_sql.sh` — enforces SQL style rules
- `hook_style_guide_dbt.sh` — injects dbt style guidance
- `hook_enforcement_dispatch.sh` — calls all enforcement hooks

## 🛠️ Skill naming

**Pattern:** `<domain>_<action>`

- **Domain prefix:** must match a domain ID from `skill_domains.yaml` (active) or `skill_domains_future.yaml` (roadmap)
- **Directory:** domain directory must exist and match the domain ID (e.g., `confluence_create_page` → `_confluence_skills/`)
- **Action:** lowercase imperative verb describing what the skill does

**Examples:**
- `confluence_create_page` — creates a Confluence page
- `jira_create` — creates a Jira issue
- `claude_review_config` — reviews Claude configuration

**Load details on-demand:** See `~/.claude/_rules/01_essentials/authoring_skills.md` for full skill creation guide, complexity scoring, and domain reference (YAML files).

## 📝 Rule naming

**Pattern:** snake_case, descriptive of the concept being enforced

- **Format:** lowercase only, words separated by underscores (e.g. `naming_standards.md`, `security.md`, `mcp_trust_model.md`)
- **Location:**
  - `01_essentials/` — blocking/safety rules (always-on imports; e.g. behaviour, security, testing, guiding_principles)
  - `02_claude_standards/` — how Claude operates (always-on imports; e.g. efficiency, git, memory)
  - `04_lazy_load/` — domain-specific rules (lazy-loaded on-demand; e.g. style guides, tool guides)
  - `04_lazy_load/<domain>/` — group related rules by subdomain (e.g. `style_guide_standards/sql.md`, `style_guide_standards/dbt.md`)
- **Name for scale:** choose a name that fits the likely higher grouping, not just today's problem — e.g. `naming_standards.md` over `hook_naming.md` (other identifiers will need naming guidance too)

**Load details on-demand:** See `~/.claude/_rules/01_essentials/authoring_rules.md` for full rule creation checklist, directory placement, and testing requirements.

## 📚 References

**Parent & siblings:**
- **Parent:** `naming_standards.md` — entry point for all naming conventions
- **Sibling:** `_naming_principles.md` — foundational naming principles (self-describing, offer options, snake_case, name for scale)
- **Related:** `claude_directory_structure.md` → `_claude_directory_naming.md` — directory and file naming conventions

**Detailed authoring guides:**
- **authoring_skills.md** — Full skill naming convention, domain list, skill_domains_future.yaml reference, examples
- **authoring_rules.md** — Rule naming standards, directory placement (01_essentials, 02_claude_standards, 04_lazy_load), pre-creation checklist
