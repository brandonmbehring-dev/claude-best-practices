# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.5] - 2026-03-25

### Fixed
- Hook events: 21 → 24 (added StopFailure, CwdChanged, FileChanged) with full matcher values
- Hook handler types: 3 → 4 (added http) in Appendix C and source-hierarchy
- Permission modes: 5 → 6 (added auto research preview) in ch03, quickstart, Appendix C
- Keyboard shortcuts: Shift+Tab cycles enabled modes (not fixed 3), Ctrl+G opens text editor (not plan)
- /effort auto: added description (resets to model default)
- FedRAMP: separated government authorizations from commercial certifications in ch14
- 60% degradation threshold: qualified as practitioner heuristic vs ~83% auto-compaction trigger
- CLAUDE.md line count: cited both official numbers (200/file, ~500 total), reframed 300 as practitioner compromise
- Caching claims: added workload-dependent qualifiers
- Two broken URLs fixed (long-running-agents, GitHub Copilot blog)

### Added
- 1M context window strategy section in ch05 (durable artifacts, PreCompact hook, decision framework)
- /btw zero-context-cost side questions in ch05
- Fast mode (research preview) subsection in ch04
- /batch parallel codebase changes section in ch09
- Agent SDK expanded subsection with Python/TypeScript examples in ch12
- Scheduled tasks (3 tiers: Cloud, Desktop, /loop) in ch12
- GitHub Actions integration section in ch12
- Remote Control and Web Sessions section in ch12
- Code intelligence plugins expanded with before/after table in ch07
- Extended thinking + compaction interaction warning in ch05
- Durable artifacts subsection (CURRENT_WORK.md, plan docs, git commits) in ch05
- Appendix C: full ~50 command reference (built-in + bundled skills)

### Changed
- Page count: 94 → 109
- Appendix C restructured: built-in commands + bundled skills sections
- Blog summary updated to reflect v2.5 content
- Quickstart version/date updated to March 2026
- volatility-watchlist.md refreshed with corrections applied section
- CHANGELOG: added v2.4 and v2.5 entries

## [v2.4] - 2026-03-17

### Fixed
- P0 corrections from initial audit (effort levels, hooks, Copilot, subagents)
- Added \sourceurl{} to 33 unsourced [Official] callouts
- Harmonized heuristics with conditional language ("up to", "workload-dependent")

## [v2.3] - 2026-02-25

### Changed
- Quickstart guide: ground-up rewrite with action-first pedagogy
  - Three-act arc (Safety → Understanding → Ownership) with dual-track SE maturity
  - Imports `claude-best-practices.sty` for Tufte-style margins and visual language
  - 14 margin notes (vocab, cross-refs, official sources, tips, warnings)
  - 13 terminal transcripts ("You type: ..." → example output)
  - Safety nets (Esc, Esc+Esc, permission dialog) taught before first edit
  - Failure handling for top 3 first-launch issues
  - Three `\whybox` mindset transitions at act boundaries
  - Three agent-building observational callouts
  - Cherry-picks: agent loop TikZ, CLAUDE.md example, descriptions-vs-commands warnbox, commands table
  - Cuts: abstract properties, hooks JSON, phase-appropriate rigor, six traps (distilled to 3-item checklist)
- Style package: scrartcl compatibility guards for chapter-dependent commands

### Removed
- Quickstart: 95-line duplicated preamble (fonts, colors, boxes) — now imports shared sty
- Quickstart: abstract properties section, 6-layer validation table, hooks JSON example

## [v2.2] - 2026-02-25

### Added
- Plan Mode workflow (Explore→Plan→Implement→Commit) in Ch3
- Course-correction section (Esc, Esc+Esc, checkpoints) in Ch3
- Permission mode documentation (5 modes, Ctrl+G, --permission-mode plan) in Ch3
- Positive vs negative instructions tip in Ch2
- Status line zero-cost monitoring section in Ch5
- Session navigation (picker shortcuts, --from-pr, naming conventions) in Ch5
- Customizing compaction and checkpoint/rewind expansion in Ch5
- Claude Interview pattern (AskUserQuestion) in Ch5
- Rich content inputs (@-file, piping, URL allowlisting) in Ch4
- Boris Cherny verification attribution in Ch6
- Plugins, sandboxing, notification hooks, and CLI tools in Ch7
- MCP permission wildcards (mcp__server__*) in Ch7
- Code intelligence plugin expansion in Ch7
- Worktree expansion (before/after, subagent isolation, housekeeping) in Ch9
- "Infinite Exploration" anti-pattern (#8) in Ch11
- /debug and /status diagnostic margintip in Ch11
- Fan-out --allowedTools with glob scoping in Ch12
- Quickstart: "First 60 Minutes" time-marker framing, Plan Mode section, 6th trap
- Volatility watchlist with conditional claims tracking in docs/

### Changed
- Softened unsourced claims (3x→2-3x, 70%+ qualified) in Ch3, Ch14
- Reference card: added /debug, /plugin, /sandbox, Esc+Esc, permission footnote
- Blog summary updated to reflect all new content
- README updated with current page count (94 pages) and version
- Anti-pattern count: 7 → 8
- Page count: 87 → 94

### Removed
- Codex completeness notebooks (distilled into volatility watchlist)

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

[v2.5]: https://github.com/brandonmbehring-dev/claude-best-practices/compare/v2.4...v2.5
[v2.4]: https://github.com/brandonmbehring-dev/claude-best-practices/compare/v2.3...v2.4
[v2.3]: https://github.com/brandonmbehring-dev/claude-best-practices/compare/v2.2...v2.3
[v2.2]: https://github.com/brandonmbehring-dev/claude-best-practices/compare/v2.1...v2.2
[v2.1]: https://github.com/brandonmbehring-dev/claude-best-practices/compare/v2.0...v2.1
[v2.0]: https://github.com/brandonmbehring-dev/claude-best-practices/compare/v1.0...v2.0
[v1.0]: https://github.com/brandonmbehring-dev/claude-best-practices/releases/tag/v1.0
