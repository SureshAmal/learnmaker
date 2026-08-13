import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { ArrowRight, ExternalLink } from "lucide-react";
import { getBook, getToc, getStats, listBooks } from "@/lib/content";
import Topbar from "@/components/Topbar";

export const revalidate = 86400;

export async function generateStaticParams() {
  try {
    const books = await listBooks();
    return books.map((b) => ({ book: b.slug }));
  } catch {
    // No database at build time (a preview build, say): pages render on first request.
    return [];
  }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ book: string }>;
}): Promise<Metadata> {
  const { book: slug } = await params;
  const book = await getBook(slug);
  return book ? { title: book.title, description: book.blurb } : {};
}

export default async function BookCover({ params }: { params: Promise<{ book: string }> }) {
  const { book: slug } = await params;
  const book = await getBook(slug);
  if (!book || !book.published) notFound();

  const [toc, stats] = await Promise.all([getToc(book.id), getStats(book.id)]);
  const first = toc.find((c) => c.sections.length)?.sections[0];
  const firstChapter = toc.find((c) => c.sections.length);

  return (
    <>
      <Topbar crumbs={[book.title]} ask />

      <div className="lesson">
        <div className="cover">
          <p className="meta">{book.subtitle || "A book"}</p>
          <h1>{book.title}</h1>
          {book.blurb ? <p className="dek">{book.blurb}</p> : null}
          {first && firstChapter ? (
            <p className="start" style={{ marginTop: 30 }}>
              <Link href={`/${book.slug}/${firstChapter.slug}/${first.slug}`}>
                Start reading <ArrowRight size={13} strokeWidth={1.9} />
              </Link>
            </p>
          ) : null}
        </div>

        <div className="figures">
          <div className="fig">
            <b>{stats.chapters}</b>
            <span>Chapters</span>
          </div>
          <div className="fig">
            <b>{stats.sections}</b>
            <span>Sections</span>
          </div>
          <div className="fig">
            <b>{(stats.words / 1000).toFixed(0)}k</b>
            <span>Words</span>
          </div>
        </div>

        <h2 className="contents-head">Contents</h2>

        {toc.map((chapter, i) => (
          <div className="ch" key={chapter.slug}>
            <p className="ch-num">Chapter {i + 1}</p>
            <h3>{chapter.title}</h3>
            <p className="ch-meta">{chapter.sections.length} sections</p>
            <ol>
              {chapter.sections.map((section) => (
                <li key={section.slug}>
                  <Link href={`/${book.slug}/${chapter.slug}/${section.slug}`}>
                    {section.title}
                  </Link>
                </li>
              ))}
            </ol>
          </div>
        ))}

        {book.source_url ? (
          <p className="sources">
            <ExternalLink className="icon" size={13} strokeWidth={1.7} />
            Built from{" "}
            <a href={book.source_url} target="_blank" rel="noopener">
              {book.source_url.replace(/^https?:\/\//, "")}
            </a>
            {book.license ? ` · ${book.license}` : ""}
          </p>
        ) : null}
      </div>
    </>
  );
}
