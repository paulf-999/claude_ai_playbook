# 🏆 Advanced

Practices for users running Claude regularly who want to scale across workstreams.

| Practice | Source | Description | Example |
|---|---|---|---|
| 🔀 Run sessions in parallel | Anthropic | Writer + reviewer pattern for independent critique, or parallel workstreams on isolated branches. | [reviewer prompt + worktree commands](#parallel-sessions) |

---

## 💻 Code examples

### 🔀 Parallel sessions

**Writer + Reviewer** — paste into a second Claude session once the writer has produced output:

```
You are a reviewer. The writer session is working on: [task description]

Review for:
- Correctness — logic errors, incorrect assumptions, broken dbt ref() calls
- Standards compliance — SQLFluff, naming conventions, DA_* audit fields present
- Completeness — anything missing from what was asked (e.g. missing dbt tests, missing limit_rows())

Group findings by severity: Blocking / Recommended / Optional.
Quote the relevant output and suggest the fix — don't just name the problem.
```

**Parallel workstreams with worktrees** — useful when developing two independent dbt features simultaneously without branch conflicts:

```bash
git worktree add ../dbt_project-feature-a feature/add_salesforce_mart
git worktree add ../dbt_project-feature-b feature/refactor_crm_staging
# Open Claude in each worktree directory separately
```
