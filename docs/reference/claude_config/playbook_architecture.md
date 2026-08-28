# 🏗️ Playbook Architecture & Design Patterns

**Purpose:** Reference guide to the playbook's structural and design decisions. Use when understanding how rules, skills, and config components fit together — or when deciding where to add new features.

> **Complements Graphify:** Graphify answers "where is X?" (structural navigation). This doc answers "why is it organized this way?" and "what patterns govern decisions?"

---

## 📐 Three-Layer Rule Structure

All rules live in `src/claude/_rules/` with three tiers:

### 1️⃣ Always-on (Imported in CLAUDE.md)

**Directory:** `_rules/01_essentials/` and `_rules/02_claude_internal/`

**Cost:** Every rule consumes 100-200 tokens per session, regardless of task type.

**What goes here:**
- **01_essentials/** — Principles and safe-guards that apply to every session:
  - `guiding_principles.md` — Meta-principles (lazy-load, intentionality, goal-driven design, automation ROI)
  - `behaviour.md` — Safety defaults (don't assume, ask clarifying questions, risky actions gate)
  - `security.md` — Secure coding (secrets, input validation, dependencies)
  - `testing.md` — Test requirements (every new code artifact needs tests)
  - `writing_style.md` — Style for all content Claude produces
  - `naming_standards.md` — Naming conventions (files, functions, rules, hooks)

- **02_claude_internal/** — Session conduct and Claude-specific behaviors:
  - `claude_efficiency.md` — Token efficiency (parallel calls, no redundant reads, sub-agent constraints)
  - `git.md` — Git workflow (commits, branches, PRs, safe patterns)
  - `security_guardrails.md` — Prompt injection defence, secret handling

**Rule of thumb:** If the rule applies to EVERY session regardless of project type, it belongs here.

### 2️⃣ Lazy-Load (Never Imported, Read on Demand)

**Directory:** `_rules/03_lazy_load/`

**Cost:** Zero tokens unless explicitly loaded during a session.

**What goes here:**
- Domain-specific rules (SQL, dbt, Terraform, Ansible)
- Technology-specific style guides
- Project-specific patterns
- Anything that applies to < 50% of sessions

**Rule of thumb:** If the rule only matters when working in a specific domain, it belongs here.

### 3️⃣ Project-Scoped (In repo's own CLAUDE.md)

**Location:** Each repo's `CLAUDE.md` file (e.g., `dbt/CLAUDE.md`)

**Cost:** Imported only when working in that repo.

**What goes here:**
- Repo-specific workflows and gotchas
- Team conventions for that codebase
- Build/test commands, dependencies, structure

---

## 🎯 Key Design Decisions & Patterns

### Pattern 1: Lazy-Load by Default

**Decision:** Domain-specific rules go in `03_lazy_load/`, not imported.

**Why:**
- Baseline context bloat limits reasoning capability
- You don't need dbt rules when working on frontend code
- A 6-month config can accumulate 20+ rules; importing all of them kills context

**How it works:**
- Always-on imports consume token budget immediately
- Lazy-load rules sit on disk, read only when needed
- **Reference:** Use `/doctor` or search `03_lazy_load/` when you need domain guidance

**Gotcha:** Lazy-load is "lean by default, load on demand" — not "magic auto-loading." You must actively reference lazy-load rules when they're relevant.

### Pattern 2: Goal-Driven Design (Principle B)

**Decision:** Align config to current work goals, ruthlessly prune during resets.

**Why:**
- Config designed for "all scenarios" becomes noise
- 6-month resets are opportunities to re-align
- Unused rules waste tokens and context

**How it works:**
- Every 6 months (per Boris Cherny), archive and reset `~/.claude/`
- During reset: audit every rule — "Does this serve my current work?"
- Keep only what's actively needed; move the rest to lazy-load or archive

**Gotcha:** Don't mistake "comprehensive" for "good." Lean config beats complete config.

### Pattern 3: Automation ROI (Principle C)

**Decision:** Only automate (hooks, skills, commands) when cost is justified by frequency.

**Why:**
- Not everything should be automated
- A $5 hook that saves 5 min/month costs more than manual
- Automation has hidden costs: maintenance, testing, registration

**How it works:**
- **Manual < 10 min?** → Stay manual
- **Automation setup time + API cost > savings?** → Not ROI-positive
- **Hook used 5+ times/month?** → Likely ROI-positive
- **Hook used < monthly?** → Probably not

**Example:** A pre-commit hook that formats code might save 2 min/month. Setup cost (dev + registration + testing) = 1 hour. ROI payback = ~30 months. Stay manual.

**Gotcha:** Automation convenience ≠ automation value. Calculate actual ROI before adding hooks/skills.

---

## 🔄 Common Workflows

### Adding a New Rule

1. **Decide tier:** Does it apply to every session (01_essentials/02_claude_internal), or just some domains (03_lazy_load)?
2. **Name it:** Use snake_case, prefix if grouping (e.g., `style_guide_sql.md`)
3. **Write it:** Follow template (H1 emoji, ~100 lines, **keyword:** bullets)
4. **Import it:** If always-on, add `@import` to CLAUDE.md
5. **Document it:** Update relevant README or docs

### Adjusting Lazy-Load Strategy

- Rule is never used? Move to archive or delete
- Rule is needed in < 25% of sessions? Keep in lazy-load
- Rule applies to every session? Move to 01_core (rare)

### Deciding: Automation vs. Manual

Use Principle C decision tree:
1. **Frequency:** How many times/month is this task done?
2. **Manual cost:** How long (minutes) does it take manually?
3. **Automation cost:** Setup time (hours) + monthly API cost ($)
4. **Payback period:** (automation cost) / (frequency × manual time / 60)
5. **If payback < 6 months → automate; else → manual**

---

## 📚 Related Docs

- **Graphify:** Structural queries — where is X defined, which files reference Y
- **Loading Strategy (lazy_load_candidates.md):** Detailed evidence for each candidate rule
- **Guiding Principles:** Meta-level: intentionality, goal-driven design, automation ROI
