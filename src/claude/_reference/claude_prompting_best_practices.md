# 💬 Claude Prompting Best Practices

**Purpose:** Quick reference for 5 high-impact prompting techniques that improve clarity, reduce hallucination, and steer model behavior effectively.

---

## 🎯 The 5 Practices

### 1️⃣ Colleague Test

**Rule:** Before finalizing a prompt, show it to someone with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too.

**Why:** Prompts that seem clear in your head often contain hidden assumptions or ambiguous phrasing that only surface when another person tries to follow them.

**When to apply:**
- Before writing a complex multi-step prompt
- When instructions will be reused across sessions
- For automation scripts or CI/CD hooks where clarification isn't possible

**Example:**
- ❌ Poor: "Find the bug and fix it"
- ✅ Better: "Read `src/auth.js`, identify the line that compares plaintext passwords without hashing, write a test case that reproduces the bug, then fix it with bcrypt hashing"

---

### 2️⃣ Frame as Positive Actions, Not Negations

**Rule:** Tell Claude what to do instead of what not to do — this reliably steers output better.

**Why:** Negations ("don't use X") are parsed as permissions to consider X, then ignore it. Positive framings ("use Y") skip the consideration step and go straight to execution.

**When to apply:**
- When specifying formatting or style
- When preventing common failure modes
- In any directive that might otherwise generate the undesired behavior

**Example:**
- ❌ "Do not use excessive markdown"
- ✅ "Write in flowing prose paragraphs with complete sentences"

**Another example:**
- ❌ "Don't overthink this"
- ✅ "Use a straightforward, direct approach without exploring edge cases"

---

### 3️⃣ Tune Exploration for Current Models

**Rule:** Newer models explore more than older ones by default. Replace blanket "be thorough" defaults with targeted instructions.

**Why:** Modern models (Opus, Sonnet) tend to over-explore, spawning unnecessary agents or tools when simple direct approaches would suffice. Haiku under-explores and needs explicit encouragement.

**When to apply:**
- When using latest models (Opus 4.8+, Sonnet 5+)
- For time-sensitive or cost-conscious tasks
- When you want a specific behavior, not "explore and decide"

**Example:**
- ❌ "Default to using [tool]" (causes overtriggering with newer models)
- ✅ "Use [tool] when it would enhance understanding of the problem"

---

### 4️⃣ Never Speculate About Code

**Rule:** Always read a file before editing or answering questions about it. Never make claims about code, file structure, or behavior without opening it first. If the user references a specific file or function, you MUST read it before answering. Grounded, hallucination-free answers only.

**Why:** Code hallucination — claiming a function exists, a file is structured a certain way, or a pattern is used — is a silent failure mode that wastes time and erodes trust.

**When to apply:**
- Every time a user references a specific file or function
- Before suggesting code changes
- Before answering "does this function exist?" or "how is this structured?"

**Example:**
- ❌ "That function probably takes a callback parameter"
- ✅ Read the file first, then: "The function takes a Promise, not a callback"

---

### 5️⃣ When NOT to Spawn Subagents

**Rule:** Avoid subagents for single-file edits, sequential operations, or simple tasks where you need to maintain context across steps. Work directly instead. Subagents are for parallelism or context isolation, not brevity.

**Why:** Subagents lose context — each agent starts fresh. Context loss compounds across sequential steps, making the overall task slower and requiring extra work to thread state between agents.

**When to apply:**
- Single-file edits → work directly
- Multi-step operations that depend on each other → work directly
- Tasks where you need to inspect output before the next step → work directly
- Only use subagents when genuinely parallelizing independent work or isolating large reads

**Example:**
- ❌ Spawn Agent to read file A, then spawn another to edit it
- ✅ Read file A yourself, then edit it directly

**Good use of subagents:**
- Parallel finders scanning different code sections concurrently
- Isolating a 50K-token code review from the main window
- Independent research tasks with no shared context

---

## 🔗 Related Rules

These practices are integrated into the global Claude config:

- **`behaviour.md`** — "colleague test", "never speculate about code", "tune exploration"
- **`writing_style.md`** — "frame as positive actions"
- **`claude_efficiency.md`** — "when NOT to spawn"

For the full rules and additional context, see `~/.claude/_rules/`.

---

## 📚 External References

- **Official Claude Prompt Engineering Guide:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices — Anthropic's official documentation on prompt engineering best practices

---

## ✅ Implementation Checklist

When crafting a prompt:

- [ ] **Colleague test:** Could someone unfamiliar with the task follow this prompt?
- [ ] **Positive framing:** Am I telling Claude what to do, not what to avoid?
- [ ] **Model-appropriate:** Is my "explore" request matched to the model I'm using?
- [ ] **No speculation:** Am I claiming anything about code without reading it?
- [ ] **Right tool:** Am I using subagents only for parallelism or context isolation?

---

Last updated: **2026-08-19**
