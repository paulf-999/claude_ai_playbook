# Quality Scorecard — technical_writer

**Date Created:** 2026-10-02
**Date Updated:** 2026-10-02

**Overall score:** 6.0/10

**Recommended improvements:**
- Add a `tools:` allowlist to the frontmatter, limited to reading files and the Confluence tools it needs
- Decide how it relates to the `git_create_pr` and `confluence_create_page` skills, then narrow its scope or hand off to them
- Record real uses of the agent, or downgrade its maturity from tactical
- Rewrite the evals as structured name, input, setup and expected-output fields, per the hard gates
- Drop the GitHub MCP requirement, because the PR template is a local file

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-02 | • 🔍 **Description:** says what it drafts, when to use it and what it isn't for<br>• 🎯 **Triggers:** a slash command plus four natural phrases |
| **Scope Boundaries** | 5/10 | 2026-10-02 | • ✅ **Not-for list:** explicit in both "When to use" and "Constraints"<br>• ⚠️ **Overlap:** `git_create_pr` already drafts PR bodies, and `confluence_create_page` already creates pages |
| **Complexity** | 6/10 | 2026-10-02 | • 🧮 **Raw complexity 4:** PR bodies and Confluence pages (Concepts 1), repo templates (Scope 1), Atlassian and GitHub MCP (Dependencies 2) |
| **Evidence of Need** | 5/10 | 2026-10-02 | • ⚠️ **No record:** nothing documents how often it's used, although its maturity is tactical |
| **Test Coverage** | 6/10 | 2026-10-02 | • 📊 **Count:** 12 scenarios, matching the tactical range of 8–12<br>• ⚠️ **Format:** prose headings with no setup field, and nothing runs them |
| **Structural Compliance** | 7/10 | 2026-10-02 | • ✅ **Basics:** frontmatter, metadata header and all five sections<br>• ⚠️ **Length:** 68 lines, over the 40–60 target<br>• ⚠️ **Version notes:** "v1.0" labels on constraints read as plans for later versions |
| **Tool Safety** | 5/10 | 2026-10-02 | • ✅ **Isolation:** runs in a worktree<br>• ⚠️ **No allowlist:** without `tools:` it can use every tool, including Bash and Write |
| **Overall** | **6.0/10** | 2026-10-02 | • 💪 **Strongest:** Clarity (8/10)<br>• ⚠️ **Weakest:** Scope Boundaries, Evidence of Need and Tool Safety (5/10) |

## 🔗 Related files

- `src/claude/agents/core/technical_writer/AGENT.md` — the agent being scored
- `src/claude/agents/core/technical_writer/evals.yaml` — Test Coverage dimension
- `src/claude/skills/_git_skills/git_create_pr/SKILL.md` — Scope Boundaries dimension
- `src/claude/skills/_atlassian_skills/confluence_create_page/SKILL.md` — Scope Boundaries dimension
- `src/claude/_rules/03_authoring_guidelines/authoring_agents/_lazy_load/_hard_gates_checklist.md` — Structural Compliance dimension
