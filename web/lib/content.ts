import "server-only";
import { sql, type Book, type Chapter, type Section } from "./db";

export type TocSection = { slug: string; title: string; position: number };
export type TocChapter = { slug: string; title: string; position: number; sections: TocSection[] };
export type Toc = TocChapter[];

/** Every book on the shelf, in shelf order. */
export async function listBooks(includeDrafts = false): Promise<Book[]> {
  return sql<Book[]>`
    select * from books
     where deleted_at is null
    ${includeDrafts ? sql`` : sql`and published`}
     order by position, id
  `;
}

export async function getBook(slug: string): Promise<Book | null> {
  const [book] = await sql<Book[]>`select * from books where slug = ${slug} and deleted_at is null limit 1`;
  return book ?? null;
}

export async function getBookById(id: number): Promise<Book | null> {
  const [book] = await sql<Book[]>`select * from books where id = ${id} limit 1`;
  return book ?? null;
}

/**
 * The whole navigation tree for one book in a single round trip. The reading pages all
 * render the same sidebar, so fetching it per page and letting the route cache hold it
 * beats stitching separate chapter and section queries together.
 */
export async function getToc(bookId: number): Promise<Toc> {
  const rows = await sql<
    {
      ch_slug: string;
      ch_title: string;
      ch_pos: number;
      s_slug: string | null;
      s_title: string | null;
      s_pos: number | null;
    }[]
  >`
    select c.slug as ch_slug, c.title as ch_title, c.position as ch_pos,
           s.slug as s_slug, s.title as s_title, s.position as s_pos
      from chapters c
      left join sections s on s.chapter_id = c.id and s.deleted_at is null
     where c.book_id = ${bookId} and c.deleted_at is null
     order by c.position, c.id, s.position, s.id
  `;

  const toc: Toc = [];
  for (const r of rows) {
    let chapter = toc[toc.length - 1];
    if (!chapter || chapter.slug !== r.ch_slug) {
      chapter = { slug: r.ch_slug, title: r.ch_title, position: r.ch_pos, sections: [] };
      toc.push(chapter);
    }
    if (r.s_slug) {
      chapter.sections.push({ slug: r.s_slug, title: r.s_title!, position: r.s_pos! });
    }
  }
  return toc;
}

export type Page = {
  book: Book;
  chapter: Chapter;
  section: Section;
};

export async function getPage(
  bookSlug: string,
  chapterSlug: string,
  sectionSlug: string,
): Promise<Page | null> {
  const [row] = await sql<
    ({ book: Book; chapter: Chapter; section: Section } & Record<string, unknown>)[]
  >`
    select to_jsonb(b) as book, to_jsonb(c) as chapter, to_jsonb(s) as section
      from sections s
      join chapters c on c.id = s.chapter_id
      join books b on b.id = c.book_id
     where b.slug = ${bookSlug} and c.slug = ${chapterSlug} and s.slug = ${sectionSlug}
       and b.deleted_at is null and c.deleted_at is null and s.deleted_at is null
     limit 1
  `;
  return row ? { book: row.book, chapter: row.chapter, section: row.section } : null;
}

export type Neighbour = { href: string; title: string; chapter: string } | null;

/** Previous and next page in reading order, crossing chapter boundaries. */
export function neighbours(
  bookSlug: string,
  toc: Toc,
  chapterSlug: string,
  sectionSlug: string,
): { prev: Neighbour; next: Neighbour } {
  const flat = toc.flatMap((c) =>
    c.sections.map((s) => ({
      href: `/${bookSlug}/${c.slug}/${s.slug}`,
      title: s.title,
      chapter: c.title,
      key: `${c.slug}/${s.slug}`,
    })),
  );
  const i = flat.findIndex((p) => p.key === `${chapterSlug}/${sectionSlug}`);
  return {
    prev: i > 0 ? flat[i - 1] : null,
    next: i >= 0 && i < flat.length - 1 ? flat[i + 1] : null,
  };
}

/** Every reading page in the store — used to pre-render the whole site at build time. */
export async function allPagePaths(): Promise<
  { book: string; chapter: string; section: string }[]
> {
  return sql<{ book: string; chapter: string; section: string }[]>`
    select b.slug as book, c.slug as chapter, s.slug as section
      from sections s
      join chapters c on c.id = s.chapter_id
      join books b on b.id = c.book_id
     where b.published and b.deleted_at is null
       and c.deleted_at is null and s.deleted_at is null
     order by b.position, c.position, s.position
  `;
}

export type BookStats = { chapters: number; sections: number; words: number };

export async function getStats(bookId: number): Promise<BookStats> {
  const [row] = await sql<{ chapters: number; sections: number; words: number }[]>`
    select count(distinct c.id)::int as chapters,
           count(s.id)::int as sections,
           coalesce(sum(array_length(regexp_split_to_array(trim(s.body), '\\s+'), 1)), 0)::int as words
      from chapters c
      left join sections s on s.chapter_id = c.id and s.deleted_at is null
     where c.book_id = ${bookId} and c.deleted_at is null
  `;
  return row ?? { chapters: 0, sections: 0, words: 0 };
}

export type Hit = {
  book: string;
  book_title: string;
  chapter: string;
  chapter_title: string;
  section: string;
  title: string;
  snippet: string;
};

export async function search(query: string, bookSlug?: string, limit = 30): Promise<Hit[]> {
  const q = query.trim();
  if (!q) return [];
  return sql<Hit[]>`
    select b.slug as book, b.title as book_title,
           c.slug as chapter, c.title as chapter_title,
           s.slug as section, s.title,
           ts_headline('english', s.body, websearch_to_tsquery('english', ${q}),
             'MaxWords=28, MinWords=12, ShortWord=3, MaxFragments=1, StartSel=<mark>, StopSel=</mark>')
             as snippet
      from sections s
      join chapters c on c.id = s.chapter_id
      join books b on b.id = c.book_id
     where b.published and b.deleted_at is null
       and c.deleted_at is null and s.deleted_at is null
       and s.search @@ websearch_to_tsquery('english', ${q})
       ${bookSlug ? sql`and b.slug = ${bookSlug}` : sql``}
     order by ts_rank(s.search, websearch_to_tsquery('english', ${q})) desc
     limit ${limit}
  `;
}
