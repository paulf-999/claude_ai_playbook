# 🧪 Tests

`evals.yaml` holds this skill's test scenarios — recorded situations (a user request, the setup, the expected result) that check `jira_create` still behaves correctly as it changes over time. They aren't code; think of them as worked examples an author checks the skill against.

## 📋 Scenarios

| # | Scenario | Phase | What it checks |
|---|---|---|---|
| 1 | `happy_path_task_ticket` | Gather & create | Full flow: defaults to Task, asks for the project, shows the ticket and creates it only after a yes |
| 2 | `mcp_unavailable` | Setup | Stops and tells the user to enable the Atlassian MCP instead of fabricating a ticket |
| 3 | `story_points_at_minimum_accepted` | Validate | Story points exactly at the 0.5 minimum are accepted |
| 4 | `story_points_below_minimum_rejected` | Validate | Story points below 0.5 are rejected before anything is created |
| 5 | `missing_title_requested` | Validate | A missing title is asked for, never invented |
| 6 | `declined_confirmation_creates_nothing` | Confirm | A "no" at the confirm step creates nothing |
| 7 | `ticket_created_reports_id_and_link` | Create & report | On success, Claude reports both the new issue's ID and its Jira link |
| 8 | `update_request_out_of_scope` | Not for | A request to update an existing ticket is turned down |

- **Only test suite:** `evals.yaml` is this skill's whole test suite, since the skill has no Python code of its own.
