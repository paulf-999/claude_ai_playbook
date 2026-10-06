<!-- version: 2.0.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-06 -->
# 📁 Multifile Document Organisation

**Purpose:** One convention for when to split a document into a parent and child files, and how to lay them out — preventing flat-level sprawl across `_rules/`, style guides, skills, agents and any other structured documentation.

---

## 🎯 The Pattern

| Shape | When | Layout |
|---|---|---|
| **Single file** | One complete, self-contained topic, ≤110 lines | `<directory>/<topic>.md`, placed flat |
| **Parent + children** | A topic with 2+ related child pages, or one that has grown past 110 lines | `<directory>/<topic>.md` plus `<directory>/<topic>/_<aspect>.md` |

- **Parent:** sits at the top level as the discoverable entry point, explains the topic and links (or, in `rules/`, points to) every child.
- **Children:** live in a subdirectory named after the parent, use the `_` prefix, and each cover one aspect of the parent's topic.
- **2+ rule:** never create a subdirectory for a single child — flatten it to a top-level file instead (e.g. `behaviour/` holding only `_decision_making.md` becomes `decision_making.md`).
  - **Why:** a one-child folder adds navigation overhead without grouping anything.
- **Sibling links:** any inline link between children is relative — `[_file.md](_file.md)`.

---

## ⚠️ When to Apply

1. **Does the topic have 2+ related child pages?** Yes → parent + subdirectory. No → single file.
2. **Is the file over 110 lines?** Yes → split into parent + children. No → split only if the topic's complexity warrants it.
3. **Are the children distinct aspects of one parent topic?** Yes → group them in one subdirectory. No → make each a standalone file, and don't mix unrelated files in one folder.

---

## 📚 Examples

```
rules/02_claude_standards/
├── behaviour.md                     ← ✅ parent: entry point
├── behaviour/
│   ├── _artefact_proposal_gates.md  ← child: validating proposals
│   ├── _decision_making.md          ← child: when to present options
│   └── …                            ← further children
└── portable_paths.md                ← ✅ single concept, flat, no children
```

**❌ Orphaned child at flat level:** a `_decision_making.md` sitting next to `behaviour.md` instead of inside `behaviour/` — no clear grouping, and the parent ends up created after the sprawl.

---

## 📏 Extra Rules for Rule Files

- **Children load on their own:** every `.md` under `rules/` loads natively, so the parent names each `<topic>/_<aspect>.md` in a `**Loads on its own from:**` line instead of an `@import`.
- **On-demand children:** keep children read only when needed in `_rules_lazy_load/<topic>/`, named in a `**Read on demand:**` pointer.
- **Contents only when earned:** add a Contents section only if the file has 3 or more real `##` headings.
- **Related links:** parent and sibling link lists go in the tier README in `_rules_lazy_load/_tier_readmes/` (or `_rules_lazy_load/README.md` for lazy and path-scoped rules) under "🔗 Related rules", never in the rule, and `01_essentials/` rules keep none (#310).
- **README:** update the tier's README in `_rules_lazy_load/_tier_readmes/` to show the new parent + child structure.
- **No READMEs in `rules/`:** any `.md` there loads every session, so indexes live in `_rules_lazy_load/`.

---

## ✅ Verification Checklist

- [ ] **Single file?** → flat at the top level
- [ ] **Parent + children?** → parent at `<directory>/<topic>.md`, children at `<directory>/<topic>/_<aspect>.md`
- [ ] **Children use the `_` prefix** and there are 2 or more of them
- [ ] **Every child relates directly to the parent topic**
- [ ] **Over 110 lines?** → split into parent + children
- [ ] **A rule file?** → the extra rules above are met

---

See [[writing_style]] for general style constraints.
