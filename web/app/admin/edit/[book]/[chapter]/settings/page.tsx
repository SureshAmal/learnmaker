import Link from "next/link";
import { notFound } from "next/navigation";
import { Archive, Save } from "lucide-react";
import { sql } from "@/lib/db";
import { updateChapter, archiveChapter } from "@/app/admin/actions";

export const dynamic = "force-dynamic";

/** Renaming a chapter, on the same layout as everything else in the editor. */
export default async function ChapterSettings({
  params,
}: {
  params: Promise<{ book: string; chapter: string }>;
}) {
  const { book, chapter } = await params;

  const [row] = await sql<{ id: number; slug: string; title: string; sections: number }[]>`
    select c.id, c.slug, c.title,
           (select count(*)::int from sections s
             where s.chapter_id = c.id and s.deleted_at is null) as sections
      from chapters c
      join books b on b.id = c.book_id
     where b.slug = ${book} and c.slug = ${chapter} and c.deleted_at is null
  `;
  if (!row) notFound();

  return (
    <div className="lesson blank-slate">
      <header className="lesson-head">
        <p className="meta">Chapter</p>
        <h1>{row.title}</h1>
        <p className="dek">
          {row.sections} section{row.sections === 1 ? "" : "s"}
        </p>
      </header>

      <form action={updateChapter}>
        <input type="hidden" name="id" value={row.id} />
        <div className="row">
          <label className="field">
            <span>Title</span>
            <input name="title" defaultValue={row.title} required autoFocus />
          </label>
          <label className="field mono">
            <span>Slug — this is the address readers see</span>
            <input name="slug" defaultValue={row.slug} required />
          </label>
        </div>
        <button className="btn primary" type="submit">
          <Save size={13} strokeWidth={1.9} /> Save chapter
        </button>
      </form>

      <h2 style={{ marginTop: 44 }}>Archive</h2>
      <p className="sources" style={{ margin: "0 0 14px" }}>
        The chapter and its sections come off the site but stay in{" "}
        <Link href="/admin/archive">the archive</Link>, restorable at any time.
      </p>
      <form action={archiveChapter}>
        <input type="hidden" name="id" value={row.id} />
        <button className="btn danger" type="submit">
          <Archive size={13} strokeWidth={1.7} /> Archive this chapter
        </button>
      </form>
    </div>
  );
}
