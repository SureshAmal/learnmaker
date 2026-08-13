/**
 * Loads the three books the Python engine already built into the content store.
 *
 * The Markdown under the `markdown` directories is the engine's own output — one file per section,
 * numbered in reading order, grouped into one directory per chapter — so the import is a
 * direct mapping rather than a conversion. Chapter titles come from the matching
 * `build/stats-*.json`, which is where the engine recorded them.
 *
 *   bun run --env-file=.env.local scripts/import.ts          # add anything missing
 *   bun run --env-file=.env.local scripts/import.ts --replace  # wipe each book first
 *
 * Re-running is safe: a book is matched by slug, and each section is upserted on
 * (chapter, slug), so an import never duplicates and never clobbers a book it does not
 * know about.
 */
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join, resolve } from "node:path";
import postgres from "postgres";
import { normalizeFences, stripHeadingAnchors } from "../lib/normalize";

const REPO = resolve(process.cwd(), "..");
const REPLACE = process.argv.includes("--replace");

const url = process.env.DATABASE_URL;
if (!url) {
  console.error("DATABASE_URL is not set.");
  process.exit(1);
}
const sql = postgres(url, {
  ssl: url.includes("localhost") || url.includes("127.0.0.1") ? false : "require",
  max: 1,
});

type Source = {
  slug: string;
  title: string;
  subtitle: string;
  blurb: string;
  source_url: string;
  license: string;
  dir: string;
  stats: string;
  /** Docs links in the .NET book are site-relative to learn.microsoft.com. */
  linkBase?: string;
};

const BOOKS: Source[] = [
  {
    slug: "llm-course",
    title: "The Hugging Face LLM course",
    subtitle: "Transformers, fine-tuning and inference",
    blurb:
      "The official Hugging Face LLM course: one page per section, every code block, " +
      "every end-of-chapter quiz.",
    source_url: "https://github.com/huggingface/course",
    license: "Apache 2.0",
    dir: "markdown",
    stats: "build/stats-llm.json",
  },
  {
    slug: "dotnet-course",
    title: "C# and .NET",
    subtitle: "The language, the libraries and the runtime",
    blurb:
      "Microsoft's own C# and .NET documentation, regrouped into a front-to-back " +
      "reading order.",
    source_url: "https://github.com/dotnet/docs",
    license: "CC BY 4.0 (samples MIT)",
    dir: "markdown-dotnet",
    stats: "build/stats-dotnet.json",
    linkBase: "https://learn.microsoft.com",
  },
  {
    slug: "ml-course",
    title: "Machine Learning",
    subtitle: "Supervised, unsupervised and the algorithms between",
    blurb:
      "A three-unit machine learning course, with the diagrams drawn as Mermaid and the " +
      "maths set in KaTeX.",
    source_url: "",
    license: "Course material",
    dir: "markdown-ml",
    stats: "build/stats-ml.json",
  },
];

function slugify(input: string, fallback = "untitled") {
  const slug = input
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
  return slug || fallback;
}

/** `chapter10` sorts after `chapter9`, which a plain string sort would get wrong. */
function numeric(name: string) {
  const m = name.match(/(\d+)/);
  return m ? Number(m[1]) : Number.MAX_SAFE_INTEGER;
}

/** Splits a section file into its title and the body below it. */
function parseSection(text: string, fallbackTitle: string) {
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  let title = fallbackTitle;
  let start = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim() || line.startsWith("<!--")) continue; // provenance comment
    const heading = line.match(/^#\s+(.+?)\s*$/);
    if (heading) {
      // The page prints the title in its own header, so it comes out of the body.
      title = heading[1].replace(/\s*<a class="anchor".*$/, "").trim();
      start = i + 1;
    }
    break;
  }

  return { title, body: lines.slice(start).join("\n").trim() + "\n" };
}

async function importBook(source: Source) {
  const dir = join(REPO, source.dir);
  if (!existsSync(dir)) {
    console.log(`skip ${source.slug}: ${source.dir} not found`);
    return;
  }

  const statsPath = join(REPO, source.stats);
  const chapterTitles: string[] = existsSync(statsPath)
    ? (JSON.parse(readFileSync(statsPath, "utf8")).chapter_titles ?? [])
    : [];

  const [book] = await sql<{ id: number }[]>`
    insert into books (slug, title, subtitle, blurb, source_url, license, position)
    values (${source.slug}, ${source.title}, ${source.subtitle}, ${source.blurb},
            ${source.source_url}, ${source.license},
            ${BOOKS.findIndex((b) => b.slug === source.slug) + 1})
    on conflict (slug) do update set
      title = excluded.title, subtitle = excluded.subtitle, blurb = excluded.blurb,
      source_url = excluded.source_url, license = excluded.license, updated_at = now()
    returning id
  `;

  if (REPLACE) await sql`delete from chapters where book_id = ${book.id}`;

  const chapterDirs = readdirSync(dir, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .sort((a, b) => numeric(a) - numeric(b));

  let sectionCount = 0;

  for (const [index, name] of chapterDirs.entries()) {
    const title = chapterTitles[index] ?? name;
    const [chapter] = await sql<{ id: number }[]>`
      insert into chapters (book_id, slug, title, position)
      values (${book.id}, ${slugify(name)}, ${title}, ${index + 1})
      on conflict (book_id, slug) do update set
        title = excluded.title, position = excluded.position, updated_at = now()
      returning id
    `;

    const files = readdirSync(join(dir, name))
      .filter((f) => f.endsWith(".md"))
      .sort((a, b) => numeric(a) - numeric(b));

    for (const [order, file] of files.entries()) {
      const raw = readFileSync(join(dir, name, file), "utf8");
      const { title: sectionTitle, body } = parseSection(raw, file.replace(/\.md$/, ""));

      // The docs sources contain fences that open indented inside a list item and close
      // at column 0; left alone they render as leaked prose and a stray ```.
      const repaired = stripHeadingAnchors(normalizeFences(body));
      const text = source.linkBase
        ? repaired.replace(/\]\((\/[^)]+)\)/g, `](${source.linkBase}$1)`)
        : repaired;

      await sql`
        insert into sections (chapter_id, slug, title, body, position)
        values (${chapter.id}, ${slugify(sectionTitle, file.replace(/\.md$/, ""))},
                ${sectionTitle}, ${text}, ${order + 1})
        on conflict (chapter_id, slug) do update set
          title = excluded.title, body = excluded.body,
          position = excluded.position, updated_at = now()
      `;
      sectionCount++;
    }
  }

  console.log(
    `${source.slug}: ${chapterDirs.length} chapters, ${sectionCount} sections`,
  );
}

for (const source of BOOKS) await importBook(source);
await sql.end();
console.log("done");
