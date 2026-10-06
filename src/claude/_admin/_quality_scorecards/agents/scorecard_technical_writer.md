# Quality Scorecard — technical_writer

**Date Created:** 2026-10-02
**Date Updated:** 2026-10-02

**Overall score:** 8.1/10

**Recommended improvements:**
- Record real uses of the agent, so its tactical maturity rests on evidence

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-02 | • 🔍 **Description:** says what it drafts, that it never publishes and which skills do<br>• 🎯 **Triggers:** a slash command plus four drafting phrases |
| **Scope Boundaries** | 9/10 | 2026-10-02 | • ✅ **Distinct job:** drafts only, while `git_create_pr` and `confluence_create_page` publish<br>• ✅ **Not-for list:** publishing, editing existing docs, ADRs, runbooks, READMEs and diagrams |
| **Complexity** | 8/10 | 2026-10-02 | • 🧮 **Raw complexity 2:** PR bodies and page text (Concepts 1), repo templates (Scope 1), no external services |
| **Evidence of Need** | 5/10 | 2026-10-02 | • ⚠️ **No record:** nothing documents how often it's used, although its maturity is tactical |
| **Test Coverage** | 8/10 | 2026-10-02 | • 📊 **Count:** 12 structured evals with assertions, within the tactical range<br>• ✅ **Boundaries:** covers the publishing hand-off and both declines<br>• ⚠️ **Not run:** nothing executes them yet |
| **Structural Compliance** | 9/10 | 2026-10-02 | • ✅ **Hard gates:** frontmatter, metadata header, all five sections, 57 lines and no future-version notes |
| **Tool Safety** | 9/10 | 2026-10-02 | • 🔒 **Allowlist:** Read, Grep, Glob and Write only, with no Bash or MCP<br>• ✅ **Isolation:** runs in a worktree |
| **Overall** | **8.1/10** | 2026-10-02 | • 💪 **Strongest:** Clarity, Scope Boundaries, Structural Compliance and Tool Safety (9/10)<br>• ⚠️ **Weakest:** Evidence of Need (5/10) |

## 🔗 Related files

- `src/claude/agents/core/technical_writer/AGENT.md` — the agent being scored
- `src/claude/agents/core/technical_writer/evals.yaml` — Test Coverage dimension
- `src/claude/skills/_git_skills/git_create_pr/SKILL.md` — Scope Boundaries dimension
- `src/claude/skills/_atlassian_skills/confluence_create_page/SKILL.md` — Scope Boundaries dimension
- `src/claude/_rules_lazy_load/authoring_agents/_hard_gates_checklist.md` — Structural Compliance dimension
