---
name: deploy-check
description: Pre-deployment readiness verification
allowed_tools: [Bash, Read, Glob, Grep]
---

# Pre-Deploy Check

1. Verify all tests pass: `npm test`
2. Check for uncommitted changes: `git status`
3. Verify version bump in package.json
4. Check CHANGELOG.md has entry for this version
5. Report readiness status (READY / NOT READY) with specific blockers if NOT READY
