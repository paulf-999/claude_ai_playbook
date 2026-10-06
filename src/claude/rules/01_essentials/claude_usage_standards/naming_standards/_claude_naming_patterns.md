<!-- version: 4.3.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-06 -->
# 🏷️ Naming patterns — files, objects, and artefacts

**Purpose:** Establish self-describing naming patterns for rules, skills, hooks, scripts, and other Claude config artefacts.

## 📝 Rule naming

| Pattern | Example | What it's for |
|---|---|---|
| `<concept>.md` | `naming_standards.md` | Naming conventions for every artefact |
| | `security.md` | Secure coding and Claude's security guardrails |
| | `mcp_trust_model.md` | Trust boundaries for MCP servers |
| `04_path_scoped/<domain>/<concept>.md` | `style_guide_standards/sql.md` | SQL style guide |
| | `style_guide_standards/dbt.md` | dbt style guide |

- **Format:** snake_case, named for the concept the rule covers
- **Subdomains:** group related lazy rules under `rules/04_path_scoped/<domain>/` or `_rules_lazy_load/<domain>/`
- **Location:** pick the tier per `claude_rule_loading_strategy.md`, which says what belongs in each of `01_essentials/` to `04_path_scoped/` and `_rules_lazy_load/`
- **Name for scale:** fit the likely higher grouping, not just today's problem — e.g. `naming_standards.md` over `hook_naming.md` (see `_naming_principles.md`)

**Load details on-demand:** See `~/.claude/rules/03_authoring_guidelines/authoring_rules.md` for full rule creation checklist, directory placement, and testing requirements.

## 🛠️ Skill naming

| Pattern | Example | What it's for |
|---|---|---|
| `<domain>_<action>` | `confluence_create_page` | Creates a Confluence page |
| | `jira_create` | Creates a Jira issue |
| | `claude_review_config` | Reviews Claude configuration |

- **Domain prefix:** must match a domain ID from `skill_domains.yaml`
- **Directory:** the skill lives in the folder its domain's `directory:` names in `skill_domains.yaml`, and several domains may share one (e.g. `confluence_create_page` → `_atlassian_skills/`)
- **Action:** lowercase imperative verb describing what the skill does

**Load details on-demand:** See `~/.claude/rules/03_authoring_guidelines/authoring_skills.md` for full skill creation guide, complexity scoring, and domain reference (YAML files).

## 🪝 Hook naming

| Pattern | Example | What it's for |
|---|---|---|
| `hook_<type>_<domain>.sh` | `hook_enforcement_naming_convention.sh` | Blocks badly named new files under the config directory |
| | `hook_style_guide_response_standards_inject.sh` | Injects the response-format directive each turn |
| | `hook_enforcement_mcp_stale_settings.sh` | Reminds you to restart after MCP settings change mid-session |
| `hook_<type>_dispatch.sh` | None yet | Fan-out hook that calls several same-type domain hooks and combines their output |

- **Prefix:** all hook files must start with `hook_` — distinguishes them from other shell scripts
- **Type:** `enforcement` (blocks or injects a warning), `style_guide` (injects style context) or `session_start` (runs when a session opens)
- **Domain:** the concern being enforced, e.g. `sql`, `mcp_stale_settings`, `naming_convention`

## 🐍 Script naming

| Pattern | Example | What it's for |
|---|---|---|
| `_scripts/_<verb>_scripts/<verb>_<subject>.py` | `_audit_scripts/audit_rule_usage.py` | Reports on the config without changing it |
| | `_clean_scripts/clean_plans.py` | Archives or removes old files |
| | `_lint_scripts/lint_claude_tags.py` | Checks files against a standard and fails on breaches |

- **Group folder:** every script sits in a `_<verb>_scripts/` folder, never loose in `_scripts/`.
- **Verb first:** the filename starts with its folder's verb, so the name says what the script does.
- **New verb:** add a new `_<verb>_scripts/` folder only once two scripts share that verb.
- **Enforced by:** `_tests/scripts/test_script_naming.py`.
