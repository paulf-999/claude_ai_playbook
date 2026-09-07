# Examples — Setup Scenarios

## Single Developer Setup

**Scenario:** Developer working on a single project repository.

```bash
cd ~/git_repos/core/my-project
/claude_setup_graphify

# Pre-flight: ✓ git, ✓ Python 3.8+, ✓ writable
# Phase 1: ✓ graphifyy installed
# Phase 2: ✓ graph extracted
# Phase 3: ✓ .gitignore updated
# Phase 4: ✓ CLAUDE.md updated
# Phase 5: ✓ /graphify callable

# Now ask questions without reading files:
$ /graphify "What functions call user_authentication()?"
# → Returns: Found in models/auth.py (3 calls), utils/helpers.py (1 call)
```

## Team Repository Setup

**Scenario:** Team shared repo, all developers need the same graph.

```bash
cd ~/git_repos/core/team-project
/claude_setup_graphify

# All 5 phases complete successfully

# Commit and push:
git add .gitignore CLAUDE.md graphify-out/graph.json
git commit -m "feat: add Graphify knowledge graph for structural queries"
git push origin feature/add-graphify

# Team members:
cd team-project
/claude_setup_graphify --skip-extract  # graph.json in repo

# All can now query the graph locally
```

## Verification Checklist

After setup, verify with:

```bash
ls -lh graphify-out/graph.json  # Check size (50KB-500KB typical)
/graphify "List Python files"   # Test skill works
grep graphify-out/ .gitignore   # Verify entry
grep "## Graphify" CLAUDE.md    # Verify CLAUDE.md updated
```
