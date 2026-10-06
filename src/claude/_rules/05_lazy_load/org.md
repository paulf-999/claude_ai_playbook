<!-- version: 1.1.0 -->
<!-- created: 2026-10-01 -->
<!-- updated: 2026-10-06 -->
<!-- miss_cost: medium — resources named or wired up against the wrong organisation conventions -->
<!-- loading: lazy — only applies to organisation-specific work, so a pointer loads it when naming or wiring resources -->
# 🏢 Organisation Standards (Index)

**Purpose:** Index the standards that apply only inside your organisation — naming, secrets and estate-specific deployment rules — kept apart from the general style guides, plus the Jira values the generic Jira guide refers to.

---

## 📋 Child pages

Add one row per organisation-specific rule, stored under `org/`.

| File | Purpose | When to load |
|------|---------|-------------|
| `org/<rule>.md` | What the rule covers | When Claude should read it |

---

## 🧭 Organisation facts

- **Jira and Confluence site:** `https://<your-site>.atlassian.net`
- **GitHub org:** `<your-org>`

---

## 🎫 Jira values

The organisation-specific values the generic Jira style guide (`style_guide_standards/jira.md`) refers to. Replace each `<placeholder>` with your own value, and leave a row as-is when it doesn't apply.

### 🗂️ Project and board

| Setting | Value |
|---|---|
| Project key | `<PROJ>` |
| Board ID | `<board-id>` |
| Claude-created label | `<team>-claude-created` |
| Summary area | `<Area>`, e.g. your team name |

### 🔧 Custom field IDs

| Field | Jira ID | Type |
|---|---|---|
| Story points | `customfield_<n>` | Number |
| Sprint | `customfield_<n>` | Integer sprint ID |
| Business value | `customfield_<n>` | ADF document |

### 🔢 Sprint IDs

| Sprint | ID |
|---|---|
| `<sprint number>` | `<sprint ID>` |

### 📦 Components

| Component | ID | When to use |
|---|---|---|
| `<year-level component>` | `<id>` | Every ticket, if your project uses one |
| `<quarter component>` | `<id>` | The quarter of the ticket's sprint |

### 💼 Business value scoring

- **Framework name:** `<your prioritisation framework>`
- **Prioritisation matrix:** `<link to your team's prioritisation matrix>`

| Category | Weight |
|---|---|
| `<category>` | `<weight %>` |

---

## 🔗 Internal references

- Links to your organisation's own pages, such as secrets or naming standards.
