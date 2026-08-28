# 📝 Task Logging Convention

**Purpose:** Establish the convention for handling "add to TODOs" requests — when a user says "add to TODOs" or "add a TODO", Claude should edit `~/.claude/TODO.md` with a new entry in the Items table.

---

## 🎯 Convention

**Trigger:** User says "add to TODOs", "add a TODO", "add this to TODOs", or similar variants indicating a task to log.

**Behavior:** Edit `~/.claude/TODO.md` and add a new entry to the **Items by Execution Order** table.

**Format:** Match the existing table structure:

| Column | Guidance |
|--------|----------|
| **#** | Next sequential number (auto-increment) |
| **Theme** | Category: Rules, Config, Process, Skills, Infrastructure, etc. |
| **Subject** | Specific area within theme (e.g., "File Structure Enforcement", "Decision-Making Rule") |
| **Item** | Brief descriptive title of the task |
| **Group** | Grouping: Complete, Quick Win, Foundation, High Effort, Core Work, Pending |
| **Status** | Icon + status: 📋 Pending, 🔄 In Progress, ✅ Done |
| **Priority** | High, Medium, Low |
| **Effort** | Low, Medium, High, Very High |
| **Value** | High, Medium, Low (impact if completed) |
| **Description** | Bullet-pointed description of the task, context, and success criteria |

**Note:** This is the default behavior unless the user explicitly specifies a different location or format.

---

## 📌 Example Usage

**User request:**
> "Add to TODOs: Create a rule for SQL formatting standards in dbt models. Should cover indentation, naming, comment styles."

**Claude action:**
1. Edit `~/.claude/TODO.md`
2. Add a new row to the Items table with:
   - Theme: Rules
   - Subject: Style Guides
   - Item: SQL Formatting Standards
   - Group: Foundation
   - Status: 📋 Pending
   - Priority: Medium
   - Effort: Medium
   - Value: High
   - Description: "Create style guide rule for SQL formatting in dbt models. Cover indentation, naming, comment styles. Aligns with payroc_engineering_naming_standards.md."

---

## 🔗 Related

- Parent: `task_request_conventions.md`
- Reference file: `~/.claude/TODO.md` (the target of all "add to TODOs" requests)
