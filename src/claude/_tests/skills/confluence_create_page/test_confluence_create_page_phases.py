# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-01
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests the confluence_create_page handler's publish phases, with the Confluence call mocked.

Covers gathering and validating details, publishing, the error each failure mode
returns, and the end-to-end flow. ``test_confluence_create_page_handler.py`` covers
input validation.
"""

from unittest.mock import MagicMock

from .confluence_create_page_handler import (
    create_confluence_page,
    phase_1_gather_details,
    phase_2_validate,
    phase_3_publish_page,
)


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
