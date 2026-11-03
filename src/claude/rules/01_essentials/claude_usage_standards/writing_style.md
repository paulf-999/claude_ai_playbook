<!-- version: 2.1.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-11-03 -->
<!-- applies_to: * -->
<!-- miss_cost: low — prose drifts from the house style, which review catches -->
<!-- loading: always-on — every reply and file Claude writes follows it -->
# ✏️ Writing style

**Purpose:** Establish consistent, scannable, and user-friendly writing conventions for all content Claude produces — ensuring clarity, respect for reader time, and professional presentation.

## 📋 Contents

- [Style — all content](#-style--all-content)
- [Clarity principles — all content](#-clarity-principles--all-content)
- [Rule files — additional constraints](#-rule-files--additional-constraints)
- [Drafts and errors](#-drafts-and-errors)
- [Child pages](#-child-pages)

---

## 🎨 Style — all content

Applies to **all** content Claude produces — responses, drafts, Confluence pages, Jira tickets, rule files, plans, scratch notes and repo docs — and no file type or context is exempt.

- 🗣️ **Frame as positive actions:** in prompts and rules, tell Claude what to do instead of what not to do, because that steers output better, while docs for people may state a plain prohibition.
  - **Avoid:** "Do not use excessive markdown."
  - **Prefer:** "Write in flowing prose paragraphs with complete sentences."
- 🔑 **Bold keyword and colon:** open a bullet with its key term in bold, such as **Why:** or **Note:**, when the label adds meaning, as for rules and definitions.
  - **Plain lists:** leave simple item lists and numbered steps unlabelled, since a label that repeats the text slows reading.
- 1️⃣ **One sentence per bullet:** put a second sentence, or a clause after a semicolon, in a child bullet, while an em-dash aside stays part of its sentence.
- ✂️ **Brevity:** if a sentence can be cut without losing meaning, cut it.
- 📜 **History lives in git:** describe only the current state in repo files, and leave notes about removed, merged, archived or renamed files to the git log.
  - **Exception:** an incident that justifies a rule stays as that rule's evidence (e.g. `portable_paths.md`).
  - **Records:** plans, audits and changelogs keep their status history, because recording it is their purpose.

### 🇬🇧 Spelling and rewritten content

- 🇬🇧 **British spelling:** use -ise and other British forms (organise, behaviour, centralise) in prose and headings, and in new identifiers.
  - **Exception:** existing code identifiers, filenames and function names keep their spelling (e.g. `_testing_file_organization.md`).
- ✍️ **No transposition exemption:** content you rewrite, copy or split into new files follows house style from the first draft, while a file only moved or renamed keeps its content.

## 👥 Clarity principles — all content

Lead with what things do, not how they work. Assume no prior familiarity with the domain. Explain jargon or use plain language instead. Readers should understand the core idea in 60 seconds. Structure for progressive disclosure: heading + opening = complete idea; first section = enough to use; later sections = advanced cases.

### ✍️ Writing Style for Skills

| Principle | ❌ Avoid | ✅ Prefer |
|---|---|---|
| 🎯 **Lead with what it does** | "This skill uses complex validation patterns" | "Validates Confluence pages against team standards" |
| 🗣️ **Plain language** | "Uses maturity framework with scope gates" | "Works with draft (early), tactical (stable), and strategic (production-ready) phases" |
| ⏱️ **Clear in 60 seconds** | An opening that needs the rest of the file | An opening someone unfamiliar gets when read aloud |
| 🪜 **Progressive disclosure** | Workflow detail before the overview | What it does, then the Overview, then Workflow and Known Gaps |

## 📏 Rule files — additional constraints

- 📐 **Limit:** about 100 lines, up to 110 tolerated, and beyond that split into a parent and child files.
- 🎯 **Scope:** one concept per file, so unrelated rules live in separate files.
- ↩️ **Newline:** files end with a single newline.
- 🔗 **Shared content:** point to it with a `Loads on its own from` or `Read on demand` line instead of copying it inline.

## 📝 Drafts and errors

- 📝 **Drafts:** write proposed content to `~/_drafts/<domain>/YYYY_MM_DD_<topic>.md`.
- 🚨 **Errors:** write error details to `~/_errors/<domain>/YYYY_MM_DD_<topic>.md`.
- 📚 **Reference:** put an evergreen guide Claude reads on demand in `~/claude/_rules_lazy_load/<topic>.md`, named in a `**Read on demand:**` pointer, and human-only background in the playbook repo's `docs/reference/`.
- 🏷️ **File naming:** date-first for drafts and errors, and a snake_case topic only for reference, e.g. `2026_08_04_onboarding_plan.md` or `claude_code_automation_commands.md`.
  - **Why underscores:** the date prefix is part of the filename, so it follows `naming_standards.md`'s snake_case rule, while `YYYY-MM-DD` stays correct as a data value.

| Domain | Use for |
|---|---|
| 👥 `1on1` | One-to-one meeting notes and prep |
| 📄 `confluence` | Confluence page drafts |
| ✉️ `email` | Email drafts |
| 🗂️ `general` | Anything that doesn't fit a specific domain |
| ❗ `important` | High-priority items requiring attention |
| 🎫 `jira` | Jira ticket drafts |
| 🗓️ `meetings` | Meeting notes and agendas |
| 🧭 `plans` | Plans and proposals |
| 📚 `reference` | Reference material |
| 💬 `teams` | Microsoft Teams message drafts |

## 🧩 Child pages

- **Loads on its own from:** `rules/01_essentials/claude_usage_standards/writing_style/_markdown_layout.md` — emojis, lists and tables.
- **Loads on its own from:** `rules/01_essentials/claude_usage_standards/writing_style/_audience_and_depth.md` — audiences, depth and the Executive Summary.
- **Loads on its own from:** `rules/01_essentials/claude_usage_standards/multifile_document_organisation.md` — when to split a document into a parent and children.
