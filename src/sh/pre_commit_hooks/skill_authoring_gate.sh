#!/bin/bash
# Pre-commit hook: Skill Authoring Gate (crawl + walk + run validation)
#
# Validates all skill changes against the three-level gate:
# - Crawl (C0–C7): Foundation criteria — BLOCKS commit on failure
# - Walk (W1–W6): Quality criteria — WARNS on failure but allows commit
# - Run (R1–R5): Comprehensive criteria — WARNS on failure but allows commit
#
# Exit code:
#   0 — all levels pass (or crawl passes + walk/run are warnings only)
#   1 — crawl level FAILS (commit is blocked)

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"
LINTER="$REPO_ROOT/src/sh/claude/skill_authoring_gate_lint.py"
COMPLEXITY_SCORER="$REPO_ROOT/src/sh/claude/skill_complexity_scorer.py"
TEST_SUITE="$REPO_ROOT/src/claude/_tests/rules/test_skill_authoring_gate.py"
SKILLS_ROOT="$REPO_ROOT/src/claude/skills"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏗️  Skill Authoring Gate — Pre-Commit Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Track exit codes
CRAWL_EXIT=0
WALK_EXIT=0

# ── Crawl Level (C0–C7): Hard Gate ──────────────────────────────────────────

echo "📋 Running Crawl validation (C0–C7 + complexity)..."
echo ""

LINTER_EXIT=0
COMPLEXITY_EXIT=0

# Run linter
if [ -f "$LINTER" ]; then
    if python3 "$LINTER" "$SKILLS_ROOT" 2>&1; then
        echo "✅ Crawl (structure): PASS"
        LINTER_EXIT=0
    else
        echo ""
        echo "❌ Crawl (structure): FAIL — Fix these errors before committing"
        LINTER_EXIT=1
    fi
else
    echo "⚠️  Crawl (structure): Linter not found at $LINTER — skipping"
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

# ── Walk Level (W1–W6) and Run Level (R1–R5): Warnings ──────────────────────

echo "📋 Running Walk/Run validation (W1–W6, R1–R5)..."
echo ""

if [ -f "$TEST_SUITE" ]; then
    # Run tests, capture output but don't fail on non-zero exit
    if python3 -m pytest "$TEST_SUITE" -v --tb=short 2>&1; then
        echo ""
        echo "✅ Walk/Run: PASS"
        WALK_EXIT=0
    else
        echo ""
        echo "⚠️  Walk/Run: WARNINGS detected — fix before code review"
        # Don't fail the commit; these are advisory
        WALK_EXIT=0
    fi
else
    echo "⚠️  Walk/Run: Test suite not found at $TEST_SUITE — skipping"
    WALK_EXIT=0
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── Summary ────────────────────────────────────────────────────────────────

if [ $CRAWL_EXIT -eq 0 ]; then
    echo "✅ Crawl (C0–C7):   PASS"
else
    echo "❌ Crawl (C0–C7):   FAIL"
fi

if [ $WALK_EXIT -eq 0 ]; then
    echo "✅ Walk/Run (W/R):  PASS or WARNINGS (address before review)"
else
    echo "⚠️  Walk/Run (W/R):  WARNINGS (address before review)"
fi

echo ""

if [ $CRAWL_EXIT -eq 0 ]; then
    echo "✅ Commit: ALLOWED (crawl criteria passed)"
    exit 0
else
    echo "❌ Commit: BLOCKED (fix crawl errors above)"
    exit 1
fi
