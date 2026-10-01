# 📦 What's installed

Last updated: 1st October 2026

This page describes what each part of `src/claude/` does and links to the index for each.

- **Install:** `make install` is disabled, so the live config is edited directly in the folder `CLAUDE_CONFIG_DIR` points at (e.g. `~/claude`).
- **Windows:** `make install_windows` syncs the config to a Windows `.claude` folder from WSL2.
- **Loading:** Claude Code reads `CLAUDE.md` at startup, which `@import`s the always-on rules.

---

## 📄 Top-level files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | 🧠 Root config that imports the always-on rules (tiers 01–04) |
| `settings.json` | ⚙️ Baseline settings — permissions, hook registration, plans directory, auto memory |
| `settings_json_readme.md` | 📘 Explains why each setting in `settings.json` exists |
| `aliases.md` | ⌨️ Quick reference for shortcuts such as `/batch`, `/goal`, `/loop` and `draft` |
| `README.md` | 🗺️ Overview of the `src/claude/` folder |

---

## 📏 Rules

See [`src/claude/_rules/README.md`](../src/claude/_rules/README.md)

Rules are grouped into five numbered tiers by purpose:

- **`01_essentials/`:** foundational principles and conventions — response standards, usage standards, guiding principles.
- **`02_claude_standards/`:** quality gates for all work — behaviour, git, security, testing, portable paths.
- **`03_authoring_guidelines/`:** how to author rules, skills and agents, including the shared metadata header.
- **`04_claude_reference/`:** how Claude Code and this config work — operational efficiency, rule loading strategy.
- **`05_lazy_load/`:** domain-specific rules such as style guides, read on demand and never imported.

- **Always-on:** tiers 01–04 are imported via `CLAUDE.md`, so they load every session.
- **Per-parent `_lazy_load/`:** bulky children of an always-on rule sit in `<parent>/_lazy_load/` and are read on demand.
- **Related links:** each tier's `README.md` holds the "🔗 Related rules" links, since READMEs aren't imported.

### 🎯 Path-scoped rules (`rules/`)

- **What:** `rules/` holds symlinks to lazy-load rules that carry `paths:` frontmatter.
- **How:** Claude Code loads a linked rule only when Claude reads a file that matches its `paths:` pattern.
- **Why no underscore:** Claude Code only reads path-scoped rules from a folder named exactly `rules/`.

| Link | Loads when Claude reads |
|------|-------------------------|
| `rules/sql.md` → SQL style guide | `**/*.sql` |

---

## 🎨 Style guides

See [`src/claude/_rules/05_lazy_load/style_guide_standards/`](../src/claude/_rules/05_lazy_load/style_guide_standards/)

Coding standards for the technologies the team uses, read on demand unless a `rules/` link loads them.

| Style guide | Covers | Loading |
|-------------|--------|---------|
| `sql.md` | SQL and SQLFluff | Path-scoped (`**/*.sql`) |
| `dbt.md` | dbt models | On demand |
| `airflow.md` | Airflow DAGs | On demand |
| `python.md` | Python code | On demand |
| `bash.md` | Shell scripts | On demand |
| `jira.md` | Jira tickets | On demand |
| `payroc_engineering_naming_standards.md` | Engineering naming | On demand |
| `infra/terraform.md` | Terraform | On demand |
| `infra/ansible.md` | Ansible | On demand |
| `infra/docker.md` | Docker | On demand |

---

## 🤖 Agents

See [`src/claude/agents/`](../src/claude/agents/)

| Agent | Purpose |
|-------|---------|
| `core/technical_writer` | ✍️ Drafts PR descriptions from the repo's template and new Confluence pages |

---

## 🛠️ Skills

See [`src/claude/skills/README.md`](../src/claude/skills/README.md)

Multi-step workflows invoked with `/<skill_name>`, grouped by domain folder.

| Group | Skill | Purpose |
|-------|-------|---------|
| `_atlassian_skills` | `confluence_create_page` | Creates a Confluence page (needs the Atlassian MCP) |
| `_atlassian_skills` | `jira_create` | Creates a Jira ticket (needs the Atlassian MCP) |
| `_claude_skills` | `claude_capture_session_prompts` | Captures session prompts into a review table |
| `_claude_skills` | `claude_kaizen` | Turns repeated corrections into rules, and prunes stale ones |
| `_claude_skills` | `claude_review_config` | Scores the Claude config across six quality dimensions |
| `_claude_skills` | `claude_setup_graphify` | Sets up a Graphify knowledge graph for a repo |
| `_git_skills` | `git_create_pr` | Creates a GitHub PR with commit message and body |

---

## 🪝 Hooks

See [`src/claude/hooks/`](../src/claude/hooks/)

Shell scripts that run at Claude Code lifecycle events once registered in `settings.json`.

| Hook | Event | What it does | Registered |
|------|-------|--------------|------------|
| `hook_style_guide_response_standards_inject.sh` | `UserPromptSubmit` | Injects the response-format reminder each turn | ✅ |
| `hook_enforcement_writing_style.sh` | `PostToolUse` | Checks `.md` files written to the config against `writing_style.md` | ✅ |
| `hook_enforcement_dir_structure.sh` | `PreToolUse` | Injects directory rules before a new config folder is created | ❌ |
| `hook_enforcement_naming_convention.sh` | `PreToolUse` | Blocks badly named new config files | ❌ |
| `hook_session_start_mcp_stale_settings.sh` | `SessionStart` | Reminds you to restart after MCP settings change | ❌ |
| `hook_style_guide_response_standards.sh` | — | Checks a response against the response standards | ❌ |

---

## 🧰 Supporting folders

| Folder | Purpose |
|--------|---------|
| `_templates/` | 📐 Starting templates for rules, agents, skills and TODO files |
| `_reference/` | 📚 Architecture and background docs, read on demand |
| `_tests/` | 🧪 Pytest suite — run with `CLAUDE_CONFIG_DIR=$PWD/src/claude python3 -m pytest src/claude/_tests` |
| `_admin/` | 📊 Quality scorecards and decision logs |

---

## 🔌 MCP servers

See [`docs/reference/claude_config/mcp/mcp_setup.md`](reference/claude_config/mcp/mcp_setup.md)

- **What:** MCP servers let Claude reach external tools such as Atlassian.
- **Toggle:** `make enable_mcp server=<name>` and `make disable_mcp server=<name>`, then restart Claude Code.

---

## 🧩 Plugins

See [`docs/reference/claude_config/plugins.md`](reference/claude_config/plugins.md)

- **What:** plugins add skills, commands and hooks to the CLI, unlike MCP servers, which connect to external tools.
- **Install:** `make install_plugins`, then `make patch_plugins` to apply team patches.
