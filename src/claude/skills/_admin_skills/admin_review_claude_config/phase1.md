# Phase 1: Scoring Themes & Artefacts

## 📂 Artefacts to read

Read the following before scoring. All paths are under `~/.claude/`.

| Artefact | Path |
|---|---|
| Global CLAUDE.md | `~/.claude/CLAUDE.md` |
| Memory index | `~/.claude/memory/MEMORY.md` |
| Behaviour rules | `~/.claude/_rules/behaviour.md` |
| Security rules | `~/.claude/_rules/security.md` |
| Naming standards | `~/.claude/_rules/naming_standards.md` |
| Writing style | `~/.claude/_rules/writing_style.md` |
| Claude internal index | `~/.claude/_rules/claude_internal/README.md` |
| Efficiency rules | `~/.claude/_rules/claude_internal/claude_efficiency.md` |
| Memory scoping rules | `~/.claude/_rules/claude_internal/memory.md` |
| Security guardrails | `~/.claude/_rules/claude_internal/security_guardrails.md` |
| Git rules | `~/.claude/_rules/claude_internal/git.md` |
| Aliases | `~/.claude/aliases.md` |
| Settings (hooks + permissions) | `~/.claude/settings.json` |
| Lazy load index | `~/.claude/_rules/lazy_load/` (list only, do not read children) |
| Tests directory | `~/.claude/_tests/` (list only, do not read test files) |
| Memory files | `~/.claude/memory/` (list all files) |

Use `bash ls` calls for directory listings. Read file content only for the paths listed above — do not recursively read all files.

---

## 📊 Scoring themes

Score each theme from 1–10 using the scale below. Adapt the theme lens to config quality, not code quality.

| Score | Meaning |
|---|---|
| 9–10 | Excellent — sets the bar |
| 7–8 | Good — meets the bar with minor gaps |
| 5–6 | Acceptable — works but has notable gaps |
| 1–4 | Needs work — significant issues |

### Theme definitions

| Theme | Config interpretation |
|---|---|
| 💻 **Rule quality** | Clarity, specificity, actionability, DRY — no duplicate guidance across files; rules use consistent formatting (emoji headings, bold-keyword bullets, Note: callouts); rationale is present where non-obvious |
| 🔀 **Config complexity** | Import chain depth, cognitive load to navigate, file sizes vs. the 100-line limit, relay files that add indirection without content, files that mix unrelated concerns |
| 🧪 **Testing** | Test coverage in `_tests/` for hooks and rules; whether enforcement hooks have corresponding tests; whether the "rules require tests" rule is self-consistently followed |
| 🔒 **Security posture** | Security rules present and separated by concern (coding standards vs. Claude's own conduct); prompt injection defence; MCP response trust model; secret handling; least privilege |
| 📝 **Documentation** | READMEs for each artefact group; MEMORY.md index is populated and curated; rationale is included in rules where non-obvious; `_wip/` directories are explained |
| 📐 **Standards adherence** | Naming conventions followed and hook-enforced; files within line limits; import pattern consistent (`@` references, no inline duplication); emoji/bold-keyword style applied uniformly |

---

## 📈 Grade mapping

**Overall score:** average of the six theme scores, rounded to one decimal place.

| Score | Grade |
|---|---|
| 9.5–10 | A+ |
| 9.0–9.4 | A |
| 8.5–8.9 | A− |
| 8.0–8.4 | B+ |
| 7.5–7.9 | B |
| 7.0–7.4 | B− |
| 6.5–6.9 | C+ |
| 6.0–6.4 | C |
| 5.5–5.9 | C− |
| 5.0–5.4 | D+ |
| 4.0–4.9 | D |
| < 4.0 | F |
