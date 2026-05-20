## Phase 1 — Identify the page

If `$ARGUMENTS` is a Confluence page URL (contains `/wiki/spaces/` or `/pages/`), extract
the numeric page ID from the URL path segment following `/pages/`.

If `$ARGUMENTS` is a numeric string, use it directly as the page ID.

If `$ARGUMENTS` is empty or neither a URL nor a numeric ID, ask the user:

> "Please provide the Confluence page URL or page ID to review."

Wait for the user's response, then extract or use the page ID before proceeding to Phase 2.
