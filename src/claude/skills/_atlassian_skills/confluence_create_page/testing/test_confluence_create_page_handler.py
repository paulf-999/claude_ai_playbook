"""Tests for confluence_create_page orchestration handler.

Validates: phase orchestration, input validation, MCP integration (mocked).
"""

import pytest
from unittest.mock import MagicMock
from confluence_create_page_handler import (
    validate_title,
    validate_sections,
    validate_pattern,
    validate_space,
    phase_1_gather_details,
    phase_2_validate,
    phase_3_publish_page,
    create_confluence_page,
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
        is_valid, space = validate_space("DA")
        assert is_valid is True
        assert space == "DA"

    def test_validate_space_lowercase_converted(self):
        """Lowercase space key is converted to uppercase."""
        is_valid, space = validate_space("da")
        assert is_valid is True
        assert space == "DA"

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
        is_valid, message = validate_space("DA-1")
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
        """All valid patterns pass."""
        patterns = ["general_page", "requirements", "design_decision", "incident_report", "how_to"]
        for p in patterns:
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


class TestPhaseOrchestration:
    """Test three-phase flow."""

    def test_phase_1_gather_minimal(self):
        """Phase 1: gather accepts minimal input."""
        result = phase_1_gather_details(title="Test", space="DA", pattern="general_page", sections=["Sec1"])
        assert result["title"] == "Test"
        assert result["space"] == "DA"
        assert result["status"] == "draft"  # Default status

    def test_phase_2_validate_valid_page(self):
        """Phase 2: validate accepts valid page."""
        details = {
            "title": "Test Page",
            "space": "da",
            "pattern": "general_page",
            "sections": ["Overview", "Details"],
            "creator": "user@payroc.com",
            "status": "draft",
        }
        result = phase_2_validate(details)
        assert result["valid"] is True
        assert result["details"]["space"] == "DA"  # Normalized to uppercase

    def test_phase_2_validate_missing_title(self):
        """Phase 2: validate rejects missing title."""
        details = {"space": "DA", "pattern": "general_page", "sections": ["Sec1"]}
        result = phase_2_validate(details)
        assert result["valid"] is False

    def test_phase_2_validate_invalid_pattern(self):
        """Phase 2: validate rejects invalid pattern."""
        details = {
            "title": "Test",
            "space": "DA",
            "pattern": "invalid_pattern",
            "sections": ["Sec1"],
        }
        result = phase_2_validate(details)
        assert result["valid"] is False

    def test_phase_3_publish_mocked(self):
        """Phase 3: call MCP tool (mocked)."""
        mock_mcp = MagicMock(return_value={"pageId": "123456", "url": "https://confluence.example.com/..."})
        details = {
            "title": "Test Page",
            "space": "DA",
            "pattern": "general_page",
            "sections": ["Overview"],
            "creator": None,
            "status": "draft",
        }
        result = phase_3_publish_page(mock_mcp, details)
        assert result["success"] is True
        assert mock_mcp.called


class TestErrorHandling:
    """Test Phase 3 error handling for MCP failures."""

    def test_phase_3_timeout_error(self):
        """Phase 3: TimeoutError returns timeout message."""
        mock_mcp = MagicMock(side_effect=TimeoutError("Request timed out"))
        details = {"title": "Test", "space": "DA", "sections": ["Sec1"]}
        result = phase_3_publish_page(mock_mcp, details)
        assert result["success"] is False
        assert result["type"] == "timeout"

    def test_phase_3_permission_error(self):
        """Phase 3: PermissionError returns permission message."""
        mock_mcp = MagicMock(side_effect=PermissionError("Access denied"))
        details = {"title": "Test", "space": "RESTRICTED", "sections": ["Sec1"]}
        result = phase_3_publish_page(mock_mcp, details)
        assert result["success"] is False
        assert result["type"] == "permission_denied"

    def test_phase_3_invalid_space_error(self):
        """Phase 3: ValueError with 'space' in message returns invalid_space error."""
        mock_mcp = MagicMock(side_effect=ValueError("Space 'BADSPACE' not found"))
        details = {"title": "Test", "space": "BADSPACE", "sections": ["Sec1"]}
        result = phase_3_publish_page(mock_mcp, details)
        assert result["success"] is False
        assert result["type"] == "invalid_space"

    def test_phase_3_connection_error(self):
        """Phase 3: ConnectionError returns network error message."""
        mock_mcp = MagicMock(side_effect=ConnectionError("Network unreachable"))
        details = {"title": "Test", "space": "DA", "sections": ["Sec1"]}
        result = phase_3_publish_page(mock_mcp, details)
        assert result["success"] is False
        assert result["type"] == "network_error"

    def test_phase_3_generic_exception(self):
        """Phase 3: Unexpected exception returns unknown error type."""
        mock_mcp = MagicMock(side_effect=RuntimeError("Unexpected failure"))
        details = {"title": "Test", "space": "DA", "sections": ["Sec1"]}
        result = phase_3_publish_page(mock_mcp, details)
        assert result["success"] is False
        assert result["type"] == "unknown"


class TestEndToEnd:
    """Test full orchestration."""

    def test_create_page_valid_no_mcp(self):
        """Full flow: valid page without MCP tool returns validated details."""
        result = create_confluence_page(
            title="Test Page",
            space="DA",
            pattern="general_page",
            sections=["Overview", "Details"]
        )
        assert result["success"] is True
        assert result["validated_details"]["title"] == "Test Page"
        assert result["validated_details"]["space"] == "DA"

    def test_create_page_invalid_title(self):
        """Full flow: invalid title rejected early."""
        result = create_confluence_page(
            title="",
            space="DA",
            sections=["Sec1"]
        )
        assert result["success"] is False
        assert len(result["errors"]) > 0

    def test_create_page_invalid_sections(self):
        """Full flow: invalid sections rejected."""
        result = create_confluence_page(
            title="Test",
            space="DA",
            sections=[]
        )
        assert result["success"] is False

    def test_create_page_input_sanitization(self):
        """Full flow: input whitespace is sanitized."""
        result = create_confluence_page(
            title="  Test Page  ",
            space="  da  ",
            pattern="GENERAL_PAGE",
            sections=["  Overview  ", "  Details  "]
        )
        assert result["success"] is True
        assert result["validated_details"]["title"] == "Test Page"
        assert result["validated_details"]["space"] == "DA"
        assert result["validated_details"]["sections"] == ["Overview", "Details"]

    def test_create_page_with_mocked_mcp(self):
        """Full flow: with mocked MCP tool."""
        mock_mcp = MagicMock(return_value={"pageId": "789", "url": "https://confluence.com/..."})
        result = create_confluence_page(
            title="Test Page",
            space="DA",
            sections=["Overview"],
            mcp_tool=mock_mcp
        )
        assert result["success"] is True
        assert mock_mcp.called


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
