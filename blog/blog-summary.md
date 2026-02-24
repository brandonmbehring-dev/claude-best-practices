# Best Practices for Using Claude: What Anthropic Recommends, What Practitioners Discover, and Where They Converge

*A practitioner's guide to getting real value from Claude Code — beyond the defaults.*

---

After using Claude Code daily across 20+ projects for over a year, I compiled my hard-won patterns and cross-referenced them against Anthropic's official documentation. Some matched. Some surprised me. Some things the docs don't mention at all.

This post extracts the highest-impact practices from a full handbook I published (link below). Every practice is tagged:

- **[Official]** — Anthropic's documented recommendation
- **[Practitioner]** — Discovered through extensive daily use
- **[Convergence]** — Both sources agree

---

## 1. The Configuration Hierarchy: Your AI's Operating Manual

Most developers use Claude Code with zero configuration. This is like using an IDE with default settings — functional but not leveraged.

### CLAUDE.md Is Everything

**[Official]** Run `/init` to auto-generate a starter CLAUDE.md. Claude analyzes your repo and proposes conventions.

**[Official]** Include: build commands Claude can't guess, code style rules, architecture decisions, testing instructions. Exclude: what Claude can infer from the codebase.

**[Practitioner]** Quality test: if Claude keeps violating a rule, one of three things is true: (1) the CLAUDE.md is too long, (2) the rule contradicts another rule, or (3) the rule should be a hook.

### The Hub-and-Spoke Pattern

**[Practitioner]** For teams managing many repos, maintain a central "hub" repo with shared patterns referenced via `@~/hub/patterns/`. This prevents duplication across repos.

```markdown
# Project CLAUDE.md (spoke)
@~/hub/patterns/git.md
@~/hub/patterns/testing.md

## Project-Specific
- Build: `make digital`
- Test: `pytest tests/`
```

### Conditional Rules

**[Official]** Place `.md` files in `.claude/rules/` with `paths:` frontmatter to control when they load.

Without this, a rule about SQL formatting loads when you're editing React components, wasting context and occasionally causing Claude to apply the wrong conventions.

```markdown
---
paths: backend/**/*.py
---
# Backend Python Rules
- Use SQLAlchemy 2.0 async syntax
- All endpoints need OpenAPI docstrings
```

---

## 2. Commands, Skills, Hooks, Agents: The Extension Hierarchy

Claude Code ships with four extension mechanisms, forming a hierarchy of increasing autonomy.

### Commands: Prompt Templates

**[Official]** Markdown files in `.claude/commands/` invoked as `/command-name`.

**[Practitioner]** The best commands encode *decisions*, not just shortcuts:

```markdown
# .claude/commands/next.md
Check the current project state:
1. Read CURRENT_WORK.md for context
2. Run `git status` and `git diff --stat`
3. Check for failing tests
4. Recommend the single highest-priority next action
```

### Skills: Domain Knowledge + Workflows

**[Official]** `.claude/skills/` with YAML frontmatter. Skills that orchestrate multiple scripts produce the highest value.

### Hooks: Enforcement, Not Advice

**[Convergence]** The golden rule: if a standard is non-negotiable, make it a hook. If it's advisory, put it in CLAUDE.md.

- **CLAUDE.md**: "Always run tests before committing." → Claude may forget.
- **Hook**: `PreCommit → pytest` → Tests run every time. Cannot be forgotten.

### Subagents and Agent Teams

**[Official]** Subagents run in isolated context, preventing research from polluting your main session. Agent Teams (research preview) add multi-agent collaboration with shared task lists.

**[Practitioner]** Match complexity to the mechanism: command → skill → subagent → agent team. Most developers jump to subagents when a skill would suffice.

---

## 3. Context Management: Your Scarcest Resource

### The Two-Failure Rule

**[Practitioner]** After two failed corrections on the same issue, `/clear` and write a better initial prompt. The cost of accumulated bad context exceeds the cost of starting fresh.

Three rounds of "no, that's not what I meant" produces ~2000 tokens of noise that actively degrades subsequent responses.

### The CURRENT_WORK.md Pattern

**[Practitioner]** Maintain a `CURRENT_WORK.md` at project root for 30-second context resume:

```markdown
## Right Now
Refactoring payment processing to async handlers.

## Next Step
Write integration tests for new async PaymentProcessor.

## Context When I Return
- 3 of 5 handler methods converted, 2 remaining
- Existing tests still pass
```

---

## 4. Cost Optimization

**[Official]** Three mechanisms for dramatic cost reduction:

| Mechanism | Savings | Best For |
|-----------|---------|----------|
| Prompt caching | 90% on cached inputs | Repeated tool defs, system prompts |
| Batch API | 50% discount | Bulk migrations, code review |
| Combined | 70%+ total | High-volume pipelines |

**[Practitioner]** Default to Sonnet for development. Escalate to Opus for architecture decisions and complex debugging. Haiku for bulk formatting.

---

## 5. Starting New Projects: The First Week Protocol

**[Convergence]** Three investments on day one compound into dramatically better outcomes:

1. **`/init`** — generate CLAUDE.md from project structure
2. **Deny rule for secrets** — `"Read(.env*)": deny`
3. **PreCommit test hook** — tests run on every commit

### Test-First with Claude

**[Practitioner]** Describe the interface → Claude writes tests → Claude writes implementation → tests run automatically.

```
Prompt: "Create a rate limiter class.
Token bucket algorithm. Configurable rate and burst.
Thread-safe. Returns (allowed, retry_after).
Write tests first, then implementation."
```

---

## 6. Refactoring Legacy Code: The Incremental Protocol

**[Practitioner]** Never attempt a big-bang rewrite. Use four-step increments:

1. **Extract** — isolate the function/module
2. **Test** — write characterization tests capturing *current* behavior
3. **Harden** — refactor with tests as safety net
4. **Promote** — move to production, verify no regressions

Each step fits in 25 minutes. Commit after each step. If interrupted, the project is always working.

**[Official]** Writer/Reviewer pattern: one session refactors, a separate session reviews for regressions.

### Characterization Tests

**[Convergence]** Before changing any code, have Claude write tests for how it *works today* — not how it *should* work:

```
Prompt: "Read src/payments/legacy_processor.py.
Write tests documenting its exact current behavior.
Do NOT test how it SHOULD work.
Test how it DOES work."
```

---

## 7. Seven Anti-Patterns

| Anti-Pattern | Symptom | Prevention |
|-------------|---------|------------|
| Context Overload | Claude ignores CLAUDE.md rules | Keep under 500 lines; use hub-and-spoke |
| Kitchen Sink Session | Quality degrades mid-session | `/clear` between unrelated tasks |
| Over-Correcting | 3+ rounds of corrections | Two-failure rule: `/clear` + better prompt |
| Permanent Prototype | No tests after weeks | Explicit phase transition checklists |
| Pipeline Direction | Downstream edits overwritten | Document flow; mark generated files |
| Verification Gap | "It looked correct" bugs | Always provide tests/verification criteria |
| Big-Bang Refactoring | Half-finished rewrites | Extract → Test → Harden → Promote |

---

## 8. The Claude Maturity Model

| Level | Name | Timeline | Milestone |
|-------|------|----------|-----------|
| L1 | Conversational | Week 1 | Create first CLAUDE.md |
| L2 | Configured | Weeks 2-4 | 5+ commands in a workflow chain |
| L3 | Systematic | Months 2-3 | Hub repo with 3+ spoke projects |
| L4 | Autonomous | Months 3-6 | Autonomous quality pipeline |
| L5 | Enterprise | Month 6+ | Team-wide deployment with metrics |

**Promote when friction justifies it, not on a schedule.** Most solo developers should stabilize at L3. L4-L5 add value primarily for teams.

---

## 9. Enterprise at Scale

For the decision-makers: Claude has been deployed at serious scale.

| Organization | Scale | Highlight |
|-------------|-------|-----------|
| Deloitte | 470K employees | Role-customized Claude personas |
| Cognizant | 350K employees | Legacy modernization |
| Snowflake | 12.6K customers | >90% text-to-SQL accuracy ($200M deal) |
| TELUS | 57K employees | 100B tokens/month |
| ServiceNow | 29K employees | 95% reduction in seller prep time |

Certifications: SOC 2 Type II, ISO 27001, ISO 42001, FedRAMP High, HIPAA BAA.

Enterprise/API data is **never** used for model training by default.

---

## Get the Full Guide

This post is extracted from a 58-page handbook with TikZ diagrams, detailed examples, and copy-paste templates.

**Want the templates?** Star the repo: [github.com/bbehring/claude-best-practices](https://github.com/bbehring/claude-best-practices)

**Want the full PDF?** Download from the repo's releases page.

**Want help implementing this for your team?** I consult on AI-assisted development workflows. [Contact me on LinkedIn](https://linkedin.com/in/brandonbehring).

---

*Content verified against Anthropic documentation as of February 2026. Licensed CC BY 4.0.*

*Generated with Claude Code.*
