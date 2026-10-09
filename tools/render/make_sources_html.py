"""Turn docs/3D_SOURCES.md into web/showcase/sources.html (so the showroom can link to it).

Run after editing the markdown:  .venv\\Scripts\\python.exe tools\\render\\make_sources_html.py
Small converter for this one file: headings, paragraphs, lists, tables, **bold**, `code`, links.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "docs" / "3D_SOURCES.md"
OUT = ROOT / "web" / "showcase" / "sources.html"


def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r'(?<!href=")(?<!">)(https?://[^\s<|)]+)', r'<a href="\1">\1</a>', s)
    s = s.replace("DERIVED – confirm with caliper", '<span class="flag d">DERIVED – confirm with caliper</span>')
    s = re.sub(r"NOT PUBLISHED[^<|]*", lambda m: f'<span class="flag n">{m.group(0)}</span>', s)
    return s


def convert(md: str) -> str:
    out, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[2:]]
            out.append('<div class="tw"><table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>")
            out += ["<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body]
            out.append("</tbody></table></div>")
            continue
        m = re.match(r"^(#{1,3}) (.*)", ln)
        if m:
            out.append(f"<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>")
        elif re.match(r"^\s*(-|\d+\.) ", ln):
            tag = "ol" if re.match(r"^\s*\d+\.", ln) else "ul"
            out.append(f"<{tag}>")
            while i < len(lines) and re.match(r"^\s*(-|\d+\.) ", lines[i]):
                out.append("<li>" + inline(re.sub(r"^\s*(-|\d+\.) ", "", lines[i])) + "</li>")
                i += 1
            out.append(f"</{tag}>")
            continue
        elif ln.startswith("> "):
            out.append(f"<blockquote>{inline(ln[2:])}</blockquote>")
        elif ln.strip() == "---":
            out.append("<hr>")
        elif ln.strip():
            out.append(f"<p>{inline(ln)}</p>")
        i += 1
    return "\n".join(out)


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>3D Model Sources</title>
<meta name="description" content="Every dimension in the SpiroBuddy 3D model with its source and confidence (generated from docs/3D_SOURCES.md).">
<style>
:root{--bg:#f4f6f9;--surface:#fff;--border:#dbe1e8;--text:#13202e;--text-2:#4a5868;--brand:#0b6e8a;--brand-soft:#e3f2f6;--amber:#a15c00;--amber-soft:#fff5e0;--red:#c62828;--red-soft:#fdecec;--radius:12px;--font:"Segoe UI",system-ui,-apple-system,Roboto,Arial,sans-serif;color-scheme:light}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0f151c;--surface:#17202a;--border:#2b3846;--text:#e8eef4;--text-2:#b4c0cc;--brand:#3fb4d4;--brand-soft:#143241;--amber:#f3b443;--amber-soft:#352914;--red:#ff6b6b;--red-soft:#3a1b1d;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0f151c;--surface:#17202a;--border:#2b3846;--text:#e8eef4;--text-2:#b4c0cc;--brand:#3fb4d4;--brand-soft:#143241;--amber:#f3b443;--amber-soft:#352914;--red:#ff6b6b;--red-soft:#3a1b1d;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font);line-height:1.5}
main{max-width:1200px;margin:0 auto;padding:24px 16px 48px}a{color:var(--brand);word-break:break-all}
h1{font-size:1.6rem}h2{font-size:1.2rem;margin-top:2rem}p,li{color:var(--text-2)}
.tw{overflow-x:auto;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius)}
table{border-collapse:collapse;width:100%;font-size:13px}th,td{padding:7px 9px;border-bottom:1px solid var(--border);vertical-align:top;text-align:left}
th{background:var(--brand-soft);position:sticky;top:0}code{background:var(--brand-soft);padding:1px 4px;border-radius:4px}
blockquote{margin:12px 0;padding:10px 14px;background:var(--surface);border-left:4px solid var(--brand);border-radius:8px;color:var(--text-2)}
.flag{font-weight:700;border-radius:6px;padding:0 4px;white-space:nowrap}.flag.d{color:var(--amber);background:var(--amber-soft)}.flag.n{color:var(--red);background:var(--red-soft)}
.top{display:flex;gap:10px;flex-wrap:wrap}.top a{font-weight:600;text-decoration:none;border:1px solid var(--border);background:var(--surface);padding:6px 12px;border-radius:8px;word-break:normal}
</style></head><body><main><div class="top"><a href="./">← 3D showroom</a><a href="videos.html">Videos</a></div>
%BODY%
<p><small>Generated from docs/3D_SOURCES.md by tools/render/make_sources_html.py.</small></p></main></body></html>
"""

if __name__ == "__main__":
    OUT.write_text(PAGE.replace("%BODY%", convert(SRC.read_text(encoding="utf-8"))), encoding="utf-8")
    print(f"wrote {OUT}")
