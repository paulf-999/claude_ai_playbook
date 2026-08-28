---
created: 2025-08-01
last_modified: 2026-08-19
---

# 🔢 Versioning Standards (Semver)

Applies to all Claude components — skills, process docs, rules, and CLAUDE.md files.

---

## 🔢 Skill-level versioning

Map semver major version to maturity tier:

| Version | Maturity | Status |
|---------|----------|--------|
| `0.x.x` | draft | Exploring; breaking changes OK; don't depend on |
| `1.x.x` | tactical | Stable; solves use case reliably |
| `2+.x.x` | strategic | Production-ready; fully maintained |

**Increment rules:**
- Patch (`x.x.N`) — bug fixes within a tier
- Minor (`x.N.0`) — new capabilities, same tier
- Major (`N.0.0`) — promotion to next tier (e.g., 0.x → 1.0)

**What NOT to bump:**
- Moving directories (e.g., wip/ → skills/) — organizational only
- Renaming files — no content change

---

## ⚠️ Common mistakes

| ❌ Mistake | ✅ Fix | Why |
|-----------|--------|-----|
| Bumping patch for breaking change | Create major version | Patch implies safe upgrade |
| Jumping major without criteria | Use maturity tier gate | Major = promotion tier, not arbitrary |
| Version = directory location | Use maturity instead | Version = stability, not organization |

---

## 📦 Repo-level releases

Align GitHub Releases to phase completion:

```
Phase 1 done → v1.0.0
Phase 2 done → v2.0.0
Bug fix in Phase 1 → v1.0.1
```

Use semver tags. Changelog generated from PR descriptions via release skill.

---

**Workflow example:** Feature merge → bump minor (v1.1.0) · Maturity promotion (draft→tactical) → bump major (v1.0.0)
