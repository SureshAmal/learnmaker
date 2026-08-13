import { notFound, redirect } from "next/navigation";
import Link from "next/link";
import { Plus, Settings } from "lucide-react";
import { sql } from "@/lib/db";
import { getBook } from "@/lib/content";
import { createChapter } from "@/app/admin/actions";

export const dynamic = "force-dynamic";

/** Opening a book lands on its first page, or on the invitation to write one. */
export default async function BookEntry({ params }: { params: Promise<{ book: string }> }) {
  const { book: slug } = await params;
  const book = await getBook(slug);
  if (!book) notFound();

  const [first] = await sql<{ chapter: string; section: string }[]>`
    select c.slug as chapter, s.slug as section
      from sections s
      join chapters c on c.id = s.chapter_id
     where c.book_id = ${book.id} and c.deleted_at is null and s.deleted_at is null
     order by c.position, s.position
     limit 1
  `;
  if (first) redirect(`/admin/edit/${slug}/${first.chapter}/${first.section}`);

  return (
    <div className="lesson blank-slate">
      <header className="lesson-head">
        <p className="meta">{book.title}</p>
        <h1>An empty book</h1>
        <p className="dek">Give it a first chapter and it will open there from now on.</p>
      </header>

      <form action={createChapter} className="blank-form">
        <input type="hidden" name="book_id" value={book.id} />
        <input name="title" placeholder="Title of the first chapter" autoFocus required />
        <button className="btn primary" type="submit">
          <Plus size={13} strokeWidth={2} /> Add chapter
        </button>
      </form>

      <p className="sources" style={{ textAlign: "center" }}>
        <Link href={`/admin/edit/${book.slug}/settings`}>
          <Settings size={12} strokeWidth={1.7} /> Book settings
        </Link>
      </p>
    </div>
  );
}
