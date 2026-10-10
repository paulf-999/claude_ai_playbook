---
created: 2025-09-01
last_modified: 2026-08-19
---

# 🔐 CODEOWNERS Fundamentals

Five core concepts for designing CODEOWNERS files that reflect actual code ownership.

---

## ✅ Fundamental 1: When to use

Add a `CODEOWNERS` file when:
- Multiple teams own distinct areas
- You need code review enforcement
- Team members understand design decisions deeply

**Skip CODEOWNERS** if ownership is shared/unclear — don't create rules that misrepresent who actually owns code.

See [Patterns](patterns.md) for how to express ownership rules in practice.

---

## 📍 Fundamental 2: File location

`CODEOWNERS` lives in `.github/` at repository root:

```
.github/CODEOWNERS
```

GitHub auto-detects and enforces rules. See [Patterns](patterns.md) for examples of well-structured files.

---

## 📐 Fundamental 3: Rule ordering (last-wins)

Rules are processed **last-wins** — GitHub applies the final matching rule. Order broad → narrow:

```
* @default-owner          # Broad
/src/components/ @team    # More specific
/src/components/auth.py @specialist  # Most specific
```

This prevents broad rules from blocking narrow assignments.

---

## 🗂️ Fundamental 4: Section structure

Organize with comments:

```
# Infrastructure
/.github/ @platform-team
/terraform/ @infrastructure-team

# Backend
/src/api/ @backend-team
```

---

## 🚫 Fundamental 5: No catch-all

Don't add `* @someone` — it stales quickly. Instead:
- List explicit ownership where review is needed
- Leave unowned paths unassigned
- Add paths as ownership becomes clear

See [Patterns — Anti-patterns](patterns.md#anti-patterns) for common mistakes to avoid.
