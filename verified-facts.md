# Verified Facts — Anthropic Documentation

**Generated**: 2026-02-24
**Purpose**: Single source of truth for the Claude Code Best Practices handbook rewrite.
**Method**: Direct web-fetch from official Anthropic documentation URLs.

**NOTE**: As of Feb 2026, all Claude Code docs have migrated from
`docs.anthropic.com/en/docs/claude-code/*` to `code.claude.com/docs/en/*` (301 redirects).
API/platform docs remain at `platform.claude.com/docs/en/`.

---

## 1. Hooks

**Source**: https://code.claude.com/docs/en/hooks-guide (+ /hooks reference)

**Key Facts**:

### Hook Events (17 total)

| Event | When it fires |
|-------|---------------|
| `SessionStart` | When a session begins or resumes |
| `UserPromptSubmit` | When you submit a prompt, before Claude processes it |
| `PreToolUse` | Before a tool call executes. Can block it |
| `PermissionRequest` | When a permission dialog appears |
| `PostToolUse` | After a tool call succeeds |
| `PostToolUseFailure` | After a tool call fails |
| `Notification` | When Claude Code sends a notification |
| `SubagentStart` | When a subagent is spawned |
| `SubagentStop` | When a subagent finishes |
| `Stop` | When Claude finishes responding |
| `TeammateIdle` | When an agent team teammate is about to go idle |
| `TaskCompleted` | When a task is being marked as completed |
| `ConfigChange` | When a configuration file changes during a session |
| `WorktreeCreate` | When a worktree is being created via `--worktree` or `isolation: "worktree"` |
| `WorktreeRemove` | When a worktree is being removed |
| `PreCompact` | Before context compaction |
| `SessionEnd` | When a session terminates |

### Hook Types (3)

- `"type": "command"` -- runs a shell command (most common)
- `"type": "prompt"` -- single-turn LLM evaluation (Haiku by default, configurable via `model` field)
- `"type": "agent"` -- multi-turn subagent with tool access (up to 50 tool-use turns, 60s default timeout)

### Matcher Syntax

Matchers are regex patterns that filter when a hook fires:

| Event(s) | Matcher filters on | Example values |
|----------|-------------------|----------------|
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` | tool name | `Bash`, `Edit\|Write`, `mcp__.*` |
| `SessionStart` | how session started | `startup`, `resume`, `clear`, `compact` |
| `SessionEnd` | why session ended | `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other` |
| `Notification` | notification type | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog` |
| `SubagentStart`, `SubagentStop` | agent type | `Bash`, `Explore`, `Plan`, or custom agent names |
| `PreCompact` | what triggered compaction | `manual`, `auto` |
| `ConfigChange` | configuration source | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | no matcher support | always fires |

### Exit Codes

- **Exit 0**: action proceeds. stdout added to Claude's context for `UserPromptSubmit` and `SessionStart`.
- **Exit 2**: action is blocked. stderr becomes Claude's feedback.
- **Any other exit code**: action proceeds. stderr logged but not shown to Claude.

### JSON Output (structured)

For `PreToolUse`, JSON stdout with `hookSpecificOutput.permissionDecision` can be:
- `"allow"` -- proceed without permission prompt
- `"deny"` -- cancel tool call, send reason to Claude
- `"ask"` -- show permission prompt to user as normal

### Hook Location (6 places)

| Location | Scope |
|----------|-------|
| `~/.claude/settings.json` | All your projects |
| `.claude/settings.json` | Single project (committable) |
| `.claude/settings.local.json` | Single project (gitignored) |
| Managed policy settings | Organization-wide |
| Plugin `hooks/hooks.json` | When plugin is enabled |
| Skill or agent frontmatter | While skill/agent is active |

### Other Key Details

- Default timeout: 10 minutes (configurable per hook via `timeout` field in seconds)
- All matching hooks run in parallel; identical commands are deduplicated
- `PermissionRequest` hooks do NOT fire in non-interactive mode (`-p`); use `PreToolUse` instead
- `Stop` hooks fire whenever Claude finishes responding, NOT only at task completion
- `stop_hook_active` field in JSON input prevents infinite loops in Stop hooks
- Prompt-based hooks return `{"ok": true}` or `{"ok": false, "reason": "..."}`
- Toggle verbose mode with `Ctrl+O` to see hook output; `claude --debug` for full details
- `/hooks` interactive menu to create/manage hooks
- `"disableAllHooks": true` in settings to disable all hooks

---

## 2. Skills

**Source**: https://code.claude.com/docs/en/skills

**Key Facts**:

### File Location

- Personal: `~/.claude/skills/<skill-name>/SKILL.md`
- Project: `.claude/skills/<skill-name>/SKILL.md`
- Enterprise: via managed settings
- Plugin: `<plugin>/skills/<skill-name>/SKILL.md`

**Precedence**: enterprise > personal > project. Plugin skills use `plugin-name:skill-name` namespace.

### Legacy Compatibility

Custom slash commands (`.claude/commands/`) merged into skills. Both work. If a skill and command share the same name, the skill takes precedence.

### Frontmatter Keys (all optional)

| Field | Description |
|-------|-------------|
| `name` | Display name, becomes `/slash-command`. Lowercase letters, numbers, hyphens only (max 64 chars). If omitted, uses directory name. |
| `description` | (Recommended) What the skill does. Claude uses this to decide when to apply it. |
| `argument-hint` | Hint shown during autocomplete, e.g. `[issue-number]` |
| `disable-model-invocation` | Set to `true` to prevent Claude from auto-loading. Default: `false`. |
| `user-invocable` | Set to `false` to hide from `/` menu. Default: `true`. |
| `allowed-tools` | Tools Claude can use without permission when skill is active. **Key name is `allowed-tools` (hyphenated), NOT `allowed_tools`.** |
| `model` | Model to use when skill is active. |
| `context` | Set to `fork` to run in a forked subagent context. |
| `agent` | Which subagent type to use when `context: fork` is set. |
| `hooks` | Hooks scoped to this skill's lifecycle. |

### String Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking |
| `$ARGUMENTS[N]` | Specific argument by 0-based index |
| `$N` | Shorthand for `$ARGUMENTS[N]` |
| `${CLAUDE_SESSION_ID}` | Current session ID |

### Dynamic Context

- `!`command`` syntax runs shell commands before skill content is sent to Claude
- Include "ultrathink" anywhere in skill content to enable extended thinking

### Skill Budget

- Skill descriptions consume 2% of context window (fallback: 16,000 characters)
- Override with `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable
- `/context` shows warnings about excluded skills

### Permission Control

- `Skill(name)` for exact match in permission rules
- `Skill(name *)` for prefix match with any arguments
- `Skill` to deny all skill tool usage

---

## 3. Sub-agents

**Source**: https://code.claude.com/docs/en/sub-agents

**Key Facts**:

### Built-in Subagents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| **Explore** | Haiku (fast) | Read-only | File discovery, code search, codebase exploration |
| **Plan** | Inherits | Read-only | Codebase research for planning |
| **General-purpose** | Inherits | All tools | Complex research, multi-step operations |
| **Bash** | Inherits | Terminal commands | Running commands in separate context |
| **statusline-setup** | Sonnet | -- | When you run `/statusline` |
| **Claude Code Guide** | Haiku | -- | Questions about Claude Code features |

### Subagent File Location

| Location | Scope | Priority |
|----------|-------|----------|
| `--agents` CLI flag | Current session | 1 (highest) |
| `.claude/agents/` | Current project | 2 |
| `~/.claude/agents/` | All your projects | 3 |
| Plugin's `agents/` directory | Where plugin is enabled | 4 (lowest) |

### Frontmatter Keys

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier, lowercase letters and hyphens |
| `description` | Yes | When Claude should delegate to this subagent |
| `tools` | No | **Key name is `tools` (NOT `allowed_tools` or `allowed-tools`).** Tools the subagent can use. Inherits all if omitted. |
| `disallowedTools` | No | Tools to deny |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit`. Default: `inherit` |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, or `plan` |
| `maxTurns` | No | Maximum agentic turns |
| `skills` | No | Skills to preload into context at startup |
| `mcpServers` | No | MCP servers available to this subagent |
| `hooks` | No | Lifecycle hooks scoped to this subagent |
| `memory` | No | Persistent memory scope: `user`, `project`, or `local` |
| `background` | No | Set to `true` to always run as background task. Default: `false` |
| `isolation` | No | Set to `worktree` for isolated git worktree |

### Key Differences from Skills

- Skills key: `allowed-tools` (hyphenated)
- Subagent key: `tools` (plain)
- Skills use `context: fork` + `agent` to run in subagent
- Subagents use `skills` field to preload skill content
- Subagents cannot spawn other subagents (no nesting)

### Task Tool Syntax

- `Task(worker, researcher)` -- allowlist specific subagents
- `Task` (no parens) -- allow spawning any subagent
- Omit `Task` from tools list -- cannot spawn any subagents
- `Task(agent-name)` restriction only applies to agents running as main thread with `claude --agent`

### Persistent Memory

| Scope | Location |
|-------|----------|
| `user` | `~/.claude/agent-memory/<name>/` |
| `project` | `.claude/agent-memory/<name>/` |
| `local` | `.claude/agent-memory-local/<name>/` |

- First 200 lines of `MEMORY.md` injected at startup
- Read, Write, Edit tools auto-enabled when memory is set

### Background Subagents

- Run concurrently while you continue working
- Permission prompts collected upfront before launching
- Auto-deny anything not pre-approved
- MCP tools not available in background subagents
- `Ctrl+B` to background a running task
- `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` to disable

---

## 4. Settings

**Source**: https://code.claude.com/docs/en/settings

**Key Facts**:

### 5-Level Precedence (highest to lowest)

1. **Managed Settings** (`managed-settings.json`) -- system-level, cannot be overridden
   - macOS: `/Library/Application Support/ClaudeCode/`
   - Linux/WSL: `/etc/claude-code/`
   - Windows: `C:\Program Files\ClaudeCode\`
2. **Command Line Arguments** -- temporary session overrides
3. **Local Project Settings** (`.claude/settings.local.json`) -- personal project, gitignored
4. **Shared Project Settings** (`.claude/settings.json`) -- team-shared, in source control
5. **User Settings** (`~/.claude/settings.json`) -- personal global

### Permission Rule Syntax

**Format**: `Tool` or `Tool(specifier)`

**Evaluation order**: deny first, then ask, then allow. First matching rule wins.

**Correct syntax examples** (uses `*` glob, NOT `:`):

| Rule | Matches |
|------|---------|
| `Bash(npm run *)` | `npm run test`, `npm run lint` |
| `Bash(git push *)` | `git push origin main` |
| `Read(./.env)` | Reading .env file |
| `Read(./secrets/**)` | Recursive directory match |
| `WebFetch(domain:example.com)` | Network requests to that domain |
| `Edit(../docs/)` | File edits in that directory |

**IMPORTANT**: The syntax is `Bash(git push *)` NOT `Bash(git push:*)`. The specifier uses shell-style globbing with `*`.

### Permission Structure

```json
{
  "permissions": {
    "allow": ["Bash(npm run lint)", "Read(~/.zshrc)"],
    "ask": ["Bash(git push *)"],
    "deny": ["Bash(curl *)", "Read(./.env)", "WebFetch"]
  }
}
```

### Notable Settings Keys

- `model` -- default model override (e.g., `"claude-sonnet-4-6"`)
- `availableModels` -- restrict model selection
- `outputStyle` -- adjust system prompt style
- `language` -- Claude's response language
- `cleanupPeriodDays` -- delete inactive sessions (default: 30)
- `defaultMode` -- default permission mode (e.g., `"acceptEdits"`)
- `alwaysThinkingEnabled` -- enable extended thinking by default
- `sandbox.enabled` -- enable bash sandboxing
- `sandbox.autoAllowBashIfSandboxed` -- auto-approve sandboxed commands
- `attribution.commit` -- git commit attribution
- `attribution.pr` -- PR attribution
- `includeCoAuthoredBy` -- DEPRECATED, use `attribution` instead
- `enableAllProjectMcpServers` -- auto-approve all project MCP servers
- `disableAllHooks` -- disable all hooks
- `allowManagedHooksOnly` -- (managed only) block user/project hooks
- `allowManagedPermissionRulesOnly` -- (managed only) block user/project permission rules
- `fileSuggestion` -- custom @ autocomplete script
- `additionalDirectories` -- extra working directories
- `plansDirectory` -- custom plan file location
- `teammateMode` -- agent team display mode
- `autoUpdatesChannel` -- `"stable"` or `"latest"`
- `CLAUDE_CODE_EFFORT_LEVEL` -- `"low"`, `"medium"`, `"high"`
- `$schema` -- `"https://json.schemastore.org/claude-code-settings.json"` for validation

### Configuration File Locations Summary

| Type | User | Project | Local | Managed |
|------|------|---------|-------|---------|
| Settings | `~/.claude/settings.json` | `.claude/settings.json` | `.claude/settings.local.json` | System + `managed-settings.json` |
| Subagents | `~/.claude/agents/` | `.claude/agents/` | -- | -- |
| MCP Servers | `~/.claude.json` | `.mcp.json` | -- | System + `managed-mcp.json` |
| Memory | `~/.claude/CLAUDE.md` | `CLAUDE.md` or `.claude/CLAUDE.md` | `CLAUDE.local.md` | -- |

---

## 5. MCP (Model Context Protocol)

**Source**: https://code.claude.com/docs/en/mcp

**Key Facts**:

### Installation

Three transport options:

```bash
# HTTP (recommended for remote servers)
claude mcp add --transport http <name> <url>

# SSE (deprecated, use HTTP where available)
claude mcp add --transport sse <name> <url>

# stdio (local processes)
claude mcp add [options] <name> -- <command> [args...]
```

**Option ordering**: All options (`--transport`, `--env`, `--scope`, `--header`) must come BEFORE the server name. `--` separates server name from command/args.

### Scopes (3 levels)

| Scope | Storage | Description |
|-------|---------|-------------|
| `local` (default) | `~/.claude.json` under project path | Private, current project only |
| `project` | `.mcp.json` in project root | Team-shared, committed to VCS |
| `user` | `~/.claude.json` | Personal, all projects |

**NOTE**: Scope names changed from older versions: `project` was called `local`, `user` was called `global`.

**Precedence**: local > project > user (when same server name exists at multiple scopes).

### Tool Search

- **Threshold**: Activates when MCP tool descriptions exceed 10% of context window (auto mode, default)
- **Configure**: `ENABLE_TOOL_SEARCH` env var: `auto` (default), `auto:<N>` (custom %), `true`, `false`
- **Requires**: Sonnet 4+ or Opus 4+ models (Haiku does not support tool search)

### Output Limits

- Warning threshold: 10,000 tokens per MCP tool output
- Default maximum: 25,000 tokens
- Configure with `MAX_MCP_OUTPUT_TOKENS` environment variable
- Startup timeout: `MCP_TIMEOUT` environment variable (milliseconds)

### MCP Resources

- Reference with `@server:protocol://resource/path` syntax
- Fuzzy-searchable in @ mention autocomplete

### MCP Prompts

- Available as `/mcp__servername__promptname` commands
- Arguments are space-separated after the command

### Claude Code as MCP Server

```bash
claude mcp serve
```

### OAuth 2.0

- `/mcp` command within Claude Code for authentication
- Supports pre-configured OAuth with `--client-id`, `--client-secret`, `--callback-port`
- `MCP_CLIENT_SECRET` env var for non-interactive

### Managed MCP

- `managed-mcp.json` in system directories for exclusive control
- `allowedMcpServers` / `deniedMcpServers` in managed settings for policy-based control
- Three restriction types: `serverName`, `serverCommand` (exact array match), `serverUrl` (wildcard `*`)

### Environment Variable Expansion in .mcp.json

- `${VAR}` -- expands to env var value
- `${VAR:-default}` -- fallback to default
- Supported in: `command`, `args`, `env`, `url`, `headers`

---

## 6. Memory

**Source**: https://code.claude.com/docs/en/memory

**Key Facts**:

### Two Kinds of Persistent Memory

1. **Auto memory**: Claude automatically saves useful context (project patterns, commands, preferences). Stored at `~/.claude/projects/<project>/memory/`. First 200 lines of `MEMORY.md` loaded into system prompt.
2. **CLAUDE.md files**: Markdown files you write and maintain with instructions/rules.

### Memory Hierarchy (6 levels)

| Type | Location | Shared With |
|------|----------|-------------|
| Managed policy | System paths (e.g., `/Library/Application Support/ClaudeCode/CLAUDE.md`) | All users in org |
| Project memory | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team via VCS |
| Project rules | `./.claude/rules/*.md` | Team via VCS |
| User memory | `~/.claude/CLAUDE.md` | Just you (all projects) |
| Project memory (local) | `./CLAUDE.local.md` | Just you (current project) |
| Auto memory | `~/.claude/projects/<project>/memory/` | Just you (per project) |

### CLAUDE.md Imports

- `@path/to/import` syntax for importing files
- Both relative and absolute paths allowed
- Relative paths resolve relative to file containing the import, not working directory
- Recursive imports up to max depth of 5 hops
- NOT evaluated inside markdown code spans/blocks
- First-time external imports show approval dialog (one-time per project)

### Modular Rules (`.claude/rules/`)

- All `.md` files discovered recursively
- Path-specific rules via `paths:` YAML frontmatter with glob patterns
- Rules without `paths:` field load unconditionally
- Subdirectories and symlinks supported
- User-level rules in `~/.claude/rules/` (lower priority than project rules)

### /memory Command

- Opens file selector to edit any memory file in system editor
- Includes auto memory entrypoint alongside CLAUDE.md files

### /init Command

- Bootstrap a CLAUDE.md for your codebase

### /compact Command

- `/compact <instructions>` to manually compact with focus instructions
- Auto compaction triggers at ~95% context capacity
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` to trigger compaction at custom percentage

### Additional Directories

- `--add-dir` flag for additional directories
- CLAUDE.md files from `--add-dir` NOT loaded by default
- Set `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` to load them

### Auto Memory Control

```bash
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1  # Force off
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=0  # Force on
```

- Being rolled out gradually; set to `0` to opt in

---

## 7. Batch Processing

**Source**: https://platform.claude.com/docs/en/build-with-claude/batch-processing

**Key Facts**:

### Limits

- **100,000** Message requests per batch OR **256 MB** in size, whichever is reached first
- **24 hours** expiry: batches expire if processing does not complete within 24 hours
- **29 days** result availability after batch creation
- Most batches complete within **1 hour**

### Pricing

**50% discount** on all standard API prices (input and output tokens).

| Model | Batch Input | Batch Output |
|-------|-------------|--------------|
| Claude Opus 4.6 | $2.50/MTok | $12.50/MTok |
| Claude Opus 4.5 | $2.50/MTok | $12.50/MTok |
| Claude Opus 4.1 | $7.50/MTok | $37.50/MTok |
| Claude Opus 4 | $7.50/MTok | $37.50/MTok |
| Claude Sonnet 4.6 | $1.50/MTok | $7.50/MTok |
| Claude Sonnet 4.5 | $1.50/MTok | $7.50/MTok |
| Claude Sonnet 4 | $1.50/MTok | $7.50/MTok |
| Claude Haiku 4.5 | $0.50/MTok | $2.50/MTok |
| Claude Haiku 3.5 | $0.40/MTok | $2/MTok |
| Claude Haiku 3 | $0.125/MTok | $0.625/MTok |

### Features

- All active models supported
- Any Messages API request can be batched (vision, tool use, system messages, multi-turn, betas)
- NOT covered by Zero Data Retention (ZDR) arrangements
- Results in `.jsonl` format; may not match input order (use `custom_id` to match)
- Result types: `succeeded`, `errored`, `canceled`, `expired`
- Prompt caching works with batches (30-98% cache hit rates typical, best-effort)
- Workspace-scoped (isolated within the Workspace)
- 1-hour cache duration recommended for better cache hits in batches

---

## 8. Prompt Caching

**Source**: https://platform.claude.com/docs/en/build-with-claude/prompt-caching

**Key Facts**:

### Two Modes

1. **Automatic caching**: Add `cache_control` at top level of request body. System auto-applies breakpoint to last cacheable block.
2. **Explicit cache breakpoints**: Place `cache_control` on individual content blocks.

### TTLs

- **5 minutes** (default) -- `"ttl": "5m"` or no TTL specified
- **1 hour** (extended) -- `"ttl": "1h"` at additional cost
- Cache refreshed for no additional cost on each hit

### Cache Duration Configuration

```json
"cache_control": {
    "type": "ephemeral",
    "ttl": "5m" | "1h"
}
```

### Pricing Multipliers

- **5-minute cache write**: 1.25x base input tokens price
- **1-hour cache write**: 2x base input tokens price
- **Cache read/hit**: 0.1x base input tokens price (90% savings on reads)

### Minimum Cacheable Prompt Length

| Model(s) | Minimum Tokens |
|----------|---------------|
| Claude Opus 4.6, Opus 4.5 | 4,096 |
| Claude Sonnet 4.6, Sonnet 4.5, Opus 4.1, Opus 4, Sonnet 4, Sonnet 3.7 | 1,024 |
| Claude Haiku 4.5 | 4,096 |
| Claude Haiku 3.5, Haiku 3 | 2,048 |

### What Can Be Cached

- Tool definitions (`tools` array)
- System messages (`system` array)
- Text messages (`messages.content` for user and assistant turns)
- Images and documents (in user turns)
- Tool use and tool results

### What Cannot Be Cached

- Thinking blocks (cannot be cached directly with `cache_control`, but CAN be cached alongside other content in assistant turns)
- Sub-content blocks (e.g., citations -- cache the top-level document block instead)
- Empty text blocks

### Cache Invalidation Hierarchy

`tools` -> `system` -> `messages`

Changes at each level invalidate that level and all subsequent levels:
- Modifying tool definitions invalidates everything
- Web search/citations toggle invalidates system + messages
- Speed setting change invalidates system + messages
- `tool_choice` changes invalidate messages only
- Image changes invalidate messages only

### Cache Isolation

- Starting Feb 5, 2026: workspace-level isolation (previously organization-level)
- Exact matching: 100% identical prompt segments required
- No effect on output token generation

### Supported Models

Claude Opus 4.6, Opus 4.5, Opus 4.1, Opus 4, Sonnet 4.6, Sonnet 4.5, Sonnet 4, Sonnet 3.7 (deprecated), Haiku 4.5, Haiku 3.5 (deprecated), Haiku 3

---

## 9. Pricing

**Source**: https://platform.claude.com/docs/en/about-claude/pricing

**Key Facts**:

### Model Pricing (Standard)

| Model | Input | Output |
|-------|-------|--------|
| Claude Opus 4.6 | $5/MTok | $25/MTok |
| Claude Opus 4.5 | $5/MTok | $25/MTok |
| Claude Opus 4.1 | $15/MTok | $75/MTok |
| Claude Opus 4 | $15/MTok | $75/MTok |
| Claude Sonnet 4.6 | $3/MTok | $15/MTok |
| Claude Sonnet 4.5 | $3/MTok | $15/MTok |
| Claude Sonnet 4 | $3/MTok | $15/MTok |
| Claude Sonnet 3.7 (deprecated) | $3/MTok | $15/MTok |
| Claude Haiku 4.5 | $1/MTok | $5/MTok |
| Claude Haiku 3.5 | $0.80/MTok | $4/MTok |
| Claude Opus 3 (deprecated) | $15/MTok | $75/MTok |
| Claude Haiku 3 | $0.25/MTok | $1.25/MTok |

### Fast Mode Pricing (Opus 4.6 only, research preview)

- Input: $30/MTok (6x standard)
- Output: $150/MTok (6x standard)
- Includes full 1M context window at no additional long context charge
- Stacks with prompt caching and data residency multipliers
- NOT available with Batch API

### Long Context Pricing (>200K input tokens)

Applies to Opus 4.6, Sonnet 4.6, Sonnet 4.5, Sonnet 4 at standard speed with 1M context enabled:

| Model | <= 200K input | > 200K input |
|-------|--------------|--------------|
| Opus 4.6 | $5 in / $25 out | $10 in / $37.50 out |
| Sonnet 4.6/4.5/4 | $3 in / $15 out | $6 in / $22.50 out |

- 1M context is beta for usage tier 4+ organizations
- 200K threshold based on input tokens only (cache reads/writes count)
- All tokens billed at premium rate once threshold exceeded

### Data Residency Pricing

- US-only inference via `inference_geo` parameter: 1.1x multiplier on all token pricing
- Applies to Opus 4.6 and newer models on Claude API (1P) only
- Global routing (default) uses standard pricing

### Tool Use Overhead

- Tool use system prompt: 346 tokens (`auto`/`none`) or 313 tokens (`any`/`tool`) for Claude 4.x
- Bash tool: 245 additional input tokens
- Text editor: 700 additional input tokens
- Web search: $10 per 1,000 searches (plus standard token costs)
- Web fetch: No additional cost (standard token costs only)
- Code execution: Free with web search/fetch; otherwise $0.05/hour per container (1,550 free hours/month, 5-min minimum)

---

## 10. Best Practices

**Source**: https://code.claude.com/docs/en/best-practices

**Key Facts**:

### Core Constraint

"Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills."

### Top Recommendations

1. **Give Claude a way to verify its work** -- include tests, screenshots, or expected outputs. "This is the single highest-leverage thing you can do."
2. **Explore first, then plan, then code** -- use Plan Mode (`Ctrl+G` to edit plan). Four phases: Explore, Plan, Implement, Commit.
3. **Provide specific context in prompts** -- reference files, mention constraints, point to patterns.
4. **Write an effective CLAUDE.md** -- run `/init` to generate starter; keep concise; treat like code.
5. **Configure permissions** -- `/permissions` to allowlist safe commands; `/sandbox` for OS-level isolation.
6. **Use CLI tools** -- `gh`, `aws`, `gcloud`, `sentry-cli` etc. for external service interaction.
7. **Connect MCP servers** -- `claude mcp add` for Notion, Figma, databases, etc.
8. **Set up hooks** -- deterministic actions that must happen every time.
9. **Create skills** -- `SKILL.md` files for domain knowledge and reusable workflows.
10. **Create custom subagents** -- specialized assistants in `.claude/agents/`.

### Session Management

- **`Esc`**: Stop mid-action (context preserved)
- **`Esc + Esc` or `/rewind`**: Rewind to previous checkpoint
- **`/clear`**: Reset context between unrelated tasks (critical for performance)
- **`/compact <instructions>`**: Manual compaction with focus
- **`claude --continue`**: Resume most recent conversation
- **`claude --resume`**: Select from recent conversations
- **`/rename`**: Name sessions for later retrieval

### Common Failure Patterns

1. **Kitchen sink session**: multiple unrelated tasks polluting context. Fix: `/clear` between tasks.
2. **Correcting over and over**: context polluted with failed approaches. Fix: after 2 failures, `/clear` and rewrite prompt.
3. **Over-specified CLAUDE.md**: too long, Claude ignores half. Fix: prune ruthlessly.
4. **Trust-then-verify gap**: plausible code without edge cases. Fix: always provide verification.
5. **Infinite exploration**: unbounded investigation. Fix: scope narrowly or use subagents.

### Scaling Patterns

- **Headless mode**: `claude -p "prompt"` for CI, scripts, automation. Output formats: text, JSON, stream-json.
- **Fan out**: Loop `claude -p` across files with `--allowedTools` for scoping.
- **Writer/Reviewer pattern**: Separate sessions for implementation and review.
- **`--dangerously-skip-permissions`**: Only in sandboxed containers without internet.

---

## 11. Claude Code Overview

**Source**: https://code.claude.com/docs/en/overview

**Key Facts**:

### What Claude Code Is

"Claude Code is an AI-powered coding assistant that helps you build features, fix bugs, and automate development tasks. It understands your entire codebase and can work across multiple files and tools to get things done."

### Available Surfaces

1. **Terminal CLI** -- full-featured, primary interface
2. **VS Code** -- extension with inline diffs, @-mentions, plan review
3. **JetBrains** -- plugin for IntelliJ, PyCharm, WebStorm, etc.
4. **Desktop app** -- standalone, visual diffs, multiple sessions, cloud sessions
5. **Web** -- browser-based, no local setup, also on Claude iOS app

### Installation Methods

- **Native install (recommended)**: `curl -fsSL https://claude.ai/install.sh | bash` (auto-updates)
- **Homebrew**: `brew install --cask claude-code` (does NOT auto-update)
- **WinGet**: `winget install Anthropic.ClaudeCode` (does NOT auto-update)
- **Windows PowerShell**: `irm https://claude.ai/install.ps1 | iex`

### Key Capabilities

- Automate tedious tasks (tests, lint, merge conflicts, dependencies)
- Build features and fix bugs from plain language descriptions
- Create commits and pull requests directly
- Connect tools via MCP (open standard)
- Customize with CLAUDE.md, skills, hooks
- Run agent teams (multiple parallel agents)
- Pipe, script, and automate with CLI
- Work from anywhere (web, iOS, desktop, terminal, IDE)

### Integration Points

| Use case | Best option |
|----------|-------------|
| Start locally, continue on mobile | Web or Claude iOS app |
| Automate PR reviews and issue triage | GitHub Actions or GitLab CI/CD |
| Route bugs from Slack to PRs | Slack integration |
| Debug live web applications | Chrome extension |
| Build custom agents | Agent SDK |

### Agent Loop

Claude Code operates as an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with development tools. Unlike a chatbot, it can autonomously explore, plan, and implement. Sessions are persistent and reversible via checkpoints.

---

## Key Changes Since Early 2026

### Documentation URL Migration

All Claude Code docs moved from `docs.anthropic.com/en/docs/claude-code/*` to `code.claude.com/docs/en/*` with 301 redirects. API docs remain at `platform.claude.com`.

### Model Naming

Current frontier models include Claude Opus 4.6, Sonnet 4.6. Claude Sonnet 3.7 is now marked as deprecated. Claude Opus 3 is also deprecated.

### New Features Since Jan 2026

- **Fast Mode**: Opus 4.6 only, 6x pricing, research preview
- **Agent teams**: Multiple agents coordinating across separate sessions
- **Plugins**: Marketplace-based extension system (`/plugin`)
- **Worktree isolation**: `isolation: "worktree"` for subagents
- **Tool Search**: Dynamic MCP tool loading (auto at 10% context threshold)
- **Data residency**: `inference_geo` parameter for US-only inference (1.1x multiplier)
- **Prompt-based and agent-based hooks**: `type: "prompt"` and `type: "agent"` alongside `type: "command"`
- **Auto memory**: Persistent per-project memory Claude maintains automatically
- **Sandbox mode**: `/sandbox` for OS-level isolation
- **Desktop app**: Standalone application with visual diffs
- **Web interface**: Browser-based Claude Code at claude.ai/code
- **1M context window**: Beta for tier 4+ orgs (Opus 4.6, Sonnet 4.6/4.5/4)
- **Code execution tool**: Free with web search/fetch, otherwise $0.05/hr
- **Cache isolation change**: Workspace-level (from Feb 5, 2026), previously organization-level

### Skills vs. Commands

"Custom slash commands have been merged into skills." Both `.claude/commands/` and `.claude/skills/` work. Skills take precedence if names conflict. Skills follow the Agent Skills open standard (agentskills.io).

### MCP Scope Renaming

- Old `project` scope is now `local`
- Old `global` scope is now `user`
- New `project` scope means shared via `.mcp.json`
