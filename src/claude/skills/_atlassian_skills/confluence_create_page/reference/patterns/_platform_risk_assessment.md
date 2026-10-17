---
date_created: "2026-10-17"
date_updated: "2026-10-17"
status: active
---

# Pattern — platform_risk_assessment

Creates a **Platform Risk & Maturity Assessment** page for one platform tool or component. Use this file in place of Phase 2 of `_phases.md`, then continue to the **Local Draft Review** phase there.

Act as an objective platform assessor: rate maturity from evidence, identify operational exposure, flag risks and gaps, and prioritise findings by impact.

Apply these maturity definitions consistently throughout:

- **High** — Automated, monitored, documented, resilient, low operational exposure.
- **Medium** — Stable but partially manual; some visibility or resilience gaps; manageable risk.
- **Low** — Manual, undocumented, unsupported, or operationally exposed.

> ⚠️ **Wide view** cannot be set via the API. After the draft is created, open it in Confluence and toggle **Page width → Wide** in the editor toolbar.

---

## 🔍 Step 1 — Gather context

Ask the user the following in a single message:

1. Which platform tool or component is being assessed?
2. Who is the page creator?
3. What is the page status? (Not started / In progress / Ready for review / Complete)
4. What is the purpose of this page — complete the sentence: "The purpose of this page is to…" If the user is unsure, offer to draft it from the tool name.
5. Who is conducting the assessment (role, not a personal name), and on what date?
6. Which Confluence space and parent page should the page go under?
7. For each theme below, describe the current state in 1–2 sentences:
   - **Environments** — How many environments exist (dev/UAT/prod)? Are they isolated?
   - **Deployment** — How is the tool deployed and updated — manually, scripted, or IaC?
   - **Versioning & Updates** — What version is running, and how are upgrades managed?
   - **Connectivity / Dependencies** — What external systems does it connect to or depend on at runtime?
   - **Monitoring & Alerting** — What monitoring exists? How are failures surfaced?
   - **Resilience / DR** — Is there a backup and restore process? Has it been tested?
   - **Operational Governance** _(optional)_ — Change management, runbooks, quality controls, key person dependencies?
   - **Documentation** _(optional)_ — Is there up-to-date technical documentation or architecture diagrams?

Wait for the user's responses before proceeding.

---

## 📐 Step 2 — Rate and summarise

For each theme, apply the maturity definitions above to assign a rating (L/M/H) from the user's descriptions. Flag any uncertain rating and explain why.

Identify the top 2–4 issues or recommendations across all themes, and draft a 3–6 line executive summary for the Maturity Status Summary table.

Present the ratings and summary to the user for confirmation.

---

## 🤔 Step 3 — Clarify and confirm

Flag any theme with no description, or where the rating is uncertain. Confirm the overall maturity level and executive summary with the user.

Wait for confirmation, then go to the **Local Draft Review** phase in `_phases.md`.

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
| Maturity Status Summary | `🔎 1. Maturity Status Summary` | `table` — two columns (bold label \| value); rows: Date of Assessment, Assessed By, Overall Maturity Level, Issues & Recommendations |
| Maturity Definitions | `📖 2. Maturity Definitions` | `bulletList` — three items: High (green badge), Medium (yellow badge), Low (red badge), each with its definition above |
| Detailed Maturity Assessment | `📋 3. Detailed Maturity Assessment` | `table` — columns: Theme \| Sub-Theme \| Current State \| Maturity (L/M/H) \| Key Observations / Comments; one row per row below |

**Detailed Maturity Assessment rows** (Theme → Sub-Theme):

| Theme | Sub-Theme |
|---|---|
| Environments | — |
| Deployment | Deployment model (manual / automated / IaC) |
| Versioning & Updates | Tool version & upgrade approach |
| Connectivity / Dependencies | External integrations & runtime dependencies |
| Monitoring & Alerting | — |
| Resilience / DR | Backup & restore approach |
| Operational Governance | Change & incident management |
| Operational Governance | Quality controls |
| Operational Governance | Runbooks / procedures |
| Operational Governance | Key person dependency |
| Documentation | Technical documentation & diagrams |

Mark anything unknown or unconfirmed as `<TODO>`.

Render each maturity rating as an inline `status` badge in its table cell (and for Overall Maturity Level):
- H → `color: "green"`, text: `"H"`
- M → `color: "yellow"`, text: `"M"`
- L → `color: "red"`, text: `"L"`

Use the ADF conventions in `_common_header.md` throughout. Return the draft URL.

**Critical constraints:** the Phase 2 constraints in `_phases.md` apply here too — no publish before draft approval, no space root, no inferred space, no personal names.
