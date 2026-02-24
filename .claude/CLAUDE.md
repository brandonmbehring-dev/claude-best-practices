# Claude Best Practices Guide

## Build Commands
```bash
make pilot    # Quick test build
make digital  # Full build with refs
```

## Writing Standards
- Every practice tagged: [Official], [Practitioner], or [Convergence]
- Margin note categories: [Official], [Tip], [Warning], [Cost], [Enterprise], [Template]
- No personal project names or identifying details in main text (appendix B exempt)
- Concrete but generic examples throughout
- All Anthropic claims include source URL in footnote
- TikZ diagrams for visual concepts
- Max 25 words per margin note

## LaTeX Conventions
- Use `\official{}`, `\practitioner{}`, `\convergence{}` for practice labels
- Use `\marginnote[Category]{text}` for margin notes
- Use `\begin{minted}{language}` for code blocks
- Cross-references with `\cref{}`
- Footnotes for source URLs

## File Organization
- One chapter per file in `chapters/`
- Templates are standalone Markdown/JSON in `templates/`
- Blog summary is extracted Markdown in `blog/`
