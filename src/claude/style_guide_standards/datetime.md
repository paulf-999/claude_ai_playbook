# Date & Time Standards

Applies to all Claude-generated content, file metadata, new code, and documentation from
adoption date onwards. Do not retroactively update existing files — apply opportunistically
when a file is being actively modified for another reason.

---

## Standard formats

| Type | Format | Example |
|---|---|---|
| Date | `YYYY-MM-DD` | `2026-04-10` |
| Datetime | `YYYY-MM-DDTHH:MM:SSZ` | `2026-04-10T14:30:00Z` |

---

## Timezone

UTC is the required timezone for all datetimes. The `Z` suffix must always be included —
it makes the timezone explicit and avoids ambiguity.

---

## Applies to

- Frontmatter fields (e.g. `last-reviewed`, `created`, `updated`)
- Changelog and release note dates
- Log entries and audit outputs
- New code files and documentation
- Existing files being actively modified for another reason — do not update files solely to fix date formatting
