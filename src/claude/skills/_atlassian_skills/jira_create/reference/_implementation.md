# 🛠️ jira_create — Implementation

**Purpose:** Set out the skill's phases in order, including the confirm step, so Claude never creates a ticket the user hasn't approved.

## 🔄 Phases

| Phase | What happens | Detail |
|---|---|---|
| **0 — Pre-check** | Call `getAccessibleAtlassianResources` to confirm access and get the cloud ID | `_error_handling.md` → MCP Connection Errors |
| **1 — Project** | Ask which Jira project to use, and never infer it | `_field_constraints.md` → Jira Project Context |
| **2 — Gather** | Collect type, title, description, assignee and story points | `_field_constraints.md` |
| **3 — Validate** | Check every field, including story points of 0.5 or more | `_field_constraints.md` → Story Points |
| **4 — Confirm** | Show the full ticket and wait for an explicit yes | SKILL.md → Instructions |
| **5 — Create** | Call `createJiraIssue` only after the yes | — |
| **6 — Report** | Show the new issue's key and link | — |

## 🚨 Error handling

- **No Atlassian access:** stop at Phase 0 and tell the user to run `make enable_mcp server=Atlassian` and restart Claude Code.
- **Validation fails:** go back to Phase 2 for the failing field, as `_error_handling.md` → Validation Errors describes.
- **Jira rejects the call:** follow `_error_handling.md` → Jira Errors, and never retry with a guessed project, type or assignee.
- **No yes at Phase 4:** create nothing, and offer to change the draft.
