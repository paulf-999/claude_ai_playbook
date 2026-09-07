# 🔎 Skill Review Framework

**Purpose:** Define the multi-layer review process that skills go through before and after creation.

---

## 3-Layer Review Process

### Layer 1️⃣: Automated Validation (Pre-commit)

**What it checks:**
- ✅ SKILL.md structure (all 8 sections present)
- ✅ Emoji headers on all `##` sections
- ✅ Skill naming format (`<domain>_<action>`)
- ✅ Complexity scoring valid (0–10, matches maturity)
- ✅ Test count matches maturity level

**Feedback:** Immediate; tells you exactly what failed. Blocks commit if violations found.

**Tool:** Pre-commit hook + naming scorer

---

### Layer 2️⃣: Claude Auto-Review (During Development)

**What it checks (4 dimensions):**
1. **Testing** — Test coverage, test organization, test quality
2. **Security** — Secret handling, permission guardrails, input validation
3. **Documentation** — Clarity, examples, completeness, known gaps
4. **Standards** — Naming conventions, file structure, style guide adherence

**Scoring:** Each dimension rated 1–10; overall grade from A–F (9+ = A, 8 = B, 7 = C, 6 = D, <6 = F).

**Feedback:** Dimension scores with reasoning and improvement suggestions.

**Invocation:** `/review_skill <path>` during development

---

### Layer 3️⃣: Human Code Review (PR Review)

**What it checks:**
- **Design:** Solves one focused problem? Clear scope?
- **Clarity:** Writing is professional? Concepts explained?
- **Completeness:** All prerequisites listed? Known gaps documented?
- **Test depth:** Tests validate behavior, not just "code runs"?
- **Integration:** Works well with other skills? No duplication?

**Feedback:** Judgment calls, design feedback, suggestions for improvement.

**Tool:** Use reviewer checklist from `_skill_quality_checklist.md`

---

## When to Use Each Layer

| Scenario | Use Layer |
|---|---|
| During skill development | 2️⃣ Claude auto-review (`/review_skill`) |
| Before git commit | 1️⃣ Automated validation (pre-commit) |
| During PR code review | 3️⃣ Human review (checklist) |
| Quick sanity check | 1️⃣ + 2️⃣ (automated + Claude) |
| Final verification | All 3 layers |
