<!-- version: 1.1.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-29 -->
<!-- applies_to: * -->
<!-- miss_cost: low — a shortcut goes unrecognised and the user types it out -->
<!-- loading: always-on — CLAUDE.md imports it so the shortcuts work in every session -->
# ⌨️ Aliases

**Purpose:** Quick reference for all Claude Code shortcuts and automated commands.

| Input | Theme | Status | Meaning |
|-------|-------|--------|---------|
| `/batch` | Automation | Testing | Decompose a large change into parallel isolated subagents, each opening a PR — **controls in `_rules_lazy_load/claude_config/automation_controls.md`** |
| `bullets` | Formatting | Ready | Format with **keyword:** bullet style — bold keyword + colon opening each bullet |
| `draft` | Atlassian | Ready | Draft content to a local `.md` file first before pushing to an external system (Confluence, Jira, etc.) |
| `/fewer-permission-prompts` | Configuration | Ready | Audit transcripts for read-only command usage; optimise `permissions.allow` in settings.json to reduce permission prompts |
| `/goal` | Automation | Testing | Work until a verifiable condition is met — **controls in `_rules_lazy_load/claude_config/automation_controls.md`** |
| `/loop` | Automation | Testing | Repeat a prompt on a schedule — **controls in `_rules_lazy_load/claude_config/automation_controls.md`** |
| `plan` | Claude mode | Ready | Enter plan mode |

---

## 📝 Note on automation controls

- **Controls file:** the three experimental automation commands (`/batch`, `/goal`, `/loop`) take their usage limits from `_rules_lazy_load/claude_config/automation_controls.md`.
- **Check it for:** turn budgets and caps, minimum intervals, approval gates and kill-switch procedures, before using any of them.
- **Why one file:** keeping the limits there avoids duplication and keeps this file a quick reference.
