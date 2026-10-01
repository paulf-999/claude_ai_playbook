# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-01
# Version:           2.0.1
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests the confluence_create_page handler's input validation.

Covers the title, space, pattern and section validators, including their boundaries.
``test_confluence_create_page_phases.py`` covers the publish phases and error handling.
"""

from .confluence_create_page_handler import (
    VALID_PATTERNS,
    validate_title,
    validate_sections,
    validate_pattern,
    validate_space,
)


class TestValidation:
    """Test input validation functions."""

    # Title validation
    def test_validate_title_valid(self):
        """Valid title (3-255 chars) passes."""
        is_valid, title = validate_title("Data Platform Roadmap")
        assert is_valid is True
        assert title == "Data Platform Roadmap"

    def test_validate_title_whitespace_stripped(self):
        """Whitespace is stripped automatically."""
        is_valid, title = validate_title("  Test Page  ")
        assert is_valid is True
        assert title == "Test Page"

    def test_validate_title_whitespace_only(self):
        """Whitespace-only title fails."""
        is_valid, message = validate_title("   \t\n  ")
        assert is_valid is False
        assert "whitespace" in message.lower()

    def test_validate_title_too_short(self):
        """Title < 3 chars fails."""
        is_valid, message = validate_title("ab")
        assert is_valid is False
        assert "too short" in message.lower()

    def test_validate_title_too_long(self):
        """Title > 255 chars fails."""
        is_valid, message = validate_title("a" * 300)
        assert is_valid is False
        assert "too long" in message.lower()

    def test_validate_title_boundary_min(self):
        """Title at minimum (3 chars) passes."""
        is_valid, title = validate_title("ABC")
        assert is_valid is True

    def test_validate_title_boundary_max(self):
        """Title at maximum (255 chars) passes."""
        is_valid, title = validate_title("a" * 255)
        assert is_valid is True

    # Space validation
    def test_validate_space_valid(self):
        """Valid space key passes."""
        is_valid, space = validate_space("DOCS")
        assert is_valid is True
        assert space == "DOCS"

    def test_validate_space_lowercase_converted(self):
        """Lowercase space key is converted to uppercase."""
        is_valid, space = validate_space("docs")
        assert is_valid is True
        assert space == "DOCS"

    def test_validate_space_with_numbers(self):
        """Space key with numbers is valid."""
        is_valid, space = validate_space("DA1")
        assert is_valid is True

    def test_validate_space_too_short(self):
        """Space key < 2 chars fails."""
        is_valid, message = validate_space("A")
        assert is_valid is False

    def test_validate_space_too_long(self):
        """Space key > 10 chars fails."""
        is_valid, message = validate_space("A" * 11)
        assert is_valid is False

    def test_validate_space_invalid_chars(self):
        """Space key with special chars fails."""
        is_valid, message = validate_space("DOCS-1")
        assert is_valid is False
        assert "alphanumeric" in message.lower() or "letters and numbers" in message.lower()

    # Pattern validation
    def test_validate_pattern_valid(self):
        """Valid pattern passes."""
        is_valid, pattern = validate_pattern("general_page")
        assert is_valid is True

    def test_validate_pattern_case_insensitive(self):
        """Pattern is case-insensitive."""
        is_valid, pattern = validate_pattern("GENERAL_PAGE")
        assert is_valid is True
        assert pattern == "general_page"

    def test_validate_pattern_invalid(self):
        """Invalid pattern fails."""
        is_valid, message = validate_pattern("invalid_pattern")
        assert is_valid is False
        assert "invalid" in message.lower()

    def test_validate_pattern_all_valid_options(self):
        """All currently-valid patterns pass — derived from VALID_PATTERNS so this
        test tracks additions/removals rather than hardcoding a stale list."""
        for p in VALID_PATTERNS:
            is_valid, _ = validate_pattern(p)
            assert is_valid is True, f"Pattern '{p}' should be valid"

    # Sections validation
    def test_validate_sections_valid(self):
        """Valid sections list passes."""
        is_valid, sections = validate_sections(["Overview", "Details", "Summary"])
        assert is_valid is True
        assert sections == ["Overview", "Details", "Summary"]

    def test_validate_sections_single_section(self):
        """Single section is valid."""
        is_valid, sections = validate_sections(["Overview"])
        assert is_valid is True

    def test_validate_sections_max_sections(self):
        """Maximum 10 sections is valid."""
        is_valid, sections = validate_sections([f"Section {i}" for i in range(10)])
        assert is_valid is True

    def test_validate_sections_too_many(self):
        """> 10 sections fails."""
        is_valid, message = validate_sections([f"Section {i}" for i in range(11)])
        assert is_valid is False
        assert "maximum" in message.lower()

    def test_validate_sections_no_sections(self):
        """Empty list fails."""
        is_valid, message = validate_sections([])
        assert is_valid is False

    def test_validate_sections_duplicates(self):
        """Duplicate sections fail."""
        is_valid, message = validate_sections(["Overview", "Details", "Overview"])
        assert is_valid is False
        assert "unique" in message.lower() or "duplicate" in message.lower()

    def test_validate_sections_whitespace_only(self):
        """Whitespace-only sections fail."""
        is_valid, message = validate_sections(["Overview", "   ", "Summary"])
        assert is_valid is False

    def test_validate_sections_whitespace_stripped(self):
        """Section whitespace is stripped."""
        is_valid, sections = validate_sections(["  Overview  ", "  Details  "])
        assert is_valid is True
        assert sections == ["Overview", "Details"]
