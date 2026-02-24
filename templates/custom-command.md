# .claude/commands/check.md

<!-- WHY: Commands that encode decision workflows produce more value
     than commands that simply run a script. This command gathers
     information and presents a summary, letting you decide next steps. -->

Run a comprehensive check of the project:

1. Run the test suite: `npm test`
2. Run the linter: `npm run lint`
3. Run the type checker: `npm run typecheck`
4. Report results as a summary table:

| Check | Status | Details |
|-------|--------|---------|
| Tests | PASS/FAIL | X passed, Y failed |
| Lint  | PASS/FAIL | N warnings |
| Types | PASS/FAIL | N errors |
