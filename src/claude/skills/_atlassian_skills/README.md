# 🔗 Atlassian Skills

Jira and Confluence workflow skills. Require the Atlassian MCP server (`make enable_mcp server=Atlassian`, then restart Claude Code).

| Skill | Description | Version | Tested |
|---|---|---|---|
| `/confluence_create_page` | Interactively create a Confluence page for a known DM team pattern | 1.2.0 | [yes](../../../../tests/skills/_atlassian_skills/test_confluence_create_page_skill.py) |
| `/manage_jira` | Batch-create, bulk-update, or run a hygiene check on Data Platform Jira tickets and epics | 1.0.0 | [yes](../../../../tests/skills/_atlassian_skills/test_manage_jira_skill.py) |
| `/populate_jira_business_value` | Populate Business Value statements and CALC scores across a Jira ticket hierarchy | 0.1.0 | yes |
| `/confluence_review_page` | Generate and post a structured Claude review comment on a Confluence page | 0.1.0 | [yes](../../../../tests/skills/_atlassian_skills/test_confluence_review_page_skill.py) |
