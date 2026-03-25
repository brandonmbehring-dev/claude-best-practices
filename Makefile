# Makefile for Claude Best Practices handbook
# Requires: lualatex, latexmk

MAIN = claude_best_practices
QUICKSTART = quickstart_guide
OUTDIR = output
LATEXMK_FLAGS = -lualatex -shell-escape -interaction=nonstopmode -file-line-error

.PHONY: pilot digital quickstart all check check-strict validate validate-json validate-hooks validate-includes validate-no-deprecated validate-doc-claims check-urls clean

# Quick test build (single pass, no refs/index)
pilot:
	@mkdir -p $(OUTDIR)
	lualatex -shell-escape -interaction=nonstopmode -file-line-error -output-directory=$(OUTDIR) $(MAIN).tex

# Full build with refs, TOC, index
digital:
	@mkdir -p $(OUTDIR)
	latexmk $(LATEXMK_FLAGS) -output-directory=$(OUTDIR) $(MAIN).tex

# Quick start guide (standalone ~6 page PDF)
# Depends on handbook .aux for xr-hyper cross-references.
# If handbook hasn't been built yet, build it first.
quickstart: $(OUTDIR)/$(MAIN).aux
	@mkdir -p $(OUTDIR)
	latexmk $(LATEXMK_FLAGS) -output-directory=$(OUTDIR) $(QUICKSTART).tex

$(OUTDIR)/$(MAIN).aux: $(MAIN).tex
	@mkdir -p $(OUTDIR)
	latexmk $(LATEXMK_FLAGS) -output-directory=$(OUTDIR) $(MAIN).tex

# Build everything: validate first, then build, then informational check
all: validate digital quickstart check

# Umbrella: run all validation guards (blocks on failure)
validate: validate-json validate-hooks validate-includes validate-no-deprecated validate-doc-claims

# --- Quality checks ---

# Informational: print summary, always exit 0
check:
	@for LOG in $(OUTDIR)/$(MAIN).log $(OUTDIR)/$(QUICKSTART).log; do \
	  if [ -f "$$LOG" ]; then \
	    NAME=$$(basename "$$LOG" .log); \
	    echo "=== $$NAME ==="; \
	    ERRORS=$$(grep -c '^!' "$$LOG" 2>/dev/null || true); \
	    WARNINGS=$$(grep -c 'Warning' "$$LOG" 2>/dev/null || true); \
	    OVERFULL=$$(grep -c 'Overfull' "$$LOG" 2>/dev/null || true); \
	    UNDERFULL=$$(grep -c 'Underfull' "$$LOG" 2>/dev/null || true); \
	    UNDEF=$$(grep -c 'undefined' "$$LOG" 2>/dev/null || true); \
	    MULTIDEF=$$(grep -c 'multiply defined' "$$LOG" 2>/dev/null || true); \
	    MISSCHAR=$$(grep -c 'Missing character' "$$LOG" 2>/dev/null || true); \
	    RERUN=$$(grep -c 'Rerun' "$$LOG" 2>/dev/null || true); \
	    echo "  Errors:            $$ERRORS"; \
	    echo "  Warnings:          $$WARNINGS"; \
	    echo "  Overfull boxes:    $$OVERFULL"; \
	    echo "  Underfull boxes:   $$UNDERFULL"; \
	    echo "  Undefined refs:    $$UNDEF"; \
	    echo "  Multiply defined:  $$MULTIDEF"; \
	    echo "  Missing characters:$$MISSCHAR"; \
	    echo "  Rerun needed:      $$RERUN"; \
	    echo ""; \
	  fi; \
	done

# Strict: exit non-zero on errors
check-strict:
	@FAIL=0; \
	for LOG in $(OUTDIR)/$(MAIN).log $(OUTDIR)/$(QUICKSTART).log; do \
	  if [ -f "$$LOG" ]; then \
	    NAME=$$(basename "$$LOG" .log); \
	    ERRORS=$$(grep -c '^!' "$$LOG" 2>/dev/null || true); \
	    if [ "$$ERRORS" -gt 0 ]; then \
	      echo "FAIL: $$NAME has $$ERRORS error(s)"; \
	      grep '^!' "$$LOG" | head -5; \
	      FAIL=1; \
	    fi; \
	  fi; \
	done; \
	if [ "$$FAIL" -eq 1 ]; then exit 1; fi; \
	echo "check-strict: PASS (zero errors)"

# --- Validation guards ---

# Validate all JSON files parse correctly
validate-json:
	@echo "=== JSON validation ==="
	@FAIL=0; \
	for f in templates/*.json; do \
	  if ! jq empty "$$f" 2>/dev/null; then \
	    echo "FAIL: $$f is not valid JSON"; FAIL=1; \
	  else \
	    echo "  OK: $$f"; \
	  fi; \
	done; \
	if [ "$$FAIL" -eq 1 ]; then exit 1; fi; \
	echo "validate-json: PASS"

# Validate hook event names against canonical allowlist
validate-hooks:
	@echo "=== Hook event validation ==="
	@FAIL=0; \
	for f in templates/*.json; do \
	  EVENTS=$$(jq -r '.hooks // {} | keys[]' "$$f" 2>/dev/null); \
	  for ev in $$EVENTS; do \
	    if ! grep -qx "$$ev" docs/valid-hook-events.txt; then \
	      echo "FAIL: $$f uses invalid hook event '$$ev'"; FAIL=1; \
	    fi; \
	  done; \
	done; \
	if [ "$$FAIL" -eq 1 ]; then exit 1; fi; \
	echo "validate-hooks: PASS"

# Detect orphaned chapter files not in the build include graph
validate-includes:
	@echo "=== Include-graph check ==="
	@FAIL=0; \
	INCLUDED=$$(grep -oP '\\input\{chapters/[^}]+' $(MAIN).tex | \
	  sed 's/\\input{//' | sed 's/$$/.tex/'); \
	for f in chapters/*.tex; do \
	  BASE=$$f; \
	  if ! echo "$$INCLUDED" | grep -qx "$$BASE"; then \
	    echo "FAIL: $$BASE exists but is not in build include graph"; FAIL=1; \
	  fi; \
	done; \
	if [ "$$FAIL" -eq 1 ]; then exit 1; fi; \
	echo "validate-includes: PASS"

# Catch deprecated hook event names in source files
validate-no-deprecated:
	@echo "=== Deprecated hook name check ==="
	@HITS=$$(grep -rlE 'PreCommit|PostCommit|PreFileWrite|PostFileWrite|PreBashRun|PostBashRun' \
	  chapters/*.tex appendices/*.tex templates/*.json $(QUICKSTART).tex 2>/dev/null | \
	  grep -v 'source-hierarchy' || true); \
	if [ -n "$$HITS" ]; then \
	  echo "FAIL: Deprecated hook event names found in:"; \
	  echo "$$HITS"; exit 1; \
	fi; \
	echo "validate-no-deprecated: PASS"

# Validate doc claims against source of truth (chapter counts, mode names, etc.)
validate-doc-claims:
	@echo "=== Doc-claims validation ==="
	@FAIL=0; \
	ACTUAL=$$(grep -c '\\input{chapters/' $(MAIN).tex); \
	for f in $(QUICKSTART).tex blog/blog-summary.md; do \
	  if [ -f "$$f" ]; then \
	    CLAIMS=$$(grep -oP '\d+ chapters' "$$f" | grep -oP '\d+'); \
	    for c in $$CLAIMS; do \
	      if [ "$$c" != "$$ACTUAL" ]; then \
	        echo "FAIL: $$f claims $$c chapters, actual is $$ACTUAL"; FAIL=1; \
	      fi; \
	    done; \
	  fi; \
	done; \
	AP_ACTUAL=$$(grep -c '\\antipattern{' chapters/11_antipatterns.tex 2>/dev/null || echo 0); \
	AP_CLAIMS=$$(grep -oP '(six|seven|eight|nine|\d+)\s+(traps|anti.?patterns)' $(QUICKSTART).tex blog/blog-summary.md 2>/dev/null || true); \
	if [ -n "$$AP_CLAIMS" ]; then \
	  echo "  Anti-pattern count in source: $$AP_ACTUAL"; \
	  echo "  Claims found: $$AP_CLAIMS"; \
	fi; \
	STALE=$$(grep -rn 'Normal mode\|Auto-Accept' $(QUICKSTART).tex chapters/ appendices/ 2>/dev/null || true); \
	if [ -n "$$STALE" ]; then \
	  echo "FAIL: Stale permission mode names found:"; \
	  echo "$$STALE"; FAIL=1; \
	fi; \
	echo "  --- Version-sensitive content (review per edition) ---"; \
	grep -rn 'Opus [0-9]\|Sonnet [0-9]\|Haiku [0-9]' $(QUICKSTART).tex chapters/ appendices/ 2>/dev/null || echo "  (none found)"; \
	REFS=$$(grep -rn 'Ch[0-9]\|chapter [0-9]' $(QUICKSTART).tex blog/ 2>/dev/null || true); \
	if [ -n "$$REFS" ]; then \
	  echo "  WARN: Hardcoded chapter references:"; \
	  echo "$$REFS"; \
	fi; \
	if [ "$$FAIL" -eq 1 ]; then exit 1; fi; \
	echo "validate-doc-claims: PASS"

# Informational: check all sourceurl citations (never blocks build)
# Auto-extracted from \sourceurl{} in .tex files (40 unique URLs as of v2.6)
CRITICAL_URLS = \
  https://code.claude.com/docs/en/hooks \
  https://code.claude.com/docs/en/best-practices \
  https://code.claude.com/docs/en/settings \
  https://code.claude.com/docs/en/skills \
  https://code.claude.com/docs/en/mcp \
  https://code.claude.com/docs/en/overview \
  https://code.claude.com/docs/en/memory \
  https://code.claude.com/docs/en/sub-agents \
  https://code.claude.com/docs/en/agent-teams \
  https://code.claude.com/docs/en/plugins \
  https://code.claude.com/docs/en/sandboxing \
  https://code.claude.com/docs/en/common-workflows \
  https://code.claude.com/docs/en/statusline \
  https://platform.claude.com/docs/en/build-with-claude/extended-thinking \
  https://platform.claude.com/docs/en/build-with-claude/prompt-caching \
  https://platform.claude.com/docs/en/agent-sdk/overview \
  https://code.claude.com/docs/en/commands \
  https://code.claude.com/docs/en/costs \
  https://code.claude.com/docs/en/discover-plugins \
  https://code.claude.com/docs/en/fast-mode \
  https://code.claude.com/docs/en/github-actions \
  https://code.claude.com/docs/en/how-claude-code-works \
  https://code.claude.com/docs/en/interactive-mode \
  https://code.claude.com/docs/en/model-config \
  https://code.claude.com/docs/en/permissions \
  https://code.claude.com/docs/en/remote-control \
  https://code.claude.com/docs/en/web-scheduled-tasks \
  https://platform.claude.com/docs/en/about-claude/pricing \
  https://platform.claude.com/docs/en/build-with-claude/batch-processing \
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview \
  https://claude.com/solutions/government \
  https://trust.anthropic.com/ \
  https://privacy.claude.com/en/articles/10015870-what-certifications-has-anthropic-obtained \
  https://privacy.claude.com/en/articles/7996885-how-do-you-use-personal-data-in-model-training \
  https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan \
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents \
  https://www.anthropic.com/news/deloitte-anthropic-partnership \
  https://www.anthropic.com/news/anthropic-accenture-partnership \
  https://www.anthropic.com/news/snowflake-anthropic-expanded-partnership \
  https://github.blog/news-insights/product-news/bringing-developer-choice-to-copilot/

check-urls:
	@echo "=== URL spot-check (informational) ==="
	@for url in $(CRITICAL_URLS); do \
	  STATUS=$$(curl -sL -o /dev/null -w '%{http_code}' --max-time 10 "$$url" 2>/dev/null); \
	  if [ "$$STATUS" = "200" ] || [ "$$STATUS" = "301" ] || [ "$$STATUS" = "302" ]; then \
	    echo "  OK ($$STATUS): $$url"; \
	  else \
	    echo "  WARN ($$STATUS): $$url"; \
	  fi; \
	done; \
	echo "check-urls: DONE (informational only)"

# Generate HTML citation dashboard
citations:
	@python3 scripts/generate_citation_index.py --output $(OUTDIR)/citation_index.html

# Generate citation dashboard with live URL checking
citations-check:
	@python3 scripts/generate_citation_index.py --check --output $(OUTDIR)/citation_index.html

# --- Cleanup ---

clean:
	@rm -rf $(OUTDIR)
	@rm -rf _minted-*
	@find . -name "*.aux" -delete 2>/dev/null || true
	@find . -name "*.log" -not -path "./$(OUTDIR)/*" -delete 2>/dev/null || true
	@find . -name "*.out" -delete 2>/dev/null || true
	@find . -name "*.toc" -delete 2>/dev/null || true
	@find . -name "*.fls" -delete 2>/dev/null || true
	@find . -name "*.fdb_latexmk" -delete 2>/dev/null || true
	@find . -name "*.synctex.gz" -delete 2>/dev/null || true
	@find . -name "*.bbl" -delete 2>/dev/null || true
	@find . -name "*.bcf" -delete 2>/dev/null || true
	@find . -name "*.blg" -delete 2>/dev/null || true
	@find . -name "*.run.xml" -delete 2>/dev/null || true
	@find . -name "*.glo" -delete 2>/dev/null || true
	@find . -name "*.gls" -delete 2>/dev/null || true
	@find . -name "*.glg" -delete 2>/dev/null || true
	@find . -name "*.idx" -delete 2>/dev/null || true
	@find . -name "*.ilg" -delete 2>/dev/null || true
	@find . -name "*.ind" -delete 2>/dev/null || true
	@find . -type d -name "_minted-*" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned."
