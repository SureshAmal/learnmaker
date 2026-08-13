import Link from "next/link";
import { notFound } from "next/navigation";
import { Archive, Save, ExternalLink } from "lucide-react";
import { getBook } from "@/lib/content";
import { updateBook, archiveBook } from "@/app/admin/actions";

export const dynamic = "force-dynamic";

/**
 * A book's own details, shown on the reading layout like everything else in the editor,
 * with the contents still beside it. There is no separate settings screen to navigate
 * away to.
 */
export default async function BookSettings({ params }: { params: Promise<{ book: string }> }) {
  const { book: slug } = await params;
  const book = await getBook(slug);
  if (!book) notFound();

  return (
    <div className="lesson blank-slate">
      <header className="lesson-head">
        <p className="meta">Book</p>
        <h1>{book.title}</h1>
        <p className="dek">
          <Link href={`/${book.slug}`} target="_blank">
            /{book.slug} <ExternalLink size={12} strokeWidth={1.7} />
          </Link>
        </p>
      </header>

      <form action={updateBook}>
        <input type="hidden" name="id" value={book.id} />
        <div className="row">
          <label className="field">
            <span>Title</span>
            <input name="title" defaultValue={book.title} required />
          </label>
          <label className="field mono">
            <span>Slug</span>
            <input name="slug" defaultValue={book.slug} required />
          </label>
        </div>
        <div className="row">
          <label className="field">
            <span>Subtitle</span>
            <input name="subtitle" defaultValue={book.subtitle} />
          </label>
          <label className="field">
            <span>Licence</span>
            <input name="license" defaultValue={book.license} />
          </label>
        </div>
        <label className="field">
          <span>Blurb</span>
          <input name="blurb" defaultValue={book.blurb} />
        </label>
        <label className="field mono">
          <span>Source URL</span>
          <input name="source_url" defaultValue={book.source_url} />
        </label>
        <label className="btn-row" style={{ margin: "0 0 18px" }}>
          <input type="checkbox" name="published" defaultChecked={book.published} />
          <span style={{ font: "400 14.5px/1 var(--serif)" }}>
            Published — visible on the public shelf
          </span>
        </label>
        <button className="btn primary" type="submit">
          <Save size={13} strokeWidth={1.9} /> Save details
        </button>
      </form>

      <h2 style={{ marginTop: 44 }}>Archive</h2>
      <p className="sources" style={{ margin: "0 0 14px" }}>
        Archiving takes the book off the shelf and out of search. Nothing is lost — it
        stays in <Link href="/admin/archive">the archive</Link>, restorable in one click.
      </p>
      <form action={archiveBook}>
        <input type="hidden" name="id" value={book.id} />
        <button className="btn danger" type="submit">
          <Archive size={13} strokeWidth={1.7} /> Archive this book
        </button>
      </form>
    </div>
  );
}
