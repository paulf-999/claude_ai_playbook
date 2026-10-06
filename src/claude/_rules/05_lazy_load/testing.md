---
paths:
  - "**/*.py"
  - "**/*.sh"
  - "**/*.sql"
  - "**/_tests/**"
---
<!-- version: 1.4.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-06 -->
<!-- miss_cost: medium — untested code the user catches in review -->
<!-- loading: path-scoped — only matters when writing code, so it loads when a Python, shell or SQL file is open -->
# 🧪 Testing

**Purpose:** Every new code artifact needs a test to prevent regressions and validate intended behavior.

## 📋 Contents

- [When Tests Are Required](#-when-tests-are-required)
- [Test Goals (What to Validate)](#-test-goals-what-to-validate)
- [Test Design Pattern & Anti-Patterns](#-test-design-pattern--anti-patterns)
- [File Organization](#-file-organization)
- [Maintenance](#-maintenance)
- [Test Metadata Standard](#-test-metadata-standard)
- [Quick Reference](#-quick-reference)

---

## ✅ When Tests Are Required

- **🆕 New features:** CLI commands, config settings, skills, hooks — all need tests.
- **🧩 New abstractions:** Functions, classes, utilities, rule files require tests.
- **🔧 Breaking changes:** Changed behavior requires updated tests.
- **🐛 Bug fixes:** Include regression test to prevent recurrence.

**Exception:** Instructional content (README, documentation) does not require *behavior-compliance* tests — whether Claude actually follows a rule isn't mechanically testable without an eval harness that grades a live session, which this repo doesn't have. `test_rules_structure.py` covers file quality for every rule by default.

**But add a lightweight content-regression test** (assert key phrases survive, mirroring `test_git.py`'s pattern) when a rule documents a real incident or hard-won lesson — the value isn't proving compliance, it's catching silent loss of the rule's text in a future edit or merge. Don't add one reflexively for every rule; reserve it for content that would be costly to lose without anyone noticing.

---

## 🎯 Test Goals (What to Validate)

Define the goal before writing the test. Tests validate *intended behavior*, not just "the code runs."

**Before writing a test, define success criteria using SMART principles:**
- **Specific:** "accurate sentiment classification" vs. "good performance"
- **Measurable:** Quantifiable metrics (F1 score, accuracy) or well-defined qualitative scales
- **Achievable:** Based on industry benchmarks and your actual requirements
- **Relevant:** Aligned with your application's real purpose, not hypothetical edge cases

**For LLM-facing code,** include edge cases that are easy to miss: ambiguous or implicit inputs (where humans would struggle), mixed/conflicting signals (sarcasm, multiple sentiments), adversarial inputs (harmful prompts), and typos/malformed text.

| Goal | Example | Purpose |
|---|---|---|
| **Structure** | `test_aliases.py` | Config file structure + required fields valid |
| **Behavior** | `test_aliases_behavior.py` | Feature works as documented |
| **Principles** | `test_settings.py` | Change aligns with guiding principles |
| **Integration** | Skill runs end-to-end | Feature integrates with rest of system |
| **Regression** | Bug fix test | Bug won't silently reappear |
| **Consistency** | Style guide hooks | Standards enforced; no exceptions |

---

## 📐 Test Design Pattern & Anti-Patterns

- **Read on demand:** [`~/.claude/_rules/05_lazy_load/testing/_testing_design_pattern.md`](testing/_testing_design_pattern.md) — before writing a new test: state the goal, test behaviour, write assertion messages, spot-check.
- **Read on demand:** [`~/.claude/_rules/05_lazy_load/testing/_testing_anti_patterns.md`](testing/_testing_anti_patterns.md) — before writing a new test: empty, over-mocked, fragile, slow and unclear tests to avoid.
- **Read on demand:** [`~/.claude/_rules/05_lazy_load/testing/_test_metadata_audit.md`](testing/_test_metadata_audit.md) — when auditing tests: the quarterly audit, worked example and archival workflow.

## 📁 File Organization

- **Read on demand:** [`~/.claude/_rules/05_lazy_load/testing/_testing_file_organization.md`](testing/_testing_file_organization.md) — before creating a test file: where it lives and how to name it.

## 🔄 Maintenance

- **Update tests with code:** change a test in the same commit as the behaviour it covers.
- **Delete dead tests:** remove a feature's tests when the feature is removed.

## 📊 Test Metadata Standard

- **Read on demand:** [`~/.claude/_rules/05_lazy_load/testing/_test_metadata.md`](testing/_test_metadata.md) — before writing or editing a test: the required header, and the quality ≥9 and complexity ≥7 floor that `test_test_score_floor.py` enforces.

---

## ⚡ Quick Reference

**Rule of thumb:** If you added code, write a test.
**Goal statement:** One sentence explaining what the test validates.
**Location:** Tests adjacent to code (`_tests/<domain>/test_<feature>.py`).
**Assertion messages:** Explain what went wrong and how to fix it.

---

## 📖 Reference (Claude's design patterns)

- **Read on demand:** `~/.claude/_reference/claude_config_architecture/_testing.md` — test layers, where each kind of test lives, and how to run the suite
