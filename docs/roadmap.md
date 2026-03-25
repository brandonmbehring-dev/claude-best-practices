# Roadmap — Claude Best Practices Guide

**Current version:** v2.5 (2026-03-25, 109 pages)
**Status:** Audit complete. All P0/P1/P2 issues resolved across 6 phases.

---

## v2.6: Content Improvements

| # | Item | Effort | Chapter | Priority |
|---|------|--------|---------|----------|
| 1 | Ch05b renumbering — two files share "05" prefix | ~30 min | ch05 | Low |
| 2 | Pricing tables with date qualifier | ~1 hr | ch14 | Medium |
| 3 | Property-based testing example (Hypothesis) | ~20 min | ch06 | Medium |
| 4 | MCP `claude mcp add` concrete example | ~20 min | ch07 | Medium |
| 5 | Ch02:61 convergence sourceurl | ~2 min | ch02 | Low |

## v3.0: Structural Enhancements

| # | Item | Effort | Notes |
|---|------|--------|-------|
| 6 | Index generation (`\makeindex` + `\index{}`) | ~3 hr | 109 pages warrants a proper index |
| 7 | Glossary appendix | ~2 hr | Collect inline definitions (context budget, compaction, worktree, etc.) |
| 8 | "What's New in v2.5" reader-facing appendix | ~1 hr | Distinct from developer CHANGELOG |
| 9 | Interactive HTML companion with clickable source URLs | ~4 hr | 109 citations as footnotes in PDF is suboptimal |

## Ongoing Maintenance

| # | Item | Cadence | Notes |
|---|------|---------|-------|
| 10 | URL spot-check (all 39 unique URLs) | Quarterly | `make check-urls` covers 5; expand or manual |
| 11 | Model release refresh (pricing, model names) | On release | ch04, ch12, ch14 model tables |
| 12 | Hook events delta check | Monthly | `make validate-hooks` vs live schema |
| 13 | Agent Teams graduation | On release | Remove experimental flag caveat in ch09 |
| 14 | `/review` plugin coverage | When stable | Deprecated command → plugin ecosystem |

---

*Generated from audit plan 2026-03-25. See CHANGELOG.md for version history.*
