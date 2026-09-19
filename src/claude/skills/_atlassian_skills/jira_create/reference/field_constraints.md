# 📋 Field Constraints & Validation

## 📊 Story Points

- **Required:** Yes
- **Valid range:** 0.5 to 100
- **Type:** Decimal
- **Examples:** 0.5 (half), 1, 2, 3, 5, 8, 13, 21
- **Validation:** Must be ≥0.5; no upper limit enforced

## 🏷️ Type (Issue Type)

- **Valid values:** Bug, Task, Improvement, Epic
- **Default:** Task (if not specified)
- **Used for:** Categorizing work in Jira

## 📝 Title (Summary)

- **Required:** Yes
- **Max length:** 255 characters
- **Validation:** Must not be empty

## 📄 Description

- **Required:** Yes
- **Type:** ADF (Atlassian Document Format) or plain text
- **Max length:** No hard limit
- **Validation:** Can be empty string but field must be provided

## 👤 Assignee

- **Required:** No
- **Type:** Email or account ID
- **Validation:** Must be valid Jira user in workspace
- **Error if invalid:** "Assignee not found" or "Invalid user"

---

## 🗂️ Jira Project Context

This skill assumes a default Jira project context. Specify which project (e.g., `INFRA`, `FEATURE`) when creating tickets for different teams.
