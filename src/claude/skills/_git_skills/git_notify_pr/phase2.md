## Phase 2 — Get PR metadata

If a PR number was passed as `$ARGUMENTS`, use it. Otherwise detect the open PR for the current branch:

```bash
gh pr view --json number,title,url,reviewRequests,author,body,files
```

Extract:
- `number`, `title`, `url`
- `author.login` — GitHub handle of the PR author; look up in the reviewer cache to get `display_name`, falling back to the handle itself if not found
- `reviewRequests[].login` — GitHub handles of assigned reviewers (may be empty)
- `body` — for change type detection
- `files[].path` — for layer detection

**Change type**: Scan `body` for `- [x]` and extract the bold label on that line (e.g. `**Feature**` → `Feature`, `**Refactoring/housekeeping**` → `Refactoring`). Strip markdown and emoji. If none found, omit the Change Type line.

**DWH layers**: Only if `layers` is non-empty in `teams_config.json` — map changed file paths to labels using the `layers` array. For each file path, check if it starts with any configured prefix and collect the corresponding label. Deduplicate and sort. Use `-` if no files match any prefix. If `layers` is empty (`[]`), skip layer detection entirely and omit the DWH layers line from the message.
