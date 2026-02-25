#!/bin/bash
# .claude/hooks/pre-commit-gate.sh
# PreToolUse hook: block git commits if tests fail or type errors exist.
# Reads JSON from stdin to check if the Bash command is a git commit.
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Only gate on git commit commands
if echo "$COMMAND" | grep -qE '^git commit'; then
  # Run tests and type checking
  if ! pytest tests/ > /dev/null 2>&1; then
    echo "$INPUT" | jq -n '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: "Tests failed. Fix failing tests before committing."
      }
    }'
    exit 0
  fi

  if ! mypy src/ > /dev/null 2>&1; then
    echo "$INPUT" | jq -n '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: "Type errors found. Fix type errors before committing."
      }
    }'
    exit 0
  fi
fi

# Allow all other commands
exit 0
