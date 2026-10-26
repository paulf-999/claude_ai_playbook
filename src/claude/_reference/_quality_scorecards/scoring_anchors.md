# ⚓ Scoring Anchors

**Purpose:** Short worked examples of what a 5, a 7 and a 9 look like for skills, rules and agents, so two reviewers give the same artefact the same score.

---

## 🎯 How to use

- **Compare first:** before scoring a dimension, find the anchor row nearest to what the files show.
- **Score between anchors:** a 6 or 8 means the artefact sits between two rows.
- **10 and below 5:** use the "10 looks like" and "1 looks like" columns in the type's rubric.
- **Evidence only:** an anchor counts as met only when a file shows it, never because the author says so.
- **Bands:** 9–10 is excellent, 7–8 meets the bar with minor gaps, 5–6 has notable gaps and 1–4 needs work, as in `claude_review_config`'s scoring guide.
- **Run pass rate:** for agents, `scripts/_audit_scripts/audit_agent_evals.py` runs the evals that have a `run` block and reports a pass rate.
  - **90% or more:** Test Coverage can reach 9, if the skipped evals are only ones that need a full session, such as routing.
  - **75–89%:** Test Coverage stays at 8 or below until the failures are fixed or explained.
  - **Below 75%, or no run:** the unrun-evals cap of 7 still applies.

---

## 🧭 Shared dimensions

These anchors apply to every type that scores the dimension.

| Dimension | ~5 | ~7 | ~9 |
|---|---|---|---|
| **Test Coverage** | • ⚠️ **Thin:** fewer evals than the maturity needs, or no "not for" case | • 📊 **Right count:** evals at the maturity's count, but prose that nothing runs (the cap for unrun evals) | • ✅ **Runs:** a test or eval runner proves the behaviour, including the "not for" cases |
| **Evidence of Need** | • ❓ **Speculative:** built for a problem nobody has hit yet | • ✅ **One real use:** a dated incident or issue, but no record of repeat use | • 📈 **Recurring:** several recorded uses or incidents, such as rows in a usage CSV |
| **Complexity** | • 🧮 **Raw 5:** several jobs, several folders and one external service | • 🧮 **Raw 3:** one job that reads across several folders | • 🧮 **Raw 1:** one job in one folder, with no external services |
| **Clarity** | • 🌫️ **Vague:** a reader can't tell when to use it without opening the body | • 🔍 **Clear body:** the opening is clear, but triggers or the description miss common phrasings | • 🎯 **Self-explaining:** the description alone says what it does, when to use it and when not to |

---

## 🛠️ Skills

| Dimension | ~5 | ~7 | ~9 |
|---|---|---|---|
| **Design** | • 🧩 **Tangled:** phases overlap, and `SKILL.md` holds the whole procedure | • 📐 **Sound:** clear phases, with one phase doing two jobs | • ✅ **Clean:** each phase does one job, and the detail lives in `reference/` |
| **Security** | • ⚠️ **Gaps:** posts or writes externally without a confirm step | • 🔒 **Confirmed:** a confirm step, but untrusted input isn't treated as data | • 🛡️ **Defended:** a confirm step, plus untrusted input handled as data throughout |
| **Standards Compliance** | • 📏 **Drift:** misses several hard gates | • ✅ **Mostly met:** one or two hard gates missed | • ✅ **All met:** every hard gate in `_hard_gates_checklist.md` passes |

- **~9 example:** `scorecard_claude_review_config.md` (9.4/10).
- **~7 example:** `scorecard_jira_create.md` (7.7/10), held back by missing adversarial-input evals.

---

## 📝 Rules

| Dimension | ~5 | ~7 | ~9 |
|---|---|---|---|
| **Token Cost Justification** | • 💸 **Unjustified:** always-on, but only one file type's sessions need it | • ⚖️ **Arguable:** always-on, and most sessions need it, but `applies_to` is unset | • ✅ **Justified:** loads only where its `applies_to` says it's needed |
| **Currency** | • 🍂 **Stale:** names a file or command that no longer exists | • 🔍 **Mostly current:** one reference out of date | • ✅ **Current:** every path and command it names exists today |
| **Structural Compliance** | • 📏 **Over length:** past 110 lines with no split, or no metadata header | • ✅ **Minor gaps:** within length, with a style slip such as a multi-sentence bullet | • ✅ **Clean:** passes `test_rules_structure.py` and the header tests with no style slips |

- **~9 example:** `scorecard_portable_paths.md` (9.4/10), backed by dated incidents.
- **~7 example:** `scorecard_automation_controls.md` (7.5/10).
- **~5 to 7 example:** `scorecard_makefile.md` (6.8/10), held back by a broken templates reference.

---

## 🤖 Agents

| Dimension | ~5 | ~7 | ~9 |
|---|---|---|---|
| **Scope Boundaries** | • 🔁 **Overlaps:** shares a job or a trigger with a skill or another agent | • ✅ **Distinct:** a distinct job, but the "not for" list misses a near neighbour | • ✅ **Fenced:** a distinct job, with every near neighbour named in "not for" |
| **Tool Safety** | • ⚠️ **Broad:** Bash or Write with no reason given, and no isolation | • 🔒 **Mostly scoped:** one tool more than the job needs | • 🔒 **Least privilege:** only the tools the job needs, plus worktree isolation if it writes |

- **~9 example:** `scorecard_code_reviewer.md` (8.9/10).
- **~8 example:** `scorecard_technical_writer.md` (8.1/10), held back by no record of use.
