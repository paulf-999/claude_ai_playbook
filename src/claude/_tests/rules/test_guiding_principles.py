"""Tests for guiding_principles.md enforcement.

Validates that lazy-load and context-efficiency principles are being followed:
- Lazy-load by default: no lazy_load/ files imported in CLAUDE.md
- Explicit over implicit: all imports have clear purpose comments
- Intentionality gates everything: every import in CLAUDE.md is documented
"""
import re
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
CLAUDE_MD = CLAUDE_DIR / "CLAUDE.md"
LAZY_LOAD_DIR = CLAUDE_DIR / "_rules/lazy_load"


def test_no_lazy_load_imports_at_top_level():
    """Lazy-load files must not be imported in CLAUDE.md — they're loaded on demand.

    This validates the "lazy-load by default" principle: CLAUDE.md should only
    import critical rules needed every session. Domain-specific rules go in
    lazy_load/ and are read on-demand via hooks or agent initialization.
    """
    claude_content = CLAUDE_MD.read_text()

    # Find all @import references
    imports = re.findall(r"@~/.claude/(.+?)(?:\s|$)", claude_content)

    # Check that none reference lazy_load/
    lazy_load_imports = [imp for imp in imports if imp.startswith("_rules/lazy_load/")]

    assert not lazy_load_imports, (
        f"CLAUDE.md imports lazy_load files (violates lazy-load principle): "
        f"{lazy_load_imports}. Move these to on-demand loading via hooks."
    )


def test_all_imports_have_purpose_comments():
    """Every import in CLAUDE.md must have a preceding comment explaining why.

    This validates the "explicit over implicit" principle: future maintenance
    depends on understanding why each import exists, not guessing.
    """
    claude_content = CLAUDE_MD.read_text()

    # Pattern: expect <!-- comment --> on the line before @import
    lines = claude_content.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("@"):
            # Check if previous non-empty line is a comment
            prev_idx = i - 1
            while prev_idx >= 0 and lines[prev_idx].strip() == "":
                prev_idx -= 1

            if prev_idx >= 0:
                prev_line = lines[prev_idx].strip()
                assert prev_line.startswith("<!--"), (
                    f"Line {i+1}: Import '{line}' lacks a purpose comment. "
                    f"Add a <!-- comment --> on the preceding line explaining why this import exists."
                )


def test_no_speculative_imports():
    """No imports added without evidence they solve a real, recurring problem.

    This validates "intentionality gates everything" — every import in CLAUDE.md
    must justify its token cost. If you can't articulate the problem it solves,
    it doesn't belong at the top level.
    """
    # This test is manual/observational: audit each import against its comment.
    # Automated detection is impractical, but the purpose-comment test above
    # ensures each import can be evaluated.

    # For now, verify that the count of imports is reasonable (< 20).
    claude_content = CLAUDE_MD.read_text()
    imports = re.findall(r"^@~/.claude/", claude_content, re.MULTILINE)

    assert len(imports) < 20, (
        f"CLAUDE.md has {len(imports)} imports. This is high and suggests "
        f"speculative bloat. Review each import: does it solve a real, recurring problem?"
    )
