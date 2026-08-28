"""Orchestration handler for confluence_create_page skill.

Three-phase flow: gather details → draft review (local) → publish to Confluence.

Example usage:
    result = create_confluence_page(
        title="Data Platform Q4 Roadmap",
        space="DA",
        pattern="general_page",
        sections=["Overview", "Deliverables", "Risks"],
        creator="user@payroc.com"
    )
"""

import pathlib
import time
import threading
from typing import Any, Callable, Dict, List, Optional, Tuple

# Field constraints
MIN_TITLE_LENGTH = 3
MAX_TITLE_LENGTH = 255
MAX_SECTIONS = 10
MIN_SECTIONS = 1
VALID_PATTERNS = ["general_page", "requirements", "design_decision", "incident_report", "how_to"]
VALID_STATUSES = ["draft", "published", "archived"]


def validate_title(title: Any) -> Tuple[bool, str]:
    """Validate page title: 3-255 chars, not whitespace-only.

    Sanitization: strips leading/trailing whitespace.

    Args:
        title: Page title string

    Returns:
        (is_valid, title_or_error_message): Tuple of validation status and result
    """
    if not title or not isinstance(title, str):
        return False, "Title is required"

    sanitized = title.strip()

    if not sanitized:
        return False, "Title cannot be whitespace-only"

    if len(sanitized) < MIN_TITLE_LENGTH:
        return False, f"Title too short (minimum {MIN_TITLE_LENGTH} chars)"

    if len(sanitized) > MAX_TITLE_LENGTH:
        return False, f"Title too long ({len(sanitized)}/{MAX_TITLE_LENGTH} chars)"

    return True, sanitized


def validate_sections(sections: Any) -> Tuple[bool, str | List[str]]:
    """Validate page sections: 1-10 unique sections, each non-empty.

    Args:
        sections: List of section titles

    Returns:
        (is_valid, sections_or_error_message): Tuple of validation status and result
    """
    if not isinstance(sections, list):
        return False, "Sections must be a list"

    if len(sections) < MIN_SECTIONS:
        return False, f"At least {MIN_SECTIONS} section required"

    if len(sections) > MAX_SECTIONS:
        return False, f"Maximum {MAX_SECTIONS} sections allowed (got {len(sections)})"

    # Sanitize and check for duplicates
    sanitized = [s.strip() for s in sections if isinstance(s, str) and s.strip()]

    if len(sanitized) != len(sections):
        return False, "Sections cannot be empty or whitespace-only"

    if len(set(sanitized)) != len(sanitized):
        return False, "Sections must be unique (no duplicates)"

    return True, sanitized


def validate_pattern(pattern: Any) -> Tuple[bool, str]:
    """Validate pattern name: must be one of predefined patterns.

    Args:
        pattern: Pattern name string

    Returns:
        (is_valid, pattern_or_error_message): Tuple of validation status and result
    """
    if not isinstance(pattern, str):
        return False, f"Pattern must be a string, got {type(pattern).__name__}"

    pattern_lower = pattern.lower().strip()

    if pattern_lower not in VALID_PATTERNS:
        return False, f"Invalid pattern '{pattern}'. Valid options: {', '.join(VALID_PATTERNS)}"

    return True, pattern_lower


def validate_space(space: Any) -> Tuple[bool, str]:
    """Validate Confluence space key: non-empty, 2-10 chars, uppercase.

    Args:
        space: Confluence space key (e.g., "DA", "INFRA")

    Returns:
        (is_valid, space_or_error_message): Tuple of validation status and result
    """
    if not isinstance(space, str):
        return False, "Space must be a string"

    sanitized = space.strip().upper()

    if len(sanitized) < 2 or len(sanitized) > 10:
        return False, "Space key must be 2-10 characters"

    if not sanitized.isalnum():
        return False, "Space key must contain only letters and numbers"

    return True, sanitized


def phase_1_gather_details(
    title: Optional[str] = None,
    space: Optional[str] = None,
    pattern: Optional[str] = None,
    sections: Optional[List[str]] = None,
    creator: Optional[str] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    """Phase 1: Gather page details into a dict for validation.

    No validation occurs here — just collects and normalizes inputs.
    Sanitization: strips whitespace from string fields.

    Args:
        title: Page title (required)
        space: Confluence space key, e.g., "DA", "INFRA" (required)
        pattern: Content pattern, one of: general_page, requirements, etc. (required)
        sections: List of section titles (required)
        creator: Page creator email (optional)
        status: Page status: draft, published, archived (optional, defaults to draft)

    Returns:
        Dict with normalized details for Phase 2 validation
    """
    return {
        "title": title.strip() if isinstance(title, str) else title,
        "space": space.strip() if isinstance(space, str) else space,
        "pattern": pattern.strip() if isinstance(pattern, str) else pattern,
        "sections": sections,
        "creator": creator.strip() if isinstance(creator, str) else creator,
        "status": status.strip().lower() if isinstance(status, str) else status or "draft",
    }


def phase_2_validate(details: Dict[str, Any]) -> Dict[str, Any]:
    """Phase 2: Validate all required and optional fields.

    Checks: title (required), space (required), pattern (required), sections (required),
    creator (optional), status (optional).
    Accumulates all errors before returning.

    Args:
        details: Dict from Phase 1 with page details

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

    # Validate space (required)
    is_valid, space_result = validate_space(details.get("space"))
    if not is_valid:
        errors.append(space_result)
    else:
        details["space"] = space_result

    # Validate pattern (required)
    is_valid, pattern_result = validate_pattern(details.get("pattern"))
    if not is_valid:
        errors.append(pattern_result)
    else:
        details["pattern"] = pattern_result

    # Validate sections (required)
    is_valid, sections_result = validate_sections(details.get("sections"))
    if not is_valid:
        errors.append(sections_result)
    else:
        details["sections"] = sections_result

    # Validate creator (optional)
    if details.get("creator"):
        if not isinstance(details["creator"], str) or "@" not in details["creator"]:
            errors.append("Creator must be a valid email address")

    # Validate status (optional, default to draft)
    if details.get("status") not in VALID_STATUSES:
        errors.append(f"Status must be one of: {', '.join(VALID_STATUSES)}")

    if errors:
        return {"valid": False, "errors": errors}

    return {"valid": True, "details": details}


def phase_3_publish_page(
    mcp_tool_call: Callable[..., Dict[str, Any]],
    details: Dict[str, Any],
    draft_content: Optional[str] = None,
) -> Dict[str, Any]:
    """Phase 3: Publish page to Confluence after draft approval.

    Calls Atlassian MCP tool to create or update page.
    Handles common failure modes: timeout, invalid space, permission denied, network errors.

    Args:
        mcp_tool_call: Function that calls mcp__atlassian__createConfluencePage
        details: Validated page details from Phase 2
        draft_content: Markdown content (generated in Phase 2, optional for testing)

    Returns:
        {"success": True, "result": {...}} with page ID and link on success
        {"success": False, "error": "msg", "type": "error_type"} on failure

    Error types:
        - timeout: MCP call took too long (120s+)
        - invalid_space: Space does not exist or user has no access
        - permission_denied: User lacks write permission to space
        - network_error: Connection failure or MCP server unreachable
        - unknown: Unexpected error from MCP tool
    """
    try:
        result = mcp_tool_call(
            spaceKey=details.get("space"),
            title=details["title"],
            body=draft_content or f"# {details['title']}\n\nPage content pending.",
            parentPageId=None,
        )
        return {"success": True, "result": result}
    except TimeoutError:
        return {
            "success": False,
            "error": "Confluence API timeout after 120 seconds. Try publishing again.",
            "type": "timeout",
        }
    except PermissionError:
        return {
            "success": False,
            "error": f"Permission denied: You lack write access to space {details.get('space')}",
            "type": "permission_denied",
        }
    except ValueError as e:
        error_msg = str(e).lower()
        if "space" in error_msg:
            return {
                "success": False,
                "error": f"Space '{details.get('space')}' not found or inaccessible",
                "type": "invalid_space",
            }
        return {"success": False, "error": str(e), "type": "validation_error"}
    except ConnectionError:
        return {
            "success": False,
            "error": "Network error: Cannot reach Confluence. Check your internet connection.",
            "type": "network_error",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "type": "unknown",
        }


def create_confluence_page(
    title: str,
    space: str,
    pattern: str = "general_page",
    sections: Optional[List[str]] = None,
    creator: Optional[str] = None,
    status: Optional[str] = None,
    draft_content: Optional[str] = None,
    mcp_tool: Optional[Callable[..., Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Main entry point: Orchestrate all three phases to create a Confluence page.

    Phase 1 (Gather): Collect page details from parameters.
    Phase 2 (Validate): Validate title, space, pattern, sections.
    Phase 3 (Publish): Call Atlassian MCP tool to publish page (after draft review).

    Args:
        title: Page title (required, 3-255 chars)
        space: Confluence space key (required, e.g., "DA", "INFRA")
        pattern: Content pattern (required, default "general_page")
        sections: List of section titles (required, 1-10 unique sections)
        creator: Page creator email (optional)
        status: Page status (optional, default "draft")
        draft_content: Markdown content (optional, generated during draft review)
        mcp_tool: Function that calls mcp__atlassian__createConfluencePage (optional for testing)

    Returns:
        On success:
            {"success": True, "result": {...}} with Confluence page ID and URL
            OR {"success": True, "validated_details": {...}} if mcp_tool not provided

        On failure:
            {"success": False, "errors": ["error1", "error2", ...]} (validation failures)
            OR {"success": False, "error": "msg", "type": "error_type"} (MCP failures)

    Example:
        result = create_confluence_page(
            title="Q4 Data Platform Roadmap",
            space="DA",
            pattern="general_page",
            sections=["Overview", "Deliverables", "Timeline"],
            creator="user@payroc.com",
            mcp_tool=atlassian_mcp.createConfluencePage
        )
        if result["success"]:
            print(f"Created page: {result['result']['url']}")
        else:
            print(f"Error: {result['error']}")
    """
    # Phase 1: Gather details from parameters
    details = phase_1_gather_details(
        title=title,
        space=space,
        pattern=pattern,
        sections=sections,
        creator=creator,
        status=status,
    )

    # Phase 2: Validate (all required fields, accumulate errors)
    validation = phase_2_validate(details)
    if not validation["valid"]:
        return {"success": False, "errors": validation["errors"]}

    # Phase 3: Publish to Confluence (skip if tool not provided, for testing)
    if mcp_tool:
        return phase_3_publish_page(mcp_tool, validation["details"], draft_content)

    # If no MCP tool provided, return validated details (for unit tests)
    return {"success": True, "validated_details": validation["details"]}


def save_draft(content: str, page_title: str) -> pathlib.Path:
    """Save draft to ~/.claude/_drafts/confluence/ directory.

    Args:
        content: Markdown content to save
        page_title: Page title (used for filename sanitization)

    Returns:
        Path object pointing to the saved draft file
    """
    drafts_dir = pathlib.Path.home() / ".claude" / "_drafts" / "confluence"
    drafts_dir.mkdir(parents=True, exist_ok=True)

    # Sanitize filename: replace spaces and special chars with underscores
    safe_title = "".join(c if c.isalnum() or c == "_" else "_" for c in page_title.lower())
    filename = f"{safe_title}_{int(time.time())}.md"

    draft_path = drafts_dir / filename
    draft_path.write_text(content)
    return draft_path


def format_timeout_dialog(elapsed: int, remaining_attempts: int) -> str:
    """Format timeout dialog message with user options.

    Args:
        elapsed: Seconds elapsed since tool call started
        remaining_attempts: Number of [C]ontinue attempts left (max 1)

    Returns:
        Formatted dialog string with options
    """
    minutes = elapsed // 60

    dialog = f"""
⏱️  CONFLUENCE PUBLISH TIMEOUT

Your page has been publishing for {minutes} minute{'s' if minutes != 1 else ''} ({elapsed} seconds).
Confluence is not responding. Choose an action:

[A]bort  — Cancel now, preserve draft in ~/.claude/_drafts/confluence/
[R]etry  — Cancel and start a fresh publish attempt
[C]ontinue — Wait 4 more minutes (max 6 minutes total)

Enter your choice (A/R/C): """

    return dialog


def parse_timeout_arg(args: List[str]) -> int:
    """Parse --timeout-seconds command-line argument.

    Args:
        args: Command-line arguments (e.g., from sys.argv)

    Returns:
        Timeout in seconds (default 120)
    """
    default_timeout = 120

    try:
        if "--timeout-seconds" in args:
            idx = args.index("--timeout-seconds")
            if idx + 1 < len(args):
                return int(args[idx + 1])
    except (ValueError, IndexError):
        pass

    return default_timeout


def create_page_with_timeout(  # noqa: C901
    tool_call: Callable[[], Dict[str, Any]],
    timeout_seconds: int = 120,
    draft_path: Optional[pathlib.Path] = None,
) -> Dict[str, Any]:
    """Wrap a Confluence publish tool call with timeout protection.

    Monitors tool call duration and shows timeout dialog if it exceeds the limit.
    User can [A]bort, [R]etry, or [C]ontinue (max 6 minutes total).

    Args:
        tool_call: Function that calls Confluence API (returns Dict with pageId)
        timeout_seconds: Initial timeout in seconds (default 120 / 2 minutes)
        draft_path: Path to draft file (for [A]bort preservation)

    Returns:
        {"status": "success", "pageId": "...", "url": "...", "elapsed": N}
        {"status": "timeout", "elapsed": N}
        {"status": "retry_requested", "elapsed": N}
        {"status": "aborted", "elapsed": N, "draft_path": "..."}
    """
    start_time = time.time()
    result_container = [None]
    exception_container = [None]

    def run_tool():
        try:
            result_container[0] = tool_call()
        except Exception as e:
            exception_container[0] = e

    # Start tool call in background thread
    thread = threading.Thread(target=run_tool, daemon=True)
    thread.start()

    # Monitor for timeout
    max_total_wait = 360  # 6 minutes maximum
    current_timeout = timeout_seconds

    while thread.is_alive():
        elapsed = int(time.time() - start_time)

        # Check if we've exceeded max wait
        if elapsed >= max_total_wait:
            return {
                "status": "aborted",
                "elapsed": elapsed,
                "draft_path": str(draft_path) if draft_path else None,
            }

        # Check if we've exceeded current timeout
        if elapsed >= current_timeout:
            # Show timeout dialog
            dialog = format_timeout_dialog(elapsed, remaining_attempts=1)
            try:
                choice = input(dialog).strip().upper()
            except (EOFError, KeyboardInterrupt):
                choice = "A"

            if choice == "A":
                return {
                    "status": "aborted",
                    "elapsed": elapsed,
                    "draft_path": str(draft_path) if draft_path else None,
                }
            elif choice == "R":
                return {"status": "retry_requested", "elapsed": elapsed}
            elif choice == "C":
                # Extend by 4 more minutes, but cap at 6 total
                current_timeout = min(elapsed + 240, max_total_wait)
            else:
                # Invalid choice, default to abort
                return {
                    "status": "aborted",
                    "elapsed": elapsed,
                    "draft_path": str(draft_path) if draft_path else None,
                }

        # Wait a bit before checking again
        time.sleep(1)

    # Tool completed
    elapsed = int(time.time() - start_time)

    if exception_container[0]:
        return {
            "status": "error",
            "error": str(exception_container[0]),
            "elapsed": elapsed,
        }

    if result_container[0]:
        return {
            "status": "success",
            "pageId": result_container[0].get("pageId"),
            "url": result_container[0].get("url"),
            "elapsed": elapsed,
        }

    return {"status": "unknown", "elapsed": elapsed}


if __name__ == "__main__":
    # Quick smoke test
    result = create_confluence_page(
        title="Test Page",
        space="DA",
        pattern="general_page",
        sections=["Section 1", "Section 2"]
    )
    print(f"Test result: {result}")
