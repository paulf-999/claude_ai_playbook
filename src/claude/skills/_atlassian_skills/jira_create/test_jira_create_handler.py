"""Tests for jira_create handler.

Validates: phase orchestration, input validation, MCP integration (mocked).
"""

import pytest
from unittest.mock import MagicMock
from jira_create_handler import (
    validate_story_points,
    validate_title,
    phase_1_gather_details,
    phase_2_validate,
    phase_3_create_ticket,
    create_jira_ticket,
)


class TestValidation:
    """Test input validation functions."""

    def test_validate_story_points_valid(self):
        """Valid story points >= 0.5 pass."""
        is_valid, value = validate_story_points(3.0)
        assert is_valid is True
        assert value == 3.0

    def test_validate_story_points_boundary(self):
        """Boundary case: 0.5 is valid."""
        is_valid, value = validate_story_points(0.5)
        assert is_valid is True
        assert value == 0.5

    def test_validate_story_points_below_minimum(self):
        """Story points < 0.5 fails."""
        is_valid, message = validate_story_points(0.25)
        assert is_valid is False
        assert "must be >= 0.5" in message

    def test_validate_story_points_invalid_type(self):
        """Non-numeric story points fail."""
        is_valid, message = validate_story_points("not a number")
        assert is_valid is False
        assert "must be a number" in message

    def test_validate_story_points_zero(self):
        """Edge case: 0 story points fail."""
        is_valid, message = validate_story_points(0)
        assert is_valid is False

    def test_validate_story_points_negative(self):
        """Edge case: negative story points fail."""
        is_valid, message = validate_story_points(-5)
        assert is_valid is False

    def test_validate_story_points_string_numeric(self):
        """Edge case: string representation of number passes (coerced to float)."""
        is_valid, value = validate_story_points("5.0")
        assert is_valid is True
        assert value == 5.0

    def test_validate_title_valid(self):
        """Valid title passes."""
        is_valid, title = validate_title("Test ticket")
        assert is_valid is True
        assert title == "Test ticket"

    def test_validate_title_empty(self):
        """Empty title fails."""
        is_valid, message = validate_title("")
        assert is_valid is False
        assert "required" in message.lower()

    def test_validate_title_too_long(self):
        """Title > 255 chars fails."""
        long_title = "a" * 300
        is_valid, message = validate_title(long_title)
        assert is_valid is False
        assert "too long" in message.lower()

    def test_validate_title_whitespace_only(self):
        """Edge case: whitespace-only title fails."""
        is_valid, message = validate_title("   \t\n  ")
        assert is_valid is False
        assert "whitespace" in message.lower()

    def test_validate_title_with_leading_trailing_whitespace(self):
        """Edge case: leading/trailing whitespace is stripped."""
        is_valid, title = validate_title("  Test ticket  ")
        assert is_valid is True
        assert title == "Test ticket"

    def test_validate_title_at_max_length(self):
        """Edge case: title at exactly 255 chars passes."""
        max_title = "a" * 255
        is_valid, title = validate_title(max_title)
        assert is_valid is True

    def test_validate_title_one_over_max_length(self):
        """Edge case: title at 256 chars fails."""
        over_max = "a" * 256
        is_valid, message = validate_title(over_max)
        assert is_valid is False


class TestPhaseOrchestration:
    """Test three-phase flow."""

    def test_phase_1_gather_minimal(self):
        """Phase 1: gather accepts minimal input."""
        result = phase_1_gather_details(title="Test ticket")
        assert result["title"] == "Test ticket"
        assert result["description"] == ""
        assert result["assignee"] is None

    def test_phase_1_gather_full(self):
        """Phase 1: gather accepts all fields."""
        result = phase_1_gather_details(
            title="Test ticket",
            description="Description",
            assignee="user@example.com",
            story_points=5.0
        )
        assert result["title"] == "Test ticket"
        assert result["description"] == "Description"
        assert result["assignee"] == "user@example.com"
        assert result["story_points"] == 5.0

    def test_phase_2_validate_valid_ticket(self):
        """Phase 2: validate accepts valid ticket."""
        details = {
            "title": "Test ticket",
            "story_points": 3.0,
            "description": "Test description"
        }
        result = phase_2_validate(details)
        assert result["valid"] is True
        assert result["details"]["title"] == "Test ticket"

    def test_phase_2_validate_missing_title(self):
        """Phase 2: validate rejects missing title."""
        details = {"title": None, "story_points": 3.0}
        result = phase_2_validate(details)
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_phase_2_validate_invalid_story_points(self):
        """Phase 2: validate rejects invalid story points."""
        details = {"title": "Test", "story_points": 0.25}
        result = phase_2_validate(details)
        assert result["valid"] is False

    def test_phase_3_create_ticket_mocked(self):
        """Phase 3: call MCP tool (mocked)."""
        mock_mcp = MagicMock(return_value={"key": "TEST-123", "id": "10000"})
        details = {
            "title": "Test ticket",
            "description": "Test",
            "story_points": 3.0,
            "project": "TEST",
            "assignee": None
        }
        result = phase_3_create_ticket(mock_mcp, details)
        assert result["success"] is True
        assert mock_mcp.called


class TestErrorHandling:
    """Test Phase 3 error handling for MCP failures."""

    def test_phase_3_timeout_error(self):
        """Phase 3: TimeoutError returns graceful timeout message."""
        mock_mcp = MagicMock(side_effect=TimeoutError("Request timed out"))
        details = {
            "title": "Test ticket",
            "description": "Test",
            "story_points": 3.0,
            "project": "TEST",
            "assignee": None,
        }
        result = phase_3_create_ticket(mock_mcp, details)
        assert result["success"] is False
        assert result["type"] == "timeout"
        assert "timeout" in result["error"].lower()
        assert "--timeout-seconds" in result["error"]

    def test_phase_3_permission_error(self):
        """Phase 3: PermissionError returns permission denied message."""
        mock_mcp = MagicMock(side_effect=PermissionError("Access denied"))
        details = {
            "title": "Test ticket",
            "description": "Test",
            "story_points": 3.0,
            "project": "RESTRICTED",
            "assignee": None,
        }
        result = phase_3_create_ticket(mock_mcp, details)
        assert result["success"] is False
        assert result["type"] == "permission_denied"
        assert "permission" in result["error"].lower()
        assert "RESTRICTED" in result["error"]

    def test_phase_3_invalid_project_error(self):
        """Phase 3: ValueError with 'project' in message returns invalid_project error."""
        mock_mcp = MagicMock(side_effect=ValueError("Project 'BADPROJECT' not found"))
        details = {
            "title": "Test ticket",
            "description": "Test",
            "story_points": 3.0,
            "project": "BADPROJECT",
            "assignee": None,
        }
        result = phase_3_create_ticket(mock_mcp, details)
        assert result["success"] is False
        assert result["type"] == "invalid_project"
        assert "not found" in result["error"].lower()

    def test_phase_3_connection_error(self):
        """Phase 3: ConnectionError returns network error message."""
        mock_mcp = MagicMock(side_effect=ConnectionError("Network unreachable"))
        details = {
            "title": "Test ticket",
            "description": "Test",
            "story_points": 3.0,
            "project": "TEST",
            "assignee": None,
        }
        result = phase_3_create_ticket(mock_mcp, details)
        assert result["success"] is False
        assert result["type"] == "network_error"
        assert "network" in result["error"].lower()

    def test_phase_3_generic_exception(self):
        """Phase 3: Unexpected exception returns unknown error type."""
        mock_mcp = MagicMock(side_effect=RuntimeError("Unexpected failure"))
        details = {
            "title": "Test ticket",
            "description": "Test",
            "story_points": 3.0,
            "project": "TEST",
            "assignee": None,
        }
        result = phase_3_create_ticket(mock_mcp, details)
        assert result["success"] is False
        assert result["type"] == "unknown"
        assert "unexpected" in result["error"].lower()


class TestEndToEnd:
    """Test full orchestration."""

    def test_create_jira_ticket_valid_no_mcp(self):
        """Full flow: valid ticket without MCP tool returns validated details."""
        result = create_jira_ticket(
            title="Test ticket",
            description="Description",
            story_points=3.0,
            project="TEST"
        )
        assert result["success"] is True
        assert result["validated_details"]["title"] == "Test ticket"

    def test_create_jira_ticket_invalid_title(self):
        """Full flow: invalid title rejected early."""
        result = create_jira_ticket(
            title="",
            story_points=3.0,
            project="TEST"
        )
        assert result["success"] is False
        assert len(result["errors"]) > 0

    def test_create_jira_ticket_invalid_story_points(self):
        """Full flow: invalid story points rejected."""
        result = create_jira_ticket(
            title="Test ticket",
            story_points=0.1,
            project="TEST"
        )
        assert result["success"] is False
        assert "story points" in str(result["errors"]).lower()

    def test_create_jira_ticket_with_mocked_mcp(self):
        """Full flow: with mocked MCP tool."""
        mock_mcp = MagicMock(return_value={"key": "TEST-456", "id": "10001"})
        result = create_jira_ticket(
            title="Test ticket",
            description="Test",
            story_points=5.0,
            project="TEST",
            mcp_tool=mock_mcp
        )
        assert result["success"] is True
        assert mock_mcp.called

    def test_create_jira_ticket_input_sanitization(self):
        """Full flow: input whitespace is sanitized."""
        result = create_jira_ticket(
            title="  Test ticket  ",
            description="  Description  ",
            assignee="  user@example.com  ",
            story_points=3.0,
            project="TEST"
        )
        assert result["success"] is True
        assert result["validated_details"]["title"] == "Test ticket"
        assert result["validated_details"]["description"] == "Description"
        assert result["validated_details"]["assignee"] == "user@example.com"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
