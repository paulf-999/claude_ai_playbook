# 💼 Business Value Tab

Standards for populating the Business Value tab (`customfield_10650`) on DM project Jira tickets — covering format, audience, scoring framework, and a worked example.

---

## Format

Every Business Value statement must follow this structure:

1. **Intro** — 1–2 sentences written for a non-technical business audience
2. **Bullet points** — up to 3 bullets covering risk, context, and scope
3. **Impact Rating block** — always present; see format below

---

## Audience guidance

The Business Value tab is read by external stakeholders and non-technical audiences.

- **Acceptable:** Named company-wide systems — e.g. "GitHub Enterprise migration", "Salesforce"
- **Not acceptable:** Internal tooling names — do not use Airflow, dbt, Docker, PAT, GHCR, or similar. Describe by function instead (e.g. "automated data pipelines", "the software that runs data transformations")

---

## Impact Rating block

Always append the following block after the intro and bullets:

```
Impact Rating (per Data Team Prioritization Framework):
* a. Prioritization Matrix: https://payroc.atlassian.net/wiki/x/k4DcRQE
* b. Priority Value Driver: <driver> – Score: <N>
* c. Secondary Value Driver: <driver> – Score: <N>
* d. Calculated Score: <value>
```

Fill in scores when the driver and rating are clear at creation time. Use `< TODO >` only when genuinely uncertain.

**Score calculation:** Only the top two drivers are scored.
`Calculated Score = (primary score × primary weight) + (secondary score × secondary weight)`

---

## Scoring frameworks

### Standard (6-category) — official Data Team framework

Use for all general work. Framework authored by Kevin Dolhay; reference: https://payroc.atlassian.net/wiki/x/k4DcRQE

| Category | Weight |
|---|---|
| Compliance & Risk | 25% |
| Transaction Integrity | 20% |
| Ops Efficiency | 15% |
| M&A Synergy | 15% |
| Exit Readiness | 15% |
| Customer Value | 10% |

**Scoring rubric:**
- [5] Critical / Immediate — regulatory fine imminent, transaction bug dropping >1% of volume, Due Diligence failure risk
- [3] Strategic / Important — schema mapping, automating 10+ hrs/week of manual work, new merchant data insight
- [1] Maintenance / Low Impact — minor tweaks, nice-to-have metadata, R&D with no clear ROI path

### Data Platform manager working convention (7-category)

Use when the ticket is primarily about **platform reliability or operational continuity** — e.g. dependency migrations before deprecation, preventing production outages, technical debt that creates operational risk.

The 6-category framework has no dedicated driver for this class of work; the closest proxies (Ops Efficiency, Compliance & Risk) do not cleanly cover infrastructure continuity work.

| Category | Weight |
|---|---|
| Compliance & Risk | 25% |
| Transaction Integrity | 20% |
| **Platform Reliability & Technical Risk** | **15%** |
| Ops Efficiency | 15% |
| M&A Synergy | 10% |
| Exit Readiness | 10% |
| Customer Value | 5% |

**Scoring rubric for Platform Reliability & Technical Risk:**
- [5] = imminent production outage or SLA breach if not addressed
- [3] = critical dependency reaching end-of-life within the quarter
- [1] = technical debt reduction with no near-term operational risk

---

## Worked example

**DM-38936 — Airflow: Git Migration Impact - Discovery - Cloudsmith Docker Image Integration**
*(Platform reliability ticket — 7-category framework applies)*

```
A mandatory company-wide system change (GitHub Enterprise migration) will prevent the
data platform from running its automated processes unless addressed before the deadline.

- All data reports and dashboards will stop receiving updates
- Non-negotiable timeline — driven by a migration outside the team's control
- Scope: identify the solution now; implementation follows as a separate piece of work

Impact Rating (per Data Team Prioritization Framework):
* a. Prioritization Matrix: https://payroc.atlassian.net/wiki/x/k4DcRQE
* b. Priority Value Driver: Platform Reliability & Technical Risk – Score: 5
* c. Secondary Value Driver: Transaction Integrity – Score: 4
* d. Calculated Score: 1.55
```

*Score calculation: 5 × 0.15 + 4 × 0.20 = 0.75 + 0.80 = 1.55*
