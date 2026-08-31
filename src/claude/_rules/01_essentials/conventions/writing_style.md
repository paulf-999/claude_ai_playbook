# ✏️ Writing style

**Purpose:** Establish consistent, scannable, and user-friendly writing conventions for all content Claude produces — ensuring clarity, respect for reader time, and professional presentation.

## 📋 Contents

- [Style — all content](#-style--all-content)
- [Clarity principles — all content](#-clarity-principles--all-content)
- [`_rules/` files — additional constraints](#-_rules-files--additional-constraints)
- [Pre-writing checks](#-pre-writing-checks)
- [Drafts and errors](#-drafts-and-errors)
- [Child pages](#-child-pages)

---

## 🎨 Style — all content

Applies to **all** content Claude produces — responses, drafts, Confluence pages, Jira tickets, `_rules/` files, plans, scratch notes, and internal docs. The list is illustrative, not exhaustive: no file type or context is exempt.

- **Emojis:** use on all major headings and callout blocks — they aid scannability.
- **Bullets:** prefer over prose for rules and lists.
- **Frame as positive actions, not negations:** tell Claude what to do instead of what not to do — this reliably steers output better.
  - ❌ "Do not use excessive markdown"
  - ✅ "Write in flowing prose paragraphs with complete sentences"
- **Leading bold keyword + colon:** open each bullet with the key term in bold:
  - `**Why:**` rationale for a decision
  - `**Note:**` a caveat or edge case
  - `**Example:**` a concrete illustration
- **One sentence per bullet:** if a bullet needs more than one sentence, use child bullets — never run multiple sentences in a single bullet.
- **Brevity:** if a sentence can be cut without losing meaning, cut it.
- **No transposition exemption:** moving, copying, or splitting existing content into new files does not exempt the output — apply house style on the first draft, never as a later pass.

## 👥 Clarity principles — all content

Lead with what things do, not how they work. Assume no prior familiarity with the domain. Explain jargon or use plain language instead. Readers should understand core idea in 60 seconds. Structure for progressive disclosure: heading + opening = complete idea; first section = enough to use; later sections = advanced cases.

- **Lead with TL;DR:** open every response with a one- to two-sentence high-level summary before any supporting detail — the reader should get the answer before the reasoning.

### ✍️ Writing Style for Skills

When writing SKILL.md files, apply these conventions specific to skill documentation:

**Lead with what it does, not how it works:**
- ❌ "This skill uses complex validation patterns"
- ✅ "Validates Confluence pages against team standards"

**Explain jargon or replace with plain language:**
- ❌ "Uses maturity framework with scope gates"
- ✅ "Works with draft (early), tactical (stable), and strategic (production-ready) phases"

**Clarity without context:** Reader should understand in 60 seconds
- Test: Read opening aloud to someone unfamiliar — do they get it?
- Use: Concrete examples, plain language, short sentences

**Progressive disclosure:** Essentials first, details layer in
- Opening: what it does
- First section (Overview): enough to use, high-level summary
- Later sections (Workflow, Known Gaps): advanced cases and roadmap

## 📏 `_rules/` files — additional constraints

- **Limit:** ~100 lines. Up to 110 tolerated; beyond that, split into a parent index + child files referenced from the parent.
- **Scope:** one concept per file — don't bundle unrelated rules into a single file.
- **Newline:** files must end with a single newline.
- **Imports:** use `@`-references for shared content — never duplicate inline.

## ✍️ Pre-writing checks

- **Audience:** before producing content for an external audience (Confluence, Jira, email, comms), confirm the target audience and calibrate technical depth accordingly — if unknown or spanning multiple groups, ask before writing.

| No. | Audience | Content focus | Technical level | Depth |
|---|---|---|---|---|
| 1 | 💼 **Management** | Business outcomes | None | • Non-technical — plain language only, no jargon<br>• Project-level — progress, status, decisions, and risks; no domain-specific terminology |
| 2 | 🔭 **Technical management** | Strategy & outcomes | Partial | • Technology-aware and strategy-level — outcomes and concepts<br>• Not implementation mechanics |
| 3 | 📊 **Data analytics team** | Data & insights | Partial | • Semi-technical — understands data concepts and business domain<br>• Not stack-aware — focus on what the data means, not how it's produced |
| 4 | 🗄️ **Data engineering team** | Technical implementation | Full | • Fully technical — data stack focus (Airflow, dbt, Snowflake, connectors) |
| 5 | ⚙️ **Infrastructure / DevOps** | Infra & operations | Full | • Fully technical — infra focus (VMs, networking, Ansible, OS, cloud) |

## 📝 Drafts and errors

- **Drafts:** write proposed content to `~/_drafts/<domain>/YYYY-MM-DD_<topic>.md`
- **Errors:** write error details to `~/_errors/<domain>/YYYY-MM-DD_<topic>.md`
- **Reference:** write evergreen how-to guides and usage references to `~/.claude/_reference/<topic>.md` — no date prefix; topic-named in snake_case
- **File naming:** date-first for drafts/errors, snake_case topic-only for reference — e.g. `2026-08-04_onboarding_plan.md` or `claude_code_automation_commands.md`

| Domain | Use for |
|---|---|
| `1on1` | One-to-one meeting notes and prep |
| `confluence` | Confluence page drafts |
| `email` | Email drafts |
| `general` | Anything that doesn't fit a specific domain |
| `important` | High-priority items requiring attention |
| `jira` | Jira ticket drafts |
| `meetings` | Meeting notes and agendas |
| `plans` | Plans and proposals |
| `reference` | Reference material |
| `teams` | Microsoft Teams message drafts |

## 📚 Multifile Document Organization

@~/.claude/_rules/01_essentials/conventions/writing_style/_multifile_document_organization.md
