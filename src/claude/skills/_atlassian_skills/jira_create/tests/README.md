# 🧪 Tests

`evals.yaml` holds this skill's test scenarios — recorded situations (a user request, the setup, the expected result) that check `jira_create` still behaves correctly as it changes over time. They aren't code; think of them as worked examples an author checks the skill against.

## 📋 Scenarios

| # | Scenario | Phase | What it checks |
|---|---|---|---|
| 1 | `happy_path_task_ticket` | Gather & create | Full flow: gathers details, defaults issue type to Task, validates, then creates the ticket |
| 2 | `mcp_unavailable` | Setup | Stops and tells the user to enable the Atlassian MCP instead of fabricating a ticket |
| 3 | `validation_pass_story_points_minimum` | Validate | Story points exactly at the 0.5 minimum boundary passes and proceeds to creation |
| 4 | `validation_failure_story_points_below_minimum` | Validate | Story points below 0.5 are rejected before any MCP call is made |
| 5 | `validation_failure_missing_title` | Validate | A missing title is rejected; Claude asks for one rather than defaulting |
| 6 | `ticket_created_reports_id_and_link` | Create & report | On success, Claude reports both the new issue's ID and its Jira link |

- **Handler tests:** `jira_create_handler.py` also has a separate pytest suite at `~/.claude/_tests/skills/jira_create/` (repo root's `_tests/`, not this folder)
- **Pytest suite covers:** the Python handler code
- **evals.yaml covers:** the skill's behavior as a whole
