import { notFound } from "next/navigation";
import { sql } from "@/lib/db";
import { getBook, getToc } from "@/lib/content";
import EditSidebar from "@/components/EditSidebar";

export const dynamic = "force-dynamic";

/**
 * The editing shell is the reading layout: the same sidebar in the same place, the same
 * paper column, the same type. Only the contents are editable and the page in the middle
 * is an editor. An author never has to translate between "the admin screen" and "the
 * page people read".
 */
export default async function EditLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ book: string }>;
}) {
  const { book: bookSlug } = await params;
  const book = await getBook(bookSlug);
  if (!book) notFound();

  const toc = await getToc(book.id);

  // The sidebar acts on database ids; the table of contents is keyed by slug.
  const rows = await sql<{ chapter: string; chapter_id: number; section: string | null; section_id: number | null }[]>`
    select c.slug as chapter, c.id as chapter_id, s.slug as section, s.id as section_id
      from chapters c
      left join sections s on s.chapter_id = c.id and s.deleted_at is null
     where c.book_id = ${book.id} and c.deleted_at is null
  `;

  const ids = {
    chapters: Object.fromEntries(rows.map((r) => [r.chapter, r.chapter_id])),
    sections: Object.fromEntries(
      rows.filter((r) => r.section).map((r) => [`${r.chapter}/${r.section}`, r.section_id!]),
    ),
  };

  return (
    <div className="editing">
      <EditSidebar
        bookSlug={book.slug}
        bookTitle={book.title}
        bookId={book.id}
        toc={toc}
        ids={ids}
      />
      <main className="paper">{children}</main>
    </div>
  );
}
