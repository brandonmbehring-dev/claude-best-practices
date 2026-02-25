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
- **Check:** SOC 2 Type II, HIPAA BAA, FedRAMP (in progress)
- **Action:** Re-verify status on anthropic.com/trust

### Government Programs
- **Claims in:** `chapters/14_enterprise.tex`
- **Check:** FedRAMP Moderate authorization status
- **Action:** Search marketplace.fedramp.gov for current status

## On Model Release

### Pricing
- **Claims in:** `chapters/14_enterprise.tex` (cost comparison table)
- **Source:** https://docs.anthropic.com/en/docs/about-claude/models
- **Action:** Verify $/MTok figures for all listed models
- **Risk:** Pricing changes with every model generation

## Monthly Checks

### URLs
- **Automated:** `make check-urls` (5 critical documentation URLs)
- **Manual:** Spot-check 2-3 partnership/news URLs from enterprise chapter
- **Action:** Fix or annotate any broken links

## Validation Commands

```bash
make validate          # All structural checks (JSON, hooks, includes, deprecated)
make check-urls        # URL reachability (informational)
```
