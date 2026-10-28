# Examples

## Example 1: Daily Session Capture

**Scenario:** End-of-day session review. Capture all prompts from today and review what was accomplished.

**Command:**
```bash
/claude_capture_session_prompts
```

**Output:** `~/_sessions/2026_08_26_claude_prompts.md`

| # | Hour | Min | Theme | Subject | Status | Proposed Action | Closure | MoSCoW | Prompt |
|---|------|-----|-------|---------|--------|-----------------|---------|--------|--------|
| 1 | 09 | 15 | Rules | Guiding principles | ✅ Done | Review usage evidence | Updated guiding_principles.md | | Review guiding principles for intentionality rule... |
| 2 | 10 | 30 | Skills | Jira creation | ✅ Done | Refactor skill structure | Refactored skill; PR ready | | Refactor jira_create skill to match... |
| 3 | 13 | 45 | Planning | Sprint planning | ⏳ Pending | Plan next sprint items | | Should | What should be the priority for next sprint? |
| 4 | 15 | 00 | Process | Session capture | ❓ Question | | | | Can we capture session prompts for review? |

- **MoSCoW:** only ⏳ Pending rows get one, from words such as "must", "should" or "could" in the prompt.

**Summary** (written below the table):
- **By status:** ✅ Done: 2, ⏳ Pending: 1, ❓ Question: 1
- **By theme:** Planning: 1, Process: 1, Rules: 1, Skills: 1
- **By theme & status:** a table with one row per theme and one column per status, plus a Total column

---

## Example 2: Historical Session Review

**Scenario:** Review prompts from a specific past date to understand what was worked on.

**Command:**
```bash
/claude_capture_session_prompts --date 2026-08-20
```

**Output:** `~/_sessions/2026_08_20_claude_prompts.md`

Generates same table structure for specified date. Use for:
- Retrospectives: what was accomplished this week?
- Planning: what was left pending?
- Auditing: what was discussed for compliance/documentation?

---

## Example 3: Manual Refinement Workflow

**Scenario:** Auto-generated categorization has inaccuracies. Refine before archiving.

1. Generate prompts table
2. Open file: `cat ~/_sessions/2026_08_26_claude_prompts.md`
3. Review and edit:
   - **Correct Theme:** "Rules" → "Process" (misclassified)
   - **Add Subject:** "MoSCoW assignment" (heuristic missed specific topic)
   - **Adjust Status:** "⏳ Pending" → "✅ Done" (task completed after capture)
   - **Add Closure:** "Updated CLAUDE.md" (heuristic didn't detect file edit)
4. Save refined markdown
   - **Edits are safe:** running the skill again for the same date stops rather than overwriting the file, unless you pass `--force`
5. Commit to git if archiving: `git add ~/_sessions/2026_08_26_claude_prompts.md && git commit -m "docs: archive session prompts for 2026-08-26"`

---

## Example 4: Using Captured Prompts for Planning

**Scenario:** Use captured high-priority pending items to plan next session.

1. Generate today's prompts: `/claude_capture_session_prompts`
2. Review pending items: Filter by `Status = ⏳ Pending` and `MoSCoW = Must/Should`
3. Create TODOs from pending items: Add high-MoSCoW items to `~/.claude/TODO.md`
4. Start next session with clear priorities based on captured activity
