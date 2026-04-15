# Codex Audit: Claude Skills Ecosystem, Plan Mode Drift, and Control Surface Risk

Date: 2026-04-01
Auditor: Codex
Primary scope: `~/Claude/*`
Extended machine scope: `~/.claude`, transcript history in `~/.claude/projects`, and other `.claude` directories discovered on the machine

## Executive Summary

Overall verdict: this is not one bad skill. It is an ecosystem design problem.

Claude Code's current documented behavior is still clear: Plan Mode is read-only and does not let Claude modify files or execute commands on its own. The issue in this environment is that the surrounding ecosystem strongly biases sessions toward execution, sometimes performs work automatically outside the normal planning flow, and provides very weak separation between read-only skills and action skills. The result is a user experience where "planning" exists in principle, but the surrounding defaults keep pushing toward "proceed now."

The main conclusion is:

1. I do **not** see evidence that repo skills themselves literally bypass official Plan Mode semantics. Current docs still say Plan Mode can analyze but not modify files or execute commands. [S3][S6]
2. I **do** see several other mechanisms that make it feel like Claude is "starting work while planning":
   - `SessionStart` hooks execute real shell work immediately, including daemon startup and a `git pull` in `lever_of_archimedes`. [L5][S4]
   - global planning-to-execution skills explicitly tell Claude to stop planning and begin execution, and that behavior is actually used in transcripts. [L3][L17][L18]
   - many repo-local skills and commands are action-oriented but lack current best-practice frontmatter such as `disable-model-invocation`, `allowed-tools`, and `paths`. [L8][L9][L10][S1][S6]
   - `bypassPermissions` is the dominant default once sessions leave Plan Mode. [L1][S3]
3. The ecosystem has more telemetry than expected, but it is not being used as a governance system. There is already `~/.claude/projects` transcript history at roughly `2.7G`, plus session indexes, morning reports, and hook progress events. [L17][L18]

My recommendation is a balanced redesign:

- keep auto-invocable skills only for read-only/reference workflows
- make side-effectful skills and commands manual-only
- add explicit Plan Mode branches to any mixed workflow that remains callable during planning
- slim the shared hook layer and add an explicit gate around `ExitPlanMode`
- replace "I think this skill is causing work" with transcript-derived telemetry and a frontmatter linter

## Bottom Line

What is actually going on is more specific than "skills are broken":

- official Plan Mode is probably behaving correctly
- your custom hooks are already doing work automatically
- your global personal skill pack contains explicit "stop planning, start executing" affordances
- your repo-local skill/command ecosystem does not consistently separate audit-only from apply/mutate workflows
- once Plan Mode is exited, your permission defaults make execution very easy

That combination is enough to create the behavior you are noticing.

## Scope and Method

I audited four layers together because current Claude Code behavior is controlled by all of them:

1. Repo-local control files in `~/Claude/*`
   - `.claude/skills/`
   - `.claude/commands/`
   - `.claude/agents/`
   - `.claude/settings*.json`
   - local `CLAUDE.md`
2. Global user-level Claude Code config in `~/.claude`
3. Runtime evidence
   - `~/.claude/projects/**/*.jsonl`
   - `sessions-index.json`
   - `lever_of_archimedes/logs/morning_reports/*.md`
4. Current official Claude Code docs as the authority baseline

I also scanned for other `.claude` directories across the machine. There are additional repos in `Downloads/`, `anki_workspace/`, and one vendor package under `~/.nvm`, but the active behavior pattern is overwhelmingly driven by `~/Claude/*` plus `~/.claude`, so those extra directories were noted but not treated as the primary control surface.

## Best-Practice Baseline

Current official guidance is fairly direct:

- "Explore first, then plan, then code." Anthropic explicitly recommends separating exploration and planning from implementation. [S6]
- Plan Mode is read-only: Claude can analyze but not modify files or execute commands. [S3]
- Side-effectful skills should use `disable-model-invocation: true`. Anthropic gives `/commit`, `/deploy`, and similar workflows as the canonical examples. [S1][S6]
- `allowed-tools` should be used to narrow what Claude can do while a skill is active. [S1]
- `paths` should be used when a skill should only auto-load for certain files or subtrees. [S1]
- `.claude/commands/*.md` and `.claude/skills/<name>/SKILL.md` now work the same way and support the same frontmatter; in practice they should be audited together. [S1]
- settings merge across scopes, so global `~/.claude` config materially shapes behavior in every repo. [S5]
- `PreToolUse` hooks can match `ExitPlanMode`, and hook input exposes `permission_mode`. [S4]
- command hooks run with the full permissions of the local user. [S4]

That baseline matters because your ecosystem diverges from it in several important ways.

## Ecosystem Inventory

### Repo-local inventory in `~/Claude`

- `61` repo-local skills
- `21` repo-local commands
- `4` repo-local agents
- `46` repo-local settings files

Highest-surface repos:

- `job_applications`: `19` skills, `1` settings file
- `lever_of_archimedes`: `16` commands, `2` agents, `2` settings files
- `consulting`: `8` skills, `2` settings files
- `causal_inference_mastery`: `6` skills, `2` settings files
- `double_ml_time_series`: `3` commands, `2` settings files

### Global user-level layer in `~/.claude`

- `14` personal global skills
- `3` personal global commands
- `25` marketplace/plugin skills on disk
- global `defaultMode` is `bypassPermissions` [L1]
- global `SessionStart` and `UserPromptSubmit` hooks point into `lever_of_archimedes` [L2]

### Settings and hook prevalence inside `~/Claude`

Across the `46` repo settings files:

- `29` set `defaultMode: "bypassPermissions"`
- `33` contain `UserPromptSubmit`
- `34` contain `SessionStart`
- `34` contain `PreToolUse`

### Frontmatter guard usage in repo-local skills and commands

Across repo-local skills and commands in `~/Claude`:

- only `1` uses `disable-model-invocation`
- only `4` use `allowed-tools`
- I found no repo-local skill or command frontmatter using `paths:`
- `8` consulting skills use invalid `user_invocable` instead of documented `user-invocable`

That is a strong signal that governance is mostly social and textual, not enforced by Claude Code's actual control primitives. [S1]

## Observed Runtime Evidence

There is already usable telemetry on disk.

### Existing telemetry sources

- `~/.claude/projects` contains transcript JSONL and session indexes; total size is about `2.7G`. [L17]
- transcript JSONL includes user slash-command messages, tool uses, hook progress, and tool results such as `ExitPlanMode`. [L18]
- morning reports in `lever_of_archimedes/logs/morning_reports/` summarize recurring topics and command usage. [L14][L15][L16]

### What I could verify from transcripts and logs

Raw transcript scan findings from `~/.claude/projects`:

- `/iterate`: `595` raw command occurrences
- `/exploring-options`: `156`
- `/model`: `91`
- `/compact`: `62`
- `/letsgo`: `6`
- `/proceeding-now`: `4`
- `/generate-resume`: `1`
- `ExitPlanMode` tool results: `388`
- `Skill` tool uses: `60`

Caveat: those are raw transcript occurrences, not deduplicated by session or sidechain.

Observed examples:

- morning reports show `/letsgo` in active use on `2026-01-24` and `2026-01-26`. [L14][L15]
- morning reports show `/gmail-status reconcile` as a next-step command on `2026-01-31`. [L16]
- sampled transcript entries show `Skill` tool use with `caller.type: "direct"` for skills such as `iterate`, `commit`, and `commit-commands:commit`, which means the transcript format is rich enough to distinguish explicit skill invocations. [L18]
- transcript entries also capture `ExitPlanMode` tool results directly. [L18]

One important nuance: I found historical transcript evidence for `/iterate` and `/letsgo`, but I did not find a current on-disk source file for `/iterate` in the active filesystem scan. That implies part of this behavior lives in historical skill/command state, not only in today's checked-in files. That is itself a governance problem.

## What I Think Is Happening

This is my best evidence-based explanation of the specific symptom you described.

### 1. Hooks are doing work before the model even gets to the "plan vs execute" question

The shared `SessionStart` hook in `lever_of_archimedes`:

- starts a background daemon
- sleeps
- performs `git -C "$PROJECT_DIR" pull --ff-only --quiet`
- injects a mandatory checklist and ecosystem signals into context [L5]

That is real work. It is not "Claude decided to write code in Plan Mode"; it is "the environment runs shell automation on session start." Because hooks run with the user's full permissions, this matters. [S4]

### 2. The ecosystem contains explicit "stop planning now" affordances

The global personal skill `/proceeding-now` literally says:

- "Stop planning and begin execution"
- "Begins implementation immediately" [L3]

There is also observed historical use of `/letsgo`, plus frequent `ExitPlanMode` events in transcripts. [L14][L15][L18]

So the design pattern is not just "plan carefully." It is "plan, then have a fast off-ramp into action." That off-ramp is being used.

### 3. Repo-local action skills are rarely constrained with Claude-native controls

Examples:

- `job_applications/.claude/skills/generate-resume.md` directly runs a generator and offers PDF compilation. [L8]
- `consulting/.claude/skills/propose.md` ends with "Save draft to `data/proposals/`". [L9]
- `lever_of_archimedes/.claude/commands/new-course-guide.md` creates directories, symlinks, files, verifies builds, initializes git, and commits. [L10]

These are legitimate workflows, but under current Anthropic guidance they should generally be manual-only and tightly scoped with frontmatter. [S1][S6]

### 4. The shared prompt-injection layer is broad and operationally loaded

The `UserPromptSubmit` hook:

- matches a very broad technical-keyword list
- runs proactive-context and domain-router scripts
- injects knowledge/context on technical prompts [L6]

The `SessionStart` hook injects mandatory work-shaping instructions, delegated-work notices, and ecosystem signals. [L5]

This does not itself prove Plan Mode bypass, but it does create a strong execution-oriented instruction environment around almost every technical session.

### 5. The current safety gate is not aimed at the failure mode you care about

The `PreToolUse` safety hook mostly blocks catastrophic Bash patterns such as `rm -rf /`, privilege escalation, and obvious exfiltration. [L7]

That is useful, but it does **not**:

- gate `ExitPlanMode`
- distinguish plan-mode sessions from execution sessions
- block ordinary `Write`, `Edit`, `MultiEdit`, or normal Bash actions that are safe in general but wrong during planning

So it does not defend against "safe-looking but premature execution."

## Prioritized Findings

### P0. The environment is missing a real planning firewall

Why this matters:

- official docs say Plan Mode is read-only [S3]
- your actual workflow layers encourage leaving planning quickly [L3][L14][L15][L18]
- there is no explicit hook or permission policy that treats `ExitPlanMode` as a governed transition [S4][L7]

Consequence:

- Plan Mode is being used, but it is not treated as a controlled phase transition
- the difference between "thinking" and "doing" depends too much on prompt wording and user vigilance

### P0. Action skills and commands are under-governed relative to current Claude Code best practice

Why this matters:

- custom commands and skills are now the same class of component for governance purposes [S1]
- Anthropic explicitly recommends `disable-model-invocation: true` for workflows with side effects [S1][S6]
- your repo-local ecosystem barely uses those controls

Consequence:

- action workflows rely on prose discipline instead of executable policy
- the most dangerous surface is not only `.claude/skills/`; it is also `.claude/commands/`

### P0. `SessionStart` already performs automatic work with full user permissions

Why this matters:

- the symptom the user experiences is partly real
- the session does start doing work automatically, just not because the model broke Plan Mode [L5][S4]

Consequence:

- even a nominally "planning" session begins in an already-mutated environment
- cross-repo freshness and background services are being managed implicitly, not explicitly

### P1. `bypassPermissions` is too widespread for a planning-heavy workflow

Why this matters:

- global user config sets `defaultMode: "bypassPermissions"` [L1]
- `29` repo settings files do the same
- Anthropic only recommends that mode in isolated environments where damage is contained. [S3]

Consequence:

- after leaving Plan Mode, the system has very little friction before doing real work
- accidental or premature exits are more costly

### P1. Invalid or stale schema reduces trust in your controls

Examples:

- consulting skills use `user_invocable`, but current docs specify `user-invocable` [L9][S1]
- `user_prompt_submit.sh` returns `system_message`, while current docs document `systemMessage` as the common field and `additionalContext` for adding conversation context in `UserPromptSubmit` hooks [L6][S4]

Consequence:

- some controls may not be doing what you think they are doing
- the ecosystem has drifted far enough that textual intent and actual runtime behavior may differ

### P1. Your control philosophy is internally inconsistent

Evidence:

- `planning-large-tasks` says large work needs a plan first [L4]
- `SessionStart` injects a mandatory planning checklist [L5]
- `proceeding-now` says stop planning and begin implementation immediately [L3]
- `rapid-prototyping` says skip tests and validation for speed [L19]

Consequence:

- the ecosystem is simultaneously trying to be highly governed and highly improvisational
- that tension is not resolved in code, only in narrative

### P2. Good patterns already exist, but they are isolated instead of standardized

Positive examples:

- `audit-resume-matches` has an explicit audit-only guard: "No edits to CSV, claims.yml, or role masters." [L11]
- `scaffold-role` begins with "Phase 1: Analysis (Read-Only)." [L12]
- `qa/fix-presentation` offers `--dry-run` and `--audit-only`. [L13]

Consequence:

- you already know how to design safer workflows
- the main problem is inconsistency, not lack of capability

## Recommendations

### Option A: Strict Planning Firewall

What to change:

- set high-risk repos to default into `plan` rather than `bypassPermissions`
- add a `PreToolUse` hook matching `ExitPlanMode|Write|Edit|MultiEdit|Bash` that checks `permission_mode` and blocks or escalates when the session is still in planning [S4]
- make all side-effectful skills and commands manual-only with `disable-model-invocation: true`
- require `allowed-tools` on every skill
- split mixed skills into explicit read-only and apply variants

Pros:

- strongest guarantee against accidental execution
- easiest mental model for the user
- aligns best with official guidance

Cons:

- highest friction
- more prompts and more mode switching
- some current "fast iteration" workflows will feel slower

Best for:

- repos where planning accuracy matters more than speed
- workflows with expensive or messy side effects

### Option B: Balanced Two-Tier Model

What to change:

- keep auto-invocable skills only for read-only/reference content
- make all mutating workflows manual-only
- add `allowed-tools: Read, Grep, Glob` to audit/reference skills
- add explicit Plan Mode branches inside mixed workflows:
  - "If `permission_mode == plan`, inspect only and produce an execution checklist"
  - "Do not write files, run mutating commands, or exit plan mode unless explicitly instructed"
- keep `bypassPermissions` only in a small number of repos where that tradeoff is deliberate
- reduce `SessionStart` and `UserPromptSubmit` injections to context that is genuinely safe in planning sessions

Pros:

- best speed/safety tradeoff
- preserves useful automation
- lowers surprise substantially without a full policy rewrite

Cons:

- requires maintaining a skill taxonomy
- still leaves some room for drift if frontmatter and hook linting are weak

Best for:

- your overall environment
- most repos in `~/Claude/*`

### Option C: Telemetry First, Policy Second

What to change:

- keep the current behavior mostly intact for now
- build a transcript parser over `~/.claude/projects/**/*.jsonl`
- add a lightweight JSONL logger hook for:
  - command name
  - skill name
  - `permission_mode`
  - `ExitPlanMode`
  - first subsequent mutating tool
  - sidechain vs main session
- add a frontmatter linter that flags:
  - side-effectful skills without `disable-model-invocation`
  - missing `allowed-tools`
  - invalid keys like `user_invocable`
  - mixed workflows lacking a plan-mode branch

Pros:

- lowest disruption
- gives you real evidence before restructuring everything
- easy to run historically because the transcripts already exist

Cons:

- does not fix the current behavior immediately
- depends on follow-through
- governance remains mostly observational until policy changes land

Best for:

- learning before reorganizing the whole system
- creating a baseline before a bigger cleanup

## My Recommendation

Take Option B now, and borrow the telemetry work from Option C immediately.

That means:

1. Reclassify every repo-local skill and command into one of three buckets:
   - `reference`
   - `mixed`
   - `action`
2. For `reference`:
   - add `allowed-tools: Read, Grep, Glob`
   - keep auto-invocation if the description is specific
3. For `mixed`:
   - add explicit plan-mode/read-only instructions
   - strongly consider splitting into `*-audit` and `*-apply`
4. For `action`:
   - add `disable-model-invocation: true`
   - add narrow `allowed-tools`
   - prefer `context: fork` when isolation is useful
5. Add a `PreToolUse` policy around `ExitPlanMode`
6. Move away from global `bypassPermissions` as the default
7. Build transcript-based telemetry before you trust intuition again

## Concrete High-Value Fixes

These are the specific changes I would make first.

### 1. Fix the global layer before repo-local cleanup

- change `~/.claude/settings.json` away from global `bypassPermissions` [L1]
- keep repo-specific overrides only where justified
- update `~/.claude/settings.local.json` hooks only after deciding what the safe default should be [L2]

### 2. Treat `.claude/commands/` as first-class risk, not as "just commands"

Under current docs they are functionally part of the same governance problem as skills. [S1]

Priority command candidates for manual-only treatment:

- `lever_of_archimedes/.claude/commands/new-course-guide.md` [L10]
- commit-oriented commands
- any scaffold, sync, submit, or publish workflow

### 3. Standardize the design pattern you already know works

Use these local patterns as templates:

- read-only first phase [L12]
- `--dry-run` / `--audit-only` [L13]
- explicit "no edits" guard [L11]

### 4. Add an explicit `ExitPlanMode` audit trail

Use existing transcript capability and/or a `PreToolUse` hook to log:

- session id
- repo
- timestamp
- prior `permission_mode`
- tool that immediately followed `ExitPlanMode`
- whether a write or Bash command occurred in the next turn

This directly answers the user's real question: "what actually happens right after planning ends?"

### 5. Fix stale schema now

- replace `user_invocable` with `user-invocable` [L9][S1]
- update any hook output using `system_message` to current documented fields such as `systemMessage` or `additionalContext`, depending on intended behavior [L6][S4]

## Telemetry Plan

You asked what to do if telemetry was missing. It is not fully missing; it is just not productized.

### What already exists

- transcript history in `~/.claude/projects`
- session indexes with metadata
- hook progress events
- morning reports
- file-history snapshots

### What is still missing

- clean per-skill dashboarding
- auto-vs-manual invocation breakdown
- plan-mode exit to first-mutation trace
- repo-by-repo governance scorecard

### Recommended telemetry stack

Short term:

- parse transcript JSONL historically
- build a daily CSV or SQLite table with:
  - `repo`
  - `session_id`
  - `timestamp`
  - `command_name`
  - `skill_name`
  - `caller_type`
  - `permission_mode`
  - `tool_name`
  - `is_sidechain`

Medium term:

- add a lightweight JSONL logger hook in `lever_of_archimedes`
- log `PreToolUse`, `SessionStart`, `UserPromptSubmit`, and `PermissionRequest`
- store logs outside repo working trees to avoid git noise

Long term:

- add a linter over the entire `~/Claude/*` skill/command surface
- fail CI or produce a morning warning for:
  - invalid frontmatter keys
  - action workflows without `disable-model-invocation`
  - missing `allowed-tools`
  - no read-only branch for mixed workflows

## Final Assessment

Your diagnosis was directionally right but technically incomplete.

The problem is not "skills are causing Claude Code to ignore Plan Mode." The problem is:

- hooks already do automatic work
- action workflows are weakly governed
- execution-oriented global skills exist and are used
- permissions are too permissive after plan exit
- telemetry exists but is not being used to govern the system

This is fixable. The encouraging part is that the repo already contains examples of the right design pattern. The next step is not inventing new theory. It is applying current Claude Code control primitives consistently across the whole ecosystem.

## Source Registry

### Official sources

- [S1] Claude Code skills: https://code.claude.com/docs/en/skills
- [S2] Claude Code commands: https://code.claude.com/docs/en/commands
- [S3] Claude Code permissions: https://code.claude.com/docs/en/permissions
- [S4] Claude Code hooks: https://code.claude.com/docs/en/hooks
- [S5] Claude Code settings: https://code.claude.com/docs/en/settings
- [S6] Claude Code best practices: https://code.claude.com/docs/en/best-practices

### Local evidence

- [L1] `/home/brandon_behring/.claude/settings.json`
- [L2] `/home/brandon_behring/.claude/settings.local.json`
- [L3] `/home/brandon_behring/.claude/skills/proceeding-now/SKILL.md`
- [L4] `/home/brandon_behring/.claude/skills/planning-large-tasks/SKILL.md`
- [L5] `/home/brandon_behring/Claude/lever_of_archimedes/hooks/session_start.sh`
- [L6] `/home/brandon_behring/Claude/lever_of_archimedes/hooks/user_prompt_submit.sh`
- [L7] `/home/brandon_behring/Claude/lever_of_archimedes/hooks/pretool_safety_gate.sh`
- [L8] `/home/brandon_behring/Claude/job_applications/.claude/skills/generate-resume.md`
- [L9] `/home/brandon_behring/Claude/consulting/.claude/skills/propose.md`
- [L10] `/home/brandon_behring/Claude/lever_of_archimedes/.claude/commands/new-course-guide.md`
- [L11] `/home/brandon_behring/Claude/job_applications/.claude/skills/audit-resume-matches.md`
- [L12] `/home/brandon_behring/Claude/job_applications/.claude/skills/scaffold-role.md`
- [L13] `/home/brandon_behring/Claude/interview_prep_series/.claude/skills/qa/fix-presentation.md`
- [L14] `/home/brandon_behring/Claude/lever_of_archimedes/logs/morning_reports/2026-01-24.md`
- [L15] `/home/brandon_behring/Claude/lever_of_archimedes/logs/morning_reports/2026-01-26.md`
- [L16] `/home/brandon_behring/Claude/lever_of_archimedes/logs/morning_reports/2026-01-31.md`
- [L17] `~/.claude/projects` session indexes and transcript inventory
- [L18] sampled transcript JSONL under `~/.claude/projects/**/*.jsonl`
- [L19] `/home/brandon_behring/.claude/skills/rapid-prototyping/SKILL.md`
