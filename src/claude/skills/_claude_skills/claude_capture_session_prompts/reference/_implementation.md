# Implementation

## 3-Phase Workflow

### Phase 1: Capture from History

Parses `~/.claude/history.jsonl` and filters prompts by date (defaults to today, Dublin time UTC+1).

```bash
python3 ~/.claude/scripts/capture_session_prompts.py [--date YYYY-MM-DD]
```

**Actions:**
- Read history.jsonl
- Filter by target date
- Parse prompt text and metadata
- Apply categorization heuristics

**Output:** Markdown table with columns: Timestamp, Theme, Subject, Status, Proposed Action, Closure, MoSCoW, Prompt Text

### Phase 2: Review & Refine (Manual)

Open generated file (`~/.claude/sessions/YYYY-MM-DD_prompts.md`) and adjust categorization as needed.

**Actions:**
- Review each row for accuracy
- Adjust Theme, Subject, Status, Proposed Action, Closure, MoSCoW if needed
- Add missing context or corrections
- Verify summary statistics

**Output:** Refined prompts table ready for archival or action planning

### Phase 3: Use for Planning (Optional)

Reference the captured prompts for session review and next-step planning.

**Actions:**
- Filter by Status (Pending) and MoSCoW (Must/Should)
- Identify high-priority items from session
- Feed into TODO planning or next-session prep
- Archive for session reference

---

## Categorization Heuristics

**Theme:** Pattern-based classification into Rules, Skills, Process, Planning, TODOs, Other, Unclassified

**Status:** Detected via markers
- ✅ Done: "complete", "finished", "done", "created"
- ⏳ Pending: "pending", "waiting", "blocked", "todo", "later"
- ✔️ Clarifying Question: "?" at end, "clarif"
- ↩️ Response: "response", "reply", "answer"
- 📋 Note: "noted", "note", "reminder"

**Subject:** Extracted via keyword patterns from prompt text

**MoSCoW:** Applied to pending items based on keyword markers
- Must: "urgent", "critical", "blocking", "asap"
- Should: "high", "important", "soon"
- Could: "nice-to-have", "future", "consider"

**Proposed Action:** Detected from action markers ("do", "create", "update", "build")

**Closure:** Extracted from file creation/update patterns or task completion markers
