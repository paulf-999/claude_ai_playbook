## Message format

When `layers` is non-empty:
```
PR raised: [#N](url)
Title: <title>
Reviewers: @DisplayName1  @DisplayName2  @DisplayName3
Raised by: <author_display_name>
Change Type: Refactoring
DWH layers: staging, mart
```

When `layers` is empty:
```
PR raised: [#N](url)
Title: <title>
Reviewers: @DisplayName1  @DisplayName2  @DisplayName3
Raised by: <author_display_name>
Change Type: Refactoring
```

---

## Phase 4 — Build message and post

### 4a — Confirm before posting

Before assembling the payload, present a confirmation prompt:

> **About to post to Teams:**
> **Title:** \<pr_title\>
> **Reviewers:** \<DisplayName1\>, \<DisplayName2\>, \<DisplayName3\>
>
> Post? (y/n)

Wait for the user's response. If the user says no, stop. Do not post.

### 4b — Assemble and post

Assemble the message text:
```
PR raised: [#N](url)
Title: <title>
Reviewers: @DisplayName1  @DisplayName2  @DisplayName3
Raised by: <author_display_name>
Change Type: Refactoring
DWH layers: staging, mart    ← omit this line if layers is []
```

Omit `Change Type` if not detected. Omit `DWH layers` if `layers` is `[]` in `teams_config.json`. Always include `Raised by`.

**All reviewers have `aad_id`** → use Adaptive Card with proper @mentions:

```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.4",
  "msteams": {
    "entities": [
      {
        "type": "mention",
        "text": "<at>Alice Example</at>",
        "mentioned": { "id": "<aad_id>", "name": "Alice Example" }
      }
    ]
  },
  "body": [
    {
      "type": "TextBlock",
      "text": "PR raised: [#N](url)",
      "wrap": true
    },
    {
      "type": "TextBlock",
      "text": "Title: <PR title>",
      "wrap": true,
      "spacing": "none"
    },
    {
      "type": "TextBlock",
      "text": "Reviewers: <at>Alice Example</at>  <at>Bob Example</at>",
      "wrap": true,
      "spacing": "none"
    },
    {
      "type": "TextBlock",
      "text": "Raised by: <author_display_name>",
      "wrap": true,
      "spacing": "none"
    },
    {
      "type": "TextBlock",
      "text": "Change Type: Refactoring",
      "wrap": true,
      "spacing": "none"
    },
    {
      "type": "TextBlock",
      "text": "DWH layers: staging",
      "wrap": true,
      "spacing": "none"
    }
  ]
}
```

Omit the Change Type TextBlock if no change type was detected. Omit the DWH layers TextBlock if `layers` is `[]`. Omit any reviewer from `msteams.entities` whose `aad_id` is null — use plain `@DisplayName` in the Reviewers TextBlock instead.

**Note on long titles**: `"wrap": true` causes long PR titles to flow onto the next line within the card — this is expected behaviour, not a formatting error.

**Any reviewer lacks `aad_id`** → use MessageCard (display names only, no clickable @mentions):

```json
{
  "@type": "MessageCard",
  "@context": "https://schema.org/extensions",
  "themeColor": "0076D7",
  "markdown": true,
  "text": "PR raised: [#N](url)\nTitle: <title>\nReviewers: @DisplayName1  @DisplayName2\nRaised by: <author_display_name>\nChange Type: Refactoring\nDWH layers: staging"
}
```

Omit `Change Type: ...` from the `text` string if not detected. Omit `\nDWH layers: ...` if `layers` is `[]`.

**Post**:

1. Write the assembled JSON payload to `/tmp/teams_payload.json` using the Write tool.
2. Post using Python's built-in `urllib.request` (no curl required):

```bash
python3 - <<'PYEOF'
import urllib.request, sys

WEBHOOK_URL = "REPLACE_WITH_WEBHOOK_URL"

with open('/tmp/teams_payload.json', 'rb') as f:
    data = f.read()

req = urllib.request.Request(
    WEBHOOK_URL,
    data=data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        http_status = resp.status
        open('/tmp/teams_notify_response.txt', 'w').write(resp.read().decode())
except urllib.error.HTTPError as e:
    http_status = e.code
    open('/tmp/teams_notify_response.txt', 'w').write(e.read().decode())

print(http_status)
PYEOF
```

Substitute the actual `webhook_url` value from `teams_config.json` into `WEBHOOK_URL` before running.

- `200` or `202` → report: `"Teams notification posted for PR #N."`
- Any other status → report the HTTP status and contents of `/tmp/teams_notify_response.txt` for diagnosis.
