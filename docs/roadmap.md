# Roadmap — Claude Best Practices Guide

**Current version:** v2.9 (2026-03-27)
**Next planned:** v3.0

---

## v2.7: Compaction Deep Dive + Stale Fixes — COMPLETE

- Two-phase compaction subsection (Ch. 5)
- PostCompact hook with JSON config (Ch. 5)
- CLAUDE.md sizing guidance: 200 lines/file, ~500 total (Ch. 5)
- CLAUDE_AUTOCOMPACT_PCT_OVERRIDE env var (Ch. 5)
- TaskCreated hook event added (Appendix C + valid-hook-events.txt)
- Hook count corrected: 24 → 25
- Auto permission mode: added --enable-auto-mode flag + Team plan prerequisite (Appendix C)
- Max output tokens added to pricing table: Opus 128K, Sonnet 64K, Haiku 64K (Ch. 14)
- What's New appendix restructured with v2.7 section

## v2.9: Env Vars, CLI Flags, Code Review Plugin — COMPLETE

- Environment variables reference: 26 key vars across 7 categories (Appendix C)
- CLI flags: +13 flags added to reference card (--agent, --agents, --mcp-config, --plugin-dir, --effort, --chrome, --remote, --teleport, --strict-mcp-config, --tools, --fallback-model, --dangerously-skip-permissions)
- Code-review plugin: expanded from 3-line deprecation notice to full architecture doc (4-agent parallel review with confidence scoring)
- 124 pages

## v2.8: Reference Card + Feature Gaps — COMPLETE

### Reference card updates (curated + footnote)

New commands (~8):
- `/copy [N]`, `/chrome`, `/keybindings`, `/terminal-setup`
- `/reload-plugins`, `/release-notes`, `/remote-env`, `/install-slack-app`

New CLI flags (~8):
- `--bare`, `--name`, `--max-turns`, `--max-budget-usd`
- `--system-prompt`, `--append-system-prompt`, `--json-schema`, `--enable-auto-mode`

Other:
- Footnote linking to official docs for complete command list
- Note `/review` deprecation → code-review plugin

### New prose sections (~1.5 pages)

| Section | Chapter | Scope |
|---------|---------|-------|
| `--bare` flag (scripted/SDK usage) | Ch. 12 (Automation) | ~0.5 page |
| Model comparison table (output limits, context, cutoffs) | Ch. 4 (Prompting) | ~0.5 page |
| Auto-mode prerequisites and behavior | Ch. 3 (First Session) | ~0.5 page |

### Deferred to v3.0+

**Real gaps:**
- IDE integration section: VS Code + JetBrains workflows (~1 page, Ch. 7)
- Server-managed settings: public beta, enterprise deployment (~0.5 page, Ch. 14)

**Nice-to-have:**
- Channels (`--channels`, research preview)
- `--json-schema` structured output (prose section)
- GitLab CI/CD (~0.5 page alongside GitHub Actions)
- Voice dictation prose (~0.5 page)
- Claude Code on the web (~0.5 page)

## v2.6: Content Improvements — COMPLETE

| # | Item | Status |
|---|------|--------|
| 1 | Ch05b renumbering | **Closed — won't fix** |
| 2 | Pricing tables with date qualifier | **Done** |
| 3 | Property-based testing example (Hypothesis) | **Done** |
| 4 | MCP `claude mcp add` concrete example | **Done** |
| 5 | Ch02:61 convergence sourceurl | **Done** |
| 6 | Hierarchical index (~114 entries) | **Done** |
| 7 | Glossary appendix (~30 terms) | **Done** |
| 8 | "What's New" reader-facing appendix | **Done** |
| 9 | Rich HTML citation dashboard | **Done** |
| 10 | URL check expanded to 40 URLs | **Done** |

## Ongoing Maintenance

| Item | Cadence | Notes |
|------|---------|-------|
| Model release refresh (pricing, model names) | On release | ch04, ch12, ch14 model tables |
| Hook events delta check | Monthly | `make validate-hooks` vs live schema |
| Agent Teams graduation | On release | Remove experimental flag in ch09 |
| `/review` plugin evolution | When stable | Deprecated → code-review plugin |
| Quarterly pricing verification | Quarterly | Verify ch14 table against platform.claude.com |

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

*Updated 2026-03-26. See CHANGELOG.md for version history.*
