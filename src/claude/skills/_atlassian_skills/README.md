# 🔗 Atlassian Skills

Jira and Confluence workflow skills. Require the Atlassian MCP server (`make enable_mcp server=Atlassian`, then restart Claude Code).

| Skill | Description | Version | Tested |
|---|---|---|---|
| `/confluence_create_page` | Interactively create a Confluence page for a known team pattern | 1.2.2 | [yes](confluence_create_page/tests/evals.yaml) |
| `/jira_create` | Create an individual Jira ticket with full field configuration and story point validation | 0.2.4 | [yes](jira_create/tests/evals.yaml) |
