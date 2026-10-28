---
date_created: "2026-09-07"
date_updated: "2026-10-28"
status: active
---

# 🔧 Troubleshooting — confluence_create_page

**Purpose:** Match a symptom to its cause and fix, for problems the steps in `_error_recovery.md` don't settle on their own.

## 🔗 Atlassian access fails at the pre-check

- **Symptom:** `getAccessibleAtlassianResources` errors or returns no sites.
- **Cause:** the Atlassian MCP server is off, or its login has expired.
- **Fix:** run `make enable_mcp server=Atlassian`, restart Claude Code, then run the skill again.

## 📂 Draft isn't where the skill said

- **Symptom:** nothing at `~/_drafts/confluence/YYYY_MM_DD_<topic>.md`.
- **Cause:** `~` wasn't expanded before the Write call, so the file landed in a literal `~` folder inside the current directory.
- **Fix:** look for a stray `~/` folder in the directory you ran Claude from, move the draft to your real home folder, and delete the stray folder.

## 🔐 Permission denied when publishing

- **Symptom:** Confluence rejects `createConfluencePage` for the chosen space.
- **Cause:** you can't add pages to that space, or the space key or parent page is wrong.
- **Fix:** check the space key and parent page in Confluence, ask a space admin for edit access, or pick a space you can write to.

## ⏳ Publishing hangs or fails part-way

- **Symptom:** the publish call is slow, errors, or you can't tell whether it worked.
- **Cause:** a slow or unreachable Confluence site, or a dropped MCP connection.
- **Fix:** check the parent page in Confluence for a new draft before retrying, so you don't create a duplicate.
  - **Draft kept:** the approved local draft stays in `~/_drafts/confluence/`, so a retry needs no new review.

## 📄 The page isn't live

- **Symptom:** the new page shows as a draft in Confluence.
- **Cause:** this is by design, because the skill always creates pages with `status: draft`.
- **Fix:** open the page in Confluence and publish it yourself, and set the wide-view toggle there if you want it.

## 👤 Names were replaced with roles

- **Symptom:** the page says "platform owner" where you gave a person's name.
- **Cause:** by design, since the pattern rules forbid naming individuals on the page.
- **Fix:** add names in Confluence after publishing if your space allows it.
