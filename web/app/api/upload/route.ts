import { NextResponse } from "next/server";
import sharp from "sharp";
import { sql } from "@/lib/db";
import { requireAdmin } from "@/lib/auth";

export const dynamic = "force-dynamic";

const ALLOWED = new Set([
  "image/png", "image/jpeg", "image/gif", "image/webp", "image/avif", "image/svg+xml",
]);
const MAX_BYTES = 8 * 1024 * 1024;

/**
 * Stores an uploaded image in the database and returns the URL to reference it by.
 *
 * Keeping the bytes in Postgres rather than an object store means uploads work the same
 * locally and on a read-only serverless filesystem, with no storage account to configure
 * and nothing to keep in sync when the database is restored from a backup.
 */
export async function POST(request: Request) {
  await requireAdmin();

  const form = await request.formData();
  const file = form.get("file");
  if (!(file instanceof File)) {
    return NextResponse.json({ error: "No file" }, { status: 400 });
  }
  if (!ALLOWED.has(file.type)) {
    return NextResponse.json({ error: `Unsupported type: ${file.type}` }, { status: 415 });
  }
  if (file.size > MAX_BYTES) {
    return NextResponse.json({ error: "Larger than 8 MB" }, { status: 413 });
  }

  const original = Buffer.from(await file.arrayBuffer());
  const stem = (file.name.replace(/\.[^.]+$/, "").replace(/[^\w\-]+/g, "-").slice(0, 110)) || "image";

  // A page never shows an image wider than its column, so a screenshot straight off a
  // retina display is resized and re-encoded before it is stored. SVG is already vector.
  let bytes = original;
  let mime = file.type;
  let name = `${stem}${file.name.match(/\.[^.]+$/)?.[0] ?? ""}`;
  if (file.type !== "image/svg+xml") {
    try {
      bytes = await sharp(original)
        .resize({ width: 1600, withoutEnlargement: true })
        .webp({ quality: 82 })
        .toBuffer();
      mime = "image/webp";
      name = `${stem}.webp`;
    } catch {
      // An image sharp cannot decode is stored exactly as uploaded rather than rejected.
    }
  }

  const [asset] = await sql<{ id: number }[]>`
    insert into assets (url, pathname, alt, size, mime, data)
    values ('', ${name}, ${String(form.get("alt") ?? "")}, ${bytes.length}, ${mime}, ${bytes})
    returning id
  `;

  // The URL contains the id, so it can only be built once the row exists.
  const url = `/media/${asset.id}/${name}`;
  await sql`update assets set url = ${url} where id = ${asset.id}`;

  return NextResponse.json({ url, id: asset.id, pathname: name });
}
