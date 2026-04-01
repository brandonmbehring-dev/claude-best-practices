# Skill Ecosystem Audit Report

**Date**: 2026-04-01
**Scope**: 68 skill files across `~/Claude/*`, 14 personal skills, 16 lever_of_archimedes commands
**Cross-referenced**: Codex audit, Gemini audit, official Claude Code documentation (April 2026)

## Context

Skills across `~/Claude/*` were causing Claude Code to "just start going" during plan mode — executing write operations without pausing for plan approval or compaction. This audit synthesizes findings from direct filesystem analysis, the Codex audit (codex_claude_skills_ecosystem_audit_2026-04-01.md), the Gemini audit (gemini_skill_audit_report.md), and current official Claude Code documentation.

---

## 1. Executive Summary

| Metric | Value | Concern |
|--------|-------|---------|
| Total skill files | 68 | High startup metadata cost (~12K tokens) |
| Personal skills | 14 | Zero used `allowed-tools` (now fixed) |
| Project skills | 54 (across 7 repos) | Only 3/54 use `allowed-tools` (all in RLHF project) |
| Skills >100 lines | 15 | 1 exceeds 500-line limit (gmail-status: 522) |
| Skills with write instructions | ~58 (85%) | None were plan-mode-aware |
| Skills using `disable-model-invocation` | 1 | Only `parallel` (now 5 total) |
| Hooks doing real work at session start | 2 | SessionStart runs git pull + daemon |
| Settings files with `bypassPermissions` | 29/46 | Near-zero friction after plan exit |
| `PreToolUse` hook gating `ExitPlanMode` | 0 | Plan exit is ungoverned |

**Diagnosis**: The problem is not one mechanism — it's a layered ecosystem that pushes toward execution from multiple directions simultaneously:

1. **Skill descriptions with imperative language** load into context during plan mode and compete with plan mode restrictions
2. **SessionStart hooks** inject MANDATORY execution-oriented checklists before the model even reaches the planning question
3. **`bypassPermissions`** means after plan mode exits, there is zero friction
4. **No `PreToolUse` hook gates `ExitPlanMode`** — the transition from planning to execution is ungoverned
5. **`user_prompt_submit.sh` uses `system_message`** — which may be an outdated field name (current docs specify `additionalContext`)

Skill descriptions that lack `disable-model-invocation: true` ARE loaded into Claude's context during plan mode (confirmed by [official docs](https://code.claude.com/docs/en/skills)), so their imperative language is active instruction competing with plan mode's read-only restriction.

---

## 2. Root Cause: The Plan Mode Conflict

### 2.1 Skill descriptions are instructions, not metadata

When Claude Code loads, every skill's `description:` field is injected into the system prompt. These descriptions contained imperative language like:

- `proceeding-now`: "Stop planning and **begin execution** with current decisions"
- `parallel`: "Delegate work to multiple **simultaneous** subagents"
- `planning-large-tasks`: "**MANDATORY** for tasks requiring >1 hour"

When plan mode says "MUST NOT execute" but skill descriptions say "begin execution immediately", Claude receives contradictory directives at the same authority level.

### 2.2 The `/proceeding-now` escape hatch

This skill's entire purpose is to exit planning and start writing. Both `/exploring-options` and `/reflecting-on-plan` reference it as their exit path, creating a planning → execution pipeline.

### 2.3 MANDATORY language competes with plan mode

| Skill | Language |
|-------|----------|
| `planning-large-tasks` | "**MANDATORY** for tasks requiring >1 hour" |
| `parallel` | "**FIRST: Create durable task records (MANDATORY)**" |
| `reviewing-milestone` | "**Commit all changes** on dev branch" |

### 2.4 Hooks inject execution context before plan mode begins

**SessionStart hook** (`lever_of_archimedes/hooks/session_start.sh`):
- Starts a Julia RAG daemon in the background
- Runs `git pull --ff-only --quiet` on every session
- Injects "SESSION START CHECKLIST (MANDATORY)" with execution imperatives ("Commit plan BEFORE writing code")

This creates a paradox: the hook injects MANDATORY planning language that itself contains execution imperatives.

**UserPromptSubmit hook** (`lever_of_archimedes/hooks/user_prompt_submit.sh`):
- Returns `system_message` field — current docs specify `additionalContext` under `hookSpecificOutput`
- Runs on every technical prompt (~100 keyword matches)
- Injects knowledge context from 5 domains per prompt

### 2.5 `bypassPermissions` removes friction after plan exit

Global `~/.claude/settings.json`: `"defaultMode": "bypassPermissions"`. 29/46 repo settings files repeat this. After `ExitPlanMode`, Claude can immediately use any tool without permission prompts.

### 2.6 Key insight: `disable-model-invocation: true` removes description from context

From [official documentation](https://code.claude.com/docs/en/skills):

| Frontmatter | Description in context | Full skill loads when |
|-------------|----------------------|----------------------|
| (default) | **Always** | Invoked by user or Claude |
| `disable-model-invocation: true` | **Not in context** | Only when user invokes |

This is the single highest-leverage fix: setting this flag on execution-oriented skills completely removes their conflicting descriptions from plan-mode context.

### 2.7 Five reinforcing mechanisms

**A — Write-imperative skills with unrestricted tools**: 4 skills with execution instructions and no `allowed-tools`.

**B — No plan-mode guard in any skill**: Zero skills across all 68 files contained plan-mode awareness.

**C — The `allowed-tools` gap**: Only 3/68 skills (all in RLHF project) used `allowed-tools`. Every other skill had unrestricted tool access.

**D — Hooks inject execution context**: SessionStart runs real work; UserPromptSubmit injects context on every prompt.

**E — Ungoverned plan exit**: No `PreToolUse` hook gates `ExitPlanMode`.

---

## 3. Ecosystem Inventory by Risk Tier

### Tier Definitions

| Tier | Label | Plan-mode safe? |
|------|-------|--------------------|
| **R0** | Read-only (search, analyze, report) | Yes |
| **R1** | Document-write (plans, reports, CSV) | Needs guard |
| **R2** | Code-write (source code, tests) | No |
| **R3** | Destructive (git commit, tag, push, delete) | Absolutely not |

### Personal Skills (14) — Final State After Remediation

| Skill | Tier | `allowed-tools` | `disable-model-invocation` |
|-------|------|-----------------|---------------------------|
| exploring-options | R0 | `Read, Grep, Glob` | no |
| reflecting-on-plan | R0 | `Read, Grep, Glob` | no |
| researching-topics | R0 | `Read, Grep, WebSearch, WebFetch` | no |
| check-delegated | R0 | `TaskList, TaskGet, TaskOutput, Read, Bash(git log:*, git diff:*, git show:*)` | no |
| checking-guide-health | R1 | `Read, Bash(python3:*), Grep` | no |
| verifying-guide-readiness | R1 | `Read, Bash(python3:*), Grep` | no |
| validating-before-commit | R1 | `Read, Bash(python3:*, make:*, git diff:*), Grep` | no |
| planning-large-tasks | R1 | `Write, Read, Bash(git:*), Grep, Glob` | no (description rewritten) |
| decomposing-functions | R2 | `Read, Write, Edit, Grep, Glob` | no |
| proceeding-now | R2 | `TaskCreate, Read` | **yes** |
| rapid-prototyping | R2 | `Read, Write, Edit, Bash, Grep, Glob` | **yes** |
| refactoring-code | R2 | `Read, Write, Edit, Bash, Grep, Glob` | **yes** |
| reviewing-milestone | R3 | `Write, Read, Bash(git:*, make:*, python3:*)` | **yes** |
| parallel | R3 | `Agent, TaskCreate, TaskUpdate, TaskList, Read, Grep, Glob` | already yes |

### Project Skills

**job_applications (19 skills)**: 4 R0, 13 R1-R2, 2 R3. `gmail-status.md` at 522 lines exceeds 500-line limit.

**interview_prep_series (17 skills)**: 6 R0 (QA audits), 11 R1-R2 (content enrichment). Zero frontmatter.

**consulting (8 skills)**: All R1 (CSV wrappers). Use non-standard `user_invocable` instead of `user-invocable`.

**causal_inference_mastery (6 skills)**: 2 R0, 4 R1-R2.

**lever_of_archimedes (16 commands)**: Old `.claude/commands/` format, not migrated to skills.

---

## 4. Design Issues Beyond Plan Mode

### 4.1 No frontmatter consistency

| Project | name | description | version | allowed-tools | effort |
|---------|------|------------|---------|---------------|--------|
| Personal (14) | 14/14 | 14/14 | 14/14 | **14/14** (fixed) | 14/14 |
| job_applications (19) | ~3/19 | ~3/19 | 0/19 | 0/19 | 0/19 |
| interview_prep_series (17) | 0/17 | 0/17 | 0/17 | 0/17 | 0/17 |
| consulting (8) | 8/8 | 8/8 | 0/8 | 0/8 | 0/8 |
| causal_inference_mastery (6) | 6/6 | 6/6 | 0/6 | 0/6 | 0/6 |
| RLHF (3) | 3/3 | 3/3 | 0/3 | **3/3** | 0/3 |

### 4.2 Skills that should be hooks

| Skill | Why Hook Is Better | Proposed Type |
|-------|--------------------|---------------|
| `validating-before-commit` | Should auto-run before every commit | PreCommit |
| `qa:pre-commit` (interview_prep) | Same | PreCommit |
| `check-freshness` (job_apps) | Periodic staleness check | Scheduled cron |

### 4.3 Duplicates

- `cover-letter.md` + `generate-cover-letter.md` in job_applications
- `checking-guide-health` + `verifying-guide-readiness` (could merge with `--mode` argument)
- `validate-economics` in two annuity projects

### 4.4 Oversized: gmail-status.md (522 lines)

Needs restructuring into dispatcher + reference files.

### 4.5 Consulting skills are over-engineered

8 skills for CSV manipulation could consolidate to 2-3.

---

## 5. Remaining Remediation (Phases 2-4)

### Phase 2: Hook-level governance

- Add PreToolUse hook gating ExitPlanMode (official docs confirm this is supported)
- Fix `system_message` → `additionalContext` in UserPromptSubmit hook
- Add plan-mode awareness to SessionStart checklist injection

### Phase 3: Ecosystem-wide frontmatter

- Add frontmatter to job_applications (19) and interview_prep_series (17) skills
- Fix `user_invocable` → `user-invocable` in consulting skills
- Split gmail-status.md

### Phase 4: Consolidation

- Merge duplicate skills
- Consolidate consulting skills from 8 to 3
- Convert pre-commit skills to hooks
- Migrate top lever_of_archimedes commands to skills format
- Update skill-template.md in best-practices guide

---

## 6. Assessment of External Audits

### Codex Audit

**Correct**: SessionStart hooks doing real work, `bypassPermissions` dominance, `user_invocable` schema issue, `system_message` field name issue, philosophical inconsistency between planning and execution affordances.

**Partially correct**: "Plan Mode is probably behaving correctly" — plan mode restrictions work, but skill descriptions without `disable-model-invocation: true` load into context and their imperative language competes with plan mode's instruction.

**Overstated**: Changing `bypassPermissions` globally (too disruptive), Telemetry First approach (delays the fix).

**Missing**: The `disable-model-invocation` context removal insight, specific `allowed-tools` per skill, the `/proceeding-now` escape hatch in planning skills.

### Gemini Audit

**Verified non-applicable**: `!command` dynamic context (zero usage), `context: fork` subagent isolation (zero usage).

**Mischaracterized**: `allowed-tools` "privilege escalation" — in `bypassPermissions` mode it acts purely as restriction, not escalation.

**Valid future concerns**: `!command` and `context: fork` are risks to watch in new skill development.

---

## 7. Combined Effect After Phase 1

**Before**: 13 skill descriptions in context including "begin execution immediately", "MANDATORY", "Commit all changes".

**After**: 9 descriptions in context — all plan-compatible or neutral. Execution-oriented descriptions removed via `disable-model-invocation: true`. All 14 skills restricted to minimum necessary tools via `allowed-tools`. 5 auto-invocable skills with write tools have Context Guard sections.

**Residual risk**: `decomposing-functions` remains auto-invocable with write tools but has specific triggers unlikely to match casual plan-mode conversation.

---

## 8. What's Working Well

1. **Two-layer architecture** — Personal vs project tier separation works
2. **Gerund naming convention** — Consistent, confirmed as best practice by official docs
3. **RLHF project** — Gold standard for `allowed-tools` usage
4. **Good patterns exist in project skills** — `audit-resume-matches.md` has "No edits" guard, `scaffold-role.md` has "Phase 1: Analysis (Read-Only)", `qa/fix-presentation.md` offers `--dry-run`
5. **"Instruct Claude, not the user" principle** — Sound curation decision
6. **Hook architecture** — Sophisticated but aimed at catastrophic failures rather than premature execution

---

## Sources

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Code Hooks Documentation](https://code.claude.com/docs/en/hooks)
- Codex audit: `codex_claude_skills_ecosystem_audit_2026-04-01.md`
- Gemini audit: `gemini_skill_audit_report.md`
- Direct filesystem analysis of 68 skill files across `~/Claude/*`
