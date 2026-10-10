---
created: 2025-09-01
last_modified: 2026-08-19
---

# 🔐 CODEOWNERS Ownership Patterns

---

## 🔒 Pattern 1: Self-ownership of `.github/`

`.github/` must have explicit ownership — never shared or unowned:

```
/.github/ @you-or-your-team
```

**Why:** Critical infrastructure (CI/CD, templates, config) requires explicit review. See [Fundamentals](fundamentals.md) for file location and rule ordering.

---

## 👥 Pattern 2: Team handles over individuals

Use team handles, not individual usernames:

```
# ❌ Don't do this
/src/db/ @alice @bob

# ✅ Do this instead
/src/db/ @backend-team
```

**Why:** Teams survive personnel changes and handle rotation.

---

## 💬 Pattern 3: Comment conventions

Comments explain *why* ownership exists, not *what* the file does:

```
# Security: auth layer changes require review
/src/auth/ @security-team

# ⚠️ Shared ownership — both teams must approve
/src/shared/ @backend-team @frontend-team
```

---

## 🚫 Anti-patterns

| ❌ Don't | Why |
|----------|-----|
| `* @everyone` | Catch-all noise; enforce review only where needed |
| `@alice @bob` | Use teams instead |
| Inline comments | Comments should explain *why*, not *what* |

---

**Compatibility note:** All patterns use GitHub's current CODEOWNERS syntax (valid as of 2026-08). Check [GitHub docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) for updates.

---

## 🚫 Anti-patterns

| ❌ Don't do | Why |
|---|---|
| `* @everyone` | Catch-all becomes noise; enforce review only where needed |
| `@alice @bob @carol` | Use teams instead; individuals drift in/out of scope |
| Inline comments: `/{path} @team # this does X` | Comments should explain *why*, not describe the file |
| Rules without owners: `/{path}` | Every rule should specify who owns it |
