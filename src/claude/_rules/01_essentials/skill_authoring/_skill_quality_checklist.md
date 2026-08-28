# ✅ Quality Checklist (Author & Reviewer)

**Purpose:** Define checkpoints for skill creation to ensure quality gates are met.

---

## 🏗️ Authoring Checklist

### Hard Gates (Block if violated)

- [ ] **Naming:** `<domain>_<action>` format, valid domain, directory matches
- [ ] **Created via `/skill_creator`** (not manually)
- [ ] **Complexity score ≤ maturity limit** (draft ≤4, tactical ≤6, strategic ≤8)
- [ ] **Contract fields:** name, version, summary, maturity, test_coverage_level, when, requires, output, reversible
- [ ] **SKILL.md structure:** All 8 sections present + emoji headers
- [ ] **Test count matches maturity:** Draft 1–2, Tactical 5–8, Strategic 15+

### Quality Checks (Request changes; negotiable)

- [ ] **Opening is clear:** Explains purpose in <60 seconds
- [ ] **Bold keywords:** All bullets use bold keywords (`**Why:**`, `**Note:**`, `**Example:**`)
- [ ] **No TODO/FIXME:** Draft only; tactical+ must resolve
- [ ] **No hardcoded paths:** No coupling to personal directories or usernames
- [ ] **File under ~100 lines:** SKILL.md stays scannable and focused

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
