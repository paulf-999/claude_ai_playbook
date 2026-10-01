#!/bin/bash
# Pre-commit hook: Skill Authoring Gate (crawl + walk + run validation)
#
# Validates all skill changes against the three-level gate, all run by one linter:
# - Crawl (C0–C7), walk (W1–W6) and run (R2–R4) checks that fail a skill — BLOCK the commit
# - Walk and run checks that need a human to judge — WARN only and allow the commit
# - Complexity score per skill — BLOCKS the commit when too high for its maturity
#
# Exit code:
#   0 — no FAILs (WARNs are advisory)
#   1 — the linter or complexity scorer reports a FAIL (commit is blocked)

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"
export CLAUDE_CONFIG_DIR="${REPO_ROOT}/src/claude"
LINTER="$REPO_ROOT/src/sh/claude/skill_authoring_gate_lint.py"
COMPLEXITY_SCORER="$REPO_ROOT/src/claude/_scripts/skill_complexity_scorer.py"
SKILLS_ROOT="$REPO_ROOT/src/claude/skills"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏗️  Skill Authoring Gate — Pre-Commit Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Track exit codes
CRAWL_EXIT=0

# ── Crawl Level (C0–C7): Hard Gate ──────────────────────────────────────────

echo "📋 Running gate validation (crawl, walk and run + complexity)..."
echo ""

LINTER_EXIT=0
COMPLEXITY_EXIT=0

# Run linter
if [ -f "$LINTER" ]; then
    if python3 "$LINTER" "$SKILLS_ROOT" 2>&1; then
        echo "✅ Gate (crawl, walk, run): PASS — any WARN lines above are advisory"
        LINTER_EXIT=0
    else
        echo ""
        echo "❌ Gate (crawl, walk, run): FAIL — fix the FAIL lines above before committing"
        LINTER_EXIT=1
    fi
else
    echo "⚠️  Gate: linter not found at $LINTER — skipping"
    LINTER_EXIT=0
fi

echo ""

# Run complexity scorer on each skill
if [ -f "$COMPLEXITY_SCORER" ] && [ -d "$SKILLS_ROOT" ]; then
    echo "📊 Checking complexity scores..."
    for skill_dir in "$SKILLS_ROOT"/**/*/; do
        if [ -f "$skill_dir/skill.contract.yaml" ]; then
            skill_name=$(basename "$skill_dir")
            if ! python3 "$COMPLEXITY_SCORER" "$skill_dir" > /dev/null 2>&1; then
                echo "❌ Complexity check failed for $skill_name"
                COMPLEXITY_EXIT=1
            fi
        fi
    done
    if [ $COMPLEXITY_EXIT -eq 0 ]; then
        echo "✅ Crawl (complexity): PASS"
    else
        echo "❌ Crawl (complexity): FAIL — Reduce skill complexity or increase maturity tier"
    fi
else
    echo "⚠️  Crawl (complexity): Scorer not found — skipping"
    COMPLEXITY_EXIT=0
fi

# Overall crawl status
if [ $LINTER_EXIT -eq 0 ] && [ $COMPLEXITY_EXIT -eq 0 ]; then
    CRAWL_EXIT=0
else
    CRAWL_EXIT=1
fi

echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── Summary ────────────────────────────────────────────────────────────────

if [ $CRAWL_EXIT -eq 0 ]; then
    echo "✅ Gate (crawl, walk, run + complexity): PASS"
else
    echo "❌ Gate (crawl, walk, run + complexity): FAIL"
fi

echo ""

if [ $CRAWL_EXIT -eq 0 ]; then
    echo "✅ Commit: ALLOWED (no gate failures)"
    exit 0
else
    echo "❌ Commit: BLOCKED (fix the gate failures above)"
    exit 1
fi
