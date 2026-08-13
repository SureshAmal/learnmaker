import { NextResponse } from "next/server";
import { revalidatePath } from "next/cache";
import { sql } from "@/lib/db";
import { requireAdmin } from "@/lib/auth";

export const dynamic = "force-dynamic";

/** Every /media/<id>/… reference in a body. */
function mediaIds(markdown: string): Set<number> {
  const ids = new Set<number>();
  for (const match of markdown.matchAll(/\/media\/(\d+)\//g)) ids.add(Number(match[1]));
  return ids;
}

/**
 * Saves one section's Markdown, and reconciles the images it references.
 *
 * An image that the author removed from the page is deleted from the server too, but
 * only once nothing else points at it — an image used in two sections survives being
 * cut from one. Images loaded in bulk from the repository (they carry a `source`) are
 * never deleted this way, because the library is their home rather than any one page.
 */
export async function POST(request: Request) {
  await requireAdmin();

  const { id, body } = (await request.json()) as { id?: number; body?: string };
  if (!id || typeof body !== "string") {
    return NextResponse.json({ error: "id and body are required" }, { status: 400 });
  }

  const [before] = await sql<{ body: string }[]>`select body from sections where id = ${id}`;
  if (!before) return NextResponse.json({ error: "No such section" }, { status: 404 });

  await sql`update sections set body = ${body}, updated_at = now() where id = ${id}`;

  const removed = [...mediaIds(before.body)].filter((mediaId) => !mediaIds(body).has(mediaId));
  let deleted = 0;
  if (removed.length) {
    const orphans = await sql<{ id: number }[]>`
      delete from assets
       where id = any(${removed})
         and source = ''
         and not exists (
           select 1 from sections
            where body like '%/media/' || assets.id || '/%'
         )
      returning id
    `;
    deleted = orphans.length;
  }

  const [row] = await sql<{ book: string; chapter: string; section: string }[]>`
    select b.slug as book, c.slug as chapter, s.slug as section
      from sections s
      join chapters c on c.id = s.chapter_id
      join books b on b.id = c.book_id
     where s.id = ${id}
  `;

  // Push the change straight to the static cache so the public page is current the
  // moment the editor says "Saved", without waiting for the revalidation window.
  if (row) revalidatePath(`/${row.book}/${row.chapter}/${row.section}`);

  return NextResponse.json({ ok: true, savedAt: new Date().toISOString(), deleted });
}
