import { notFound } from "next/navigation";
import { getBook, getToc } from "@/lib/content";
import Sidebar from "@/components/Sidebar";
import SearchPalette from "@/components/SearchPalette";
import AskPanel from "@/components/AskPanel";

export const revalidate = 86400;

/**
 * The chrome every page of a book shares. Fetching the table of contents here rather
 * than in each page means one query per navigation instead of one per component, and
 * the sidebar keeps its scroll position across a client-side move.
 */
export default async function BookLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ book: string }>;
}) {
  const { book: bookSlug } = await params;
  const book = await getBook(bookSlug);
  if (!book || !book.published) notFound();

  const toc = await getToc(book.id);

  return (
    <>
      <Sidebar
        bookSlug={book.slug}
        bookTitle={book.title}
        toc={toc}
        note={book.license ? `Source material: ${book.license}` : undefined}
      />
      <SearchPalette bookSlug={book.slug} />
      <AskPanel bookSlug={book.slug} />
      <main className="paper">{children}</main>
    </>
  );
}
