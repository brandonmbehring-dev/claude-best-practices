---
paths: backend/**/*.py
---

# Backend Python Standards

<!-- WHY: The paths: frontmatter ensures these rules only load when
     editing backend Python files. Without it, they load globally
     and waste context when working on frontend or other modules. -->

- Use async/await for all I/O operations
- SQLAlchemy 2.0 query syntax (not legacy)
- Type hints on all function signatures
- Docstrings on all public functions
- Run `pytest backend/tests/` after changes
