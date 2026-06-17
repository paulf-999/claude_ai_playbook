# 🔗 Atlassian Skills

Jira and Confluence workflow skills. Require the Atlassian MCP server (`make enable_mcp server=Atlassian`, then restart Claude Code).

| Skill | Description | Version | Tested |
|---|---|---|---|
| `/confluence_create_page` | Interactively create a Confluence page for a known DM team pattern | 1.2.0 | [yes](../../../../tests/skills/_atlassian_skills/test_confluence_create_page_skill.py) |
| `/jira_create` | Batch-create Data Platform Jira tickets from a template or create a standalone epic | 1.0.0 | [yes](../../../../tests/skills/_atlassian_skills/test_jira_create_skill.py) |
| `/jira_hygiene` | Scan Jira tickets for missing or incorrect fields and optionally auto-fix issues | 1.0.0 | [yes](../../../../tests/skills/_atlassian_skills/test_jira_hygiene_skill.py) |
| `/jira_subtask` | Create one or more sub-tasks under a parent Jira ticket for the Data Platform team | 0.1.0 | [yes](../../../../tests/skills/_atlassian_skills/test_jira_subtask_skill.py) |
| `/jira_update` | Bulk-update one or more fields across multiple Jira tickets matched by a JQL filter | 1.0.0 | [yes](../../../../tests/skills/_atlassian_skills/test_jira_update_skill.py) |
| `/populate_jira_business_value` | Populate Business Value statements and CALC scores across a Jira ticket hierarchy | 0.1.0 | yes |
| `/confluence_review_page` | Generate and post a structured Claude review comment on a Confluence page | 0.1.0 | [yes](../../../../tests/skills/_atlassian_skills/test_confluence_review_page_skill.py) |
