#!/bin/bash
# Repoprompt SSH Tool - Patrick Only
# This tool provides secure access to Repoprompt via SSH

# Security check - only Patrick can use this
check_user() {
    local slack_user="$1"
    if [[ "$slack_user" != "U04C7A4DE" ]]; then
        echo "ERROR: Access denied. This tool is restricted to Patrick only."
        exit 1
    fi
}

# SSH connection details
SSH_HOST="shanahanland@100.67.25.22"
REPOPROMPT_PATH="~/RepoPrompt/repoprompt_cli"

# Main function
repoprompt() {
    local action="$1"
    local workspace="$2"
    shift 2
    local args="$@"
    
    case "$action" in
        "list")
            ssh "$SSH_HOST" "$REPOPROMPT_PATH -e 'workspace list'"
            ;;
        "view")
            if [[ -z "$workspace" ]]; then
                echo "ERROR: Workspace ID required"
                exit 1
            fi
            ssh "$SSH_HOST" "$REPOPROMPT_PATH -e 'workspace view' --workspace '$workspace'"
            ;;
        "extract")
            if [[ -z "$workspace" ]]; then
                echo "ERROR: Workspace ID required"
                exit 1
            fi
            ssh "$SSH_HOST" "$REPOPROMPT_PATH -e 'workspace extract' --workspace '$workspace' $args"
            ;;
        "help")
            echo "Usage: repoprompt-ssh <action> [workspace] [options]"
            echo ""
            echo "Actions:"
            echo "  list              List all workspaces"
            echo "  view <id>         View workspace details"
            echo "  extract <id>      Extract workspace to XML"
            echo ""
            echo "Examples:"
            echo "  repoprompt-ssh list"
            echo "  repoprompt-ssh view 612664F9-2C29-4AB5-9D35-BE52CCFA1EBC"
            echo "  repoprompt-ssh extract 612664F9-2C29-4AB5-9D35-BE52CCFA1EBC --include '*.py'"
            ;;
        *)
            echo "ERROR: Unknown action: $action"
            echo "Run 'repoprompt-ssh help' for usage"
            exit 1
            ;;
    esac
}

# Entry point
if [[ "$1" == "--check-access" ]]; then
    # Special mode for Henri to verify access
    check_user "$2"
    echo "Access granted for Patrick"
else
    # Normal operation
    repoprompt "$@"
fi