import { NextResponse } from "next/server";
import sharp from "sharp";
import { sql } from "@/lib/db";
import { requireAdmin } from "@/lib/auth";

export const dynamic = "force-dynamic";

/**
 * Files a picture the browser generated into the media library.
 *
 * The model was called by the browser with the author's own key; this only stores the
 * result, so a generated diagram becomes an ordinary asset — same table, same /media/
 * route, deletable from the same library.
 */
export async function POST(request: Request) {
  await requireAdmin();

  const { data, prompt } = (await request.json()) as { data?: string; prompt?: string };
  if (!data) return NextResponse.json({ error: "No image" }, { status: 400 });

  const description = (prompt ?? "diagram").trim();
  const bytes = await sharp(Buffer.from(data, "base64"))
    .resize({ width: 1600, withoutEnlargement: true })
    .webp({ quality: 82 })
    .toBuffer();

  const name =
    `${description.toLowerCase().replace(/[^a-z0-9]+/g, "-").slice(0, 60) || "diagram"}.webp`;

  const [asset] = await sql<{ id: number }[]>`
    insert into assets (url, pathname, alt, size, mime, data, tag)
    values ('', ${name}, ${description.slice(0, 200)}, ${bytes.length}, 'image/webp',
            ${bytes}, 'generated')
    returning id
  `;
  const url = `/media/${asset.id}/${name}`;
  await sql`update assets set url = ${url} where id = ${asset.id}`;

  return NextResponse.json({ url, id: asset.id });
}
