#!/usr/bin/env python3
"""Build the Machine Learning course book from the unit notes in ./ml-course.

Same reading furniture as the other two books (hash routes, Ctrl+K search, the Ask
panel, the outline ruler, light/dark), built by the shared engine in build.py. What is
different here: the source is three hand-written Markdown units, each split into section
pages at its `##` headings, and the pages load two small libraries from a CDN so the
notes can carry real diagrams and math instead of screenshots:

    ```mermaid ... ```   -> a Mermaid diagram or chart (flowcharts, trees, pies, xy)
    $ ... $  /  $$ ... $$ -> KaTeX-rendered math, inline and display

    python3 build/build_ml.py

    site-ml/index.html            contents
    site-ml/unitN/M.html          one page per section
    markdown-ml/unitN/M.md        cleaned Markdown
    ml-course.html                the whole book as one self-contained page (bar the CDNs)
"""

from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path

import ask as ask_panel
import build as engine

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "ml-course"
SITE = ROOT / "site-ml"
MD_OUT = ROOT / "markdown-ml"
SINGLE = ROOT / "ml-course.html"

BOOK_TITLE = "Machine Learning"
UNITS = ["unit-1.md", "unit-2.md", "unit-3.md"]

# ---- CDN libraries: diagrams and charts via Mermaid, math via KaTeX -------------------
KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"

MLX_HEAD = f'<link rel="stylesheet" href="{KATEX}/katex.min.css" crossorigin="anonymous">'

# Diagrams and math re-render after every in-page navigation (the single file swaps the
# article in place) and after a theme switch, so both are driven off a MutationObserver
# rather than a one-shot load handler.
MLX_SCRIPT = f"""
<script defer src="{KATEX}/katex.min.js" crossorigin="anonymous"></script>
<script defer src="{KATEX}/contrib/auto-render.min.js" crossorigin="anonymous"></script>
<script type="module">
import mermaid from '{MERMAID}';
const dark = () => document.documentElement.getAttribute('data-theme') === 'dark';
const mtheme = () => dark() ? 'dark' : 'neutral';
mermaid.initialize({{ startOnLoad: false, theme: mtheme(), securityLevel: 'loose',
  fontFamily: 'inherit', flowchart: {{ curve: 'basis' }} }});
const paper = () => document.querySelector('.paper') || document.body;
function math(el) {{
  if (!window.renderMathInElement) return;
  try {{ renderMathInElement(el, {{ delimiters: [
    {{ left: '$$', right: '$$', display: true }},
    {{ left: '$', right: '$', display: false }},
    {{ left: '\\\\(', right: '\\\\)', display: false }},
    {{ left: '\\\\[', right: '\\\\]', display: true }} ],
    ignoredTags: ['script','noscript','style','textarea','pre','code'],
    throwOnError: false }}); }} catch (e) {{}}
}}
async function diagrams(el) {{
  const nodes = [...el.querySelectorAll('pre.mermaid:not([data-done])')];
  nodes.forEach(n => {{ if (!n.dataset.src) n.dataset.src = n.textContent; }});
  if (!nodes.length) return;
  try {{ await mermaid.run({{ nodes }}); }} catch (e) {{}}
  nodes.forEach(n => n.dataset.done = '1');
}}
let raf = 0;
function renderAll() {{
  cancelAnimationFrame(raf);
  raf = requestAnimationFrame(() => {{ const el = paper(); diagrams(el); math(el); }});
}}
if (document.readyState !== 'loading') renderAll();
window.addEventListener('load', renderAll);
const p = document.querySelector('.paper');
if (p) new MutationObserver(renderAll).observe(p, {{ childList: true }});
new MutationObserver(() => {{
  mermaid.initialize({{ startOnLoad: false, theme: mtheme(), securityLevel: 'loose',
    fontFamily: 'inherit', flowchart: {{ curve: 'basis' }} }});
  paper().querySelectorAll('pre.mermaid[data-done]').forEach(n => {{
    n.removeAttribute('data-done'); n.removeAttribute('data-processed');
    n.innerHTML = ''; n.textContent = n.dataset.src || '';
  }});
  diagrams(paper());
}}).observe(document.documentElement, {{ attributes: true, attributeFilter: ['data-theme'] }});
</script>
"""

ML_CSS = """
/* diagrams and math (Mermaid + KaTeX, loaded from a CDN) */
pre.mermaid{background:none;border:0;padding:0;margin:1.8em 0;text-align:center;
  font:inherit;line-height:normal;overflow-x:auto}
pre.mermaid:not([data-done]){color:var(--faint);font:400 12px/1.6 var(--mono)}
pre.mermaid svg{max-width:100%;height:auto}
.katex{font-size:1.03em}
.katex-display{margin:1.2em 0;overflow-x:auto;overflow-y:hidden;padding:2px 0}
"""


# --------------------------------------------------------------------------------------
# source: three units, each split into section pages at its ## headings
# --------------------------------------------------------------------------------------

FRONT = re.compile(r"\A---\n.*?\n---\n", re.S)
SECTION = re.compile(r"(?m)^##\s+(.+?)\s*$")


def parse_unit(path):
    """Return (unit_title, [(section_title, section_markdown), ...])."""
    raw = FRONT.sub("", path.read_text(encoding="utf-8").replace("\r\n", "\n"))
    m = re.search(r"(?m)^#\s+(.+?)\s*$", raw)
    unit_title = m.group(1).strip() if m else path.stem
    body = raw[m.end():] if m else raw

    parts = SECTION.split(body)          # [preamble, title, body, title, body, ...]
    preamble = parts[0].strip()
    sections = [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]
    if preamble:
        sections.insert(0, ("Overview", preamble))
    return unit_title, sections


DEMOTE = re.compile(r"(?m)^(#{3,6})(\s)")
MERMAID = re.compile(r"^```mermaid[ \t]*\n(.*?)\n```[ \t]*$", re.S | re.M)
# $$...$$ display math, or $...$ inline (no newline, not an escaped \$)
MATH = re.compile(r"\$\$.+?\$\$|(?<![\\$])\$(?!\s)(?:\\.|[^$\\\n])+?\$", re.S)


def render_section(md_text, converter):
    """Section Markdown -> (body_html, [headings], mermaid_count)."""
    # sub-headings inside a section are ### and deeper; lift each one level so they
    # render as the page's own h2/h3 (the section title is the page h1, shown in the head)
    text = DEMOTE.sub(lambda m: "#" * (len(m.group(1)) - 1) + m.group(2), md_text)

    # lift mermaid diagrams and math spans out before the Markdown pass so python-markdown
    # and Pygments leave them alone; both go back in afterwards
    diagrams, maths = [], []

    def keep(store, tag, value):
        store.append(value)
        return f"\x00{tag}{len(store) - 1}\x00"

    text = MERMAID.sub(lambda m: "\n" + keep(diagrams, "M", m.group(1)) + "\n", text)
    # shield real code fences before pulling out math, so a `$` inside a code sample is
    # never mistaken for a math delimiter; the code goes back before the Markdown pass
    text, codeblocks = engine.protect_code(text)
    text = MATH.sub(lambda m: keep(maths, "X", m.group(0)), text)
    text = engine.restore_code(text, codeblocks)

    headings = []

    def heading(m):
        hashes, name, anchor = m.group(1), m.group(2).strip(), m.group(3)
        anchor = anchor or engine.slugify(name)
        if len(hashes) in (2, 3):
            headings.append((len(hashes), re.sub(r"[*`\[\]]", "", name), anchor))
        return f'{hashes} {name} <a class="anchor" href="#{anchor}" id="{anchor}">#</a>'

    text = engine.HEADING.sub(heading, engine.rewrite_alerts(text))
    body_html = engine.render_markdown(text, converter)

    body_html = re.sub(
        r"(?:<p>\s*)?\x00M(\d+)\x00(?:\s*</p>)?",
        lambda m: f'<pre class="mermaid">{html.escape(diagrams[int(m.group(1))])}</pre>',
        body_html)
    body_html = re.sub(r"\x00X(\d+)\x00", lambda m: maths[int(m.group(1))], body_html)
    return engine.new_tab(body_html), headings, len(diagrams)


# --------------------------------------------------------------------------------------
# page templates (the shared furniture, an ML plate, plus the CDN diagram/math libs)
# --------------------------------------------------------------------------------------

def sidebar(chapters, current=None, depth=1, hashed=False):
    up = "../" * depth
    out = [f'<a class="logo" href="{"#" if hashed else up + "index.html"}">ML Course</a>', "<nav>"]
    for title, sections in chapters:
        out.append(f"<section><h2>{html.escape(title)}</h2><ul>")
        for route, section_title, _ in sections:
            href = f"#{route}" if hashed else f"{up}{route}.html"
            extra = f' data-route="{route}"' if hashed else ""
            cls = ' class="active"' if (not hashed and route == current) else ""
            out.append(f'<li><a{cls}{extra} href="{href}">{html.escape(section_title)}</a></li>')
        out.append("</ul></section>")
    out.append("</nav>")
    out.append('<p class="side-note">A course reader on machine learning'
               '<br><span class="mono">diagrams &amp; math via CDN</span></p>')
    return "".join(out)


def topbar(crumb, prev_href, next_href):
    prev_html = (f'<a href="{prev_href}" class="nudge prev" aria-label="Previous section">{engine.icon("left", 15)}</a>'
                 if prev_href else f'<span class="nudge off">{engine.icon("left", 15)}</span>')
    next_html = (f'<a href="{next_href}" class="nudge next" aria-label="Next section">{engine.icon("right", 15)}</a>'
                 if next_href else f'<span class="nudge off">{engine.icon("right", 15)}</span>')
    return (f'<div class="topbar">{prev_html}{next_html}<div class="crumb">{crumb}</div>'
            f'<button class="ask-open" type="button" title="Ask about this book (Ctrl I)"'
            f' aria-label="Ask about this book">{engine.icon("spark", 14)}<kbd>Ask</kbd></button>'
            f'<button class="find" type="button" title="Search the book (Ctrl K)"'
            f' aria-label="Search the book">{engine.icon("search", 14)}<kbd>Ctrl K</kbd></button>'
            f'<button class="theme" type="button" aria-label="Toggle theme">'
            f'<span class="ico-light">{engine.icon("moon", 15)}</span>'
            f'<span class="ico-dark">{engine.icon("sun", 15)}</span></button></div>')


def article(meta):
    toc = ""
    if len(meta["headings"]) > 2:
        items = "".join(f'<li class="lvl{level}"><a href="#{anchor}">{html.escape(name)}</a></li>'
                        for level, name, anchor in meta["headings"])
        toc = (f'<nav class="page-toc"><h2>{engine.icon("hash", 13)}<span>In this section</span></h2>'
               f"<ul>{items}</ul></nav>")
    pager = []
    if meta["prev"]:
        pager.append(f'<a class="prev" href="{meta["prev_href"]}">{engine.icon("left", 14)}'
                     f'<span><em>Previous</em>{html.escape(meta["prev"])}</span></a>')
    if meta["next"]:
        pager.append(f'<a class="next" href="{meta["next_href"]}">'
                     f'<span><em>Next</em>{html.escape(meta["next"])}</span>{engine.icon("right", 14)}</a>')
    head = ('<header class="lesson-head">'
            f'<p class="meta">{html.escape(meta["chapter"].upper())}</p>'
            f'<h1>{html.escape(meta["title"])}</h1>'
            f'<p class="rule">-----</p></header>')
    foot = (f'<footer class="lesson-foot"><div class="pager">{"".join(pager)}</div></footer>')
    return (topbar(meta["crumb"], meta["prev_href"], meta["next_href"])
            + f'<article class="lesson">{head}{toc}{meta["html"]}{foot}</article>')


def cover(chapters, stats, hashed=False):
    cards = []
    for title, sections in chapters:
        links = "".join(f'<li><a href="{"#" + route if hashed else route + ".html"}">'
                        f"{html.escape(section_title)}</a></li>"
                        for route, section_title, _ in sections)
        cards.append(f'<section class="ch"><p class="ch-num">{html.escape(title)}</p>'
                     f'<p class="ch-meta">{len(sections)} sections</p><ol>{links}</ol></section>')
    first = chapters[0][1][0]
    first_href = f"#{first[0]}" if hashed else f"{first[0]}.html"
    return f"""{topbar('<span>Contents</span>', '', first_href)}
<article class="lesson home-body">
<header class="cover">
  <p class="meta">A COURSE READER</p>
  <h1>{BOOK_TITLE}</h1>
  <p class="dek">The machine-learning syllabus read front to back: the four families of
  learning and the pipeline, supervised and unsupervised methods, statistical learning
  theory and ensembles &mdash; with the code, diagrams and math drawn in place.</p>
  <p class="rule">-----</p>
  <p class="start"><a href="{first_href}">Begin with {html.escape(first[1])}
  {engine.icon('right', 14)}</a></p>
</header>
<div class="figures">
  <div class="fig"><b>{stats['chapters']}</b><span>units</span></div>
  <div class="fig"><b>{stats['lessons']}</b><span>sections</span></div>
  <div class="fig"><b>{stats['words']:,}</b><span>words</span></div>
  <div class="fig"><b>{stats['code']}</b><span>code blocks</span></div>
  <div class="fig"><b>{stats['diagrams']}</b><span>diagrams</span></div>
</div>
<h2 class="contents-head">Contents</h2>
<div class="ch-list">{''.join(cards)}</div>
<footer class="lesson-foot"><p class="sources">{engine.icon("book", 13)}A course reader.
Diagrams render with Mermaid and math with KaTeX, both loaded from a CDN.</p></footer>
</article>
"""


def page(title, body, chapters, current=None, depth=1, body_class=""):
    up = "../" * depth
    v = engine.asset_stamp()
    ask_markup = ask_panel.ask_markup(engine.icon, "ml")
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} &middot; {BOOK_TITLE}</title>
<script>/* set the theme before the first paint, or every page flashes light */
(function(){{var t;try{{t=localStorage.getItem('llmcourse-theme')}}catch(e){{}}
document.documentElement.setAttribute('data-theme',t||(window.matchMedia&&
window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'))}})();</script>
<link rel="stylesheet" href="{up}assets/style.css?v={v}">
{MLX_HEAD}
</head>
<body class="{body_class}">
<button class="nav-toggle" type="button" aria-label="Toggle contents">{engine.icon("menu", 18)}</button>
<aside class="sidebar">{sidebar(chapters, current, depth)}</aside>
<div class="paper">{body}</div>
<div class="ruler"><div class="rail" aria-hidden="true"></div><div class="gauge"><div class="ticks" aria-hidden="true"></div><nav class="marks" aria-label="Section outline"></nav><span class="pct">0.00</span></div></div>
<div class="palette" hidden data-base="{up}" data-v="{v}">
  <div class="palette-box" role="dialog" aria-label="Search the book" aria-modal="true">
    <div class="palette-field">{engine.icon("search", 16)}
      <input type="search" placeholder="Search the book" autocomplete="off"
             spellcheck="false" aria-label="Search query">
      <kbd class="esc">Esc</kbd>
    </div>
    <div class="palette-results" role="listbox"></div>
    <div class="palette-foot">
      <span><kbd>&uarr;</kbd><kbd>&darr;</kbd> move</span>
      <span><kbd>{engine.icon("enter", 11)}</kbd> open</span>
      <span class="hits"></span>
    </div>
  </div>
</div>
{ask_markup}
<script src="{up}assets/app.js?v={v}"></script>
{MLX_SCRIPT}
</body>
</html>
"""


def single_file(chapters, routes, home_body, bodies, stats):
    templates = [f'<template data-route="__home">{home_body}</template>']
    for route, body in bodies:
        templates.append(f'<template data-route="{route}">{body}</template>')
    payload = json.dumps(routes, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    ask_markup = ask_panel.ask_markup(engine.icon, "ml")
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{BOOK_TITLE}</title>
<meta name="description" content="A machine-learning course reader as one self-contained
page: {stats['lessons']} sections across {stats['chapters']} units, with diagrams and math.">
<script>/* set the theme before the first paint, or the page flashes light */
(function(){{var t;try{{t=localStorage.getItem('llmcourse-theme')}}catch(e){{}}
document.documentElement.setAttribute('data-theme',t||(window.matchMedia&&
window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'))}})();</script>
<style>{engine.STYLE.strip()}{ML_CSS}</style>
{MLX_HEAD}
</head>
<body>
<button class="nav-toggle" type="button" aria-label="Toggle contents">{engine.icon("menu", 18)}</button>
<aside class="sidebar">{sidebar(chapters, None, 0, hashed=True)}</aside>
<div class="paper"></div>
<div class="ruler"><div class="rail" aria-hidden="true"></div><div class="gauge"><div class="ticks" aria-hidden="true"></div><nav class="marks" aria-label="Section outline"></nav><span class="pct">0.00</span></div></div>
<div class="palette" hidden>
  <div class="palette-box" role="dialog" aria-label="Search the book" aria-modal="true">
    <div class="palette-field">{engine.icon("search", 16)}
      <input type="search" placeholder="Search the book" autocomplete="off"
             spellcheck="false" aria-label="Search query">
      <kbd class="esc">Esc</kbd>
    </div>
    <div class="palette-results" role="listbox"></div>
    <div class="palette-foot">
      <span><kbd>&uarr;</kbd><kbd>&darr;</kbd> move</span>
      <span><kbd>{engine.icon("enter", 11)}</kbd> open</span>
      <span class="hits"></span>
    </div>
  </div>
</div>
{"".join(templates)}
{ask_markup}
<script>window.COURSE_ROUTES = {payload};</script>
<script>{engine.SINGLE_JS.strip()}</script>
{MLX_SCRIPT}
</body>
</html>
"""


# --------------------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------------------

def build():
    units = [parse_unit(SRC / name) for name in UNITS]

    plan = []                          # [(unit_title, [(route, section_title, body_md)])]
    for u, (unit_title, sections) in enumerate(units, start=1):
        rows = [(f"unit{u}/{s}", title, body) for s, (title, body) in enumerate(sections, start=1)]
        plan.append((unit_title, rows))
    chapters = [(t, [(r, st, None) for r, st, _ in rows]) for t, rows in plan]
    flat = [(route, title, body, unit_title)
            for unit_title, rows in plan for route, title, body in rows]

    for out in (SITE, MD_OUT):
        if out.exists():
            shutil.rmtree(out)
    (SITE / "assets").mkdir(parents=True)
    (SITE / "assets" / "style.css").write_text(engine.STYLE.strip() + "\n" + ML_CSS, encoding="utf-8")
    (SITE / "assets" / "app.js").write_text(engine.APP_JS.strip() + "\n", encoding="utf-8")

    converter = engine.make_converter()
    words_total = code_total = diagram_total = 0
    index, bodies = [], []

    for i, (route, title, body_md, unit_title) in enumerate(flat):
        body_html, headings, ndiag = render_section(body_md, converter)
        body_text = engine.plain_text(body_html)
        words = len(re.findall(r"\b[\w'-]+\b", body_text))
        words_total += words
        code_total += body_html.count('class="codeblock')
        diagram_total += ndiag

        (MD_OUT / route).parent.mkdir(parents=True, exist_ok=True)
        (MD_OUT / f"{route}.md").write_text(f"# {title}\n\n{body_md.strip()}\n", encoding="utf-8")

        prev_row = flat[i - 1] if i else None
        next_row = flat[i + 1] if i + 1 < len(flat) else None
        meta = {
            "route": route, "title": title, "chapter": unit_title,
            "html": body_html, "headings": headings, "words": words,
            "crumb": (f'<span>{html.escape(unit_title)}</span><b>/</b>'
                      f'<span class="here">{html.escape(title)}</span>'),
            "prev": prev_row[1] if prev_row else None,
            "next": next_row[1] if next_row else None,
            "prev_href": f"../{prev_row[0]}.html" if prev_row else "",
            "next_href": f"../{next_row[0]}.html" if next_row else "",
        }
        (SITE / route).parent.mkdir(parents=True, exist_ok=True)
        (SITE / f"{route}.html").write_text(page(title, article(meta), chapters, current=route, depth=1),
                                            encoding="utf-8")

        hashed = dict(meta)
        hashed["prev_href"] = f"#{prev_row[0]}" if prev_row else ""
        hashed["next_href"] = f"#{next_row[0]}" if next_row else ""
        bodies.append((route, engine.in_page_anchors(
            re.sub(r'href="\.\./(unit\d+/\d+)\.html', r'href="#\1', article(hashed)), route)))

        index.append({"u": f"{route}.html", "t": title, "c": unit_title,
                      "h": [{"a": a, "t": t} for _, t, a in headings], "b": body_text})

    stats = {"chapters": len(plan), "lessons": len(flat), "words": words_total,
             "code": code_total, "diagrams": diagram_total, "quizzes": 0}

    (SITE / "index.html").write_text(
        page("Contents", cover(chapters, stats), chapters, current=None, depth=0, body_class="home"),
        encoding="utf-8")
    (SITE / "assets" / "search-data.js").write_text(engine.search_index(index), encoding="utf-8")

    routes = [{"u": r, "t": e["t"], "c": e["c"]} for (r, *_), e in zip(flat, index)]
    home = re.sub(r'href="(unit\d+/\d+)\.html"', r'href="#\1"', cover(chapters, stats, hashed=True))
    SINGLE.write_text(single_file(chapters, routes, home, bodies, stats), encoding="utf-8")

    (Path(__file__).resolve().parent / "stats-ml.json").write_text(
        json.dumps({**stats, "chapter_titles": [t for t, _ in plan]}, indent=2), encoding="utf-8")

    print(f"built {len(flat)} sections in {len(plan)} units")
    print(f"  {words_total:,} words | {code_total} code blocks | {diagram_total} diagrams")
    print(f"  html      -> {SITE}")
    print(f"  markdown  -> {MD_OUT}")
    print(f"  one file  -> {SINGLE} ({SINGLE.stat().st_size / 1048576:.2f} MB)")


if __name__ == "__main__":
    build()
