---
date_created: "2026-10-17"
date_updated: "2026-11-03"
status: active
---

# Pattern — platform_risk_assessment

Creates a **Platform Risk & Maturity Assessment** page for one platform tool or component. Use this file in place of Phase 2 of `_implementation.md`, then continue to the **Local Draft Review** phase there.

Act as an objective platform assessor: rate maturity from evidence, identify operational exposure, flag risks and gaps, and prioritise findings by impact.

Apply these maturity definitions consistently throughout, always as full words — never `L`/`M`/`H`:

- **High** — Automated, monitored, documented, resilient, low operational exposure.
- **Medium** — Stable but partially manual; some visibility or resilience gaps; manageable risk.
- **Low** — Manual, undocumented, unsupported, or operationally exposed.

> ⚠️ **Wide view** cannot be set via the API. After the draft is created, open it in Confluence and toggle **Page width → Wide** in the editor toolbar.

---

## 🔍 Step 1 — Gather context

Ask the user the following in a single message:

1. Which platform tool or component is being assessed?
2. Who is the page creator?
3. Which Confluence space and parent page should the page go under?
4. Where does the tool's existing documentation live (Confluence pages, repos, drafts)?

Default the page status to **In review**, the date to today, and the purpose to: "The purpose of this page is to provide a structured assessment of the risk and maturity of the platform component for the specified tool." Confirm these rather than asking.

**Pre-fill from evidence:** read the existing Confluence pages first, then repos and drafts, and propose a 1–2 sentence current state for each theme below. Cite a page or file for every claim, and use `<TODO>` where there's no evidence — never guess.

- 🏗️ **Build**
  - **Code quality and documentation** — Is the code or configuration reviewed and tested, and is there up-to-date technical documentation or architecture diagrams?
  - **Deployment mechanism** — How is the tool deployed — manually, scripted, or IaC?
  - **Environments** — How many environments exist (dev/UAT/prod)? Are they isolated?
  - **Versioning and updates** — What version is running, and how are upgrades managed?
- ⚙️ **Run**
  - **Monitoring and alerting** — What monitoring exists? How are failures surfaced?
  - **Resilience and disaster recovery** — Is there a backup and restore process? Has it been tested?
  - **Integrations and connectivity** — What external systems does it connect to or depend on at runtime?
- 🧭 **Govern** — operational governance
  - **Change and incident management** — How are changes approved and incidents handled?
  - **Runbooks and procedures** — Are there runbooks for routine and failure scenarios?
  - **Key person dependencies** — Does running or fixing the tool depend on one or two people? Describe the pattern, never a name.

Present the pre-filled answers and wait for the user's corrections before proceeding.

---

## 📐 Step 2 — Rate and summarise

Rate each theme Low, Medium or High against the definitions above, then rate each group (Build, Run, Govern) and the platform overall. Flag any uncertain rating and explain why.

Draft a two-bullet summary (a verdict and a direction) and the top 2–4 issues or recommendations across all themes.

Present the ratings and summary to the user for confirmation.

---

## 🤔 Step 3 — Clarify and confirm

Flag any theme still at `<TODO>`, or where the rating is uncertain. Confirm the overall maturity level and summary with the user.

Wait for confirmation, then go to the **Local Draft Review** phase in `_implementation.md`.

**Cell writing:** in the draft, write every Current State, Observations, Summary and Issues cell as `•` bullets, one per line — each an emoji, a bold keyword and colon, then one short sentence. Link every page, incident, ticket or vendor doc inline where it's mentioned.

---

## 🏗️ Step 4 — Create the Confluence page (after draft approval only)

Run this step only once the Local Draft Review phase has an approved draft. Ask: "Should the page title be prefixed with `WIP - `? (default: yes)"

The page title format is: `Platform Risk & Maturity Assessment: <tool name>`.

Create the page as a **draft** using `createConfluencePage` with `contentFormat: adf` and `status: draft`, in the space and under the parent page the user confirmed in Step 1 — never infer either.

### ADF structure

Include the following nodes in the `content` array, in order:

**Header** — read `reference/common/_common_header.md` and include those nodes first.

**Body sections** — after the header, add these sections, each followed by a `rule` divider:

| Section | Heading | Content type |
|---|---|---|
| Maturity Status Summary | `🔎 1. Maturity Status Summary` | `table` — two columns (bold label \| value); rows: Date of Assessment, Overall Maturity Level, 3.1 Build, 3.2 Run, 3.3 Govern, Summary, Issues & Recommendations. Each group row's label has a second, italic paragraph saying what the group covers |
| Maturity Definitions | `📖 2. Maturity Definitions` | `bulletList` — three items: High (green badge), Medium (yellow badge), Low (red badge), each with its definition above |
| Detailed Maturity Assessment | `📋 3. Detailed Maturity Assessment` | Three level-2 sub-headings — `🏗️ 3.1 Build`, `⚙️ 3.2 Run`, `🧭 3.3 Govern` — each followed by a `table` with columns: Theme \| Current State \| Maturity (Low/Medium/High) \| Key Observations / Comments; one row per theme in Step 1 |
| Related Pages | `🔗 4. Related Pages` | `bulletList` — up to 5 key source pages, each an emoji, a bold keyword and colon, then the linked page title |

In table cells, put each `•` bullet in its own `paragraph` node, and render inline links as `link` marks.

Render each maturity rating as an inline `status` badge in its table cell (and for Overall Maturity Level and each group row):
- High → `color: "green"`, text: `"High"`
- Medium → `color: "yellow"`, text: `"Medium"`
- Low → `color: "red"`, text: `"Low"`

Use the ADF conventions in `_common_header.md` throughout. Return the draft URL.

**Critical constraints:** the Phase 2 constraints in `_implementation.md` apply here too — no publish before draft approval, no space root, no inferred space, no personal names.
