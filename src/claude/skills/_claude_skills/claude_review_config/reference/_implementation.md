# Implementation — 4-Phase Workflow

## Phase 1: Read & Score

Reads key config artefacts from the config folder (`$CLAUDE_CONFIG_DIR`, or `~/.claude/` when it's unset) and scores across six quality dimensions:

**Dimensions:**
1. **Rule quality** — Clarity, specificity, actionability, DRY (no duplicate guidance)
2. **Config complexity** — Import chain depth, file sizes vs. 100-line limit
3. **Testing** — Test coverage in `_tests/` for hooks and rules
4. **Security posture** — Separation of concerns, prompt injection defence, secret handling
5. **Documentation** — READMEs, MEMORY.md index, rationale in rules
6. **Standards adherence** — Naming conventions, line limits, import patterns, emoji/bold-keyword style

**Scoring scale:** 1–10, where 9–10 = excellent, 7–8 = good, 5–6 = acceptable, 1–4 = needs work

**Output:** Scorecard with per-dimension scores and reasoning

---

## Phase 2: Generate Gap Analysis

Produces a MoSCoW table identifying missing elements:

| MoSCoW | Examples |
|---|---|
| **Must** | Critical gaps (missing security rules, no tests for enforcement hooks, high-risk issues) |
| **Should** | Important gaps (missing documentation, incomplete style guides, low-priority standardization) |
| **Could** | Nice-to-have improvements (future enhancements, nice-to-have features) |
| **Won't** | Explicitly out of scope for this audit |

**Output:** Prioritized table of actionable items

---

## Phase 3: Create Scorecard & Recommendations

Generates comprehensive audit report with:

- **Overall grade:** A–F based on average of six dimension scores
- **Scorecard table:** Per-dimension scores with reasoning
- **Gap analysis:** MoSCoW table of missing elements
- **Recommendations:** Severity-rated improvements with rationale

**Output:** Markdown file (`~/claude/_drafts/general/YYYY_MM_DD_claude_config_review.md`) with full scorecard, analysis, and recommendations

---

## Phase 4: Offer Fixes (Optional)

For each Must/Should item in the gap analysis:

1. Present the issue and proposed fix
2. Ask for confirmation
3. Apply the fix to the config folder only if that fix was confirmed
4. Optionally sync to the playbook repo (`src/claude/`)
5. List the files changed, and leave committing to the user

**Output:** Updated config files, never committed automatically
