# Roadmap — Claude Best Practices Guide

**Current version:** v2.6 (2026-03-25, 118 pages)
**Status:** All 14 issues resolved. v2.6 complete.

---

## v2.6: Content Improvements — COMPLETE

| # | Item | Status | Issue |
|---|------|--------|-------|
| 1 | Ch05b renumbering | **Closed — won't fix** (cascading rename, cosmetic) | #1 |
| 2 | Pricing tables with date qualifier | **Done** | #2 |
| 3 | Property-based testing example (Hypothesis) | **Done** | #3 |
| 4 | MCP `claude mcp add` concrete example | **Done** | #4 |
| 5 | Ch02:61 convergence sourceurl | **Done** | #5 |
| 6 | Hierarchical index (~114 entries) | **Done** | #6 |
| 7 | Glossary appendix (~30 terms) | **Done** | #7 |
| 8 | "What's New in v2.5" reader-facing appendix | **Done** | #8 |
| 9 | Rich HTML citation dashboard | **Done** (`make citations`) | #9 |
| 10 | URL check expanded to 40 URLs | **Done** (`make check-urls`) | #10 |

## Ongoing Maintenance

| # | Item | Cadence | Issue | Notes |
|---|------|---------|-------|-------|
| 11 | Model release refresh (pricing, model names) | On release | #11 (closed) | ch04, ch12, ch14 model tables |
| 12 | Hook events delta check | Monthly | #12 (closed) | `make validate-hooks` vs live schema |
| 13 | Agent Teams graduation | On release | #13 (closed) | Remove experimental flag in ch09 |
| 14 | `/review` plugin coverage | When stable | #14 (closed) | Deprecated command → plugin ecosystem |

## Build Targets

```bash
make pilot         # Quick test build
make digital       # Full refs-resolved build
make validate      # All structural checks
make check-urls    # Verify all 40 unique URLs
make citations     # Generate HTML citation dashboard
make citations-check  # Citation dashboard with live URL verification
```

---

*Updated 2026-03-25. See CHANGELOG.md for version history.*
