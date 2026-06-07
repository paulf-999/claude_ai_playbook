# Date & Time Standards

ISO format applies to technical contexts (code, metadata, logs). Human-facing content uses
English sentence-style dates instead. Do not retroactively update existing files — apply
opportunistically when a file is being actively modified for another reason.

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

## Applies to — technical contexts

Use ISO format where dates are machine-readable, sortable, or stored:

- Frontmatter fields (e.g. `last-reviewed`, `created`, `updated`)
- Changelog and release note dates
- Log entries and audit outputs
- Code files and technical documentation
- Memory files and plan files
- Existing files being actively modified for another reason — do not update files solely to fix date formatting

---

## Known exceptions

| Context | Format | Reason |
|---|---|---|
| Draft filenames (`~/_drafts/`) | `YYYY-MMM-DD` | 3-letter month abbreviation is easier to read at a glance in `ls` output — e.g. `rundeck_page_2026-May-20.md` |

---

## Does not apply to — human-facing content

Use English sentence-style dates (e.g. `1st May 2026`, `23rd April 2026`) in content written for a human audience:

- Confluence pages
- Pull request descriptions
- Teams messages and emails
- Jira ticket descriptions and comments
- Meeting notes, agendas, and catchup prep output
- DR tracking notes and similar narrative documents
