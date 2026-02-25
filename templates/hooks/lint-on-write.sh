#!/bin/bash
# .claude/hooks/lint-on-write.sh
# PostToolUse hook: auto-lint files after Edit or Write tool calls.
# Reads JSON from stdin to extract the file path.
FILE_PATH=$(jq -r '.tool_input.file_path // empty')

if [ -n "$FILE_PATH" ] && [[ "$FILE_PATH" == *.py ]]; then
  ruff check --fix "$FILE_PATH" 2>/dev/null
fi
