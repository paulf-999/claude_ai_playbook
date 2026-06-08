## 🚀 Phase 2 — Present the plan and execute

### 2a — Title confirmation

Present the proposed PR title on its own — nothing else:

> **Proposed PR title:**
> `<type(scope): plain English description>`
>
> `y` to confirm · `list` for alternatives · or type your own

Wait for the user's response before continuing.

- **`y`** — title confirmed; proceed to Phase 2b.
- **`list`** — generate 2–3 alternative phrasings (same type and scope, different plain-English descriptions). Present them numbered. Ask the user to pick by number, or type their own. Once chosen, proceed to Phase 2b.
- **Anything else** — treat the response as the custom title. Proceed to Phase 2b.

### 2b — Full plan

Present the full plan to the user in this format:

```
Here is what I will run:

1. git checkout -b <branch_name>        # (omit if already on feature/hotfix branch)
2. git add <file1> <file2> ...
3. git commit -m "<commit message>"
4. git push -u origin <branch_name>
5. cat <<'EOF' >/tmp/pr_body.md
<full PR body>
EOF
6. gh pr create --base main --title "<pr title>" --body-file /tmp/pr_body.md [--label "<label>"]

Commit message: <type(scope): imperative description>
PR title:       <type(scope): plain English description>

PR body:
---
<full PR body>
---
```

Wait for the user to confirm or request changes before proceeding.

Once confirmed, execute the commands in sequence. After each git-mutating command, verify it succeeded before continuing. If any step fails, stop and report the error — do not skip ahead.

For the commit, use a heredoc to preserve formatting:
```
git commit -m "$(cat <<'EOF'
<commit message>
EOF
)"
```

Write the PR body to `/tmp/pr_body.md` before running `gh pr create`.

If pre-commit hooks fail, report the failure clearly. Do not retry with `--no-verify` unless the user explicitly instructs it.
