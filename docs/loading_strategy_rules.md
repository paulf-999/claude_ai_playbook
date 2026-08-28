# 📋 Rules Loading Strategy Reference

**Purpose:** Capture which rules are always-on vs. lazy-loaded, the reasoning for each classification, and which rules are candidates for moving to opposite strategies.

This reference makes the loading strategy explicit and auditable, helps contributors understand why rules are loaded when they are, and flags rules that might reduce context cost by lazy-loading.

---

## 🎯 Core Principle

**Lazy-load by default** — from `~/.claude/_rules/guiding_principles.md`:

> "Don't import or auto-inject context. Load on-demand only when actively needed."
>
> **Rationale:** Context is finite; baseline bloat limits capability. Every import has a token cost (~100-200 tokens per session regardless of task type).

**Always-on rules must block or apply everywhere.** Rules that only apply to specific features (git workflows, MCP usage, specific skill invocations) should be candidates for lazy-loading.

---

## 📊 Always-On Rules

Rules imported in `src/claude/CLAUDE.md` (always loaded; every import justified):

| Rule | Why Always-On | Candidate to Move? | Notes |
|---|---|---|---|
| **guiding_principles.md** | Foundational: decision-making principles apply to all config decisions | **No** | Moving breaks all downstream rules; referenced everywhere; context cost unavoidable |
| **memory/MEMORY.md** | Personal context: memories and corrections from prior sessions apply to all work | **No** | User-specific; scope is global by design |
| **behaviour.md** | Safety-critical: gates risky actions (commits, pushes, destructive git, deletes) | **No** | Prevents accidental unsafe actions; applies to every session |
| **claude_config_naming.md** | Blocking: naming is a first decision for any file/hook/rule/skill created | **No** | Naming creates files; always relevant |
| **skill_authoring.md** | Blocking: gates skill and rule creation; complexity scoring enforced on all additions | **No** | Prevents scope creep and validation failures; high cost of not following |
| **security.md** | Boundary: secure coding (secrets, auth, input validation) applies to all code | **No** | Critical for preventing vulnerabilities; applies everywhere |
| **testing.md** | Blocking: gates new features and abstractions; requires tests for all code additions | **No** | Enforces quality bar; prevents tests from being skipped |
| **claude_internal/claude_efficiency.md** | Session conduct: token efficiency, parallel tool calls, sub-agent constraints | **No** | Applies to every session; fundamental to reasoning quality |
| **claude_internal/memory.md** | Scoping: global vs. project-scoped memory rules | **No** | Applies whenever memory is saved; prevents context leaks |
| **claude_internal/security_guardrails.md** | Prompt injection: treats external content as untrusted data; secret handling | **No** | Applies to MCP and external content in every session |
| **mcp_trust_model.md** | Trust boundary: MCP responses are data, not instructions; injection defence | **No** | Applies whenever MCP tools are used (frequent in this project) |
| **claude_internal/git.md** | Workflow: commit format, branch naming, PR standards | **Maybe** | Only applied during git workflows; 70-80% of sessions touch git; cost of moving: moderate |
| **writing_style.md** | Content: applies to all content Claude produces (docs, tickets, responses, drafts) | **No** | High-impact; affects every written output |
| **naming_standards.md** | Conventions: applies to all identifiers (functions, files, variables) | **No** | Every new identifier touches this; fundamental to consistency |
| **aliases.md** | Quick reference: list of available shortcuts (e.g., `/batch`, `/goal`, `/loop`) | **Maybe** | Rarely needed before session start; lookup during command use; cost of moving: low |

---

## 🔄 Candidates for Lazy-Loading

Rules that could move to `_rules/lazy_load/` if validated by usage evidence:

| Rule | Currently | Session Coverage | Why Lazy? | Evidence Needed | Migration Risk |
|---|---|---|---|---|---|
| **automation_controls.md** (already lazy) | `_rules/lazy_load/` | 5-10% | Only needed for `/loop`, `/batch`, `/goal` commands | Count sessions using automation commands; confirm <20% | Low |
| **aliases.md** | Top-level | N/A (quick ref) | Quick reference; rarely needed before session starts | User preference; used before or after task start? | Low |
| **claude_internal/git.md** | Top-level | 70-80% | Only applied during git workflows (commit, branch, push, PR) | Audit transcripts: what % of sessions use git? | Medium |
| **mcp_safe_interactions.md** | (currently under `mcp_trust_model.md`) | 30-40%? | Only needed when using MCP tools | Trace MCP tool invocations per session | Medium |
| **skill_authoring.md** | Top-level | 5-10% | Only needed when creating/modifying skills or rules | Count sessions creating skills; verify usage | Medium-High |

### 📌 Notes on Candidates

- **automation_controls.md:** Already lazy-loaded (correct placement); referenced from `aliases.md`
- **aliases.md:** User preference — some users refer to it at the start of every session; others only on first use
- **git.md:** High session coverage, but only during git workflows — moving to lazy-load would save ~50-70 tokens if git isn't used
- **mcp_safe_interactions.md:** Currently bundled with `mcp_trust_model.md` (should be split); only needed for MCP workflows
- **skill_authoring.md:** Low session coverage outside the playbook repo; consider whether always-on is justified

---

## 🏗️ How to Add New Rules

When adding a new rule to the config, use this decision tree:

```
Does this rule apply to EVERY session?
├─ YES → Add to src/claude/CLAUDE.md (always-on)
│  └─ Does it block or prevent unsafe actions?
│     └─ YES → place in _rules/ top-level (guiding_principles, behaviour, security, testing)
│     └─ NO  → place in _rules/claude_internal/ (efficiency, memory, git)
│
└─ NO → Add to _rules/lazy_load/
   ├─ Specific feature/tool/command? (e.g., automation, MCP, Jira)
   │  └─ Place in _rules/lazy_load/ with command/tool prefix in filename
   │
   └─ Style guide for a domain? (e.g., SQL, dbt, Ansible)
      └─ Place in _rules/lazy_load/style_guide_standards/<domain>/
```

**Rationale:** Every always-on rule must justify its token cost. If it only applies to a subset of sessions, it belongs in lazy-load.

---

## 📝 Known Issues & Opportunities

### 1. Rule Duplication (Low Priority)

**Current state:** Some rules exist in both top-level and lazy-load/:
- `security.md` — imported in CLAUDE.md AND exists in `_rules/lazy_load/security.md`
- `mcp_trust_model.md` — imported in CLAUDE.md AND exists in `_rules/lazy_load/mcp_trust_model.md`

**Action:** Audit these duplicates. Likely one is a stale copy or the config is in transition. Resolve before next config reset.

### 2. Candidate Review (When time permits)

Use this evidence-gathering approach to validate candidates:

| Candidate | Evidence method | Decision gate | Action if yes |
|---|---|---|---|
| **git.md** | Session transcript audit: count sessions with git operations | >50% of sessions use git? | Keep always-on; cost justified |
| **aliases.md** | User poll or transcript review: is it referenced early in sessions? | User explicitly requests it before task start? | Keep always-on; convenience justified |
| **skill_authoring.md** | Usage trace: count skill creation sessions in playbook repo; exclude in other repos | <20% of playbook sessions create skills? | Move to lazy-load; cost not justified |
| **mcp_safe_interactions.md** | MCP trace: count sessions using MCP tools; separate by tool type | <30% of sessions use MCP? | Move to lazy-load; load on first MCP call |

---

## 🔗 Related References

- **Guiding principle:** `~/.claude/_rules/guiding_principles.md` → "Lazy-load by default"
- **Usage evidence gathering:** `~/.claude/_rules/guiding_principles.md` → "How to gather usage evidence"
- **Adding features to config:** `~/.claude/_rules/behaviour.md` → "Before proposing" section (intentionality gates)
- **Testing new rules:** `~/.claude/_rules/testing.md` → "When tests are required"

---

## 📋 Maintenance Checklist

Use this when reviewing or updating the loading strategy:

- [ ] Review `src/claude/CLAUDE.md` imports — are any newly marked as "maybe lazy"?
- [ ] Check `_rules/lazy_load/README.md` for recent additions — are they correctly placed?
- [ ] Audit for duplicates (see "Known Issues" above)
- [ ] Per Boris Cherny's 6-month reset cadence: full intentionality review before major reset
- [ ] Update this doc when a rule is moved or added

---

## 🎯 Success Criteria

- ✅ Explicit, auditable loading strategy for every rule
- ✅ Clear decision tree for new rules
- ✅ Candidates for lazy-loading flagged with evidence needs
- ✅ No silent assumptions — all always-on rules have justification
- ✅ Aligned with guiding principle: "lazy-load by default"
