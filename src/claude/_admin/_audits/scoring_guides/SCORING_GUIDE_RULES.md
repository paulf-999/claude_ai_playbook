# 📊 Scoring Guide — Rules

Scoring rubric for behavior/guidance rules (how Claude should act). Scores range 1–10 across six quality dimensions.

---

## 🎯 The 6 Dimensions

| # | Dimension | What it measures | Higher score = |
|---|---|---|---|
| **1️⃣** | **Clarity** | Is the rule clearly written and understandable? | Easy to understand and follow |
| **2️⃣** | **Scope** | Is it focused on one concern/concept? | Focused and narrowly scoped |
| **3️⃣** | **Accuracy** | Is it correct and current? | Accurate and up-to-date |
| **4️⃣** | **Enforceability** | Can it be checked/verified/audited? | Objectively measurable |
| **5️⃣** | **Integration** | Does it interact well with other rules without conflicts? | Composable with existing rules |
| **6️⃣** | **Documentation** | Examples, rationale, when to apply? | Well-documented |

**Weighting:** Documentation 20%, Clarity 20%, Enforceability 20%, Accuracy 15%, Integration 15%, Scope 10%

---

## 1️⃣ Clarity (1–10)

**Principle:** Rules must be unambiguous and self-contained.

Measures writing clarity, jargon explanation, and actionability.

| Score | Writing | Jargon | Actionability | Example |
|---|---|---|---|---|
| 1–4 | Difficult to follow; ambiguous | Unexplained technical terms | Unclear what to do | "Behave well" |
| 5–6 | Mostly clear; some ambiguity | Some jargon explained | Mostly clear what to do | "Avoid risky actions; ask first" (unclear what counts as risky) |
| 7–8 | Clear, direct writing | Jargon explained or avoided | Clear what to do | "Before deleting files, ask the user first" |
| 9–10 | Excellent clarity; unambiguous | All jargon explained | Crystal clear actions | "Before running `rm -rf`, check with user and explain the impact" |

---

## 2️⃣ Scope (1–10)

**Principle:** One rule = one concept. Don't bundle unrelated concerns.

Measures conceptual focus and whether the rule could be split.

| Score | Focus | Concepts | Judgment |
|---|---|---|---|
| **9–10/10** | ✅ Laser-focused | Single, crystal-clear concept | Rule covers one concern exhaustively; no sprawl |
| **7–8/10** | ✅ Focused | One primary + minor related | Related concepts naturally bundled; clear hierarchy |
| **5–6/10** | ⚠️ Moderate | 2–3 related concepts | Could benefit from splitting; somewhat bundled |
| **3–4/10** | ⚠️ Broad | 3–4 distinct concepts | Should be split; topics loosely related |
| **1–2/10** | ❌ Unfocused | 5+ unrelated concepts | Bundle of unrelated rules; should be separated |

---

## 3️⃣ Accuracy (1–10)

**Principle:** Rules must be correct and current.

Measures correctness and alignment with actual practices/constraints.

| Score | Correctness | Currentness | Consistency | Example |
|---|---|---|---|---|
| 1–4 | Incorrect or misleading | >1 year stale; contradicts practice | Conflicts with other rules | "Always force push to main" |
| 5–6 | Mostly correct; edge cases wrong | 6–12 months old | Minor conflicts | "Commit messages should be lowercase" (conflicts with Conventional Commits) |
| 7–8 | Correct; spot-checked | 2–3 months old; verified | No conflicts | "Commit messages follow Conventional Commits format" |
| 9–10 | Authoritative; actively verified | Current; inline with practice | Fully consistent | "Commit messages follow Conventional Commits; use format `type(scope): description`" |

---

## 4️⃣ Enforceability (1–10)

**Principle:** Rules should be auditable and objectively measurable.

Measures whether the rule can be verified and checked.

| Score | Measurability | Verification | Audit | Example |
|---|---|---|---|---|
| 1–4 | Subjective; hard to verify | No clear way to check | Can't audit | "Write good code" |
| 5–6 | Mostly measurable; some subjectivity | Can be checked manually | Possible but tedious | "Code should be clear" |
| 7–8 | Mostly objective; clear criteria | Can be checked with tools/manual review | Easy to audit | "Commit messages must follow format `type(scope): description`" |
| 9–10 | Fully objective; testable | Automated check possible | Trivial to audit | "All `##` headers must have emoji prefix (linter-checked)" |

---

## 5️⃣ Integration (1–10)

**Principle:** Rules must compose well and not contradict each other.

Measures whether the rule conflicts with or enhances other rules.

| Score | Conflicts | Synergy | Composition | Example |
|---|---|---|---|---|
| 1–4 | Multiple conflicts with existing rules | Adds confusion | Can't combine with others | "Always use git stash" + "Never use git stash" |
| 5–6 | One or two conflicts | Some enhancement | Works but with friction | Rule applies to edge cases not covered elsewhere |
| 7–8 | No conflicts; natural composition | Enhances other rules | Works smoothly | Rule fills gap or strengthens related rule |
| 9–10 | No conflicts; strong synergy | Amplifies related rules | Perfect composition | Rule complements and strengthens related rules |

---

## 6️⃣ Documentation (1–10)

**Principle:** Rules need examples, rationale, and context.

Measures completeness of supporting material.

| Score | Rationale | Examples | When to Apply | Related Rules |
|---|---|---|---|---|
| 1–4 | Not explained | None or wrong | Not specified | Not linked |
| 5–6 | Brief rationale | One basic example | Vague guidance | One or two linked |
| 7–8 | Clear rationale; trade-offs noted | Multiple examples | Clear decision tree | Good cross-links |
| 9–10 | Detailed rationale; WHY is clear | Rich examples + anti-patterns | Precise applicability | Excellent cross-references |

**Documentation checklist:**
- **Why:** Why does this rule exist? What problem does it solve?
- **Example:** What does compliance look like?
- **When:** When should this rule apply?
- **Related:** What other rules does this interact with?

---

## Overall Score Calculation

**Formula:** Weighted average across six dimensions

```
Overall = (
  Clarity           × 0.20 +
  Scope             × 0.10 +
  Accuracy          × 0.15 +
  Enforceability    × 0.20 +
  Integration       × 0.15 +
  Documentation     × 0.20
)
```

---

## How to Use This Guide

**During assessment:**
1. Read the rule in full, including related rules it references
2. For each dimension, identify the band that best describes it
3. Score should be defensible — cite specific examples
4. When unsure, err toward middle bands (5–6)

**Scoring expectations:**
- Well-written rules score 7–8 overall
- Prescriptive rules (e.g., "always do X") are easier to score high on Enforceability
- Principle-based rules (e.g., "prefer simplicity") score lower on Enforceability but higher on Scope

**Maintaining scores:**
- Review when the rule is updated or conflicts emerge
- Re-score if related rules change
- Document rationale for scores near extremes (1–2, 9–10)

---

## Related Guidance

- Behavior rules: `~/.claude/_rules/behaviour.md`
- Security rules: `~/.claude/_rules/security.md`
- Writing style: `~/.claude/_rules/writing_style.md`
- Guiding principles: `~/.claude/_rules/guiding_principles.md`
