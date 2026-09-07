# Examples

## Example 1: Daily Session Capture

**Scenario:** End-of-day session review. Capture all prompts from today and review what was accomplished.

**Command:**
```bash
$ /capture_session_prompts
```

**Output:** `~/.claude/sessions/2026-08-26_prompts.md`

| Timestamp | Theme | Subject | Status | Proposed Action | Closure | MoSCoW | Prompt |
|---|---|---|---|---|---|---|---|
| 09:15 | Rules | Guiding principles | ✅ Done | Review usage evidence | Updated guiding_principles.md | Must | Review guiding principles for intentionality rule... |
| 10:30 | Skills | Jira creation | ✅ Done | Refactor skill structure | Refactored skill; PR ready | Must | Refactor jira_create skill to match... |
| 13:45 | Planning | Sprint planning | ⏳ Pending | Plan next sprint items | TODO added | Should | What should be next sprint focus? |
| 15:00 | Process | Session capture | ⏳ Pending | Capture session activity | In progress | Should | Capture session prompts for review... |

**Summary:**
- **By Status:** Done: 2, Pending: 2, Other: 0
- **By Theme:** Rules: 1, Skills: 1, Planning: 1, Process: 1
- **By MoSCoW:** Must: 2, Should: 2, Could: 0

---

## Example 2: Historical Session Review

**Scenario:** Review prompts from a specific past date to understand what was worked on.

**Command:**
```bash
$ /capture_session_prompts --date 2026-08-20
```

**Output:** `~/.claude/sessions/2026-08-20_prompts.md`

Generates same table structure for specified date. Use for:
- Retrospectives: what was accomplished this week?
- Planning: what was left pending?
- Auditing: what was discussed for compliance/documentation?

---

## Example 3: Manual Refinement Workflow

**Scenario:** Auto-generated categorization has inaccuracies. Refine before archiving.

1. Generate prompts table
2. Open file: `cat ~/.claude/sessions/2026-08-26_prompts.md`
3. Review and edit:
   - **Correct Theme:** "Rules" → "Process" (misclassified)
   - **Add Subject:** "MoSCoW assignment" (heuristic missed specific topic)
   - **Adjust Status:** "⏳ Pending" → "✅ Done" (task completed after capture)
   - **Add Closure:** "Updated CLAUDE.md" (heuristic didn't detect file edit)
4. Save refined markdown
5. Commit to git if archiving: `git add ~/.claude/sessions/2026-08-26_prompts.md && git commit -m "docs: archive session prompts for 2026-08-26"`

---

## Example 4: Using Captured Prompts for Planning

**Scenario:** Use captured high-priority pending items to plan next session.

1. Generate today's prompts: `/capture_session_prompts`
2. Review pending items: Filter by `Status = ⏳ Pending` and `MoSCoW = Must/Should`
3. Create TODOs from pending items: Add high-MoSCoW items to `~/.claude/TODO.md`
4. Start next session with clear priorities based on captured activity
