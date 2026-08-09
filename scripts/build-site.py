#!/usr/bin/env python3
"""Build the specassay.com static site into public-out/.

- Homepage: site/index.html (hand-authored) -> /index.html
- Field guide: docs/field-guide.md rendered to /field-guide/index.html, wrapped
  in the shared shell, with docs/images/ copied to /field-guide/images/.

Zero external dependencies. Re-run after editing docs/field-guide.md so the
served page matches the source. (dryfoos.com uses the same pre-build pattern.)
"""
from __future__ import annotations
import html, posixpath, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public-out"
GH = "https://github.com/rdryfoos/specassay/blob/main"


def resolve_href(u: str) -> str:
    """Field-guide links are relative to docs/. Keep site-local ones; point repo
    files (other .md docs, samples) at GitHub so they aren't dead on the site."""
    if u.startswith(("http://", "https://", "#", "mailto:", "/")) or u.startswith("images/"):
        return u
    return f"{GH}/{posixpath.normpath(posixpath.join('docs', u))}"

NAV = """  <header class="top">
    <div class="brand"><a href="/" style="color:inherit">SpecAssay</a> <span class="of">hallmark the work</span></div>
    <nav>
      <a href="/field-guide">Field guide</a>
      <a href="https://loupe.dryfoos.com/">Loupe</a>
      <a href="https://github.com/rdryfoos/specassay">GitHub</a>
    </nav>
  </header>"""

FOOTER = """  <footer>
    <div class="row">
      <div>SpecAssay hallmarks the work; <a href="https://loupe.dryfoos.com/">Loupe</a> reads the mark.<br>A Spec Kit bundle — the thread lives in the repo.</div>
      <div style="text-align:right"><a href="https://github.com/rdryfoos/specassay">GitHub</a><br><a href="https://dryfoos.com/">dryfoos.com</a></div>
    </div>
  </footer>"""


def inline(t: str) -> str:
    codes: list[str] = []
    t = re.sub(r"`([^`]+)`", lambda m: codes.append(m.group(1)) or f"\x00{len(codes)-1}\x00", t)
    t = html.escape(t, quote=False)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{resolve_href(m.group(2))}">{m.group(1)}</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", t)
    t = re.sub(r"\x00(\d+)\x00", lambda m: "<code>" + html.escape(codes[int(m.group(1))], quote=False) + "</code>", t)
    return t


def render_md(md: str) -> str:
    lines = md.split("\n")
    out: list[str] = []
    i, n = 0, len(lines)
    para: list[str] = []

    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(para).strip()) + "</p>")
            para.clear()

    while i < n:
        line = lines[i]
        # fenced code
        if line.startswith("```"):
            flush_para()
            i += 1
            buf = []
            while i < n and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            out.append("<pre><code>" + html.escape("\n".join(buf), quote=False) + "</code></pre>")
            continue
        # standalone image
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", line)
        if m:
            flush_para()
            out.append(f'<img src="{m.group(2)}" alt="{html.escape(m.group(1), quote=True)}">')
            i += 1
            continue
        # heading
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush_para()
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2).strip())}</h{lvl}>")
            i += 1
            continue
        # table
        if line.lstrip().startswith("|") and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1]):
            flush_para()
            def cells(row: str) -> list[str]:
                row = row.strip()
                if row.startswith("|"): row = row[1:]
                if row.endswith("|"): row = row[:-1]
                return [c.strip() for c in row.split("|")]
            header = cells(line)
            i += 2
            body = []
            while i < n and lines[i].lstrip().startswith("|"):
                body.append(cells(lines[i])); i += 1
            th = "".join(f"<th>{inline(c)}</th>" for c in header)
            trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
            out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>")
            continue
        # horizontal rule
        if re.match(r"^\s*---+\s*$", line):
            flush_para()
            out.append("<hr>")
            i += 1
            continue
        # unordered list
        if re.match(r"^\s*[-*]\s+", line):
            flush_para()
            items = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i])); i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue
        # ordered list
        if re.match(r"^\s*\d+\.\s+", line):
            flush_para()
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i])); i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
            continue
        # blockquote
        if line.lstrip().startswith(">"):
            flush_para()
            buf = []
            while i < n and lines[i].lstrip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i])); i += 1
            out.append("<blockquote>" + inline(" ".join(buf).strip()) + "</blockquote>")
            continue
        # blank line
        if not line.strip():
            flush_para()
            i += 1
            continue
        para.append(line)
        i += 1
    flush_para()
    return "\n".join(out)


def page(title: str, desc: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<div class="wrap">
{NAV}
{body}
{FOOTER}
</div>
</body>
</html>
"""


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    # homepage + assets
    shutil.copy(ROOT / "site" / "index.html", OUT / "index.html")
    shutil.copytree(ROOT / "site" / "assets", OUT / "assets")

    # field guide
    md = (ROOT / "docs" / "field-guide.md").read_text(encoding="utf-8")
    rendered = render_md(md)
    body = (
        '<article class="doc">\n'
        '<p class="doc-eyebrow">SpecAssay field guide</p>\n'
        f"{rendered}\n"
        '<a class="doc-back" href="/">← Back to SpecAssay</a>\n'
        "</article>"
    )
    fg = OUT / "field-guide"
    fg.mkdir()
    (fg / "index.html").write_text(
        page("Field guide — SpecAssay", "A visual tour of SpecAssay, the trace-manifest, and Loupe — one screenshot at a time.", body),
        encoding="utf-8",
    )
    shutil.copytree(ROOT / "docs" / "images", fg / "images")

    print(f"built specassay site -> {OUT}")
    for p in sorted(OUT.rglob("*")):
        if p.is_file():
            print("  ", p.relative_to(OUT))


if __name__ == "__main__":
    main()
