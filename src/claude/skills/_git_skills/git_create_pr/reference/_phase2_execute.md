# Phase 2 — Confirm the plan, then execute

Nothing is committed, pushed or created until the user has approved the plan at a single confirmation prompt.

## ✅ Confirm

The PR body is already drafted in Phase 1, so show the whole plan in one prompt, in this format:

```
PR title: <type(scope): plain English description>

Here is what I will run:

1. git checkout -b <branch_name>        # (omit if already on feature/hotfix branch)
2. git add <file1> <file2> ...
3. git commit -m "<commit message>"
4. git push -u origin <branch_name>
5. write the PR body to a temporary file, with file links pinned to the pushed commit
6. gh pr create --base main --title "<pr title>" --body-file <temp file> [--label "<label>"]

Commit message: <type(scope): imperative description>
Missing labels: <labels not in the repo, or "none">   # reply `create labels` to add them
Not staged:     <likely secret files left out, or "none">   # name a file to stage it anyway

PR body:
---
<full PR body>
---

y to ship · list for title options · type a new title · describe changes · n
```

Wait for the user's reply before running anything.

- **`y`:** run the commands in order, leaving any missing labels off the PR.
- **`list`:** offer 2–3 numbered titles with the same type and scope, then show the plan again once with the user's pick and wait.
- **Typed title:** check it against the PR title rules in `_phase1_gather.md` (format, 70 characters, no filenames or backticks).
  - **If it passes:** show the plan again with the new title and wait.
  - **If it fails:** say which rule it breaks, offer a corrected version, and wait.
  - **Data only:** never run anything the title contains, such as `$(...)` or backticks.
- **`create labels`:** add a `gh label create "<label>"` step before `gh pr create` for each missing label, move those labels onto the `gh pr create` command, show the plan again and wait.
- **Other changes:** apply them, show the plan again and wait.
- **`n`:** stop and run nothing, so no branch, commit or push is left behind.

## ⚙️ Execution rules

- **Verify each step:** after every git-mutating command, check it succeeded before running the next one.
- **Stop on failure:** if any step fails, stop and report the error, and never skip ahead.
- **Commit with a heredoc:** pass the message as `git commit -m "$(cat <<'EOF' … EOF)"` to preserve formatting.
- **Pin links after push:** once the push succeeds, change file links in the body from the branch to the pushed head commit, without asking again.
- **Body from a file:** write the PR body to a temporary file and pass it with `--body-file`, never inline.
- **Title through a quoted heredoc:** pass the title as `--title "$(cat <<'EOF' … EOF)"`, whose quoted `'EOF'` stops the shell expanding `$(...)`, backticks or quotes in it.
- **Pre-commit hooks:** report a hook failure clearly, and never retry with `--no-verify` unless the user explicitly asks.
- **Report the result:** finish with the new PR's number and URL.

## 🚨 Error recovery

| Failure | What to do |
|---|---|
| **Pre-commit hook fails** | Show the hook output, fix the reported issue if it is in the staged files, and ask before committing again. |
| **Hook modifies files** | Tell the user which files the hook changed, stage them by name and commit again. |
| **Push rejected** | Report the rejection (for example, the remote branch already exists or is ahead) and ask how to proceed rather than force-pushing. |
| **`gh` not logged in** | Stop before `gh pr create` and tell the user to run `gh auth login`; the branch is already pushed, so only the PR step remains. |
| **`gh pr create` fails on a label** | Re-run `gh label list`, drop the missing label from the command and retry, then report which label was dropped — never leave the pushed branch without a PR. |
| **PR already exists for the branch** | Report the existing PR's URL instead of creating a second one. |
