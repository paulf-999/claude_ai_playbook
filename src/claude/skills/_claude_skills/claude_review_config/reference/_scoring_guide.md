# Scoring Guide — Six Dimensions

## Scoring Scale

| Score | Meaning |
|---|---|
| 9–10 | Excellent — Exemplary in all aspects |
| 7–8 | Good — Meets bar with minor gaps |
| 5–6 | Acceptable — Has notable gaps |
| 1–4 | Needs work — Significant issues |

---

## Dimensions at a Glance

| Dimension | What to assess | 9–10 | 7–8 | 5–6 | 1–4 |
|---|---|---|---|---|---|
| **Rule Quality** | Clarity, specificity, actionability, DRY | Clear, specific, zero duplication | Good clarity, minor duplication | Some clarity, mixed actionability | Vague, unclear, heavy duplication |
| **Config Complexity** | Import chain depth, file sizes, indirection | Shallow chains, all <100 lines, no indirection | Mostly shallow, <10% >100 lines | Some deep chains, some >100 lines | Deep chains, many >100 lines |
| **Testing** | Hook tests, rule structure tests, coverage | All hooks tested, high coverage | Most hooks tested, good coverage | Some hooks tested, partial coverage | Few hooks tested, low coverage |
| **Security** | Separation, injection defence, secrets, perms | Clear separation, explicit defence, safe secrets, scoped perms | Good separation, some defence, mostly safe | Partial separation, basic defence, some hardcoding | Mixed concerns, no defence, exposed secrets |
| **Documentation** | READMEs, MEMORY.md, rationale, WIP notes | Comprehensive READMEs, curated memory | Most READMEs, curated memory, good rationale | Some READMEs, partial curation, some rationale | Few READMEs, stale memory, missing rationale |
| **Standards Adherence** | Naming, line limits, imports, emoji/bold style | Consistent naming, all <100 lines, clean imports, uniform style | Good naming, mostly <100 lines, mostly clean | Naming inconsistent, some >100 lines, some duplication | Naming inconsistent, many >100 lines, duplicated |

---

## Grade Mapping

**Overall:** Average of six dimension scores, rounded to one decimal place.

| Score | Grade | Score | Grade |
|---|---|---|---|
| 9.5–10.0 | A+ | 6.5–6.9 | C+ |
| 9.0–9.4 | A | 6.0–6.4 | C |
| 8.5–8.9 | A− | 5.5–5.9 | C− |
| 8.0–8.4 | B+ | 5.0–5.4 | D+ |
| 7.5–7.9 | B | 4.0–4.9 | D |
| 7.0–7.4 | B− | <4.0 | F |
