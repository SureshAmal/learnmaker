import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { ChevronLeft, ChevronRight, List } from "lucide-react";
import { getPage, getToc, neighbours, allPagePaths } from "@/lib/content";
import { renderMarkdown, firstParagraph } from "@/lib/markdown";
import Topbar from "@/components/Topbar";
import Ruler from "@/components/Ruler";
import PageRuntime from "@/components/PageRuntime";

export const revalidate = 86400;

export async function generateStaticParams() {
  try {
    return await allPagePaths();
  } catch {
    return [];
  }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ book: string; chapter: string; section: string }>;
}): Promise<Metadata> {
  const { book, chapter, section } = await params;
  const page = await getPage(book, chapter, section);
  if (!page) return {};
  return {
    title: `${page.section.title} · ${page.book.title}`,
    description: page.section.dek || firstParagraph(page.section.body, 160),
  };
}

export default async function SectionPage({
  params,
}: {
  params: Promise<{ book: string; chapter: string; section: string }>;
}) {
  const { book: bookSlug, chapter: chapterSlug, section: sectionSlug } = await params;
  const page = await getPage(bookSlug, chapterSlug, sectionSlug);
  if (!page || !page.book.published) notFound();

  const { book, chapter, section } = page;
  const [toc, rendered] = await Promise.all([
    getToc(book.id),
    renderMarkdown(section.body),
  ]);
  const { prev, next } = neighbours(book.slug, toc, chapter.slug, section.slug);
  const dek = section.dek || firstParagraph(section.body);

  return (
    <>
      <Topbar
        crumbs={[book.title, chapter.title, section.title]}
        prev={prev?.href}
        next={next?.href}
        ask
      />

      <article className="lesson">
        <header className="lesson-head">
          <p className="meta">{chapter.title}</p>
          <h1>{section.title}</h1>
          {dek ? <p className="dek">{dek}</p> : null}
        </header>
        <p className="rule">§ § §</p>

        {rendered.headings.length > 2 ? (
          <nav className="page-toc">
            <h2>
              <List size={12} strokeWidth={1.9} /> On this page
            </h2>
            <ul>
              {rendered.headings.map((h) => (
                <li key={h.id} className={h.depth === 3 ? "lvl3" : undefined}>
                  <a href={`#${h.id}`}>{h.text}</a>
                </li>
              ))}
            </ul>
          </nav>
        ) : null}

        {/* Server-rendered from the section's Markdown: KaTeX is already static HTML,
            Mermaid sources are still plain text for the client runtime to draw. */}
        <div dangerouslySetInnerHTML={{ __html: rendered.html }} />

        <footer className="lesson-foot">
          <div className="pager">
            {prev ? (
              <Link href={prev.href} className="prev">
                <ChevronLeft size={15} strokeWidth={1.7} className="icon" />
                <span>
                  <em>Previous</em>
                  {prev.title}
                </span>
              </Link>
            ) : null}
            {next ? (
              <Link href={next.href} className="next">
                <span>
                  <em>Next</em>
                  {next.title}
                </span>
                <ChevronRight size={15} strokeWidth={1.7} className="icon" />
              </Link>
            ) : null}
          </div>
        </footer>
      </article>

      <Ruler headings={rendered.headings} />
      <PageRuntime hasDiagrams={rendered.diagrams > 0} />
    </>
  );
}
