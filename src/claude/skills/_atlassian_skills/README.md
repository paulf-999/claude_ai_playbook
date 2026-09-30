# 🔗 Atlassian Skills

Jira and Confluence workflow skills. Require the Atlassian MCP server (`make enable_mcp server=Atlassian`, then restart Claude Code).

| Skill | Description | Version | Tested |
|---|---|---|---|
| `/confluence_create_page` | Interactively create a Confluence page for a known DM team pattern | 1.2.0 | [yes](../../_tests/skills/confluence_create_page/test_confluence_create_page_handler.py) |
| `/jira_create` | Create an individual Jira ticket with full field configuration and story point validation | 0.1.0 | [yes](../../_tests/skills/jira_create/test_jira_create_handler.py) |
