# Codex Audit: Claude Ecosystem Control Surfaces vs Current Claude Code Guidance

Date: 2026-04-01  
Auditor: Codex  
Primary scope: `/home/brandon_behring/Claude/*`  
Appendix scope: archived and embedded material inside those repos, plus user-level `~/.claude` runtime context

This report supersedes the narrower same-day skills-only audits:

- `codex_claude_skills_ecosystem_audit_2026-04-01.md`
- `docs/audits/skill_ecosystem_2026-04-01.md`

It re-checks reused claims instead of inheriting them. One concrete correction: the current `lever_of_archimedes/hooks/user_prompt_submit.sh` emits `hookSpecificOutput.additionalContext`; the earlier synthesized audit's `system_message` concern is no longer current.

## Executive Summary

Overall verdict: the ecosystem has a coherent operating model, but it is governed more like a personal workstation than a portable multi-repo platform.

The strongest pattern is centralization. `lever_of_archimedes` provides a shared hook stack, shared commands, shared conventions, and shared MCP expectations. That reduces duplication, but it also creates a large single point of failure and pushes many repos toward machine-local behavior.

The highest-priority findings are:

| Severity | Finding | Why it matters |
|---|---|---|
| Critical | The shared Bash safety gate is stale against the current hook payload schema. | The hook reads `.parameters.command`, but current Claude Code hook docs show `.tool_input.command`. A safe runtime check confirmed the hook returns allow on a destructive-looking payload in the documented schema. |
| High | Project-shared behavior is mostly implemented in local-only settings. | Claude's settings docs say project scope is for team-shared settings and local scope is for personal or machine-specific overrides. In this tree, 24 top-level repos have `.claude/settings.local.json` but no `.claude/settings.json`, and only 3 repos track `settings.local.json`. |
| High | 32 top-level repos are coupled to one hardcoded shared hook path in `lever_of_archimedes`. | This is operationally efficient but brittle: path portability, bootstrapping, and outage risk all concentrate in one personal repo. |
| High | The skills surface is split between current and legacy patterns. | Recursive tree scan found 46 flat legacy skill files under `.claude/skills/*.md` versus 15 current-format `skills/<name>/SKILL.md` entrypoints. The highest-surface project repos are mostly still on the older layout. |
| Medium | Rules are only partially scoped. | Recursive scan found 69 rules, but only 48 use `paths:` frontmatter. Claude's memory docs say rules without `paths` load unconditionally at launch. |
| Medium | Permission defaults are very permissive once planning ends. | 29 of 46 settings files set `defaultMode: "bypassPermissions"`. User-level `~/.claude/settings.json` also uses `bypassPermissions` and `skipDangerousModePermissionPrompt: true`. |

The ecosystem is not uniformly poor. There are good patterns worth reusing:

- `job_applications` and `lever_of_archimedes` already use focused repo-level agents.
- `research-kb`, `annuity-pricing`, and parts of `job_applications` and `interview_prep_series` show solid rule decomposition.
- User-level `~/.claude/skills` already follows the modern directory-based skill layout.
- `causal_inference_mastery` is the cleanest project-local example of current-format skills.

## Scope Notes

- The actual repo tree is `/home/brandon_behring/Claude/*`. Lowercase `~/claude/*` does not exist here.
- Primary scope in this report is the top-level first-party repos in that tree.
- Archived content, embedded course/vendor repos, and knowledge mirrors are covered in the appendix and called out when they distort raw counts.
- `~/.claude` is included only as runtime context because it materially affects how the repo tree behaves.

## Authority Baseline

This audit uses current official Claude Code documentation as the baseline:

- Memory and `CLAUDE.md`: <https://code.claude.com/docs/en/memory>
- Settings scopes and permission defaults: <https://code.claude.com/docs/en/settings>
- Skills, frontmatter, and command compatibility: <https://code.claude.com/docs/en/skills>
- Hooks input schema and security guidance: <https://code.claude.com/docs/en/hooks>
- Subagents: <https://code.claude.com/docs/en/sub-agents>

Key guidance from those sources that directly matters here:

- `CLAUDE.md` files are loaded in full; shorter files adhere better, and Claude recommends targeting under 200 lines per file.
- `.claude/rules/` is the preferred way to modularize instructions; rules without `paths` load unconditionally.
- Project settings are for team-shared settings; local settings are for personal or machine-specific overrides and are not shareable.
- Skills are recommended over legacy `.claude/commands/`, though commands still work.
- Current skill layout is `.claude/skills/<skill-name>/SKILL.md`; `paths`, `allowed-tools`, and `disable-model-invocation` are part of the supported frontmatter.
- Current hook examples use `tool_name` and `tool_input.command`, and return `hookSpecificOutput.permissionDecision`.
- Hook docs explicitly say command hooks run with the full permissions of the local user account and recommend using absolute paths via `"$CLAUDE_PROJECT_DIR"`.
- Subagent best practices emphasize focused responsibilities and limited tool access.

## Ecosystem Map

### Quantitative Snapshot

Primary top-level repo count:

- 34 top-level repos under `/home/brandon_behring/Claude/*`
- 30 use root `CLAUDE.md`
- 4 use `.claude/CLAUDE.md`
- 32 top-level repos have `.claude/settings.local.json`
- 9 top-level repos have `.claude/settings.json`
- 24 top-level repos rely on local settings only, with no project settings file
- 13 top-level repos have richer control surfaces beyond `CLAUDE.md` and settings
- 21 top-level repos are thin spokes with only `CLAUDE.md` and/or settings

Cross-tree recursive scan, excluding `.git`, `.venv*`, `venv`, and `node_modules`:

- 46 flat legacy skill files
- 15 directory-based `SKILL.md` entrypoints
- 21 command files
- 4 agent files
- 69 rule files
- 48 path-scoped rules
- 46 settings files
- 29 settings files with `defaultMode: "bypassPermissions"`
- 14 settings files enabling `research-kb`
- 7 settings files enabling `enableAllProjectMcpServers`

These raw recursive totals are inflated by appendix material, especially inside `course_learning` and `lever_of_archimedes`. The primary operating behavior is driven much more by a smaller set of high-surface repos.

### Cluster View

| Cluster | Repos | Primary pattern | Assessment |
|---|---|---|---|
| Shared infrastructure | `lever_of_archimedes` | Central hooks, commands, agents, shared path references | Valuable, but too coupled and too personal-machine-specific |
| High-surface workflow repos | `course_learning`, `interview_prep_series`, `job_applications`, `consulting` | Most skills, rules, and task-specific workflows live here | These repos should be the first migration targets |
| Current-format islands | `causal_inference_mastery`, `facure_augment`, active nested subprojects in `course_learning`, user-level `~/.claude/skills` | Modern `SKILL.md` layout, better frontmatter discipline | Best source of reusable patterns |
| Thin spokes | 21 repos listed in Appendix A | Mostly `CLAUDE.md` + settings only | Low local complexity, high dependency on shared hooks |

### Densest Top-Level Repos

Raw control-surface counts by top-level repo:

| Repo | Count | Notes |
|---|---:|---|
| `course_learning` | 180 | Includes active subprojects plus appendix archive and embedded material |
| `interview_prep_series` | 62 | Rule-heavy and legacy-skill-heavy |
| `lever_of_archimedes` | 42 | Shared infrastructure hub |
| `job_applications` | 33 | Legacy flat skills plus focused agents |
| `consulting` | 14 | Compact but still legacy-skill-heavy |
| `causal_inference_mastery` | 9 | Small, but modern skill layout |

## Shared Infrastructure Findings

### 1. The shared PreToolUse safety hook is currently nonfunctional for the documented input schema

File:

- `lever_of_archimedes/hooks/pretool_safety_gate.sh`

What the code does now:

- reads JSON from stdin
- extracts `.parameters.command`
- falls through to allow if that field is missing

What the current hook docs show:

- `PreToolUse` tool events provide `tool_name`
- command payload is at `.tool_input.command`
- deny decisions should be returned in `hookSpecificOutput.permissionDecision`

Safe runtime validation:

```bash
printf '%s' '{"tool_name":"Bash","tool_input":{"command":"rm -rf /tmp/test"}}' \
  | /home/brandon_behring/Claude/lever_of_archimedes/hooks/pretool_safety_gate.sh
```

Observed output:

```json
{"allow": true}
```

Assessment:

- This is a real break, not a stylistic nit.
- The hook still blocks only if fed an older or different payload shape.
- Because 32 top-level repos rely on the shared hook stack, this is the single most important issue in the ecosystem.

### 2. `lever_of_archimedes` is a hardcoded single point of failure

Observed pattern:

- 32 top-level repos reference shared hooks at absolute paths under `/home/brandon_behring/Claude/lever_of_archimedes/hooks/...`
- the shared stack is invoked from project settings rather than vendored into each repo or packaged as a plugin

Why this matters:

- path portability is poor
- bootstrapping another machine is fragile
- any break in `lever_of_archimedes` immediately affects most of the ecosystem
- the design assumes one user account and one filesystem layout

The hook docs recommend absolute paths but specifically call out `"$CLAUDE_PROJECT_DIR"` as the project-root-safe pattern. The current design uses hardcoded personal paths instead.

### 3. `SessionStart` is doing too much synchronous work

File:

- `lever_of_archimedes/hooks/session_start.sh`

What it does:

- starts a Julia daemon
- sleeps
- scans delegated-work output
- injects large static checklist text
- may run `git pull --ff-only --quiet` in `lever_of_archimedes` when ecosystem tracker files exist

Why this matters:

- current docs say `SessionStart` runs on every new or resumed session
- docs also say to keep `SessionStart` hooks fast and use `CLAUDE.md` for static context that does not require a script
- this hook mixes static reminders, observability, daemon startup, and repo mutation

Assessment:

- Centralized startup behavior is fine in principle.
- Mixing static prompt shaping and operational side effects into one always-on hook is not.

### 4. Plan/permission governance exists, but it is weak

Files:

- `lever_of_archimedes/hooks/pretool_plan_gate.sh`
- `lever_of_archimedes/.claude/settings.json`

Observed behavior:

- `pretool_plan_gate.sh` only logs `ExitPlanMode` and returns allow
- it does not inspect `permission_mode`, branch on repo, or enforce any transition policy
- 29 settings files default to `bypassPermissions`
- user-level `~/.claude/settings.json` also defaults to `bypassPermissions` and sets `skipDangerousModePermissionPrompt: true`

Assessment:

- This is not a direct product bug.
- It does mean the environment has relatively little friction once execution starts.
- In a heavily hook-driven ecosystem, that is a meaningful risk amplifier.

## Repo-Cluster Findings

### 1. Settings scope is inverted in practice

Current docs:

- project scope is for team-shared settings
- local scope is for personal overrides, testing, and machine-specific settings

Observed here:

- 24 top-level repos have `.claude/settings.local.json` but no `.claude/settings.json`
- only 3 repos track `.claude/settings.local.json`
- many local-only files carry shared hooks, shared MCP defaults, or operational permissions

Examples:

- `annuity-pricing/.claude/settings.local.json`
- `research-kb/.claude/settings.local.json`
- `post_transformers/.claude/settings.local.json`

Assessment:

- This makes the ecosystem work well for one machine and one operator.
- It makes it much harder to tell which behaviors are intentional project policy versus local convenience.

### 2. Skills are split across two eras

Current docs:

- modern skills live at `.claude/skills/<name>/SKILL.md`
- legacy `.claude/commands/*.md` still works
- skills are recommended because they support supporting files and newer frontmatter

Observed here:

- 46 flat legacy skill files under `.claude/skills/*.md`
- 15 current-format `SKILL.md` entrypoints
- the most active project repos are mostly still on the flat legacy layout

Legacy-heavy repos:

- `job_applications` with 19 flat skills
- `interview_prep_series` with 17 flat skills
- `consulting` with 8 flat skills
- the annuity elasticity repos with 1 flat skill each

Current-format islands:

- `causal_inference_mastery` with 6 directory-based skills
- `facure_augment` with 1 directory-based skill
- active nested subprojects inside `course_learning`
- user-level `~/.claude/skills`, which is entirely directory-based

Assessment:

- The skill surface is not broken.
- It is fragmented, which makes governance, templating, and future automation harder than it needs to be.

### 3. Rules are a good pattern, but only partially deployed well

Current docs:

- `.claude/rules/` is the right place to modularize instructions
- rules without `paths` load unconditionally
- `paths` should be used when the instruction is conditional

Observed here:

- 69 rules total
- 48 path-scoped
- 21 unscoped

Good examples:

- `research-kb/.claude/rules/testing.md`
- `job_applications/.claude/rules/data-integrity.md`
- `annuity-pricing/.claude/rules/*.md`
- `interview_prep_series/.claude/rules/volumes/*.md`

Weak point:

- several large shared rule files in `interview_prep_series` load broadly and add context even when the user is not touching that specific concern

Assessment:

- Rules are the strongest shared-instruction mechanism in this ecosystem.
- The next step is not invention; it is finishing the scoping work already started.

### 4. Repo-level agents are sparse, but the ones that exist are reasonably focused

Observed agent files:

- `lever_of_archimedes/.claude/agents/code-reviewer.md`
- `lever_of_archimedes/.claude/agents/test-generator.md`
- `job_applications/.claude/agents/job-app/jd-analyzer.md`
- `job_applications/.claude/agents/job-app/materials-reviewer.md`

Assessment:

- This is one of the healthier areas.
- The repo-local agents are specialized and clearly task-shaped.
- The bigger gap is uneven adoption, not obviously poor agent design.

### 5. CLAUDE.md quality is mixed

Current docs:

- target under 200 lines per file
- keep instructions specific, concise, and non-contradictory
- move conditional detail into rules

Observed oversized files:

- `causal_inference_mastery/CLAUDE.md` at 385 lines
- `interview_prep_series/.claude/CLAUDE.md` at 262 lines
- `job_applications/CLAUDE.md` at 219 lines

Assessment:

- Most thin spokes are small and fine.
- A few high-surface repos have accumulated enough instruction density that they should be decomposed into rules or imports.

## Best-Practice Gap Analysis

| Area | Current guidance | Observed pattern | Assessment |
|---|---|---|---|
| `CLAUDE.md` and memory | Keep instructions concise; target under 200 lines; split large instruction sets using imports or `.claude/rules/` | Several high-surface repos still carry oversized always-loaded `CLAUDE.md` files | Medium gap |
| Rules | Use `.claude/rules/`; add `paths` when rules are conditional | 48 rules are scoped well, but 21 still load globally | Medium gap |
| Settings scopes | Use project settings for team-shared behavior and local settings for personal overrides | Shared hooks, shared MCP, and permissions often live only in local settings | High gap |
| Skills and commands | Prefer `.claude/skills/<name>/SKILL.md`; commands still work but skills are recommended; use `paths`, `allowed-tools`, and `disable-model-invocation` deliberately | Legacy flat skills dominate the highest-surface project repos; commands remain concentrated in `lever_of_archimedes` | High gap |
| Hooks | Use current input schema, keep SessionStart fast, sanitize inputs, and use `"$CLAUDE_PROJECT_DIR"` in absolute paths | Shared safety gate is stale; SessionStart is heavy; hook paths are hardcoded to one personal repo | Critical/high gap |
| Subagents | Design focused subagents and limit tool access | Repo-local agents are focused and limited; adoption is sparse but quality is decent | Low gap |
| MCP settings | Use project scope for shared servers; be deliberate with broad discovery | `research-kb` is enabled in 14 settings files, mostly local-only; 7 settings enable all project MCP servers | Medium gap |

## Constructive Remediation Roadmap

### Phase 1: Fix safety and portability in the shared hook layer

Start in `lever_of_archimedes`.

1. Update `pretool_safety_gate.sh` to parse `.tool_input.command` and return current `hookSpecificOutput.permissionDecision` output.
2. Add a tiny test fixture set for hook payloads copied from the current docs examples.
3. Replace hardcoded user paths with a portable pattern:
   - per-repo wrapper scripts under `.claude/hooks/`, or
   - a packaged plugin/shared hook distribution, or
   - a documented symlink/bootstrap layer
4. Split `SessionStart` into:
   - static context moved to `CLAUDE.md` or `.claude/rules/`
   - a small fast hook for dynamic state only
5. Remove `git pull` from automatic session-start behavior.

### Phase 2: Normalize settings scopes

Start with the repos that actually define shared behavior for collaborators:

- `lever_of_archimedes`
- `job_applications`
- `interview_prep_series`
- `research-kb`
- `course_learning`

Concrete changes:

1. Move shareable hooks, MCP defaults, and permissions into `.claude/settings.json`.
2. Keep `.claude/settings.local.json` only for machine-specific or personal overrides.
3. Stop tracking `settings.local.json` except where there is a very explicit reason.
4. Re-evaluate whether `bypassPermissions` should be the default in shared repos.

### Phase 3: Migrate the skill surface to one current convention

Start with the most active legacy repos:

- `job_applications`
- `interview_prep_series`
- `consulting`
- `annuity-elasticity-experimental`
- `price-elasticity-of-annuities`

Concrete changes:

1. Move flat skills to `.claude/skills/<name>/SKILL.md`.
2. Add `paths` where activation should be file-scoped.
3. Add `disable-model-invocation: true` for side-effect workflows.
4. Add `allowed-tools` deliberately rather than letting every skill inherit the ambient session surface.
5. Reserve `.claude/commands/` for backward compatibility; prefer skills for new work.

### Phase 4: Reduce always-loaded instruction bulk

1. Split oversized `CLAUDE.md` files using `.claude/rules/` and imports.
2. Scope broad rule files in `interview_prep_series`.
3. Keep thin spoke repos thin; do not duplicate shared instructions there unless truly repo-specific.

### Phase 5: Add a recurring ecosystem audit

This deliverable is report-only, but the next logical step is a lightweight audit script or checklist that flags:

- stale hook schema usage
- hardcoded cross-repo hook paths
- tracked `settings.local.json`
- legacy flat skill files
- unscoped rules
- oversized `CLAUDE.md`

## What Is Working Well

- The ecosystem has a real architecture, not just ad hoc config files.
- Shared conventions in `lever_of_archimedes` are consistent enough that most thin spokes stay simple.
- Rule decomposition is already strong in `research-kb`, `annuity-pricing`, and parts of `job_applications` and `interview_prep_series`.
- Repo-level agents in `lever_of_archimedes` and `job_applications` are focused and aligned with current subagent guidance.
- User-level `~/.claude/skills` is already on the modern directory-based layout and is a better template than several project repos.

## Appendix A: Primary Top-Level Repo Inventory

### Richer Control-Surface Repos

| Repo | Main control surfaces | Tracking profile | Main note |
|---|---|---|---|
| `lever_of_archimedes` | 17 commands, 2 agents, shared hooks, settings.json + settings.local.json | Mixed | Shared infrastructure hub |
| `course_learning` | Root rules and command, plus active nested current-format skills | Tracked-heavy at top level, mixed overall | Appendix content inflates raw counts |
| `interview_prep_series` | 41 rules, 17 flat skills, hidden `CLAUDE.md`, settings.json + settings.local.json | Mixed | Best rule library, but still legacy-skill-heavy |
| `job_applications` | 6 rules, 19 flat skills, 2 agents, tracked settings.local.json | Mixed | Highest-value migration target after shared hooks |
| `consulting` | 3 rules, 8 flat skills, settings.json + settings.local.json | Mixed | Compact repo with legacy skill layout |
| `causal_inference_mastery` | 6 directory-based skills, settings.json + settings.local.json | Mostly local-only | Cleanest project-local skill layout |
| `research-kb` | 6 rules, settings.local.json | Mostly local-only | Strong rules, but shared MCP behavior is local-only |
| `double_ml_time_series` | 3 commands, settings.json + settings.local.json | Mostly local-only | Small command-oriented repo |
| `annuity-pricing` | 4 rules, settings.local.json | Mostly local-only | Good rule scoping, weak settings sharing |
| `annuity-elasticity-experimental` | 1 rule, 1 flat skill, settings.local.json | Mostly local-only | Small legacy-skill surface |
| `price-elasticity-of-annuities` | 1 rule, 1 flat skill, settings.local.json | Mostly local-only | Small legacy-skill surface |
| `facure_augment` | 1 current-format skill, settings.json + settings.local.json | Mostly local-only | Useful current-format island |
| `brandon_professional_profile` | hidden `CLAUDE.md`, 2 rules, tracked settings.local.json | Mixed | Clear project-memory intent, but local settings are tracked |

### Thin Spokes

These 21 repos have no repo-local rules, skills, commands, or agents beyond `CLAUDE.md` and/or settings:

- `AnnuityCore.jl`
- `AnnuityData.jl`
- `AnnuityProducts.jl`
- `TemporalValidation`
- `annuity-knowledge-base`
- `bayesian-cold-start`
- `claude-best-practices`
- `claude-code-field-guide`
- `insurance_ai_toolkit`
- `interview_practice_bot`
- `julia_archive_audit`
- `julia_cas_exploration`
- `llm-eval`
- `myga-elasticity-v2`
- `post_transformers`
- `precision_aq`
- `research-agent`
- `rl_and_control`
- `sourcekit`
- `temporalcv`
- `temporalcv-julia`

### Raw Inventory Snapshot

This is the direct top-level rollup used for the report.

```text
AnnuityCore.jl	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
AnnuityData.jl	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
AnnuityProducts.jl	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
TemporalValidation	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
annuity-elasticity-experimental	git=yes	CLAUDE=1/0	settings=0/1	rules=1	skills_flat=1	skills_dir=0	commands=0	agents=0	shared_hooks=1
annuity-knowledge-base	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
annuity-pricing	git=yes	CLAUDE=1/0	settings=0/1	rules=4	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
bayesian-cold-start	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
brandon_professional_profile	git=yes	CLAUDE=0/1	settings=0/1	rules=2	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
causal_inference_mastery	git=yes	CLAUDE=1/0	settings=1/1	rules=0	skills_flat=0	skills_dir=6	commands=0	agents=0	shared_hooks=1
claude-best-practices	git=yes	CLAUDE=0/1	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
claude-code-field-guide	git=yes	CLAUDE=0/1	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
consulting	git=yes	CLAUDE=1/0	settings=1/1	rules=3	skills_flat=8	skills_dir=0	commands=0	agents=0	shared_hooks=1
course_learning	git=yes	CLAUDE=1/0	settings=0/1	rules=5	skills_flat=0	skills_dir=8	commands=1	agents=0	shared_hooks=1
double_ml_time_series	git=yes	CLAUDE=1/0	settings=1/1	rules=0	skills_flat=0	skills_dir=0	commands=3	agents=0	shared_hooks=1
facure_augment	git=yes	CLAUDE=1/0	settings=1/1	rules=0	skills_flat=0	skills_dir=1	commands=0	agents=0	shared_hooks=1
insurance_ai_toolkit	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
interview_practice_bot	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
interview_prep_series	git=yes	CLAUDE=0/1	settings=1/1	rules=41	skills_flat=17	skills_dir=0	commands=0	agents=0	shared_hooks=1
job_applications	git=yes	CLAUDE=1/0	settings=0/1	rules=6	skills_flat=19	skills_dir=0	commands=0	agents=2	shared_hooks=1
julia_archive_audit	git=yes	CLAUDE=1/0	settings=1/0	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=0
julia_cas_exploration	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
lever_of_archimedes	git=yes	CLAUDE=1/0	settings=1/1	rules=0	skills_flat=0	skills_dir=0	commands=17	agents=2	shared_hooks=1
llm-eval	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
myga-elasticity-v2	git=yes	CLAUDE=1/0	settings=1/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
post_transformers	git=yes	CLAUDE=1/0	settings=1/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
precision_aq	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
price-elasticity-of-annuities	git=yes	CLAUDE=1/0	settings=0/1	rules=1	skills_flat=1	skills_dir=0	commands=0	agents=0	shared_hooks=1
research-agent	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
research-kb	git=yes	CLAUDE=1/0	settings=0/1	rules=6	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
rl_and_control	git=yes	CLAUDE=1/0	settings=0/0	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=0
sourcekit	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
temporalcv	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
temporalcv-julia	git=yes	CLAUDE=1/0	settings=0/1	rules=0	skills_flat=0	skills_dir=0	commands=0	agents=0	shared_hooks=1
```

## Appendix B: Archived and Embedded Material

These counts are intentionally not treated as equal to active first-party control surfaces.

| Category | Count | Notes |
|---|---:|---|
| `_archived` or `ARCHIVE` material | 18 | Mostly old `CLAUDE.md` and one archived settings file in `course_learning` |
| `Archive/` material | 3 | Older `lever_of_archimedes` bundles |
| Embedded knowledge mirrors | 7 | `lever_of_archimedes/knowledge/sources/repos/...` |
| Embedded course/vendor repos | 4 | Active nested course repos with their own Claude assets |
| Template hook examples | 2 | `claude-best-practices/templates/hooks/*` |
| Non-Claude git hook example | 1 | `interview_prep_series/.github/hooks/pre-commit` |

Interpretation:

- `course_learning` raw counts are the most inflated by appendix-only material.
- `lever_of_archimedes` also contains mirrored knowledge repos and archived bundles that should not drive primary policy decisions.

## Appendix C: User-Level `~/.claude` Context

This layer is not the primary audit target, but it materially shapes runtime behavior.

Observed state:

- 14 user-level directory-based skills
- 2 user-level commands
- `~/.claude/settings.json` sets `defaultMode: "bypassPermissions"`
- `~/.claude/settings.json` also sets `skipDangerousModePermissionPrompt: true`
- user-level `~/.claude/CLAUDE.md` imports the broader `lever_of_archimedes` operating model

Assessment:

- User-level skills are more current-format than many project repos.
- User-level permission posture is more permissive than the ecosystem's shared-hook complexity justifies.

## Appendix D: Prior Audit Status

Files consulted as prior work:

- `codex_claude_skills_ecosystem_audit_2026-04-01.md`
- `docs/audits/skill_ecosystem_2026-04-01.md`
- `gemini_skill_audit_report.md`

What held up after revalidation:

- the general concern about ecosystem-level execution bias
- the importance of `lever_of_archimedes` as the shared control plane
- the portability and governance risk from centralization and permissive defaults

What did not fully hold up:

- the synthesized skill audit's claim that `user_prompt_submit.sh` still uses `system_message`
- some narrower skills-only framing that over-attributed behavior to skill text instead of the broader settings and hook stack

This report should be treated as the current authority among the local audit documents because it re-validated the filesystem state and current docs instead of inheriting same-day findings wholesale.
