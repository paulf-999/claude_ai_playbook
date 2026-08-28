---
created: 2025-10-01
last_modified: 2026-08-19
---

# ⚙️ Tier 2–3 Settings — Common & Niche Options

Detailed reference for Tier 2 (common) and Tier 3 (niche) `settings.json` configuration options. See the parent doc for Tier 1 essentials.

---

## 🔐 Permissions & security (Tier 2–3)

| Setting | What it does | Industry impact | Confidence | Philosophy fit | Verdict rationale |
|---|---|---|---|---|---|
| `permissions.ask` | Force a confirmation prompt for matched patterns | Tier 2 (~25 %) | ✅ | **Skip** | Git ops are allowed by design and gated via CLAUDE.md rules — an ask list re-introduces prompts that `allow` deliberately removes. |
| `permissions.additionalDirectories` | Extra dirs Claude may access beyond cwd | Tier 3 (~15 %) | 🟡 | **Skip** | Not found under this name in current docs; single-repo workflow doesn't need it. |

---

## 🧠 Model & cost (Tier 2–3)

| Setting | What it does | Industry impact | Confidence | Philosophy fit | Verdict rationale |
|---|---|---|---|---|---|
| `fallbackModel` | Model chain when primary is unavailable | Tier 3 | ✅ | **Skip** | No observed availability failures to solve. |
| `effortLevel` | Persistent reasoning effort (`low`…`xhigh`) | Tier 3 | ✅ | **Skip** | Real key (was assumed fabricated). Per-task effort is chosen live; a persistent floor fights the Haiku-default cost posture. |
| `alwaysThinkingEnabled` | Extended thinking on by default | Tier 3 | ✅ | **Skip** | Always-on thinking is a standing token cost with no measured payoff here. |
| `advisorModel` | Model for the server-side advisor tool | Tier 4 | ✅ | **Skip** | Real key. Specialist; no use case. |
| `env.MAX_THINKING_TOKENS` | Cap extended-thinking tokens | Tier 3 | ✅ | **Skip** | Useful only once thinking is enabled — not applicable. |

---

## 🗂️ Context & memory (Tier 2–3)

| Setting | What it does | Industry impact | Confidence | Philosophy fit | Verdict rationale |
|---|---|---|---|---|---|
| `cleanupPeriodDays` | Session-transcript retention (default `30`) | Tier 2 (~30 %) | ✅ | **Consider** | Turns an implicit default into a documented, auditable choice. Near-zero cost. Adopt with explicit evidence that you want a different value. |
| `autoCompactEnabled` / `autoCompactWindow` | Toggle + threshold for auto-compaction | Tier 3 | ✅ | **Skip** | Defaults work; no observed compaction problem to tune. |
| `env.CLAUDE_CODE_AUTO_COMPACT_WINDOW` | Env-var form of the compaction threshold | Tier 2 | ✅ | **Skip** | Real key (was assumed community-only). Duplicates `autoCompactWindow`; no need to tune either. |

---

## 🌱 Environment variables (Tier 2–3)

| Setting | What it does | Industry impact | Confidence | Philosophy fit | Verdict rationale |
|---|---|---|---|---|---|
| `env.DISABLE_TELEMETRY` | Disable telemetry collection | Tier 3 (~25 %) | ✅ | **Skip** | Privacy nicety; no recurring problem. Evidence-gated. |
| `env.DISABLE_NON_ESSENTIAL_MODEL_CALLS` | Suppress non-essential background API calls | Tier 3 | ✅ | **Skip** | Marginal token saving; not yet an observed cost driver. |
| `env.DISABLE_ERROR_REPORTING` | Disable error reporting | Tier 3 | ✅ | **Skip** | Privacy nicety; no problem to solve. |
| `env.MAX_MCP_OUTPUT_TOKENS` | Cap MCP tool response size | Tier 3 | ✅ | **Skip** | Real key. MCP is enabled per-session only — cap when a specific server floods context, not pre-emptively. |
| `env.BASH_DEFAULT_TIMEOUT_MS` | Default shell-command timeout | Tier 3 | ✅ | **Skip** | Real key. No recurring hung-command problem. |

---

## 🪝 Hooks (Tier 2)

| Setting | What it does | Industry impact | Confidence | Philosophy fit | Verdict rationale |
|---|---|---|---|---|---|
| `PreToolUse` | Run a hook before a tool call (e.g. block `rm -rf` / `.env` writes) | Tier 2 (~35 %) | ✅ | **Reject** | Hooks were deliberately removed (5000+ tokens/session, zero observed value). The destructive-op guard is better served by `permissions.deny` at zero context cost. |
| `PostToolUse` | Run a hook after a tool call (e.g. auto-format) | Tier 2 (~30 %) | ✅ | **Reject** | A silent formatter is the only tempting case — but pre-commit already covers formatting → fails the engineer test. |
| `disableAllHooks` | Kill-switch for all hooks + status line | Tier 4 | ✅ | **Skip** | No hooks registered, so nothing to disable. |

---

## 🎛️ UX / meta (Tier 2–3)

| Setting | What it does | Industry impact | Confidence | Philosophy fit | Verdict rationale |
|---|---|---|---|---|---|
| `statusLine` | Custom persistent status line (context %, model, branch…) | Tier 3 (~20 %) | ✅ | **Consider** | The one UX addition that directly serves "context efficiency is non-negotiable" — live context visibility. Adopt only if actually watched. Needs concrete evidence of use. |
| `showClearContextOnPlanAccept` | Offer to clear context on plan accept | Tier 3 | ✅ (live config) | **Have** | Set to `true`. Not in current docs table but working. |
| `outputStyle` | Named output rendering style | Tier 3 | ✅ | **Skip** | Default is fine; `writing_style.md` already governs output. |
| `editorMode` | `normal` / `vim` key bindings | Tier 3 | ✅ | **Skip** | Personal-preference chrome. |
| `theme` | Colour scheme | Tier 3 | ✅ | **Skip** | Personal-preference chrome. |
| `spinnerTipsEnabled` | Show spinner tips | Tier 4 | ✅ | **Skip** | Cosmetic. |

---

## 🔌 MCP (Tier 3)

| Setting | What it does | Industry impact | Confidence | Philosophy fit | Verdict rationale |
|---|---|---|---|---|---|
| `enableAllProjectMcpServers` | Auto-approve every project `.mcp.json` server | Tier 3 | ✅ | **Reject** | Auto-trusting arbitrary project servers conflicts with the MCP trust model and per-session enablement. |
| `enabledMcpjsonServers` | Approve specific `.mcp.json` servers | Tier 3 | ✅ | **Skip** | Real key. MCP is enabled per-session via `make enable_mcp` — no static allowlist wanted. |
| `disabledMcpjsonServers` | Reject specific `.mcp.json` servers | Tier 3 | ✅ | **Skip** | Same rationale as above. |

---

## 📊 Summary

**Tier 2 considerations:**
- `cleanupPeriodDays` — consider if you want explicit control over session-transcript retention
- `permissions.ask` — skip; conflicts with design choice to allow git operations
- Hooks — rejected; permission deny-list is more efficient

**Tier 3 recommendations:**
- `statusLine` — consider only if you actively watch live context usage
- Model tuning (`effortLevel`, `alwaysThinkingEnabled`) — skip; cost vs. per-task choice tradeoff
- Environment flags — skip; no recurring problems observed
- MCP settings — skip; per-session enablement covers the use case

---

## 🔗 Related docs

- **Parent (Tier 1 essentials):** `settings_json_recommendations.md`
- **Enterprise settings:** `_enterprise.md`
- **Official schema:** <https://code.claude.com/docs/en/settings>
