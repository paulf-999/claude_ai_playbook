# 📊 Scoring Guides — Master Index

Unified scoring framework for evaluating quality across Claude artifacts. Each artifact type has a dedicated scoring guide with dimensions tailored to its purpose.

---

## 🎯 Quick Reference — Dimensions by Artifact Type

### Skills (6 dimensions)
| # | Dimension | Focus |
|---|---|---|
| 1️⃣ | **Complexity** | Code size, phases, dependencies, conceptual difficulty |
| 2️⃣ | **Test Coverage** | Test count, breadth, and depth of test suite |
| 3️⃣ | **Code Quality** | Maintainability, clarity, error handling, code organization |
| 4️⃣ | **Security** | Input validation, secret handling, permission guardrails |
| 5️⃣ | **Documentation** | SKILL.md clarity, examples, known gaps, runbook quality |
| 6️⃣ | **Standards Compliance** | Naming, file structure, style guide adherence |

**Weighting:** Standards 20%, Test Coverage 20%, Code Quality 20%, Documentation 15%, Complexity 10%, Security 15%

**Full guide:** [`scoring_guides/SCORING_GUIDE_SKILLS.md`](scoring_guides/SCORING_GUIDE_SKILLS.md)

---

### Reference Files (5 dimensions)
| # | Dimension | Focus |
|---|---|---|
| 1️⃣ | **Coverage** | Topic focus, content completeness, gaps documented |
| 2️⃣ | **Clarity** | Writing quality, jargon, readability, comprehension |
| 3️⃣ | **Accuracy** | Up-to-date, links valid, aligned with current practice |
| 4️⃣ | **Documentation** | Examples, prerequisites, gaps, related references |
| 5️⃣ | **Presentation** | Organization, hierarchy, formatting, style compliance |

**Weighting:** Presentation 25%, Clarity/Documentation 20% each, Coverage/Accuracy 15% each

**Full guide:** [`scoring_guides/SCORING_GUIDE_REFERENCE_FILES.md`](scoring_guides/SCORING_GUIDE_REFERENCE_FILES.md)

---

### Rules (6 dimensions)
| # | Dimension | Focus |
|---|---|---|
| 1️⃣ | **Clarity** | Is the rule clearly written and understandable? |
| 2️⃣ | **Scope** | Is it focused on one concern/concept? |
| 3️⃣ | **Accuracy** | Is it correct and current? |
| 4️⃣ | **Enforceability** | Can it be checked/verified/audited? |
| 5️⃣ | **Integration** | Does it interact well with other rules without conflicts? |
| 6️⃣ | **Documentation** | Examples, rationale, when to apply? |

**Weighting:** Documentation 20%, Clarity/Enforceability 20% each, Accuracy/Integration 15% each, Scope 10%

**Full guide:** [`scoring_guides/SCORING_GUIDE_RULES.md`](scoring_guides/SCORING_GUIDE_RULES.md)

---

### Agents (6 dimensions)
| # | Dimension | Focus |
|---|---|---|
| 1️⃣ | **Purpose Clarity** | Is the agent's purpose and scope clearly defined? |
| 2️⃣ | **Capability** | Can it do what's intended? Breadth of tasks? |
| 3️⃣ | **Reliability** | Does it produce consistent, correct results? |
| 4️⃣ | **Integration** | Works well with main loop and other agents? |
| 5️⃣ | **Documentation** | Clear instructions, examples, edge cases, failure modes? |
| 6️⃣ | **Efficiency** | Appropriate tool selection, reasoning depth, token cost? |

**Weighting:** Reliability 20%, Documentation 20%, Capability 15%, Integration 15%, Purpose Clarity 15%, Efficiency 15%

**Full guide:** [`scoring_guides/SCORING_GUIDE_AGENTS.md`](scoring_guides/SCORING_GUIDE_AGENTS.md)

---

## 📖 How to Use

1. **Identify artifact type** — Is it a skill, reference file, rule, or agent?
2. **Read the guide** — Open the corresponding guide in `scoring_guides/`
3. **Score each dimension** — 1–10 scale per dimension
4. **Calculate overall** — Use the weighting formula from the guide
5. **Document rationale** — Explain scores near extremes (1–2, 9–10)

---

## 🔗 Related Files

- **Audits:** `audit_reference_files.md`, `audit_rules.md` (TBD), `audit_agents.md` (TBD)
- **README:** `README.md` — Audit overview and methodology

---

Last updated: **2026-08-19**
