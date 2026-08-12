#!/usr/bin/env python3
"""Build the C# / .NET book from the official Microsoft documentation sources.

Source of truth: github.com/dotnet/docs -> docs/**.md (copied into ./source-dotnet).
Prose is CC BY 4.0, code samples are MIT; both are redistributable with attribution.

The rendering engine, stylesheet and client-side app are shared with the LLM book in
build.py. What lives here is the Microsoft-flavoured Markdown front end: snippet
includes, triple-colon directives, xref API links and the curriculum in curriculum.py.

    python3 build/build_dotnet.py

    site-dotnet/index.html          contents
    site-dotnet/chN/M.html          one page per article
    markdown-dotnet/chN/M.md        cleaned Markdown
    dotnet-course.html              the whole book as one self-contained file
"""

from __future__ import annotations

import html
import json
import re
import shutil
import urllib.request
from pathlib import Path

import markdown
import yaml

import ask as ask_panel
import build as engine
import curriculum

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source-dotnet"
SITE = ROOT / "site-dotnet"
MD_OUT = ROOT / "markdown-dotnet"
SINGLE = ROOT / "dotnet-course.html"

REPO = "https://github.com/dotnet/docs"
RAW = "https://raw.githubusercontent.com/dotnet/docs/main/docs"
SAMPLE_RAW = "https://raw.githubusercontent.com/dotnet/docs/main"
LEARN = "https://learn.microsoft.com/dotnet"
API = "https://learn.microsoft.com/dotnet/api"
COMMIT = "main"

BRAND = "C# &amp; .NET"
BOOK_TITLE = "C# and .NET"


# --------------------------------------------------------------------------------------
# curriculum selection
# --------------------------------------------------------------------------------------

def toc_tree(toc_path):
    """Flatten a docs TOC into [(name_path, href), ...] in document order."""
    data = yaml.safe_load(toc_path.read_text(encoding="utf-8"))
    items = data["items"] if isinstance(data, dict) else data
    out = []

    def walk(nodes, trail):
        for node in nodes:
            name = node.get("name", "")
            here = trail + (name,)
            href = node.get("href")
            if href and href.endswith(".md") and not href.startswith("http"):
                out.append((here, href))
            walk(node.get("items") or [], here)

    walk(items, ())
    return out


def resolve(base, href):
    return (base / href).resolve()


def find_file(path):
    """Sample paths in the docs do not always match the file's case on disk."""
    if path.exists():
        return path
    parent = path.parent
    if not parent.is_dir():
        # the directory itself may be the mismatch
        try:
            grand = find_dir(parent)
        except OSError:
            return None
        if grand is None:
            return None
        parent = grand
    wanted = path.name.lower()
    for child in parent.iterdir():
        if child.name.lower() == wanted:
            return child
    return None


def find_dir(path):
    if path.is_dir():
        return path
    parent = path.parent
    if not parent.is_dir():
        parent = find_dir(parent)
        if parent is None:
            return None
    wanted = path.name.lower()
    for child in parent.iterdir():
        if child.is_dir() and child.name.lower() == wanted:
            return child
    return None


def select():
    """Return [(chapter_title, [(title, Path), ...]), ...] for the whole book."""
    tocs = {"csharp": toc_tree(SRC / "csharp" / "toc.yml")}
    chapters = []
    seen = set()

    for chapter_title, picks in curriculum.CHAPTERS:
        entries = []
        for kind, spec in picks:
            if kind == "files":
                for title, rel in spec:
                    path = SRC / rel
                    if path.exists() and str(path) not in seen:
                        seen.add(str(path))
                        entries.append((title, path))
                continue

            base = SRC / kind
            cap = curriculum.LIMIT.get((kind, spec))
            taken = 0
            for name_path, href in tocs[kind]:
                if name_path[:len(spec)] != spec:
                    continue
                rel = f"{kind}/{href}"
                if any(rel.endswith(s) or s in rel for s in curriculum.SKIP):
                    continue
                path = resolve(base, href)
                if not path.exists() or str(path) in seen:
                    continue
                if cap is not None and taken >= cap:
                    continue
                seen.add(str(path))
                entries.append((name_path[-1], path))
                taken += 1
        if entries:
            chapters.append((chapter_title, entries))
    return chapters


# --------------------------------------------------------------------------------------
# Microsoft-flavoured Markdown
# --------------------------------------------------------------------------------------

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
INCLUDE = re.compile(r"\[!INCLUDE\s*\[[^\]]*\]\(([^)]+)\)\]")
TRIPLE_CODE = re.compile(r"^([ \t]*):::code\s+(.+?):::[ \t]*$", re.M)
TRIPLE_IMAGE = re.compile(r"^([ \t]*):::image\s+(.+?):::[ \t]*$", re.M)
TRIPLE_OTHER = re.compile(r"^:::(?:zone|moniker|form|row|column|no-loc)[^\n]*$", re.M)
ATTR = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')
DIV_MARK = re.compile(r"^\s*>?\s*\[!div[^\]]*\]\s*$", re.M)
XREF_TAG = re.compile(r"<xref:([^>\s]+)>")
XREF_LINK = re.compile(r"\]\(xref:([^)\s]+)\)")
VIDEO = re.compile(r"^\s*>\s*\[!(?:VIDEO|Video)\]\(([^)]+)\)\s*$", re.M)


def strip_frontmatter(text):
    match = FRONTMATTER.match(text)
    if not match:
        return text, {}
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return text[match.end():], meta


def inline_includes(text, base, depth=0):
    """`[!INCLUDE [x](../includes/y.md)]` pulls another file in verbatim."""
    if depth > 3:
        return text

    def repl(match):
        target = (base / match.group(1).split("#")[0]).resolve()
        if not target.exists():
            return ""
        body, _ = strip_frontmatter(target.read_text(encoding="utf-8"))
        return inline_includes(body.strip(), target.parent, depth + 1)

    return INCLUDE.sub(repl, text)


def snippet_of(path, attrs):
    """Pull the referenced region out of a sample file.

    Docs mark regions either with `// <Name>` ... `// </Name>` comment tags or with
    `#region Name`; `range=` selects raw line numbers instead.
    """
    try:
        source = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError):
        return None
    lines = source.replace("\r\n", "\n").split("\n")

    name = attrs.get("id") or attrs.get("ID")
    if name:
        # docs reference a region by a short name (`#35`, `#FirstImplementation`) while
        # the sample marks it `Snippet` + that name (`<Snippet35>`, `<SnippetFirst...>`),
        # so try the bare name and the Snippet-prefixed form
        candidates = [name, f"Snippet{name}"]
        start = end = None
        for cand in candidates:
            open_tag = re.compile(rf"<{re.escape(cand)}>\s*$", re.I)
            close_tag = re.compile(rf"</{re.escape(cand)}>", re.I)
            region = re.compile(rf"#region\s+{re.escape(cand)}\s*$", re.I)
            endregion = re.compile(r"#endregion")
            for i, line in enumerate(lines):
                if start is None and (open_tag.search(line) or region.search(line)):
                    start = i + 1
                elif start is not None and (close_tag.search(line) or endregion.search(line)):
                    end = i
                    break
            if start is not None:
                break
        if start is None:
            return None
        chunk = lines[start:end if end is not None else len(lines)]
    elif attrs.get("range"):
        chunk = []
        for part in attrs["range"].split(","):
            bounds = part.split("-")
            first = int(bounds[0])
            last = int(bounds[-1]) if len(bounds) > 1 else first
            chunk += lines[first - 1:last]
    else:
        chunk = lines

    # drop any nested region markers and blank edges, then dedent
    chunk = [ln for ln in chunk if not re.search(r"</?\w[\w.]*>\s*$", ln.strip())
             or not ln.strip().startswith("//")]
    chunk = [ln for ln in chunk if "#region" not in ln and "#endregion" not in ln]
    while chunk and not chunk[0].strip():
        chunk.pop(0)
    while chunk and not chunk[-1].strip():
        chunk.pop()
    if not chunk:
        return None
    pad = min((len(ln) - len(ln.lstrip()) for ln in chunk if ln.strip()), default=0)
    return "\n".join(ln[pad:] if ln.strip() else "" for ln in chunk)


MISSING = []
CODE_MARK = "\x05CODE%d\x05"
CODE_SLOT = re.compile(r"(?:<p>\s*)?\x05CODE(\d+)\x05(?:\s*</p>)?")

_highlighter = markdown.Markdown(
    extensions=["fenced_code", "codehilite"],
    extension_configs={"codehilite": {"guess_lang": False, "css_class": "hl",
                                      "linenums": False}},
)


def render_code(lang, body):
    """Highlight a sample directly.

    A `:::code` directive often sits inside a numbered list, and an indented fence is
    not reliably parsed as a fence, so these never go through the Markdown pass at all.
    """
    _highlighter.reset()
    fence = "````" if "```" in body else "```"
    out = _highlighter.convert(f"{fence}{lang}\n{body}\n{fence}")
    label = html.escape(LANG_LABEL.get(lang, lang or "code"))
    return f'<div class="codeblock"><span class="lang">{label}</span>{out}</div>'


LANG_LABEL = {"csharp": "c#", "cs": "c#", "vb": "visual basic", "fsharp": "f#",
              "console": "output", "output": "output", "txt": "text",
              "dotnetcli": "cli", "powershell": "powershell", "bash": "bash"}


WRAPPED_SLOT = re.compile(
    r'<div class="codeblock"[^>]*>.*?</pre></div></div>', re.S)


def unwrap_slots(body_html, samples):
    """Render code slots, never one inside another.

    A slot line can be indented enough that Markdown reads it as an indented code
    block, which would wrap the rendered sample in a second, language-less block.
    Any wrapper that only exists to hold slots is replaced by the slots themselves.
    """

    def unwrap(match):
        found = CODE_SLOT.findall(match.group(0))
        if not found:
            return match.group(0)
        return "".join(render_code(*samples[int(n)]) for n in found)

    body_html = WRAPPED_SLOT.sub(unwrap, body_html)
    return CODE_SLOT.sub(lambda m: render_code(*samples[int(m.group(1))]), body_html)


def rewrite_code_blocks(text, base, stash):
    """`:::code language="csharp" source="snippets/x.cs" id="Y":::` -> a code slot."""

    def repl(match):
        indent = match.group(1)
        attrs = dict(ATTR.findall(match.group(2)))
        lang = attrs.get("language", "csharp")
        source = attrs.get("source")
        if not source:
            return ""
        # resolve beside-article files locally and fetch samples/ ones the same way the
        # older [!code-] references do, so `:::code source="~/samples/..."` inlines too
        path = local_sample(source.split("#")[0], base)
        body = snippet_of(path, attrs) if path else None
        if body is None:
            # a sample we cannot resolve: say nothing rather than link somewhere broken,
            # and never inject a block that would split the surrounding list
            MISSING.append(source)
            return ""
        stash.append((lang, body))
        return f"\n{list_indent(indent)}{CODE_MARK % (len(stash) - 1)}\n"

    return TRIPLE_CODE.sub(repl, text)


CODE_REF = re.compile(
    r'^([ \t]*)\[!code-([\w-]+)\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)\][ \t]*$', re.M)


def code_ref_url(path_part, base):
    """Where a `[!code-]` sample lives when we can't ship it.

    These legacy snippets sit in a top-level `samples/` dir of the dotnet/docs repo.
    Both `~/samples/...` (`~` is that repo root) and a `../../samples/...` climb out of
    the article resolve there - not to the separate dotnet/samples repo, which is why
    the first cut 404'd."""
    m = re.search(r"(?:^|/)(samples/.+)$", path_part)
    if m:
        return f"{REPO}/blob/main/{m.group(1)}"
    if path_part.startswith("~/"):
        return f"{REPO}/blob/main/docs/{path_part[2:]}"
    target = (base / path_part).resolve()
    try:
        return f"{REPO}/blob/main/docs/{target.relative_to(SRC).as_posix()}"
    except ValueError:
        return REPO


FETCHED = []
_fetch_failed = set()


def local_sample(path_part, base):
    """Resolve a `[!code-]` sample to a file on disk.

    Files that sit beside the article are already in our checkout. The legacy
    snippets under `samples/` are not - they live in a top-level dir of dotnet/docs
    that the text-only source copy leaves out - so fetch each one the first time and
    cache it under the source tree, keeping later builds offline. Returns None when the
    reference isn't fetchable (or the network is down), so the caller links out."""
    m = re.search(r"(?:^|/)(samples/.+)$", path_part)
    if not m:
        if path_part.startswith(("~", "/")):
            return None
        return find_file((base / path_part).resolve())
    rel = m.group(1)
    dest = SRC / rel
    if dest.exists():
        return dest
    hit = find_file(dest)
    if hit:
        return hit
    if rel in _fetch_failed:
        return None
    # raw.githubusercontent is case-sensitive, but docs often write `program.cs` for a
    # repo `Program.cs`; try the referenced case first, then a capitalised file name
    head, _, name = rel.rpartition("/")
    candidates = [rel]
    if name[:1].islower():
        alt = f"{name[:1].upper()}{name[1:]}"
        candidates.append(f"{head}/{alt}" if head else alt)
    data = None
    for cand in candidates:
        try:
            with urllib.request.urlopen(f"{SAMPLE_RAW}/{cand}", timeout=20) as resp:
                data = resp.read()
            break
        except Exception:
            continue
    if data is None:
        _fetch_failed.add(rel)
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    FETCHED.append(rel)
    return dest


def rewrite_code_refs(text, base, stash):
    """Older `[!code-csharp[title](path#region)]` sample references.

    These predate the `:::code:::` directive and point into the dotnet/samples repo,
    which is mostly outside our source copy. Inline the snippet when the file is here;
    otherwise link to the sample on GitHub. Either way the raw directive never
    survives to the page, where Markdown would turn it into stray text plus a broken
    `[title](path)` link - which is exactly what leaked before.
    """

    def repl(match):
        indent, lang, ref = match.group(1), match.group(2).lower(), match.group(3)
        path_part, _, frag = ref.partition("#")
        attrs = {}
        if frag:
            # only an L-prefixed fragment (`#L10-L20`) is a line range; a bare number
            # like `#36` is a region name (`<Snippet36>`), not line 36
            span = re.fullmatch(r"L(\d+)(?:-L?(\d+))?", frag)
            if span:
                attrs["range"] = span.group(1) if not span.group(2) else \
                    f"{span.group(1)}-{span.group(2)}"
            else:
                attrs["id"] = frag
        path = local_sample(path_part, base)
        body = snippet_of(path, attrs) if path else None
        if body is not None:
            stash.append((lang, body))
            return f"\n{list_indent(indent)}{CODE_MARK % (len(stash) - 1)}\n"
        MISSING.append(path_part)
        name = html.escape(path_part.rsplit("/", 1)[-1] or path_part)
        return f"{indent}[{name} (sample on GitHub)]({code_ref_url(path_part, base)})"

    return CODE_REF.sub(repl, text)


QUOTED_FENCE = re.compile(
    r"^(?P<pre>[ \t]*>[ \t]?)(?P<fence>```+)(?P<lang>[\w#+-]*)[ \t]*\n"
    r"(?P<body>(?:(?:[ \t]*>[ \t]?).*\n)*?)"
    r"(?:[ \t]*>[ \t]?)(?P=fence)[ \t]*$",
    re.M,
)


def hoist_quoted_fences(text, stash):
    """Markdown does not parse a fence inside a blockquote, and the docs put samples
    inside `> [!NOTE]` callouts, so those become code slots as well."""

    def repl(match):
        pre = match.group("pre")
        body = "\n".join(
            re.sub(r"^[ \t]*>[ \t]?", "", line) for line in match.group("body").split("\n")
        ).strip("\n")
        if not body.strip():
            return match.group(0)
        stash.append((match.group("lang") or "csharp", body))
        return f"{pre}{CODE_MARK % (len(stash) - 1)}"

    return QUOTED_FENCE.sub(repl, text)


INDENTED_FENCE = re.compile(
    r"^(?P<ind>[ \t]{1,7})(?P<fence>```+)(?P<lang>[\w#+-]*)[ \t]*\n"
    r"(?P<body>.*?)\n"
    r"[ \t]*(?P=fence)[ \t]*$",
    re.M | re.S,
)


def list_indent(indent):
    """Re-indent a list continuation to what python-markdown expects.

    The converter runs at a tab length of 2, matching how the docs indent list
    continuations (one marker width per level). A block written at 2 or 3 spaces sits
    one level deep, 4 or 5 two levels, and so on - snap it to that even boundary so it
    stays inside its item rather than starting an indented code block.
    """
    width = len(indent.expandtabs(4))
    if not width:
        return ""
    return " " * (2 * (width // 2))


def hoist_indented_fences(text, stash):
    """Fences written inside a list item have the same indentation problem."""

    def repl(match):
        body = match.group("body")
        lines = [ln for ln in body.split("\n")]
        pad = min((len(ln) - len(ln.lstrip()) for ln in lines if ln.strip()), default=0)
        body = "\n".join(ln[pad:] if ln.strip() else "" for ln in lines).strip("\n")
        if not body:
            return ""
        stash.append((match.group("lang") or "text", body))
        return f"{list_indent(match.group('ind'))}{CODE_MARK % (len(stash) - 1)}"

    return INDENTED_FENCE.sub(repl, text)


def rewrite_images(text, base):
    def repl(match):
        attrs = dict(ATTR.findall(match.group(2)))
        source = attrs.get("source")
        if not source:
            return ""
        path = (base / source).resolve()
        try:
            url = f"{RAW}/{path.relative_to(SRC).as_posix()}"
        except ValueError:
            return ""
        alt = html.escape(attrs.get("alt-text", ""), quote=True)
        return f'\n\n<img src="{url}" alt="{alt}" loading="lazy">\n\n'

    return TRIPLE_IMAGE.sub(repl, text)


def api_url(target):
    """Turn `System.String.Format%2A?displayProperty=nameWithType` into a docs URL."""
    ref = target.split("?")[0]
    ref = ref.replace("%2A", "").replace("*", "").rstrip("*")
    ref = re.sub(r"`\d+$", "", ref)
    ref = re.sub(r"\(.*\)$", "", ref)
    slug = ref.replace("`", "-").lower()
    return f"{API}/{slug}", ref


def rewrite_xrefs(text):
    """API references become links to the .NET API browser."""
    def bare(match):
        url, ref = api_url(match.group(1))
        shown = ref.split(".")[-1] if "displayProperty" not in match.group(1) else ref
        return f"[`{shown}`]({url})"

    text = XREF_LINK.sub(lambda m: f"]({api_url(m.group(1))[0]})", text)
    return XREF_TAG.sub(bare, text)


def rewrite_video(text):
    def repl(match):
        url = match.group(1)
        return (f'\n\n<p class="demo"><a href="{url}" target="_blank" rel="noopener">'
                f'{engine.icon("video", 15)}<span>Watch the video</span></a></p>\n\n')

    return VIDEO.sub(repl, text)


HREF = re.compile(r'href="([^"]+)"')


def fix_links(body_html, base, routes, learn_path=""):
    """Repoint every link in the rendered article.

    Done after Markdown rather than before, so nothing depends on the link having been
    written in Markdown syntax in the first place. Two kinds need work: site-absolute
    paths like `/nuget/consume-packages/...`, which are learn.microsoft.com URLs and
    would otherwise resolve against our own host, and `.md` paths, which point at either
    a page we ship or one we don't.
    """

    ids = set(re.findall(r'id="([^"]+)"', body_html))

    def repl(match):
        href = match.group(1)
        # a same-page anchor for a heading this article does not have: the upstream
        # article does, so send the reader there rather than nowhere
        if href.startswith("#"):
            if href[1:] and href[1:] not in ids and learn_path:
                return f'href="{LEARN}/{learn_path}{href}"'
            return match.group(0)
        # an xref written inside a raw HTML href turns into a Markdown link there
        wrapped = re.match(r"^\[[^\]]*\]\((.+)\)$", href)
        if wrapped:
            href = wrapped.group(1)
            return f'href="{href}"'
        if re.match(r"^(?:[a-z]+:|//|mailto:)", href):
            return match.group(0)
        if href.startswith("/"):
            return f'href="{LEARN.rsplit("/dotnet", 1)[0]}{href}"'
        path, _, anchor = href.partition("#")
        anchor = f"#{anchor}" if anchor else ""
        # docs TOC landing pages are .yml, and sample references point into the
        # dotnet/samples repository through a `~/` docs root
        if path.endswith(".yml"):
            target = (base / path).resolve()
            try:
                rel = target.relative_to(SRC).as_posix()
            except ValueError:
                return f'href="{LEARN}{anchor}"'
            return f'href="{LEARN}/{rel[:-4]}{anchor}"'
        sample = re.search(r"(?:^|/)(samples/.+)$", path)
        if sample:
            return f'href="{REPO}/blob/main/{sample.group(1)}{anchor}"'
        if path.startswith("~/"):
            return f'href="{LEARN}/{path[2:]}{anchor}"'
        # sample files referenced beside the article live in the docs repo itself
        if re.search(r"\.(?:cs|vb|fs|csproj|fsproj|vbproj|json|xml|csv|razor|cshtml|"
                     r"config|txt|props|targets|sln|ps1|sh|py|js|ts|sql|http)$", path):
            target = (base / path).resolve()
            try:
                rel = target.relative_to(SRC).as_posix()
            except ValueError:
                return f'href="{REPO}{anchor}"'
            return f'href="{REPO}/blob/main/docs/{rel}{anchor}"'
        if not path.endswith(".md"):
            return match.group(0)
        target = (base / path).resolve()
        route = routes.get(str(target))
        if route:
            return f'href="../{route}.html{anchor}"'
        try:
            rel = target.relative_to(SRC).as_posix()
        except ValueError:
            return f'href="{LEARN}{anchor}"'
        return f'href="{LEARN}/{rel[:-3]}{anchor}"'

    return engine.new_tab(HREF.sub(repl, body_html))


def rewrite_doc_links(text, base, routes):
    """Point `.md` links at our own pages when we ship them, at Learn when we don't."""

    def repl(match):
        label, href = match.group(1), match.group(2)
        anchor = ""
        if "#" in href:
            href, anchor = href.split("#", 1)
            anchor = "#" + anchor
        if not href.endswith(".md"):
            return match.group(0)
        target = (base / href).resolve()
        route = routes.get(str(target))
        if route:
            return f"[{label}](../{route}.html{anchor})"
        try:
            rel = target.relative_to(SRC).as_posix()
        except ValueError:
            return f"[{label}]({LEARN}{anchor})"
        return f"[{label}]({LEARN}/{rel[:-3]}{anchor})"

    return re.sub(r"\[([^\]]*)\]\(([^)\s]+\.md(?:#[\w-]+)?)\)", repl, text)


def to_markdown(path, routes):
    """Return (markdown, title, description, headings, code_samples)."""
    raw = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    text, meta = strip_frontmatter(raw)
    base = path.parent

    samples = []
    text = inline_includes(text, base)
    text, blocks = engine.protect_code(text)
    text = rewrite_code_blocks(text, base, samples)
    text = rewrite_code_refs(text, base, samples)
    text = rewrite_images(text, base)
    text = TRIPLE_OTHER.sub("", text)
    text = re.sub(r"^:::\s*$", "", text, flags=re.M)
    text = DIV_MARK.sub("", text)
    text = rewrite_video(text)
    text = rewrite_xrefs(text)
    text = rewrite_doc_links(text, base, routes)
    text = engine.rewrite_alerts(text)
    text = hoist_quoted_fences(text, samples)
    text = hoist_indented_fences(text, samples)
    text = engine.COMMENT.sub("", text)

    headings = []
    title = None

    def heading(match):
        nonlocal title
        hashes, name, anchor = match.group(1), match.group(2), match.group(3)
        name = name.strip()
        anchor = anchor or engine.slugify(name)
        if len(hashes) == 1 and title is None:
            title = engine.unescape_md(name)
            return ""
        if len(hashes) in (2, 3):
            headings.append((len(hashes), engine.unescape_md(re.sub(r"[*`\[\]]", "", name)), anchor))
        return f'{hashes} {name} <a class="anchor" href="#{anchor}" id="{anchor}">#</a>'

    text = engine.HEADING.sub(heading, text)
    text = engine.restore_code(text, blocks)
    text = re.sub(r"\n{4,}", "\n\n\n", text).strip() + "\n"

    heading_title = title or meta.get("title") or path.stem.replace("-", " ").title()
    return text, str(heading_title), str(meta.get("description") or ""), headings, samples


# --------------------------------------------------------------------------------------
# page templates (same furniture as the LLM book, different plate)
# --------------------------------------------------------------------------------------

def sidebar(chapters, current=None, depth=1, hashed=False):
    up = "../" * depth
    out = [f'<a class="logo" href="{"#" if hashed else up + "index.html"}">C# / .NET</a>', "<nav>"]
    for title, sections in chapters:
        out.append(f"<section><h2>{html.escape(title)}</h2><ul>")
        for route, section_title, _ in sections:
            href = f"#{route}" if hashed else f"{up}{route}.html"
            extra = f' data-route="{route}"' if hashed else ""
            cls = ' class="active"' if (not hashed and route == current) else ""
            out.append(f'<li><a{cls}{extra} href="{href}">{html.escape(section_title)}</a></li>')
        out.append("</ul></section>")
    out.append("</nav>")
    out.append(
        '<p class="side-note">Built from the official Microsoft documentation'
        f'<br><span class="mono">dotnet/docs &middot; CC BY 4.0</span></p>'
    )
    return "".join(out)


def topbar(crumb, prev_href, next_href):
    prev_html = (
        f'<a href="{prev_href}" class="nudge prev" aria-label="Previous section">{engine.icon("left", 15)}</a>'
        if prev_href else f'<span class="nudge off">{engine.icon("left", 15)}</span>'
    )
    next_html = (
        f'<a href="{next_href}" class="nudge next" aria-label="Next section">{engine.icon("right", 15)}</a>'
        if next_href else f'<span class="nudge off">{engine.icon("right", 15)}</span>'
    )
    return (
        f'<div class="topbar">{prev_html}{next_html}'
        f'<div class="crumb">{crumb}</div>'
        f'<button class="ask-open" type="button" title="Ask about this book (Ctrl I)"'
        f' aria-label="Ask about this book">{engine.icon("spark", 14)}<kbd>Ask</kbd></button>'
        f'<button class="find" type="button" title="Search the book (Ctrl K)"'
        f' aria-label="Search the book">{engine.icon("search", 14)}<kbd>Ctrl K</kbd></button>'
        f'<button class="theme" type="button" aria-label="Toggle theme">'
        f'<span class="ico-light">{engine.icon("moon", 15)}</span>'
        f'<span class="ico-dark">{engine.icon("sun", 15)}</span></button></div>'
    )


def article(meta):
    toc = ""
    if len(meta["headings"]) > 2:
        items = "".join(
            f'<li class="lvl{level}"><a href="#{anchor}">{html.escape(name)}</a></li>'
            for level, name, anchor in meta["headings"]
        )
        toc = (f'<nav class="page-toc"><h2>{engine.icon("hash", 13)}<span>In this section</span></h2>'
               f"<ul>{items}</ul></nav>")

    pager = []
    if meta["prev"]:
        pager.append(f'<a class="prev" href="{meta["prev_href"]}">{engine.icon("left", 14)}'
                     f'<span><em>Previous</em>{html.escape(meta["prev"])}</span></a>')
    if meta["next"]:
        pager.append(f'<a class="next" href="{meta["next_href"]}">'
                     f'<span><em>Next</em>{html.escape(meta["next"])}</span>{engine.icon("right", 14)}</a>')

    dek = html.escape(meta["dek"]) if meta["dek"] else html.escape(meta["chapter"])
    head = (
        '<header class="lesson-head">'
        f'<p class="meta">{html.escape(meta["chapter"].upper())}</p>'
        f'<h1>{html.escape(meta["title"])}</h1>'
        f'<p class="dek">{dek}</p><p class="rule">-----</p></header>'
    )
    foot = (
        '<footer class="lesson-foot">'
        f'<div class="pager">{"".join(pager)}</div>'
        f'<p class="sources">{engine.icon("link", 13)}'
        f'<a href="{LEARN}/{meta["learn"]}" target="_blank" rel="noopener">'
        "Read this article on learn.microsoft.com</a></p></footer>"
    )
    return (topbar(meta["crumb"], meta["prev_href"], meta["next_href"])
            + f'<article class="lesson">{head}{toc}{meta["html"]}{foot}</article>')


def cover(chapters, stats, hashed=False):
    cards = []
    for title, sections in chapters:
        number, _, name = title.partition(". ")
        links = "".join(
            f'<li><a href="{"#" + route if hashed else route + ".html"}">'
            f"{html.escape(section_title)}</a></li>"
            for route, section_title, _ in sections
        )
        cards.append(
            f'<section class="ch"><p class="ch-num">Chapter {html.escape(number)}</p>'
            f"<h3>{html.escape(name)}</h3>"
            f'<p class="ch-meta">{len(sections)} articles</p><ol>{links}</ol></section>'
        )
    first = chapters[0][1][0]
    first_href = f"#{first[0]}" if hashed else f"{first[0]}.html"

    return f"""{topbar('<span>Contents</span>', '', first_href)}
<article class="lesson home-body">
<header class="cover">
  <p class="meta">A BOOK BUILD OF THE OFFICIAL DOCUMENTATION</p>
  <h1>{BOOK_TITLE}</h1>
  <p class="dek">The C# language and the .NET runtime, read front to back:
  {stats['lessons']} articles from Microsoft's own documentation, ordered as a course,
  with every code sample pulled in from its sample project.</p>
  <p class="rule">-----</p>
  <p class="start"><a href="{first_href}">Begin with {html.escape(first[1])}
  {engine.icon('right', 14)}</a></p>
</header>

<div class="figures">
  <div class="fig"><b>{stats['chapters']}</b><span>chapters</span></div>
  <div class="fig"><b>{stats['lessons']}</b><span>articles</span></div>
  <div class="fig"><b>{stats['words']:,}</b><span>words</span></div>
  <div class="fig"><b>{stats['code']:,}</b><span>code samples</span></div>
</div>

<h2 class="contents-head">Contents</h2>
<div class="ch-list">{''.join(cards)}</div>

<footer class="lesson-foot">
<p class="sources">{engine.icon("book", 13)}Text and figures come from
<a href="{REPO}" target="_blank" rel="noopener">dotnet/docs</a>, the source of
learn.microsoft.com/dotnet, used under
<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC&nbsp;BY&nbsp;4.0</a>;
code samples are MIT. This build only reorders and reformats them.</p>
</footer>
</article>
"""


def page(title, body, chapters, current=None, depth=1, body_class=""):
    up = "../" * depth
    v = engine.asset_stamp()
    ask_markup = ask_panel.ask_markup(engine.icon, "dotnet")
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
</body>
</html>
"""


def single_file(chapters, routes, home_body, bodies, stats):
    templates = [f'<template data-route="__home">{home_body}</template>']
    for route, body in bodies:
        templates.append(f'<template data-route="{route}">{body}</template>')
    payload = json.dumps(routes, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    ask_markup = ask_panel.ask_markup(engine.icon, "dotnet")

    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{BOOK_TITLE}</title>
<meta name="description" content="The C# language and the .NET runtime as a single
self-contained page: {stats['lessons']} articles, {stats['code']} code samples,
built from Microsoft's official documentation.">
<script>/* set the theme before the first paint, or the page flashes light */
(function(){{var t;try{{t=localStorage.getItem('llmcourse-theme')}}catch(e){{}}
document.documentElement.setAttribute('data-theme',t||(window.matchMedia&&
window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'))}})();</script>
<style>{engine.STYLE.strip()}</style>
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
</body>
</html>
"""


# --------------------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------------------

def build():
    picked = select()

    # route ids first: pages cross-link to each other, so every path must be known up front
    routes_by_path = {}
    plan = []
    for c, (chapter_title, entries) in enumerate(picked):
        rows = []
        for s, (title, path) in enumerate(entries, start=1):
            route = f"ch{c}/{s}"
            routes_by_path[str(path)] = route
            rows.append((route, title, path))
        plan.append((chapter_title, rows))

    flat = [(route, title, path, chapter_title)
            for chapter_title, rows in plan for route, title, path in rows]

    for out in (SITE, MD_OUT):
        if out.exists():
            shutil.rmtree(out)
    (SITE / "assets").mkdir(parents=True)
    (SITE / "assets" / "style.css").write_text(engine.STYLE.strip() + "\n", encoding="utf-8")
    (SITE / "assets" / "app.js").write_text(engine.APP_JS.strip() + "\n", encoding="utf-8")

    # the docs indent list continuations by one marker width (2 spaces for a bullet),
    # not the 4 python-markdown assumes, so at the default a bullet's description and
    # nested sub-list detach from it; a tab length of 2 nests them the way the docs mean
    converter = engine.make_converter(tab_length=2)
    words_total = code_total = 0
    index, bodies, nav = [], [], []

    for i, (route, title, path, chapter_title) in enumerate(flat):
        md_text, doc_title, dek, headings, samples = to_markdown(path, routes_by_path)
        title = doc_title or title
        body_html = engine.render_markdown(md_text, converter)
        body_html = unwrap_slots(body_html, samples)
        body_html = fix_links(body_html, path.parent, routes_by_path,
                              path.relative_to(SRC).as_posix()[:-3])

        body_text = engine.plain_text(body_html)
        words = len(re.findall(r"\b[\w'-]+\b", body_text))
        words_total += words
        code_total += body_html.count('class="codeblock')

        md_path = MD_OUT / f"{route}.md"
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(
            f"<!-- source: {REPO}/blob/main/docs/{path.relative_to(SRC).as_posix()} -->\n\n"
            f"# {title}\n\n" + CODE_SLOT.sub(
                lambda m: "```%s\n%s\n```" % samples[int(m.group(1))],
                re.sub(r"\x04\w+\x04([^\x04]*)\x04", r"**\\1**", md_text)),
            encoding="utf-8",
        )

        prev_row = flat[i - 1] if i else None
        next_row = flat[i + 1] if i + 1 < len(flat) else None
        meta = {
            "route": route,
            "title": title,
            "dek": dek,
            "chapter": chapter_title,
            "html": body_html,
            "headings": headings,
            "words": words,
            "learn": path.relative_to(SRC).as_posix()[:-3],
            "crumb": (f'<span>{html.escape(chapter_title)}</span><b>/</b>'
                      f'<span class="here">{html.escape(title)}</span>'),
            "prev": prev_row[1] if prev_row else None,
            "next": next_row[1] if next_row else None,
            "prev_href": f"../{prev_row[0]}.html" if prev_row else "",
            "next_href": f"../{next_row[0]}.html" if next_row else "",
        }
        inner = article(meta)

        html_path = SITE / f"{route}.html"
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(
            page(title, inner, plan, current=route, depth=1), encoding="utf-8"
        )

        hashed = dict(meta)
        hashed["prev_href"] = f"#{prev_row[0]}" if prev_row else ""
        hashed["next_href"] = f"#{next_row[0]}" if next_row else ""
        bodies.append((route, engine.in_page_anchors(
            re.sub(r'href="\.\./(ch\d+/\d+)\.html', r'href="#\1', article(hashed)), route)))

        index.append({"u": f"{route}.html", "t": title, "c": chapter_title,
                      "h": [{"a": a, "t": t} for _, t, a in headings], "b": body_text})
        nav.append({"u": route, "t": title, "c": chapter_title})

    stats = {"chapters": len(plan), "lessons": len(flat),
             "words": words_total, "code": code_total, "quizzes": 0}

    (SITE / "index.html").write_text(
        page("Contents", cover(plan, stats), plan, current=None, depth=0, body_class="home"),
        encoding="utf-8",
    )
    (SITE / "assets" / "search-data.js").write_text(engine.search_index(index), encoding="utf-8")

    home = re.sub(r'href="(ch\d+/\d+)\.html"', r'href="#\1"', cover(plan, stats, hashed=True))
    SINGLE.write_text(single_file(plan, nav, home, bodies, stats), encoding="utf-8")

    if FETCHED:
        print(f"  fetched {len(FETCHED)} sample files from dotnet/docs into {SRC}")
    if MISSING:
        print(f"  note: {len(MISSING)} sample references could not be resolved, linked out")
    (Path(__file__).resolve().parent / "stats-dotnet.json").write_text(
        json.dumps({**stats, "chapter_titles": [t for t, _ in plan]}, indent=2),
        encoding="utf-8",
    )
    print(f"built {len(flat)} articles in {len(plan)} chapters")
    print(f"  {words_total:,} words | {code_total} code samples")
    print(f"  html      -> {SITE}")
    print(f"  markdown  -> {MD_OUT}")
    print(f"  one file  -> {SINGLE} ({SINGLE.stat().st_size / 1048576:.2f} MB)")


if __name__ == "__main__":
    build()
