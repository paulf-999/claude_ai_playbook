# Phase 3 Fix Workflow — audit_agents

Work through the prioritised action list from the audit report, starting with High severity.

For **each finding**:

1. Explain the proposed fix clearly.
2. Confirm with the user before applying.
3. Apply the edit to the **installed file** at `~/.claude/agents/...`
4. Apply the **same edit** to the corresponding **repo source file** at `~/github_repository/dmt-scripts-claude_ai_playbook/src/claude/agents/...`
   - If no repo source file exists, note this and ask the user whether to create one.
5. Move to the next finding only after both edits are complete.

Do not batch fixes — one finding at a time, with user confirmation at each step.

---

## Phase 4 — Commit and push

After all fixes are applied, check if there are any changes staged in the repo:

```bash
cd ~/github_repository/dmt-scripts-claude_ai_playbook && git status
```

If repo files were modified:

1. Show the user a summary of what was changed.
2. Ask: "Shall I commit and push these fixes to the playbook repo?"
3. If yes:
   - Create a conventional commit on the current branch (or `feature/agent-audit-fixes` if on main):
     ```
     fix(agents): apply audit findings — <brief summary of fixes>
     ```
   - Push to remote.
   - Report the branch and commit SHA.
4. If no: leave the changes staged for the user to commit manually.
