# 🛠️ claude_kaizen — Implementation

**Purpose:** How the audit, promotion, validation and pruning phases work, in order.

`<config-dir>` below means `$CLAUDE_CONFIG_DIR`, or `~/.claude` when it's unset.

---

## 1️⃣ Audit

- **Source:** read the error logs in `~/claude/_errors/`.
- **Missing folder:** if `~/claude/_errors/` doesn't exist or is empty, say so and stop, without proposing any rule.
- **Patterns:** group logs that describe the same mistake, such as missing input validation.

## 2️⃣ Track candidates

- **Ledger:** each pattern has a row in `<config-dir>/_rules/learned/candidates.md` with its occurrence count.
- **Update:** add new patterns at count 1, and increase the count of ones seen again.
- **Threshold:** a pattern is promoted only once its count reaches **2**.
- **Below threshold:** record it, and tell the user it will be promoted if it recurs.

## 3️⃣ Draft

- **Rule:** for each candidate at the threshold, draft one rule in `authoring_rules.md` style.
- **Eval case:** draft a matching case for `evals/claude_ai_playbook.yaml`, with `must_match` and `must_not_match` regexes that prove the rule works.

## 4️⃣ Validate

- **Cost first:** `evals/runner.py` makes one headless Claude call per case, so tell the user before running it.
- **Before:** `python evals/runner.py --before evals/claude_ai_playbook.yaml`
- **After:** apply the draft to a copy of the config, then `python evals/runner.py --after --config-dir <copy> evals/claude_ai_playbook.yaml`
- **Login:** the runner builds a private throwaway config that links the rules under test and your existing login, so headless Claude stays signed in.
- **Regression:** if any case that passed before now fails, name it in the proposal and don't recommend approving the rule.

## 5️⃣ Propose

- **Diff only:** show the new rule, its eval case and the before/after results as a diff.
- **Approval:** write to `<config-dir>/_rules/learned/` only after an explicit yes.
- **Declined:** leave `_rules/learned/` unchanged and confirm that nothing was applied.

## 6️⃣ Prune

- **Stale rules:** list learned rules older than 6 months with their last validation date.
- **Never remove:** suggest re-validating them, but don't delete or edit them.

---

## 🚫 Out of scope

- **Cross-repo promotion:** planned for v2 (see `_roadmap.md`), so offer to run the audit for the current repo only.
- **Auto-apply and bulk removal:** every change goes through a reviewed diff.
