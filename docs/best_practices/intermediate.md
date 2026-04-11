# 🔧 Intermediate

Practices that pay off once you are comfortable with the basics. Each one reduces wasted effort or improves output quality.

| Practice | Source | Description | Example |
|---|---|---|---|
| 🧠 Enable auto-memory | Anthropic | Persist project knowledge across sessions — dbt patterns, DAG conventions, decisions — without manual effort. | [`"autoMemoryEnabled": true`](../../src/claude/settings.json#L2) |
| 🔌 MCP server discipline | Team | Integration servers (Jira, Confluence, email) enabled per session, not always-on — keeps attack surface small. | [enable/disable config](#mcp-discipline) |
| ⚖️ Frame work as trivial or non-trivial | Anthropic | Match your process to task complexity — not every change deserves the same approach. | [Trivial vs non-trivial](#trivial-vs-non-trivial) |
| ✅ Quality commands | Team | 5 mid-session slash commands for stress-testing, reviewing, and debugging work in progress. | [commands/](../../src/claude/commands/README.md) |
| 🤖 Automate repetitive instructions | Anthropic | Turn recurring instructions (run the linter, follow these conventions) into hooks or skills so they fire automatically. | [`claude_prompt_reviewer.py`](../../src/claude/hooks/claude_prompt_reviewer.py), [`claude_session_cost.py`](../../src/claude/hooks/claude_session_cost.py) |
| 🏷️ Tag schema | Team | Stamp maturity and criticality metadata on every skill you create — makes auditing the skill library meaningful. | [Tag schema](#tag-schema) |
| 🧰 CLAUDE.md maintenance | Team | Periodically audit and improve CLAUDE.md files using the built-in plugin. | [CLAUDE.md maintenance](#claudemd-maintenance) |

---

## 💻 Code examples

### ⚖️ Trivial vs non-trivial

**Trivial** (renaming a CTE, fixing a typo in a YAML description, bumping a package version) — describe what you want and let Claude proceed.

**Non-trivial** (designing a new mart model, refactoring a DAG, adding a new Airflow data source) — slow down deliberately:

- Gather requirements first: *"I want to add a mart model for Salesforce opportunity revenue. Ask me questions about the grain, dimensions, and aggregations until you have what you need. Then write a spec."*
- Ask Claude to reason carefully: *"think step by step about the tradeoffs"* or *"think carefully about whether this should be incremental or table materialisation"* before responding.

Use [`/grill_me`](../../src/claude/commands/grill_me.md) to run a structured design interview — Claude asks one question at a time until the approach is solid before any model is written.

---

### 🔌 MCP discipline

**Always-active core servers:**

| Server | Purpose |
|---|---|
| `memory` | Persistent memory across sessions |
| `context7` | Fetches current library and framework documentation (dbt, Airflow, Snowflake, etc.) |
| `filesystem` | File system access |
| `sequential-thinking` | Structured reasoning for complex tasks |

**Integration servers — enable per session only:**

| Server | Connects to |
|---|---|
| `Atlassian` | Jira, Confluence |
| `Microsoft_365` | Outlook, Teams, Calendar, SharePoint |
| `GitHub` | Repositories, PRs, issues |

To enable an integration server, remove it from `deniedMcpServers` in `~/.claude/settings.json` and restart Claude Code. Add it back when done:

```json
{
  "deniedMcpServers": [
    { "serverName": "Atlassian" },
    { "serverName": "Microsoft_365" },
    { "serverName": "GitHub" }
  ]
}
```

Integration servers have write access to external systems. Keeping them denied by default prevents accidental Jira ticket creation or Confluence edits, and avoids session costs when the integrations aren't needed.

---

### 🏷️ Tag schema

Every skill generated via `/skill-creator` carries standard YAML frontmatter tags. The plugin prompts for maturity tier during "Capture Intent" and stamps four Tier 1 tags automatically:

| Tag | Values |
|---|---|
| `maturity` | `draft` / `tactical` / `strategic` |
| `criticality` | `must` / `should` / `could` / `want` |
| `status` | `active` / `dormant` / `deprecated` / `wip` |
| `tested` | `true` / `false` |

The maturity tier also controls a scope gate block in the skill body:

| Maturity | Claude behaviour |
|---|---|
| `draft` | Happy path only — log gaps as TODOs, no refactoring |
| `tactical` | Main path + light error handling — no gold-plating |
| `strategic` | Full coverage — edge cases, documentation, evals expected |

Full schema (Tier 1 + optional Tier 2 tags): `src/claude/skills/patches/claude-tag-schema.md`

---

### 🧰 CLAUDE.md maintenance

The `claude-md-management` plugin provides `/revise-claude-md`, which audits all CLAUDE.md files in a project against a quality rubric and proposes targeted improvements.

Invoke it when:
- Setting up a new project for the first time
- After significant architectural changes (new layers, renamed directories, changed tooling)
- At session wrap-up to keep project context current

```
/revise-claude-md
```

The plugin scores each file on commands, architecture clarity, non-obvious patterns, conciseness, currency, and actionability. It outputs a scored report and shows diffs before making any changes.

> **Tip:** Press `#` during any Claude session to have Claude auto-incorporate session learnings into the active project CLAUDE.md without a full audit.
