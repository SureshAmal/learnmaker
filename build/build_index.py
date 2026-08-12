#!/usr/bin/env python3
"""Build the root index.html: the shelf both books sit on.

Run after the two book builders - it reads the stats they leave behind, so the
numbers on the shelf can never drift away from what was actually built.

    python3 build/build_index.py     ->  index.html
"""

from __future__ import annotations

import html
import json
from pathlib import Path

import build as engine

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent

BOOKS = [
    {
        "stats": "stats-llm.json",
        "title": "Large Language Models",
        "sub": "The Hugging Face LLM course",
        "one": "llm-course.html",
        "site": "site/index.html",
        "md": "markdown",
        "dek": "Transformers end to end: pipelines and tokenizers, fine-tuning, datasets, "
               "the classical NLP tasks, then building, sharing and reasoning models. "
               "Every end-of-chapter quiz is playable.",
        "source": "huggingface/course",
        "source_url": "https://github.com/huggingface/course",
        "licence": "Apache 2.0",
        "unit": "sections",
        "extra": "quizzes",
    },
    {
        "stats": "stats-dotnet.json",
        "title": "C# and .NET",
        "sub": "Built from the official Microsoft documentation",
        "one": "dotnet-course.html",
        "site": "site-dotnet/index.html",
        "md": "markdown-dotnet",
        "dek": "The language and the runtime, front to back: the CLI, the type system, "
               "object-oriented and functional C#, generics, LINQ, async, the GC and "
               "memory, then what each recent version added.",
        "source": "dotnet/docs",
        "source_url": "https://github.com/dotnet/docs",
        "licence": "CC BY 4.0",
        "unit": "articles",
        "extra": "code samples",
    },
    {
        "stats": "stats-ml.json",
        "title": "Machine Learning",
        "sub": "A course reader on machine learning",
        "one": "ml-course.html",
        "site": "site-ml/index.html",
        "md": "markdown-ml",
        "dek": "The machine-learning syllabus front to back: the four families of learning "
               "and the pipeline, supervised and unsupervised methods, gradient descent, "
               "clustering and ensembles, then statistical learning theory and model "
               "evaluation. Worked code, with diagrams and math drawn in place.",
        "source": "course notes",
        "source_url": "",
        "licence": "diagrams & math via CDN",
        "unit": "sections",
        "extra": "code samples",
    },
]

EXTRA_CSS = """
.shelf{width:min(760px,calc(100% - 74px));margin:0 auto;padding:0 0 90px}
.shelf-head{padding:96px 0 0;text-align:center}
.shelf-head h1{margin:.42em 0 .3em;font:400 50px/1.1 var(--serif);letter-spacing:-.02em}
.book{display:block;padding:30px 0;border-top:1px solid var(--hair);text-decoration:none;
  color:var(--ink)}
.book:hover .book-title{color:var(--blue)}
.book-num{margin:0;font:700 9.5px/1 var(--mono);letter-spacing:.09em;
  text-transform:uppercase;color:var(--blue)}
.book-title{margin:.42em 0 .12em;font:400 30px/1.16 var(--serif);letter-spacing:-.01em}
.book-sub{margin:0 0 12px;font:700 10px/1.5 var(--mono);letter-spacing:.06em;
  text-transform:uppercase;color:var(--faint)}
.book-dek{margin:0;font:400 16px/1.7 var(--serif);color:var(--muted);max-width:62ch}
.book-figures{display:flex;flex-wrap:wrap;gap:8px 30px;margin:16px 0 0;
  font:700 9.5px/2 var(--mono);letter-spacing:.07em;text-transform:uppercase;color:var(--faint)}
.book-figures b{color:var(--ink);font-weight:700}
.book-more{display:flex;flex-wrap:wrap;gap:9px;margin:16px 0 0}
.book-more a{display:inline-flex;align-items:center;gap:7px;padding:8px 12px;
  border:1px solid var(--hair);background:var(--side);text-decoration:none;color:var(--ink);
  font:700 10px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase}
.book-more a:hover{border-color:var(--blue);color:var(--blue)}
.book-more a.solid{border-color:var(--ink)}
.book-more .src-note{display:inline-flex;align-items:center;gap:7px;padding:8px 12px;
  border:1px dashed var(--hair);color:var(--faint);
  font:700 10px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase}
.shelf-note{margin:46px 0 0;padding-top:22px;border-top:1px solid var(--hair);
  font:400 13.5px/1.75 var(--serif);color:var(--muted)}
.shelf-note .icon{vertical-align:-2px;margin-right:7px}
.shelf-note + .shelf-note{margin-top:14px;padding-top:0;border:0}
@media (max-width:1020px){
  .shelf{width:calc(100% - 40px)}
  .shelf-head h1{font-size:34px}
  .book-title{font-size:25px}
}
"""


def load(name):
    path = HERE / name
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def size_of(rel):
    path = ROOT / rel
    if not path.exists():
        return None
    return f"{path.stat().st_size / 1048576:.1f} MB"


def book_block(index, book):
    stats = load(book["stats"])
    if not stats:
        return ""

    figures = [
        f'<span><b>{stats["chapters"]}</b> chapters</span>',
        f'<span><b>{stats["lessons"]}</b> {book["unit"]}</span>',
        f'<span><b>{stats["words"]:,}</b> words</span>',
    ]
    if book["extra"] == "quizzes" and stats.get("quizzes"):
        figures.append(f'<span><b>{stats["quizzes"]}</b> quiz questions</span>')
    else:
        figures.append(f'<span><b>{stats["code"]:,}</b> code samples</span>')
    size = size_of(book["one"])
    if size:
        figures.append(f'<span><b>{size}</b> one file</span>')

    more = [
        f'<a class="solid" href="{book["one"]}">{engine.icon("book", 13)}'
        f"<span>Read the book</span></a>",
        f'<a href="{book["site"]}">{engine.icon("hash", 13)}<span>Page-per-section</span></a>',
        f'<a href="{book["md"]}">{engine.icon("code", 13)}<span>Markdown</span></a>',
    ]
    if book["source_url"]:
        more.append(
            f'<a href="{book["source_url"]}" target="_blank" rel="noopener">'
            f'{engine.icon("link", 13)}<span>{html.escape(book["source"])} &middot; '
            f'{html.escape(book["licence"])}</span></a>')
    else:
        more.append(
            f'<span class="src-note">{engine.icon("link", 13)}'
            f'<span>{html.escape(book["source"])} &middot; '
            f'{html.escape(book["licence"])}</span></span>')

    return f"""<section class="book">
  <p class="book-num">Book {index}</p>
  <h2 class="book-title">{html.escape(book["title"])}</h2>
  <p class="book-sub">{html.escape(book["sub"])}</p>
  <p class="book-dek">{html.escape(book["dek"])}</p>
  <div class="book-figures">{''.join(figures)}</div>
  <div class="book-more">{''.join(more)}</div>
</section>"""


def build():
    blocks = "".join(book_block(i, book) for i, book in enumerate(BOOKS, start=1))
    page = f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Learn &middot; technical books built from official sources</title>
<meta name="description" content="Three offline-readable technical books built from the
source material of each subject: the Hugging Face LLM course, C# and .NET, and a machine
learning course reader.">
<script>/* set the theme before the first paint, or the page flashes light */
(function(){{var t;try{{t=localStorage.getItem('llmcourse-theme')}}catch(e){{}}
document.documentElement.setAttribute('data-theme',t||(window.matchMedia&&
window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'))}})();</script>
<style>{engine.STYLE.strip()}
{EXTRA_CSS.strip()}</style>
</head>
<body>
<div class="paper" style="margin:0 auto;width:min(960px,100%);border-inline:1px solid var(--line)">
<div class="topbar"><span class="nudge off">{engine.icon("left", 15)}</span>
<span class="nudge off">{engine.icon("right", 15)}</span>
<div class="crumb"><span class="here">Bookshelf</span></div>
<button class="theme" type="button" aria-label="Toggle theme">
<span class="ico-light">{engine.icon("moon", 15)}</span>
<span class="ico-dark">{engine.icon("sun", 15)}</span></button></div>

<div class="shelf">
<header class="shelf-head">
  <p class="meta">THREE BOOKS, BUILT FROM THE SOURCE</p>
  <h1>Learn</h1>
  <p class="dek">Each book is generated from the source material of its subject
  and reads front to back. Every one ships as a single self-contained file with the same
  reading furniture &mdash; search, an Ask panel, light and dark.</p>
  <p class="rule">-----</p>
</header>

{blocks}

<p class="shelf-note">{engine.icon("search", 13)}In either book, <b>Ctrl&nbsp;K</b> searches
every section and <b>Ctrl&nbsp;I</b> opens an Ask panel that answers from that book's own
content, citing the sections it used. The Ask panel needs your own Google Gemini or
Vertex&nbsp;AI credentials; they are kept in your browser and sent only to Google.</p>
<p class="shelf-note">{engine.icon("book", 13)}All text and figures belong to their original
authors and are used under the licence shown for each book. These builds only reorder and
reformat them.</p>
</div>
</div>
<script>
(function(){{
  var root=document.documentElement,btn=document.querySelector('.theme');
  btn.addEventListener('click',function(){{
    var next=root.getAttribute('data-theme')==='dark'?'light':'dark';
    root.setAttribute('data-theme',next);
    try{{localStorage.setItem('llmcourse-theme',next)}}catch(e){{}}
  }});
}})();
</script>
</body>
</html>
"""
    out = ROOT / "index.html"
    out.write_text(page, encoding="utf-8")
    print(f"built the shelf -> {out} ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    build()
