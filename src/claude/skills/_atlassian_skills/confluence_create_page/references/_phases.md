# Interactive phases

## 🔍 Phase 1 — Identify the page type

**Skip this phase if:** Pattern argument was provided and validated ✓

**Otherwise:** Ask the user which type of Confluence page they want to create. For the MVP, present:

**Available pattern:**

| Pattern | Description |
|---|---|
| `general_page` | General-purpose page — free-form sections using the standard DM page template |

Additional patterns (how_to, requirements, incident_report, design_decision, and data platform patterns) will be available in Phase 2.

Wait for the user's response before proceeding.

---

## 🏗️ Phase 2 — Follow the pattern

Read the pattern file and follow the instructions within it exactly:

- **Generic patterns** — `~/.claude/skills/confluence_create_page/templates/<pattern_name>.md`
- **Data platform patterns** — `~/.claude/skills/confluence_create_page/templates/data_platform/<pattern_name>.md`

Every pattern includes its own phases (typically: gather page details, gather section content, clarify and confirm). Follow the pattern's instructions precisely, gathering all inputs interactively.

The pattern will conclude with a **"Create the Confluence page"** instruction. Do not execute that yet — proceed to the **Local Draft Review** phase below first.

**Critical constraints:**
- Do NOT skip the Local Draft Review phase — never call `createConfluencePage` or `updateConfluencePage` without first completing draft review.
- Do NOT publish at the space root — all pages must have a parent page confirmed by the pattern or the user.
- Do NOT infer the target Confluence space — confirm it with the user if not stated in the request.
- Do NOT include names of individuals in the page — use generic role descriptors throughout.

---

## 🖊️ Local Draft Review (mandatory — always runs)

**This phase cannot be bypassed.** Even if the user provides all arguments via flags or config file, you must complete this phase before publishing.

After gathering all page content via the pattern phases, before creating anything in Confluence:

1. **Write the draft** — Save the page content as a markdown file:
   - Directory: `~/_drafts/confluence/`
   - Filename: `<slug>_YYYY-MMM-DD.md` (slug: lowercase, words separated by underscores, no special characters)
   - Render the content faithfully — use markdown equivalents of ADF components (e.g. `> ℹ️` for info panels, `> 📝` for note panels, `**bold**` for labels, tables for structured data)

2. **Ask for feedback** — Inform the user of the file path and request review:
   > "Draft written to `~/_drafts/confluence/<filename>`. Please review and let me know any changes before I publish to Confluence."

3. **Iterate** — Apply feedback and rewrite the file until the user explicitly approves.

4. **Publish** — Once approved, proceed with the pattern's original "Create the Confluence page" step, building the ADF from the approved draft content.

5. **Optional review** — After publishing, ask:
   > "Page published. Would you like a Claude review posted as a comment? (y/n)"
   If yes, invoke `/confluence_review_page` with the newly published page ID.
