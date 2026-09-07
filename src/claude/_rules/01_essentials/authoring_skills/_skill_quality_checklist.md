# ✅ Quality Checklist (Author & Reviewer)

**Purpose:** Define checkpoints for skill creation to ensure quality gates are met.

---

## 📊 Quality Scorecard Dimensions

Every skill includes a quality scorecard (reference/_quality_scorecard.md) scoring 7 dimensions on 1–10 scale. Dimensions are:

| Dimension | What it measures | Scoring notes |
|-----------|------------------|---------------|
| **Design** | Scope clarity, boundaries (not_for), feature focus | 10 = crisp scope, explicit limits; 1 = feature creep, no boundaries |
| **Complexity** | Concept count, dependencies, edge cases | 10 = simple (1–2 concepts); 1 = tangled (5+ concepts) |
| **Test Coverage** | Evals aligned with maturity level | 10 = all phases covered; 1 = happy paths only |
| **Code Quality** | Clarity, error handling, maintainability | 10 = defensive, well-structured; 1 = brittle, ad-hoc |
| **Security** | Secret handling, input validation, permissions | 10 = least privilege, validated inputs; 1 = credentials hardcoded |
| **Documentation** | Clarity, completeness, known gaps | 10 = ultra-clear + roadmap; 1 = vague or missing |
| **Standards** | Naming, structure, style adherence | 10 = full compliance; 1 = violations |

**Scorecard dimensions are scored *against evals.yaml*, not independently.** If evals don't cover a dimension, the scorecard reflects that gap.

---

## 🏗️ Authoring Checklist

### Hard Gates (Block if violated)

- [ ] **Contract complete BEFORE SKILL.md** — never write SKILL.md without contract finalization
  - [ ] name, version, summary, maturity all defined
  - [ ] dispatch.triggers documented
  - [ ] dispatch.not_for documented (MOST IMPORTANT; scope boundaries)
  - [ ] output (type, confirmation_required, reversible, returns) declared
- [ ] **Naming:** `<domain>_<action>` format, valid domain, directory matches
- [ ] **Complexity score ≤ maturity limit** (draft ≤4, tactical ≤6, strategic ≤8)
- [ ] **SKILL.md structure:** 5 sections only + emoji headers + ≤60 lines
  - [ ] Frontmatter, Purpose, Example Usage, Best For, References
  - [ ] No detail sections (Security, Prerequisites, Workflow, Error Recovery, Known Gaps)
- [ ] **evals.yaml [REQUIRED]:** Test count matches maturity
  - [ ] Draft 5–8 evals | Tactical 8–12 evals | Strategic 12+ evals
  - [ ] Each eval: name, description, input, setup, expected_output
  - [ ] Organized by phase/feature
- [ ] **Quality scorecard [REQUIRED]:** reference/_quality_scorecard.md
  - [ ] All 7 dimensions scored (Design, Complexity, Test Coverage, Code Quality, Security, Documentation, Standards)
  - [ ] Maturity level justified with evidence
  - [ ] Design rationale explained
- [ ] **Reference files [REQUIRED]:**
  - [ ] reference/_quality_scorecard.md exists
  - [ ] reference/_implementation.md exists (phases, logic, error handling)
  - [ ] reference/_formats.md [IF APPLICABLE] (standards, validation, examples)

### Evals Drive Quality Scoring

**Do not score quality dimensions independently.** Instead:

1. Write evals.yaml first — 10–15 scenarios covering happy paths, errors, edge cases
2. Score complexity based on *how many concepts evals must validate* (not how many classes you wrote)
3. Score test coverage by *what evals demonstrate* — if evals don't cover a dimension, scorecard reflects that
4. Score code quality by *robustness observed in evals* — does the skill recover from errors documented in evals?

**Anti-pattern:** Writing code, then creating evals to match. Leads to false confidence (evals test code, not requirements).

**Correct pattern:** Define evals (requirements), write code to pass them, score quality *against evals*.

---

### Quality Checks (Request changes; negotiable)

- [ ] **Opening is clear:** Explains purpose in <60 seconds
- [ ] **Bold keywords:** All bullets use bold keywords (`**Why:**`, `**Note:**`, `**Example:**`)
- [ ] **No TODO/FIXME:** Draft only; tactical+ must resolve
- [ ] **No hardcoded paths:** No coupling to personal directories or usernames
- [ ] **File under 60 lines:** SKILL.md stays scannable; excess detail belongs in reference/

---

## 🔍 Reviewer Checklist

### Hard Gates

- [ ] **Naming compliance:** Valid domain, matches directory
- [ ] **Complexity valid:** Score ≤ maturity limit; no scope creep
- [ ] **Contract complete:** All required YAML fields present and valid
- [ ] **Structure correct:** All 8 sections in canonical order
- [ ] **Emoji headers:** Every `##` section has emoji prefix
- [ ] **Tests exist:** Count matches maturity level

### Advisory (Request changes; seek author's perspective)

- [ ] **Writing clarity:** Opening is understandable; no jargon
- [ ] **Scope focused:** Solves one problem; no bundled unrelated concerns
- [ ] **Prerequisites realistic:** Author has assumed user background correctly
- [ ] **Integration:** Doesn't duplicate or conflict with existing skills
- [ ] **Error handling:** Error Recovery section covers common failure modes
