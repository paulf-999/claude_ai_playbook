<!-- version: 2.0.0 -->
<!-- created: 2026-06-07 -->
<!-- updated: 2026-10-06 -->
# 💼 Business Value Tab

Standards for populating the Business Value tab on Jira tickets — covering format, audience, scoring framework, and a worked example. The field ID, framework name, matrix link and weights live in the Jira values in `~/.claude/_rules/05_lazy_load/org.md`.

## 📋 Contents

- [Format](#-format)
- [Audience guidance](#-audience-guidance)
- [Impact Rating block](#-impact-rating-block)
- [Scoring frameworks](#-scoring-frameworks)
- [Worked example](#-worked-example)

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
Impact Rating (per <your prioritisation framework>):
* a. Prioritization Matrix: <link to your team's prioritisation matrix>
* b. Priority Value Driver: <driver> – Score: <N>
* c. Secondary Value Driver: <driver> – Score: <N>
* d. Calculated Score: <value>
```

Fill in scores when the driver and rating are clear at creation time. Use `< TODO >` only when genuinely uncertain.

**Score calculation:** Only the top two drivers are scored.
`Calculated Score = (primary score × primary weight) + (secondary score × secondary weight)`

---

## Scoring frameworks

Use your organisation's framework, with the categories and weights listed in `org.md`.

- **Second framework:** if your team weights some work differently (for example platform reliability or operational continuity), list that framework in `org.md` too, and say when it applies.
- **No framework yet:** leave the Impact Rating scores as `< TODO >` rather than inventing categories or weights.

**Scoring rubric:**
- [5] Critical / Immediate — imminent regulatory, financial or customer impact, or a production outage if not addressed
- [3] Strategic / Important — removes significant recurring manual work, or unlocks a new insight or capability
- [1] Maintenance / Low Impact — minor tweaks, nice-to-have metadata, R&D with no clear ROI path

---

## Worked example

See: `~/.claude/_rules/05_lazy_load/style_guide_standards/jira/templates/template_business_value_example.txt`
