<!-- version: 1.0.0 -->
<!-- created: 2026-11-02 -->
<!-- updated: 2026-11-02 -->
# 🧱 Writing style — Markdown layout

**Purpose:** Set how headings, lists and tables are laid out, so every page scans the same way.

---

## 😀 Emojis

- 📍 **Location decides:** repo docs, rule files, PRs, issues and plans use the rules below, chat follows `claude_response_standards.md`, and other content uses the audience table's Emojis column.
- ✅ **Give one emoji to:** each heading, top-level bullet and table body row, in the row's first cell.
- 🚫 **Give none to:** header rows, child bullets, bullets inside cells, numbered items, and pointer bullets such as `Part of`, `Read`, `Read on demand` and `Loads on its own from`.
- ⬅️ **Placement:** the emoji comes first, before the bold keyword.
- 🗒️ **Plans:** plan tables also put an emoji on each cell bullet, as `plan_file_format.md` sets out.

## 🔢 Lists

- 📝 **Bullets over prose:** use a list for rules and steps rather than a paragraph.
- 5️⃣ **Five at most:** keep each list, bulleted or numbered, to 5 top-level items, counted as displayed, since a blank line doesn't end a list.
- ➗ **Overflow:** move a sixth item under a new subheading, or into a table if the items share fields.

## 📊 Tables

- 🧮 **When:** use a table to compare two or more categories that share the same fields, and keep a single list with no comparison as bullets.
  - **Signal:** writing `**Category A:**` then `**Category B:**` with the same fields for each means it's a table.
  - **Example:** a `| Tool | Can do | Can't do |` table beats a separate bullet list per tool.
- 🧱 **Cells:** keep each cell to 25 words or fewer, and use plain text unless it holds two or more points.
- 🔘 **Cell bullets:** open each with a bold keyword and hold one sentence, joined as `• **A:** … <br>• **B:** …`, with no `<br>` after the last.
