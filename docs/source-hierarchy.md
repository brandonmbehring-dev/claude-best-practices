# Source Hierarchy — Claude Best Practices Handbook

**Last updated:** 2026-03-25

## Canonical Source Precedence

When handbook claims conflict, resolve by source tier (higher wins):

| Tier | Domain | Authority For |
|------|--------|---------------|
| 1 | `code.claude.com/docs/en/*` | Claude Code product behavior, hooks, skills, settings, memory, MCP |
| 2 | `json.schemastore.org/claude-code-settings.json` | Configuration schema truth (hook events, permission syntax, settings keys) |
| 3 | `platform.claude.com/docs/en/*` | API primitives, pricing, prompt caching, batch processing, extended thinking |
| 4 | `support.claude.com`, `privacy.claude.com`, `trust.anthropic.com` | Contractual/compliance claims (certifications, data retention, training) |
| 5 | `claude.com/solutions/*` | Government, enterprise program terms |
| 6 | `www.anthropic.com/news/*`, `www.anthropic.com/engineering/*` | Partnership announcements, research blog posts |

## URL Migration (Feb 2026)

All Claude Code docs migrated from `docs.anthropic.com/en/docs/claude-code/*` to `code.claude.com/docs/en/*` (301 redirects active). API/platform docs remain at `platform.claude.com`.

**Handbook rule:** Always use the canonical domain. Never cite a redirect URL.

## Hook Events (24 Total — Verified 2026-03-25)

The following 24 events are documented at `code.claude.com/docs/en/hooks`. Matchers are specific enum values, not arbitrary regex.

| Event | Matcher Values | Notes |
|-------|---------------|-------|
| `SessionStart` | `startup`, `resume`, `clear`, `compact` | |
| `InstructionsLoaded` | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact` | When CLAUDE.md or rules files load |
| `UserPromptSubmit` | (no matcher) | Always fires |
| `PreToolUse` | Tool name: `Bash`, `Edit`, `Write`, `Read`, `mcp__.*` | |
| `PermissionRequest` | Tool name | Does NOT fire in headless mode (`-p`) |
| `PostToolUse` | Tool name | Same matchers as PreToolUse |
| `PostToolUseFailure` | Tool name | Same matchers as PreToolUse |
| `Notification` | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog` | |
| `Elicitation` | MCP server name | MCP server requests structured user input |
| `ElicitationResult` | MCP server name | User responds to an elicitation dialog |
| `SubagentStart` | Agent type or custom name | `Bash`, `Explore`, `Plan`, custom |
| `SubagentStop` | Agent type or custom name | Same as SubagentStart |
| `Stop` | (no matcher) | Always fires when Claude finishes responding |
| `StopFailure` | `rate_limit`, `authentication_failed`, `billing_error`, `server_error`, `max_output_tokens`, `unknown` | Handle session failures |
| `TeammateIdle` | (no matcher) | Agent teams only |
| `TaskCompleted` | (no matcher) | Always fires |
| `ConfigChange` | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` | |
| `CwdChanged` | (no matcher) | Working directory changed |
| `FileChanged` | Filename basename (e.g., `.envrc`, `.env`) | External file changes |
| `WorktreeCreate` | (no matcher) | Worktree setup |
| `WorktreeRemove` | (no matcher) | Worktree cleanup |
| `PreCompact` | `manual`, `auto` | |
| `PostCompact` | `manual`, `auto` | |
| `SessionEnd` | `clear`, `resume`, `logout`, `prompt_input_exit`, `other` | |

**INVALID events (removed from handbook):** `PreCommit`, `PostCommit`, `PreFileWrite`, `PostFileWrite`, `PreBashRun`, `PostBashRun`. These never existed in the schema. The correct pattern is `PreToolUse`/`PostToolUse` with tool name matchers.

## Hook Types (4)

- `"type": "command"` -- shell command (most common). 10-minute timeout.
- `"type": "http"` -- POST JSON to a URL. 30-second default timeout. Best for webhooks, CI triggers.
- `"type": "prompt"` -- single-turn LLM evaluation (Haiku by default)
- `"type": "agent"` -- multi-turn subagent with tool access

## Permission Syntax

Both styles are valid per the settings schema:

- **Glob style:** `Bash(git push *)`, `Edit(/src/**/*.ts)`, `Read(./secrets/**)`
- **Domain constraint:** `WebFetch(domain:example.com)`
- **Plain:** `Bash`, `Edit`, `WebFetch` (matches all uses of that tool)

## Keyboard Shortcuts (Verified 2026-03-25)

| Shortcut | Action |
|----------|--------|
| `Shift+Tab` / `Alt+M` | Cycle through enabled permission modes (all 6, not fixed 3) |
| `Ctrl+G` | Open prompt or custom response in default text editor |
| `Alt+T` / `Option+T` | Toggle extended thinking |
| `Alt+O` / `Option+O` | Toggle fast mode |
| `Alt+P` / `Option+P` | Switch model |
| `Ctrl+B` | Background a running task (tmux users press twice) |
| `Ctrl+O` | Toggle verbose output (show tool details, expand MCP calls) |
| `Ctrl+T` | Toggle task list display |
| `Ctrl+R` | Reverse search command history |
| `Ctrl+V` | Paste image from clipboard |
| `Ctrl+C` | Cancel current generation |
| `Esc` | Stop Claude mid-action (context preserved) |
| `Esc + Esc` | Open rewind menu (restore conversation, code, or summarize) |

## Cost Claims (Verified Feb 2026)

| Claim | Value | Source |
|-------|-------|--------|
| Prompt cache read savings | 90% (0.1x base input price) | `platform.claude.com/docs/en/build-with-claude/prompt-caching` |
| Batch API discount | 50% off standard prices | `platform.claude.com/docs/en/build-with-claude/batch-processing` |
| Batch size limit | 100,000 requests OR 256 MB | Same |
| Batch result availability | Within 24 hours (most finish <1 hour) | Same |
| Cache write premium (5m) | 1.25x base input price | Prompt caching docs |
| Cache write premium (1h) | 2x base input price | Prompt caching docs |

## Maintenance

- **Monthly:** Re-fetch all Tier 1-3 sources. Check for schema changes.
- **Quarterly:** Verify Tier 4-5 claims (certifications, government programs).
- **On model release:** Update pricing tables and model names.
