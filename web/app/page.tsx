import Link from "next/link";
import { listBooks, getStats } from "@/lib/content";
import ThemeToggle from "@/components/ThemeToggle";
import SearchPalette from "@/components/SearchPalette";

// Pages are rebuilt on demand when the admin saves; between saves they are served from
// the static cache, with a daily rebuild as a backstop.
export const revalidate = 86400;

export default async function Shelf() {
  const books = await listBooks();
  const stats = await Promise.all(books.map((b) => getStats(b.id)));

  return (
    <>
      <SearchPalette />
      <main className="paper" style={{ marginLeft: "auto", marginRight: "auto" }}>
        <div className="topbar">
          <div className="crumb">
            <span className="here">The shelf</span>
          </div>
          <ThemeToggle />
        </div>

        <div className="lesson">
          <div className="cover">
            <p className="meta">Learn</p>
            <h1>Technical books, built from their sources</h1>
            <p className="dek">
              Every book is one Markdown page per section, rendered with the same
              typography, the same diagrams and the same maths.
            </p>
          </div>

          {books.length === 0 ? (
            <p className="empty">
              No books yet. <Link href="/admin">Sign in to the editor</Link> to add one.
            </p>
          ) : (
            <div className="shelf">
              {books.map((book, i) => (
                <Link key={book.slug} href={`/${book.slug}`}>
                  <span className="shelf-meta">
                    {stats[i].chapters} chapters · {stats[i].sections} sections ·{" "}
                    {stats[i].words.toLocaleString()} words
                  </span>
                  <b>{book.title}</b>
                  {book.blurb ? <p>{book.blurb}</p> : null}
                </Link>
              ))}
            </div>
          )}

          <p className="side-note" style={{ marginTop: 60 }}>
            <Link href="/admin">Editor →</Link>
          </p>
        </div>
      </main>
    </>
  );
}
