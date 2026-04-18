"""
Extract Vibe Engineering MEAP V02 content using Docling (CPU).

Outputs:
  - vibe_engineering.md         Full markdown with tables
  - vibe_engineering.json       Structured document model
  - chapters/ch00-ch08.md       Per-chapter splits
  - companion_inventory.md      Catalog of companion repo files
"""

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────
os.environ["OMP_NUM_THREADS"] = "16"

BASE_DIR = Path("/home/brandon_behring/Claude/claude-best-practices")
PDF_PATH = BASE_DIR / "Vibe_Engineering_v2_MEAP (1).pdf"
OUT_DIR = BASE_DIR / "vibe_engineering_extracted"
CHAPTERS_DIR = OUT_DIR / "chapters"
COMPANION_DIR = OUT_DIR / "manning_vibe_engineering-main"

CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)


# ── 1. PDF Extraction via Docling ───────────────────────────────
def extract_pdf():
    """Convert PDF to markdown and JSON using Docling."""
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import (
        AcceleratorOptions,
        PdfPipelineOptions,
        TableFormerMode,
    )
    from docling.document_converter import DocumentConverter, PdfFormatOption

    print("[1/4] Configuring Docling (CPU, 16 threads, accurate tables)...")
    accel = AcceleratorOptions(num_threads=16, device="cpu")
    pipeline_options = PdfPipelineOptions(accelerator_options=accel, do_table_structure=True)
    pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )

    print(f"[2/4] Converting {PDF_PATH.name} ({PDF_PATH.stat().st_size // 1024 // 1024} MB)...")
    result = converter.convert(str(PDF_PATH))

    # Export markdown
    md_path = OUT_DIR / "vibe_engineering.md"
    md_content = result.document.export_to_markdown()
    md_path.write_text(md_content, encoding="utf-8")
    print(f"  → {md_path.name}: {len(md_content):,} chars, {md_content.count(chr(10)):,} lines")

    # Export JSON document model
    json_path = OUT_DIR / "vibe_engineering.json"
    json_content = json.dumps(result.document.export_to_dict(), indent=2, ensure_ascii=False)
    json_path.write_text(json_content, encoding="utf-8")
    print(f"  → {json_path.name}: {len(json_content):,} chars")

    return md_content


# ── 2. Chapter Splitting ────────────────────────────────────────
# Known chapter titles from the PDF TOC
CHAPTER_TITLES = {
    0: "Front Matter",
    1: "Building on Quicksand: The challenges of Vibe Engineering",
    2: "Building a legacy modernization framework powered by Vibe Engineering",
    3: "Context Engineering: Optimizing context for AI Agents",
    4: "LLM-driven data analytics and visualization",
    5: "Continuous AI development",
    6: "A scientific approach for validating LLM-based solutions",
    7: "Vibe Performance Engineering: When assumptions mislead",
    8: "Evaluation is King: Ultra-tight engineering loop for AI-powered codebases",
    9: "FinOps for LLMs: Cost-cutting, confidentiality, and the right chips",
    10: "Code Organization for AI: Tame your codebase with Monorepo & Friends",
}


def split_chapters(md_content: str):
    """Split full markdown into per-chapter files.

    Docling outputs chapter headings as '## N  Title' (double space).
    Subsections are '## N.M ...' — we must NOT match those.
    MEAP V02 contains chapters 1, 2, 3, 6, 7 only.
    """
    print("[3/4] Splitting into chapters...")

    # Match ONLY top-level chapter headings: "## 1  Title" (digit NOT followed by a dot)
    chapter_pattern = re.compile(
        r'^(#{1,2}\s+(\d+)\s{2,}.+)$',
        re.MULTILINE,
    )

    matches = list(chapter_pattern.finditer(md_content))

    if not matches:
        print("  ⚠ No chapter headings found — saving as single file")
        (CHAPTERS_DIR / "ch00_full.md").write_text(md_content, encoding="utf-8")
        return

    print(f"  Found {len(matches)} chapter headings")

    # Front matter: everything before first chapter
    front_matter = md_content[: matches[0].start()].strip()
    if front_matter:
        path = CHAPTERS_DIR / "ch00_front_matter.md"
        path.write_text(f"# Front Matter\n\n{front_matter}", encoding="utf-8")
        print(f"  → ch00_front_matter.md ({len(front_matter):,} chars)")

    # Each chapter: from its heading to the next chapter heading (or EOF)
    for i, match in enumerate(matches):
        ch_num = int(match.group(2))
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md_content)
        chapter_text = md_content[start:end].strip()

        title = CHAPTER_TITLES.get(ch_num, f"Chapter {ch_num}")
        fname = f"ch{ch_num:02d}.md"
        path = CHAPTERS_DIR / fname
        path.write_text(chapter_text, encoding="utf-8")
        print(f"  → {fname}: {title} ({len(chapter_text):,} chars)")


# ── 3. Companion Repo Inventory ─────────────────────────────────
def build_companion_inventory():
    """Build a detailed inventory of the companion code repository."""
    print("[4/4] Building companion repo inventory...")

    if not COMPANION_DIR.exists():
        print("  ⚠ Companion directory not found — skipping inventory")
        return

    lines = [
        "# Vibe Engineering Companion Repository Inventory",
        "",
        "Source: `manning_vibe_engineering-main (1).zip`",
        "",
    ]

    # Global stats
    all_files = list(COMPANION_DIR.rglob("*"))
    all_files = [f for f in all_files if f.is_file()]
    total_size = sum(f.stat().st_size for f in all_files)
    lines.append(f"**Total**: {len(all_files)} files, {total_size / 1024 / 1024:.1f} MB")
    lines.append("")

    # Per-chapter breakdown
    chapter_dirs = sorted(COMPANION_DIR.glob("CH_*"))
    for ch_dir in chapter_dirs:
        ch_num = ch_dir.name.replace("CH_0", "CH_").replace("CH_", "")
        ch_title = CHAPTER_TITLES.get(int(ch_num), "")
        ch_files = [f for f in ch_dir.rglob("*") if f.is_file()]
        ch_size = sum(f.stat().st_size for f in ch_files)

        lines.append(f"## {ch_dir.name}: {ch_title}")
        lines.append(f"**{len(ch_files)} files, {_fmt_size(ch_size)}**")
        lines.append("")

        # File type breakdown
        ext_counts = defaultdict(lambda: {"count": 0, "size": 0})
        for f in ch_files:
            ext = f.suffix.lower() or "(no ext)"
            ext_counts[ext]["count"] += 1
            ext_counts[ext]["size"] += f.stat().st_size

        lines.append("| Type | Count | Size |")
        lines.append("|------|------:|-----:|")
        for ext, info in sorted(ext_counts.items(), key=lambda x: -x[1]["size"]):
            lines.append(f"| `{ext}` | {info['count']} | {_fmt_size(info['size'])} |")
        lines.append("")

        # Key files
        readme = ch_dir / "README.md"
        if readme.exists():
            lines.append("### README Highlights")
            readme_text = readme.read_text(encoding="utf-8", errors="replace")

            # Extract prompts (lines starting with prompt-like patterns)
            prompts = _extract_prompts(readme_text)
            if prompts:
                lines.append(f"**Prompts found: {len(prompts)}**")
                for j, prompt in enumerate(prompts[:5], 1):
                    # Truncate long prompts
                    display = prompt[:200] + "..." if len(prompt) > 200 else prompt
                    lines.append(f"{j}. `{display}`")
                if len(prompts) > 5:
                    lines.append(f"   ... and {len(prompts) - 5} more")
            lines.append("")

        # Notable files (notebooks, large CSVs, HTML reports)
        notable = []
        for f in ch_files:
            rel = f.relative_to(ch_dir)
            size = f.stat().st_size
            if f.suffix in (".ipynb", ".html", ".csv") and size > 100_000:
                notable.append((str(rel), _fmt_size(size)))
            elif f.suffix in (".ipynb",):
                notable.append((str(rel), _fmt_size(size)))

        if notable:
            lines.append("### Notable Files")
            for name, size in notable:
                lines.append(f"- `{name}` ({size})")
            lines.append("")

    # Root README
    root_readme = COMPANION_DIR / "README.md"
    if root_readme.exists():
        lines.append("## Root README")
        lines.append("```")
        lines.append(root_readme.read_text(encoding="utf-8", errors="replace").strip())
        lines.append("```")

    inventory_path = OUT_DIR / "companion_inventory.md"
    inventory_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  → companion_inventory.md ({len(lines)} lines)")


def _extract_prompts(text: str) -> list[str]:
    """Extract prompt-like content from README text."""
    prompts = []
    # Common patterns: quoted prompts, code blocks with prompts, lines with "prompt:" etc.
    # Pattern 1: Lines in code blocks that look like prompts (imperative instructions to AI)
    code_blocks = re.findall(r'```(?:\w*\n)?(.*?)```', text, re.DOTALL)
    for block in code_blocks:
        block = block.strip()
        # Heuristic: if the block contains AI-prompt-like language
        if any(kw in block.lower() for kw in [
            "generate", "create", "write", "implement", "refactor",
            "analyze", "convert", "build", "design", "migrate",
            "optimize", "explain", "suggest", "help me",
        ]):
            prompts.append(block.split("\n")[0].strip())

    # Pattern 2: Lines starting with ">" (blockquotes often used for prompts)
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("> ") and len(line) > 20:
            clean = line.lstrip("> ").strip()
            if any(kw in clean.lower() for kw in [
                "generate", "create", "write", "implement",
                "refactor", "analyze", "build", "migrate",
            ]):
                prompts.append(clean)

    return prompts


def _fmt_size(size_bytes: int) -> str:
    """Format file size for display."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / 1024 / 1024:.1f} MB"
    else:
        return f"{size_bytes / 1024 / 1024 / 1024:.1f} GB"


# ── Main ────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Vibe Engineering MEAP V02 — Content Extraction")
    print("=" * 60)

    # PDF extraction
    md_content = extract_pdf()

    # Chapter splitting
    split_chapters(md_content)

    # Companion inventory (no docling needed)
    build_companion_inventory()

    print("\n" + "=" * 60)
    print("DONE. Outputs in:", OUT_DIR)
    print("=" * 60)


if __name__ == "__main__":
    main()
