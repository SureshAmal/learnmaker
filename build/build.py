#!/usr/bin/env python3
"""Build a static, offline-readable course site from the Hugging Face LLM course MDX sources.

Source of truth: github.com/huggingface/course -> chapters/en/*.mdx (copied into ./source).
Output:
    site/index.html               course home + full table of contents
    site/chapterN/M.html          one page per lesson
    site/assets/style.css|app.js  shared, self-contained assets
    markdown/chapterN/M.md        cleaned Markdown version of every lesson

Design follows the makingsoftware.com book layout: a paper column on a neutral field,
monospace labels, serif body text, a single blue accent, no emoji anywhere.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
from pathlib import Path

import markdown
import yaml

import ask as ask_panel

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source"
SITE = ROOT / "site"
MD_OUT = ROOT / "markdown"

REPO = "https://github.com/huggingface/course/blob/main/chapters/en"
HF_URL = "https://huggingface.co/learn/llm-course/en"
COMMIT = "5805d51"


# --------------------------------------------------------------------------------------
# icons (inline SVG, stroke-based, 1.6px on a 24 grid)
# --------------------------------------------------------------------------------------

def icon(name, size=16, cls="icon"):
    paths = ICONS[name]
    return (
        f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{paths}</svg>'
    )


ICONS = {
    "left": '<path d="M15 5l-7 7 7 7"/>',
    "right": '<path d="M9 5l7 7-7 7"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2'
           'M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4"/>',
    "moon": '<path d="M20 14.5A8.5 8.5 0 019.5 4a8.5 8.5 0 1010.5 10.5z"/>',
    "copy": '<rect x="9" y="9" width="11" height="11" rx="2"/>'
            '<path d="M5 15V6a2 2 0 012-2h9"/>',
    "check": '<path d="M4 12.5l5.5 5.5L20 6.5"/>',
    "note": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.6v.4"/>',
    "warn": '<path d="M12 4.5L2.9 20h18.2L12 4.5z"/><path d="M12 10v4.5M12 17.4v.3"/>',
    "pencil": '<path d="M4 20h4L20 8l-4-4L4 16v4z"/><path d="M14.5 5.5l4 4"/>',
    "video": '<rect x="2.5" y="5" width="14" height="14" rx="3"/>'
             '<path d="M16.5 10.5l5-3v9l-5-3z"/>',
    "book": '<path d="M4 4.5h6a3 3 0 013 3V20a2.5 2.5 0 00-2.5-2.5H4z"/>'
            '<path d="M20 4.5h-6a3 3 0 00-3 3V20a2.5 2.5 0 012.5-2.5H20z"/>',
    "code": '<path d="M9 7l-5 5 5 5M15 7l5 5-5 5"/>',
    "quiz": '<circle cx="12" cy="12" r="9"/>'
            '<path d="M9.4 9.3a2.7 2.7 0 015.2.9c0 1.8-2.6 2.2-2.6 4M12 17.6v.3"/>',
    "link": '<path d="M10.5 13.5a4 4 0 006 .5l2.5-2.5a4 4 0 00-5.7-5.7L12 7.2"/>'
            '<path d="M13.5 10.5a4 4 0 00-6-.5L5 12.5a4 4 0 005.7 5.7L12 16.8"/>',
    "hash": '<path d="M6 9h13M5 15h13M10.5 4l-2 16M16 4l-2 16"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "trash": '<path d="M4 7h16M9.5 7V5h5v2M6.5 7l1 13h9l1-13"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
    "spark": '<path d="M12 3l1.9 5.4L19.5 10l-5.6 1.6L12 17l-1.9-5.4L4.5 10l5.6-1.6z"/>'
             '<path d="M18.5 15.5l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7z"/>',
    "send": '<path d="M4.5 12h14"/><path d="M12.5 5.5L19 12l-6.5 6.5"/>',
    "gear": '<circle cx="12" cy="12" r="3.2"/><path d="M19.4 15a1.7 1.7 0 00.3 1.9l.1.1a2 2 0 11-2.8 2.8l-.1-.1a1.7 1.7 0 00-2.9 1.2 2 2 0 11-4 0 1.7 1.7 0 00-2.9-1.2l-.1.1a2 2 0 11-2.8-2.8l.1-.1A1.7 1.7 0 003 15a2 2 0 110-4 1.7 1.7 0 001.2-2.9l-.1-.1a2 2 0 112.8-2.8l.1.1A1.7 1.7 0 0010 4.2a2 2 0 114 0 1.7 1.7 0 002.9 1.2l.1-.1a2 2 0 112.8 2.8l-.1.1A1.7 1.7 0 0021 11a2 2 0 110 4z"/>',
    "enter": '<path d="M20 6v6.5a2 2 0 01-2 2H5"/><path d="M8.5 11L5 14.5 8.5 18"/>',
}


# --------------------------------------------------------------------------------------
# emoji removal
# --------------------------------------------------------------------------------------

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF←-⇿⌀-⏿①-➿"
    "⬀-⯿️‍Ⓜ〰]"
)

TRY_MARK = "@@TRYITOUT@@"


def de_emoji(text):
    text = text.replace("\U0001F917 ", "Hugging Face ").replace("\U0001F917", "Hugging Face")
    text = re.sub(r"✏️?\s*", TRY_MARK, text)
    text = EMOJI.sub("", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text


# --------------------------------------------------------------------------------------
# table of contents
# --------------------------------------------------------------------------------------

def load_toc():
    """Return [(chapter_title, [(local, section_title, is_quiz), ...]), ...]."""
    data = yaml.safe_load((SRC / "_toctree.yml").read_text(encoding="utf-8"))
    chapters = []
    for chapter in data:
        sections = []
        for section in chapter.get("sections") or []:
            local = section["local"]
            if not (SRC / f"{local}.mdx").exists():
                continue
            title = de_emoji(section["title"]).replace(TRY_MARK, "").strip()
            sections.append((local, title, "quiz" in section))
        if sections:
            title = de_emoji(chapter["title"]).replace(TRY_MARK, "").strip()
            chapters.append((title, sections))
    return chapters


# --------------------------------------------------------------------------------------
# MDX -> Markdown
# --------------------------------------------------------------------------------------

CODE_FENCE = re.compile(r"^(```+)[^\n]*\n.*?^\1[ \t]*$", re.S | re.M)


def protect_code(text):
    """Replace fenced code blocks with placeholders so rewriting cannot touch them."""
    blocks = []

    def stash(match):
        blocks.append(match.group(0))
        return f"\x00CODE{len(blocks) - 1}\x00"

    return CODE_FENCE.sub(stash, text), blocks


def restore_code(text, blocks):
    for i, block in enumerate(blocks):
        text = text.replace(f"\x00CODE{i}\x00", block)
    return text


def find_balanced(text, start, open_ch, close_ch):
    """Index just past the balanced closer that matches text[start] == open_ch."""
    depth = 0
    in_str = None
    i = start
    while i < len(text):
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == in_str:
                in_str = None
        elif ch in "\"'`":
            in_str = ch
        elif ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


def strip_jsx_tag(text, name):
    """Remove every self-closing <Name ... /> occurrence, however many lines it spans."""
    out = []
    pos = 0
    pattern = re.compile(rf"<{name}\b")
    while True:
        match = pattern.search(text, pos)
        if not match:
            out.append(text[pos:])
            break
        end = text.find("/>", match.end())
        if end == -1:
            out.append(text[pos:])
            break
        scan = match.end()
        while True:
            brace = text.find("{", scan)
            if brace == -1 or brace > end:
                break
            close = find_balanced(text, brace, "{", "}")
            if close == -1:
                break
            scan = close
            if close > end:
                end = text.find("/>", close)
                if end == -1:
                    end = len(text) - 2
        out.append(text[pos:match.start()])
        pos = end + 2
    return "".join(out)


JS_KEY = re.compile(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:)")
JS_TRAILING_COMMA = re.compile(r",(\s*[\]}])")


def quote_keys(literal):
    """Quote bare object keys, skipping anything inside a string value.

    A naive regex would also "fix" `, inputs:` inside an explanation string.
    """
    out = []
    i = 0
    while i < len(literal):
        ch = literal[i]
        if ch == '"':
            end = i + 1
            while end < len(literal):
                if literal[end] == "\\":
                    end += 2
                    continue
                if literal[end] == '"':
                    break
                end += 1
            out.append(literal[i:end + 1])
            i = end + 1
            continue
        match = JS_KEY.match(literal, i)
        if match:
            out.append(f'{match.group(1)}"{match.group(2)}"{match.group(3)}')
            i = match.end()
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def parse_choices(literal):
    """Parse a JSX `[{text: "..", explain: "..", correct: true}, ...]` array."""
    text = quote_keys(literal)
    text = JS_TRAILING_COMMA.sub(r"\1", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def extract_questions(text):
    """Replace <Question choices={[...]} /> with markers; return the parsed data."""
    questions = []
    out = []
    pos = 0
    pattern = re.compile(r"<Question\b")
    while True:
        match = pattern.search(text, pos)
        if not match:
            out.append(text[pos:])
            break
        brace = text.find("{", match.end())
        close = find_balanced(text, brace, "{", "}") if brace != -1 else -1
        end = text.find("/>", close) if close != -1 else -1
        if end == -1:
            out.append(text[pos:match.end()])
            pos = match.end()
            continue
        choices = parse_choices(text[brace + 1:close - 1].strip())
        out.append(text[pos:match.start()])
        if choices:
            out.append(f"\n\n\x01QUIZ{len(questions)}\x01\n\n")
            questions.append(choices)
        pos = end + 2
    return "".join(out), questions


TIP = re.compile(r"<Tip([^>]*)>(.*?)</Tip>", re.S)
TIP_TITLE = re.compile(r'title="([^"]*)"')
YOUTUBE = re.compile(r"<Youtube\s+id=\"([\w-]+)\"\s*/?>")
COMMENT = re.compile(r"<!--.*?-->", re.S)
HEADING = re.compile(r"^(#{1,6})\s*(.+?)\s*(?:\[\[([\w-]+)\]\])?\s*$", re.M)


def rewrite_tips(text):
    def repl(match):
        attrs, body = match.group(1), match.group(2).strip()
        warning = "warning={true}" in attrs
        named = TIP_TITLE.search(attrs)
        label = named.group(1) if named else ("Watch out" if warning else "Note")
        kind = "warn" if warning else "note"
        body = re.sub(r"^", "> ", body, flags=re.M)
        return f"\n\n> \x04{kind}\x04{label}\x04\n>\n{body}\n\n"

    return TIP.sub(repl, text)


ALERT = re.compile(r"^([ \t]*)>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$", re.M)
ALERT_LABEL = {
    "NOTE": ("note", "Note"), "TIP": ("note", "Tip"), "IMPORTANT": ("note", "Important"),
    "WARNING": ("warn", "Watch out"), "CAUTION": ("warn", "Caution"),
}


def rewrite_alerts(text):
    """GitHub alert syntax (`> [!TIP]`) is what the newer chapters use for callouts."""

    def repl(match):
        indent, kind_key = match.group(1), match.group(2)
        kind, label = ALERT_LABEL[kind_key]
        return f"{indent}> \x04{kind}\x04{label}\x04\n{indent}>"

    return ALERT.sub(repl, text)


def rewrite_youtube(text):
    def repl(match):
        vid = match.group(1)
        return (
            f'\n\n<p class="video"><a href="https://www.youtube.com/watch?v={vid}" '
            f'target="_blank" rel="noopener">{icon("video", 15)}'
            f"<span>Companion video &middot; youtu.be/{vid}</span></a></p>\n\n"
        )

    return YOUTUBE.sub(repl, text)


IFRAME = re.compile(r"<iframe\b[^>]*?>(?:\s*</iframe>)?", re.S)
IFRAME_SRC = re.compile(r'src=\s*"([^"]+)"')


def rewrite_iframes(text):
    """The course embeds live Gradio Spaces. Most are asleep or erroring, and each one
    leaves a few hundred pixels of dead frame, so link out instead of embedding."""

    def repl(match):
        src = IFRAME_SRC.search(match.group(0))
        if not src:
            return ""
        url = src.group(1)
        host = re.sub(r"^https?://", "", url).rstrip("/")
        kind = "Interactive quiz" if "quiz" in host or "exam" in host else "Live demo"
        return (
            f'\n\n<p class="demo"><a href="{url}" target="_blank" rel="noopener">'
            f'{icon("code", 15)}<span>{kind} &middot; {html.escape(host)}</span></a></p>\n\n'
        )

    return IFRAME.sub(repl, text)


def rewrite_links(text, known):
    """Point /course/... links at the local pages; keep unbuilt chapters on the web."""
    text = re.sub(r"\(\((/course/[\w/]*)\)\)", r"(\1)", text)  # an upstream typo

    def section(match):
        target = f"chapter{match.group(1)}/{match.group(2)}"
        if target in known:
            return f"(../{target}.html)"
        return f"({HF_URL}/chapter{match.group(1)}/{match.group(2)})"

    def chapter(match):
        target = f"chapter{match.group(1)}/1"
        if target in known:
            return f"(../{target}.html)"
        return f"({HF_URL}/chapter{match.group(1)}/1)"

    text = re.sub(r"\(/course/chapter(\d+)/(\d+)\)", section, text)
    text = re.sub(r"\(/course/chapter(\d+)\)", chapter, text)
    text = re.sub(r"\(/course/?\)", "(../index.html)", text)
    return text


MD_ESCAPE = re.compile(r"\\([\\`*_{}\[\]()#+.!<>|~-])")


def unescape_md(text):
    """Undo the source's own escaping of a title.

    `C\\#` is a Markdown escape, and some headings are written with HTML entities
    (`# dotnet new &lt;TEMPLATE&gt;`). Both have to be plain text here, because the
    page template escapes the title once on the way out.
    """
    return html.unescape(MD_ESCAPE.sub(r"\1", text))


def slugify(title):
    """Match the anchor the docs toolchains generate, including the edge cases.

    `#### Continuations with _into_` has to become `continuations-with-into`, not
    `continuations-with-into-`, or every cross-reference to it dangles.
    """
    slug = re.sub(r"[^\w\s-]", "", title.lower()).strip()
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "section"


def mdx_to_markdown(raw, known=frozenset()):
    """Return (markdown_text, page_title, questions, headings)."""
    text = raw.replace("\r\n", "\n")
    text, blocks = protect_code(text)

    text = COMMENT.sub("", text)
    for tag in ("FrameworkSwitchCourse", "CourseFloatingBanner", "CourseCheckpoint"):
        text = strip_jsx_tag(text, tag)
    text, questions = extract_questions(text)
    text = rewrite_tips(text)
    text = rewrite_alerts(text)
    text = rewrite_youtube(text)
    text = rewrite_iframes(text)
    text = rewrite_links(text, known)
    text = de_emoji(text)

    headings = []
    page_title = None

    def heading(match):
        nonlocal page_title
        hashes, title, anchor = match.group(1), match.group(2), match.group(3)
        title = title.replace(TRY_MARK, "").strip()
        anchor = anchor or slugify(title)
        if len(hashes) == 1 and page_title is None:
            page_title = unescape_md(title)
            return ""  # the page template renders the title itself
        if len(hashes) in (2, 3):
            headings.append((len(hashes), unescape_md(re.sub(r"[*`]", "", title)), anchor))
        return f'{hashes} {title} <a class="anchor" href="#{anchor}" id="{anchor}">#</a>'

    text = HEADING.sub(heading, text)
    text = restore_code(text, blocks)
    # the hugging-face glyph also shows up inside sample strings in code blocks
    text = text.replace("\U0001F917 ", "Hugging Face ").replace("\U0001F917", "Hugging Face")
    text = re.sub(r"\n{4,}", "\n\n\n", text).strip() + "\n"
    return text, page_title, questions, headings


# --------------------------------------------------------------------------------------
# Markdown -> HTML
# --------------------------------------------------------------------------------------

LANG_ALIASES = {
    "python out": "text", "py out": "text", "bash out": "text",
    "out": "text", "python py": "python",
}


def normalize_fences(md_text):
    """```python out is HF's "this is program output" marker; make it a real language."""

    def repl(match):
        fence, info = match.group(1), match.group(2).strip()
        lang = LANG_ALIASES.get(info.lower(), info.split()[0] if info else "")
        return f"{fence}{lang}"

    return re.sub(r"^(```+)([^\n]*)$", repl, md_text, flags=re.M)


def fence_labels(md_text):
    """Record the language shown on each code block's gutter label, in order."""
    labels = []
    open_fence = None
    for line in md_text.split("\n"):
        match = re.match(r"^(```+)([^\n]*)$", line)
        if not match:
            continue
        if open_fence is None:
            open_fence = match.group(1)
            info = match.group(2).strip().lower()
            if info.endswith(" out") or info == "out":
                labels.append("output")
            else:
                lang = info.split()[0] if info else "code"
                labels.append({"py": "python", "js": "javascript", "sh": "bash",
                               "yml": "yaml", "": "code"}.get(lang, lang))
        elif match.group(1).startswith(open_fence):
            open_fence = None
    return labels


def make_converter(tab_length=4):
    return markdown.Markdown(
        extensions=["fenced_code", "codehilite", "tables", "attr_list",
                    "md_in_html", "sane_lists"],
        extension_configs={
            "codehilite": {"guess_lang": False, "css_class": "hl", "linenums": False},
        },
        tab_length=tab_length,
    )


CALLOUT = re.compile(r"<blockquote>\s*<p>\x04(\w+)\x04([^\x04]*)\x04\s*</p>", re.S)


def render_markdown(md_text, converter):
    labels = fence_labels(md_text)
    converter.reset()
    out = converter.convert(normalize_fences(md_text))

    # blockquote-based callouts -> figure-style boxes with an icon
    def callout(match):
        kind, label = match.group(1), match.group(2).strip()
        return (
            f'<blockquote class="callout {kind}"><p class="callout-head">'
            f'{icon("warn" if kind == "warn" else "note", 15)}'
            f"<span>{html.escape(label)}</span></p>"
        )

    out = CALLOUT.sub(callout, out)

    # per-block language label in the code gutter
    counter = {"i": 0}

    def label_pre(match):
        i = counter["i"]
        counter["i"] += 1
        lang = labels[i] if i < len(labels) else "code"
        cls = " output" if lang == "output" else ""
        return f'<div class="codeblock{cls}"><span class="lang">{html.escape(lang)}</span>{match.group(0)}'

    out = re.sub(r"<div class=\"hl\">", label_pre, out)
    out = out.replace("</pre></div>", "</pre></div></div>")

    # "Try it out!" exercises: tag the paragraph, then unwrap the blockquote
    # the course wraps it in, so the exercise reads as its own box.
    out = re.sub(
        rf"<p>\s*{re.escape(TRY_MARK)}\s*",
        lambda m: f'<p class="tryit">{icon("pencil", 15)}<span>',
        out,
    )
    out = re.sub(r'(<p class="tryit">(?:(?!</p>).)*)</p>', r"\1</span></p>", out, flags=re.S)
    out = re.sub(
        r'<blockquote>\s*(<p class="tryit">(?:(?!</blockquote>).)*?)\s*</blockquote>',
        r"\1",
        out,
        flags=re.S,
    )
    out = out.replace(TRY_MARK, "")
    out = re.sub(r"<p>\s*</p>", "", out)
    return new_tab(out)


HREF_ATTR = re.compile(r'href="([^"]+)"')
HF_DOCS = "https://huggingface.co/docs/transformers"
HF_HUB = "https://huggingface.co"
COURSE_SHAPE = re.compile(
    r"^(?:\.\./)?(?:/?course/(?:en/)?)?chapter(\d+)(?:/([\w-]+))?/?(?:\.html)?$"
)


def fix_course_links(markup, known, local="chapter1/1"):
    """Repoint every link in a rendered section.

    Section ids are not all numeric - the course has `chapter6/3b` - so anything that
    pattern-matched on digits missed those and left a relative path that resolves
    against whatever directory the page happens to sit in.
    """

    def repl(match):
        href = match.group(1)
        if re.match(r"^(?:[a-z]+:|//|#|mailto:)", href):
            return match.group(0)
        path, _, anchor = href.partition("#")
        anchor = f"#{anchor}" if anchor else ""

        shape = COURSE_SHAPE.match(path)
        if shape:
            chapter, section = shape.group(1), shape.group(2) or "1"
            route = f"chapter{chapter}/{section}"
            if route in known:
                return f'href="../{route}.html{anchor}"'
            return f'href="{HF_URL}/chapter{chapter}/{section}{anchor}"'

        if path.startswith(("model_doc/", "main_classes/", "internal/", "package_reference/")):
            return f'href="{HF_DOCS}/{path}{anchor}"'
        if path.startswith("hf.co/"):
            return f'href="https://{path}{anchor}"'
        if path.startswith("/course"):
            return f'href="{HF_URL}{anchor}"'
        if re.match(r"^/[\w.-]+/[\w.-]+/?$", path):        # a Hub org/repo path
            return f'href="{HF_HUB}{path}{anchor}"'
        if path.startswith("/"):
            return f'href="{HF_HUB}{path}{anchor}"'
        # a file that lives beside the source of this section
        if re.search(r"\.[a-z0-9]{1,5}$", path):
            folder = local.split("/")[0]
            clean = path.lstrip("./")
            return f'href="{REPO}/{folder}/{clean}{anchor}"'
        return match.group(0)

    return HREF_ATTR.sub(repl, markup)


ANCHOR = re.compile(r"<a\s+([^>]*?)>", re.S)


def new_tab(markup):
    """Send links that leave the book to a new tab, so the reader keeps their place."""

    def repl(match):
        attrs = match.group(1)
        if "target=" in attrs:
            return match.group(0)
        href = re.search(r'href="([^"]*)"', attrs)
        if not href or not re.match(r"^(?:https?:)?//", href.group(1)):
            return match.group(0)
        rel = "" if "rel=" in attrs else ' rel="noopener"'
        return f'<a {attrs.rstrip()} target="_blank"{rel}>'

    return ANCHOR.sub(repl, markup)


def render_quiz(qid, choices):
    correct = [i for i, c in enumerate(choices) if c.get("correct")]
    multi = len(correct) > 1
    kind = "checkbox" if multi else "radio"
    hint = "Select every correct answer" if multi else "Select one answer"
    rows = []
    for i, choice in enumerate(choices):
        rows.append(
            '<label class="choice">'
            f'<input type="{kind}" name="q{qid}" value="{i}" '
            f'data-correct="{str(bool(choice.get("correct"))).lower()}">'
            f'<span class="choice-text">{inline(choice.get("text", ""))}</span>'
            f'<span class="explain">{inline(choice.get("explain", ""))}</span>'
            "</label>"
        )
    return (
        f'<div class="quiz" data-quiz="{qid}">'
        f'<p class="quiz-hint">{icon("quiz", 14)}<span>{hint}</span></p>'
        f'{"".join(rows)}'
        '<div class="quiz-actions"><button type="button" class="btn-check">Check answer'
        '</button><span class="verdict"></span></div></div>'
    )


def inline(text):
    """Minimal inline Markdown for quiz strings: code spans and links."""
    text = de_emoji(text).replace(TRY_MARK, "")
    parts = []
    pos = 0
    for match in re.finditer(r"`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)", text):
        parts.append(html.escape(text[pos:match.start()]))
        if match.group(1):
            parts.append(f"<code>{html.escape(match.group(1))}</code>")
        else:
            href = html.escape(match.group(3), quote=True)
            away = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
            parts.append(f'<a href="{href}"{away}>{html.escape(match.group(2))}</a>')
        pos = match.end()
    parts.append(html.escape(text[pos:]))
    return "".join(parts)


# --------------------------------------------------------------------------------------
# page templates
# --------------------------------------------------------------------------------------

def sidebar(chapters, current=None, depth=1):
    up = "../" * depth
    out = [
        f'<a class="logo" href="{up}index.html">LLM COURSE</a>',
        "<nav>",
    ]
    for title, sections in chapters:
        out.append(f"<section><h2>{html.escape(title)}</h2><ul>")
        for local, section_title, is_quiz in sections:
            cls = ' class="active"' if local == current else ""
            out.append(
                f'<li><a{cls} href="{up}{local}.html">{html.escape(section_title)}</a></li>'
            )
        out.append("</ul></section>")
    out.append("</nav>")
    out.append(
        '<p class="side-note">Built from the official course sources '
        f'<br><span class="mono">huggingface/course @ {COMMIT}</span></p>'
    )
    return "".join(out)


TAG = re.compile(r"<[^>]+>")


def plain_text(body_html):
    """Flatten a rendered lesson to searchable text, keeping code identifiers."""
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", body_html, flags=re.S)
    text = TAG.sub(" ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def search_index(entries, depth_note="assets/search-data.js"):
    """A plain JS file, not JSON: it has to load over file:// where fetch is blocked."""
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</", "<\\/")
    return (
        "// Generated by build/build.py - the Ctrl+K index, loaded on first search.\n"
        f"window.COURSE_INDEX = {payload};\n"
    )


def topbar(crumb, prev_href, next_href, depth=1):
    prev_html = (
        f'<a href="{prev_href}" class="nudge prev" aria-label="Previous section">{icon("left", 15)}</a>'
        if prev_href else f'<span class="nudge off">{icon("left", 15)}</span>'
    )
    next_html = (
        f'<a href="{next_href}" class="nudge next" aria-label="Next section">{icon("right", 15)}</a>'
        if next_href else f'<span class="nudge off">{icon("right", 15)}</span>'
    )
    return (
        f'<div class="topbar">{prev_html}{next_html}'
        f'<div class="crumb">{crumb}</div>'
        f'<button class="ask-open" type="button" title="Ask about this book (Ctrl I)"'
        f' aria-label="Ask about this book">{icon("spark", 14)}<kbd>Ask</kbd></button>'
        f'<button class="find" type="button" title="Search the course (Ctrl K)"'
        f' aria-label="Search the course">'
        f'{icon("search", 14)}<kbd>Ctrl K</kbd></button>'
        f'<button class="theme" type="button" aria-label="Toggle theme">'
        f'<span class="ico-light">{icon("moon", 15)}</span>'
        f'<span class="ico-dark">{icon("sun", 15)}</span></button></div>'
    )


def asset_stamp():
    """Hash of the shared assets, so a browser never serves a stale stylesheet."""
    blob = (STYLE + APP_JS).encode("utf-8")
    return hashlib.sha1(blob).hexdigest()[:8]


def page(title, body, chapters, current=None, depth=1, body_class=""):
    up = "../" * depth
    v = asset_stamp()
    ask_markup = ask_panel.ask_markup(icon, "llm")
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} &middot; Hugging Face LLM Course</title>
<script>/* set the theme before the first paint, or every page flashes light */
(function(){{var t;try{{t=localStorage.getItem('llmcourse-theme')}}catch(e){{}}
document.documentElement.setAttribute('data-theme',t||(window.matchMedia&&
window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'))}})();</script>
<link rel="stylesheet" href="{up}assets/style.css?v={v}">
</head>
<body class="{body_class}">
<button class="nav-toggle" type="button" aria-label="Toggle contents">{icon("menu", 18)}</button>
<aside class="sidebar">{sidebar(chapters, current, depth)}</aside>
<div class="paper">{body}</div>
<div class="ruler"><div class="rail" aria-hidden="true"></div><div class="gauge"><div class="ticks" aria-hidden="true"></div><nav class="marks" aria-label="Section outline"></nav><span class="pct">0.00</span></div></div>
<div class="palette" hidden data-base="{up}" data-v="{v}">
  <div class="palette-box" role="dialog" aria-label="Search the course" aria-modal="true">
    <div class="palette-field">{icon("search", 16)}
      <input type="search" placeholder="Search the course" autocomplete="off"
             spellcheck="false" aria-label="Search query">
      <kbd class="esc">Esc</kbd>
    </div>
    <div class="palette-results" role="listbox"></div>
    <div class="palette-foot">
      <span><kbd>&uarr;</kbd><kbd>&darr;</kbd> move</span>
      <span><kbd>{icon("enter", 11)}</kbd> open</span>
      <span class="hits"></span>
    </div>
  </div>
</div>
{ask_markup}
<script src="{up}assets/app.js?v={v}"></script>
</body>
</html>
"""


def lesson_inner(meta):
    local = meta["local"]
    chapter_no, section_no = local.split("/")
    prev_href = f'../{meta["prev"][0]}.html' if meta["prev"] else ""
    next_href = f'../{meta["next"][0]}.html' if meta["next"] else ""

    crumb = (
        f'<span>{html.escape(meta["chapter_title"])}</span>'
        f'<b>/</b><span class="here">{html.escape(meta["title"])}</span>'
    )

    toc = ""
    if len(meta["headings"]) > 2:
        items = "".join(
            f'<li class="lvl{level}"><a href="#{anchor}">{html.escape(title)}</a></li>'
            for level, title, anchor in meta["headings"]
        )
        toc = (
            f'<nav class="page-toc"><h2>{icon("hash", 13)}<span>In this section</span></h2>'
            f"<ul>{items}</ul></nav>"
        )

    pager = []
    if meta["prev"]:
        pager.append(
            f'<a class="prev" href="{prev_href}">{icon("left", 14)}'
            f'<span><em>Previous</em>{html.escape(meta["prev"][1])}</span></a>'
        )
    if meta["next"]:
        pager.append(
            f'<a class="next" href="{next_href}">'
            f'<span><em>Next</em>{html.escape(meta["next"][1])}</span>{icon("right", 14)}</a>'
        )

    head = (
        '<header class="lesson-head">'
        f'<p class="meta">CHAPTER {chapter_no.replace("chapter", "")}'
        f", SECTION {section_no}</p>"
        f'<h1>{html.escape(meta["title"])}</h1>'
        f'<p class="dek">{html.escape(meta["chapter_title"])}, section '
        f'{section_no}</p><p class="rule">-----</p></header>'
    )
    foot = (
        '<footer class="lesson-foot">'
        f'<div class="pager">{"".join(pager)}</div>'
        f'<p class="sources">{icon("link", 13)}'
        f'<a href="{HF_URL}/{chapter_no}/{section_no}" target="_blank" rel="noopener">'
        "Read this section on huggingface.co</a></p></footer>"
    )
    return (
        topbar(crumb, prev_href, next_href)
        + f'<article class="lesson">{head}{toc}{meta["html"]}{foot}</article>'
    )


def lesson_page(meta, chapters):
    return page(meta["title"], lesson_inner(meta), chapters,
                current=meta["local"], depth=1)


def index_page(chapters, stats):
    return page("Contents", index_inner(chapters, stats), chapters,
                current=None, depth=0, body_class="home")


def index_inner(chapters, stats):
    cards = []
    for title, sections in chapters:
        number, _, name = title.partition(". ")
        links = "".join(
            f'<li><a href="{local}.html">{html.escape(section_title)}</a></li>'
            for local, section_title, _ in sections
        )
        cards.append(
            f'<section class="ch"><p class="ch-num">Chapter {html.escape(number)}</p>'
            f"<h3>{html.escape(name)}</h3>"
            f'<p class="ch-meta">{len(sections)} sections</p>'
            f"<ol>{links}</ol></section>"
        )
    first_local, first_title = chapters[0][1][0][0], chapters[0][1][0][1]

    body = f"""{topbar('<span>Contents</span>', '', first_local + '.html')}
<article class="lesson home-body">
<header class="cover">
  <p class="meta">A BOOK BUILD OF THE OFFICIAL COURSE</p>
  <h1>Large Language Models</h1>
  <p class="dek">The complete Hugging Face LLM course, rebuilt from its Markdown sources
  as {stats['lessons']} standalone pages: full prose, every code block, every quiz.</p>
  <p class="rule">-----</p>
  <p class="start"><a href="{first_local}.html">Begin with {html.escape(first_title)}
  {icon('right', 14)}</a></p>
</header>

<div class="figures">
  <div class="fig"><b>{stats['chapters']}</b><span>chapters</span></div>
  <div class="fig"><b>{stats['lessons']}</b><span>sections</span></div>
  <div class="fig"><b>{stats['words']:,}</b><span>words</span></div>
  <div class="fig"><b>{stats['code']:,}</b><span>code blocks</span></div>
  <div class="fig"><b>{stats['quizzes']}</b><span>quiz questions</span></div>
</div>

<h2 class="contents-head">Contents</h2>
<div class="ch-list">{''.join(cards)}</div>

<footer class="lesson-foot">
<p class="sources">{icon("book", 13)}Text and figures come unchanged from
<a href="https://github.com/huggingface/course" target="_blank" rel="noopener">huggingface/course</a>
at commit <code>{COMMIT}</code>, released under Apache&nbsp;2.0. This build only reformats them.</p>
</footer>
</article>
"""
    return new_tab(body)


# --------------------------------------------------------------------------------------
# assets
# --------------------------------------------------------------------------------------

STYLE = r"""
/* cross-document navigation crossfades instead of flashing white */
@view-transition{navigation:auto}
::view-transition-old(root),::view-transition-new(root){animation-duration:.16s}
/* the chrome is identical on every page, so hold it still through the transition */
.sidebar{view-transition-name:nav}
.ruler{view-transition-name:gutter}
::view-transition-old(nav),::view-transition-new(nav),
::view-transition-old(gutter),::view-transition-new(gutter){animation:none;opacity:1}
@media (prefers-reduced-motion:reduce){@view-transition{navigation:none}}

:root{
  color-scheme:light;
  --blue:#2457ff;
  --ink:#252525;
  --muted:#6c6c6c;
  --faint:#8f8f8f;
  --line:#dedede;
  --hair:#ececec;
  --paper:#fff;
  --outside:#f4f4f3;
  --side:#f7f7f7;
  --sink:#f0f0f0;
  --ok:#0a7d42;
  --bad:#c0392b;
  --thumb:#c2c2c6;
  --thumb-hot:#9a9aa0;
  --mono:ui-monospace,"SFMono-Regular",Menlo,Monaco,Consolas,monospace;
  --serif:Georgia,"Iowan Old Style","Times New Roman",serif;
  --sidebar:306px;
  --askw:0px;
  --reserve:0px;
}
/* The Ask panel is docked, so the page column shrinks instead of being covered.
   --reserve keeps a 58px lane for the outline ruler between text and panel, so the
   ruler never lands on the text and swallow clicks or wheel events. */
html.with-ask{--askw:420px;--reserve:478px}
@media (max-width:1100px){html.with-ask{--askw:0px;--reserve:0px}}
html[data-theme=dark]{
  color-scheme:dark;
  --blue:#7fa1ff;
  --ink:#e4e4e6;
  --muted:#a2a2a8;
  --faint:#7d7d85;
  --line:#33333a;
  --hair:#2a2a30;
  --paper:#16161a;
  --outside:#0f0f12;
  --side:#131317;
  --sink:#1d1d22;
  --ok:#57c98a;
  --bad:#ef8b7f;
  --thumb:#3a3a44;
  --thumb-hot:#52525e;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;background:var(--outside)}
/* one scrollbar treatment for the page and for every panel inside it */
*{scrollbar-width:thin;scrollbar-color:var(--thumb) transparent}
body{margin:0;background:var(--outside);color:var(--ink);
  font-family:var(--serif);line-height:1.72;overflow-x:clip}
a{color:var(--blue);text-underline-offset:3px}
img,svg,video{display:block;max-width:100%;height:auto}
.icon{display:inline-block;vertical-align:-2px;flex:none}
code{font-family:var(--mono);font-size:.86em;background:var(--sink);
  padding:.08em .28em;border-radius:2px;overflow-wrap:break-word}
::-webkit-scrollbar{width:8px;height:8px}
/* styling the scrollbar re-enables the classic arrow buttons */
::-webkit-scrollbar-button{display:none;width:0;height:0}
::-webkit-scrollbar-corner{background:transparent}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--thumb);border:2px solid transparent;
  background-clip:padding-box;border-radius:999px}
::-webkit-scrollbar-thumb:hover{background:var(--thumb-hot);background-clip:padding-box}

/* ---------------- sidebar ---------------- */
.sidebar{
  position:fixed;inset:0 auto 0 0;width:var(--sidebar);overflow-y:auto;
  background:var(--side);border-right:1px solid var(--line);padding:40px 23px 70px;z-index:30
}
.logo{display:block;margin:0 0 34px;color:var(--blue);font:700 14px/1 var(--mono);
  letter-spacing:.08em;text-decoration:none}
.sidebar h2{margin:0 0 10px;font:700 11px/1.45 var(--mono);letter-spacing:.045em;
  text-transform:uppercase;color:var(--ink)}
.sidebar section{margin:0 0 25px}
.sidebar ul{margin:0;padding:0 0 0 16px}
.sidebar li{padding:2.5px 0;font:400 13px/1.5 var(--serif)}
.sidebar li::marker{color:var(--faint)}
.sidebar a{color:var(--ink);text-decoration:none}
.sidebar a:hover{color:var(--blue)}
.sidebar a.active{color:var(--blue);font-weight:700}
.side-note{margin:34px 0 0;padding-top:16px;border-top:1px solid var(--line);
  font:400 11.5px/1.6 var(--serif);color:var(--faint)}
.side-note .mono{font:400 10.5px/1.6 var(--mono)}
.nav-toggle{display:none}

/* ---------------- paper ---------------- */
.paper{
  width:min(960px,calc(100vw - 370px - var(--reserve)));
  min-height:100vh;
  margin-left:calc(var(--sidebar) + max(55px,(100vw - var(--sidebar) - var(--reserve) - 960px)/2));
  background:var(--paper);
  border-inline:1px solid var(--line)
}
.topbar{
  position:sticky;top:0;z-index:15;height:52px;display:flex;align-items:center;gap:6px;
  padding:0 18px;background:color-mix(in srgb,var(--paper) 95%,transparent);
  backdrop-filter:blur(8px);border-bottom:1px solid var(--hair);
  font:700 9px/1 var(--mono);text-transform:uppercase;letter-spacing:.065em;color:var(--faint)
}
.nudge{display:grid;place-items:center;width:26px;height:26px;border-radius:3px;
  color:var(--muted);text-decoration:none}
.nudge:hover{background:var(--sink);color:var(--blue)}
.nudge.off{opacity:.25}
.crumb{flex:1;min-width:0;margin-left:8px;white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis}
.crumb b{padding:0 8px;color:var(--line);font-weight:400}
.crumb .here{color:var(--ink)}
.theme{display:grid;place-items:center;width:28px;height:28px;padding:0;cursor:pointer;
  border:1px solid var(--hair);border-radius:3px;background:none;color:var(--muted)}
.theme:hover{color:var(--blue);border-color:var(--line)}
html[data-theme=dark] .ico-light,html[data-theme=light] .ico-dark{display:none}
.find{display:flex;align-items:center;gap:7px;height:28px;margin-right:2px;padding:0 6px;
  cursor:pointer;border:0;background:none;color:var(--faint);
  font:700 9px/1 var(--mono);letter-spacing:.07em;text-transform:uppercase}
.find:hover{color:var(--blue)}
.find kbd{font:inherit;letter-spacing:.06em}

/* ---------------- search palette ---------------- */
.palette{position:fixed;inset:0;z-index:60;display:flex;justify-content:center;
  padding:11vh 20px 20px;background:color-mix(in srgb,var(--outside) 76%,transparent);
  backdrop-filter:blur(3px)}
.palette[hidden]{display:none}
.palette-box{display:flex;flex-direction:column;width:min(680px,100%);max-height:74vh;
  background:var(--paper);border:1px solid var(--line);box-shadow:0 24px 70px rgba(0,0,0,.17)}
html[data-theme=dark] .palette-box{box-shadow:0 24px 70px rgba(0,0,0,.5)}
.palette-field{display:flex;align-items:center;gap:11px;padding:14px 16px;
  border-bottom:1px solid var(--hair);color:var(--muted)}
.palette-field input{flex:1;min-width:0;border:0;background:none;color:var(--ink);
  font:400 17px/1.4 var(--serif);outline:none}
.palette-field input::placeholder{color:var(--faint)}
.palette-field input::-webkit-search-cancel-button{display:none}
.esc,.palette-foot kbd{font:700 9px/1 var(--mono);letter-spacing:.05em;color:var(--faint);
  border:1px solid var(--hair);border-radius:2px;padding:4px 5px}
.palette-results{flex:1;overflow-y:auto;padding:6px}
.hit{display:block;padding:9px 11px;text-decoration:none;color:var(--ink);border-radius:2px}
.hit:hover,.hit.on{background:var(--side)}
.hit.on{box-shadow:inset 2px 0 0 var(--blue)}
.hit-where{font:700 9px/1.5 var(--mono);letter-spacing:.08em;text-transform:uppercase;
  color:var(--faint)}
.hit-title{font:400 16px/1.35 var(--serif);margin:1px 0 2px}
.hit-snip{font:400 13px/1.5 var(--serif);color:var(--muted)}
.hit mark{background:color-mix(in srgb,var(--blue) 18%,transparent);color:inherit;
  border-radius:2px;padding:0 1px}
.palette-empty{padding:22px 12px;text-align:center;font:400 14px/1.6 var(--serif);
  color:var(--faint)}
.palette-foot{display:flex;align-items:center;gap:16px;padding:9px 14px;
  border-top:1px solid var(--hair);font:700 9px/1 var(--mono);letter-spacing:.07em;
  text-transform:uppercase;color:var(--faint)}
.palette-foot span{display:flex;align-items:center;gap:5px}
.palette-foot kbd{display:grid;place-items:center}
.palette-foot .hits{margin-left:auto}

.lesson{width:min(700px,calc(100% - 74px));margin:0 auto;padding:0 0 90px}

/* ---------------- lesson head ---------------- */
.lesson-head{padding:62px 0 8px;text-align:center}
.meta{margin:0;font:700 10px/1.5 var(--mono);letter-spacing:.09em;
  text-transform:uppercase;color:var(--muted)}
.lesson-head h1{margin:.5em 0 .32em;font:400 40px/1.14 var(--serif);letter-spacing:-.012em}
.dek{margin:0 auto;max-width:46ch;font:400 16px/1.6 var(--serif);color:var(--muted)}
.rule{margin:34px 0 42px;color:var(--faint);font:400 12px/1 var(--mono);letter-spacing:.18em}

/* ---------------- prose ---------------- */
.lesson p,.lesson li{font-size:17px}
.lesson h2{margin:2.5em 0 .55em;padding-top:.55em;border-top:1px solid var(--hair);
  font:400 26px/1.25 var(--serif);letter-spacing:-.008em}
.lesson h3{margin:2em 0 .4em;font:700 18px/1.35 var(--serif)}
.lesson h4{margin:1.7em 0 .35em;font:700 15px/1.4 var(--mono);letter-spacing:.02em}
.lesson h5,.lesson h6{margin:1.5em 0 .35em;font:700 13px/1.4 var(--mono);
  text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
.anchor{float:right;margin-right:-.9em;color:transparent;text-decoration:none;font:400 15px var(--mono)}
h2:hover .anchor,h3:hover .anchor{color:var(--line)}
.anchor:hover{color:var(--blue)}
.lesson ul,.lesson ol{padding-left:1.35em}
.lesson li{margin:.28em 0}
.lesson li::marker{color:var(--faint)}
hr{border:0;border-top:1px solid var(--hair);margin:2.6em 0}
strong{font-weight:700}

/* ---------------- page toc ---------------- */
.page-toc{margin:0 0 44px;padding:16px 20px;background:var(--side);
  border:1px solid var(--hair)}
.page-toc h2{display:flex;align-items:center;gap:7px;margin:0 0 8px;padding:0;border:0;
  font:700 9.5px/1 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.page-toc ul{margin:0;padding:0;list-style:none}
.page-toc li{margin:.1em 0;font-size:14px}
.page-toc .lvl3{padding-left:15px;font-size:13px;color:var(--muted)}
.page-toc a{color:var(--ink);text-decoration:none}
.page-toc a:hover{color:var(--blue)}

/* ---------------- code ---------------- */
.codeblock{position:relative;margin:1.7em 0;border:1px solid var(--hair);background:var(--side)}
.codeblock .lang{position:absolute;left:0;top:0;padding:4px 9px;
  font:700 9px/1 var(--mono);letter-spacing:.09em;text-transform:uppercase;
  color:var(--faint);background:var(--sink);border-right:1px solid var(--hair);
  border-bottom:1px solid var(--hair)}
.codeblock.output{background:var(--paper)}
.codeblock.output pre{color:var(--muted)}
.codeblock pre{margin:0;padding:34px 16px 15px;overflow-x:auto;
  font:400 13px/1.62 var(--mono);background:none;border:0}
.codeblock pre code{background:none;padding:0;font-size:inherit}
.copy{position:absolute;right:6px;top:5px;display:grid;place-items:center;width:26px;
  height:24px;padding:0;cursor:pointer;border:1px solid transparent;border-radius:3px;
  background:none;color:var(--faint);opacity:0;transition:opacity .12s}
.codeblock:hover .copy,.copy:focus{opacity:1}
.copy:hover{color:var(--blue);border-color:var(--hair);background:var(--paper)}
.copy.done{color:var(--ok);opacity:1}

/* ---------------- callouts / figures ---------------- */
blockquote{margin:1.8em 0;padding:14px 18px;border:1px solid var(--hair);
  border-left:2px solid var(--blue);background:var(--side)}
blockquote p{margin:.5em 0;font-size:15.5px}
blockquote p:first-child{margin-top:0}
blockquote p:last-child{margin-bottom:0}
.callout-head{display:flex;align-items:center;gap:7px;
  font:700 9.5px/1.4 var(--mono)!important;letter-spacing:.09em;text-transform:uppercase;
  color:var(--muted)}
blockquote.warn{border-left-color:var(--bad)}
blockquote.warn .callout-head{color:var(--bad)}
.tryit{padding:12px 16px;border:1px dashed var(--line);background:var(--side);
  display:flex;gap:9px;align-items:flex-start;font-size:15.5px!important}
.tryit .icon{margin-top:4px;color:var(--blue)}
.tryit>span{flex:1}
.tryit strong{font:700 10px/1.9 var(--mono);letter-spacing:.09em;text-transform:uppercase;display:block;color:var(--blue)}
.video a,.demo a{display:inline-flex;align-items:center;gap:8px;padding:9px 13px;
  border:1px solid var(--hair);background:var(--side);text-decoration:none;color:var(--ink);
  font:700 11px/1 var(--mono);letter-spacing:.05em;text-transform:uppercase}
.video a:hover,.demo a:hover{border-color:var(--blue);color:var(--blue)}
.demo a{border-style:dashed}
.flex.justify-center{display:flex;justify-content:center;margin:2em 0}
img{margin:0 auto}
html[data-theme=dark] .dark\:hidden{display:none}
html[data-theme=light] .hidden.dark\:block{display:none}
figure{margin:2em 0}
figcaption{margin-top:9px;text-align:center;font:400 12.5px/1.5 var(--mono);color:var(--faint)}

table{border-collapse:collapse;width:100%;margin:1.9em 0;font-size:14.5px;display:block;
  overflow-x:auto}
th,td{border:1px solid var(--hair);padding:8px 11px;text-align:left;vertical-align:top}
th{background:var(--side);font:700 11px/1.4 var(--mono);letter-spacing:.04em;
  text-transform:uppercase}

/* ---------------- quiz ---------------- */
.quiz{margin:1.2em 0 2.4em;padding:16px 18px;border:1px solid var(--hair);background:var(--side)}
.quiz-hint{display:flex;align-items:center;gap:7px;margin:0 0 10px;
  font:700 9.5px/1 var(--mono)!important;letter-spacing:.09em;text-transform:uppercase;
  color:var(--muted)}
.choice{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;padding:8px 10px;
  border:1px solid transparent;cursor:pointer}
.choice:hover{background:var(--paper)}
.choice input{margin-top:6px;accent-color:var(--blue)}
.choice-text{font-size:15.5px}
.explain{grid-column:2;display:none;padding-left:11px;border-left:1px solid var(--line);
  font-size:13.5px;color:var(--muted)}
.quiz.revealed .explain{display:block}
.quiz.revealed .right{border-color:var(--ok);background:var(--paper)}
.quiz.revealed .wrong-picked{border-color:var(--bad);background:var(--paper)}
.quiz-actions{display:flex;align-items:center;gap:13px;margin-top:12px}
.btn-check{padding:7px 14px;cursor:pointer;border:1px solid var(--line);background:var(--paper);
  color:var(--ink);font:700 10px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase}
.btn-check:hover{border-color:var(--blue);color:var(--blue)}
.verdict{font:700 10px/1 var(--mono);letter-spacing:.07em;text-transform:uppercase}
.verdict.ok{color:var(--ok)}
.verdict.bad{color:var(--bad)}

/* ---------------- footer ---------------- */
.lesson-foot{margin-top:64px;padding-top:26px;border-top:1px solid var(--hair)}
.pager{display:flex;gap:14px;flex-wrap:wrap}
.pager a{flex:1 1 230px;display:flex;gap:10px;align-items:center;padding:13px 15px;
  border:1px solid var(--hair);text-decoration:none;color:var(--ink);background:var(--side)}
.pager a:hover{border-color:var(--blue)}
.pager .next{justify-content:flex-end;text-align:right}
.pager em{display:block;font:700 9px/1.8 var(--mono);letter-spacing:.09em;
  text-transform:uppercase;color:var(--faint);font-style:normal}
.pager span{font:400 15px/1.4 var(--serif)}
/* not a flex row: the inline links inside it would become flex items and column up */
.sources{margin:22px 0 0;font:400 13px/1.7 var(--serif);color:var(--muted)}
.sources .icon{vertical-align:-2px;margin-right:7px}

/* ---------------- ruler ---------------- */
.ruler{position:fixed;right:var(--askw);top:0;bottom:0;width:58px;z-index:12;pointer-events:none;
  transition:width .16s ease,background .16s ease}
/* only the rail and the marks take the pointer, so the paper stays clickable */
.rail{position:absolute;right:0;top:0;bottom:0;width:58px;pointer-events:auto;
  transition:width .16s ease}
.ruler:hover .rail{width:100%}
.ruler:hover{width:min(430px,40vw);
  background:linear-gradient(to left,var(--paper) 62%,transparent)}
/* one coordinate space for the ticks, the section marks and the readout */
.gauge{position:absolute;left:0;right:0;top:96px;bottom:26px}
.pct{position:absolute;right:30px;top:0;transform:translateY(-50%);
  font:700 10px/1 var(--mono);color:var(--blue);letter-spacing:.04em;
  transition:opacity .14s ease}
/* the readout shares its lane with the labels, so yield to them on hover */
.ruler:hover .pct{opacity:0}
.ticks{position:absolute;right:14px;top:0;bottom:0;display:flex;
  flex-direction:column;justify-content:space-between;align-items:flex-end}
.ticks i{display:block;height:1px;width:9px;background:var(--line)}
.ticks i.on{width:16px;background:var(--blue)}
.marks{position:absolute;inset:0;pointer-events:none}
.mark{position:absolute;right:14px;display:flex;align-items:center;gap:10px;
  transform:translateY(-50%);text-decoration:none;pointer-events:auto}
.mark i{display:block;width:22px;height:1px;background:var(--ink);flex:none}
.mark .lbl{font:700 10px/1.4 var(--mono);letter-spacing:.07em;text-transform:uppercase;
  color:var(--ink);white-space:nowrap;opacity:0;transform:translateX(10px);
  transition:opacity .14s ease,transform .14s ease}
.ruler:hover .lbl{opacity:1;transform:none}
.mark.here i{background:var(--blue);width:30px}
.mark.here .lbl{color:var(--blue)}
.mark:hover i{background:var(--blue);width:30px}
.mark:hover .lbl{color:var(--blue)}

/* ---------------- home ---------------- */
.cover{padding:96px 0 0;text-align:center}
.cover h1{margin:.42em 0 .3em;font:400 52px/1.08 var(--serif);letter-spacing:-.02em}
.start a{display:inline-flex;align-items:center;gap:7px;padding:11px 18px;
  border:1px solid var(--ink);text-decoration:none;color:var(--ink);
  font:700 10px/1 var(--mono);letter-spacing:.09em;text-transform:uppercase}
.start a:hover{border-color:var(--blue);color:var(--blue)}
.figures{display:flex;flex-wrap:wrap;gap:26px 42px;justify-content:center;
  padding:34px 0 6px;border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);
  margin:52px 0 0}
.fig{text-align:center;margin-bottom:28px}
.fig b{display:block;font:400 30px/1 var(--serif)}
.fig span{font:700 9.5px/2.2 var(--mono);letter-spacing:.09em;text-transform:uppercase;
  color:var(--muted)}
.contents-head{margin:56px 0 6px!important;border:0!important;padding:0!important;
  font:700 10px/1 var(--mono)!important;letter-spacing:.1em;text-transform:uppercase;
  color:var(--muted)}
.ch{padding:26px 0;border-top:1px solid var(--hair)}
.ch-num{margin:0;font:700 9.5px/1 var(--mono);letter-spacing:.09em;
  text-transform:uppercase;color:var(--blue)}
.ch h3{margin:.4em 0 .1em;font:400 23px/1.25 var(--serif)}
.ch-meta{margin:0 0 10px;font:400 12px/1.5 var(--mono);color:var(--faint)}
.ch ol{margin:0;padding-left:1.5em;columns:2;column-gap:34px}
.ch li{margin:.15em 0;font-size:14.5px;break-inside:avoid}
.ch a{color:var(--ink);text-decoration:none}
.ch a:hover{color:var(--blue)}

/* ---------------- responsive ---------------- */
/* below this the ruler would sit on top of the paper edge */
@media (max-width:1400px){.ruler{display:none}}
/* the ruler sits in the lane --reserve keeps for it, left of the docked panel */
html.with-ask .ruler:hover{width:min(360px,32vw)}
@media (max-width:1020px){
  .nav-toggle{display:grid;place-items:center;position:fixed;left:12px;top:11px;z-index:41;
    width:34px;height:34px;border:1px solid var(--line);border-radius:3px;
    background:var(--paper);color:var(--ink);cursor:pointer}
  .sidebar{transform:translateX(-100%);transition:transform .18s ease;z-index:40;
    width:86vw;max-width:320px;box-shadow:0 0 44px rgba(0,0,0,.16)}
  body.nav-open .sidebar{transform:none}
  body.nav-open .nav-toggle{border-color:transparent;background:transparent}
  .paper{width:100%;margin-left:0;border:0}
  .topbar{padding-left:56px}
  .lesson{width:calc(100% - 40px)}
  .cover h1{font-size:38px}
  .find span,.find kbd{display:none}
  .find{padding:0 7px}
  .palette{padding:8vh 12px 12px}
  .lesson-head h1{font-size:31px}
  .ch ol{columns:1}
}
@media print{
  .sidebar,.topbar,.ruler,.nav-toggle,.pager,.quiz-actions,.copy{display:none}
  .paper{width:100%;margin:0;border:0}
  .quiz .explain{display:block}
}

/* ---------------- syntax highlighting ---------------- */
.hl .c,.hl .c1,.hl .cm,.hl .ch,.hl .cs,.hl .cp{color:#8a8f98;font-style:italic}
.hl .k,.hl .kn,.hl .kd,.hl .kc,.hl .kp,.hl .kr,.hl .ow{color:#8b2fb5}
.hl .kt,.hl .nc,.hl .nn{color:#9a6400}
.hl .s,.hl .s1,.hl .s2,.hl .sb,.hl .sd,.hl .se,.hl .sh,.hl .si,.hl .sx,.hl .sr,
.hl .ss,.hl .sa{color:#1f7a3d}
.hl .m,.hl .mi,.hl .mf,.hl .mh,.hl .mo,.hl .il{color:#9a5a00}
.hl .nb,.hl .bp{color:#0a6f8f}
.hl .nf,.hl .fm{color:#2457ff}
.hl .nd{color:#9a5a00}
.hl .o,.hl .p{color:#5a5a5a}
.hl .err{color:inherit;border:0}
.hl .gd{color:#c0392b}
.hl .gi{color:#0a7d42}
html[data-theme=dark] .hl .c,html[data-theme=dark] .hl .c1,
html[data-theme=dark] .hl .cm,html[data-theme=dark] .hl .cp{color:#71717d}
html[data-theme=dark] .hl .k,html[data-theme=dark] .hl .kn,html[data-theme=dark] .hl .kd,
html[data-theme=dark] .hl .kc,html[data-theme=dark] .hl .kp,html[data-theme=dark] .hl .kr,
html[data-theme=dark] .hl .ow{color:#c78ce6}
html[data-theme=dark] .hl .s,html[data-theme=dark] .hl .s1,html[data-theme=dark] .hl .s2,
html[data-theme=dark] .hl .sb,html[data-theme=dark] .hl .sd,html[data-theme=dark] .hl .se,
html[data-theme=dark] .hl .sa{color:#8fce9b}
html[data-theme=dark] .hl .m,html[data-theme=dark] .hl .mi,html[data-theme=dark] .hl .mf,
html[data-theme=dark] .hl .mh,html[data-theme=dark] .hl .il,
html[data-theme=dark] .hl .nd{color:#e0a86a}
html[data-theme=dark] .hl .nb,html[data-theme=dark] .hl .bp{color:#63b6cf}
html[data-theme=dark] .hl .nf,html[data-theme=dark] .hl .fm{color:#7fa1ff}
html[data-theme=dark] .hl .kt,html[data-theme=dark] .hl .nc,
html[data-theme=dark] .hl .nn{color:#dcb572}
html[data-theme=dark] .hl .o,html[data-theme=dark] .hl .p{color:#9a9aa4}
"""

APP_JS = r"""
(function () {
  'use strict';

  var root = document.documentElement;

  // ---- theme (the inline head script already picked it; this only toggles) --
  var themeBtn = document.querySelector('.theme');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('llmcourse-theme', next); } catch (e) {}
    });
  }

  // ---- contents drawer -----------------------------------------------------
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () { document.body.classList.toggle('nav-open'); });
  }
  document.addEventListener('click', function (ev) {
    if (!document.body.classList.contains('nav-open')) return;
    if (ev.target.closest('.sidebar') || ev.target.closest('.nav-toggle')) return;
    document.body.classList.remove('nav-open');
  });
  var active = document.querySelector('.sidebar a.active');
  if (active) active.scrollIntoView({ block: 'center' });

  // ---- copy buttons --------------------------------------------------------
  var COPY = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 012-2h9"/></svg>';
  var DONE = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5.5 5.5L20 6.5"/></svg>';

  Array.prototype.forEach.call(document.querySelectorAll('.codeblock'), function (block) {
    var pre = block.querySelector('pre');
    if (!pre) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy';
    btn.title = 'Copy code';
    btn.setAttribute('aria-label', 'Copy code');
    btn.innerHTML = COPY;
    block.appendChild(btn);
    btn.addEventListener('click', function () {
      var text = pre.innerText;
      var done = function () {
        btn.innerHTML = DONE;
        btn.classList.add('done');
        setTimeout(function () { btn.innerHTML = COPY; btn.classList.remove('done'); }, 1300);
      };
      if (navigator.clipboard) { navigator.clipboard.writeText(text).then(done, done); return; }
      var ta = document.createElement('textarea');
      ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); } catch (e) {}
      document.body.removeChild(ta); done();
    });
  });

  // ---- quizzes -------------------------------------------------------------
  Array.prototype.forEach.call(document.querySelectorAll('.quiz'), function (quiz) {
    var btn = quiz.querySelector('.btn-check');
    var verdict = quiz.querySelector('.verdict');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var picked = 0, wrong = 0, missed = 0;
      Array.prototype.forEach.call(quiz.querySelectorAll('.choice'), function (choice) {
        var input = choice.querySelector('input');
        var isCorrect = input.getAttribute('data-correct') === 'true';
        choice.classList.remove('right', 'wrong-picked');
        if (isCorrect) choice.classList.add('right');
        if (input.checked) {
          picked++;
          if (!isCorrect) { wrong++; choice.classList.add('wrong-picked'); }
        } else if (isCorrect) { missed++; }
      });
      quiz.classList.add('revealed');
      if (!picked) { verdict.textContent = 'Pick an answer'; verdict.className = 'verdict bad'; return; }
      if (!wrong && !missed) { verdict.textContent = 'Correct'; verdict.className = 'verdict ok'; }
      else { verdict.textContent = 'Not quite'; verdict.className = 'verdict bad'; }
    });
  });

  // ---- reading ruler: progress ticks plus a hover outline of the sections ---
  var ruler = document.querySelector('.ruler');
  if (ruler) {
    var ticks = ruler.querySelector('.ticks');
    var lane = ruler.querySelector('.marks');
    var pct = ruler.querySelector('.pct');

    var COUNT = 46, bars = [];
    for (var i = 0; i < COUNT; i++) {
      var tick = document.createElement('i');
      ticks.appendChild(tick);
      bars.push(tick);
    }

    // one labelled mark per top-level section, parked at its place in the page
    var heads = [].slice.call(document.querySelectorAll('.lesson h2[id], .lesson h2 > a.anchor'));
    var seen = {}, marks = [];
    heads.forEach(function (node) {
      var head = node.tagName === 'A' ? node.parentNode : node;
      var anchor = node.id || (head.querySelector('a.anchor') || {}).id;
      if (!anchor || seen[anchor]) return;
      seen[anchor] = 1;
      var label = head.textContent.replace(/#\s*$/, '').trim();
      var mark = document.createElement('a');
      mark.className = 'mark';
      mark.href = '#' + anchor;
      mark.innerHTML = '<span class="lbl"></span><i></i>';
      mark.querySelector('.lbl').textContent = label;
      lane.appendChild(mark);
      marks.push({ el: mark, head: head });
    });

    // Sections that sit close together in the page would stack their labels on top of
    // each other, so nudge them apart: push down, then push the tail back up.
    var place = function () {
      var docH = document.documentElement.scrollHeight;
      var laneH = lane.clientHeight;
      if (!laneH || !marks.length) return;
      var GAP = 17;
      var items = marks.map(function (m) {
        var top = m.head.getBoundingClientRect().top + window.scrollY;
        return { m: m, y: Math.max(0, Math.min(laneH, (top / docH) * laneH)) };
      });
      items.sort(function (a, b) { return a.y - b.y; });
      for (var i = 1; i < items.length; i++) {
        if (items[i].y - items[i - 1].y < GAP) items[i].y = items[i - 1].y + GAP;
      }
      var lastItem = items[items.length - 1];
      if (lastItem.y > laneH) lastItem.y = laneH;
      for (var j = items.length - 1; j > 0; j--) {
        if (items[j].y - items[j - 1].y < GAP) items[j - 1].y = items[j].y - GAP;
      }
      items.forEach(function (it) { it.m.el.style.top = Math.max(0, it.y) + 'px'; });
    };

    var last = -1, current = null;
    var update = function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var ratio = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      pct.textContent = (ratio * 100).toFixed(2);
      pct.style.top = (ratio * 100) + '%';
      var idx = Math.round(ratio * (COUNT - 1));
      if (idx !== last) {
        if (last >= 0) bars[last].classList.remove('on');
        bars[idx].classList.add('on');
        last = idx;
      }
      var here = null, edge = window.innerHeight * 0.28;
      marks.forEach(function (m) {
        if (m.head.getBoundingClientRect().top <= edge) here = m;
      });
      if (here !== current) {
        if (current) current.el.classList.remove('here');
        if (here) here.el.classList.add('here');
        current = here;
      }
    };

    place();
    update();
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', function () { place(); update(); });
    window.addEventListener('load', function () { place(); update(); });
    // images settle late and shift every offset with them
    setTimeout(function () { place(); update(); }, 900);
  }

  // ---- Ctrl+K search -------------------------------------------------------
  var palette = document.querySelector('.palette');
  if (palette) {
    var field = palette.querySelector('input');
    var list = palette.querySelector('.palette-results');
    var hits = palette.querySelector('.hits');
    var base = palette.getAttribute('data-base') || '';
    var loading = false, index = null, rows = [], cursor = -1;

    var esc = function (s) {
      return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    };
    var terms = function (q) {
      return q.toLowerCase().split(/[^a-z0-9_.+#]+/).filter(function (t) { return t.length > 1; });
    };
    var highlight = function (text, ts) {
      var low = text.toLowerCase(), spans = [];
      ts.forEach(function (t) {
        var from = 0, at;
        while ((at = low.indexOf(t, from)) >= 0) { spans.push([at, at + t.length]); from = at + t.length; }
      });
      if (!spans.length) return esc(text);
      spans.sort(function (a, b) { return a[0] - b[0]; });
      var merged = [], cur = spans[0].slice();
      for (var i = 1; i < spans.length; i++) {
        if (spans[i][0] <= cur[1]) cur[1] = Math.max(cur[1], spans[i][1]);
        else { merged.push(cur); cur = spans[i].slice(); }
      }
      merged.push(cur);
      var out = '', pos = 0;
      merged.forEach(function (span) {
        out += esc(text.slice(pos, span[0])) + '<mark>' + esc(text.slice(span[0], span[1])) + '</mark>';
        pos = span[1];
      });
      return out + esc(text.slice(pos));
    };

    // pull a readable window of body text around the first match
    var snippet = function (body, ts) {
      var low = body.toLowerCase(), at = -1;
      for (var i = 0; i < ts.length && at < 0; i++) at = low.indexOf(ts[i]);
      if (at < 0) return body.slice(0, 150) + '...';
      var from = Math.max(0, at - 70), to = Math.min(body.length, at + 130);
      return (from ? '...' : '') + body.slice(from, to).trim() + (to < body.length ? '...' : '');
    };

    var score = function (entry, ts) {
      var title = entry.t.toLowerCase(), chapter = entry.c.toLowerCase();
      var body = entry.b.toLowerCase(), total = 0, hit;
      for (var i = 0; i < ts.length; i++) {
        var t = ts[i], any = 0;
        if (title.indexOf(t) >= 0) { total += 30; any = 1; }
        if (chapter.indexOf(t) >= 0) { total += 6; any = 1; }
        for (var h = 0; h < entry.h.length; h++) {
          if (entry.h[h].t.toLowerCase().indexOf(t) >= 0) { total += 10; any = 1; break; }
        }
        var n = 0, from = 0;
        while ((from = body.indexOf(t, from)) >= 0) { n++; from += t.length; if (n > 12) break; }
        if (n) { total += Math.min(n, 12); any = 1; }
        if (!any) return 0;                       // every term has to appear somewhere
      }
      if (ts.length > 1 && (title + ' ' + body).indexOf(ts.join(' ')) >= 0) total += 25;
      return total;
    };

    var render = function () {
      var q = field.value.trim();
      var ts = terms(q);
      list.innerHTML = '';
      rows = [];
      cursor = -1;
      if (!index) { list.innerHTML = '<p class="palette-empty">Loading the index...</p>'; return; }
      if (!ts.length) {
        list.innerHTML = '<p class="palette-empty">Type to search titles, headings and body text.</p>';
        hits.textContent = index.length + ' sections';
        return;
      }
      var found = [];
      index.forEach(function (entry) {
        var s = score(entry, ts);
        if (s > 0) found.push({ e: entry, s: s });
      });
      found.sort(function (a, b) { return b.s - a.s; });
      hits.textContent = found.length + (found.length === 1 ? ' match' : ' matches');
      if (!found.length) {
        list.innerHTML = '<p class="palette-empty">Nothing matches ' + esc(q) + '.</p>';
        return;
      }
      found.slice(0, 30).forEach(function (found_one) {
        var entry = found_one.e;
        // deep-link to the matching heading when one of them matches
        var anchor = '';
        for (var h = 0; h < entry.h.length; h++) {
          var head = entry.h[h].t.toLowerCase();
          if (ts.some(function (t) { return head.indexOf(t) >= 0; })) { anchor = '#' + entry.h[h].a; break; }
        }
        var row = document.createElement('a');
        row.className = 'hit';
        row.href = base + entry.u + anchor;
        row.innerHTML =
          '<div class="hit-where">' + esc(entry.c) + '</div>' +
          '<div class="hit-title">' + highlight(entry.t, ts) + '</div>' +
          '<div class="hit-snip">' + highlight(snippet(entry.b, ts), ts) + '</div>';
        list.appendChild(row);
        rows.push(row);
      });
      move(0);
    };

    var move = function (to) {
      if (!rows.length) return;
      if (cursor >= 0) rows[cursor].classList.remove('on');
      cursor = (to + rows.length) % rows.length;
      rows[cursor].classList.add('on');
      rows[cursor].scrollIntoView({ block: 'nearest' });
    };

    // the index is a plain script, so it also loads from file:// where fetch cannot
    var load = function () {
      if (index || loading) return;
      loading = true;
      var tag = document.createElement('script');
      tag.src = base + 'assets/search-data.js?v=' + (palette.getAttribute('data-v') || '1');
      tag.onload = function () { index = window.COURSE_INDEX || []; render(); };
      tag.onerror = function () {
        list.innerHTML = '<p class="palette-empty">Could not load the search index.</p>';
      };
      document.head.appendChild(tag);
    };

    var open = function () {
      palette.hidden = false;
      document.body.style.overflow = 'hidden';
      field.value = '';
      load();
      render();
      field.focus();
    };
    var close = function () {
      palette.hidden = true;
      document.body.style.overflow = '';
    };

    var findBtn = document.querySelector('.find');
    if (findBtn) findBtn.addEventListener('click', open);
    palette.addEventListener('click', function (ev) {
      if (!ev.target.closest('.palette-box')) close();
    });
    field.addEventListener('input', render);
    field.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowDown') { ev.preventDefault(); move(cursor + 1); }
      else if (ev.key === 'ArrowUp') { ev.preventDefault(); move(cursor - 1); }
      else if (ev.key === 'Enter' && cursor >= 0) { ev.preventDefault(); rows[cursor].click(); }
      else if (ev.key === 'Escape') { ev.preventDefault(); close(); }
    });
    document.addEventListener('keydown', function (ev) {
      if ((ev.ctrlKey || ev.metaKey) && (ev.key === 'k' || ev.key === 'K')) {
        ev.preventDefault();
        palette.hidden ? open() : close();
        return;
      }
      if (ev.key === 'Escape' && !palette.hidden) close();
      if (ev.key === '/' && palette.hidden && !/^(input|textarea|select)$/i.test(ev.target.tagName)) {
        ev.preventDefault();
        open();
      }
    });
  }

  // ---- Ask panel: reuse the search index for retrieval ---------------------
  installAsk({
    getIndex: function (done) {
      if (index) { done(index); return; }
      var tag = document.createElement('script');
      tag.src = base + 'assets/search-data.js?v=' + (palette.getAttribute('data-v') || '1');
      tag.onload = function () { index = window.COURSE_INDEX || []; done(index); };
      document.head.appendChild(tag);
    },
    hrefFor: function (entry) { return base + entry.u; },
    // the section this page is showing, keyed the same way the index is
    currentKey: function () {
      return location.pathname.split('/').slice(-2).join('/');
    }
  });

  // ---- keep the reading position, and [ / ] paging ------------------------
  var key = 'llmcourse-pos:' + location.pathname;
  var saved = null;
  try { saved = sessionStorage.getItem(key); } catch (e) {}
  // jump, never animate: a smooth restore reads as the page sliding on arrival
  if (saved && !location.hash) window.scrollTo({ top: parseInt(saved, 10) || 0, behavior: 'instant' });
  window.addEventListener('beforeunload', function () {
    try { sessionStorage.setItem(key, String(window.scrollY)); } catch (e) {}
  });

  document.addEventListener('keydown', function (ev) {
    if (ev.metaKey || ev.ctrlKey || ev.altKey) return;
    var tag = (ev.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea') return;
    var sel = ev.key === '[' ? '.topbar a.prev' : ev.key === ']' ? '.topbar a.next' : null;
    if (!sel) return;
    var link = document.querySelector(sel);
    if (link) location.href = link.getAttribute('href');
  });
})();
"""


SINGLE_JS = r"""
(function () {
  'use strict';

  var root = document.documentElement;
  var paper = document.querySelector('.paper');
  var palette = document.querySelector('.palette');
  var ruler = document.querySelector('.ruler');
  var routes = window.COURSE_ROUTES || [];
  var order = routes.map(function (r) { return r.u; });

  var tpl = function (route) {
    return document.querySelector('template[data-route="' + route + '"]');
  };

  // ---- router: #chapter2/2 for a section, #chapter2/2--anchor for a heading -
  var parse = function () {
    var raw = decodeURIComponent(location.hash.replace(/^#/, ''));
    if (!raw) return { route: '__home', anchor: '' };
    var cut = raw.indexOf('--');
    if (cut < 0) return { route: raw, anchor: '' };
    return { route: raw.slice(0, cut), anchor: raw.slice(cut + 2) };
  };

  var current = null;

  var paint = function (where) {
    var node = tpl(where.route) || tpl('__home');
    paper.innerHTML = node.innerHTML;
    current = where.route;

    var meta = routes.filter(function (r) { return r.u === where.route; })[0];
    document.title = (meta ? meta.t + ' · ' : '') + 'The Hugging Face LLM Course';

    var links = document.querySelectorAll('.sidebar a[data-route]');
    Array.prototype.forEach.call(links, function (a) {
      var on = a.getAttribute('data-route') === where.route;
      a.classList.toggle('active', on);
      if (on) a.scrollIntoView({ block: 'nearest' });
    });

    enhance();

    if (where.anchor) {
      var target = document.getElementById(where.anchor);
      if (target) {
        target.scrollIntoView();
        return;
      }
    }
    window.scrollTo({ top: 0, behavior: 'instant' });
  };

  var show = function () {
    var where = parse();
    if (where.route === current && where.anchor) {
      var target = document.getElementById(where.anchor);
      if (target) { target.scrollIntoView({ behavior: 'smooth' }); return; }
    }
    // the first render has nothing to cross-fade from, so paint it straight away
    if (current === null || where.route === current || !document.startViewTransition) {
      paint(where);
      return;
    }
    try {
      document.startViewTransition(function () { paint(where); });
    } catch (e) {
      paint(where);
      return;
    }
    // never let a stalled transition hold the content hostage
    setTimeout(function () { if (current !== where.route) paint(where); }, 320);
  };

  window.addEventListener('hashchange', show);

  // ---- per-render enhancers ------------------------------------------------
  var COPY = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 012-2h9"/></svg>';
  var DONE = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5.5 5.5L20 6.5"/></svg>';

  var marks = [], bars = [], lane, ticks, pct, COUNT = 46, lastBar = -1, here = null;

  var buildRuler = function () {
    if (!ruler) return;
    lane = ruler.querySelector('.marks');
    ticks = ruler.querySelector('.ticks');
    pct = ruler.querySelector('.pct');
    if (!bars.length) {
      for (var i = 0; i < COUNT; i++) {
        var bar = document.createElement('i');
        ticks.appendChild(bar);
        bars.push(bar);
      }
    }
    lane.innerHTML = '';
    marks = [];
    here = null;
    var heads = paper.querySelectorAll('.lesson h2 > a.anchor');
    Array.prototype.forEach.call(heads, function (link) {
      var head = link.parentNode;
      var mark = document.createElement('a');
      mark.className = 'mark';
      mark.href = '#' + current + '--' + link.id;
      mark.innerHTML = '<span class="lbl"></span><i></i>';
      mark.querySelector('.lbl').textContent = head.textContent.replace(/#\s*$/, '').trim();
      lane.appendChild(mark);
      marks.push({ el: mark, head: head });
    });
    place();
    track();
  };

  var place = function () {
    if (!lane || !marks.length) return;
    var docH = document.documentElement.scrollHeight;
    var laneH = lane.clientHeight;
    if (!laneH) return;
    var GAP = 17;
    var items = marks.map(function (m) {
      var top = m.head.getBoundingClientRect().top + window.scrollY;
      return { m: m, y: Math.max(0, Math.min(laneH, (top / docH) * laneH)) };
    });
    items.sort(function (a, b) { return a.y - b.y; });
    for (var i = 1; i < items.length; i++) {
      if (items[i].y - items[i - 1].y < GAP) items[i].y = items[i - 1].y + GAP;
    }
    var tail = items[items.length - 1];
    if (tail.y > laneH) tail.y = laneH;
    for (var j = items.length - 1; j > 0; j--) {
      if (items[j].y - items[j - 1].y < GAP) items[j - 1].y = items[j].y - GAP;
    }
    items.forEach(function (it) { it.m.el.style.top = Math.max(0, it.y) + 'px'; });
  };

  var track = function () {
    if (!pct) return;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    var ratio = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
    pct.textContent = (ratio * 100).toFixed(2);
    pct.style.top = (ratio * 100) + '%';
    var idx = Math.round(ratio * (COUNT - 1));
    if (idx !== lastBar) {
      if (lastBar >= 0) bars[lastBar].classList.remove('on');
      bars[idx].classList.add('on');
      lastBar = idx;
    }
    var found = null, edge = window.innerHeight * 0.28;
    marks.forEach(function (m) {
      if (m.head.getBoundingClientRect().top <= edge) found = m;
    });
    if (found !== here) {
      if (here) here.el.classList.remove('here');
      if (found) found.el.classList.add('here');
      here = found;
    }
  };

  var enhance = function () {
    Array.prototype.forEach.call(paper.querySelectorAll('.codeblock'), function (block) {
      if (block.querySelector('.copy')) return;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'copy';
      btn.title = 'Copy code';
      btn.setAttribute('aria-label', 'Copy code');
      btn.innerHTML = COPY;
      block.appendChild(btn);
    });
    buildRuler();
    // images arrive late and move every offset with them
    setTimeout(function () { place(); track(); }, 700);
  };

  window.addEventListener('scroll', track, { passive: true });
  window.addEventListener('resize', function () { place(); track(); });
  window.addEventListener('load', function () { place(); track(); });

  // ---- delegated interactions ----------------------------------------------
  document.addEventListener('click', function (ev) {
    var theme = ev.target.closest('.theme');
    if (theme) {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('llmcourse-theme', next); } catch (e) {}
      return;
    }
    if (ev.target.closest('.find')) { openFind(); return; }

    var copy = ev.target.closest('.copy');
    if (copy) {
      var pre = copy.parentNode.querySelector('pre');
      var text = pre ? pre.innerText : '';
      var done = function () {
        copy.innerHTML = DONE;
        copy.classList.add('done');
        setTimeout(function () { copy.innerHTML = COPY; copy.classList.remove('done'); }, 1300);
      };
      if (navigator.clipboard) { navigator.clipboard.writeText(text).then(done, done); }
      else {
        var ta = document.createElement('textarea');
        ta.value = text; document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); } catch (e) {}
        document.body.removeChild(ta); done();
      }
      return;
    }

    var check = ev.target.closest('.btn-check');
    if (check) {
      var quiz = check.closest('.quiz');
      var verdict = quiz.querySelector('.verdict');
      var picked = 0, wrong = 0, missed = 0;
      Array.prototype.forEach.call(quiz.querySelectorAll('.choice'), function (choice) {
        var input = choice.querySelector('input');
        var right = input.getAttribute('data-correct') === 'true';
        choice.classList.remove('right', 'wrong-picked');
        if (right) choice.classList.add('right');
        if (input.checked) {
          picked++;
          if (!right) { wrong++; choice.classList.add('wrong-picked'); }
        } else if (right) { missed++; }
      });
      quiz.classList.add('revealed');
      if (!picked) { verdict.textContent = 'Pick an answer'; verdict.className = 'verdict bad'; }
      else if (!wrong && !missed) { verdict.textContent = 'Correct'; verdict.className = 'verdict ok'; }
      else { verdict.textContent = 'Not quite'; verdict.className = 'verdict bad'; }
      return;
    }

    if (ev.target.closest('.nav-toggle')) {
      document.body.classList.toggle('nav-open');
      return;
    }
    if (document.body.classList.contains('nav-open') && !ev.target.closest('.sidebar')) {
      document.body.classList.remove('nav-open');
    }
    if (ev.target.closest('.sidebar a')) document.body.classList.remove('nav-open');
  });

  // ---- search over the inline sections -------------------------------------
  var field = palette.querySelector('input');
  var list = palette.querySelector('.palette-results');
  var hits = palette.querySelector('.hits');
  var index = null, rows = [], cursor = -1;

  // the sections are already in the document, so the index costs one text pass
  var buildIndex = function () {
    if (index) return;
    index = routes.map(function (r) {
      var node = tpl(r.u);
      var text = node ? node.content.textContent.replace(/\s+/g, ' ').trim() : '';
      var heads = [];
      if (node) {
        Array.prototype.forEach.call(node.content.querySelectorAll('h2 > a.anchor'), function (a) {
          heads.push({ a: a.id, t: a.parentNode.textContent.replace(/#\s*$/, '').trim() });
        });
      }
      return { u: r.u, t: r.t, c: r.c, h: heads, b: text };
    });
  };

  var esc = function (s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  };
  var terms = function (q) {
    return q.toLowerCase().split(/[^a-z0-9_.+#]+/).filter(function (t) { return t.length > 1; });
  };
  var highlight = function (text, ts) {
    var low = text.toLowerCase(), spans = [];
    ts.forEach(function (t) {
      var from = 0, at;
      while ((at = low.indexOf(t, from)) >= 0) { spans.push([at, at + t.length]); from = at + t.length; }
    });
    if (!spans.length) return esc(text);
    spans.sort(function (a, b) { return a[0] - b[0]; });
    var merged = [], cur = spans[0].slice();
    for (var i = 1; i < spans.length; i++) {
      if (spans[i][0] <= cur[1]) cur[1] = Math.max(cur[1], spans[i][1]);
      else { merged.push(cur); cur = spans[i].slice(); }
    }
    merged.push(cur);
    var out = '', pos = 0;
    merged.forEach(function (span) {
      out += esc(text.slice(pos, span[0])) + '<mark>' + esc(text.slice(span[0], span[1])) + '</mark>';
      pos = span[1];
    });
    return out + esc(text.slice(pos));
  };
  var snippet = function (body, ts) {
    var low = body.toLowerCase(), at = -1;
    for (var i = 0; i < ts.length && at < 0; i++) at = low.indexOf(ts[i]);
    if (at < 0) return body.slice(0, 150) + '...';
    var from = Math.max(0, at - 70), to = Math.min(body.length, at + 130);
    return (from ? '...' : '') + body.slice(from, to).trim() + (to < body.length ? '...' : '');
  };
  var score = function (entry, ts) {
    var title = entry.t.toLowerCase(), chapter = entry.c.toLowerCase();
    var body = entry.b.toLowerCase(), total = 0;
    for (var i = 0; i < ts.length; i++) {
      var t = ts[i], any = 0;
      if (title.indexOf(t) >= 0) { total += 30; any = 1; }
      if (chapter.indexOf(t) >= 0) { total += 6; any = 1; }
      for (var h = 0; h < entry.h.length; h++) {
        if (entry.h[h].t.toLowerCase().indexOf(t) >= 0) { total += 10; any = 1; break; }
      }
      var n = 0, from = 0;
      while ((from = body.indexOf(t, from)) >= 0) { n++; from += t.length; if (n > 12) break; }
      if (n) { total += Math.min(n, 12); any = 1; }
      if (!any) return 0;
    }
    if (ts.length > 1 && (title + ' ' + body).indexOf(ts.join(' ')) >= 0) total += 25;
    return total;
  };

  var move = function (to) {
    if (!rows.length) return;
    if (cursor >= 0) rows[cursor].classList.remove('on');
    cursor = (to + rows.length) % rows.length;
    rows[cursor].classList.add('on');
    rows[cursor].scrollIntoView({ block: 'nearest' });
  };

  var render = function () {
    var q = field.value.trim(), ts = terms(q);
    list.innerHTML = '';
    rows = [];
    cursor = -1;
    if (!ts.length) {
      list.innerHTML = '<p class="palette-empty">Type to search titles, headings and body text.</p>';
      hits.textContent = index.length + ' sections';
      return;
    }
    var found = [];
    index.forEach(function (entry) {
      var s = score(entry, ts);
      if (s > 0) found.push({ e: entry, s: s });
    });
    found.sort(function (a, b) { return b.s - a.s; });
    hits.textContent = found.length + (found.length === 1 ? ' match' : ' matches');
    if (!found.length) {
      list.innerHTML = '<p class="palette-empty">Nothing matches ' + esc(q) + '.</p>';
      return;
    }
    found.slice(0, 30).forEach(function (one) {
      var entry = one.e, anchor = '';
      for (var h = 0; h < entry.h.length; h++) {
        var head = entry.h[h].t.toLowerCase();
        if (ts.some(function (t) { return head.indexOf(t) >= 0; })) { anchor = '--' + entry.h[h].a; break; }
      }
      var row = document.createElement('a');
      row.className = 'hit';
      row.href = '#' + entry.u + anchor;
      row.innerHTML =
        '<div class="hit-where">' + esc(entry.c) + '</div>' +
        '<div class="hit-title">' + highlight(entry.t, ts) + '</div>' +
        '<div class="hit-snip">' + highlight(snippet(entry.b, ts), ts) + '</div>';
      row.addEventListener('click', closeFind);
      list.appendChild(row);
      rows.push(row);
    });
    move(0);
  };

  function openFind() {
    palette.hidden = false;
    document.body.style.overflow = 'hidden';
    field.value = '';
    buildIndex();
    render();
    field.focus();
  }
  function closeFind() {
    palette.hidden = true;
    document.body.style.overflow = '';
  }

  palette.addEventListener('click', function (ev) {
    if (!ev.target.closest('.palette-box')) closeFind();
  });
  field.addEventListener('input', render);
  field.addEventListener('keydown', function (ev) {
    if (ev.key === 'ArrowDown') { ev.preventDefault(); move(cursor + 1); }
    else if (ev.key === 'ArrowUp') { ev.preventDefault(); move(cursor - 1); }
    else if (ev.key === 'Enter' && cursor >= 0) { ev.preventDefault(); rows[cursor].click(); }
    else if (ev.key === 'Escape') { ev.preventDefault(); closeFind(); }
  });

  document.addEventListener('keydown', function (ev) {
    if ((ev.ctrlKey || ev.metaKey) && (ev.key === 'k' || ev.key === 'K')) {
      ev.preventDefault();
      palette.hidden ? openFind() : closeFind();
      return;
    }
    if (ev.key === 'Escape' && !palette.hidden) { closeFind(); return; }
    var typing = /^(input|textarea|select)$/i.test(ev.target.tagName);
    if (ev.key === '/' && palette.hidden && !typing) { ev.preventDefault(); openFind(); return; }
    if (typing || ev.metaKey || ev.ctrlKey || ev.altKey) return;
    if (ev.key === '[' || ev.key === ']') {
      var at = order.indexOf(current);
      var to = ev.key === '[' ? at - 1 : at + 1;
      if (at >= 0 && to >= 0 && to < order.length) location.hash = '#' + order[to];
    }
  });

  installAsk({
    getIndex: function (done) { buildIndex(); done(index); },
    hrefFor: function (entry) { return '#' + entry.u; },
    currentKey: function () { return current; }
  });

  show();
})();
"""


# The Ask panel's stylesheet and script are shared by both layouts and by the other book.
STYLE = STYLE.rstrip() + "\n\n" + ask_panel.ASK_CSS.strip() + "\n"
# The Ask panel's script is shared by both layouts and by the other book.
APP_JS = ask_panel.ASK_JS.strip() + "\n\n" + APP_JS.strip() + "\n"
SINGLE_JS = ask_panel.ASK_JS.strip() + "\n\n" + SINGLE_JS.strip() + "\n"

# --------------------------------------------------------------------------------------
# single-file edition
# --------------------------------------------------------------------------------------

def hashify(markup):
    """Rewrite a page's links for the one-file build, where routes live in the hash."""
    # cross-section links, with and without a heading anchor
    markup = re.sub(r'href="(?:\.\./)?(chapter\d+/[\w-]+)\.html#([\w-]+)"', r'href="#\1--\2"', markup)
    markup = re.sub(r'href="(?:\.\./)?(chapter\d+/[\w-]+)\.html"', r'href="#\1"', markup)
    markup = re.sub(r'href="(?:\.\./)?index\.html"', 'href="#"', markup)
    return markup


def in_page_anchors(markup, local):
    """Same-page `#heading` links have to carry the route with them."""
    return re.sub(
        r'href="#([\w-]+)"',
        lambda m: f'href="#{local}--{m.group(1)}"',
        markup,
    )


def single_page(chapters, routes, home_body, bodies, stats):
    nav = []
    for title, sections in chapters:
        nav.append(f"<section><h2>{html.escape(title)}</h2><ul>")
        for local, section_title, _ in sections:
            nav.append(
                f'<li><a data-route="{local}" href="#{local}">{html.escape(section_title)}</a></li>'
            )
        nav.append("</ul></section>")
    side = (
        '<a class="logo" href="#">LLM COURSE</a><nav>' + "".join(nav) + "</nav>"
        '<p class="side-note">Built from the official course sources '
        f'<br><span class="mono">huggingface/course @ {COMMIT}</span></p>'
    )

    templates = [f'<template data-route="__home">{home_body}</template>']
    for local, body in bodies:
        templates.append(f'<template data-route="{local}">{body}</template>')

    payload = json.dumps(routes, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    ask_markup = ask_panel.ask_markup(icon, "llm")

    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Hugging Face LLM Course</title>
<meta name="description" content="The complete Hugging Face LLM course as a single
self-contained page: {stats['lessons']} sections, {stats['code']} code blocks,
{stats['quizzes']} quiz questions.">
<script>/* set the theme before the first paint, or the page flashes light */
(function(){{var t;try{{t=localStorage.getItem('llmcourse-theme')}}catch(e){{}}
document.documentElement.setAttribute('data-theme',t||(window.matchMedia&&
window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'))}})();</script>
<style>{STYLE.strip()}</style>
</head>
<body>
<button class="nav-toggle" type="button" aria-label="Toggle contents">{icon("menu", 18)}</button>
<aside class="sidebar">{side}</aside>
<div class="paper"></div>
<div class="ruler"><div class="rail" aria-hidden="true"></div><div class="gauge"><div class="ticks" aria-hidden="true"></div><nav class="marks" aria-label="Section outline"></nav><span class="pct">0.00</span></div></div>
<div class="palette" hidden>
  <div class="palette-box" role="dialog" aria-label="Search the course" aria-modal="true">
    <div class="palette-field">{icon("search", 16)}
      <input type="search" placeholder="Search the course" autocomplete="off"
             spellcheck="false" aria-label="Search query">
      <kbd class="esc">Esc</kbd>
    </div>
    <div class="palette-results" role="listbox"></div>
    <div class="palette-foot">
      <span><kbd>&uarr;</kbd><kbd>&darr;</kbd> move</span>
      <span><kbd>{icon("enter", 11)}</kbd> open</span>
      <span class="hits"></span>
    </div>
  </div>
</div>
{"".join(templates)}
{ask_markup}
<script>window.COURSE_ROUTES = {payload};</script>
<script>{SINGLE_JS.strip()}</script>
</body>
</html>
"""


# --------------------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------------------

def build():
    chapters = load_toc()
    flat = [
        (local, title, chapter_title)
        for chapter_title, sections in chapters
        for local, title, _ in sections
    ]
    total = len(flat)
    known = frozenset(local for local, _, _ in flat)

    for path in (SITE, MD_OUT):
        if path.exists():
            shutil.rmtree(path)
    (SITE / "assets").mkdir(parents=True)
    (SITE / "assets" / "style.css").write_text(STYLE.strip() + "\n", encoding="utf-8")
    (SITE / "assets" / "app.js").write_text(APP_JS.strip() + "\n", encoding="utf-8")

    converter = make_converter()
    words_total = code_blocks = quiz_count = 0
    index = []
    bodies = []

    for i, (local, title, chapter_title) in enumerate(flat):
        raw = (SRC / f"{local}.mdx").read_text(encoding="utf-8")
        md_text, mdx_title, questions, headings = mdx_to_markdown(raw, known)
        title = mdx_title or title

        md_path = MD_OUT / f"{local}.md"
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(
            f"<!-- source: {REPO}/{local}.mdx -->\n\n# {title}\n\n"
            + md_text.replace("\x04", " ").replace(TRY_MARK, "Try it out: "),
            encoding="utf-8",
        )

        body_html = render_markdown(md_text, converter)
        for n, choices in enumerate(questions):
            body_html = body_html.replace(
                f"\x01QUIZ{n}\x01", render_quiz(f"{local.replace('/', '-')}-{n}", choices)
            )

        body_html = new_tab(fix_course_links(body_html, known, local))
        body_text = plain_text(body_html)
        words = len(re.findall(r"\b[\w'-]+\b", body_text))
        words_total += words
        index.append({
            "u": f"{local}.html",
            "t": title,
            "c": chapter_title,
            "h": [{"a": anchor, "t": head} for _, head, anchor in headings],
            "b": body_text,
        })
        code_blocks += body_html.count('class="codeblock')
        quiz_count += len(questions)

        html_path = SITE / f"{local}.html"
        html_path.parent.mkdir(parents=True, exist_ok=True)
        lesson_meta = {
            "local": local,
            "title": title,
            "chapter_title": chapter_title,
            "html": body_html,
            "headings": headings,
            "words": words,
            "prev": (flat[i - 1][0], flat[i - 1][1]) if i else None,
            "next": (flat[i + 1][0], flat[i + 1][1]) if i + 1 < total else None,
        }
        html_path.write_text(lesson_page(lesson_meta, chapters), encoding="utf-8")
        bodies.append((local, in_page_anchors(hashify(lesson_inner(lesson_meta)), local)))

    stats = {
        "chapters": len(chapters), "lessons": total, "words": words_total,
        "code": code_blocks, "quizzes": quiz_count,
    }
    (SITE / "index.html").write_text(index_page(chapters, stats), encoding="utf-8")
    (SITE / "assets" / "search-data.js").write_text(search_index(index), encoding="utf-8")

    routes = [{"u": local, "t": entry["t"], "c": entry["c"]}
              for local, entry in zip((b[0] for b in bodies), index)]
    single = single_page(
        chapters, routes, hashify(index_inner(chapters, stats)), bodies, stats
    )
    single_path = ROOT / "llm-course.html"
    single_path.write_text(single, encoding="utf-8")

    (Path(__file__).resolve().parent / "stats-llm.json").write_text(
        json.dumps({**stats, "chapter_titles": [t for t, _ in chapters]}, indent=2),
        encoding="utf-8",
    )
    print(f"built {total} sections in {len(chapters)} chapters")
    print(f"  {words_total:,} words | {code_blocks} code blocks | {quiz_count} quiz questions")
    print(f"  html      -> {SITE}")
    print(f"  markdown  -> {MD_OUT}")
    print(f"  one file  -> {single_path} ({single_path.stat().st_size / 1048576:.2f} MB)")


if __name__ == "__main__":
    build()
