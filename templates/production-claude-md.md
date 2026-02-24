# Project Name

## Build & Verify
<!-- WHY: Every command Claude needs to verify its own work -->
- `pytest tests/` — run test suite
- `mypy src/` — type checking
- `ruff check src/` — lint
- `nbstripout notebooks/` — strip notebook outputs before commit

## Architecture
<!-- WHY: Tells Claude WHERE things go, reducing misplaced code -->
- src/features/ — feature engineering pipelines
- src/models/ — model training and evaluation
- src/data/ — data loading and validation
- notebooks/ — exploratory analysis (EDA, prototyping)
- data/raw/ — immutable source data (never modify)
- data/processed/ — transformed artifacts
- configs/ — experiment configs, hyperparameters
- tests/ — mirrors src/ structure

## Code Conventions
<!-- WHY: Only rules Claude wouldn't infer from the codebase -->
- Type hints on all function signatures
- Functional style: prefer pure functions, immutable DataFrames
- Error handling: raise ValueError/TypeError with context, never swallow exceptions
- Naming: snake_case variables, PascalCase classes, UPPER_SNAKE constants

## Testing Standards
<!-- WHY: These lines improve every interaction (Ch 6) -->
- Run tests after every code change
- Never commit without passing lint + tests + type check
- Coverage target: 80% for src/ modules
- Every new function needs: happy path + error case + edge case (empty DataFrame, NaN-heavy input)

## ML Standards
<!-- WHY: Prevents the most expensive ML bugs -->
- No data leakage: features must use only pre-split data
- Log all hyperparameters to MLflow
- Save model artifacts to models/ with versioned names
- Include reproducibility seed in all experiment configs
- Document feature distributions for training data

## Git Conventions
- Conventional commits: feat/fix/refactor/test/docs
- PR description includes: Summary, Test Plan, Breaking Changes

## Security
<!-- WHY: Defense in depth — CLAUDE.md advisory + deny rules enforced + hooks guaranteed -->
- Never read .env files
- Never commit secrets, API keys, or credentials
- Never commit raw data files (data/raw/ is gitignored)
