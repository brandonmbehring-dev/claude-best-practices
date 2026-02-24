# Project Name

## Build Commands
<!-- WHY: Every command Claude needs to verify its own work -->
- `npm run build` — compile TypeScript
- `npm test` — run Jest tests
- `npm run lint` — ESLint + Prettier check
- `npm run typecheck` — tsc --noEmit

## Architecture
<!-- WHY: Tells Claude WHERE things go, reducing misplaced code -->
- src/routes/ — API endpoints (one file per resource)
- src/services/ — Business logic (no HTTP concerns)
- src/models/ — Database models (Prisma)
- src/middleware/ — Express middleware
- tests/ — mirrors src/ structure

## Code Conventions
<!-- WHY: Only rules Claude wouldn't infer from the codebase -->
- TypeScript strict mode, no `any`
- Functional style: prefer pure functions, immutable data
- Error handling: throw typed errors, never swallow exceptions
- Naming: camelCase variables, PascalCase types, UPPER_SNAKE constants

## Testing Standards
<!-- WHY: These lines improve every interaction (Ch 6) -->
- Run tests after every code change
- Never commit without passing lint + tests + typecheck
- Coverage target: 80% for src/ modules
- Every new function needs: happy path + error case + edge case

## Git Conventions
- Conventional commits: feat/fix/refactor/test/docs
- PR description includes: Summary, Test Plan, Breaking Changes

## Security
<!-- WHY: Defense in depth — CLAUDE.md advisory + deny rules enforced + hooks guaranteed -->
- Never read .env files
- Never commit secrets, API keys, or credentials
- Validate all user input at API boundary
