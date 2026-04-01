---
name: pipeline-check
description: Verifies pre-merge pipeline readiness by running tests, checking git status, and reporting blockers.
allowed-tools: Bash(pytest:*, git status:*), Read, Glob, Grep
---

# Pipeline Check

<!-- SKILL DESIGN CHECKLIST (from skill_ecosystem_2026-04-01 audit):

  FRONTMATTER (required):
    name:              Gerund convention, lowercase+hyphens, max 64 chars
    description:       Third person, under 250 chars, front-load key use case
    allowed-tools:     ALWAYS specify. Be restrictive. Read-only skills: Read, Grep, Glob

  FRONTMATTER (recommended):
    version:           SemVer (0.1.0)
    effort:            low | medium | high

  FRONTMATTER (conditional):
    disable-model-invocation: true   — For side-effect skills (commit, deploy, generate)
    argument-hint:                    — For skills that take arguments

  CONTEXT GUARD (required for auto-invocable skills with write tools):
    Add a "Context Guard" section at the top of the skill body:
    "If plan mode is active, describe what WOULD be done. Do NOT create/modify files."

  DESCRIPTION RULES:
    - Third person ("Verifies..." not "Verify...")
    - Under 250 chars (truncated in skill listing)
    - No ALL-CAPS imperatives (MANDATORY, ALWAYS, MUST)
    - Front-load the key use case
    - Include 2-3 trigger phrases ("Use for X or Y")

  CONVENTION: Save as .claude/skills/<skill-name>/SKILL.md
  (each skill gets its own directory with a SKILL.md file).
  Supporting files go in the same directory.
  Keep SKILL.md under 500 lines — use progressive disclosure for complex skills.
-->

## Context Guard

If plan mode is active, describe which checks would run and what the expected outcome is.
Do NOT execute tests, run commands, or modify state.

## Process

1. Verify all tests pass: `pytest tests/`
2. Check for uncommitted changes: `git status`
3. Verify no data leakage in feature code
4. Check model metrics logged to MLflow
5. Report readiness status (READY / NOT READY) with specific blockers if NOT READY
