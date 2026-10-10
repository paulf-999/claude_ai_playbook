<!-- version: 3.0.1 -->
<!-- created: 2026-09-18 -->
<!-- updated: 2026-09-29 -->
# 🚪 Scope Boundaries & Low-Maintenance Design

**Purpose:** Every skill must declare what it does NOT do, and be designed to stay stable once shipped.

---

## 🚪 Scope Boundaries [REQUIRED]

Every skill must explicitly declare what it does AND what it does NOT do. This prevents feature creep and sets user expectations upfront.

**In `skill.contract.yaml`, list them under `dispatch.not_for` — example (git_create_pr):**
```yaml
not_for:
  - complex merge conflict scenarios
  - non-main branch PRs
  - release branch workflows (v2.0+)
```

**In SKILL.md's Best For line, explain why:**
- Why these boundaries? (design choice? technical limitation? future roadmap?)
- What would v2.0 add?
- What's the tradeoff? (keeps skill lean vs. limits applicability)

### Anti-Patterns: What NOT to Do

**❌ Don't try to handle everything**
- A skill that handles "all Confluence page operations" becomes bloated and unmaintainable
- Better: narrow scope (e.g., `confluence_create_page`, `confluence_update_page` as separate skills)
- Use `not_for` to document explicit boundaries

**❌ Don't substitute `test_*_handler.py` for `evals.yaml` — match the test type to what's being tested**
- `evals.yaml` is mandatory for every skill — it specifies the skill's prompt-driven behavior (what Claude should do reading `SKILL.md`), which isn't automatable in this repo's tooling since nothing invokes a live Claude session to grade it
- `test_<handler>.py` (pytest) is a welcome *addition*, not a replacement, when a skill ships deterministic Python code (an MCP handler, validation logic) — automate what's automatable, since pytest runs unattended in pre-commit/CI
- The anti-pattern is skipping `evals.yaml` in favour of pytest, not writing pytest at all — a skill with real code should have both; a skill that's pure prompt-following logic only needs `evals.yaml`

---

## 🛠️ Low-Maintenance Design [CRITICAL]

Design skills to be stable and self-contained, so they rarely need changing.

- **Design for immutability:** once v1.0 ships, assume it won't need changes.
  - **Note:** a new capability is a new skill with its own name, not an update to the old one.
- **Isolate dependencies:** no skill-to-skill calls, and prefer local-only over API-dependent.
- **Battle-tested tools only:** proven APIs such as GitHub or Slack, never experimental tools.
- **Freeze scope with `not_for`:** document any v2.0 ideas separately, not in the v1.0 contract.
- **Evals are the contract:** run `evals.yaml` before any update, and don't merge if they break.
