---
name: deploy-check
description: Pre-deployment readiness verification
allowed-tools: [Bash, Read, Glob, Grep]
---

# Pre-Deploy Check

<!-- WHY: Skills that orchestrate multiple checks produce the highest value.
     This skill replaces 5 manual commands with one invocation.
     CONVENTION: Save as .claude/skills/deploy-check/SKILL.md
     (each skill gets its own directory with a SKILL.md file). -->

1. Verify all tests pass: `npm test`
2. Check for uncommitted changes: `git status`
3. Verify version bump in package.json
4. Check CHANGELOG.md has entry for this version
5. Report readiness status (READY / NOT READY) with specific blockers if NOT READY
