# 📊 Scoring Guide — Skills

Scoring rubric for skills (executable workflows). Scores range 1–10 across six quality dimensions.

---

## 🎯 The 6 Dimensions

| # | Dimension | What it measures | Higher score = |
|---|---|---|---|
| **1️⃣** | **Complexity** | Code size, phases, dependencies, conceptual difficulty | Simpler, more focused |
| **2️⃣** | **Test Coverage** | Test count, breadth (happy path + edge cases), depth (unit + integration) | More thoroughly tested |
| **3️⃣** | **Code Quality** | Maintainability, clarity, error handling, code organization | Better structured code |
| **4️⃣** | **Security** | Input validation, secret handling, permission guardrails, threat model | More secure |
| **5️⃣** | **Documentation** | SKILL.md clarity, examples, known gaps, runbook completeness | Better documented |
| **6️⃣** | **Standards Compliance** | Naming conventions, file structure, style guide adherence | More standards-compliant |

**Weighting:** Standards 20%, Test Coverage 20%, Code Quality 20%, Documentation 15%, Complexity 10%, Security 15%

---

## 1️⃣ Complexity (1–10)

**Principle:** Higher score = lower (simpler) complexity. **Goal: minimize scope, do one thing well.**

Measures code size, architectural complexity, number of phases, and conceptual difficulty.

| Score | Complexity Level | Scope | Lines | Phases | Judgment |
|---|---|---|---|---|---|
| **9–10/10** | ✅ **LOW** (simple, excellent) | Single focused task | 50–100 | 2–3 | Skill does one thing well, minimal scope, excellent design |
| **7–8/10** | ✅ **MODERATE** (appropriately complex) | Moderately scoped | 100–200 | 3–4 | Appropriately complex, some feature set, justified complexity |
| **5–6/10** | ⚠️ **ELEVATED** (some over-engineering) | Multiple features | 200–400 | 4–5 | Moderately complex, some scope creep, acceptable with documentation |
| **3–4/10** | ⚠️ **SUBSTANTIAL** (legitimately complex) | Complex system | 400–700 | 6–9 | Legitimately complex (e.g., graph generation), must be justified by scope |
| **1–2/10** | ❌ **HIGH** (over-engineered, bad) | Over-scoped | 700+ | 10+ | Unnecessarily complicated, multiple unrelated features, should be refactored |

**How to assess:**
- Count lines in SKILL.md, phase files, and implementation files
- Count distinct phases in the workflow
- Assess whether the skill touches external systems (MCP, APIs) or performs complex computations
- Higher score = simpler design, better maintainability

---

## 2️⃣ Test Coverage (1–10)

Measures test count, breadth (happy path + edge cases), and depth (unit + integration).

| Score | Test Count | Coverage | Types | Example |
|---|---|---|---|---|
| 1–3 | 0–2 or placeholder tests | Happy path only | Unit only | `jira_create` — 1–2 draft tests, no error cases |
| 4–6 | 3–8 tests | Main path + light edge cases | Unit + basic integration | `confluence_create_page` — draft review flow + pattern selection |
| 7–8 | 8–15 tests | Main + error cases + state validation | Unit + integration | `admin_review_claude_config` — scoring logic, recommendation generation |
| 9–10 | 15+ tests | Comprehensive (all paths, edge cases, regression) | Unit + integration + E2E | Hypothetical: full compliance suite with edge case coverage |

**How to assess:**
- Count test files in `test_*.py` or `*_test.py` files adjacent to the skill
- Read test cases: do they cover happy path only, or error cases?
- Check for integration tests (tests that run the skill end-to-end)

---

## 3️⃣ Code Quality (1–10)

Measures maintainability, clarity, error handling, and code organization.

| Score | Clarity | Error Handling | Structure | Example |
|---|---|---|---|---|
| 1–4 | Hard to follow; unclear naming; inconsistent style | None or catch-all try/except | Monolithic, tangled dependencies | Happy-path only, no error recovery |
| 5–6 | Mostly clear; some naming gaps; minor style inconsistencies | Basic checks, limited graceful degradation | Mostly organized, some tight coupling | Main path clear; edge cases commented as "TODO" |
| 7–8 | Clear code; consistent naming; well-organized | Main-path error handling; graceful fallbacks | Modular, documented dependencies | Well-structured phases; error messages informative |
| 9–10 | Excellent clarity; descriptive naming; consistent style | Full coverage (main + error cases); recovery strategies | Modular, decoupled, testable | Production-grade defensive programming |

---

## 4️⃣ Security (1–10)

Measures input validation, secret handling, permission guardrails, and threat model awareness.

| Score | Input Validation | Secrets | Permissions | Threat Model |
|---|---|---|---|---|
| 1–4 | None or minimal | Hardcoded or passed unsafely | Overly broad | Not considered |
| 5–6 | Basic validation for required fields | Accessed via env/secrets manager | Least-privilege intended but not enforced | Partial (main attack vector identified) |
| 7–8 | Type/constraint validation; injection prevention | Accessed via secrets manager; never logged | Explicit permission checks | Clear (documented trust boundaries) |
| 9–10 | Full validation + sanitization; context-aware | Secrets never exposed; audit trail | Fine-grained, enforced at API layer | Comprehensive (threat model documented) |

---

## 5️⃣ Documentation (1–10)

Measures SKILL.md quality, examples, known gaps, and runbook completeness.

| Score | SKILL.md | Examples | Known Gaps | Runbook |
|---|---|---|---|---|
| 1–4 | Minimal or unclear | None or outdated | Not documented | None |
| 5–6 | Basic structure; some jargon | One example | Listed but brief | Partial (main path only) |
| 7–8 | Clear opening; prerequisites clear; most paths documented | Multiple examples | Clear with workarounds | Complete for main path; error handling noted |
| 9–10 | Excellent clarity; end-to-end flow; all edge cases | Rich examples with variations | Comprehensive; roadmap included | Full coverage incl. error recovery, troubleshooting |

---

## 6️⃣ Standards Compliance (1–10)

Measures adherence to naming conventions, file structure, and style guide.

| Score | Naming | Structure | Style Guide | Frontmatter |
|---|---|---|---|---|
| 1–4 | Unclear or inconsistent | Missing files; tangled | Not followed | Incomplete or missing |
| 5–6 | Mostly clear | Required files present; some optional missing | Partially followed | Basic fields present |
| 7–8 | Clear, consistent naming | All required files; optional ones organized | Mostly followed | Complete; follows format |
| 9–10 | Excellent clarity; self-documenting | Exemplary structure; well-organized | Fully followed | Complete + custom fields as needed |

---

## Overall Score Calculation

**Formula:** Weighted average across six dimensions

```
Overall = (
  Complexity              × 0.10 +
  Test Coverage           × 0.20 +
  Code Quality            × 0.20 +
  Security                × 0.15 +
  Documentation           × 0.15 +
  Standards Compliance    × 0.20
)
```

---

## How to Use This Guide

**During assessment:**
1. Read the skill's SKILL.md and code in full
2. For each dimension, identify the band that best describes the skill
3. Score should be defensible — cite specific examples
4. When unsure, err toward middle bands (5–6)

**Scoring expectations:**
- Most well-maintained skills score 7–8 overall
- Overly large skills (>400 lines) typically score 1–4 on Complexity
- Early-stage skills can score 5–6 even if complete (utility-specific)

**Maintaining scores:**
- Review annually or when major changes occur
- Update scores when gaps are fixed or new tests added
- Document in audit scorecard the rationale for scores near extremes (1–2, 9–10)

---

## Related Guidance

- Skill authoring: `~/.claude/_rules/skill_authoring.md`
- Testing: `~/.claude/_rules/testing.md`
- Security: `~/.claude/_rules/security.md`
