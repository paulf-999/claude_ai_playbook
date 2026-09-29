<!-- version: 1.1.2 -->
<!-- created: 2026-09-18 -->
<!-- updated: 2026-09-29 -->
# ✅ Rule Directory Patterns — Examples & Checklist

**Purpose:** Worked examples, the "2+ rule", and a verification checklist for applying the parent+child rule directory pattern correctly.

---

## ✅ Examples

### ✅ Correct: Multi-concept structure (Behaviour)

```
behaviour.md                            ← parent: safe conduct guidelines
behaviour/
├── _artefact_proposal_gates.md         ← child: validating proposals
└── _decision_making.md                 ← child: when to present options
```

**Why:** Two distinct concepts (safe conduct, decision-making) grouped under behaviour. Parent is entry point; children are reference material.

### ✅ Correct: Single-concept rule (Security)

```
security.md                             ← complete, self-contained rule
```

**Why:** One concept (secure coding practices), no child rules, <110 lines, discoverable at top level.

### ❌ Wrong: Orphaned child at flat level (Anti-pattern)

```
_rules/01_essentials/
├── _decision_making.md                 ← ❌ orphaned child at flat level
└── behaviour.md                        ← ❌ parent created after sprawl
```

**Why:** Child file at flat level creates clutter and confusion. No clear grouping; difficult to navigate and maintain.

---

## 🚫 The "2+ Rule"

Do not create a subdirectory for a single child file.

- ❌ `behaviour/` with only `_decision_making.md` → Flatten to top-level, name `decision_making.md`
- ✅ `behaviour/` with `_artefact_proposal_gates.md` + `_decision_making.md` → Justified; two related children

**Why:** Single-child subdirectories create unnecessary navigation overhead. Threshold is 2+.

---

## ✅ Verification Checklist

Before organizing a rule into parent+child structure:

- [ ] **Is this a single-concept rule?** → Keep flat at top level
- [ ] **Is this multi-concept (2+ related rules)?** → Create parent + subdirectory
  - [ ] Parent rule at: `_rules/<tier>/<concept>.md`
  - [ ] Child rules at: `_rules/<tier>/<concept>/_<aspect>.md`
  - [ ] Child files use underscore prefix `_<aspect>.md`
  - [ ] Parent rule `@import`s each `<concept>/_<aspect>.md`, with a Contents section only if it has 3 or more real `##` headings
  - [ ] Any inline link to a sibling in the rule body uses a relative path: `[_file.md](_file.md)`
  - [ ] Parent and sibling link lists go in the tier `README.md` under "🔗 Related rules", not in the rule
- [ ] **Is the parent rule >110 lines?** → Consider if splitting is justified
- [ ] **Do you have only 1 child rule?** → Violates 2+ rule; flatten to top level instead
- [ ] **Are all children directly related to parent concept?** → Avoid mixing unrelated rules in one subdirectory

---

## 📝 Documentation Requirements

When creating a multi-concept rule structure:

1. **Parent rule:** Explain purpose, link to all children, guide reader to start with parent
2. **Child rules:** Keep parent and sibling links out of the rule file itself
3. **README:** Update `_rules/<tier>/README.md` to show the new parent+child structure, and list each file's parent and siblings under "🔗 Related rules"
4. **CLAUDE.md:** If rule is top-level import, update path from `@~/.claude/_rules/<tier>/<concept>.md` to match parent location
