# Design Rationale — confluence_create_page

Why we chose the Phase 1a/1b/2/3 architecture instead of alternatives.

---

## Design Decision: Four-Phase Workflow

**Chosen approach:**
- Phase 1a: Context detection + outline collection
- Phase 1b: Title proposal (3 interactive choices)
- Phase 2: Draft generation with auto-filled metadata
- Phase 3: Local review + publish

**Alternatives considered:**

| Alternative | Pros | Cons | Why Rejected |
|---|---|---|---|
| **Gather-all-upfront** (original) | One question phase; simpler code | Cognitive overload; title guessed first; auto-fills hidden | Violates progressive disclosure |
| **Title proposal first** | Early clarity on page intent | Commits user to intent before seeing structure | Premature; needs outline first |
| **Skip draft review** | Fewer steps; less friction | Mistakes publish directly; no recovery | Too risky for team use |
| **Chosen: Phase 1a/1b/2/3** | Progressive disclosure; context-aware; draft-first; clear separation | Slightly more code; more interactions | ✅ Best UX + safety |

---

## Design Decision: Dynamic User Resolution

**Chosen approach:**
- Resolve `user.name` from git config → FULLNAME env → whoami
- Resolve email from git config → EMAIL env → constructed fallback
- Graceful degradation on each failure

**Alternatives considered:**

| Alternative | Pros | Cons | Why Rejected |
|---|---|---|---|
| **Hardcoded creator** (original) | Simple; no dependencies | Only works for Paul Fry; breaks for team | Not team-safe |
| **Require explicit entry** | Always accurate; no assumptions | Friction; every user has to remember email | Blocks workflow |
| **System user only** | Works everywhere | Usernames often not readable (paulfrya); not professional | Bad UX |
| **Chosen: dynamic resolution** | Team-safe; uses readable git name; email auto-correct; fallbacks | Slightly more subprocess overhead | ✅ Balances simplicity + robustness |

---

## Design Decision: Title Proposal (3 Candidates)

**Chosen approach:**
- Generate 3 distinct title styles from outline keywords
- Let user select from list or provide custom

**Alternatives considered:**

| Alternative | Pros | Cons | Why Rejected |
|---|---|---|---|
| **User types title** | Always exactly what they want | Open-ended; slower; hesitation | Cognitive friction |
| **Auto-generate one title** | Fast; no choice overhead | Often misses intent; no alternatives | Too rigid |
| **Chosen: 3 candidates** | Anchors decision; gives options; fallback to custom | Keywords-only (not semantic) | ✅ Best UX for outline-first approach |
| **LLM-based titles (Phase 2)** | Semantic understanding; better quality | Adds latency; requires API call | Defer to v2.0 |

---

## Design Decision: Auto-Filled Metadata

**Chosen approach:**
- Creator: dynamically resolved from user config
- Version: hardcoded "1.0" (all new pages)
- Date: auto-generated from today
- Status: auto-set to "🟡 In progress" (for review)

**Alternatives considered:**

| Alternative | Pros | Cons | Why Rejected |
|---|---|---|---|
| **Prompt for all metadata** | Complete control; no assumptions | Friction; 4 extra prompts | Too interactive |
| **Hide auto-fills entirely** | Cleaner UX; auto-magic | Changes invisible until publish; surprises | Violates transparency |
| **Chosen: auto-fill + show** | Fast; visible for review; editable in Phase 3 | Can't override version/date (v1.0) | ✅ Balances automation + control |

---

## Design Decision: Draft Review (Mandatory)

**Chosen approach:**
- Always generate local draft before publishing
- User must explicitly approve before Confluence publish
- Can't bypass with flags or automation

**Alternatives considered:**

| Alternative | Pros | Cons | Why Rejected |
|---|---|---|---|
| **Skip draft review** | Faster; fewer steps | No recovery from mistakes; publish surprises | Too risky |
| **Optional draft review** | User chooses friction level | Inconsistent safety; some users skip | Unreliable |
| **Chosen: always mandatory** | Prevents bad publishes; clear safety gate; recovery option | Adds one step | ✅ Enterprise-safe default |

---

## Trade-offs Made

### Complexity vs. UX
- **Choice:** More phases (1a/1b/2/3) over fewer (1/2/3)
- **Rationale:** Progressive disclosure beats one-shot bulk collection
- **Cost:** ~4 extra code functions; test coverage needed

### Simplicity vs. Team-Safety
- **Choice:** Dynamic user resolution over hardcoded
- **Rationale:** Single-user tools break at team scale
- **Cost:** subprocess calls + fallback chains + testing

### Speed vs. Quality
- **Choice:** Mandatory draft review + local save
- **Rationale:** Prevents publishing mistakes
- **Cost:** One extra step per page creation

### Semantics vs. Speed
- **Choice:** Keyword-based title generation now, LLM v2.0
- **Rationale:** v1.0 ships fast; Phase 2 adds semantic richness
- **Cost:** Generic titles; workaround = custom title entry

---

## Why Not...?

**Why not merge Phase 1a/1b?**
- Context detection and title proposal are independent concerns
- Separating them allows skipping Phase 1b if title is already explicit (via `--title`)
- Clear module boundaries aid testing and maintenance

**Why not auto-publish after draft approval?**
- Publishing is risky; explicit confirmation is safety gate
- Users may want to edit draft after review but before publish
- Automation should never surprise; confirmation ensures intent

**Why not use LLM for titles in v1.0?**
- Adds latency and external dependency (Claude API)
- Keyword-based approach is fast, local, and good-enough for MVP
- Phase 2 can add semantic titles without breaking v1.0

**Why not support page editing (as well as creation)?**
- Editing is distinct workflow with different UX (fetch → modify → publish)
- Scope creep risk; separate skill (`confluence_update_page`) is cleaner
- Phase 2 roadmap includes this as separate skill

---

## Future Enhancements (Phase 2+)

- **LLM-based titles** — Use Claude API to generate semantically intelligent titles
- **Page editing** — Support updating existing pages (`confluence_update_page` skill)
- **Template selection** — More patterns (requirements, incident_report, design_decision)
- **Batch creation** — Create multiple pages from outline (via CSV or JSON)
- **Schedule publishing** — Defer publish to specific time (useful for announcements)
- **Collaboration** — Invite reviewers to draft before publish
