<!-- version: 4.0.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-09-30 -->
# 🏷️ Naming patterns — files, objects, and artefacts

**Purpose:** Establish self-describing naming patterns for hooks, skills, rules, and other Claude config artefacts.

## 🪝 Hook naming

**Pattern:** `hook_<type>_<domain>.sh`

- **Prefix:** all hook files must start with `hook_` — distinguishes them from other shell scripts
- **Type:** `enforcement` (blocks or injects a warning), `style_guide` (injects style context) or `session_start` (runs when a session opens)
- **Domain:** the concern being enforced, e.g. `sql`, `dir_structure`, `naming_convention`
- **Dispatcher:** `hook_<type>_dispatch.sh` — fan-out hook that calls multiple same-type domain hooks and aggregates their output

**Examples:**
- `hook_enforcement_naming_convention.sh` — blocks badly named new files under the config directory
- `hook_style_guide_response_standards_inject.sh` — injects the response-format directive each turn
- `hook_session_start_mcp_stale_settings.sh` — reminds you to restart after MCP settings change

## 🛠️ Skill naming

**Pattern:** `<domain>_<action>`

- **Domain prefix:** must match a domain ID from `skill_domains.yaml`
- **Directory:** the skill lives in the folder its domain's `directory:` names in `skill_domains.yaml`, and several domains may share one (e.g. `confluence_create_page` → `_atlassian_skills/`)
- **Action:** lowercase imperative verb describing what the skill does

**Examples:**
- `confluence_create_page` — creates a Confluence page
- `jira_create` — creates a Jira issue
- `claude_review_config` — reviews Claude configuration

**Load details on-demand:** See `~/.claude/_rules/03_authoring_guidelines/authoring_skills.md` for full skill creation guide, complexity scoring, and domain reference (YAML files).

## 📝 Rule naming

**Pattern:** snake_case, descriptive of the concept being enforced

- **Format:** lowercase only, words separated by underscores (e.g. `naming_standards.md`, `security.md`, `mcp_trust_model.md`)
- **Location:** pick the tier per `claude_rule_loading_strategy.md`, which says what belongs in each of `01_essentials/` to `05_lazy_load/`
  - **Subdomains:** group related lazy-loaded rules under `05_lazy_load/<domain>/` (e.g. `style_guide_standards/sql.md`, `style_guide_standards/dbt.md`)
- **General principles:** self-describing names and naming for scale apply here too — see `_naming_principles.md`

**Load details on-demand:** See `~/.claude/_rules/03_authoring_guidelines/authoring_rules.md` for full rule creation checklist, directory placement, and testing requirements.
