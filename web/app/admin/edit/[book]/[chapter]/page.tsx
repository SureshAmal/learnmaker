import { notFound, redirect } from "next/navigation";
import { Plus } from "lucide-react";
import { sql } from "@/lib/db";
import { createSection } from "@/app/admin/actions";

export const dynamic = "force-dynamic";

/**
 * A chapter has no page of its own — readers meet chapters through their sections. So
 * opening one either goes straight to its first section, or, when it has none yet, offers
 * the one thing worth doing here: writing the first.
 */
export default async function ChapterEntry({
  params,
}: {
  params: Promise<{ book: string; chapter: string }>;
}) {
  const { book, chapter } = await params;

  const [row] = await sql<{ id: number; title: string; first: string | null }[]>`
    select c.id, c.title,
           (select s.slug from sections s
             where s.chapter_id = c.id and s.deleted_at is null
             order by s.position limit 1) as first
      from chapters c
      join books b on b.id = c.book_id
     where b.slug = ${book} and c.slug = ${chapter} and c.deleted_at is null
  `;
  if (!row) notFound();

  if (row.first) redirect(`/admin/edit/${book}/${chapter}/${row.first}`);

  return (
    <div className="lesson blank-slate">
      <header className="lesson-head">
        <p className="meta">{row.title}</p>
        <h1>Nothing in this chapter yet</h1>
        <p className="dek">A chapter is a shelf; the writing lives in its sections.</p>
      </header>

      <form action={createSection} className="blank-form">
        <input type="hidden" name="chapter_id" value={row.id} />
        <input name="title" placeholder="Title of the first section" autoFocus required />
        <button className="btn primary" type="submit">
          <Plus size={13} strokeWidth={2} /> Add section
        </button>
      </form>
    </div>
  );
}
