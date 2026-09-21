# 🧪 Tests

`evals.yaml` holds this skill's test scenarios — recorded situations (a user request, the setup, the expected result) that check `confluence_create_page` still behaves correctly as it changes over time. They aren't code; think of them as worked examples an author checks the skill against by hand or via the skill-review tooling.

## 📋 Scenarios

| # | Scenario | Phase | What it checks |
|---|---|---|---|
| 1 | `happy_path_general_page` | Draft & review | Full flow: gathers details, writes a local draft, waits for explicit approval before publishing |
| 2 | `mcp_unavailable` | Setup | Stops and tells the user to enable the Atlassian MCP if it isn't connected |
| 3 | `validation_failure_title` | Validate | Rejects a title under 3 characters before any draft is written |
| 4 | `validation_failure_space` | Validate | Rejects a space key containing non-alphanumeric characters |
| 5 | `validation_failure_pattern` | Validate | Rejects a pattern name outside the supported list, offers a valid one instead |
| 6 | `validation_failure_sections` | Validate | Rejects duplicate section names |
| 7 | `draft_review_iteration` | Draft & review | Applies requested changes and re-asks for approval, never publishing mid-iteration |
| 8 | `publish_timeout_all_choices` | Publish | Each choice (Abort / Retry / Continue) in the publish-timeout dialog behaves correctly |
| 9 | `publish_permission_denied` | Publish | A permission error names the space, preserves the draft, and points to troubleshooting docs |

- **Handler tests:** `confluence_create_page_handler.py` also has a separate pytest suite at `~/.claude/_tests/skills/confluence_create_page/` (repo root's `_tests/`, not this folder)
- **Pytest suite covers:** the Python handler code
- **evals.yaml covers:** the skill's behavior as a whole
