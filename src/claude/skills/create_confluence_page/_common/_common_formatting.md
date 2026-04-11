# Shared Confluence page formatting rules

Apply these rules consistently to every page created by any `create_confluence_page` pattern.

---

## Section headings

- All level-1 section headings must include an emoji prefix.
- Use the standard emoji mapping in `_common/_common_header.md`. Choose a contextually appropriate emoji for any section not in the standard mapping.

---

## Status fields

- Page status and any item-level statuses (e.g. sprint item status, task status) must always use the ADF `status` node — never plain text.
- Standard colour mapping:

| Status | color |
|---|---|
| Not started | `red` |
| In progress | `yellow` |
| Ready for review | `blue` |
| Complete | `green` |

- For item-level statuses outside the standard set, apply the closest match:

| Status type | color |
|---|---|
| Planned | `neutral` |
| Blocked / Waiting | `red` |
| In progress / Active | `yellow` |
| Done / Complete | `green` |
| Needs review / Input required | `blue` |

---

## Tables

- All table nodes must include `"attrs": {"layout": "full-width", "isNumberColumnEnabled": false}` to ensure the table fills the available page width and is not rendered at a reduced or centred size.
- Header row cells must use `tableHeader` nodes (not `tableCell`).
- Header cell text must be bold: `"marks": [{"type": "strong"}]`.
- Cells containing multiple values (e.g. key tasks, to-dos) should use multiple `paragraph` nodes within the `tableCell` — not a single comma-separated string.
- Cells that describe a step, action, phase, or category must include a contextually appropriate emoji prefix to aid scannability. Use the emoji mapping in `_common_header.md` as a guide; extend it as needed. Examples: `🔍 Select pattern`, `✅ Confirm`, `⚠️ Risk identified`.
- Step cells in sequential tables (e.g. "How it works") must be numbered: `1. 📋 Step name`, `2. 💬 Next step`, etc.

---

## Panels

- Use `note` panel for disclaimers, callouts, and system-generated notices.
- Use `info` panel for purpose statements and contextual guidance.
- Use `warning` panel for important warnings that require user attention.
- Any content prefixed with "Important:" must always be placed in a `note` panel — never as inline text or a blockquote.

---

## Prerequisites

- If a component or page has prerequisites, they must always appear under their own dedicated heading (e.g. `⚙️ Prerequisites`) rather than embedded as a bullet point within another section.

---

## Inline code

- Wrap component names, file paths, commands, and technical identifiers in inline code: `"marks": [{"type": "code"}]`.

---

## Bold labels

- Field labels in metadata and summary sections (e.g. **Creator**, **Version**, **Date Created**) must be bold: `"marks": [{"type": "strong"}]`.

---

## Rule dividers

- Place a `rule` node after every body section, including the last section on the page.

---

## Lists

- Prefer `bulletList` over prose when presenting multiple items.
- Use `orderedList` for sequential steps or ranked items.
- Do not use comma-separated inline lists where a bullet list would be clearer.
- Keep bullet lists to a maximum of 5 items. If more are needed, either:
  - Group related items under sub-bullets, or
  - Restructure the content as a table — this is usually the better choice when items have consistent structure.

---

## Alignment

- All block-level components must be left-aligned (or full-width) by default. This applies to tables, code blocks, panels, and any other block-level node.
- Do not centre or right-align any component unless explicitly requested.
- In ADF, this means omitting any alignment attribute from nodes that support it, or setting `"attrs": {"layout": "default"}` on `codeBlock` nodes — the Confluence default rendering is left-aligned.
