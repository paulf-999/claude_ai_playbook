# 🔑 CODEOWNERS Style Guide

File location, rule ordering, team handle conventions, section structure, and self-ownership rules.

---

## 📋 When to use CODEOWNERS

Only add an entry where you own the code and know the design decisions behind it — where incorrect changes would have repercussions. CODEOWNERS is not a registry of all files; it is a gate on meaningful change.

Low-risk paths (e.g. `docs/`, `archive/`) generally do not need explicit entries. Leave them unowned by design rather than adding noise.

---

## 📁 File location

Always `.github/CODEOWNERS`. Never the repo root or any other path.

---

## ⬇️ Rule ordering — last-wins

GitHub evaluates top-to-bottom; the **last matching rule wins**. Order broad → narrow: catch-all first, top-level directories next, subdirectory refinements last.

**Wrong** — catch-all below `src/` overrides it:
```
src/   @org/dpe
*      @org/everyone
```
**Right:**
```
*      @org/everyone
src/   @org/dpe
```

### No catch-all by design

Omitting `*` is valid and intentional. Document it:
```
# No catch-all — CODEOWNERS is applied only where changes carry meaningful risk.
```

---

## 🔒 Self-ownership

`.github/` must always be explicitly assigned — never left to a catch-all:
```
.github/    @your-org/your-team
```

---

## 👥 Team handles over individuals

Prefer `@org/team` handles. Use named individuals when they own the code and know the design decisions behind it — not just to manage notification volume. Document the reason:
```
# Rajesh owns the dbt DAG scheduling logic — changes here affect pipeline dependencies.
dags/topics/dbt_dags/**/* @org/dpe @rajesh-rao_pyrc
```

Other valid reasons to add named individuals — always document the reason in a comment:

| Pattern | Consideration |
|---|---|
| Timezone coverage | If the owning team is concentrated in one timezone, consider adding individuals who can provide review coverage during off-hours. Document which timezone gap they cover. |
| Break-glass approvers | Managers or seniors can be added to high-impact paths as an escalation route, not as day-to-day reviewers. Document this intent explicitly. |

---

## 💬 Comment conventions

Every rule or block needs a comment explaining the rationale — why this ownership, not what the rule does.

Co-own across multiple handles where a repo enforces a minimum of 1 approver — prevents any single person from being a bottleneck:
```
# Session config — co-owned to distribute review load (1 approver min).
src/claude/process/    @org/dpe @user1_pyrc
```

Use a warning comment for high-impact shared code:
```
# ⚠️  EDIT WITH CAUTION — shared logic imported everywhere; changes here affect every pipeline.
includes/ @org/dpe @user1_pyrc
```

---

## 🗂️ Section structure

Group related rules with section dividers, ordered broad → narrow:
```
# -------------------------------------------------------------------------
# Section name
# -------------------------------------------------------------------------
```

---

## 🔀 Override pattern

Add a narrower rule after a broader one to override it for a specific path:
```
# All skills — dpe + den co-owned
src/claude/skills/                           @org/dpe @den1_pyrc

# Platform patterns within skills — dpe only
src/claude/skills/create_page/data_platform/ @org/dpe
```
