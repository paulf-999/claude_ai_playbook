# Phase 2 — Confirm the plan, then execute

Nothing is committed, pushed or created until the user has approved both the PR title and the full plan.

## 2a — Title confirmation

Present the proposed PR title on its own, with nothing else:

> **Proposed PR title:**
> `<type(scope): plain English description>`
>
> `y` to confirm · `list` for alternatives · or type your own

Wait for the user's response before continuing.

- **`y`:** the title is confirmed, so go to 2b.
- **`list`:** generate 2–3 alternative phrasings with the same type and scope, present them numbered, and let the user pick one or type their own, then go to 2b.
- **Anything else:** treat the reply as the custom title, then go to 2b.

## 2b — Full plan

Present the full plan in this format:

```
Here is what I will run:

1. git checkout -b <branch_name>        # (omit if already on feature/hotfix branch)
2. git add <file1> <file2> ...
3. git commit -m "<commit message>"
4. git push -u origin <branch_name>
5. write the PR body to a temporary file
6. gh pr create --base main --title "<pr title>" --body-file <temp file> [--label "<label>"]

Commit message: <type(scope): imperative description>
PR title:       <type(scope): plain English description>

PR body:
---
<full PR body>
---
```

Wait for the user to confirm or request changes.

- **Confirm:** run the commands in order.
- **Request changes:** apply them, show the updated plan again and wait for approval.
- **Decline:** stop and run nothing, so no branch, commit or push is left behind.

## ⚙️ Execution rules

- **Verify each step:** after every git-mutating command, check it succeeded before running the next one.
- **Stop on failure:** if any step fails, stop and report the error, and never skip ahead.
- **Commit with a heredoc:** pass the message as `git commit -m "$(cat <<'EOF' … EOF)"` to preserve formatting.
- **Body from a file:** write the PR body to a temporary file and pass it with `--body-file`, never inline.
- **Pre-commit hooks:** report a hook failure clearly, and never retry with `--no-verify` unless the user explicitly asks.
- **Report the result:** finish with the new PR's number and URL.

## 🚨 Error recovery

| Failure | What to do |
|---|---|
| **Pre-commit hook fails** | Show the hook output, fix the reported issue if it is in the staged files, and ask before committing again. |
| **Hook modifies files** | Tell the user which files the hook changed, stage them by name and commit again. |
| **Push rejected** | Report the rejection (for example, the remote branch already exists or is ahead) and ask how to proceed rather than force-pushing. |
| **`gh` not logged in** | Stop before `gh pr create` and tell the user to run `gh auth login`; the branch is already pushed, so only the PR step remains. |
| **PR already exists for the branch** | Report the existing PR's URL instead of creating a second one. |
