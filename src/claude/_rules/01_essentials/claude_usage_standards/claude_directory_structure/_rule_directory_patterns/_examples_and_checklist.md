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
  - [ ] Parent rule has contents section with links to `<concept>/_<aspect>.md`
  - [ ] Sibling links within subdirectory use relative paths: `[_file.md](_file.md)`
- [ ] **Is the parent rule >110 lines?** → Consider if splitting is justified
- [ ] **Do you have only 1 child rule?** → Violates 2+ rule; flatten to top level instead
- [ ] **Are all children directly related to parent concept?** → Avoid mixing unrelated rules in one subdirectory

---

## 📝 Documentation Requirements

When creating a multi-concept rule structure:

1. **Parent rule:** Explain purpose, link to all children, guide reader to start with parent
2. **Child rules:** Reference parent and siblings clearly; use relative links
3. **README:** Update `_rules/<tier>/README.md` to show new parent+child structure
4. **CLAUDE.md:** If rule is top-level import, update path from `@~/.claude/_rules/<tier>/<concept>.md` to match parent location

---

## 🔗 Related

- Parent: `_rule_directory_patterns.md` — the pattern itself, when to apply it
