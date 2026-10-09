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
<script>/* same light/dark choice as the nurse site (stored by its moon/sun button) */
try { var t = localStorage.getItem('sb_theme'); if (t === 'dark' || t === 'light') document.documentElement.setAttribute('data-theme', t); } catch (e) {}</script>
<style>
  /* Tokens copied from web/css/styles.css section 1 (one design system). If a value changes there, change it here too. */
  :root {
    --brand: #0b6e8a; --brand-hover: #095a71; --brand-ink: #ffffff; --brand-soft: #e4f1f5; --brand-line: #b5d9e4;
    --bg: #f4f6f8; --surface: #ffffff; --surface-2: #f8fafb; --surface-3: #eef2f5; --border: #e0e5ea; --border-strong: #c3ccd5;
    --text: #101c27; --text-2: #445263; --text-3: #5b6878;
    --red: #c62828; --red-soft: #fdeded; --red-line: #f2c1c1;
    --yellow: #8f5100; --yellow-dot: #e8970f; --yellow-soft: #fff5e1; --yellow-line: #f0d49a;
    --green: #1b7035; --green-dot: #2e9d4e; --green-soft: #e8f5ec; --green-line: #b6dfc2;
    --focus: #1a73e8;
    --font: "Segoe UI", system-ui, -apple-system, Roboto, "Helvetica Neue", Arial, "Nirmala UI", "Noto Sans", "Noto Sans Devanagari", sans-serif;
    --mono: ui-monospace, "Cascadia Mono", Consolas, monospace;
    --fs-xs: .75rem; --fs-sm: .8125rem; --fs-md: .875rem; --fs-base: .9375rem; --fs-lg: 1.0625rem; --fs-xl: 1.25rem; --fs-2xl: 1.5rem;
    --sp-1: 4px; --sp-2: 8px; --sp-3: 12px; --sp-4: 16px; --sp-5: 20px; --sp-6: 24px; --sp-8: 32px; --sp-12: 48px;
    --r-xs: 4px; --r-sm: 6px; --r-md: 8px; --r-lg: 12px; --r-pill: 999px; --radius: var(--r-lg); --radius-sm: var(--r-md);
    --elev-1: 0 1px 2px rgba(16, 28, 39, .05); --elev-2: 0 1px 2px rgba(16, 28, 39, .06), 0 4px 12px rgba(16, 28, 39, .06); --shadow: var(--elev-2);
    --target: 44px; --top-h: 56px;
    color-scheme: light;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --brand: #3fb4d4; --brand-hover: #66c6e0; --brand-ink: #06202a; --brand-soft: #12303d; --brand-line: #1f5266;
      --bg: #0d1319; --surface: #151d26; --surface-2: #1a2430; --surface-3: #202c39; --border: #283544; --border-strong: #3a4a5c;
      --text: #e8eef4; --text-2: #b4c0cc; --text-3: #95a2b0;
      --red: #ff7b7b; --red-soft: #3a1b1e; --red-line: #6b2b30;
      --yellow: #f3b443; --yellow-dot: #f3b443; --yellow-soft: #33280f; --yellow-line: #6a5120;
      --green: #63d083; --green-dot: #4cc06d; --green-soft: #13301d; --green-line: #285c38;
      --focus: #7ab4ff; --elev-1: 0 1px 2px rgba(0, 0, 0, .4); --elev-2: 0 2px 10px rgba(0, 0, 0, .45);
      color-scheme: dark;
    }
  }
  :root[data-theme="dark"] {
    --brand: #3fb4d4; --brand-hover: #66c6e0; --brand-ink: #06202a; --brand-soft: #12303d; --brand-line: #1f5266;
    --bg: #0d1319; --surface: #151d26; --surface-2: #1a2430; --surface-3: #202c39; --border: #283544; --border-strong: #3a4a5c;
    --text: #e8eef4; --text-2: #b4c0cc; --text-3: #95a2b0;
    --red: #ff7b7b; --red-soft: #3a1b1e; --red-line: #6b2b30;
    --yellow: #f3b443; --yellow-dot: #f3b443; --yellow-soft: #33280f; --yellow-line: #6a5120;
    --green: #63d083; --green-dot: #4cc06d; --green-soft: #13301d; --green-line: #285c38;
    --focus: #7ab4ff; --elev-1: 0 1px 2px rgba(0, 0, 0, .4); --elev-2: 0 2px 10px rgba(0, 0, 0, .45);
    color-scheme: dark;
  }
  /* shared base: same type, buttons, chips and focus ring as the nurse site */
  *, *::before, *::after { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--text); font-family: var(--font); font-size: var(--fs-base); line-height: 1.5; -webkit-font-smoothing: antialiased; }
  a { color: var(--brand); text-underline-offset: 2px; }
  a:hover { color: var(--brand-hover); }
  h1, h2, h3 { line-height: 1.2; font-weight: 650; letter-spacing: -.005em; }
  :focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; border-radius: var(--r-xs); }
  svg.i { flex: none; vertical-align: -3px; }
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-lg); box-shadow: var(--shadow); }
  .logo { display: flex; align-items: center; gap: var(--sp-2); font-weight: 750; font-size: 1.1rem; letter-spacing: -.01em; color: var(--text); text-decoration: none; white-space: nowrap; }
  .logo:hover { color: var(--text); }
  .logo svg { width: 30px; height: 30px; flex: none; }
  .here { color: var(--text-2); font-size: var(--fs-md); font-weight: 600; padding-left: var(--sp-3); border-left: 1px solid var(--border); white-space: nowrap; }
  .btn { display: inline-flex; align-items: center; justify-content: center; gap: var(--sp-2); font: inherit; font-size: var(--fs-md); font-weight: 600; line-height: 1.2; border: 1px solid var(--border-strong); background: var(--surface); color: var(--text); border-radius: var(--r-md); padding: 0 var(--sp-3); min-height: 40px; cursor: pointer; text-decoration: none; white-space: nowrap; transition: background 120ms, border-color 120ms; }
  .btn:hover { background: var(--surface-3); color: var(--text); }
  .btn:active { transform: translateY(1px); }
  .btn:disabled { opacity: .55; cursor: not-allowed; }
  .btn.primary { background: var(--brand); border-color: var(--brand); color: var(--brand-ink); }
  .btn.primary:hover { background: var(--brand-hover); border-color: var(--brand-hover); color: var(--brand-ink); }
  .chip { display: inline-flex; align-items: center; gap: 6px; font-size: var(--fs-sm); font-weight: 600; padding: 2px var(--sp-3); min-height: 26px; border-radius: var(--r-pill); background: var(--surface-2); color: var(--text-2); border: 1px dashed var(--border-strong); }
  .spacer { flex: 1; }
  @media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; transition: none !important; } }
  main { max-width: 1200px; margin: 0 auto; padding: var(--sp-5) var(--sp-4) var(--sp-12); }
  main a { word-break: break-all; }
  header { display: flex; align-items: center; gap: var(--sp-3); flex-wrap: wrap; padding-bottom: var(--sp-4); margin-bottom: var(--sp-5); border-bottom: 1px solid var(--border); }
  header nav { display: flex; gap: var(--sp-2); flex-wrap: wrap; }
  header a { word-break: normal; }
  h1 { font-size: var(--fs-2xl); font-weight: 700; margin: 0 0 var(--sp-3); }
  h2 { font-size: var(--fs-lg); margin: var(--sp-8) 0 var(--sp-2); }
  h3 { font-size: var(--fs-base); margin: var(--sp-5) 0 var(--sp-2); }
  p, li { color: var(--text-2); overflow-wrap: anywhere; }
  ol, ul { padding-left: var(--sp-6); }
  p { margin: 0 0 var(--sp-3); }
  hr { border: 0; border-top: 1px solid var(--border); margin: var(--sp-6) 0; }
  .tw { overflow-x: auto; background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-lg); box-shadow: var(--elev-1); margin: var(--sp-3) 0; }
  table { border-collapse: collapse; width: 100%; font-size: var(--fs-sm); }
  th, td { padding: var(--sp-2) var(--sp-3); border-bottom: 1px solid var(--border); vertical-align: top; text-align: left; }
  tbody tr:last-child td { border-bottom: 0; }
  th { background: var(--surface-2); position: sticky; top: 0; font-size: var(--fs-xs); text-transform: uppercase; letter-spacing: .05em; color: var(--text-3); font-weight: 700; white-space: nowrap; }
  code { font-family: var(--mono); font-size: .9em; background: var(--surface-3); padding: 1px 4px; border-radius: var(--r-xs); }
  blockquote { margin: var(--sp-3) 0; padding: var(--sp-3) var(--sp-4); background: var(--brand-soft); border: 1px solid var(--brand-line); border-radius: var(--r-md); color: var(--text); }
  /* flags: the words say what it is; colour only repeats it */
  .flag { font-weight: 700; font-size: .92em; border-radius: var(--r-xs); padding: 0 4px; border: 1px solid transparent; }
  .flag.d { color: var(--yellow); background: var(--yellow-soft); border-color: var(--yellow-line); }
  .flag.n { color: var(--red); background: var(--red-soft); border-color: var(--red-line); }
  small { color: var(--text-3); }
</style></head><body><main>
<header><a class="logo" href="../index.html" title="Back to the SpiroBuddy dashboard"><svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#0b6e8a"/><rect x="9" y="6" width="6" height="20" rx="3" fill="#fff" opacity=".35"/><rect x="9" y="13" width="6" height="13" rx="3" fill="#fff"/><path d="M19 12c3 0 3 4 6 4M19 18c3 0 3 4 6 4" stroke="#7fe0c8" stroke-width="2.2" fill="none" stroke-linecap="round"/></svg><span>SpiroBuddy</span></a><span class="here">3D model sources</span><span class="spacer"></span><nav aria-label="Showroom"><a class="btn" href="./"><svg class="i" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>3D showroom</a><a class="btn" href="videos.html"><svg class="i" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect x="2" y="2" width="20" height="20" rx="2.18"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="17" y1="7" x2="22" y2="7"/></svg>Videos</a></nav></header>
%BODY%
<p><small>Generated from docs/3D_SOURCES.md by tools/render/make_sources_html.py.</small></p></main></body></html>
"""

if __name__ == "__main__":
    OUT.write_text(PAGE.replace("%BODY%", convert(SRC.read_text(encoding="utf-8"))), encoding="utf-8")
    print(f"wrote {OUT}")
