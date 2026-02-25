# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.1] - 2026-02-24

### Added
- GitHub Actions CI workflow running `make validate` on push and PR
- `make validate` umbrella target with four blocking guards:
  - `validate-json` — JSON syntax check for all templates
  - `validate-hooks` — Hook event names vs `docs/valid-hook-events.txt` allowlist
  - `validate-includes` — Orphaned `.tex` file detection
  - `validate-no-deprecated` — Deprecated hook name grep guard
- `check-urls` informational target — spot-checks 5 critical Anthropic doc URLs
- `docs/volatility-watchlist.md` — tracks URLs likely to break
- `docs/source-hierarchy.md` — defines [Official]/[Practitioner]/[Convergence] sourcing rules
- DS/ML domain examples throughout (replaced SWE-only examples)
- Maturity calibration tags on all practices

### Fixed
- Hook event names normalized to official schema (`PreToolUse`, not `PreCommit`)
- Hook documentation tables corrected across all chapters
- Permission syntax guidance corrected (`Bash(*)` not `Bash(all)`)
- Cost/pricing claims verified against current Anthropic documentation
- Source URLs normalized and cited with footnotes
- Zero-warning LaTeX build (eliminated 48 errors, 12 warnings, 38 box messages)

### Removed
- Orphaned chapter files (`chapters/deprecated-*.tex`, v1 archive)
- Deprecated hook event names from all source files

## [v2.0] - 2026-02-23

### Added
- Complete pedagogical reorganization — workflow-organized teaching document
- Chapter 5 "Thinking Together" — prompt engineering and collaboration patterns
- Quickstart guide (`quickstart_guide.pdf`) — standalone 6-page onboarding PDF
- Skills section expansion with detailed examples
- DS/ML domain retargeting with data science examples

### Fixed
- TikZ step key conflict in diagram generation
- Zero-warning build target achieved

## [v1.0] - 2026-02-22

### Added
- Initial handbook (14 sections + 4 appendices)
- Self-contained Tufte-based LaTeX style (`claude-best-practices.sty`)
- Build system (Makefile with `pilot`/`digital` targets)
- Starter templates for CLAUDE.md, settings.json, hooks, commands, skills, agents, rules
- Blog summary extraction (Markdown in `blog/`)

[v2.1]: https://github.com/brandonmbehring-dev/claude-best-practices/compare/v2.0...v2.1
[v2.0]: https://github.com/brandonmbehring-dev/claude-best-practices/compare/v1.0...v2.0
[v1.0]: https://github.com/brandonmbehring-dev/claude-best-practices/releases/tag/v1.0
