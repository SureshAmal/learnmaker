import Link from "next/link";
import { notFound } from "next/navigation";
import { Save, Archive } from "lucide-react";
import { sql } from "@/lib/db";
import { getToc, neighbours } from "@/lib/content";
import { firstParagraph } from "@/lib/markdown";
import { updateSectionMeta, archiveSection } from "@/app/admin/actions";
import Editor from "@/components/editor/Editor";

export const dynamic = "force-dynamic";

type Row = {
  id: number;
  slug: string;
  title: string;
  dek: string;
  body: string;
  chapter_id: number;
  chapter_title: string;
  book_id: number;
  book_title: string;
};

export default async function EditOnPage({
  params,
}: {
  params: Promise<{ book: string; chapter: string; section: string }>;
}) {
  const { book, chapter, section } = await params;

  const [page] = await sql<Row[]>`
    select s.id, s.slug, s.title, s.dek, s.body,
           c.id as chapter_id, c.title as chapter_title,
           b.id as book_id, b.title as book_title
      from sections s
      join chapters c on c.id = s.chapter_id
      join books b on b.id = c.book_id
     where b.slug = ${book} and c.slug = ${chapter} and s.slug = ${section}
       and s.deleted_at is null
  `;
  if (!page) notFound();

  const toc = await getToc(page.book_id);
  const { prev, next } = neighbours(book, toc, chapter, section);
  const viewHref = `/${book}/${chapter}/${section}`;

  const details = (
    <>
      <form action={updateSectionMeta}>
        <input type="hidden" name="id" value={page.id} />
        <div className="row">
          <label className="field">
            <span>Title</span>
            <input name="title" defaultValue={page.title} required />
          </label>
          <label className="field mono">
            <span>Slug</span>
            <input name="slug" defaultValue={page.slug} required />
          </label>
        </div>
        <label className="field">
          <span>Deck — blank uses the first paragraph</span>
          <input name="dek" defaultValue={page.dek} />
        </label>
        <div className="btn-row">
          <button className="btn primary" type="submit">
            <Save size={13} strokeWidth={1.9} /> Save details
          </button>
          <Link className="btn" href={`/admin/edit/${book}/settings`}>
            Book settings
          </Link>
        </div>
      </form>

      <form action={archiveSection} style={{ marginTop: 14 }}>
        <input type="hidden" name="id" value={page.id} />
        <input type="hidden" name="back" value="chapter" />
        <button className="btn danger" type="submit">
          <Archive size={13} strokeWidth={1.7} /> Archive this section
        </button>
      </form>
    </>
  );

  return (
    <Editor
      key={page.id}
      sectionId={page.id}
      initialBody={page.body}
      viewHref={viewHref}
      details={details}
      title={page.title}
      // Mirrors the reading page: the stored deck, or the opening line when it is blank.
      dek={page.dek || firstParagraph(page.body)}
      crumbs={[page.book_title, page.chapter_title]}
      prev={prev ? `/admin/edit/${book}/${prev.href.split("/").slice(2).join("/")}` : null}
      next={next ? `/admin/edit/${book}/${next.href.split("/").slice(2).join("/")}` : null}
      onPage
      aiReady
    />
  );
}
