import Link from "next/link";
import { RotateCcw, Trash2 } from "lucide-react";
import { sql } from "@/lib/db";
import {
  restoreBook, purgeBook, restoreChapter, purgeChapter, restoreSection, purgeSection,
} from "../actions";

export const dynamic = "force-dynamic";
export const metadata = { title: "Archive" };

type Row = { id: number; title: string; where: string; deleted_at: string };

function when(value: string) {
  return new Date(value).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export default async function ArchivePage() {
  const books = await sql<Row[]>`
    select id, title, slug as where, deleted_at from books
     where deleted_at is not null order by deleted_at desc
  `;

  const chapters = await sql<Row[]>`
    select c.id, c.title, b.title as where, c.deleted_at
      from chapters c join books b on b.id = c.book_id
     where c.deleted_at is not null order by c.deleted_at desc
  `;

  const sections = await sql<Row[]>`
    select s.id, s.title, b.title || ' · ' || c.title as where, s.deleted_at
      from sections s
      join chapters c on c.id = s.chapter_id
      join books b on b.id = c.book_id
     where s.deleted_at is not null order by s.deleted_at desc
  `;

  const groups = [
    { label: "Books", rows: books, restore: restoreBook, purge: purgeBook },
    { label: "Chapters", rows: chapters, restore: restoreChapter, purge: purgeChapter },
    { label: "Sections", rows: sections, restore: restoreSection, purge: purgeSection },
  ];

  const total = books.length + chapters.length + sections.length;

  return (
    <div className="admin">
      <h1>Archive</h1>
      <p className="lede">
        Everything removed from the site, kept whole. Restore puts an item back exactly
        where it was. Deleting permanently is the only action here that loses content.
      </p>

      {total === 0 ? (
        <div className="list" style={{ marginTop: 30 }}>
          <p className="empty">
            Nothing archived. <Link href="/admin">Back to the books</Link>.
          </p>
        </div>
      ) : null}

      {groups.map((group) =>
        group.rows.length ? (
          <section key={group.label}>
            <h2>
              {group.label} ({group.rows.length})
            </h2>
            <div className="list">
              {group.rows.map((row) => (
                <div className="list-row" key={row.id}>
                  <span className="grow">
                    <span style={{ font: "400 16px/1.3 var(--serif)" }}>{row.title}</span>
                    <span className="sub">
                      {row.where} · archived {when(row.deleted_at)}
                    </span>
                  </span>
                  <form action={group.restore}>
                    <input type="hidden" name="id" value={row.id} />
                    <button className="btn" type="submit">
                      <RotateCcw size={12} strokeWidth={1.8} /> Restore
                    </button>
                  </form>
                  <form action={group.purge}>
                    <input type="hidden" name="id" value={row.id} />
                    <button
                      className="btn danger"
                      type="submit"
                      title="Delete permanently — this cannot be undone"
                    >
                      <Trash2 size={12} strokeWidth={1.7} />
                    </button>
                  </form>
                </div>
              ))}
            </div>
          </section>
        ) : null,
      )}
    </div>
  );
}
