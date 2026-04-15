"""Build companion repo inventory (no docling needed)."""
import re
import sys
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path("/home/brandon_behring/Claude/claude-best-practices")
OUT_DIR = BASE_DIR / "vibe_engineering_extracted"
COMPANION_DIR = OUT_DIR / "manning_vibe_engineering-main"

CHAPTER_TITLES = {
    0: "Front Matter",
    1: "Introduction to Vibe Engineering",
    2: "Legacy Modernization Framework",
    3: "Context is Currency: Precision Prompts",
    4: "Drug Data Science: Vibe Engineering",
    5: "Continuous AI: Pair-Programming Style",
    6: "Scientific Approach to Text-to-SQL",
    7: "Vibe Performance Engineering",
    8: "FinOps for LLMs",
}


def _fmt_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / 1024 / 1024:.1f} MB"
    else:
        return f"{size_bytes / 1024 / 1024 / 1024:.1f} GB"


def _extract_prompts(text: str) -> list[str]:
    prompts = []
    code_blocks = re.findall(r'```(?:\w*\n)?(.*?)```', text, re.DOTALL)
    for block in code_blocks:
        block = block.strip()
        if any(kw in block.lower() for kw in [
            "generate", "create", "write", "implement", "refactor",
            "analyze", "convert", "build", "design", "migrate",
            "optimize", "explain", "suggest", "help me",
        ]):
            prompts.append(block.split("\n")[0].strip())
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


def main():
    lines = [
        "# Vibe Engineering Companion Repository Inventory",
        "",
        "Source: `manning_vibe_engineering-main (1).zip`",
        "",
    ]
    all_files = [f for f in COMPANION_DIR.rglob("*") if f.is_file()]
    total_size = sum(f.stat().st_size for f in all_files)
    lines.append(f"**Total**: {len(all_files)} files, {total_size / 1024 / 1024:.1f} MB")
    lines.append("")

    chapter_dirs = sorted(COMPANION_DIR.glob("CH_*"))
    for ch_dir in chapter_dirs:
        ch_num_str = ch_dir.name.replace("CH_", "")
        ch_num = int(ch_num_str)
        ch_title = CHAPTER_TITLES.get(ch_num, "")
        ch_files = [f for f in ch_dir.rglob("*") if f.is_file()]
        ch_size = sum(f.stat().st_size for f in ch_files)

        lines.append(f"## {ch_dir.name}: {ch_title}")
        lines.append(f"**{len(ch_files)} files, {_fmt_size(ch_size)}**")
        lines.append("")

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

        readme = ch_dir / "README.md"
        if readme.exists():
            lines.append("### README Highlights")
            readme_text = readme.read_text(encoding="utf-8", errors="replace")
            prompts = _extract_prompts(readme_text)
            if prompts:
                lines.append(f"**Prompts found: {len(prompts)}**")
                for j, prompt in enumerate(prompts[:5], 1):
                    display = prompt[:200] + "..." if len(prompt) > 200 else prompt
                    lines.append(f"{j}. `{display}`")
                if len(prompts) > 5:
                    lines.append(f"   ... and {len(prompts) - 5} more")
            else:
                lines.append("No AI prompts detected in README.")
            lines.append("")

        notable = []
        for f in ch_files:
            rel = f.relative_to(ch_dir)
            size = f.stat().st_size
            if f.suffix in (".ipynb",):
                notable.append((str(rel), _fmt_size(size)))
            elif f.suffix in (".html",) and size > 100_000:
                notable.append((str(rel), _fmt_size(size)))
            elif f.suffix in (".csv",) and size > 100_000:
                notable.append((str(rel), _fmt_size(size)))

        if notable:
            lines.append("### Notable Files")
            for name, size in notable:
                lines.append(f"- `{name}` ({size})")
            lines.append("")

    root_readme = COMPANION_DIR / "README.md"
    if root_readme.exists():
        lines.append("## Root README")
        lines.append("```")
        lines.append(root_readme.read_text(encoding="utf-8", errors="replace").strip())
        lines.append("```")

    inventory_path = OUT_DIR / "companion_inventory.md"
    inventory_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Done: {inventory_path} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
