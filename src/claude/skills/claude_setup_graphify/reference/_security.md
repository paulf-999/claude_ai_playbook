# Security Measures

**Input Validation:**
- Path traversal: Reject ".." escapes, absolute paths, invalid characters
- Shell injection: Quote all variables, validate character sets
- Examples: `if [[ "$dir" == *".."* ]]; then error; fi`

**File Permissions:**
- Check not world-writable: `.gitignore`, `CLAUDE.md` should be 600 or 644 max
- Safe creation: `umask 0077` before creating files
- Post-verify: `chmod 600 graphify-out/graph.json`

**Symlink Safety:**
- Detect symlinks: `if [ -L .gitignore ]; then error; fi`
- Prevents directory escape attacks on critical files

**Git Repository:**
- Verify repo: `git rev-parse --git-dir`
- Check ownership: `.git` directory owned by user
- Warn on detached HEAD (unusual state)

**Backup & Rollback:**
- Pre-backup critical files before modifications
- Atomic rollback on failure: restore from backup, exit cleanly
- Enables safe retry without corruption

**Isolation Boundaries:**
- Stay in repo root: `REPO_ROOT=$(git rev-parse --show-toplevel)`
- No parent dir access: reject "..", "../.."
- No sudo: `if [ "$EUID" -eq 0 ]; then error; fi`
- Only modify repo files, not system files

**Data Integrity:**
- JSON validation: `jq empty graphify-out/graph.json`
- Verify required fields: nodes, edges, metadata present
- File size check: >1KB, <500MB (sanity bounds)
- Checksums: md5sum before/after modifications

**Audit Checklist** (post-setup verification):
- No symlinks: `ls -lh | grep "^l"`
- Safe permissions: `stat -c '%A'` shows 600 or 644
- Valid JSON: `jq empty` succeeds
- Git clean: `git status` shows no unexpected changes
- Repo isolation: in git root, not outside bounds
