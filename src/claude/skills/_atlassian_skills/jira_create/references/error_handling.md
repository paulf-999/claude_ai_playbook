# 🆘 Error Handling & Recovery

## 🔗 MCP Connection Errors

**Error:** `MCP server not available` or `Connection timeout`

**Cause:** Atlassian MCP not enabled or Claude Code not restarted after enabling

**Recovery:**
```bash
make enable_mcp server=Atlassian
# Restart Claude Code (Cmd+Shift+P → "Restart Claude Code")
```

---

## ✅ Validation Errors

### 📊 Story Points Validation Fails

**Error:** `Story points must be ≥0.5`

**Cause:** Entered value less than 0.5 or non-numeric

**Recovery:**
- **Valid values:** Use decimals: `0.5`, `1`, `2`, `3`, `5`, etc.
- **No upper limit:** Any value ≥0.5 is accepted.

---

## 🎯 Jira Errors

### 🔐 Permission Denied (403)

**Error:** `Access denied` or `Insufficient permissions`

**Cause:** Jira workspace doesn't have write permission to target project

**Recovery:**
- **Verify permissions:** Your Jira user must have Contributor role.
- **Check project settings:** Confirm who can create issues.

### ❌ Issue Type Not Found (404)

**Error:** `Issue type 'X' not found`

**Cause:** Specified issue type doesn't exist in project

**Recovery:**
- **Valid types:** Bug, Task, Improvement, Epic.
- **Custom types:** Check project settings for custom issue types.

### 👤 Assignee Not Found

**Error:** `User 'X' not found` or `Invalid assignee`

**Cause:** Email or account ID doesn't match any Jira user

**Recovery:**
- **Verify spelling:** Email addresses are case-insensitive.
- **Use full email:** e.g., `alice@company.com`
- **Or account ID:** Use Jira account ID (format: `5ab...`).
- **Skip if unsure:** Leave assignee empty if uncertain.

---

## 🔄 Recovery Workflow

**If ticket creation fails:**
1. **Find your error:** Match error message against the categories above.
2. **Apply steps:** Follow the recovery instructions for that error.
3. **Retry:** Use same details or corrected values.
4. **Manual test:** Try creating a ticket directly in Jira browser UI.
