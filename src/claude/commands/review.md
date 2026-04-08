Review the current changes using the code-reviewer sub-agent.

Run `git diff` and `git diff --cached` to get the full diff of unstaged and staged changes. If there are no changes, check the most recent commit with `git diff HEAD~1 HEAD`.

Then review the changes for:
- Correctness and logic errors
- Compliance with project style guides (Python, SQL, bash) and rules
- Security concerns
- Test coverage gaps
- Unnecessary complexity

Lead with a summary verdict: approve, approve with suggestions, or request changes.
Group feedback by severity: blocking, recommended, optional.
