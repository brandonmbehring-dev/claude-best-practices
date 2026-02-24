# Best Practices for Using Claude: What Anthropic Recommends, What Practitioners Discover, and Where They Converge

*A practitioner's handbook for getting real value from Claude Code — from first session to enterprise deployment.*

---

After using Claude Code daily across 20+ projects for over a year, I compiled my hard-won patterns and cross-referenced them against Anthropic's official documentation. Some matched. Some surprised me. Some things the docs don't mention at all.

This post extracts the highest-impact practices from a full handbook (v2.0, 70+ pages). Every practice is tagged:

- **[Official]** — Anthropic's documented recommendation
- **[Practitioner]** — Discovered through extensive daily use
- **[Convergence]** — Both sources agree

---

## Part I: Foundations — What Everyone Needs

### Understand the Mental Model

Claude Code is an agent loop: prompt → reason → tool → observe → repeat. Three things define the system:

1. **Context window** — finite workspace, not infinite memory
2. **Tool use** — Claude calls tools (Read, Edit, Bash), each consuming context
3. **Configuration layers** — CLAUDE.md, rules, settings, output styles shape behavior

### Four Engineering Principles

These principles become *more* important when AI generates code:

1. **Never fail silently** — configure Claude to surface problems, not work around them
2. **Simplicity over complexity** — simple code is easier for Claude to reason about
3. **Immutability by default** — pure functions are easier to test and modify
4. **Fail fast with diagnostics** — error messages should include what failed AND what to do

### Your First CLAUDE.md

**[Official]** Run `/init` to auto-generate one. Then refine:

```markdown
# Demand Forecasting

## Build & Verify
- `pytest tests/` — run test suite
- `mypy src/` — type checking
- `ruff check src/` — lint

## Architecture
- src/features/ — feature engineering pipelines
- src/models/ — model training and evaluation
- src/data/ — data loading and validation
- notebooks/ — exploratory analysis
- tests/ — mirrors src/ structure

## Standards
- Type hints on all function signatures
- Run tests after every code change
- Never commit without passing lint + tests
```

**[Practitioner]** Include what Claude can't infer. Exclude what it can.

---

## Part II: Personal Practice — Daily Workflows

### Prompting That Works

**[Practitioner]** Build a precision vocabulary:

| Natural Language | Precise Version |
|-----------------|-----------------|
| "Clean this data" | `validate schema, impute nulls with median, drop rows where target is NaN` |
| "Train a model" | `fit XGBoost on train split, evaluate AUC on val, log params to MLflow` |
| "Check if this works" | `validate: run pytest, check no data leakage, verify feature distributions match prod` |

### Context as Currency

**[Practitioner]** The Two-Failure Rule: after two corrections, `/clear` and write a better prompt. Three rounds of "no, that's not what I meant" produces ~2,500 tokens of noise.

**[Practitioner]** Maintain `CURRENT_WORK.md` for 30-second context resume:

```markdown
## Right Now
Refactoring feature engineering to use sklearn Pipelines.

## Next Step
Write tests verifying no leakage across CV folds.
```

### The Edit-Test-Commit Loop

**[Convergence]** "Give Claude a way to verify its work" is the single highest-leverage practice.

- **6-layer validation**: types → input checks → unit → integration → E2E → property tests
- **Phase-appropriate standards**: exploration (manual OK) → development (80% coverage) → production (full validation)
- **Test-first with Claude**: describe interface → tests → implementation → automatic verification

### Extending Claude

**[Convergence]** The golden rule: if a standard is non-negotiable, make it a hook. If advisory, put it in CLAUDE.md.

Four mechanisms, in order of complexity: Commands → Skills → Hooks → MCP Servers.

---

## Part III: Advanced Craft — Mastery Patterns

### CLAUDE.md Architecture

**[Practitioner]** Hub-and-spoke: one shared-patterns directory, each project imports via `@~/shared-patterns/git.md`. Update once, all projects inherit.

### Agents & Parallel Work

Delegate when: independent, context-heavy, parallelizable, needs fresh perspective.
Do directly when: quick, context-dependent, sequential, simple.

**[Official]** Writer/Reviewer pattern: one session makes changes, another reviews the diff without context about intent. Catches errors the writer is blind to.

### Seven Anti-Patterns (with Recovery Guides)

| Anti-Pattern | Prevention | Recovery |
|-------------|------------|---------|
| Context Overload | Hub-and-spoke, rules, hooks | Split CLAUDE.md, move to rules |
| Kitchen Sink Session | `/clear` between tasks | Stop, note state, `/clear` |
| Over-Correcting | Two-failure rule | `/clear`, write better prompt |
| Permanent Prototype | Phase transition checklists | Add DEVELOPMENT phase today |
| Pipeline Direction | Mark generated files | `git checkout` + edit source |
| Verification Gap | Tests with code, hooks | Test 3 critical functions first |
| Big-Bang Refactoring | Extract→Test→Harden→Promote | `git stash`, restart incrementally |

---

## Part IV: Team & Enterprise

### Team Patterns

- Commit `settings.json` for team standards
- Keep `settings.local.json` for personal preferences
- New team members productive on day 1 via committed configuration

### Enterprise at Scale

Certifications: SOC 2 Type II, ISO 27001, ISO 42001, FedRAMP High, HIPAA BAA.

Enterprise/API data is **never** used for model training by default.

Cost optimization: prompt caching (90%) + Batch API (50%) = 70%+ combined savings.

---

## Try This

Three exercises from the handbook, completable in 10 minutes each:

1. **Audit one feature engineering function** against the four principles: silently drops NaN rows? Too long? Mutates its input DataFrame? Vague error messages?
2. **Run `/init`** on your current project. Add deny rules for `.env*`, `data/raw/**`, and credentials. Start a session and verify Claude reads your CLAUDE.md.
3. **Take your last 3 prompts** and rewrite them with precise verbs (validate schema, fit on train split, check no leakage) and verification criteria. Estimate how many correction rounds each rewrite would have saved.

---

## Get the Full Handbook

This post is extracted from a 70+ page handbook with TikZ diagrams, before/after examples, decision frameworks, and copy-paste templates.

**Want the templates?** Star the repo: [github.com/bbehring/claude-best-practices](https://github.com/bbehring/claude-best-practices)

**Want the full PDF?** Download from the repo's releases page.

**Want help implementing this for your team?** I consult on AI-assisted development workflows. [Contact me on LinkedIn](https://linkedin.com/in/brandonbehring).

---

*Content verified against Anthropic documentation as of February 2026. Licensed CC BY 4.0.*

*Generated with Claude Code.*
