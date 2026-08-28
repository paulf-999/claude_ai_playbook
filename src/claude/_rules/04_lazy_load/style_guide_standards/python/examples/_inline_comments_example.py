# ruff: noqa: F821  # illustrative example; referenced handlers are not meant to be defined here
"""
Example: Inline commenting style for Python code.

Shows the expected level of commenting for logical phases and non-obvious flow.
"""


def dispatch_command(parsed_args):
    """Dispatch parsed arguments to the appropriate handler.

    :param parsed_args: Parsed command-line arguments from argparse.
    """
    # Dispatch to the appropriate handler, converting parsed args to list format
    if parsed_args.command == "export":
        # Export: pass server name as single positional arg
        handler_export([parsed_args.server])
    elif parsed_args.command == "import":
        # Import: pass server name + optional --apply flag
        args = [parsed_args.server]
        if parsed_args.apply:
            args.append("--apply")
        handler_import(args)
    elif parsed_args.command == "create":
        # Create: pass optional --config and --apply flags
        args = []
        if parsed_args.config:
            args.extend(["--config", parsed_args.config])
        if parsed_args.apply:
            args.append("--apply")
        handler_create(args)
    else:
        # No command provided — print help and exit
        print_help()
        sys.exit(1)


def process_items(items):
    """Process a list of items in distinct phases.

    :param items: List of items to process.
    """
    # Phase 1: Validate all items before proceeding
    for item in items:
        if not is_valid(item):
            raise ValueError(f"Invalid item: {item}")

    # Phase 2: Transform items
    transformed = [transform(item) for item in items]

    # Phase 3: Write results (slower operation, separate phase for clarity)
    write_results(transformed)
