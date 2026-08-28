# 📊 Scoring Guide — Reference Files

Scoring rubric for reference documentation. Scores range 1–10 across five quality dimensions.

---

## 🎯 The 5 Dimensions

| # | Dimension | What it measures | Higher score = |
|---|---|---|---|
| **1️⃣** | **Coverage** | Topic focus, content completeness, gaps documented | Complete coverage of focused topic |
| **2️⃣** | **Clarity** | Writing quality, jargon, readability, comprehension | Easy to understand |
| **3️⃣** | **Accuracy** | Up-to-date, links valid, aligned with current practice | Current and accurate |
| **4️⃣** | **Documentation** | Examples, prerequisites, gaps, related references | Well-documented |
| **5️⃣** | **Presentation** | Organization, hierarchy, formatting, style compliance | Well-presented |

**Weighting:** Presentation 25%, Clarity 20%, Documentation 20%, Coverage 15%, Accuracy 15%

---

## 1️⃣ Coverage (1–10)

**Principle:** Topic should be focused AND thoroughly covered. **Goal: single focused topic, exhaustively documented.**

Measures conceptual density, completeness relative to scope, and gap documentation.

| Score | Complexity | Scope | Completeness | Judgment |
|---|---|---|---|---|
| **9–10/10** | ✅ **LOW** | Single, focused topic | 95%+ covered; all gaps documented with workarounds | Reference covers one concept exhaustively; no sprawl |
| **7–8/10** | ✅ **MODERATE** | Coherent multi-part guide | 80–90% covered; documented with context | Multiple related sections; clear hierarchy; some gaps OK |
| **5–6/10** | ⚠️ **ELEVATED** | Broad reference spanning 2–3 domains | 60–70% covered; gaps noted but not explained | Multiple domains covered; could benefit from splitting |
| **3–4/10** | ⚠️ **SUBSTANTIAL** | Sprawling reference covering 3+ domains | <60% covered; gaps not documented | Multiple unrelated topics; cognitive overload |
| **1–2/10** | ❌ **HIGH** | Over-scoped monolith | Chaotic, incomplete | Should have been split into 3+ child docs; unnavigable |

**How to assess:**
- Is the topic title self-contained? (e.g., "CODEOWNERS Fundamentals" vs. "GitHub Standards")
- Could the content be understood in 60 seconds if you read the headings?
- How many distinct domains/concerns does it cover?
- Are gaps acknowledged and do they have workarounds?
- Higher score = tighter scope, more complete

---

## 2️⃣ Clarity (1–10)

**Principle:** How well can a reader understand the content without external context?

Measures writing clarity, jargon explanation, and comprehension time.

| Score | Writing | Jargon | Comprehension | Examples |
|---|---|---|---|---|
| 1–4 | Difficult to follow; tangled sentences | Unexplained technical terms | Confusing; reader needs other sources | Minimal or none |
| 5–6 | Mostly clear; some verbose passages | Some jargon explained; some assumed | Mostly understandable with effort | One basic example |
| 7–8 | Clear, direct writing; easy to scan | Jargon explained or avoided | Reader understands in <2 min | Multiple examples for key concepts |
| 9–10 | Excellent clarity; concise writing; skimmable | All jargon explained simply | Reader understands in <60 seconds | Rich examples with variations and edge cases |

**How to assess:**
- Read the opening 2–3 sentences: does a newcomer understand the topic?
- Find a technical term: is it explained?
- Open a random section: can you skim headings and understand the content?
- How long to understand the core concept?

---

## 3️⃣ Accuracy (1–10)

**Principle:** Is the content still accurate and relevant?

Measures up-to-dateness, link validity, and alignment with current practice.

| Score | Accuracy | Links/Sources | Last Updated | Risk of Staleness |
|---|---|---|---|---|
| 1–4 | Outdated; contradicts current practice | Broken or missing sources | >1 year old; explicitly stale | High; content known to be obsolete |
| 5–6 | Mostly current; minor inconsistencies | Most links valid; some sources noted | 6–12 months ago; not verified | Moderate; not actively maintained |
| 7–8 | Current and accurate; spot-checked | Sources linked and working | 2–3 months ago; spot-checked | Low; seems maintained |
| 9–10 | Authoritative; actively maintained | All sources linked, verified, dated | <1 month old; actively used | Very low; constantly updated or verifiable |

**How to assess:**
- Are external links (docs, references) still valid?
- Does the content match current tools/versions?
- Is there a "last updated" date or verification?
- Would this content surprise users who've read the official docs recently?

---

## 4️⃣ Documentation (1–10)

**Principle:** Is the reference production-grade? Are examples, prerequisites, and known gaps documented?

Measures completeness of supporting material.

| Score | Examples | Prerequisites | Known Gaps | Related Refs |
|---|---|---|---|---|
| 1–4 | None or unclear | Not stated | Not mentioned | Missing |
| 5–6 | One basic example | Listed but minimal | Brief mention | One or two linked |
| 7–8 | Multiple examples; some variations | Clear prerequisites; access noted | Documented with context | Good cross-references |
| 9–10 | Rich examples with explanations | Prerequisites crystal clear | Comprehensive gap list + workarounds | Well-linked; navigation clear |

**How to assess:**
- Is there at least one worked example?
- Are prerequisites stated? (e.g., "requires sudo access", "macOS only")
- Are known limitations acknowledged?
- Does the doc link to related references?

---

## 5️⃣ Presentation (1–10)

**Principle:** Is the document easy to navigate and properly formatted?

Measures information architecture, scanning efficiency, and style compliance.

| Score | Hierarchy | Navigation | Scanning | Standards |
|---|---|---|---|---|
| 1–4 | No clear structure; flat | Hard to locate information | Dense paragraphs; no markers | Not compliant |
| 5–6 | Basic hierarchy; some sections | Mostly navigable | Some formatting; could be better | Mostly compliant |
| 7–8 | Clear hierarchy with emojis/headers | Easy to locate; good TOC | Scannable with bold + bullets | Well-compliant |
| 9–10 | Excellent hierarchy; nested sections | Instant navigation; detailed index | Highly scannable with emojis + tables | Exemplary |

**Compliance checklist:**
- Do all `##` headers have emoji prefixes?
- Do bullets start with **bold keyword:** pattern?
- Is the file <110 lines? (Exceeding is a red flag for refactoring)
- Are there trailing newlines?

---

## Overall Score Calculation

**Formula:** Weighted average across five dimensions

```
Overall = (
  Coverage            × 0.15 +
  Clarity             × 0.20 +
  Accuracy            × 0.15 +
  Documentation       × 0.20 +
  Presentation        × 0.25
)
```

---

## How to Use This Guide

**During assessment:**
1. Read the entire reference file
2. For each dimension, identify the band that best describes it
3. Score should be defensible — cite specific examples
4. When unsure, err toward middle bands (5–6)

**Scoring expectations:**
- Most well-maintained reference files score 7–8 overall
- Overly long files (>150 lines) typically score 1–4 on Coverage or Presentation
- One-time setup docs (e.g., environment setup) can score 5–6 even if well-written (limited utility)

**Maintaining scores:**
- Review annually or when major changes occur
- Update scores when gaps are fixed or content drifts
- Document in audit scorecard the rationale for scores near extremes (1–2, 9–10)

---

## Related Guidance

- Writing style: `~/.claude/_rules/writing_style.md`
- Naming standards: `~/.claude/_rules/naming_standards.md`
- Lazy-load strategy: `~/.claude/_rules/lazy_load/README.md`
