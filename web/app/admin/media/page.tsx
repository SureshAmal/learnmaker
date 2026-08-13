import Link from "next/link";
import { sql } from "@/lib/db";
import Uploader from "./Uploader";
import MediaGrid, { type Asset } from "./MediaGrid";

export const dynamic = "force-dynamic";
export const metadata = { title: "Media" };

const PER_PAGE = 60;

export default async function Media({
  searchParams,
}: {
  searchParams: Promise<{ tag?: string; q?: string; page?: string }>;
}) {
  const { tag = "", q = "", page = "1" } = await searchParams;
  const offset = (Math.max(1, Number(page) || 1) - 1) * PER_PAGE;

  const tags = await sql<{ tag: string; n: number }[]>`
    select tag, count(*)::int as n from assets group by tag order by tag
  `;

  const assets = await sql<Asset[]>`
    select id, url, pathname, size, tag from assets
     where true
       ${tag ? sql`and tag = ${tag}` : sql``}
       ${q ? sql`and pathname ilike ${"%" + q + "%"}` : sql``}
     order by created_at desc, id desc
     limit ${PER_PAGE} offset ${offset}
  `;

  const [{ total }] = await sql<{ total: number }[]>`
    select count(*)::int as total from assets
     where true
       ${tag ? sql`and tag = ${tag}` : sql``}
       ${q ? sql`and pathname ilike ${"%" + q + "%"}` : sql``}
  `;

  const pages = Math.max(1, Math.ceil(total / PER_PAGE));
  const current = Math.max(1, Number(page) || 1);
  const link = (p: number) =>
    `/admin/media?${new URLSearchParams({ ...(tag && { tag }), ...(q && { q }), page: String(p) })}`;

  return (
    <div className="admin">
      <h1>Media</h1>
      <p className="lede">
        Images are stored in the database and served from <code>/media/…</code>. Click one
        to see it full size. To put an image on a page, drop it into the editor.
      </p>

      <Uploader />

      <h2>Collections</h2>
      <div className="btn-row">
        <Link className={`btn${tag === "" ? " primary" : ""}`} href="/admin/media">
          All ({tags.reduce((n, t) => n + t.n, 0)})
        </Link>
        {tags.map((t) => (
          <Link
            key={t.tag}
            className={`btn${tag === t.tag ? " primary" : ""}`}
            href={`/admin/media?tag=${encodeURIComponent(t.tag)}`}
          >
            {t.tag || "uploads"} ({t.n})
          </Link>
        ))}
      </div>

      <form style={{ marginTop: 16 }}>
        {tag ? <input type="hidden" name="tag" value={tag} /> : null}
        <label className="field mono">
          <span>Filter by filename</span>
          <input name="q" defaultValue={q} placeholder="kmeans" />
        </label>
      </form>

      <h2>
        {total} image{total === 1 ? "" : "s"}
        {pages > 1 ? ` · page ${current} of ${pages}` : ""}
      </h2>

      {assets.length === 0 ? (
        <div className="list">
          <p className="empty">Nothing here yet.</p>
        </div>
      ) : (
        <MediaGrid assets={assets} />
      )}

      {pages > 1 ? (
        <div className="btn-row" style={{ marginTop: 20 }}>
          {current > 1 ? (
            <Link className="btn" href={link(current - 1)}>
              ← Previous
            </Link>
          ) : null}
          {current < pages ? (
            <Link className="btn" href={link(current + 1)}>
              Next →
            </Link>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
