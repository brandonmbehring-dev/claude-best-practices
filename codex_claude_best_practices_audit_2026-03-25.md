# Codex Audit: Claude Best Practices Repo vs Current Claude Code Guidance

Date: 2026-03-25
Repo: `claude-best-practices`
Auditor: Codex

## Executive Summary

Overall verdict: the repo is directionally strong on stable Claude Code practice, but it is not current enough to claim full March 25, 2026 accuracy without edits.

| Dimension | Verdict | Notes |
|---|---|---|
| Stable workflow advice | Strong | CLAUDE.md-first configuration, `/init`, verification-first, `/clear` vs `/compact`, status line, hooks, worktrees, and subagents are mostly aligned with current Anthropic guidance. |
| Volatile product-surface facts | Needs refresh | Hook events, permission modes, shortcut behavior, enterprise compliance wording, and model/version language have drifted. |
| Completeness | Mixed | Strong on setup, testing, and extension patterns; weaker on durable-state artifacts for long-running work and on exact 1M-context wording. |
| Publication readiness | Not yet | Correct P0/P1 drift before calling the repo "verified" as of 2026-03-25. |

Most important findings:

1. `P0`: hook inventory material is stale and internally inconsistent. Live Claude Code docs show 22 hook events, including `StopFailure`; `docs/source-hierarchy.md` still says 17 plus `Setup`, and `docs/valid-hook-events.txt` has 21 and omits `StopFailure`. `[S6]`
2. `P0`: permission-mode and shortcut guidance is stale. Live docs now show six permission modes, `Shift+Tab` / `Alt+M` cycle enabled modes, and `Ctrl+G` opens the default text editor for prompt/custom-response editing rather than "the current plan." `[S3][S4]`
3. `P1`: enterprise/compliance wording overstates current commercial documentation by listing `FedRAMP High` as an Anthropic certification in the enterprise chapter and blog. Current commercial certification docs do not list it. `[S19]`
4. `P1`: model/version wording needs exact March 25, 2026 language. In Claude Code, the current aliases are `sonnet[1m]` and `opus[1m]`; platform docs say Claude Opus 4.6 and Claude Sonnet 4.6 have 1M-token context windows. `[S9][S12]`
5. `P1`: several numeric thresholds are useful heuristics but are presented too close to hard facts: `60%`, `60-70%`, `70%`, `100`, `200`, `300`, `500`, and `~2,500 tokens`. Anthropic docs support proactive context management and concise CLAUDE.md files, but not one universal numeric rule. `[S1][S5][S10][S17][S18]`
6. `P1`: long-task guidance should emphasize durable artifacts more strongly than compaction alone. Anthropic's long-running-agent guidance explicitly says compaction is not sufficient by itself. `[S18]`

Publication recommendation: do not market the repo as fully "verified against Anthropic docs" until the hook, permissions, enterprise, and model-version fixes below are applied.

## Scope and Method

Primary repo corpus included:

- handbook chapters in `chapters/`
- `quickstart_guide.tex`
- `README.md`
- `blog/blog-summary.md`
- repo-local `.claude/CLAUDE.md`
- `docs/source-hierarchy.md`
- `docs/valid-hook-events.txt`
- `docs/volatility-watchlist.md`
- advice-bearing files in `templates/`

Excluded from the primary corpus:

- archived plans in `docs/plans/**`
- generated or third-party extracted materials such as `vibe_engineering_extracted/**`
- release PDFs and build outputs
- pure implementation shell snippets without standalone normative guidance, unless referenced by a prose template

Audit unit:

- one row per advice-bearing claim block, with mirrored or near-verbatim repo occurrences grouped into the same row and each occurrence listed in the `Repo source(s)` cell

Cross-check method:

1. Read the repo claim block in context.
2. Resolve it against live Anthropic sources.
3. Cross-check with multiple local `~/Claude/*` documents.
4. Downgrade unsupported or heuristic material even if multiple low-authority local notes repeat it.

I also ran the requested non-mutating checks:

- `make validate` -> PASS
- `make check-urls` -> PASS

## Source Authority and Currency Note

Authority model used in this audit:

- `A1`: `code.claude.com` product docs for Claude Code behavior
- `A2`: `platform.claude.com` plus Anthropic support/privacy docs for model, SDK, pricing, plan, and commercial/legal claims
- `A3`: Anthropic engineering/blog posts for operational patterns and long-running-agent guidance
- `A4`: repo-internal notes such as `docs/source-hierarchy.md`
- `A5`: other `~/Claude/*` working notes and repo-local operational docs
- `A6`: archived/generated/course-note material

When sources conflicted, `A1`/`A2` overruled `A4`-`A6`. No decisive verdict below depends solely on `A5` or `A6`.

### External Source Registry

| ID | Source | Authority | Currency |
|---|---|---|---|
| S1 | Claude Code best practices: https://code.claude.com/docs/en/best-practices | A1 | Accessed 2026-03-25 |
| S2 | Claude Code commands: https://code.claude.com/docs/en/commands | A1 | Accessed 2026-03-25 |
| S3 | Claude Code interactive mode: https://code.claude.com/docs/en/interactive-mode | A1 | Accessed 2026-03-25 |
| S4 | Claude Code permissions: https://code.claude.com/docs/en/permissions | A1 | Accessed 2026-03-25 |
| S5 | Claude Code memory: https://code.claude.com/docs/en/memory | A1 | Accessed 2026-03-25 |
| S6 | Claude Code hooks: https://code.claude.com/docs/en/hooks | A1 | Accessed 2026-03-25 |
| S7 | Claude Code common workflows: https://code.claude.com/docs/en/common-workflows | A1 | Accessed 2026-03-25 |
| S8 | Claude Code settings: https://code.claude.com/docs/en/settings | A1 | Accessed 2026-03-25 |
| S9 | Claude Code model config: https://code.claude.com/docs/en/model-config | A1 | Accessed 2026-03-25 |
| S10 | Claude Code costs: https://code.claude.com/docs/en/costs | A1 | Accessed 2026-03-25 |
| S11 | Claude Code status line: https://code.claude.com/docs/en/statusline | A1 | Accessed 2026-03-25 |
| S22 | Claude Code skills: https://code.claude.com/docs/en/skills | A1 | Accessed 2026-03-25 |
| S23 | Claude Code sub-agents: https://code.claude.com/docs/en/sub-agents | A1 | Accessed 2026-03-25 |
| S24 | Claude Code agent teams: https://code.claude.com/docs/en/agent-teams | A1 | Accessed 2026-03-25 |
| S25 | Claude Code plugins: https://code.claude.com/docs/en/plugins | A1 | Accessed 2026-03-25 |
| S26 | Claude Code sandboxing: https://code.claude.com/docs/en/sandboxing | A1 | Accessed 2026-03-25 |
| S27 | Claude Code MCP: https://code.claude.com/docs/en/mcp | A1 | Accessed 2026-03-25 |
| S12 | Claude API context windows: https://platform.claude.com/docs/en/build-with-claude/context-windows | A2 | Accessed 2026-03-25 |
| S13 | Claude API prompt caching: https://platform.claude.com/docs/en/build-with-claude/prompt-caching | A2 | Accessed 2026-03-25 |
| S14 | Claude API batch processing: https://platform.claude.com/docs/en/build-with-claude/batch-processing | A2 | Accessed 2026-03-25 |
| S15 | Claude API extended thinking: https://platform.claude.com/docs/en/build-with-claude/extended-thinking | A2 | Accessed 2026-03-25 |
| S16 | Claude Agent SDK user input: https://platform.claude.com/docs/en/agent-sdk/user-input | A2 | Accessed 2026-03-25 |
| S17 | Anthropic engineering, effective context engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | A3 | Published 2025-09-29; accessed 2026-03-25 |
| S18 | Anthropic engineering, effective harnesses for long-running agents: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | A3 | Published 2025-11-26; accessed 2026-03-25 |
| S19 | Anthropic privacy, certifications: https://privacy.claude.com/en/articles/10015870-what-certifications-has-anthropic-obtained | A2 | Updated over a week ago; accessed 2026-03-25 |
| S20 | Anthropic privacy, model-training policy: https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training | A2 | Updated over a week ago; accessed 2026-03-25 |
| S21 | Anthropic support, Team/Enterprise Claude Code access: https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan | A2 | Updated over a week ago; accessed 2026-03-25 |

### Local Corroboration Registry

| ID | Local source | Authority | Use in this audit |
|---|---|---|---|
| L1 | `/home/brandon_behring/Claude/lever_of_archimedes/docs/guides/PROMPT_TO_CONTEXT_QUICKSTART.md` | A5 | Supports CLAUDE.md-first and context hygiene; also repeats unsupported hard numbers like `95% -> 60%` accuracy and `100 lines`, so it was used only as corroboration, not control. |
| L2 | `/home/brandon_behring/Claude/lever_of_archimedes/docs/reference/PATTERNS_QUICK_REFERENCE.md` | A5 | Supports `/clear`, `/compact`, and current-work artifacts; repeats `70%` and `100-200 lines` heuristics. |
| L3 | `/home/brandon_behring/Claude/lever_of_archimedes/docs/reference/CONTEXT_ENGINEERING_BOOK_FEEDBACK_CODEX.md` | A5 | Useful corroborant on exact model/version caution and handoff artifacts. |
| L4 | `/home/brandon_behring/Claude/annuity-price-elasticity-v3/docs/onboarding/USING_CLAUDE_CODE.md` | A5 | Supports CLAUDE.md, `/clear`, and `/compact` usage from another active repo. |
| L5 | `/home/brandon_behring/Claude/annuity-price-elasticity-v2/docs/onboarding/USING_CLAUDE_CODE.md` | A5 | Same as L4; additional corroboration from a separate repo version. |

## Prioritized Findings

### P0. Fix hook inventory and validation material before claiming current accuracy

Affected files:

- `docs/source-hierarchy.md`
- `docs/valid-hook-events.txt`
- `chapters/07_extending.tex`

Why this is high risk:

- live Claude Code docs currently expose 22 hook events, including `StopFailure` `[S6]`
- `docs/source-hierarchy.md` still says 17 events plus `Setup`
- `docs/valid-hook-events.txt` has 21 events and omits `StopFailure`
- `chapters/07_extending.tex` omits `StopFailure` and describes `PostCompact` as having no matcher, while the live docs say it shares the `manual|auto` trigger matcher with `PreCompact` `[S6]`

Exact replacement wording:

```text
As of March 25, 2026, Claude Code documents 22 hook events, including `StopFailure`.
The current set is: SessionStart, InstructionsLoaded, UserPromptSubmit, PreToolUse,
PermissionRequest, PostToolUse, PostToolUseFailure, Notification, Elicitation,
ElicitationResult, SubagentStart, SubagentStop, Stop, StopFailure, TeammateIdle,
TaskCompleted, ConfigChange, WorktreeCreate, WorktreeRemove, PreCompact,
PostCompact, and SessionEnd.
```

### P0. Update permission-mode and shortcut guidance everywhere it appears

Affected files:

- `chapters/03_first_session.tex`
- `quickstart_guide.tex`
- `docs/source-hierarchy.md`
- `docs/volatility-watchlist.md`
- `blog/blog-summary.md`

Why this is high risk:

- live docs currently list six modes: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` `[S4]`
- `Shift+Tab` / `Alt+M` cycle enabled modes, not a fixed three-mode loop `[S3][S4]`
- `Ctrl+G` currently opens the default text editor for prompt/custom-response editing, not "the current plan" `[S3]`

Exact replacement wording:

```text
As of March 25, 2026, Claude Code documents six permission modes:
`default`, `acceptEdits`, `plan`, `auto` (research preview),
`dontAsk`, and `bypassPermissions`.
`Shift+Tab` or `Alt+M` cycles through the modes you have enabled.
`Ctrl+G` opens the default text editor for prompt/custom-response editing.
```

### P1. Remove or rescope `FedRAMP High` from the commercial certification list

Affected files:

- `chapters/14_enterprise.tex`
- `blog/blog-summary.md`

Why this matters:

- current commercial certification docs list HIPAA-ready configuration, ISO 27001:2022, ISO/IEC 42001:2023, and SOC 2 Type I & II `[S19]`
- they do not list `FedRAMP High`
- government-program marketing pages are not the same thing as Anthropic's current commercial certification inventory

Exact replacement wording:

```text
For Anthropic commercial products, current published compliance credentials
include HIPAA-ready configuration (BAA available), ISO 27001:2022,
ISO/IEC 42001:2023, and SOC 2 Type I & II.
Do not list `FedRAMP High` here unless you clearly scope it to a separate,
current government-specific offering and cite the relevant source.
```

### P1. Pin all 1M-context guidance to exact current models and date

Affected files:

- `chapters/04_prompting.tex`
- `chapters/14_enterprise.tex`
- `blog/blog-summary.md`
- any future README or release text describing "1M Opus"

Why this matters:

- Claude Code model-config docs currently expose `sonnet[1m]` and `opus[1m]` aliases `[S9]`
- platform docs say Claude Opus 4.6 and Claude Sonnet 4.6 have 1M-token context windows `[S12]`
- vague wording such as "1M Opus" ages badly across model releases

Exact replacement wording:

```text
As of March 25, 2026, Claude Code exposes `sonnet[1m]` and `opus[1m]`
for long sessions. Anthropic's platform docs state that Claude Opus 4.6
and Claude Sonnet 4.6 have 1M-token context windows.
Use exact model names and the verification date whenever this is mentioned.
```

### P1. Reframe hard numbers as heuristics, not official thresholds

Affected files:

- `chapters/05_context.tex`
- `quickstart_guide.tex`
- `chapters/08_claude_md_architecture.tex`
- `blog/blog-summary.md`
- several templates and local `~/Claude/*` notes

Why this matters:

- Anthropic officially recommends proactive context management and concise CLAUDE.md files `[S1][S5][S10]`
- Anthropic does not publish one universal "quality drops at 60%" rule
- current official CLAUDE.md guidance says target under 200 lines per file `[S5]`, while Claude Code cost docs also say to aim under about 500 lines by keeping only essentials `[S10]`

Recommended replacement wording:

```text
Treat 60-70% context usage and 200-300 CLAUDE.md lines as practitioner heuristics,
not product guarantees. Use them as early-warning thresholds, then verify with
your actual session quality, `/context`, and the status line.
```

### P1. Strengthen long-task guidance around durable artifacts, not just compaction

Affected files:

- `chapters/05_context.tex`
- `chapters/09_agents_parallel.tex`
- `chapters/10_projects.tex`
- `blog/blog-summary.md`

Why this matters:

- Anthropic's long-running-agent guidance explicitly says compaction is not sufficient by itself and recommends leaving clear artifacts for the next session `[S18]`
- Anthropic's context-engineering guidance also stresses that long-context success depends on what is in context, not just how much fits `[S12][S17]`

Recommended addition:

- explicit handoff artifacts: `CURRENT_WORK.md`, plan docs, failing-test lists, structured progress files, and git history
- more direct guidance to push verbose exploration into subagents and parallel file changes into worktrees

## Direct Answer: Intelligent Compaction and 1M Opus

Short answer: 1M Opus gives you more headroom, not a license to carry stale context. The best compaction strategy is still to keep the live session narrow, instruct compaction deliberately, and externalize durable state.

As of March 25, 2026:

- Claude Code exposes `sonnet[1m]` and `opus[1m]` for long sessions `[S9]`
- Anthropic's platform docs state that Claude Opus 4.6 and Claude Sonnet 4.6 have 1M-token context windows `[S12]`
- Anthropic's own long-running-agent guidance says compaction helps but is not sufficient on its own for multi-window work `[S18]`

Best practice:

1. Use `/clear` between unrelated tasks. This is still the cleanest way to prevent stale context from polluting future work. `[S1][S10]`
2. Use `/compact [instructions]` when you are staying on the same task and want continuity. Example: `/compact Preserve modified files, failed tests, open blockers, and next step.` `[S2][S10]`
3. Use partial summarization when only the tail of the conversation is noisy. `Esc` + `Esc` or `/rewind` lets you summarize from a selected message instead of compacting the whole session. `[S2]`
4. Put compaction instructions in `CLAUDE.md` so the summary preserves the same project-specific state every time. `[S10]`
5. Offload verbose search, exploration, and comparison work to subagents. Anthropic explicitly recommends subagents and separate sessions to reduce context pollution. `[S1][S7][S10]`
6. Use worktrees or separate sessions for parallel changes, not one giant omniscient thread. `[S7]`
7. Store durable state outside the context window. Anthropic's long-running-agent guidance recommends leaving clear artifacts; that matters even with 1M context. `[S18]`

Recommended durable artifacts for this repo and similar repos:

- `CURRENT_WORK.md` with current goal, last verified state, modified files, blocker, and next step
- plan/spec docs for large tasks
- explicit test-status notes such as "last full suite result" and "known failing cases"
- git commits and branch/worktree naming that make rollback and resumption obvious

Recommended `CLAUDE.md` compaction block:

```markdown
## Compact instructions
When compacting, preserve:
- current goal and acceptance criteria
- modified files and why they changed
- last test command and result
- open blockers or unanswered questions
- exact next step
- branch, worktree, or PR context if relevant
```

What not to do:

- do not rely on the model to remember tacit intent across many windows
- do not treat 1M context as a substitute for handoff artifacts
- do not keep unrelated exploratory dead ends in the main thread just because they still fit

Best one-line rule:

- use `1M` for headroom, `/compact` for same-task continuity, `/clear` for task boundaries, and files plus git for real memory

## Validation Results

### `make validate`

Result: PASS

Notable output:

- `validate-json`: PASS
- `validate-hooks`: PASS
- `validate-includes`: PASS
- `validate-no-deprecated`: PASS
- `validate-doc-claims`: PASS
- the doc-claims validation output already flags model references as version-sensitive, which supports this audit's recommendation to pin exact model/version/date wording

### `make check-urls`

Result: PASS

All sampled URLs returned HTTP `200`. One repo-specific note: the README still says `check-urls` spot-checks five URLs, but the current target set is larger than that.

## Exhaustive Claim Matrix

Method note: this matrix is exhaustive at the claim-block level. Mirrored handbook/blog/template occurrences are grouped into the same row, with every repo occurrence listed in the `Repo source(s)` cell.

### Meta, Source Discipline, and Repo Operations

| Repo source(s) | Claim summary | Class | Topic | Verdict | Why | Primary external citation(s) | Local corroborants / contradictions | Authority | Dates | Recommended fix |
|---|---|---|---|---|---|---|---|---|---|---|
| `README.md:20`<br>`README.md:31`<br>`README.md:93`<br>`chapters/00_preamble.tex:11`<br>`chapters/00_preamble.tex:87`<br>`blog/blog-summary.md:9`<br>`blog/blog-summary.md:230` | Repo taxonomy (`Official` / `Practitioner` / `Convergence`) and "verified as of February 2026" framing | Official meta | source discipline | accurate but stale | The tagging model is coherent, but the verification date is stale as of 2026-03-25. | S1-S21 | L1-L5 show why stale dates matter in fast-moving Claude docs. | A1/A2 > A4/A5 | Repo says Feb 2026; audit access date 2026-03-25 | Refresh all "verified as of" markers to the actual audit date and link the source registry. |
| `README.md:60`<br>`README.md:73`<br>`docs/volatility-watchlist.md:33`<br>`docs/volatility-watchlist.md:83` | Validation and URL-check coverage claims | Official repo ops | validation | incomplete | `make validate` currently includes `validate-doc-claims`, which the README omits. `make check-urls` checks more than five URLs in current practice. | n/a; validated by local run in this audit | n/a | A4 | Local execution on 2026-03-25 | Update the README validation table to match actual targets and current URL-check scope. |
| `.claude/CLAUDE.md:10` | Writing rule: all Anthropic claims include source URLs; content is carefully tagged and structured | Official repo process | editorial discipline | partially accurate | The repo usually cites sources, but several volatile claims are now stale or over-precise without exact date/version language. | S1-S21 | L1-L3 reinforce the need to date volatile claims. | A2/A4 | Accessed 2026-03-25 | Add an explicit rule requiring exact dates for model/version/permissions/compliance claims. |
| `docs/source-hierarchy.md:7`<br>`docs/source-hierarchy.md:20`<br>`docs/source-hierarchy.md:89` | Canonical source precedence and maintenance cadence | Official repo process | source governance | partially accurate | The general principle is good, but the file is itself stale on hooks and shortcuts and should explicitly include support/privacy sources for commercial/legal claims. | S6, S8, S19-S21 | L3 supports exact-version caution. | A1/A2 > A4 | File updated 2026-02-24; audit 2026-03-25 | Keep the source-precedence concept, but refresh the file and widen the authority note for commercial/legal claims. |
| `docs/volatility-watchlist.md:1`<br>`docs/volatility-watchlist.md:25`<br>`docs/volatility-watchlist.md:38`<br>`docs/volatility-watchlist.md:60` | Drift watchlist and false-positive handling | Official repo process | maintenance | partially accurate | The watchlist correctly identifies drift-heavy areas, but several entries are now themselves stale, including permissions, shortcuts, and pricing-source URLs. | S3, S4, S6, S13, S14, S19 | L1-L3 show the same drift patterns across other repos. | A1/A2 > A4/A5 | Audit 2026-03-25 | Refresh the watchlist after this audit and mark resolved false positives as re-opened where the product surface changed again. |

### Core Claude Code Mental Model and CLAUDE.md Guidance

| Repo source(s) | Claim summary | Class | Topic | Verdict | Why | Primary external citation(s) | Local corroborants / contradictions | Authority | Dates | Recommended fix |
|---|---|---|---|---|---|---|---|---|---|---|
| `chapters/01_principles.tex:15`<br>`chapters/01_principles.tex:18`<br>`chapters/01_principles.tex:37`<br>`blog/blog-summary.md:21` | Claude Code as an agent loop with finite context, tool use, and configuration layers | Official + Convergence | mental model | accurate | This matches current Claude Code docs and remains a strong framing device. | S1 | L1, L4, L5 support the same framing. | A1 > A5 | Accessed 2026-03-25 | Retain. |
| `chapters/01_principles.tex:61`<br>`chapters/01_principles.tex:97`<br>`chapters/01_principles.tex:114`<br>`chapters/01_principles.tex:125`<br>`chapters/01_principles.tex:156`<br>`blog/blog-summary.md:29`<br>`blog/blog-summary.md:202` | Engineering principles and "codebase is the curriculum" | Practitioner / Convergence | code quality | accurate | This is mostly general engineering guidance rather than Claude-product surface, and it is compatible with Anthropic's emphasis on verification and clear context. | S1, S17 | L1-L3 converge on "good artifacts teach the model." | A1/A3 > A5 | Accessed 2026-03-25 | Retain, but keep labeling as practitioner or convergence rather than pure product documentation. |
| `chapters/02_first_claude_md.tex:15`<br>`chapters/02_first_claude_md.tex:18`<br>`chapters/02_first_claude_md.tex:28`<br>`quickstart_guide.tex:323`<br>`quickstart_guide.tex:326`<br>`blog/blog-summary.md:38` | `/init`, CLAUDE.md importance, and hierarchical loading | Official | CLAUDE.md | accurate | Current docs still support `/init`, automatic CLAUDE.md loading, and the hierarchy of global/project/nested CLAUDE.md files. | S1, S5 | L1, L4, L5 support CLAUDE.md-first practice. | A1 > A5 | Accessed 2026-03-25 | Retain. |
| `chapters/02_first_claude_md.tex:59`<br>`chapters/02_first_claude_md.tex:117`<br>`chapters/02_first_claude_md.tex:131`<br>`quickstart_guide.tex:332`<br>`quickstart_guide.tex:378`<br>`blog/blog-summary.md:61` | Include what Claude cannot infer; prefer terse actionable instructions | Convergence | CLAUDE.md content | accurate | This aligns with current memory and best-practices docs. | S1, S5 | L1-L5 strongly converge. | A1 > A5 | Accessed 2026-03-25 | Retain. |
| `chapters/02_first_claude_md.tex:143`<br>`chapters/02_first_claude_md.tex:162`<br>`templates/settings.json:1`<br>`chapters/10_projects.tex:23` | Day-one deny rules and secret protection | Official + Convergence | permissions | accurate | Deny rules remain strong practice and align with current settings/permissions docs. | S4, S8 | L4, L5 support the same pattern. | A1 > A5 | Accessed 2026-03-25 | Retain. |
| `templates/minimal-claude-md.md:3`<br>`templates/production-claude-md.md:3`<br>`templates/production-claude-md.md:28` | CLAUDE.md template content: build commands, testing standards, conventions | implicit template guidance | templates | accurate | These are good starter templates. Coverage targets and style conventions are house rules, not Anthropic-official defaults, which is fine if labeled as templates. | S1, S5 | L1-L5 converge on build/test commands and verification rules. | A1/A5 | Accessed 2026-03-25 | Keep, but note in template comments that numeric coverage targets are project standards, not Claude Code product requirements. |

### Session Hygiene, Context Management, and Planning

| Repo source(s) | Claim summary | Class | Topic | Verdict | Why | Primary external citation(s) | Local corroborants / contradictions | Authority | Dates | Recommended fix |
|---|---|---|---|---|---|---|---|---|---|---|
| `chapters/03_first_session.tex:129`<br>`chapters/03_first_session.tex:148`<br>`chapters/05_context.tex:20`<br>`chapters/05_context.tex:100`<br>`quickstart_guide.tex:413`<br>`quickstart_guide.tex:419`<br>`blog/blog-summary.md:79` | `/clear` between unrelated tasks, `/compact` for continuity, and the two-failure rule | Official + Practitioner | context hygiene | accurate | The `/clear` and `/compact` guidance matches current docs. The two-failure rule is a practitioner heuristic, not an official numeric guarantee. | S1, S2, S10 | L1-L5 support the pattern; L1/L2 repeat similar heuristics. | A1 > A5 | Accessed 2026-03-25 | Retain, but keep the two-failure rule explicitly labeled as practitioner heuristic. |
| `chapters/03_first_session.tex:168`<br>`quickstart_guide.tex:141`<br>`quickstart_guide.tex:508`<br>`blog/blog-summary.md:97` | `Esc`, `Esc+Esc`, checkpoints, rewind, and recovery | Convergence | checkpointing | accurate | Current command/interactive docs support rewind, summarize-from-here, and checkpoint-based recovery. | S2, S3 | L2, L4, L5 support the workflow. | A1 > A5 | Accessed 2026-03-25 | Retain. |
| `chapters/03_first_session.tex:196`<br>`chapters/03_first_session.tex:206`<br>`quickstart_guide.tex:156`<br>`quickstart_guide.tex:511`<br>`quickstart_guide.tex:522`<br>`docs/source-hierarchy.md:64`<br>`docs/volatility-watchlist.md:43`<br>`blog/blog-summary.md:104` | Plan Mode, permission modes, `Shift+Tab`, and `Ctrl+G` shortcut behavior | Official / Convergence | modes and shortcuts | incorrect | Live docs now document six permission modes, `Shift+Tab` / `Alt+M` cycling enabled modes, and `Ctrl+G` as opening the default text editor for prompt/custom-response editing. The repo's fixed three-mode cycle and "open current plan" wording are stale. | S3, S4 | L1-L3 support planning before implementation, but not the stale shortcut details. | A1 > A5 | Accessed 2026-03-25 | Update all permission-mode tables and shortcut notes to current wording. |
| `quickstart_guide.tex:143` | "In Default mode, Claude always asks before editing" | Official | permissions | partially accurate | Default mode prompts on first use of each tool, not literally before every edit. The current wording overstates how often prompts appear. | S4 | n/a | A1 | Accessed 2026-03-25 | Replace with: "Default mode prompts on first use of each tool and when otherwise required by permission settings." |
| `quickstart_guide.tex:354`<br>`chapters/08_claude_md_architecture.tex:143`<br>`chapters/08_claude_md_architecture.tex:220` | Keep CLAUDE.md under 300 lines, split long files into rules/imports | Practitioner + Official | CLAUDE.md size | partially accurate | Official docs now say target under 200 lines per CLAUDE.md file, while Claude Code cost docs also say to aim under about 500 lines by including only essentials. The repo's `300` line rule is a useful heuristic but should not be framed as the canonical official number. | S5, S10 | L1 and L2 use even stricter 100-200-line heuristics. | A1 > A5 | Accessed 2026-03-25 | Reframe as: "Official target under 200 lines per file; in practice, split before 200-300 if adherence drops." |
| `quickstart_guide.tex:413`<br>`chapters/05_context.tex:84`<br>`chapters/05_context.tex:125`<br>`chapters/05_context.tex:149`<br>`blog/blog-summary.md:79` | `~60%` or `60-70%` context threshold for quality degradation | Practitioner | context thresholds | partially accurate | Official docs support proactive context management, but not one universal `60%` rule. This should be clearly marked as heuristic. | S1, S10, S17, S18 | L1 and L2 repeat the same heuristic, which strengthens its practitioner status but not its official status. | A1/A3 > A5 | Accessed 2026-03-25 | Keep as a heuristic, not an official threshold. |
| `chapters/05_context.tex:133`<br>`blog/blog-summary.md:93`<br>`docs/volatility-watchlist.md:55` | Status line is local, zero-token, and useful for model/branch/cost/context monitoring | Official | status line | accurate | This aligns with current status-line docs. | S11 | L2 supports "watch context continuously." | A1 > A5 | Accessed 2026-03-25 | Retain. |
| `chapters/05_context.tex:190`<br>`chapters/05_context.tex:201` | Custom compaction instructions in `CLAUDE.md` and partial summarize-from-here flows | Official | compaction | accurate | Current commands and costs docs explicitly support `/compact [instructions]` and CLAUDE.md compaction instructions. | S2, S10 | L3 supports explicit handoff templates. | A1 > A5 | Accessed 2026-03-25 | Retain and surface this earlier in the repo. |
| `chapters/05_context.tex:252`<br>`chapters/05_context.tex:292`<br>`chapters/05_context.tex:343`<br>`blog/blog-summary.md:81` | `CURRENT_WORK.md`, auto-memory, and persistence separation | Practitioner + Official | durable state | accurate but incomplete | The separation of CLAUDE.md, memory, and transient current-work state is strong. The missing piece is a more explicit statement that long-running work still needs durable artifacts because compaction alone is not enough. | S5, S18 | L1-L5 strongly converge on current-work artifacts. | A1/A3 > A5 | Accessed 2026-03-25 | Keep and strengthen with explicit long-running-agent rationale. |
| `chapters/05_context.tex:363`<br>`chapters/10_projects.tex:66` | Explore -> Plan -> Implement -> Commit, plus plan docs for large tasks | Official + Practitioner | planning | accurate | Current best-practices docs still support the four-phase workflow. The `>1 hour or 500 lines` trigger is practitioner guidance. | S1 | L3 supports handoff docs for larger efforts. | A1 > A5 | Accessed 2026-03-25 | Retain, but label the numeric trigger as heuristic. |
| `chapters/05_thinking_partner.tex:317`<br>`blog/blog-summary.md:120` | Let Claude interview the user; `AskUserQuestion` for clarifying requirements | Practitioner | elicitation | partially accurate | The general pattern is sound. The exact `AskUserQuestion` tool name is documented in Agent SDK material, but it is not a current headline Claude Code best-practices surface in the public product docs. | S16 | L3 supports interview-style handoff patterns. | A2 > A5 | Accessed 2026-03-25 | Keep the interviewing advice, but relabel it as practitioner/SDK-adjacent rather than a core Claude Code UI claim. |

### Testing, Thinking, Models, and Costs

| Repo source(s) | Claim summary | Class | Topic | Verdict | Why | Primary external citation(s) | Local corroborants / contradictions | Authority | Dates | Recommended fix |
|---|---|---|---|---|---|---|---|---|---|---|
| `quickstart_guide.tex:214`<br>`chapters/06_testing.tex:18`<br>`chapters/06_testing.tex:38`<br>`chapters/06_testing.tex:69`<br>`chapters/06_testing.tex:171`<br>`blog/blog-summary.md:112` | Verification is highest leverage; six-layer validation; quality hooks | Official + Convergence | testing | accurate | Verification-first remains a central Anthropic recommendation. The six-layer testing structure and phase-specific thresholds are practitioner guidance layered on top of that. | S1 | L1-L5 strongly converge on verification-first. | A1 > A5 | Accessed 2026-03-25 | Retain. |
| `chapters/04_prompting.tex:143`<br>`chapters/04_prompting.tex:152`<br>`chapters/04_prompting.tex:166`<br>`docs/volatility-watchlist.md:45` | Extended thinking, adaptive thinking on Opus 4.6, effort controls, `Alt+T` | Official + Practitioner | reasoning controls | accurate but stale | The adaptive-thinking and effort-control guidance is aligned with current docs. The repo should continue using exact model/version language because this area changes quickly. | S9, S15, S3 | n/a | A1/A2 | Accessed 2026-03-25 | Retain, but keep version/date language explicit. |
| `chapters/04_prompting.tex:202`<br>`chapters/04_prompting.tex:207`<br>`chapters/04_prompting.tex:218`<br>`chapters/14_enterprise.tex:80`<br>`docs/source-hierarchy.md:76`<br>`docs/volatility-watchlist.md:65`<br>`blog/blog-summary.md:194` | Prompt caching, Batch API, and combined savings claims | Official | cost optimization | accurate | The core pricing claims are current: cached reads at `0.1x`, cache writes at `1.25x` or `2x`, Batch API `50%` discount, and workload-dependent combination benefits. | S13, S14 | L1-L3 generally agree, though local notes are less precise. | A2 > A5 | Accessed 2026-03-25 | Retain; keep "up to" and "workload-dependent" language. |
| `chapters/04_prompting.tex:226`<br>`chapters/04_prompting.tex:242`<br>`chapters/14_enterprise.tex:90` | Haiku / Sonnet / Opus model-selection guidance | Official + Practitioner | model choice | accurate but stale | The model-shape guidance is sound, but it should be tied to current model names and 1M support details instead of generic or drifting wording. | S9, S10, S12 | L3 explicitly warns against vague model-version language. | A1/A2 > A5 | Accessed 2026-03-25 | Add exact wording for Opus 4.6, Sonnet 4.6, and the `sonnet[1m]` / `opus[1m]` aliases. |

### Hooks, Extensions, Subagents, and Automation

| Repo source(s) | Claim summary | Class | Topic | Verdict | Why | Primary external citation(s) | Local corroborants / contradictions | Authority | Dates | Recommended fix |
|---|---|---|---|---|---|---|---|---|---|---|
| `chapters/07_extending.tex:175`<br>`chapters/07_extending.tex:181`<br>`chapters/09_agents_parallel.tex:121` | Skills and subagents isolate context; exact `~2%` skill-description claim | Official + Practitioner | context isolation | partially accurate | The isolation point is strong. The exact `~2%` / `16,000 characters` figure is currently documented for skill-description budgeting, but it is volatile and should not be treated as a durable rule. | S22, S10 | L1-L3 support "keep extra instructions out of base context" but not the exact percentage. | A1 > A5 | Accessed 2026-03-25 | Keep the isolation guidance; soften the exact `%` claim. |
| `chapters/07_extending.tex:206`<br>`chapters/07_extending.tex:220`<br>`chapters/07_extending.tex:238`<br>`chapters/07_extending.tex:245`<br>`docs/source-hierarchy.md:24`<br>`docs/valid-hook-events.txt:1`<br>`docs/volatility-watchlist.md:7` | Hook inventory, allowlist, and "if non-negotiable, make it a hook" | Convergence | hooks | incorrect | The golden rule is good. The inventory is not: live docs now show 22 events including `StopFailure`; local allowlist has 21; source-hierarchy says 17 plus `Setup`; chapter table omits `StopFailure` and gives `PostCompact` the wrong matcher shape. | S6 | L3 supports treating volatile hook details as high-risk drift. | A1 > A4/A5 | Accessed 2026-03-25 | Update all hook inventories and the allowlist, then rerun validation. |
| `chapters/07_extending.tex:250`<br>`chapters/07_extending.tex:253`<br>`docs/source-hierarchy.md:50` | Hook handler types, HTTP support, and timeout behavior | partially Official | hooks | partially accurate | `chapters/07_extending.tex` is largely current on four handler types including `http`. `docs/source-hierarchy.md` is stale because it still lists only three hook types and omits `http`. | S6 | n/a | A1 > A4 | Accessed 2026-03-25 | Bring `docs/source-hierarchy.md` into alignment with the live hooks docs. |
| `chapters/07_extending.tex:291`<br>`chapters/07_extending.tex:317`<br>`chapters/07_extending.tex:343`<br>`chapters/07_extending.tex:357`<br>`chapters/07_extending.tex:388`<br>`chapters/07_extending.tex:421`<br>`chapters/07_extending.tex:437`<br>`blog/blog-summary.md:131` | Notification hooks, MCP wildcards, MCP audit workflow, plugins, sandboxing, CLI efficiency | Convergence | extensions | accurate | This cluster aligns well with current docs: notification hooks, MCP scoping, plugins, sandboxing, and preferring CLI tools over heavy MCP context are all supported. | S4, S6, S7, S25, S26, S27 | L1-L5 broadly converge. | A1 > A5 | Accessed 2026-03-25 | Retain. |
| `chapters/08_claude_md_architecture.tex:130`<br>`chapters/13_team.tex:23`<br>`chapters/13_team.tex:48`<br>`chapters/13_team.tex:63` | Shared vs local settings, managed-settings precedence, merged hooks | Official + Practitioner | settings | accurate | This matches current settings docs, including managed-settings precedence and the shared/local split. | S8 | L4 and L5 use the same shared/local pattern. | A1 > A5 | Accessed 2026-03-25 | Retain. |
| `chapters/09_agents_parallel.tex:89`<br>`chapters/09_agents_parallel.tex:129`<br>`chapters/09_agents_parallel.tex:162`<br>`chapters/09_agents_parallel.tex:181` | Continue subagents with `SendMessage`; worktree isolation and housekeeping | Official | subagents and worktrees | accurate | Current sub-agent and common-workflow docs support resume behavior, worktree isolation, and `.claude/worktrees/` metadata patterns. | S23, S7 | L3 supports durable-isolation patterns. | A1 > A5 | Accessed 2026-03-25 | Retain. |
| `chapters/09_agents_parallel.tex:197`<br>`chapters/09_agents_parallel.tex:227`<br>`blog/blog-summary.md:155`<br>`blog/blog-summary.md:159` | Writer/reviewer pattern and agent teams | Official + Practitioner | parallel workflows | accurate | Separate-session review remains recommended. Agent teams are still preview/experimental and the repo correctly warns about that. | S1, S24, S10 | L3 supports perspective isolation. | A1/A3 > A5 | Accessed 2026-03-25 | Retain. |
| `chapters/10_projects.tex:23`<br>`chapters/10_projects.tex:41`<br>`chapters/10_projects.tex:66`<br>`chapters/10_projects.tex:89` | Day-one project setup, commit gate hook, plan mode first, incremental adoption | Convergence | project lifecycle | accurate | Strong practitioner guidance that fits current Claude Code behavior well. | S1, S8 | L4 and L5 support the same "start with CLAUDE.md + deny rules + hooks" pattern. | A1 > A5 | Accessed 2026-03-25 | Retain. |
| `chapters/11_antipatterns.tex:19`<br>`chapters/11_antipatterns.tex:68`<br>`chapters/11_antipatterns.tex:92`<br>`chapters/11_antipatterns.tex:201`<br>`chapters/11_antipatterns.tex:286` | Anti-pattern catalog: context overload, kitchen-sink sessions, over-correcting, infinite exploration, recovery commands | Practitioner | failure modes | accurate | These are good practitioner diagnostics built on top of current official recovery primitives. | S1, S2, S3 | L1-L5 converge on the same failure modes. | A1 > A5 | Accessed 2026-03-25 | Retain. |
| `chapters/12_automation.tex:20`<br>`chapters/12_automation.tex:60`<br>`chapters/12_automation.tex:85`<br>`blog/blog-summary.md:163` | `claude -p`, `--allowedTools`, headless permissions, `--dangerously-skip-permissions` | Official | automation | accurate | The automation guidance aligns with current CLI usage. The warning around skip-permissions remains important. | S1, S4 | L3 supports tool scoping for automated flows. | A1 > A5 | Accessed 2026-03-25 | Retain. |
| `templates/hook-examples.json:1`<br>`templates/subagent-template.md:1`<br>`templates/custom-command.md:1`<br>`templates/rule-with-paths.md:1`<br>`templates/skill-template.md:1` | Template guidance for hooks, subagents, commands, rules, and skills | implicit template guidance | templates | accurate | These templates are sensible examples and generally align with current capabilities. | S6, S8, S22, S23 | L1-L5 converge on the same structure. | A1 > A5 | Accessed 2026-03-25 | Retain; add a note that examples should be revalidated on future hook-surface changes. |

### Team, Enterprise, and Mirrored Blog Claims

| Repo source(s) | Claim summary | Class | Topic | Verdict | Why | Primary external citation(s) | Local corroborants / contradictions | Authority | Dates | Recommended fix |
|---|---|---|---|---|---|---|---|---|---|---|
| `chapters/13_team.tex:15`<br>`chapters/13_team.tex:81`<br>`chapters/13_team.tex:119` | Team-seat access, onboarding, shared extensions at scale | Official + Practitioner | team rollout | accurate but stale | The general team-governance advice is strong. Seat wording should match the current support article exactly, including newer enterprise-seat nuances. | S21, S8 | L4/L5 support committed CLAUDE.md plus local settings. | A2/A1 > A5 | Updated over a week ago; accessed 2026-03-25 | Refresh seat wording to match the current support article. |
| `chapters/14_enterprise.tex:14`<br>`chapters/14_enterprise.tex:18`<br>`chapters/14_enterprise.tex:25`<br>`blog/blog-summary.md:190` | Certifications list including `FedRAMP High` | Official | enterprise compliance | incorrect | Current commercial certification docs do not list `FedRAMP High`. | S19 | n/a | A2 > A4/A5 | Updated over a week ago; accessed 2026-03-25 | Remove or rescope `FedRAMP High` claims. |
| `chapters/14_enterprise.tex:31`<br>`chapters/14_enterprise.tex:42`<br>`chapters/14_enterprise.tex:50`<br>`blog/blog-summary.md:192` | IAM features, no-training-by-default, ZDR | Official | enterprise data and access | partially accurate | IAM and ZDR framing are broadly aligned, but the cited training-policy article ID is stale and the wording "never used for model training" is too absolute because Anthropic explicitly carves out feedback/opt-in exceptions. | S20 | n/a | A2 | Updated over a week ago; accessed 2026-03-25 | Update the citation and replace "never" with "not used by default; explicit feedback or opt-in can change that." |
| `chapters/14_enterprise.tex:80`<br>`chapters/14_enterprise.tex:98`<br>`blog/blog-summary.md:194` | Enterprise cost optimization: caching, Batch API, model right-sizing, spending caps | Official + Practitioner | enterprise cost | partially accurate | The caching and batch numbers are current, but the stronger claim that caching saves more than switching from Opus to Sonnet is too broad without workload qualification. | S10, S13, S14 | L3 supports exact-version and workload-sensitive wording. | A1/A2 > A5 | Accessed 2026-03-25 | Keep the cost levers, but qualify cross-model cost assertions as workload-dependent. |
| `chapters/14_enterprise.tex:129`<br>`chapters/14_enterprise.tex:152` | Competitive positioning and government options | Practitioner | enterprise positioning | incomplete | The comparative framing is fine as opinionated guidance, but government/compliance language should be more carefully scoped so commercial certifications are not conflated with public-sector deployment options. | S19, S21 | n/a | A2 | Accessed 2026-03-25 | Split commercial compliance from government deployment commentary. |
| `blog/blog-summary.md:38`<br>`blog/blog-summary.md:79`<br>`blog/blog-summary.md:93`<br>`blog/blog-summary.md:97` | Blog mirrors handbook guidance on `/init`, context hygiene, status line, and recovery | Mixed | mirrored summary | accurate but stale | Most of the mirrored workflow advice is still sound, but the blog inherits stale dates and several stale volatile claims from the handbook. | S1, S2, S11 | L1-L5 broadly converge on the stable parts. | A1 > A5 | Audit 2026-03-25 | Refresh the blog after fixing the handbook-level drift. |
| `blog/blog-summary.md:104`<br>`blog/blog-summary.md:131`<br>`blog/blog-summary.md:155`<br>`blog/blog-summary.md:159`<br>`blog/blog-summary.md:163` | Blog mirrors stale permissions/shortcut details but mostly current extension and worktree guidance | Mixed | mirrored summary | partially accurate | The extension and worktree advice remains good; the permission-mode and `Ctrl+G` details are stale. | S3, S4, S7 | L3 supports the worktree/subagent patterns. | A1 > A5 | Accessed 2026-03-25 | Update blog shortcut and permission wording at the same time as the handbook. |

## Appendix: High-Signal Local `~/Claude/*` Evidence

### What the local sweep added

- strong convergence on `CLAUDE.md` as the first durable context layer
- strong convergence on `/clear` between tasks and `/compact` for same-task continuity
- strong convergence on keeping a current-work artifact outside the conversation itself
- repeated low-authority hard numbers (`70%`, `100 lines`, `95% -> 60%`) that should not be promoted into repo-wide "official" claims

### Local evidence notes

| Local source | Supports | Contradicts or weakens |
|---|---|---|
| `L1` | CLAUDE.md-first, context hygiene, handoff artifacts | Unsupported exact claims like `95% -> 60%` accuracy and a universal `100-line` max |
| `L2` | `/clear`, `/compact`, status/context checks, compact quick-reference patterns | Repeats `70%` and `100-200 lines` as if universal |
| `L3` | Exact model/version caution, compaction prompts, handoff templates | Does not contradict official docs; useful as secondary corroboration only |
| `L4` | CLAUDE.md usage, `/clear`, `/compact` from another active repo | No major contradiction |
| `L5` | Same as L4 from a second repo version | No major contradiction |

## Practical Remediation Queue

1. Update `docs/valid-hook-events.txt`, `docs/source-hierarchy.md`, and `chapters/07_extending.tex` together from the live hooks docs.
2. Replace every "five permission modes" and fixed `Shift+Tab` three-mode loop reference with the current six-mode wording.
3. Remove `FedRAMP High` from the commercial certifications list unless it is explicitly reintroduced with narrowly scoped, current government-offering sourcing.
4. Replace vague "1M Opus" language with exact March 25, 2026 model wording: `opus[1m]`, `sonnet[1m]`, Opus 4.6, Sonnet 4.6.
5. Reframe all hard numbers around context and CLAUDE.md length as heuristics.
6. Strengthen long-task guidance around durable artifacts, not just compaction.
7. Refresh README validation and URL-check descriptions so repo metadata matches the current tooling.

## Bottom Line

The repo already teaches many of the right habits: explicit project memory, verification, context hygiene, hooks for enforcement, and subagents/worktrees for isolation. The main problem is not conceptual quality. The main problem is drift in fast-changing product details and a few enterprise claims that now overstate what current first-party documentation says.

If the P0/P1 items above are corrected, the repo will be in strong shape again. As it stands on March 25, 2026, it should be described as directionally accurate, but not fully up to date.
