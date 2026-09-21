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

## 📐 Test Design Pattern

@~/.claude/_rules/02_claude_standards/testing/_testing_design_pattern.md

## 🚫 Anti-Patterns

@~/.claude/_rules/02_claude_standards/testing/_testing_anti_patterns.md

## 📁 File Organization

@~/.claude/_rules/02_claude_standards/testing/_testing_file_organization.md

## 🔄 Maintenance

@~/.claude/_rules/02_claude_standards/testing/_testing_maintenance.md

## 📊 Test Metadata Standard

@~/.claude/_rules/02_claude_standards/testing/_test_metadata.md

---

## ⚡ Quick Reference

**Rule of thumb:** If you added code, write a test.
**Goal statement:** One sentence explaining what the test validates.
**Location:** Tests adjacent to code (`_tests/<domain>/test_<feature>.py`).
**Assertion messages:** Explain what went wrong and how to fix it.

---

## 📖 Reference (Claude's design patterns)

<!-- Testing strategy: test layers, coverage, integration patterns -->
@~/.claude/_reference/claude_config_architecture/_testing.md
