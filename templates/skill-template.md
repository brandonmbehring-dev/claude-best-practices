---
name: pipeline-check
description: Pre-merge pipeline readiness verification
allowed-tools: [Bash, Read, Glob, Grep]
---

# Pipeline Check

<!-- WHY: Skills that orchestrate multiple checks produce the highest value.
     This skill replaces 5 manual commands with one invocation.
     CONVENTION: Save as .claude/skills/pipeline-check/SKILL.md
     (each skill gets its own directory with a SKILL.md file). -->

1. Verify all tests pass: `pytest tests/`
2. Check for uncommitted changes: `git status`
3. Verify no data leakage in feature code
4. Check model metrics logged to MLflow
5. Report readiness status (READY / NOT READY) with specific blockers if NOT READY
