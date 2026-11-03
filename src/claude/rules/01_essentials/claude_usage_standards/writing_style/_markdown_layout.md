<!-- version: 1.3.0 -->
<!-- created: 2026-11-02 -->
<!-- updated: 2026-11-03 -->
# 🧱 Writing style — Markdown layout

**Purpose:** Set how headings, lists and tables are laid out and how much each holds, so every page scans the same way.

---

## 😀 Emojis

- 📍 **Location decides:** repo docs, rule files, PRs, issues and plans use the rules below, chat follows `claude_response_standards.md`, and other content uses the audience table's Emojis column.
- ✅ **Give one emoji to:** each heading, labelled top-level bullet and table body row, in the row's first cell.
- 🚫 **Give none to:** header rows, child bullets, bullets inside cells, plain list items, numbered items, and pointer bullets such as `Part of`, `Read`, `Read on demand` and `Loads on its own from`.
- ⬅️ **Placement:** the emoji comes first, before the bold keyword.
- 🗒️ **Plans:** plan tables also put an emoji on each cell bullet, as `plan_file_format.md` sets out.

## 🔢 Lists

- 📝 **Bullets over prose:** use a list for rules and steps rather than a paragraph.
- 5️⃣ **Five at most:** keep each bulleted list to 5 top-level items, counted as displayed, since a blank line doesn't end a list.
- 🔢 **Steps:** numbered steps can run past 5, since a procedure needs every step.
- 📋 **Lead-in:** open a list with a sentence saying what the items are, unless the heading right above it already says so.
- ➗ **Overflow:** move a sixth item under a new subheading, or into a table if the items share fields.

## 📊 Tables

- 🧮 **When:** use a table to compare two or more categories that share the same fields, and keep a single list with no comparison as bullets.
  - **Signal:** writing `**Category A:**` then `**Category B:**` with the same fields for each means it's a table.
  - **Example:** a `| Tool | Can do | Can't do |` table beats a separate bullet list per tool.
- 🧱 **Cells:** default to one point in plain text, in 25 words or fewer.
- 🔘 **Cell bullets:** use 2–3 when a cell genuinely holds separate points, as on reference pages, each opening with a bold keyword, joined as `• **A:** … <br>• **B:** …`.
  - **Overdone:** if most cells in a table need bullets, split the table or move the detail to a child page.

## ✂️ Density

- 🎯 **Limits are ceilings:** aim well under any length limit, since a page that fills its limit is usually packed.
- 1️⃣ **One point each:** give a second point its own bullet or row, or cut it.
- 🧹 **Caveats:** keep a qualifier only if the reader would act differently without it.
- 📏 **Short sentences:** one idea each, about 25 words at most, with caveats split out or cut.
- 🔁 **Review for cuts:** ask what can be removed, not only what's missing.
  - ❌ **Packed, when every cell looks like this:** `| 🌱 **Minimal** | • **Mandatory:** only CLAUDE.md, tests, CI and two checks.<br>• **Everything else:** optional. |`
  - ✅ **One point:** `| 🌱 **Minimal** | Only the baseline is mandatory. |`
