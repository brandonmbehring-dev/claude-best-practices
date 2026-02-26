# Plan: Color Scheme Redesign — "Warm Tol Hybrid"

**Status**: Implemented
**Date**: 2026-02-26
**Estimated scope**: ~500 lines across 9 files

## Objective

Replace the guide's 14 organically accumulated colors with a cohesive 5-hue system
combining Paul Tol's mathematically-proven color-distance relationships with Anthropic's
warm brand personality.

## Decisions Made

| # | Question | Answer | Rationale |
|---|----------|--------|-----------|
| 1 | Palette philosophy | Warm Tol Hybrid | Tol accessibility + Anthropic warmth |
| 2 | Background tint | !5 | Subtle but perceptible |
| 3 | Target medium | Screen PDF | Primary consumption method |
| 4 | Cover title color | Both variants | WarmBlue default + WarmRose toggle |
| 5 | Naming strategy | Full rename | No backward-compat aliases |
| 6 | Code highlighting | Custom minted style | `warmtol` Pygments style installed |
| 7 | Contrast check | During build | Visual spot-check, zero build errors |
| 8 | Color names | WarmX names | WarmBlue, WarmRose, WarmGreen, WarmPlum, WarmGold |

## New Palette

| Name | Hex | Semantic Role |
|------|-----|---------------|
| WarmBlue | #3B6FA0 | Structure, information, navigation |
| WarmRose | #C06858 | Attention, warnings, alerts |
| WarmGreen | #4A7E3F | Positive, growth, practitioner |
| WarmPlum | #8A4E82 | Authority, depth, official |
| WarmGold | #C09840 | Insight, convergence, reasoning |
| CodeBg | #F7F5F0 | Warm off-white code background |
| CodeFrame | #B5B3AA | Warm gray code border |
| DarkText | #1A1A19 | Body text |

## Files Modified

1. `claude-best-practices.sty` — All color definitions, box definitions, margin notes,
   practice labels, heading styles, hyperlinks, listings config, cover, maturitylevel
2. `chapters/00_preamble.tex` — Practice label colors in TikZ
3. `chapters/04_prompting.tex` — TikZ diagram colors
4. `chapters/07_extending.tex` — TikZ diagram colors
5. `chapters/08_claude_md_architecture.tex` — TikZ diagram colors
6. `chapters/10_projects.tex` — TikZ diagram colors
7. `appendices/maturity.tex` — TikZ diagram colors
8. `quickstart_guide.tex` — TikZ diagram colors + title
9. `warmtol_pygments/` — Custom Pygments style (new)

## Verification

- [x] `make pilot` — zero errors
- [x] `make quickstart` — zero errors
- [x] `make check` — zero errors, zero warnings, zero overfull
- [x] Grep for old color names — zero matches
- [ ] Visual spot-check of PDF (user)
- [ ] Compare WarmRose cover variant (user toggle: `\covertitlerose`)
