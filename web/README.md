# The book app

Content and build are separate. Postgres holds the Markdown; Next.js renders it to static
HTML at build time and re-renders the affected pages the moment the editor saves. One
domain serves both the books and the editor that writes them.

```
Postgres  ──▶  lib/markdown.ts  ──▶  static HTML page
   ▲                                      ▲
   │                                      │ revalidatePath() on save
   └────── /admin editor ─────────────────┘
```

## Run it locally

```bash
bun install
cp .env.example .env.local          # fill in DATABASE_URL and SESSION_SECRET
bun run db:migrate                  # create the tables
bun run db:import                   # load the three existing books
bun run db:images                   # load the slide and diagram images
bun run db:figures                  # place those images into the ML book
bun run dev                         # http://localhost:3000
```

The editor is at `/admin`, behind `ADMIN_USER` / `ADMIN_PASSWORD`.

## What an author gets

`/admin` is the whole content system:

| | |
| --- | --- |
| **Books** | create, rename, reorder, publish or unpublish, delete |
| **Chapters** | per book, reorderable |
| **Sections** | per chapter, reorderable — one page of Markdown each |
| **Editor** | edits the page on the reading layout itself — see below |
| **Media** | drag-and-drop upload, browsable library, click a thumbnail to view it full size |

Books have a **Visible / Hidden** toggle on `/admin`: hidden books disappear from the
public shelf and their pages 404, while staying fully editable.

### Images

Uploads are resized to 1600px and re-encoded as WebP, then stored in Postgres and served
from `/media/<id>/<name>` with a one-year immutable cache. Nothing is written to disk, so
uploading works the same locally and on a read-only serverless filesystem, and a database
backup contains the pictures as well as the prose.

Two collections ship with the repo and are loaded by `bun run db:images`:

- `ref/openai-generated-diagrams/reference-style/` — 38 concept diagrams
- `slide-notes/assets/` — 412 lecture slides, tagged by deck

`bun run db:figures` places them into the ML book: the 38 diagrams from an explicit
name-to-section table in `scripts/place-ml-figures.ts`, and the slides by scoring each
one's page notes against the section title, keeping only confident matches (two per
section). Every inserted block is wrapped in a `<!-- figures:auto -->` marker, so
re-running replaces what the last run added and never touches hand-written prose.
`--clear` removes them all.

### Editing on the page

`/admin/edit/<book>/<chapter>/<section>` is the reading layout with the contents made
editable: the same sidebar in the same place, the same paper column, the same type. The
sidebar reorders by dragging, adds a chapter or section inline, and archives one in a
click — each of them one step from the page it changes. The top bar switches between
**Write**, **Markdown** and **Read**, so the rendered page is always one click away and
never a different screen.

Editing is desktop-only. Below 860px the controls are hidden and the page stays readable:
a block editor with drag handles has nowhere to go on a phone, and a mis-drag there costs
real content.

The editor has two modes over one document:

- **Visual** — an Editor.js block surface. No standing toolbar: a `+` opens the block
  menu, selecting text raises a floating bar, and each block has a drag handle for
  reordering. Images are blocks, so they move, caption and delete like anything else.
- **Markdown** — CodeMirror, for when the source is the point.

Markdown is the document in both cases; blocks are a view onto it. Before the visual
editor opens a page it converts the Markdown to blocks and back, and compares the two —
if anything a reader would notice differs, it refuses the page and leaves the author in
Markdown mode. A page can never be silently rewritten by being opened.

Measured over all 409 pages: **ML 100%, C#/.NET 92%, LLM 91% — 93% overall** open in the
block editor. The remainder are pages using constructs the block model would alter, and
they stay in Markdown mode. Anything written in this editor is block-editable from the
start. Constructs with no honest block equivalent — display maths, Mermaid fences, raw
HTML — appear as a source box and come back byte-identical.

Dropped images are held in the browser as `blob:` URLs and uploaded only when the page is
saved, so an image pasted and then removed never reaches the server. An image deleted from
a page is deleted server-side too, once nothing else references it.

The editor autosaves 1.8 s after typing stops, and on Ctrl/Cmd+S. The preview is rendered
by the server through the same pipeline the published page uses, so it is the output
rather than an approximation of it.

### Nothing is deleted

Archiving a book, chapter or section stamps `deleted_at`: it leaves the site, search and
the admin lists, and `/admin/archive` restores it in one click. Permanent deletion exists
only inside the archive.

## What a page may contain

Every book gets the same treatment, so a reader never meets two different houses:

- **GitHub Markdown** — tables, task lists, footnotes, strikethrough
- **Maths** — `$inline$` and `$$display$$`, rendered to static KaTeX HTML on the server
- **Diagrams** — ` ```mermaid ` fences, drawn in the browser, redrawn on a theme switch,
  and click-to-zoom into a full-screen viewer
- **Plots and figures** — inline `<svg>` passes through untouched; `.figsvg` and `.figimg`
  wrappers pick up the book's own figure styling and the same zoom viewer
- **Images** — Markdown or raw `<img>`, from Blob or any URL
- **Code** — any language, highlighted by Shiki in both themes at once, with a copy button

## Deploying to Vercel

1. **Import the repo**, and set **Root Directory** to `web`. Bun and Next are detected
   from `bun.lock`; no build command override is needed.
2. **Add a Postgres database** (Neon, Supabase or Vercel Postgres) and set `DATABASE_URL`.
   The build reads it to pre-render every page, so it must be set for *Production*,
   *Preview* and *Development*. Budget for the images: the three books plus all 450
   pictures come to roughly **35 MB**, which fits inside a Neon or Supabase free tier.
3. **Set** `ADMIN_USER`, `ADMIN_PASSWORD` and `SESSION_SECRET`. No storage credentials
   are needed — images live in the same database.
4. **Run the migration and the imports once** against the production database:
   ```bash
   export DATABASE_URL='<production url>'
   bun run ./scripts/migrate.ts
   bun run ./scripts/import.ts
   bun run ./scripts/import-images.ts
   bun run ./scripts/place-ml-figures.ts
   ```
5. **Point your domain** at the project. Everything lives under it: `/` is the shelf,
   `/<book>/<chapter>/<section>` is a page, `/admin` is the editor.

### On caching

Reading pages are statically generated and revalidate daily. Every write in the editor
calls `revalidatePath` for what it touched, so a save is visible immediately — the daily
window is only a backstop.

## Security note

`ADMIN_PASSWORD` is stored and compared as plain text, by request: there is no hash and no
user table. The session cookie itself is signed (HS256, httpOnly, `SameSite=Lax`), so it
cannot be forged, and `proxy.ts` rejects any unsigned request to `/admin` or `/api/admin`
before it reaches the database. The exposure that remains is the password itself — anyone
who can read the environment can sign in. Keep it out of the repo and rotate it if a
deploy log, a screenshot or a shared dashboard account ever leaks it.

Raw HTML and inline SVG in a section body are rendered as written. That is deliberate —
it is what makes hand-drawn figures possible — and it is safe only because the single
admin is the only person who can write content. Do not open authoring to untrusted users
without adding sanitisation to `lib/markdown.ts`.

## Layout

```
app/
  page.tsx                        the shelf
  [book]/                         cover, then [chapter]/[section] reading pages
  admin/                          editor: books, chapters, sections, media
  api/                            search, preview, section save, upload
lib/
  markdown.ts                     the one render pipeline
  content.ts                      every read query
  db.ts  schema.sql               connection and tables
  auth.ts                         sign-in and the session cookie
scripts/
  migrate.ts  import.ts           set up, and load the existing books
```
