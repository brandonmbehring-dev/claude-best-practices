# Project Name

## Build & Verify
<!-- WHY: Claude cannot guess non-standard build commands -->
- `pytest tests/` — run test suite
- `mypy src/` — type checking
- `ruff check src/` — lint

## Code Style
<!-- WHY: Only rules that differ from standard conventions -->
- Type hints on all function signatures
- Docstrings on all public functions

## Testing
<!-- WHY: Verification criteria improve every interaction (Ch 6) -->
- Run tests after every code change
- Never commit without passing lint + tests
