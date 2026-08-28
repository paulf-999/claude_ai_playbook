# Phase 4: Fix Workflow

## 🔧 Offer to fix

After presenting findings, ask the user:

> "Would you like me to work through the Must and Should recommendations and apply fixes? I'll handle them one at a time and confirm each change before applying."

**If no:** Stop here.

**If yes:**
1. Address Must items first, then Should items
2. For each item:
   - State the finding clearly
   - Propose the specific fix
   - Wait for user confirmation
   - Apply the change to both `~/.claude/` and the playbook repo source at `~/git_repos/core/dmt-scripts-claude_ai_playbook/src/claude/`
   - Move to the next item

**Confirmation before each fix:**
- Never apply a fix without explicit user confirmation
- Show the exact change that will be made
- If the user has questions, clarify before proceeding
