import { sql } from "@/lib/db";

/**
 * Serves an uploaded image out of the database.
 *
 * The filename in the path is decoration — the id is what is looked up — but it keeps
 * the URL readable in a Markdown source and gives the browser a sensible name on save.
 * Bytes for a given id never change (a re-upload gets a new row), so the response is
 * immutable and the CDN keeps it for a year.
 */
export async function GET(
  _request: Request,
  { params }: { params: Promise<{ id: string; name: string }> },
) {
  const { id } = await params;

  const [asset] = await sql<{ data: Uint8Array | null; mime: string }[]>`
    select data, mime from assets where id = ${Number(id)}
  `;
  if (!asset?.data) return new Response("Not found", { status: 404 });

  return new Response(new Uint8Array(asset.data), {
    headers: {
      "content-type": asset.mime,
      "content-length": String(asset.data.length),
      "cache-control": "public, max-age=31536000, immutable",
    },
  });
}
