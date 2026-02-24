# Makefile for Claude Best Practices handbook
# Requires: lualatex, latexmk

MAIN = claude_best_practices
QUICKSTART = quickstart_guide
OUTDIR = output
LATEXMK_FLAGS = -lualatex -shell-escape -interaction=nonstopmode -file-line-error

.PHONY: pilot digital quickstart all check check-strict clean

# Quick test build (single pass, no refs/index)
pilot:
	@mkdir -p $(OUTDIR)
	lualatex -shell-escape -interaction=nonstopmode -file-line-error -output-directory=$(OUTDIR) $(MAIN).tex

# Full build with refs, TOC, index
digital:
	@mkdir -p $(OUTDIR)
	latexmk $(LATEXMK_FLAGS) -output-directory=$(OUTDIR) $(MAIN).tex

# Quick start guide (standalone ~6 page PDF)
quickstart:
	@mkdir -p $(OUTDIR)
	latexmk $(LATEXMK_FLAGS) -output-directory=$(OUTDIR) $(QUICKSTART).tex

# Build everything + informational check
all: digital quickstart check

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
