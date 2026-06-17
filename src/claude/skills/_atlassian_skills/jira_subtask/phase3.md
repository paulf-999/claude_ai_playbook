# Phase 3 — Create sub-tasks (detail)

## ⚠️ Critical field rules — do not deviate

| Rule | Detail |
|---|---|
| Issue type | Always `Sub-task` — with a hyphen. Never `Subtask`, `sub-task`, or `Sub Task`. |
| Sprint field | **Never include** `customfield_10020` on sub-tasks — the API rejects it. |
| Parent field | Set via `parent: { key: "<parent_key>" }` in the request body. |
| Components | Copy from parent. |
| Story points | **Never include** `customfield_10028` — sub-tasks do not carry story points. |
| Label | Always include `dm-claude-created`. |
| Business Value | Do **not** set on sub-tasks — field is for stories/epics only. |

## Request structure per sub-task

```json
{
  "fields": {
    "project": { "key": "<project_key>" },
    "parent": { "key": "<parent_key>" },
    "issuetype": { "name": "Sub-task" },
    "summary": "<title>",
    "description": "<description if provided>",
    "priority": { "name": "<priority>" },
    "assignee": { "accountId": "<account_id>" },
    "components": [{ "id": "<id>" }],
    "labels": ["dm-claude-created"]
  }
}
```

If the parent has no assignee (`assignee: null`), omit the `assignee` field from the request entirely — do not pass `{"accountId": null}` as this will cause an API error.

Create sub-tasks sequentially. After each API call, record the outcome before proceeding to the next. Do not stop on failure — continue through all sub-tasks and report failures at the end.
