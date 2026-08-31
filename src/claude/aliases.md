# ⌨️ Aliases

**Purpose:** Quick reference for all Claude Code shortcuts and automated commands.

| Input | Theme | Status | Meaning |
|-------|-------|--------|---------|
| `/batch` | Automation | Testing | Decompose a large change into parallel isolated subagents, each opening a PR — **controls in `_rules/03_lazy_load/automation_controls.md`** |
| `bullets` | Formatting | Ready | Format with **keyword:** bullet style — bold keyword + colon opening each bullet |
| `draft` | Atlassian | Ready | Draft content to a local `.md` file first before pushing to an external system (Confluence, Jira, etc.) |
| `/fewer-permission-prompts` | Configuration | Ready | Audit transcripts for read-only command usage; optimize `permissions.allow` in settings.json to reduce permission prompts |
| `/goal` | Automation | Testing | Work until a verifiable condition is met — **controls in `_rules/03_lazy_load/automation_controls.md`** |
| `/loop` | Automation | Testing | Repeat a prompt on a schedule — **controls in `_rules/03_lazy_load/automation_controls.md`** |
| `plan` | Claude mode | Ready | Enter plan mode |

---

## 📝 Note on automation controls

The three experimental automation commands (`/batch`, `/goal`, `/loop`) have detailed usage constraints documented in `_rules/03_lazy_load/automation_controls.md`. When using these features, always reference that file for:
- Turn budgets and caps
- Minimum intervals (for `/loop`)
- Approval gates
- Kill-switch procedures if the feature becomes unreliable

This consolidation prevents duplication while keeping aliases.md focused on quick reference.
