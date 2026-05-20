## Phase 3 — Resolve reviewers

### 3a — Determine reviewer list

**If `reviewRequests` is non-empty**: use those handles directly. Proceed to 3b.

**If `reviewRequests` is empty** (no auto-assigned reviewers):
1. Get the current UTC time: `date -u +"%H:%M"`.
2. Read the window boundaries from `go_to_reviewers` in `teams_config.json`:
   - `uk_ireland.window.start` / `uk_ireland.window.end`
   - `north_america.window.start` / `north_america.window.end`
3. Evaluate which windows are active based on current UTC time.
   - **Overlap** (both windows active): merge both handle lists.
4. Select the reviewer pool:
   - Both windows active → merge UK/Ireland + North America handles (deduplicated), label: `all active teams`
   - UK/Ireland only → UK/Ireland handles, label: `UK/Ireland team`
   - North America only → North America handles, label: `North America team`
   - Neither window active → use whichever window's end is closest to the current time
5. Exclude the PR author's GitHub handle from the suggestion list.
6. Present the suggested handles to the user:
   > "No reviewers auto-assigned. Suggesting <label> (HH:MM UTC):\n> `handle1`, `handle2`, `handle3`\n> Proceed with these, or specify different handles?"
7. Wait for confirmation. If the user provides a different list, use that instead.

### 3b — Look up each handle

> **Note:** Auto-resolve (step 4 below) requires the Microsoft 365 MCP to be active. If it is not, the placeholder `aad_id` will remain unresolved and the skill will fall back to a plain text @mention.

For each GitHub handle:

1. Check the mapping cache (`github_teams_mapping.json`) for the handle as a key.
2. **Cache hit, valid `aad_id`** — use the cached `display_name` and `aad_id`. Proceed to the next handle.
3. **Cache hit, placeholder `aad_id`** — if `aad_id` equals `"00000000-0000-0000-0000-000000000000"`, treat as a cache miss and proceed to step 4 to auto-resolve the real value.
4. **Cache miss** — attempt automated lookup via Teams message search:
   a. Derive a search name: strip `_pyrc` suffix, replace `-` with space, capitalise each word (e.g. `alice-example_pyrc` → `Alice Example`).
   b. Search Teams chat messages for recent messages from that person:
      ```
      mcp__claude_ai_Microsoft_365__chat_message_search
      query: "from:<first name>"
      limit: 5
      ```
      Scan results for a match on `from.displayName`. Pick the first result whose display name matches.
   c. Read the full message resource (`mcp__claude_ai_Microsoft_365__read_resource` with the message URI) to extract `from.id` (AAD Object ID) and `from.displayName`.
   d. Write the resolved entry to `github_teams_mapping.json`:
      ```json
      "alice-example_pyrc": {
        "display_name": "Alice Example",
        "aad_id": "00000000-0000-0000-0000-000000000000"
      }
      ```
   e. **If no Teams message found** — fall back to derived display name with `aad_id: null`, and warn:
      > "Reviewer `<handle>` not found in Teams message history. Added with derived display name. Post will use plain text @mention."

After resolving all reviewers, note whether **all** have a non-null, non-placeholder `aad_id` — this determines the payload format.
