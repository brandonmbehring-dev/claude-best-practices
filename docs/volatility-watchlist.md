# Volatility Watchlist

Items that drift over time and need periodic manual verification.

## Quarterly Checks

### Hook Events
- **Source:** https://code.claude.com/docs/en/hooks
- **Local:** `docs/valid-hook-events.txt`
- **Action:** Compare allowlist against official docs; update if events added/removed
- **Automated:** `make validate-hooks` catches invalid events in templates

### Certifications & Compliance
- **Claims in:** `chapters/14_enterprise.tex`
- **Check:** SOC 2 Type II, HIPAA BAA, FedRAMP High, IL5
- **Action:** Re-verify status on anthropic.com/trust

### Government Programs
- **Claims in:** `chapters/14_enterprise.tex`
- **Check:** FedRAMP High authorization status
- **Action:** Search marketplace.fedramp.gov for current status

## On Model Release

### Pricing
- **Claims in:** `chapters/14_enterprise.tex` (cost comparison table)
- **Source:** https://platform.claude.com/docs/en/about-claude/pricing
- **Action:** Verify $/MTok figures for all listed models
- **Risk:** Pricing changes with every model generation

## Monthly Checks

### URLs
- **Automated:** `make check-urls` (5 critical documentation URLs)
- **Manual:** Spot-check 2-3 partnership/news URLs from enterprise chapter
- **Action:** Fix or annotate any broken links

## Corrections Applied (v2.5, 2026-03-25)

Codex notebooks flagged these as potentially outdated. Two were confirmed correct;
two were corrected in v2.5 after live-doc verification:

- **Shift+Tab cycles enabled permission modes**: Corrected in v2.5. Previously
  described as a fixed 3-mode loop (Normal → Auto-Accept → Plan). Live docs confirm
  it cycles through ALL enabled modes, which can include \code{auto} and others.
- **Ctrl+G opens prompt in default text editor**: Corrected in v2.5. Previously
  described as "opens plan in external editor." Live docs confirm it opens the
  current prompt or custom response in the system's default text editor.
- **Alt+T toggles extended thinking**: Confirmed correct in official docs.
- **Ctrl+B backgrounds a running task**: Confirmed correct in official docs.

## New URLs Added (v2.2, 2026-02-25)

These URLs were added in the Phases 2-3 content update and should be monitored:

| URL | Used in | Claim |
|-----|---------|-------|
| https://code.claude.com/docs/en/statusline | ch05 (status line) | Status line is customizable, zero API tokens |
| https://code.claude.com/docs/en/common-workflows | ch09 (worktrees), ch07 (notification, plugins) | Worktree lifecycle, notification hooks, code intelligence |
| https://code.claude.com/docs/en/permissions | ch03, ref card (permission modes) | Six permission modes, MCP wildcard syntax |
| https://code.claude.com/docs/en/best-practices | ch04 (rich inputs), ch12 (allowedTools) | @file references, --allowedTools scoping |

## Conditional Claims (Need Re-verification on Major Updates)

These claims use conditional language ("up to", "workload-dependent") and reference
official maximums. Re-verify if Anthropic changes pricing or caching behavior:

- **Prompt caching up to 90%**: ch04, ch14
- **Batch API 50% discount**: ch04, ch14
- **Combined up to 70%+ savings**: ch04, ch14
- **Up to 60-80% per-session cost reduction via caching**: ch04

## Codex Notebook Provenance

Insights from two codex notebooks were distilled into this watchlist and the
implementation plan (2026-02-25). The notebooks themselves have been removed:
- `codex_claude_guides_completeness_notebook.md` — coverage audit, accuracy checks
- `codex_quickstart_principles_quickwins_notebook.md` — narrative flow, quick-win structure

Key insights preserved:
- Permission mode model has 6 modes, not 3 (addressed: footnote + margin note added)
- Numeric claims needed conditional language (addressed: "up to", "workload-dependent")
- Quickstart benefits from "First 60 Minutes" time-marker framing (addressed)
- All handbook URLs returned HTTP 200 at time of v2.2 audit (39 unique URLs verified again for v2.5)

## Validation Commands

```bash
make validate          # All structural checks (JSON, hooks, includes, deprecated)
make check-urls        # URL reachability (informational)
```
