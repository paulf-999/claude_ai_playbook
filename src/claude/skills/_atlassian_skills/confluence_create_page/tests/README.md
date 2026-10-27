# 🧪 Tests

`evals.yaml` holds this skill's test scenarios — recorded situations (a user request, the setup, the expected result) that check `confluence_create_page` still behaves correctly as it changes over time. They aren't code; think of them as worked examples an author checks the skill against by hand or via the skill-review tooling.

## 📋 Scenarios

| # | Scenario | Phase | What it checks |
|---|---|---|---|
| 1 | `happy_path_general_page` | Draft & review | Full flow: gathers details, writes a local draft, waits for explicit approval before publishing |
| 2 | `happy_path_platform_risk_assessment` | Draft & review | Platform risk pattern: confirms space and parent, rates each theme L/M/H, publishes only after draft approval |
| 3 | `mcp_unavailable` | Setup | Stops and tells the user to enable the Atlassian MCP if it isn't connected |
| 4 | `space_not_named_is_confirmed` | Pattern | Asks for the Confluence space instead of inferring one |
| 5 | `parent_page_required` | Pattern | Never publishes at the space root, and asks for a parent page |
| 6 | `unsupported_pattern_offers_valid_ones` | Not for | Turns down an unsupported pattern and offers the two supported ones |
| 7 | `personal_names_replaced_with_roles` | Pattern | Replaces a named individual with a role descriptor |
| 8 | `draft_review_iteration` | Draft & review | Applies requested changes and re-asks for approval, never publishing mid-iteration |
| 9 | `publish_permission_denied` | Publish | A permission error names the space, keeps the draft, and points to the error-recovery doc |
| 10 | `page_update_request_out_of_scope` | Not for | Turns down a request to edit an existing page |

- **Only test suite:** `evals.yaml` is this skill's whole test suite, since the skill has no Python code of its own.
