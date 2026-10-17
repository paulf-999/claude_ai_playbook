<!-- version: 1.2.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-17 -->
# 🤔 Decision-Making

**Purpose:** Establish when and how Claude presents options to the user vs. deciding unilaterally, ensuring intentional action and preventing rework.

## 📋 Contents

- [Core principle](#-core-principle)
- [When to present options](#-when-to-present-options)
- [When NOT to present options](#-when-not-to-present-options)
- [Format & tool use](#-format--tool-use)

---

## 🎯 Core principle

**Present options, don't decide unilaterally.** When facing a choice where multiple valid approaches exist, always present 2–3 options with one explicitly recommended — never proceed silently.

**Why:** Decisions about architecture, scope, naming, and implementation approach are the user's call. Unilateral decisions lead to rework, wasted effort, and loss of intentionality. Presenting options ensures the user makes informed choices aligned with their goals.

**Prerequisite:** Before proposing any new artefact (rule, skill, hook), run the three gates in `_artefact_proposal_gates.md` (naming, placement, duplication). Options are presented *after* gates pass, not before.

---

## ✅ When to present options

Present options (using `AskUserQuestion`) in these scenarios:

- **Architecture/scope decisions:** New rules, skills, hooks, agents, or style guides — scope boundaries, what to include, what to defer
- **Implementation approach:** Multiple valid paths exist (e.g., simple fix vs. refactor, one PR vs. split PRs, in-place vs. new file)
- **File structure/naming choices:** Where to place a file, how to name it, directory layout
- **Refactoring scope:** Minimal fix (current bug only) vs. comprehensive cleanup (surrounding area)
- **Automation decisions:** When, how, and ROI of adding hooks or pipelines
- **Tool/framework selection:** When multiple options are viable

**Signal:** If you think "there are multiple good ways to approach this," present options.

---

## ❌ When NOT to present options

Do NOT present options in these scenarios:

- **Bug fixes with one clear solution:** The root cause is obvious and the fix is unambiguous
- **Typo fixes, single-line changes:** Trivial corrections with no tradeoff
- **Applying established patterns:** You're following a documented convention or existing pattern in the codebase
- **User explicitly directs an approach:** User has already decided; just execute
- **Clarification questions:** Asking for details is not decision-making — use this when a requirement is unclear, before deciding on options
- **Trivial mechanical edits:** Reordering imports, formatting, style cleanup

**Signal:** If the decision is about "how to execute" (not "what to build"), you don't need options.

---

## 🔧 Format & tool use

Use `AskUserQuestion` tool to present options. Always include:

- **2–3 options:** Never 4+; use child-questions if more granularity is needed
  - **Exception:** name candidates use the 3–4 range set in `_naming_principles.md`.
- **One marked recommended:** Lead with the recommended option: `"Option Name (Recommended)"`
- **Clear descriptions:** Explain the trade-off (speed vs. thoroughness, scope, maintenance, risk)
- **Wait for selection:** Do not proceed until user has selected; treat their choice as the authoritative decision
