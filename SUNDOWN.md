# Sunset — claude-best-practices

**Date**: 2026-04-18
**Final version**: v2.9 (tagged at HEAD 962be84)
**Status**: Maintenance-only. No new features.

## Why this sunset

The 2026-04-17 pivot decision moved forward-looking work on agentic
coding to a new repo with a different pedagogy:

> **Successor**: [book-template-astro](https://github.com/brandon-behring/book-template-astro) — *Agentic Coding: Principles and Practices*

The pivot was driven by:

- Scope drift in this repo toward Claude-specific trivia rather than
  transferable practice principles.
- Desire for a pedagogy (Koller-Friedman: Representation → Operation →
  Evolution) that demands a tool-agnostic framing the LaTeX single-tool
  structure couldn't accommodate.
- Need for structured data (YAML manifests for sources, patterns,
  changelog) that drive live features like freshness badges and
  convergence dashboards.

## What migrates conceptually

Two pieces of infrastructure from this repo survive in the new repo as
methodology, not file-copy:

### 1. Volatility watchlist → `sources/manifest.yaml` + freshness badges

- **Here**: `docs/volatility-watchlist.md` tracked hook events (monthly),
  pricing (per model release), URLs (monthly), certs (quarterly).
- **New repo**: `sources/manifest.yaml` entries carry `last_verified` +
  `tier`. Combined with per-chapter `volatility` classes, the same
  drift signal surfaces automatically as freshness badges on chapter
  headers.

### 2. Source hierarchy → `sourceTiers` taxonomy

- **Here**: `docs/source-hierarchy.md` mapped content to source origin
  (Anthropic official, practitioner discovery, convergence).
- **New repo**: `sourceTiers` enum in `src/content.config.ts` encodes
  T1-official / T2-release-notes / T3-practitioner / T4-conjecture.
  Methodology prose moves to the scaffold skill's
  `pedagogy/source-tiers.md`.

### 3. Skill ecosystem audit pattern

- **Here**: `docs/audits/skill_ecosystem_2026-04-01.md` is a one-off
  but valuable audit-doc shape.
- **New repo**: will adopt `docs/audits/` with a quarterly audit cadence
  post-v1.0.

### 4. Makefile drift-detection targets

- **Here**: `make validate-hooks` + `make check-urls` — still-useful
  automation tied to the LaTeX build.
- **New repo (post-v1.0)**: migrate as `scripts/validate-hooks.sh` +
  `scripts/check-urls.sh`, wire into CI.

## Maintenance posture

- **Quarterly**: verify pricing table accuracy; rebuild PDF if changed.
- **Monthly**: `make check-urls`.
- **Security-only patches**; no new features.
- **Feature requests**: route to
  [book-template-astro](https://github.com/brandon-behring/book-template-astro).

The repo remains discoverable (not archived) until the new book covers
equivalent content.

## Tags retroactively applied

- `v2.7` → `7981bf2` (feat: v2.7 — compaction deep dive)
- `v2.8` → `3cb1533` (feat: v2.8 — reference card expansion)
- `v2.9` → `962be84` (HEAD — final v2.9 snapshot including audit + rebuild)

Tags v2.6 and earlier were already in place.

## `extract_vibe_engineering.py` relocation

Moved from repo root to `research/extract_vibe_engineering.py`. This is
exploratory tooling (Docling PDF extraction of Manning's *Vibe
Engineering* MEAP v2) not part of the book build. `research/` is the
natural home for any future exploratory scripts.

---

*Sunset committed 2026-04-18. See
[book-template-astro](https://github.com/brandon-behring/book-template-astro)
for the successor project.*
