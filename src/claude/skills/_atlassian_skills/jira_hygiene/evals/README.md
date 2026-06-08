# Evals — jira_hygiene

Behavioural test prompts for the `jira_hygiene` skill.

## Running evals

Evals are defined in `evals.json`. Each eval contains a prompt and a list of assertions
to check manually or via an automated harness.

To run manually: invoke each prompt in a Claude Code session and verify all assertions pass.

## Coverage

| Eval | Prompt | Key assertions |
|---|---|---|
| 1 | Natural language hygiene check | MCP pre-check, pattern read, report-before-fix |
| 2 | Slash command with MCP unavailable | MCP failure stops execution, user informed |
| 3 | Sprint-scoped check with auto-fix | JQL filter, criteria checks, confirm before fix |
