<!-- version: 1.2.5 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-26 -->
# 🎯 Task Request Conventions

**Purpose:** Establish durable, version-controlled conventions for how Claude responds to specific, recurring user request types — patterns that are behavioural, not mechanical, and codified as guidance rules.

> **Scope:** Behavioural conventions for user request patterns (e.g., "add to TODOs", "propose a hook"). Not mechanical enforcement (hooks, tests) — those are governed by `testing.md` and individual enforcement rules.

---

## 🎯 Overview

- **Convention:** when a user makes a specific request type, Claude follows the documented convention.
- **Contents:** this file groups repeatable patterns for handling common, recurring requests, not foundational principles.
- **Room to grow:** the structure groups related conventions and scales to future patterns (e.g., "when user asks for a plan", "when user says verify").

**Benefits:**
- **Versioned:** conventions are versioned and tracked (not lost in resets)
- **Discoverable:** they live in one file
- **Consistent:** they apply the same way across sessions
- **Extensible:** new conventions are easy to add

---

## 📝 Task logging convention

Convention for "add to TODOs" requests — when a user says "add to TODOs" or "add a TODO", Claude should edit `~/.claude/TODO.md` with a new entry in the Items table.

**Trigger:** User says "add to TODOs", "add a TODO", "add this to TODOs", or similar variants indicating a task to log.

**Behaviour:** Edit `~/.claude/TODO.md` and add a new entry to the **Items by Execution Order** table.

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

**Note:** This is the default behaviour unless the user explicitly specifies a different location or format.

### 📌 Example usage

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
   - Description: "Create style guide rule for SQL formatting in dbt models. Cover indentation, naming, comment styles. Aligns with naming_standards.md."

---

## 🪝 Hooks decision framework

**Read on demand:** `~/.claude/_rules_lazy_load/claude_config/hooks_decision_framework.md` — before proposing any hook or automation.

ROI criteria and guardrails before proposing automation. When considering hook proposals, evaluate using the framework to prevent low-ROI automation.
