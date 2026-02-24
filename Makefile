# Makefile for Claude Best Practices handbook
# Requires: lualatex, latexmk

MAIN = claude_best_practices
OUTDIR = output

.PHONY: pilot digital clean

# Quick test build (single pass, no refs/index)
pilot:
	@mkdir -p $(OUTDIR)
	-lualatex -shell-escape -interaction=nonstopmode -output-directory=$(OUTDIR) $(MAIN).tex

# Full build with refs, TOC, index
digital:
	@mkdir -p $(OUTDIR)
	latexmk -f -lualatex -shell-escape -interaction=nonstopmode -output-directory=$(OUTDIR) $(MAIN).tex

# Clean build artifacts
clean:
	@rm -rf $(OUTDIR)
	@rm -rf _minted-*
	@echo "Cleaned."
