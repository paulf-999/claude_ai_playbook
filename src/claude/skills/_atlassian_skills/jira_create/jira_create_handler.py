"""Minimal executable handler for jira_create skill.

Three-phase flow: gather details → validate → create ticket via Atlassian MCP.

Example usage:
    result = create_jira_ticket(
        title="Fix database timeout",
        description="Postgres queries timing out after 30s",
        story_points=5.0,
        project="DATA"
    )
"""

from typing import Any, Callable, Dict, Optional, Tuple

# Field constraints and Jira-specific mappings
MIN_STORY_POINTS = 0.5
MAX_TITLE_LENGTH = 255
DEFAULT_ISSUE_TYPE = "Story"
# customfield_10016 is Jira's internal ID for story points (varies by Jira instance but 10016 is standard)
STORY_POINTS_FIELD_ID = "customfield_10016"


def validate_story_points(points: Any) -> Tuple[bool, str | float]:
    """Validate story points >= 0.5.

    Args:
        points: Numeric story points estimate

    Returns:
        (is_valid, value_or_error_message): Tuple of validation status and result
    """
    try:
        value = float(points)
        if value < MIN_STORY_POINTS:
            return False, f"Story points must be >= {MIN_STORY_POINTS}, got {value}"
        return True, value
    except (ValueError, TypeError):
        return False, f"Story points must be a number, got {points}"


def validate_title(title: Any) -> Tuple[bool, str]:
    """Validate title: non-empty, <= MAX_TITLE_LENGTH chars, not whitespace-only.

    Sanitization: strips leading/trailing whitespace automatically.

    Args:
        title: Ticket title string

    Returns:
        (is_valid, title_or_error_message): Tuple of validation status and result
    """
    if not title or not isinstance(title, str):
        return False, "Title is required"

    # Sanitize: strip whitespace
    sanitized = title.strip()

    if not sanitized:
        return False, "Title cannot be whitespace-only"

    if len(sanitized) > MAX_TITLE_LENGTH:
        return False, f"Title too long ({len(sanitized)}/{MAX_TITLE_LENGTH} chars)"

    return True, sanitized


def phase_1_gather_details(
    title: Optional[str] = None,
    description: Optional[str] = None,
    assignee: Optional[str] = None,
    story_points: Optional[float] = None,
) -> Dict[str, Any]:
    """Phase 1: Gather ticket details into a dict for validation.

    No validation occurs here — just collects and normalizes (sanitizes) inputs.
    Sanitization: strips whitespace from all string fields.

    Args:
        title: Ticket title (required for Phase 2)
        description: Ticket description (defaults to empty string, sanitized)
        assignee: Jira user email or account ID (optional, sanitized)
        story_points: Story points estimate (optional, >= 0.5 if provided)

    Returns:
        Dict with keys: title, description, assignee, story_points (all sanitized)
    """
    return {
        "title": title.strip() if isinstance(title, str) else title,
        "description": (description.strip() if isinstance(description, str) else description) or "",
        "assignee": assignee.strip() if isinstance(assignee, str) else assignee,
        "story_points": story_points,
    }


def phase_2_validate(details: Dict[str, Any]) -> Dict[str, Any]:
    """Phase 2: Validate all required and optional fields.

    Checks: title (required), story_points (optional, >= 0.5 if provided).
    Accumulates all errors before returning.

    Args:
        details: Dict from Phase 1 with ticket details

    Returns:
        {"valid": True, "details": {...}} on success
        {"valid": False, "errors": [msg1, msg2, ...]} on failure
    """
    errors = []

    # Validate title (required)
    is_valid, title_result = validate_title(details.get("title"))
    if not is_valid:
        errors.append(title_result)
    else:
        details["title"] = title_result

    # Validate story points if provided (optional field)
    if details.get("story_points") is not None:
        is_valid, points_result = validate_story_points(details.get("story_points"))
        if not is_valid:
            errors.append(points_result)
        else:
            details["story_points"] = points_result

    if errors:
        return {"valid": False, "errors": errors}

    return {"valid": True, "details": details}


def phase_3_create_ticket(
    mcp_tool_call: Callable[..., Dict[str, Any]],
    details: Dict[str, Any],
) -> Dict[str, Any]:
    """Phase 3: Call Atlassian MCP tool to create ticket.

    Handles common failure modes: timeout, invalid project, permission denied,
    network errors. Returns structured result for caller to handle.

    Args:
        mcp_tool_call: Function that calls mcp__atlassian__createJiraIssue
        details: Validated ticket details from Phase 2

    Returns:
        {"success": True, "result": {...}} with issue ID and link on success
        {"success": False, "error": "message", "type": "error_type"} on failure

    Error types:
        - timeout: MCP call took too long (30s+)
        - invalid_project: Project does not exist or user has no access
        - permission_denied: User lacks write permission to project
        - network_error: Connection failure or MCP server unreachable
        - unknown: Unexpected error from MCP tool
    """
    try:
        result = mcp_tool_call(
            projectIdOrKey=details.get("project"),
            issueTypeName=DEFAULT_ISSUE_TYPE,
            summary=details["title"],
            description=details.get("description", ""),
            assignee=details.get("assignee"),
            customFields={STORY_POINTS_FIELD_ID: details.get("story_points")} if details.get("story_points") else {}
        )
        return {"success": True, "result": result}
    except TimeoutError as e:
        return {
            "success": False,
            "error": f"Jira API timeout after 30 seconds. Try again with --timeout-seconds 60.",
            "type": "timeout",
        }
    except PermissionError as e:
        return {
            "success": False,
            "error": f"Permission denied: You lack write access to project {details.get('project')}",
            "type": "permission_denied",
        }
    except ValueError as e:
        error_msg = str(e).lower()
        if "project" in error_msg:
            return {
                "success": False,
                "error": f"Project '{details.get('project')}' not found or inaccessible",
                "type": "invalid_project",
            }
        return {"success": False, "error": str(e), "type": "validation_error"}
    except ConnectionError as e:
        return {
            "success": False,
            "error": "Network error: Cannot reach Jira. Check your internet connection.",
            "type": "network_error",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "type": "unknown",
        }


def create_jira_ticket(
    title: str,
    description: Optional[str] = None,
    assignee: Optional[str] = None,
    story_points: Optional[float] = None,
    project: Optional[str] = None,
    mcp_tool: Optional[Callable[..., Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Main entry point: Orchestrate all three phases to create a Jira ticket.

    Phase 1 (Gather): Collect ticket details from parameters.
    Phase 2 (Validate): Validate title (required) and story_points (optional).
    Phase 3 (Create): Call Atlassian MCP tool to create ticket.

    Args:
        title: Ticket title (required, max 255 chars)
        description: Ticket description (optional, defaults to empty)
        assignee: Jira user email or account ID (optional)
        story_points: Story points estimate (optional, must be >= 0.5 if provided)
        project: Jira project key (required for Phase 3, e.g. "DATA", "INFRA")
        mcp_tool: Function that calls mcp__atlassian__createJiraIssue (optional for testing)

    Returns:
        On success:
            {"success": True, "result": {...}} with Jira issue ID and link
            OR {"success": True, "validated_details": {...}} if mcp_tool not provided

        On failure:
            {"success": False, "errors": ["error1", "error2", ...]} (validation failures)
            OR {"success": False, "error": "msg", "type": "error_type"} (MCP failures)

    Example:
        result = create_jira_ticket(
            title="Fix timeout in payment processor",
            description="Database queries timing out after 30s",
            story_points=5.0,
            project="DATA",
            mcp_tool=atlassian_mcp.createJiraIssue
        )
        if result["success"]:
            print(f"Created issue: {result['result']['key']}")
        else:
            print(f"Error: {result['error']}")
    """
    # Phase 1: Gather details from parameters
    details = phase_1_gather_details(
        title=title,
        description=description,
        assignee=assignee,
        story_points=story_points
    )
    details["project"] = project

    # Phase 2: Validate (title required, story_points optional but validated if present)
    validation = phase_2_validate(details)
    if not validation["valid"]:
        return {"success": False, "errors": validation["errors"]}

    # Phase 3: Create ticket via MCP tool (skip if tool not provided, for testing)
    if mcp_tool:
        return phase_3_create_ticket(mcp_tool, validation["details"])

    # If no MCP tool provided, return validated details (for unit tests)
    return {"success": True, "validated_details": validation["details"]}


if __name__ == "__main__":
    # Quick smoke test
    result = create_jira_ticket(
        title="Test ticket",
        description="This is a test",
        story_points=3.0,
        project="TEST"
    )
    print(f"Test result: {result}")
