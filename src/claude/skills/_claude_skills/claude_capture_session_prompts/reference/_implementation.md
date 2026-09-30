# Implementation

## 3-Phase Workflow

### Phase 1: Capture from History

Parses `history.jsonl` in the Claude config directory (`$CLAUDE_CONFIG_DIR`, default `~/.claude`) and filters prompts by date (defaults to today, local time).

Run the **Run:** command in SKILL.md → Example Usage. It uses `${CLAUDE_SKILL_DIR}`, which Claude Code expands only inside SKILL.md.

**Actions:**
- Read history.jsonl
- Filter by target date
- Parse prompt text and metadata
- Apply categorization heuristics

**Output:** Markdown table with columns: Timestamp, Theme, Subject, Status, Proposed Action, Closure, MoSCoW, Prompt Text

### Phase 2: Review & Refine (Manual)

Open generated file (`~/_sessions/YYYY_MM_DD_claude_prompts.md`) and adjust categorization as needed.

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

Rules are checked in the order listed; the first match wins. Matching is lowercase substring matching, so "but" also matches "button".

**Theme:**
- **Unclassified (-):** the whole prompt is `yes`, `no`, `1`, `y` or `n`
- **Rules:** rule, hooks, naming, multifile, style guide, framework, claude_config
- **Skills:** skill, domain, skill.md
- **Process:** refactor, trimming, file, structure, child page
- **TODOs:** todo
- **Planning:** two or more of prompt, audit, capture, session, table, theme, status
- **Other:** anything else

**Status:**
- ✔️ **Clarifying Question:** ends with `?` (unless it starts with a quote mark)
- ↩️ **Response:** contains but, however, "no.", "yes,", i never said, re:, go to plan, entries containing — or is exactly `yes`, `y` or `1`
- 📋 **Note:** starts with "this ", "the " or "it " and has no directive verb (create, add, update, review, audit, ensure)
- ✅ **Done:** contains create a dir, go to plan, or create artifact
- ⏳ **Pending:** contains so i don't like, you've jumped, i want, i told you, you should, before continuing
- ✅ **Done:** contains a directive verb (create, add, update, review, audit, ensure, document)
- ↩️ **Response:** anything else

**Subject:** the first match of Style guides (style guide, payroc_engineering), Hooks (hook), Child pages (child page, multifile), Naming (name), Skill domains (domain), Rules (rule), Prompt audit (prompt, audit, capture), TODOs (todo); blank otherwise

**MoSCoW (Pending prompts only):**
- **Must:** must, critical, urgent, blocker
- **Should:** should, important, priority
- **Could:** could, nice, defer

**Proposed Action:** "Create Artifact" or "Go To Plan Mode" when the prompt contains that phrase

**Closure:** the first file-change phrase found, e.g. "created notes.md", "config.yaml created", "readme updated", "renamed a → b", "removed x from"
