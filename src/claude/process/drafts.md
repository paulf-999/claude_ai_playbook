# 📝 Draft files

Working and draft files written during a session go under `~/_drafts/`, not `/tmp/` or arbitrary locations.

---

## 📁 Root path

```
~/_drafts/
```

The underscore prefix sorts this directory to the top in `ls` output, making it easy to find. Create the directory on first use — do not assume it exists.

---

## 🗂️ Subdirectories by type

Organise drafts into subdirectories by content type:

| Subdirectory | Use for |
|---|---|
| `confluence/` | Confluence page drafts |
| `jira/` | Jira ticket drafts or bulk input files |
| `meetings/` | Meeting prep and agenda outputs |
| `pr/` | PR body drafts |
| `teams/` | Teams message drafts |
| `email/` | Email drafts |
| `general/` | Anything that does not fit the above |

Create subdirectories on first use.

---

## 🏷️ Filename format

```
<slug>_YYYY-MMM-DD.md
```

- `slug` — lowercase, underscores, descriptive (e.g. `rundeck_page`, `sprint_63_tickets`)
- `YYYY-MMM-DD` — today's date with 3-letter month abbreviation (e.g. `2026-May-20`). Note: this intentionally deviates from the ISO `YYYY-MM-DD` standard — 3-letter months are easier to read at a glance in `ls` output.

Example: `~/_drafts/confluence/rundeck_page_2026-May-20.md`

---

## ♻️ Lifecycle

Draft files are working artefacts — they are not committed and not cleaned up automatically. The user is responsible for clearing `~/_drafts/` when no longer needed.
