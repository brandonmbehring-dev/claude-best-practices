#!/usr/bin/env python3
"""Generate an HTML citation dashboard from LaTeX \\sourceurl{} citations.

Extracts all \\sourceurl{} references from .tex files, groups them by chapter,
and produces a rich single-page HTML dashboard with:
- Clickable URLs
- The claim text surrounding each citation
- Verification date
- HTTP status badge (live check)

Usage:
    python3 scripts/generate_citation_index.py [--check] [--output FILE]

Options:
    --check     Verify each URL returns HTTP 200 (slow, ~30s)
    --output    Output file (default: output/citation_index.html)
"""

import argparse
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def extract_citations(tex_dir: Path) -> dict[str, list[dict]]:
    """Extract all \\sourceurl{} citations grouped by chapter file."""
    citations: dict[str, list[dict]] = defaultdict(list)
    # Pattern: \sourceurl{URL} — capture URL and surrounding context
    url_pattern = re.compile(r'\\sourceurl\{([^}]+)\}')
    # Pattern to extract chapter title from \chapter{Title}
    chapter_pattern = re.compile(r'\\chapter\{([^}]+)\}')

    tex_files = sorted(tex_dir.glob('chapters/*.tex')) + sorted(tex_dir.glob('appendices/*.tex'))
    tex_files.append(tex_dir / 'quickstart_guide.tex')

    for tex_file in tex_files:
        if not tex_file.exists():
            continue
        content = tex_file.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Find chapter title
        chapter_match = chapter_pattern.search(content)
        chapter_title = chapter_match.group(1) if chapter_match else tex_file.stem

        for line_num, line in enumerate(lines, 1):
            for url_match in url_pattern.finditer(line):
                url = url_match.group(1)
                # Extract surrounding context (the line, stripped of LaTeX commands)
                context = line.strip()
                # Clean up LaTeX for display
                context = re.sub(r'\\[a-zA-Z]+\{', '', context)
                context = context.replace('}', '').replace('{', '')
                context = re.sub(r'\\[a-zA-Z]+', '', context)
                context = context.strip(' %~')
                if len(context) > 200:
                    context = context[:200] + '...'

                citations[f"{tex_file.name} — {chapter_title}"].append({
                    'url': url,
                    'line': line_num,
                    'context': context,
                    'file': tex_file.name,
                })

    return citations


def check_url(url: str, timeout: int = 10) -> tuple[int, str]:
    """Check if a URL is reachable. Returns (status_code, status_text)."""
    try:
        req = Request(url, method='HEAD', headers={'User-Agent': 'CitationChecker/1.0'})
        with urlopen(req, timeout=timeout) as resp:
            return resp.status, 'OK'
    except HTTPError as e:
        return e.code, str(e.reason)
    except URLError as e:
        return 0, str(e.reason)
    except Exception as e:
        return 0, str(e)


def generate_html(
    citations: dict[str, list[dict]],
    url_status: Optional[dict[str, tuple[int, str]]] = None,
    verification_date: str = '',
) -> str:
    """Generate the HTML citation dashboard."""
    # Count unique URLs
    all_urls = set()
    total_citations = 0
    for chapter_cites in citations.values():
        for cite in chapter_cites:
            all_urls.add(cite['url'])
            total_citations += 1

    # Group status counts
    ok_count = broken_count = unchecked_count = 0
    if url_status:
        for url in all_urls:
            status = url_status.get(url)
            if status is None:
                unchecked_count += 1
            elif 200 <= status[0] < 400:
                ok_count += 1
            else:
                broken_count += 1
    else:
        unchecked_count = len(all_urls)

    chapters_html = []
    for chapter, cites in citations.items():
        rows = []
        for cite in cites:
            status_badge = ''
            if url_status and cite['url'] in url_status:
                code, text = url_status[cite['url']]
                if 200 <= code < 400:
                    status_badge = f'<span class="badge ok">{code}</span>'
                else:
                    status_badge = f'<span class="badge fail">{code} {text}</span>'
            else:
                status_badge = '<span class="badge unchecked">?</span>'

            rows.append(f'''
            <tr>
              <td class="line">L{cite['line']}</td>
              <td class="context">{_escape(cite['context'])}</td>
              <td class="url"><a href="{_escape(cite['url'])}" target="_blank">{_escape(_shorten(cite['url']))}</a></td>
              <td class="status">{status_badge}</td>
            </tr>''')

        chapters_html.append(f'''
        <section>
          <h2>{_escape(chapter)} <span class="count">({len(cites)} citations)</span></h2>
          <table>
            <thead><tr><th>Line</th><th>Claim Context</th><th>Source URL</th><th>Status</th></tr></thead>
            <tbody>{''.join(rows)}</tbody>
          </table>
        </section>''')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Citation Index — Claude Best Practices Guide</title>
<style>
  :root {{ --bg: #1a1a2e; --card: #252542; --border: #3d3d5c; --text: #eee; --muted: #888; }}
  body {{ font: 14px/1.6 system-ui, sans-serif; margin: 0; background: var(--bg); color: var(--text); }}
  header {{ background: var(--card); padding: 20px 40px; border-bottom: 1px solid var(--border); }}
  header h1 {{ margin: 0 0 8px; font-size: 22px; }}
  .stats {{ display: flex; gap: 24px; font-size: 13px; color: var(--muted); }}
  .stats strong {{ color: var(--text); }}
  main {{ max-width: 1200px; margin: 0 auto; padding: 20px 40px; }}
  section {{ margin-bottom: 32px; }}
  h2 {{ font-size: 16px; margin: 0 0 12px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }}
  .count {{ color: var(--muted); font-weight: normal; font-size: 13px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ text-align: left; padding: 6px 10px; background: var(--card); color: var(--muted); font-size: 11px; text-transform: uppercase; }}
  td {{ padding: 6px 10px; border-bottom: 1px solid var(--border); vertical-align: top; }}
  .line {{ width: 50px; color: var(--muted); font-family: monospace; }}
  .context {{ max-width: 400px; color: #ccc; }}
  .url {{ max-width: 350px; word-break: break-all; }}
  .url a {{ color: #6ea8fe; text-decoration: none; }}
  .url a:hover {{ text-decoration: underline; }}
  .status {{ width: 70px; text-align: center; }}
  .badge {{ padding: 2px 8px; border-radius: 3px; font-size: 11px; font-weight: bold; }}
  .badge.ok {{ background: #0e8a16; color: white; }}
  .badge.fail {{ background: #d73a49; color: white; }}
  .badge.unchecked {{ background: #6b7280; color: white; }}
  tr:hover {{ background: rgba(255,255,255,0.03); }}
</style>
</head>
<body>
<header>
  <h1>Citation Index — Claude Best Practices Guide v2.6</h1>
  <div class="stats">
    <span><strong>{total_citations}</strong> citations</span>
    <span><strong>{len(all_urls)}</strong> unique URLs</span>
    <span><strong>{len(citations)}</strong> chapters</span>
    <span>{'<strong class="badge ok">' + str(ok_count) + ' OK</strong>' if url_status else ''}</span>
    <span>{'<strong class="badge fail">' + str(broken_count) + ' broken</strong>' if broken_count else ''}</span>
    <span>Verified: <strong>{verification_date or 'not checked'}</strong></span>
  </div>
</header>
<main>
{''.join(chapters_html)}
</main>
</body>
</html>'''


def _escape(text: str) -> str:
    """Escape HTML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def _shorten(url: str, max_len: int = 60) -> str:
    """Shorten a URL for display."""
    if len(url) <= max_len:
        return url
    return url[:max_len - 3] + '...'


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Generate HTML citation dashboard')
    parser.add_argument('--check', action='store_true', help='Verify URLs (slow)')
    parser.add_argument('--output', default='output/citation_index.html', help='Output file')
    args = parser.parse_args()

    tex_dir = Path(__file__).parent.parent
    citations = extract_citations(tex_dir)

    if not citations:
        print('No citations found.', file=sys.stderr)
        sys.exit(1)

    total = sum(len(c) for c in citations.values())
    unique = len({cite['url'] for cites in citations.values() for cite in cites})
    print(f'Found {total} citations ({unique} unique URLs) across {len(citations)} files.')

    url_status = None
    verification_date = datetime.now().strftime('%Y-%m-%d')

    if args.check:
        print('Checking URLs...')
        all_urls = {cite['url'] for cites in citations.values() for cite in cites}
        url_status = {}
        for i, url in enumerate(sorted(all_urls), 1):
            status, text = check_url(url)
            url_status[url] = (status, text)
            badge = 'OK' if 200 <= status < 400 else f'FAIL ({status})'
            print(f'  [{i}/{len(all_urls)}] {badge}: {url}')

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    html = generate_html(citations, url_status, verification_date)
    output_path.write_text(html, encoding='utf-8')
    print(f'Generated: {output_path} ({output_path.stat().st_size:,} bytes)')


if __name__ == '__main__':
    main()
