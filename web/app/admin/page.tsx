import Link from "next/link";
import { Plus, ExternalLink, Eye, EyeOff, Settings } from "lucide-react";
import { sql } from "@/lib/db";
import { createBook, togglePublished } from "./actions";
import MoveButtons from "@/components/MoveButtons";

export const dynamic = "force-dynamic";
export const metadata = { title: "Books" };

type Row = {
  id: number;
  slug: string;
  title: string;
  published: boolean;
  chapters: number;
  sections: number;
};

export default async function AdminBooks() {
  const books = await sql<Row[]>`
    select b.id, b.slug, b.title, b.published,
           count(distinct c.id)::int as chapters,
           count(s.id)::int as sections
      from books b
      left join chapters c on c.book_id = b.id and c.deleted_at is null
      left join sections s on s.chapter_id = c.id and s.deleted_at is null
     where b.deleted_at is null
     group by b.id
     order by b.position, b.id
  `;

  return (
    <div className="admin">
      <h1>Books</h1>
      <p className="lede">Each book holds chapters; each chapter holds sections of Markdown.</p>

      <h2>Shelf</h2>
      {books.length === 0 ? (
        <div className="list">
          <p className="empty">No books yet. Add the first one below.</p>
        </div>
      ) : (
        <div className="list">
          {books.map((book, i) => (
            <div className="list-row" key={book.id}>
              <span className="handle">{i + 1}</span>
              <span className="grow">
                <Link href={`/admin/edit/${book.slug}`}>{book.title}</Link>
                <span className="sub">
                  /{book.slug} · {book.chapters} chapters · {book.sections} sections
                </span>
              </span>
              {book.published ? null : <span className="chip draft">Hidden</span>}
              <form action={togglePublished}>
                <input type="hidden" name="id" value={book.id} />
                <button
                  className="btn"
                  type="submit"
                  title={
                    book.published
                      ? "Hide this book from the public shelf"
                      : "Show this book on the public shelf"
                  }
                >
                  {book.published ? (
                    <>
                      <Eye size={13} strokeWidth={1.7} /> Visible
                    </>
                  ) : (
                    <>
                      <EyeOff size={13} strokeWidth={1.7} /> Hidden
                    </>
                  )}
                </button>
              </form>
              <Link className="btn" href={`/admin/edit/${book.slug}/settings`} title="Book settings">
                <Settings size={13} strokeWidth={1.7} /> Settings
              </Link>
              <Link className="nudge" href={`/${book.slug}`} target="_blank" aria-label="View">
                <ExternalLink size={14} strokeWidth={1.7} />
              </Link>
              <MoveButtons
                kind="book"
                id={book.id}
                first={i === 0}
                last={i === books.length - 1}
              />
            </div>
          ))}
        </div>
      )}

      <h2>New book</h2>
      <form action={createBook}>
        <div className="row">
          <label className="field">
            <span>Title</span>
            <input name="title" required placeholder="Machine Learning" />
          </label>
          <label className="field mono">
            <span>Slug (optional)</span>
            <input name="slug" placeholder="machine-learning" />
          </label>
        </div>
        <label className="field">
          <span>Blurb</span>
          <input name="blurb" placeholder="One line for the shelf card." />
        </label>
        <button className="btn primary" type="submit">
          <Plus size={13} strokeWidth={2} /> Create book
        </button>
      </form>
    </div>
  );
}
