# 📦 Python Module Organisation

**Purpose:** Establish conventions for module docstrings, metadata, and public/private function organisation — ensuring modules are self-documenting and their interfaces are clear.

---

## 📋 Contents

- [Module docstrings & metadata](#-module-docstrings--metadata) — `module_organisation/_docstrings.md`
- [Public vs private functions](#-public-vs-private-functions) — `module_organisation/_public_private.md`
- [Quick reference](#-quick-reference)
- [Related](#-related)

---

## 📝 Module docstrings & metadata

@module_organisation/_docstrings.md

---

## 🔒 Public vs private functions

@module_organisation/_public_private.md

---

## ⚡ Quick reference

| Element | Convention | Example |
|---------|-----------|---------|
| **Module docstring** | Multi-line at top, before imports | `"""Description: ..."""` |
| **Date created** | In docstring | `Date created: 2026-06-26` |
| **`__author__`** | String, after docstring | `__author__ = "Paul Fry"` |
| **`__version__`** | String, after docstring | `__version__ = "0.1"` |
| **Public function** | No underscore | `def load_config():` |
| **Private function** | Leading underscore | `def _make_client():` |
| **Constants** | SCREAMING_SNAKE_CASE, grouped | `TIMEOUT = 30` |
| **Constant group label** | Comment above group | `# Defaults` |

---

## 🔗 Related

- Parent: `python.md` — Full Python style guide
- Sibling: `python/testing.md` — Testing conventions
- Sibling: `python/logging.md` — Logging conventions
