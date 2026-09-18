#!/bin/bash
# enforcement_markdown_file_locations.sh
# Validates .md files written to ~/.claude/ against writing_style.md conventions
# Mode: blocking (returns exit code 1 for invalid paths)

FILE_PATH="${CLAUDE_TOOL_INPUT_FILE_PATH:-$1}"

# Skip if not a .md file or not under ~/.claude/
if [[ ! "$FILE_PATH" =~ \.md$ ]] || [[ ! "$FILE_PATH" =~ ^$HOME/\.claude/ ]]; then
  exit 0
fi

# Exempt patterns (these follow different conventions)
EXEMPT_PATTERNS=(
  "CLAUDE.md$"           # Config files
  "MEMORY.md$"           # Global memory index
  "README.md$"           # Directory readmes
  "/_rules/.*README\.md$" # Rules documentation
  "/skills/.*/SKILL\.md$" # Skill documentation
  "/agents/.*/.*\.md$"   # Agent documentation
  "/keybindings\.json"   # Non-markdown
)

# Check if file matches exemption patterns
for pattern in "${EXEMPT_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" =~ $pattern ]]; then
    exit 0
  fi
done

# Valid domains for dated paths (_drafts, _errors)
VALID_DOMAINS="(1on1|confluence|email|general|important|jira|meetings|plans|reference|teams)"

# Valid path patterns from writing_style.md
# Drafts:   ~/.claude/_drafts/<domain>/YYYY-MM-DD_<topic>.md
# Errors:   ~/.claude/_errors/<domain>/YYYY-MM-DD_<topic>.md
# Reference: ~/.claude/_reference/<topic>.md (no date)
# Sessions: ~/.claude/_sessions/YYYY-MM-DD_<domain>_<topic>.md

VALID_PATTERNS=(
  "^$HOME/\.claude/_drafts/${VALID_DOMAINS}/[0-9]{4}-[0-9]{2}-[0-9]{2}_[a-z0-9_]+\.md$"
  "^$HOME/\.claude/_errors/${VALID_DOMAINS}/[0-9]{4}-[0-9]{2}-[0-9]{2}_[a-z0-9_]+\.md$"
  "^$HOME/\.claude/_reference/[a-z0-9_]+\.md$"
  "^$HOME/\.claude/_sessions/[0-9]{4}-[0-9]{2}-[0-9]{2}_[a-z0-9_]+_[a-z0-9_]+\.md$"
  "^$HOME/\.claude/memory/.*\.md$"
  "^$HOME/\.claude/_rules/.*\.md$"
  "^$HOME/\.claude/projects/.*/memory/.*\.md$"
)

# Check if file matches any valid pattern
for pattern in "${VALID_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" =~ $pattern ]]; then
    exit 0
  fi
done

# If we get here, file doesn't match valid conventions — block write
RELATIVE_PATH="${FILE_PATH#"$HOME"/}"
cat >&2 << EOF
❌ Error: Markdown file location does not follow writing_style.md conventions:
   Path: $RELATIVE_PATH

   Valid locations:
   • Drafts:     ~/.claude/_drafts/<domain>/YYYY-MM-DD_<topic>.md
   • Errors:     ~/.claude/_errors/<domain>/YYYY-MM-DD_<topic>.md
   • Reference:  ~/.claude/_reference/<topic>.md
   • Sessions:   ~/.claude/_sessions/YYYY-MM-DD_<domain>_<topic>.md

   Domains: 1on1, confluence, email, general, important, jira, meetings, plans, reference, teams

   See: ~/.claude/_rules/01_core/writing_style.md → Drafts and errors section
EOF

exit 1
