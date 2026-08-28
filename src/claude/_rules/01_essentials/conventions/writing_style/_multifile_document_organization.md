# 📁 Multifile Document Organization

**Purpose:** Establish a universal directory structure convention for multi-file documents across all Claude config directories — preventing flat-level sprawl and keeping related files organized into dedicated subdirectories.

Applies to all `.md` files in `_rules/`, `style_guide_standards/`, `process/`, agents, skills, and any other structured documentation in the Claude context.

---

## 🎯 The Pattern

Documents follow a **size-based organization principle**:

### Single-file documents (stay flat)
**Condition:** One document covering a complete topic, ≤110 lines, self-contained.

```
_rules/03_lazy_load/
├── rule_one.md           ← single file, stays at top level
├── rule_two.md           ← single file, stays at top level
└── rule_three.md         ← single file, stays at top level
```

**Decision rule:**
- File is self-contained with no child pages
- No index/parent file required
- Place directly in the directory (flat level)

### Multi-file documents (get subdirectories)
**Condition:** One parent index file + 2+ child files covering related aspects of a topic.

```
_rules/01_essentials/
├── behaviour.md                             ← parent index at top level (entry point)
├── behaviour/                               ← child files in dedicated subdirectory
│   └── _decision_making.md
```

**Decision rule:**
- Parent index file at top level (discoverable entry point)
- All child files in dedicated subdirectory named `<topic>/`
- Child files use underscore prefix: `_<aspect>.md` (distinguishes from top-level docs)
- Parent file lists all children with links to `subdirectory/_file.md`
- Sibling links within subdirectory are relative: `[_file.md](_file.md)`

---

## ⚠️ When to Apply

**Trigger:** Any document growing to 2+ related child pages, or when >110 lines.

**Questions to ask:**

1. Does this document have multiple related child pages?
   - **YES** → create parent index + subdirectory structure
   - **NO** → keep as single file

2. Is the file > 110 lines?
   - **YES** → split into parent index + child files
   - **NO** → assess if topic complexity warrants splitting anyway

3. Are child pages distinct topics grouped under one parent?
   - **YES** → use subdirectory for the group
   - **NO** → each should be a standalone document file

---

## 📚 Examples

### ✅ Correct: Multi-file structure (Behaviour)

```
behaviour.md                            ← parent: safe defaults and action guidelines
behaviour/
└── _decision_making.md                 ← child: when to present options vs. decide unilaterally
```

**Why:** Two distinct aspects (core principles, decision-making specifics) grouped under one topic. Parent is the entry point; child is reference material.

### ✅ Correct: Single-file (Simple rule)

```
some_rule.md                             ← complete, self-contained rule
```

**Why:** One concept, <110 lines, no need for child pages.

### ❌ Wrong: Flat-level sprawl (Anti-pattern)

```
_rules/01_essentials/
├── _decision_making.md                 ← ❌ orphaned child at flat level
└── behaviour.md                        ← ❌ parent created after child scattered
```

**Why:** Child files at flat level create clutter. No clear grouping. Difficult to maintain and extend.

---

## ✅ Verification Checklist

Before creating or modifying a document:

- [ ] **Is this a single-file document?** → Place at top level (flat)
- [ ] **Is this multi-file (2+ pages)?** → Create parent index + subdirectory
  - [ ] Parent index file at: `<directory>/<topic>.md`
  - [ ] Child files at: `<directory>/<topic>/_<aspect>.md`
  - [ ] Child files use underscore prefix `_<aspect>.md`
  - [ ] Parent index has table/list with links to `<topic>/_<aspect>.md`
  - [ ] Sibling links within subdirectory are relative: `[_file.md](_file.md)`
- [ ] **Is the file > 110 lines?** → Consider splitting into parent + children
- [ ] **Will this document likely grow?** → Use subdirectory structure preemptively

---

See [[writing_style]] for general style constraints.
