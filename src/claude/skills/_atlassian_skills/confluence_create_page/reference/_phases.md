---
date_created: "2026-08-28"
date_updated: "2026-10-17"
status: active
---

# Interactive phases

## 🔍 Phase 1 — Identify the page type

**Skip this phase if:** Pattern argument was provided and validated ✓

**Otherwise:** Ask the user which type of Confluence page they want to create. Present:

**Available patterns:**

| Pattern | Description |
|---|---|
| `general_page` | General-purpose page — free-form sections using the standard page template |
| `platform_risk_assessment` | Platform Risk & Maturity Assessment — rates one tool or component across fixed themes (L/M/H) |

Wait for the user's response before proceeding.

---

## 🏗️ Phase 2 — Follow the chosen pattern

Read the chosen pattern's file and follow it, then continue to the **Local Draft Review** phase below:

- `general_page` → `reference/patterns/_general_page.md`
- `platform_risk_assessment` → `reference/patterns/_platform_risk_assessment.md`

**Critical constraints (every pattern):**
- Do NOT skip the Local Draft Review phase — never call `createConfluencePage` or `updateConfluencePage` without first completing draft review.
- Do NOT publish at the space root — all pages must have a parent page confirmed by the user.
- Do NOT infer the target Confluence space — confirm it with the user if not stated in the request.
- Do NOT include names of individuals in the page — use generic role descriptors throughout.

---

## 🖊️ Local Draft Review (mandatory — always runs)

**This phase cannot be bypassed.** Even if the user provides all arguments via flags or config file, you must complete this phase before publishing.

After gathering all page content via the pattern phases, before creating anything in Confluence:

1. **Write the draft** — Save the page content as a markdown file:
   - Directory: `~/_drafts/confluence/`
   - Filename: `YYYY_MM_DD_<slug>.md` — date first, underscores only, per `writing_style.md` (slug: lowercase, words separated by underscores, no special characters)
   - Path: expand `~` to the user's absolute home path before calling Write — never write inside the Claude config folder
   - Render the content faithfully — use markdown equivalents of ADF components (e.g. `> ℹ️` for info panels, `> 📝` for note panels, `**bold**` for labels, tables for structured data)

2. **Ask for feedback** — Inform the user of the file path and request review:
   > "Draft written to `~/_drafts/confluence/<filename>`. Please review and let me know any changes before I publish to Confluence."

3. **Iterate** — Apply feedback and rewrite the file until the user explicitly approves.

4. **Publish** — Once approved, proceed with the pattern's original "Create the Confluence page" step, building the ADF from the approved draft content.
