/**
 * Loads the repository's image sets into the media library:
 *
 *   ref/openai-generated-diagrams/reference-style/   38 topic diagrams, one per concept
 *   slide-notes/assets/<deck>/page-NNN.png          the lecture slides, per deck
 *
 * Each file is stored once, keyed by its path under `source`, so re-running updates
 * rather than duplicating. Slides carry the deck as their tag, which is what the media
 * library filters on.
 *
 *   bun run --env-file=.env.local ./scripts/import-images.ts
 */
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join, resolve, extname } from "node:path";
import postgres from "postgres";
import sharp from "sharp";

const REPO = resolve(process.cwd(), "..");

const url = process.env.DATABASE_URL;
if (!url) {
  console.error("DATABASE_URL is not set.");
  process.exit(1);
}
const sql = postgres(url, {
  ssl: url.includes("localhost") || url.includes("127.0.0.1") ? false : "require",
  max: 1,
});

const MIME: Record<string, string> = {
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".avif": "image/avif",
  ".svg": "image/svg+xml",
};

/** Rendered slides and diagrams arrive at print resolution — around 1 MB each, which is
 *  three megabytes on a page carrying three figures. A page never shows one wider than
 *  the paper column, so they are resized to fit a high-density screen and re-encoded as
 *  WebP. SVG is vector already and passes through untouched. */
const MAX_WIDTH = 1600;

async function optimise(absolute: string, mime: string) {
  if (mime === "image/svg+xml") {
    return { bytes: readFileSync(absolute), mime, extension: extname(absolute) };
  }
  const bytes = await sharp(absolute)
    .resize({ width: MAX_WIDTH, withoutEnlargement: true })
    .webp({ quality: 82 })
    .toBuffer();
  return { bytes, mime: "image/webp", extension: ".webp" };
}

async function store(absolute: string, relative: string, tag: string) {
  const source = MIME[extname(absolute).toLowerCase()];
  if (!source) return false;

  const { bytes, mime, extension } = await optimise(absolute, source);
  const name = relative.split("/").pop()!.replace(/\.[^.]+$/, "") + extension;

  const [asset] = await sql<{ id: number }[]>`
    insert into assets (url, pathname, alt, size, mime, data, source, tag)
    values ('', ${name}, '', ${bytes.length}, ${mime}, ${bytes}, ${relative}, ${tag})
    on conflict (source) where source <> '' do update set
      data = excluded.data, size = excluded.size, mime = excluded.mime,
      pathname = excluded.pathname, tag = excluded.tag
    returning id
  `;

  // The URL embeds the row id, so it is written back once the row is known. Slides keep
  // the deck in the filename segment so a pasted link says what it points at.
  const label = tag ? `${tag}-${name}` : name;
  await sql`update assets set url = ${`/media/${asset.id}/${label}`} where id = ${asset.id}`;
  return true;
}

async function importDirectory(dir: string, tag: string, recurse = false) {
  const absolute = join(REPO, dir);
  if (!existsSync(absolute)) {
    console.log(`skip ${dir}: not found`);
    return 0;
  }

  let count = 0;
  for (const entry of readdirSync(absolute, { withFileTypes: true }).sort((a, b) =>
    a.name.localeCompare(b.name),
  )) {
    const child = `${dir}/${entry.name}`;
    if (entry.isDirectory()) {
      if (recurse) count += await importDirectory(child, entry.name);
      continue;
    }
    if (await store(join(absolute, entry.name), child, tag)) count++;
  }
  return count;
}

const diagrams = await importDirectory(
  "ref/openai-generated-diagrams/reference-style",
  "reference-style",
);
console.log(`reference diagrams: ${diagrams}`);

// One image per diagram in the ML source, drawn to replace the Mermaid original.
const units = await importDirectory(
  "ref/openai-generated-diagrams/unit-diagrams",
  "unit-diagrams",
);
console.log(`unit diagrams: ${units}`);

// The raw lecture slides. Kept in the library for reference; they are not placed into
// pages, because a photographed PowerPoint slide reads badly next to typeset prose.
const slides = await importDirectory("slide-notes/assets", "", true);
console.log(`slides: ${slides}`);

await sql.end();
console.log("done");
