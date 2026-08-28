# 🧪 Testing

**Purpose:** Every new code artifact needs a test to prevent regressions and validate intended behavior.

## 📋 Contents

- [When Tests Are Required](#-when-tests-are-required)
- [Test Goals (What to Validate)](#-test-goals-what-to-validate)
- [Child Files (Load As Needed)](#-child-files-load-as-needed)
- [Quick Reference](#-quick-reference)

---

## ✅ When Tests Are Required

- **🆕 New features:** CLI commands, config settings, skills, hooks — all need tests.
- **🧩 New abstractions:** Functions, classes, utilities, rule files require tests.
- **🔧 Breaking changes:** Changed behavior requires updated tests.
- **🐛 Bug fixes:** Include regression test to prevent recurrence.

**Exception:** Instructional content (README, documentation) does not require tests — `test_rules_structure.py` validates file quality.

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

## 📐 Test Design Pattern

@~/.claude/_rules/02_claude_standards/testing/_testing_design_pattern.md

## 🚫 Anti-Patterns

@~/.claude/_rules/02_claude_standards/testing/_testing_anti_patterns.md

## 📁 File Organization

@~/.claude/_rules/02_claude_standards/testing/_testing_file_organization.md

## 🔄 Maintenance

@~/.claude/_rules/02_claude_standards/testing/_testing_maintenance.md

---

## ⚡ Quick Reference

**Rule of thumb:** If you added code, write a test.
**Goal statement:** One sentence explaining what the test validates.
**Location:** Tests adjacent to code (`_tests/<domain>/test_<feature>.py`).
**Assertion messages:** Explain what went wrong and how to fix it.

---

## 📖 Reference (Claude's design patterns)

<!-- Testing principles overview -->
@~/.claude/_reference/claude_design_patterns/testing/_testing.md

<!-- Advanced testing patterns and strategies -->
@~/.claude/_reference/claude_design_patterns/testing/_testing_strategy.md

<!-- How to add tests to new features -->
@~/.claude/_reference/claude_design_patterns/testing/_adding_tests.md
