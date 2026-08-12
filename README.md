# Learn — technical books built from official sources

Three offline-readable books, built by the same engine from the source material
of each subject. Each one ships as a single self-contained HTML file, as a multi-page
site, and as clean Markdown.

| Book | One file | Source | Licence |
| --- | --- | --- | --- |
| The Hugging Face LLM course | `llm-course.html` | [huggingface/course](https://github.com/huggingface/course) | Apache 2.0 |
| C# and .NET | `dotnet-course.html` | [dotnet/docs](https://github.com/dotnet/docs) | CC BY 4.0 (samples MIT) |
| Machine Learning | `ml-course.html` | course notes (`ml-course/*.md`) | course material |

The first two are fully self-contained. The Machine Learning book is the one exception:
its diagrams render with [Mermaid](https://mermaid.js.org) and its math with
[KaTeX](https://katex.org), both loaded from a CDN, so those pages want a network
connection to draw the figures.

Both have the same reading furniture: hash-routed sections, Ctrl+K search, an
Ask panel (below), a section-outline ruler, light/dark, and no external dependencies.

---

# Book 1 — the Hugging Face LLM course

A static, offline-readable build of the official
[Hugging Face LLM course](https://huggingface.co/learn/llm-course/en). One page per section,
full original prose, every code block, and every end-of-chapter quiz made interactive.

The layout follows the [makingsoftware.com](https://www.makingsoftware.com) book format:
a paper column on a neutral field, monospace labels, serif body, one blue accent, no emoji.

## Read it

**One file, nothing else:** open `llm-course.html`. All 100 sections, the CSS, the JS and
the search index are inside that single 2.9 MB file — double-click it, drop it on a USB
stick, or commit it anywhere static. No server, no build step, no asset folder.

To publish on GitHub Pages, just enable Pages on the branch: `index.html` in the repo
root is a shelf page linking to both books, so `/` lands on the chooser and
`/llm-course.html` on this book.

Sections are routed through the hash — `…/index.html#chapter2/2` for a section,
`…#chapter2/2--attention-masks` for a heading — so deep links and the back button work,
and every URL survives being pasted somewhere.

**Or the multi-page build**, one HTML file per section:

```bash
python3 -m http.server -d site 8000    # then open http://localhost:8000
```

`site/index.html` also opens fine straight from disk. Either way, nothing loads from a
bundler or CDN — the only remote requests are the course's own diagrams on huggingface.co.

## Layout

| Path | What it is |
| --- | --- |
| `index.html` | The root shelf page: both books, their figures, and their sources |
| `llm-course.html` | **The whole course as one self-contained file** — the thing to host |
| `source/` | The upstream `.mdx` files, copied verbatim from `huggingface/course` |
| `build/build.py` | The generator: MDX -> HTML + Markdown |
| `site/` | Generated site: `index.html`, `chapterN/M.html`, `assets/` (incl. the search index) |
| `markdown/` | Generated plain Markdown of every section, JSX stripped |
| `huggingface_llm_course_full_source_coverage_book.html` | The earlier single-file summary; superseded by `site/` |

## Rebuild

```bash
python3 build/build.py          # this book
python3 build/build_dotnet.py   # the .NET book
python3 build/build_ml.py       # the machine learning book
python3 build/build_index.py    # the root shelf page (reads every builder's stats)
```

Requires `markdown`, `pyyaml`, `pygments`. To pick up upstream changes:

```bash
git clone --depth 1 https://github.com/huggingface/course /tmp/hfcourse
rm -rf source && cp -r /tmp/hfcourse/chapters/en source && rm -rf source/events
python3 build/build.py
```

Then update `COMMIT` in `build/build.py` so the footer credits the right revision.

## What the generator does

- Strips MDX-only components (`<CourseFloatingBanner>`, `<FrameworkSwitchCourse>`).
- Turns `<Question choices={[...]} />` into interactive quizzes — click *Check answer*
  to score and reveal the per-option explanations. 133 questions across the course.
- Converts `<Tip>` and GitHub alert callouts (`> [!TIP]`, `> [!WARNING]`) into boxed notes.
- Turns `<Youtube id=…>` into a link out (no third-party embeds, no tracking).
- Labels every code block with its language and marks program output separately.
- Replaces every emoji with an inline SVG icon or plain words (`🤗 Transformers`
  becomes `Hugging Face Transformers`), including inside sample strings in code.
- Rewrites `/course/chapterN/M` links to point at the local pages.

## Reading aids

- **Ctrl+K** (or `Cmd+K`, or just `/`) opens search over all 100 sections — titles,
  headings, and body text, including code. Arrow keys move, Enter opens, Esc closes.
  A hit whose heading matched deep-links straight to that heading. The index
  (`site/assets/search-data.js`) is loaded as a script on first use, so search works
  over `file://` too, where `fetch` is blocked.
- `[` and `]` page to the previous/next section.
- The ruler on the right edge tracks your position: the percentage readout rides alongside
  the tick you are currently on, and each section of the page gets a longer mark at its
  real position. Hover the ruler to reveal the section names as an outline, and click one
  to jump. The current section's mark stays highlighted.
- Scroll position is remembered per page for the session.
- Light and dark themes, following the OS by default, toggled from the top bar. The theme
  is applied by a tiny inline script in `<head>`, before the first paint, so pages never
  flash light before turning dark.
- Page-to-page navigation crossfades (`@view-transition`) with the sidebar and ruler held
  still, and is disabled under `prefers-reduced-motion`. Asset URLs carry a content hash,
  so a stale cached stylesheet can't survive a rebuild.
- Every link that leaves the book opens in a new tab, so you never lose your place;
  links between sections navigate in place as normal.
- Copy button on every code block.
- Print stylesheet: quiz explanations are expanded, chrome is hidden.

## Credit

All text, code, and figures are from
[huggingface/course](https://github.com/huggingface/course) at commit `5805d51`,
Apache 2.0. This repository only reformats them.


---

# Book 2 — C# and .NET

The C# language and the .NET runtime, read front to back: **257 articles in 15 chapters,
305,000 words, 1,733 code samples**, built from Microsoft's own documentation.

```bash
python3 build/build_dotnet.py        # -> dotnet-course.html, site-dotnet/, markdown-dotnet/
```

Open `dotnet-course.html`, or serve `site-dotnet/`. Same as the other book: one file,
no server, hash routes, reachable from the root `index.html` shelf page.

## Where the content comes from

[dotnet/docs](https://github.com/dotnet/docs) is the repository behind
learn.microsoft.com/dotnet. Prose is CC BY 4.0, samples are MIT — both redistributable
with attribution, which every page carries.

The reading order is not invented: it follows Microsoft's own `docs/csharp/toc.yml`,
regrouped front-to-back in `build/curriculum.py`. Left out on purpose: the language
reference and API listings (lookup material, not reading material), breaking-change
logs, and the Roslyn compiler SDK.

| Chapter | |
| --- | --- |
| 0 | Setup and the .NET CLI |
| 1 | A tour of C# |
| 2 | Program structure and types |
| 3 | Values, nulls, and strings |
| 4 | Expressions, statements, and control flow |
| 5 | Object-oriented C# |
| 6 | Methods, delegates, and events |
| 7 | Generics and collections |
| 8 | LINQ |
| 9 | Asynchronous programming |
| 10 | Exceptions and functional techniques |
| 11 | Advanced C# |
| 12 | The .NET runtime |
| 13 | What's new in C# |
| 14 | Guided tutorials |

## What the .NET builder has to do

Microsoft's Markdown is its own dialect, handled in `build/build_dotnet.py`:

- `:::code language="csharp" source="snippets/x.cs" id="Y":::` — code lives in real,
  compilable sample projects, not in the article. Each directive is resolved against the
  sample file and the named region (`// <Y>` … `// </Y>`, or `#region Y`, or `range=`)
  is pulled in, dedented. 1,733 samples resolved; the 33 whose files aren't in the source
  copy are dropped silently rather than left as a broken link.
- `[!INCLUDE [x](../includes/y.md)]` — 524 of them, inlined recursively.
- `<xref:System.String.Format%2A>` — 6,000+ API references, turned into links to the
  .NET API browser.
- `> [!NOTE] / [!TIP] / [!WARNING]` — rendered as the same callouts as the other book.
- Code inside list items and inside callouts is rendered directly rather than via the
  Markdown fence parser: the docs indent list continuations by 3 spaces, python-markdown
  wants 4, and fences inside blockquotes aren't parsed at all. Both cases used to leak
  raw ``` into the page and restart list numbering.
- `.md` links point at our own pages when we ship the target, at learn.microsoft.com
  when we don't. Sample paths are resolved case-insensitively (the docs say
  `numbers.cs`, the repo ships `Numbers.cs`).

## Refreshing from upstream

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/dotnet/docs /tmp/dotnetdocs
git -C /tmp/dotnetdocs sparse-checkout set --skip-checks docs/csharp docs/standard docs/core docs/fundamentals
# copy the text files (not media - images are linked from raw.githubusercontent.com)
python3 build/build_dotnet.py
```

---

# The Ask panel (Gemini / Vertex AI)

Both books can answer questions **from their own content**. Press **Ctrl+I** or the
`Ask` button in the top bar. It is a docked right-hand sidebar, not a dialog: the text
column narrows to make room and stays readable, so you can follow the answer against the
book. Press the button again to close it.

Clicking a citation moves the *book* to that section with the panel still open, and in
the page-per-section build the panel and its open chat come back after the page load.

How a question is answered:

1. The question is matched against the book's index locally — the same scoring the
   search palette uses, over titles, headings and body text.
2. The six best sections are cut down to the passages that actually mention the
   question, capped at 1,800 characters each.
3. Those excerpts are sent to the model with instructions to answer *only* from them,
   to say so when the book doesn't cover something, and to cite excerpts as `[1]`, `[2]`.
4. The answer **streams** in over Server-Sent Events (`streamGenerateContent?alt=sse`),
   repainting on frame boundaries rather than per token, with a caret while it arrives.
   If an endpoint can't stream, it falls back to a single response.
5. Each citation is a link to the section it came from, plus a *Sections used* list.
   Code in answers is highlighted client-side with the same classes the book's own code
   blocks use, so it matches in both themes.
6. Every answer carries a collapsible **Request** block: the exact endpoint and method,
   the provider and model, how many sections and characters were sent, and the verbatim
   prompt. The API key is replaced with `***` even there. Retrieval always happens
   locally, so the model only ever sees those excerpts, never the whole book.

Settings (the gear icon) take a provider, an API key and a model name. Nothing else —
no project, no location, no OAuth token.

| Provider | Key from | Endpoint |
| --- | --- | --- |
| AI Studio (Gemini API) | `aistudio.google.com` | `generativelanguage.googleapis.com` |
| Vertex AI | Google Cloud console | `aiplatform.googleapis.com/v1/publishers/google/models/…` |

The chosen provider is tried first; if the key isn't valid there the other is tried
automatically, and whichever answered is remembered for next time.

## Chat history

The panel keeps a sidebar of past chats, newest first, with the question as the title.
Click one to reopen it, `+ New` to start fresh, the bin icon to delete. History is stored
locally, per book, so the two books never mix.

Storage writes to **IndexedDB and localStorage together** and merges them on read. That
sounds redundant, and it is deliberate: a browser can have IndexedDB present but stalled
(an opened database whose transactions never fire an event, which is what `file://`
does in some browsers), and the two backends disagree about which pages can use them.
Every call is also time-boxed, so a stalled database degrades to the other store instead
of leaving the sidebar empty forever.

**On credentials.** No key is ever written into the built files — the page ships with
none, and the builder never sees one. What you type is kept in that browser's
`localStorage` and sent only to Google. That means: anyone with access to that browser
profile can read it, so don't enter a key on a shared machine, and don't treat a
published copy of these files as a way to share a key. If you want many people to use
the Ask panel, put a small proxy in front of the API and hold the credential there
instead of handing each reader a key. Vertex AI may also need CORS allowed for
browser-origin calls; the Gemini API key mode works from the browser as-is.
