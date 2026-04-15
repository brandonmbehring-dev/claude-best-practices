# Gemini Skill Audit Report: Plan Mode Bypass Analysis

## Executive Summary
This audit investigates the architectural interaction between custom skills (typically stored in `~/.claude/skills/` or project-level `.claude/skills/`) and Claude Code's "Plan Mode". The core issue—skills causing Claude to perform mutating work while in Plan Mode—stems from a conflict between skill-level permissions and session-level restrictions. 

*Note: Direct inspection of `~/claude/*` was restricted by workspace boundaries, so this audit is based on the reference architectures, templates, and documentation found within the `claude-best-practices` repository.*

## Root Cause Analysis: Why Claude Does Work in Plan Mode

### 1. `allowed-tools` Privilege Escalation
In Claude Code, the `allowed-tools` YAML frontmatter in a `SKILL.md` file (e.g., `allowed-tools: [Bash, Replace, Write]`) grants the skill permission to use those tools **without prompting the user**. 
- **The Vulnerability:** If a skill is auto-applied while the user is in Plan Mode (which is intended to be read-only), the skill's `allowed-tools` whitelist supersedes the Plan Mode restrictions. Claude will silently execute `Bash` or file-writing tools because the active skill explicitly permits it.

### 2. Overly Broad `description` Triggers
Claude auto-applies skills based on the semantic matching of their `description` field against the user's prompt. 
- **The Vulnerability:** If a skill in `~/.claude/skills/` has a generic description (e.g., "Helps analyze and test Python code"), Claude may silently activate it during a routine Plan Mode exploration. Once active, the skill's escalated tool permissions are granted immediately, leading to unexpected background work.

### 3. Dynamic Context Execution (`!command`)
Skills support dynamic context injection using the `!command` syntax (e.g., `!git status` or `!python prep.py`), which runs shell commands to inject live data into the prompt.
- **The Vulnerability:** These shell commands are executed **at skill load time**, before the prompt is fully evaluated by the LLM. If a user enters Plan Mode and Claude evaluates a skill containing a state-mutating `!command`, that command executes instantly, violating the read-only expectation of Plan Mode.

### 4. Subagent Forking (`context: fork`)
Skills configured with `context: fork` launch a subagent to handle long-running analysis.
- **The Vulnerability:** Subagents operate with their own isolated context and tool permissions. If a skill forks a subagent during Plan Mode, the subagent may not inherit the read-only constraint of the parent session, allowing it to perform mutating actions asynchronously.

## Constructive Feedback & Best Practices for Improvement

To fix the ecosystem and prevent skills from breaking Plan Mode, implement the following design changes across all skills in `~/claude/*`:

### 1. Enforce the Principle of Least Privilege
**Current Anti-Pattern:** Blanket allowing `Bash` in skills (e.g., `allowed-tools: [Bash, Read, Glob]`).
**Recommendation:** Remove mutating tools (`Bash`, `Replace`, `WriteFile`) from `allowed-tools` unless absolutely necessary for the skill's core function. If a skill is meant for analysis, restrict it strictly to read-only tools: `[Read, Glob, Grep]`. 

### 2. Disable Auto-Invocation for Mutating Skills
**Current Anti-Pattern:** Allowing dangerous or state-mutating skills to auto-load based on broad descriptions.
**Recommendation:** For any skill that modifies the codebase, add the `disable-model-invocation: true` flag to its frontmatter. This forces the user to explicitly invoke the skill via a slash command (e.g., `/run-tests`), preventing accidental triggering during Plan Mode exploration.

### 3. Sanitize Dynamic Contexts
**Current Anti-Pattern:** Using `!command` for scripts that modify state or have side effects.
**Recommendation:** Audit all `!command` blocks in your `SKILL.md` files. Ensure they only run read-only binaries (e.g., `git log`, `cat`, `ls`). Move any setup or state-mutating logic into explicit tool calls within the skill's instruction body, so they remain subject to standard permission checks if not explicitly whitelisted.

### 4. Limit Global Skill Scope
**Current Anti-Pattern:** Placing highly specific or aggressive workflow skills in the global `~/.claude/skills/` directory.
**Recommendation:** Migrate project-specific skills out of the global directory and into local `.claude/skills/` folders. Reserve `~/.claude/skills/` only for universally applicable, strictly read-only workflows. This minimizes the "blast radius" of an aggressive skill polluting Plan Mode in unrelated projects.
