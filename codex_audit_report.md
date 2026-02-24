# Codex Audit Report: `claude-best-practices`

Date: 2026-02-24

## Scope
I audited the full content set in `/home/brandon_behring/Claude/claude-best-practices` (chapters, appendices, templates, README/blog/source index), focusing on:
- factual accuracy vs current official docs,
- methodology quality,
- missing or overlooked guidance,
- citation health.

## Methodology
- Read all authored content and templates in-repo.
- Verified claims against current primary sources (Anthropic docs, support/privacy, and first-party announcements).
- Ran link-health checks on cited URLs.
- Classified findings by severity and implementation risk.

## Executive Assessment
- **Overall quality:** solid framework and high practical value, but evidence hygiene has drifted.
- **Biggest risk:** several copy-paste examples now conflict with current Claude Code schema, so readers may implement broken configs.
- **Credibility risk:** some enterprise/government claims are under-cited, stale, or tied to mismatched sources.

## High-Severity Findings

| ID | Finding | Why it matters | Repo evidence | Corrective direction |
|---|---|---|---|---|
| H1 | **Hook event model is outdated in multiple files.** | Hook configs may fail or not run as intended. | `chapters/02_extensions.tex` (events table + JSON examples), `appendices/reference_card.tex`, `templates/hook-examples.json` | Update to current hook events (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `Stop`, `SubagentStart`, `SubagentStop`, `PreCompact`, etc.) and current matcher-based schema.[2] |
| H2 | **Skill/subagent frontmatter keys are stale (`allowed_tools`).** | Users copying templates can get invalid configs. | `templates/skill-template.md`, `templates/subagent-template.md`, `chapters/02_extensions.tex` examples | For skills use `allowed-tools`; for subagents use `tools` (plus supported fields like `disallowedTools`, `permissionMode`, `memory`, etc.).[3][4] |
| H3 | **Permission pattern syntax likely mismatched (`Bash(git push:*)` style).** | Security controls can silently fail to match intended commands. | `templates/settings.json`, `appendices/templates.tex`, `chapters/01_configuration.tex` examples | Normalize to documented rule style (`Bash(git push *)`, etc.) and add test examples for deny/ask precedence.[5] |
| H4 | **Batch API limits are inaccurate.** | Planning/cost assumptions can be wrong for large automation jobs. | `chapters/04_prompting.tex:149-151` ("up to 10,000 requests") | Current docs specify up to **100,000 requests or 256 MB**, with 24h expiry semantics.[10] |
| H5 | **Enterprise data-training claim uses mismatched citation.** | High-stakes trust/compliance language needs precise sourcing. | `chapters/13_enterprise.tex:46` cites consumer retention article | Cite commercial training/retention docs directly (commercial products are not trained on by default unless opted in; separate retention policy details).[15][16][17] |
| H6 | **Government section includes claims not supported by current linked page (e.g., free 1-year plan language).** | Buyer-facing inaccuracies can undermine the guide. | `chapters/13_enterprise.tex:103-113` | Revalidate against current government page and remove unverifiable historical claims.[18] |
| H7 | **MCP ecosystem numbers are likely stale/unverified (10,000 servers, 100M downloads).** | Inflated ecosystem claims erode trust. | `chapters/09_mcp.tex:13` | Keep only claims documented in current MCP docs or cite a primary MCP stats source directly.[7] |
| H8 | **At least one key source link is broken (soft-404).** | Weakens reproducibility and citation integrity. | `appendices/sources.tex` Cognizant URL | Replace or remove broken references; run automated URL checks in CI. |

## Medium-Severity Findings

| ID | Finding | Repo evidence | Corrective direction |
|---|---|---|---|
| M1 | `/status` is presented as the main context-usage command; current docs expose `/context` for usage visualization. | `chapters/03_context.tex:36-39` | Shift guidance to `/context` for usage and keep `/status` for version/model/account diagnostics.[6] |
| M2 | Some hard-threshold statements are overconfident (for example, deterministic "500 lines causes silent deprioritization"). | `chapters/01_configuration.tex:31`, `chapters/11_antipatterns.tex:19-23` | Reword as heuristic guidance with uncertainty language and doc-aligned phrasing.[1][3] |
| M3 | "User prompts are followed more reliably than system prompts" is risky framing. | `chapters/04_prompting.tex:61-64` | Reframe toward role separation and instruction clarity, not precedence claims absent direct support.[12] |
| M4 | Commands vs skills taxonomy drift: docs now treat command files as skill-compatible workflow artifacts. | `chapters/02_extensions.tex` | Update extension model narrative to current docs while noting backward compatibility.[3] |
| M5 | Competitive positioning table includes strong comparative assertions without primary citations. | `chapters/13_enterprise.tex:176-183` | Either source each comparative statement or remove hard claims and present as "decision heuristics." |
| M6 | Enterprise case-study metrics include unsourced values (for example, ServiceNow row) and mixed provenance. | `chapters/13_enterprise.tex:126-132` | Keep only metrics with direct source links in `appendices/sources.tex`; add per-row citation IDs.[19][20][21][22] |

## Low-Severity Findings

| ID | Finding | Repo evidence | Corrective direction |
|---|---|---|---|
| L1 | Several `[Official]` statements lack direct source URLs in-line. | e.g., `chapters/03_context.tex:110`, `chapters/01_configuration.tex:207` | Require URL for every official assertion, even if repeated. |
| L2 | Source appendix is broad but not claim-addressable. | `appendices/sources.tex` | Add claim IDs (e.g., `C13-04`) mapped to exact source links and verification date. |

## What You Got Right
- Strong practitioner framing and usable workflows.
- Clear separation of `[Official]`, `[Practitioner]`, `[Convergence]` is excellent and should be preserved.
- Context hygiene emphasis is directionally aligned with current Claude Code guidance.[1][6]
- Cost section direction (prompt caching + batch + model right-sizing) is broadly correct, though some numbers/details need tightening.[9][10][11]

## Overlooked Areas (Current Best-Practice Additions)
1. **Evidence-grade system:** tag each claim as `official-doc`, `official-announcement`, `benchmark`, or `practitioner`, with last-verified date.
2. **Automated citation checks:** CI job for URL health + domain allowlist + stale-date warnings.
3. **Versioned volatility watchlist:** pricing, model support, context-window constraints, plan features, and compliance status should have short refresh cadence (weekly/monthly).
4. **Schema regression tests for templates:** small validation harness that checks template fields against current docs schemas (skills/subagents/hooks/settings).
5. **Enterprise claim governance:** no uncited numeric claims in buyer-facing chapters.

## Current Best-Practice Snapshot (as of 2026-02-24)
- Use `/init`, keep `CLAUDE.md` concise, and use rules/skills for modular instructions.[1][3][8]
- Prefer current hook schema with matchers and supported lifecycle events.[2]
- Define skills as `.../.claude/skills/<name>/SKILL.md` with frontmatter like `allowed-tools` and optional invocation controls.[3]
- Define subagents with `tools` and modern frontmatter (`permissionMode`, `skills`, `memory`, `isolation`, etc.).[4]
- For MCP scale, rely on tool search behavior and configure thresholds with `ENABLE_TOOL_SEARCH` when needed.[7]
- Batch API discount and prompt caching stack, but use current hard limits (100k requests/256MB/24h behavior) and current pricing tables.[9][10][11]
- For enterprise privacy/security claims, separate consumer vs commercial documentation and cite the commercial privacy pages for training/retention commitments.[15][16][17]

## Prioritized Remediation Plan
1. **Fix schema-breaking templates first (H1-H3).**
2. **Repair enterprise/government accuracy and citation mismatches (H5-H8).**
3. **Refactor high-volatility claims into a versioned facts appendix with verification timestamps.**
4. **Add CI validation for links + schema snippets + claim IDs.**
5. **Do a final editorial pass to downgrade absolute language where evidence is heuristic.**

## References
[1] https://docs.anthropic.com/en/docs/claude-code/best-practices
[2] https://docs.anthropic.com/en/docs/claude-code/hooks-guide
[3] https://docs.anthropic.com/en/docs/claude-code/skills
[4] https://docs.anthropic.com/en/docs/claude-code/sub-agents
[5] https://docs.anthropic.com/en/docs/claude-code/settings
[6] https://docs.anthropic.com/en/docs/claude-code/interactive-mode
[7] https://docs.anthropic.com/en/docs/claude-code/mcp
[8] https://docs.anthropic.com/en/docs/claude-code/memory
[9] https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[10] https://platform.claude.com/docs/en/build-with-claude/batch-processing
[11] https://platform.claude.com/docs/en/about-claude/pricing
[12] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
[13] https://platform.claude.com/docs/en/build-with-claude/extended-thinking
[14] https://platform.claude.com/docs/en/build-with-claude/context-windows
[15] https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan
[16] https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan
[17] https://privacy.claude.com/en/articles/7996885-how-do-you-use-personal-data-in-model-training
[18] https://claude.com/solutions/government
[19] https://www.anthropic.com/news/deloitte-anthropic-partnership
[20] https://www.anthropic.com/news/anthropic-accenture-partnership
[21] https://www.anthropic.com/news/snowflake-anthropic-expanded-partnership
[22] https://www.anthropic.com/customers/telus
[23] https://privacy.claude.com/en/articles/10015870-what-certifications-has-anthropic-obtained
