# 🔌 Rules — External integrations (MCP servers)

These rules apply whenever interacting with external services via MCP servers (Atlassian, GitHub, Microsoft 365, etc.). API calls to external services can be slow and expensive — minimise them.

---

## ♻️ Reuse before querying

- Before making a new MCP call, check whether the data is already available locally:
  - MCP tool results are persisted to disk in the session's `tool-results/` directory — grep or parse these first.
  - Data fetched earlier in the same session (issues, field metadata, components, sprints) should be reused rather than re-fetched.
- Only make a new API call when the required data is genuinely not available locally or is likely stale.

---

## 🎯 Fetch only what you need

- Use field filters (`fields` parameter) when available to limit response payload — do not fetch full issue objects when only one or two fields are needed.
- Use `maxResults` and pagination rather than fetching all records at once.
- Prefer a single targeted call over multiple broad calls that return large payloads.

---

## 🧮 Calculate over query

- Where data can be derived from what is already known (e.g. sprint dates calculated from a known cadence, quarter derived from a date), prefer calculation over an additional API call.
- Only query external systems when the derived value would be unreliable or the source data is unavailable.

---

## 📦 Batch operations

- When creating or updating multiple records, batch changes into the fewest possible calls.
- Group reads before writes — fetch all required data first, then apply all changes in sequence.
