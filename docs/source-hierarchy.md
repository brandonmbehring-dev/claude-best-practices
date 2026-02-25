# Source Hierarchy — Claude Best Practices Handbook

**Last updated:** 2026-02-24

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

## Hook Events (Schema-Validated)

The following 17 events are documented at `code.claude.com/docs/en/hooks` and present in the settings schema (the schema also lists `Setup` as an 18th event):

| Event | Matcher Target | Notes |
|-------|---------------|-------|
| `SessionStart` | How session started | `startup`, `resume`, `clear`, `compact` |
| `UserPromptSubmit` | (no matcher) | Always fires |
| `PreToolUse` | Tool name | `Bash`, `Edit\|Write`, `mcp__.*` |
| `PermissionRequest` | Tool name | Does NOT fire in headless mode (`-p`) |
| `PostToolUse` | Tool name | Same matchers as PreToolUse |
| `PostToolUseFailure` | Tool name | Same matchers as PreToolUse |
| `Notification` | Notification type | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog` |
| `SubagentStart` | Agent type | `Bash`, `Explore`, `Plan`, custom names |
| `SubagentStop` | Agent type | Same as SubagentStart |
| `Stop` | (no matcher) | Always fires when Claude finishes responding |
| `TeammateIdle` | (no matcher) | Agent teams only |
| `TaskCompleted` | (no matcher) | Always fires |
| `ConfigChange` | Config source | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `WorktreeCreate` | (no matcher) | Replaces default git worktree behavior |
| `WorktreeRemove` | (no matcher) | Worktree cleanup |
| `PreCompact` | Trigger type | `manual`, `auto` |
| `SessionEnd` | Why ended | `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other` |

**INVALID events (removed from handbook):** `PreCommit`, `PostCommit`, `PreFileWrite`, `PostFileWrite`, `PreBashRun`, `PostBashRun`. These never existed in the schema. The correct pattern is `PreToolUse`/`PostToolUse` with tool name matchers.

## Hook Types (3)

- `"type": "command"` -- shell command (most common)
- `"type": "prompt"` -- single-turn LLM evaluation (Haiku by default)
- `"type": "agent"` -- multi-turn subagent with tool access

## Permission Syntax

Both styles are valid per the settings schema:

- **Glob style:** `Bash(git push *)`, `Edit(/src/**/*.ts)`, `Read(./secrets/**)`
- **Domain constraint:** `WebFetch(domain:example.com)`
- **Plain:** `Bash`, `Edit`, `WebFetch` (matches all uses of that tool)

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Shift+Tab` | Cycle permission modes: Normal -> Auto-Accept -> Plan |
| `Ctrl+G` | Open current plan in external text editor |
| `Alt+T` / `Option+T` | Toggle extended thinking |
| `Ctrl+B` | Background a running task |
| `Ctrl+O` | Toggle verbose mode (show hook output) |
| `Ctrl+C` | Cancel current generation |
| `Esc` | Cancel current input |

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
