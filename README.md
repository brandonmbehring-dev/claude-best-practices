# Best Practices for Using Claude

**From Personal Mastery to Enterprise Scale**

What Anthropic recommends, what practitioners discover, and where they converge.

## What This Is

A comprehensive guide to using Claude effectively, covering:
- Configuration hierarchy (CLAUDE.md, rules, settings)
- Commands, skills, hooks, and agents
- Context management and memory
- Prompt engineering and cost optimization
- Testing and quality control
- Greenfield and brownfield project workflows
- Automation pipelines and MCP integration
- Anti-patterns and the Claude Maturity Model
- Enterprise deployment at scale

Every practice is tagged:
- **[Official]** -- Anthropic's documented recommendation
- **[Practitioner]** -- Discovered through extensive daily use
- **[Convergence]** -- Both sources agree

## Formats

| Format | Location | Description |
|--------|----------|-------------|
| PDF Handbook | `output/claude_best_practices.pdf` | Full 87-page Tufte-style guide |
| Blog Summary | `blog/blog-summary.md` | 12-page Markdown extract |
| Templates | `templates/` | Copy-paste starter files |

## Building

Requires LuaLaTeX with `latexmk`:

```bash
make pilot    # Quick test build (~30s)
make digital  # Full build with references (~2min)
make validate # Run all validation guards (JSON, hooks, includes, deprecated names)
make all      # validate + digital + quickstart + check
```

### Validation Guards

Run `make validate` before submitting changes. It checks:

| Target | What it catches |
|--------|----------------|
| `validate-json` | Malformed JSON in `templates/` |
| `validate-hooks` | Invalid hook event names vs `docs/valid-hook-events.txt` |
| `validate-includes` | Orphaned `.tex` files not in the build graph |
| `validate-no-deprecated` | Deprecated hook names (PreCommit, PostCommit, etc.) |

Informational (never blocks):

| Target | What it does |
|--------|--------------|
| `check-urls` | Spot-checks 5 critical documentation URLs |
| `check` | Summarizes LaTeX warnings/errors from build logs |

## Templates

Standalone copy-paste files in `templates/`:

| File | Purpose |
|------|---------|
| `minimal-claude-md.md` | 10-line starter CLAUDE.md |
| `production-claude-md.md` | 50-line production CLAUDE.md |
| `settings.json` | Sensible default permissions |
| `custom-command.md` | Slash command template |
| `skill-template.md` | Skill definition template |
| `subagent-template.md` | Subagent definition template |
| `hook-examples.json` | Common hook configurations |
| `rule-with-paths.md` | Rules file with paths: frontmatter |

## Version

v1.0 -- February 2026

Content verified against Anthropic documentation as of February 2026.

## License

CC BY 4.0 -- see [LICENSE](LICENSE).
