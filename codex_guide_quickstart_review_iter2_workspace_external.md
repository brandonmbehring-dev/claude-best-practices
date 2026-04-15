# codex Iteration 2 Review (Workspace + External Research)

## Scope expansion completed
- Ran a broad sweep across `~/Claude/*` and identified 3,651 candidate files with relevant signals.
- Focused deep reads on onboarding/checklist/audit artifacts that repeatedly encode reusable practices.
- Performed external validation against current Claude docs and documentation-architecture references.

## Net-new findings since v1 review

### P0 — External drift: quick start install path appears outdated
- Evidence:
  - Current quick start uses npm install: `quickstart_guide.tex:66`
  - Official quick start now surfaces native installers (curl script, Homebrew, Winget), and includes `/init` in the first workflow:
    - `https://docs.anthropic.com/en/docs/claude-code/quickstart` (install snippets, `/init` example)
- Why this matters:
  - First-run failures and trust hit if users follow stale install path.
- Recommendation:
  - Replace the default install block with official installer-first paths.
  - Keep npm only as optional fallback (if still supported), clearly labeled.

### P0 — External drift: permission mode terminology likely stale in the guide
- Evidence:
  - Guide uses `Normal` / `Auto-Accept` and mentions settings-only `dontAsk`: `quickstart_guide.tex:148`, `appendices/reference_card.tex:59-61`
  - Current permissions docs name modes as `Default`, `Accept Edits`, `Plan`, `Bypass Permissions`:
    - `https://docs.anthropic.com/en/docs/claude-code/iam/permissions`
- Why this matters:
  - Users may not find matching labels in UI/CLI.
- Recommendation:
  - Normalize all mode names to current docs.
  - Add a one-line “legacy naming” note only if needed.

### P1 — Add a dedicated “critical traps before proceeding” box
- Evidence pattern from workspace:
  - `annuity-price-elasticity-v3/QUICK_START.md:68-74` explicitly blocks forward progress until reading known traps.
- Why this matters:
  - Prevents expensive early mistakes; frames “what fails in practice” before scale-up.
- Recommendation:
  - Add a short trap block near minute 10-15 in quick start:
    - context bloat,
    - approving broad diffs,
    - committing without tests,
    - using stale sessions for unrelated tasks.

### P1 — Add competency checkpoints, not just task completion
- Evidence pattern from workspace:
  - `day_one_checklist.md:101-106`, `192-197`, `200-219` uses “Morning checkpoint,” “Afternoon checkpoint,” and “Knowledge check.”
- Why this matters:
  - Better transfer: user proves understanding, not just command execution.
- Recommendation:
  - Add 3 short “Can you now…” checks in quick start:
    - explain your verification loop,
    - identify when to `/clear` vs `/compact`,
    - distinguish project rules vs enforceable hooks.

### P1 — Add content maturity labels to reduce accidental over-trust
- Evidence pattern from workspace audit:
  - Proposed `draft/validated/production` gating: `codex_workspace_audit_report_2026-02-24.md:79-80`, `160-163`
- Why this matters:
  - Large handbooks and templates are often consumed as authoritative even when sections are evolving.
- Recommendation:
  - Add maturity tags at chapter level (or appendix level) and a release note that defines the tags.

### P1 — Add automated consistency checks for narrative claims
- Evidence pattern from workspace audit:
  - Auto-sync/fail-CI pattern for metrics drift: `codex_workspace_audit_report_2026-02-24.md:31-33`, `145-147`
- Why this matters:
  - Prevents “16 chapters vs 15 chapters” and similar trust-breaking mismatches.
- Recommendation:
  - Add a `make validate-doc-claims` step that checks:
    - chapter count claims,
    - cross-ref chapter number labels (`ChN` mentions),
    - anti-pattern count references.

### P2 — Add an evidence-based remediation log format for doc updates
- Evidence pattern from workspace:
  - Strong “Issue → Evidence → Verification” structure in assessment checklist:
    - `temporalcv/docs/ASSESSMENT_CHECKLIST.md:24-37`, `166-174`, `210-214`
- Why this matters:
  - Easier reviewer confidence and faster future maintenance.
- Recommendation:
  - Keep a lightweight `docs/plans/current/review-remediation.md` with per-fix verification entries.

### P2 — Add a compact structured-prompt template to quick start
- Evidence pattern from workspace:
  - Constraint-driven template improves scope control:
    - `PROMPTING_TEMPLATES.md:42-59`, `99-131`
- Why this matters:
  - New users benefit from a repeatable prompt skeleton before learning full prompt engineering chapter.
- Recommendation:
  - Include one 6-line template:
    - `Role`, `Task`, `Constraints`, `Success Criteria`, `Files`, `Validation Command`.

### P2 — Add explicit plan-mode pre-implementation checklist
- Evidence pattern from workspace:
  - Plan-mode prompt asks for files, risks, test impact, dependencies:
    - `PLAN_MODE_THINK_MODES.md:41-50`, `101-110`
- Why this matters:
  - Reduces regressions for multi-file changes.
- Recommendation:
  - Add one “Plan Mode for non-trivial tasks” box to quick start and Ch3 with fixed prompt text.

## External research synthesis (what to align with)
- Claude best-practices docs emphasize clear objectives and acceptance criteria, plus session/context hygiene:
  - `https://docs.anthropic.com/en/docs/claude-code/common-workflows`
- Claude permissions docs indicate current mode naming and behavior:
  - `https://docs.anthropic.com/en/docs/claude-code/iam/permissions`
- Claude quick start uses installer-first setup and `/init` in early flow:
  - `https://docs.anthropic.com/en/docs/claude-code/quickstart`
- Documentation architecture reference (for narrative structure hygiene):
  - Diátaxis 4 forms (tutorial, how-to, reference, explanation):
    - `https://diataxis.fr/start-here/`

## Suggested implementation order (incremental)
1. Fix external-drift risks:
- installer instructions,
- permission mode naming.
2. Fix narrative trust breakers:
- chapter count/cross-ref automation,
- anti-pattern count consistency.
3. Improve onboarding transfer:
- traps block,
- checkpoints,
- compact structured-prompt template,
- plan-mode checklist.
4. Add governance:
- maturity labels,
- evidence-based remediation log.

