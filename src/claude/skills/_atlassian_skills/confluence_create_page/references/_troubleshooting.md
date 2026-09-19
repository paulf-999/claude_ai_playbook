---
date_created: "2026-09-07"
date_updated: "2026-09-19"
status: active
---

# Troubleshooting — confluence_create_page

Common issues and how to resolve them.

---

## Phase 2: Creator Name Incorrect

**Symptom:** Draft shows creator as "paulfry.payroc" or unexpected name; not your real name.

**Root cause:** Creator retrieved from `git config user.name` in this order:
1. git config user.name
2. FULLNAME environment variable
3. System whoami

**Solutions:**

| Source | Command | Example |
|---|---|---|
| Git config | `git config user.name "Your Real Name"` | `git config user.name "Paul Fry"` |
| Environment | `export FULLNAME="Your Real Name"` | `export FULLNAME="Paul Fry"` |
| System | Modify system user (not recommended) | — |

**Verify current user:**
```bash
# Check current resolution (in order)
git config user.name || echo "Not set in git config"
echo $FULLNAME || echo "Not set in FULLNAME env var"
whoami
```

---

## Phase 2: Creator Email Incorrect or Missing

**Symptom:** Creator email shows as "user@payroc.com" or non-Payroc domain.

**Root cause:** Email retrieved from `git config user.email` in this order:
1. git config user.email
2. EMAIL environment variable
3. Constructed as "firstname.lastname@payroc.com"

**Solutions:**

| Source | Command | Example |
|---|---|---|
| Git config | `git config user.email "your.email@payroc.com"` | `git config user.email "paul.fry@payroc.com"` |
| Environment | `export EMAIL="your.email@payroc.com"` | `export EMAIL="paul.fry@payroc.com"` |

**Verify current resolution:**
```bash
git config user.email || echo "Not set in git config"
echo $EMAIL || echo "Not set in EMAIL env var"
```

---

## Phase 3: Draft Not Appearing in Expected Location

**Symptom:** Skill says "Draft written to `~/_drafts/confluence/`" but file not there.

**Possible causes:**

1. **Directory doesn't exist:** Skill auto-creates it; may fail if permissions denied
2. **Hidden directory:** Use `ls -la ~/_drafts/confluence/` to show hidden files
3. **Different shell:** File written to wrong home directory (multi-user systems)
4. **Timeout before save:** If Confluence API call times out before draft is saved, draft may be lost

**Debug steps:**

```bash
# Check if directory exists
ls -la ~/_drafts/confluence/

# Create directory manually if needed
mkdir -p ~/_drafts/confluence/

# Check permissions
ls -ld ~/_drafts/
stat ~/.claude/

# Find drafts anywhere
find ~ -name "*confluence*" -type f 2>/dev/null | head -10
```

---

## Phase 3: Confluence API Timeout

**Symptom:** "⏱️ CONFLUENCE PUBLISH TIMEOUT" appears after 2 minutes; page may or may not publish.

**Causes:**

- Confluence server slow or unreachable
- Large page content (many sections with extensive text)
- Network latency
- Atlassian MCP server rate-limiting

**Solutions:**

| Action | Result |
|---|---|
| **[A] Abort** | Cancel publish, preserve draft in `~/_drafts/confluence/` for retry later |
| **[R] Retry** | Cancel, start fresh publish attempt (may succeed if server recovered) |
| **[C] Continue** | Wait 4 more minutes (max 6 min total); for very slow Confluence instances |

**Prevention:**

- Use `--timeout-seconds N` to adjust timeout (default 120s):
  ```
  /confluence_create_page --outline "X" --title "Y" --timeout-seconds 60
  ```
- Keep page size reasonable (~10 sections max, short content per section)
- Publish during low-traffic hours

**If timeout occurs:**

1. Save the draft path shown in dialog
2. Fix Confluence server issues (if known)
3. Retry: `/confluence_create_page --outline "X" --title "Y" --timeout-seconds 180`

---

## Phase 3: Permission Denied Error

**Symptom:** "Permission denied: You lack write access to space DA"

**Causes:**

- User doesn't have edit permission in target space
- Atlassian MCP token expired or invalid
- Target space doesn't exist

**Solutions:**

1. **Check permissions:** Ask space admin to grant "Editor" role in Confluence space
2. **Re-enable MCP:** `make enable_mcp server=Atlassian` and restart Claude Code
3. **Verify space exists:** Confirm space key (e.g., "DA") in Confluence UI
4. **Use different space:** Specify `--space "YOURSPACE"` if you have access to another space

---

## General: How to Report Issues

If you encounter a bug not listed above:

1. **Save the full error message** — copy entire output
2. **Note the phase:** Phase 1a, 1b, 2, or 3?
3. **Provide context:** What message/outline/title triggered the issue?
4. **Include diagnostic info:**
   ```bash
   git config user.name
   git config user.email
   echo $FULLNAME
   echo $EMAIL
   ```
5. **Check logs:** `~/.claude/logs/` if logging enabled

---

## Performance Tips

- **Faster outline detection:** Lead with action verb and topic: "create page describing X" (vs. "I want to create a page about X")
- **Better titles:** Provide specific outlines: "Airflow cluster deployment in us-west-2" (better than "Airflow")
- **Quicker drafts:** Keep sections list short (<10 sections)
- **Reliable publishing:** Test Confluence access before bulk page creation

---

## Known Limitations (v1.0)

- **Title generation is keyword-based:** May miss semantic nuance; use custom title for important pages
- **No page editing:** This skill creates pages only; use Confluence UI to edit after publishing
- **Pattern detection limited:** Only recognizes `describing`, `about`, `for`, `on` keywords
- **Auto-sections generic:** Defaults to "Overview", "Details", "Summary"; use `--sections` for custom

These will be addressed in Phase 2+ enhancements.
