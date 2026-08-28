# 📝 Python Logging Conventions

**Purpose:** Establish logging standards for debugging, monitoring, and auditing — ensuring logs are useful, secure, and structured.

---

## 📋 Contents

- [Logger setup and levels](#-logger-setup-and-levels) — `logging/_setup_and_levels.md`
- [What to log and what not to log](#-what-to-log-and-what-not-to-log) — `logging/_what_to_log.md`
- [Logging in error handling](#-logging-in-error-handling) — `logging/_error_handling.md`
- [Quick reference](#-quick-reference)
- [Related](#-related)

---

## 🔧 Logger setup and levels

@logging/_setup_and_levels.md

---

## ✅ What to log and what not to log

@logging/_what_to_log.md

---

## 🚨 Logging in error handling

@logging/_error_handling.md

---

## ⚡ Quick reference

| Scenario | Level | Example |
|---|---|---|
| **Function starts/ends** | INFO | `logger.info(f"Starting migration process")` |
| **Important decision** | INFO | `logger.info(f"Using fallback config")` |
| **State change** | INFO | `logger.info(f"Connection disabled")` |
| **Unexpected but recoverable** | WARNING | `logger.warning(f"File not found, using default")` |
| **Error before re-raise** | ERROR | `logger.error(f"Config invalid: {e}")` |
| **Development debug info** | DEBUG | `logger.debug(f"Variable x = {x}")` |

---

## 🔗 Related

- Parent: `python.md` — Full Python style guide
- Sibling: `python/testing.md` — Testing conventions
- Sibling: `python/module_organisation.md` — Module docstrings and public/private functions
