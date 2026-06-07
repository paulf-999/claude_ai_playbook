## Phase 2 — Fetch page data

Call these two tools in parallel:

1. `getConfluencePage` with the page ID — returns title, body content, space key, author,
   last modified date, and version number
2. `getConfluencePageFooterComments` with the page ID — returns existing footer comments

From the results, extract:

| Field | Source |
|---|---|
| `page_id` | The Confluence page ID |
| `page_title` | The page title |
| `space_key` | The Confluence space key |
| `author` | Display name of the page author |
| `last_modified` | ISO date of last modification |
| `body_content` | Page body as plain text (extracted from ADF or storage format) |
| `page_url` | Full Confluence URL — returned directly, or constructed as `<base_url>/wiki/spaces/<space_key>/pages/<page_id>` |

If the body content exceeds 3000 words, truncate to 3000 words and include this note
when passing content to the reviewer agent in Phase 3:

> *"Note: page content truncated to 3000 words — review covers visible content only."*
