import "server-only";
import { sql } from "./db";

/**
 * Retrieval for the Ask panel: BM25 over the book, returning short focused excerpts
 * rather than whole sections.
 *
 * Postgres full-text search is used to find candidates — it is indexed and fast — but
 * `ts_rank` is a coverage score, not a relevance model: it does not know that a word
 * appearing in three sections is worth more than one appearing in three hundred, and it
 * does not discount long sections that match simply by being long. BM25 does both, so
 * the candidates are re-scored here before the best few are handed over.
 *
 * The excerpt sent back is a window around the densest run of query terms, not the top
 * of the section, which is what keeps the prompt small: a few hundred characters that
 * bear on the question instead of two thousand that mostly do not.
 */

const K1 = 1.2; // term-frequency saturation
const B = 0.75; // length normalisation

const STOPWORDS = new Set([
  "what", "why", "when", "which", "where", "does", "doing", "with", "from", "that",
  "this", "there", "then", "than", "about", "into", "over", "under", "between", "have",
  "has", "had", "the", "and", "for", "are", "was", "were", "will", "would", "should",
  "could", "work", "works", "used", "use", "using", "explain", "tell", "show", "how",
  "who", "whom", "its", "it", "a", "an", "of", "to", "in", "on", "is", "be", "by", "or",
  "at", "as", "do", "did", "can", "may", "might", "must", "not", "but", "if", "so",
]);

export type Passage = {
  book: string;
  book_title: string;
  chapter: string;
  chapter_title: string;
  section: string;
  title: string;
  excerpt: string;
  score: number;
};

export function terms(question: string): string[] {
  return [
    ...new Set(
      question
        .toLowerCase()
        .replace(/[^a-z0-9\s]/g, " ")
        .split(/\s+/)
        .filter((w) => w.length > 2 && !STOPWORDS.has(w)),
    ),
  ].slice(0, 12);
}

/** Words as BM25 counts them: lowercase, punctuation stripped. */
function tokenise(text: string): string[] {
  return text.toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/).filter(Boolean);
}

/**
 * The window of prose where the query's *informative* terms cluster.
 *
 * Weighting by idf matters more than it sounds: for "why does the learning rate matter
 * in gradient descent", the words "gradient" and "descent" are everywhere in the section
 * about gradient descent, so an unweighted window lands on whichever paragraph repeats
 * them most and misses the two rare words that carry the question. Scoring the window by
 * idf puts "learning rate" ahead of its own topic's name.
 */
function excerpt(body: string, weights: Map<string, number>, width: number): string {
  const clean = body
    .replace(/```[\s\S]*?```/g, " [code sample] ")
    .replace(/!\[[^\]]*\]\([^)]*\)/g, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/[#*_>|]/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  if (clean.length <= width) return clean;

  const words = clean.split(" ");
  const keys: (string | null)[] = words.map((w) => {
    const key = w.toLowerCase().replace(/[^a-z0-9]/g, "");
    return weights.has(key) ? key : null;
  });

  // Each term saturates after a couple of occurrences, exactly as it does in BM25.
  // Without that, a section repeating its own title word twenty times beats the one
  // paragraph that actually answers the question.
  const CAP = 2;
  const span = Math.max(20, Math.round(width / 6));
  const counts = new Map<string, number>();

  const score = () => {
    let total = 0;
    for (const [term, n] of counts) total += (weights.get(term) ?? 0) * Math.min(n, CAP);
    return total;
  };

  const add = (i: number) => {
    const key = keys[i];
    if (key) counts.set(key, (counts.get(key) ?? 0) + 1);
  };
  const drop = (i: number) => {
    const key = keys[i];
    if (!key) return;
    const n = (counts.get(key) ?? 1) - 1;
    if (n > 0) counts.set(key, n);
    else counts.delete(key);
  };

  for (let i = 0; i < Math.min(span, words.length); i++) add(i);
  let best = score();
  let bestAt = 0;

  for (let i = span; i < words.length; i++) {
    add(i);
    drop(i - span);
    const now = score();
    if (now > best) {
      best = now;
      bestAt = i - span + 1;
    }
  }

  const text = words.slice(bestAt, bestAt + span).join(" ");
  return (bestAt > 0 ? "… " : "") + text + (bestAt + span < words.length ? " …" : "");
}

/**
 * Candidates from the index, re-scored with BM25.
 *
 * `width` is the size of each excerpt in characters — the single biggest lever on how
 * much a model has to read.
 */
export async function findPassages(
  question: string,
  book?: string,
  { limit = 4, width = 700, candidates = 40 } = {},
): Promise<Passage[]> {
  const words = terms(question);
  if (!words.length) return [];

  // Any of the words, so a question phrased differently from the page still finds it.
  const query = words.join(" | ");

  const rows = await sql<
    {
      book: string; book_title: string; chapter: string; chapter_title: string;
      section: string; title: string; body: string;
    }[]
  >`
    select b.slug as book, b.title as book_title,
           c.slug as chapter, c.title as chapter_title,
           s.slug as section, s.title, s.body
      from sections s
      join chapters c on c.id = s.chapter_id
      join books b on b.id = c.book_id
     where b.published and b.deleted_at is null
       and c.deleted_at is null and s.deleted_at is null
       and s.search @@ to_tsquery('english', ${query})
       ${book ? sql`and b.slug = ${book}` : sql``}
     order by ts_rank(s.search, to_tsquery('english', ${query})) desc
     limit ${candidates}
  `;
  if (!rows.length) return [];

  // Document frequency for each term across the whole corpus, and the corpus size —
  // BM25 needs both to know which words are worth anything.
  const [stats] = await sql<{ total: number; avglen: number }[]>`
    select count(*)::int as total,
           coalesce(avg(array_length(regexp_split_to_array(trim(body), '\\s+'), 1)), 1) as avglen
      from sections s
      join chapters c on c.id = s.chapter_id
      join books b on b.id = c.book_id
     where b.published and b.deleted_at is null
       and c.deleted_at is null and s.deleted_at is null
       ${book ? sql`and b.slug = ${book}` : sql``}
  `;

  const dfRows = await sql<{ term: string; df: number }[]>`
    select t.term, (
      select count(*)::int
        from sections s
        join chapters c on c.id = s.chapter_id
        join books b on b.id = c.book_id
       where b.published and b.deleted_at is null
         and c.deleted_at is null and s.deleted_at is null
         and s.search @@ plainto_tsquery('english', t.term)
         ${book ? sql`and b.slug = ${book}` : sql``}
    ) as df
    from unnest(${words}::text[]) as t(term)
  `;

  const total = Math.max(1, stats?.total ?? 1);
  const avglen = Math.max(1, Number(stats?.avglen ?? 1));
  const idf = new Map(
    dfRows.map((r) => {
      const df = Math.min(r.df, total);
      // Standard BM25 idf, floored so a term in every section cannot go negative.
      return [r.term, Math.max(0.01, Math.log(1 + (total - df + 0.5) / (df + 0.5)))];
    }),
  );

  const scored = rows.map((row) => {
    const tokens = tokenise(`${row.title} ${row.title} ${row.body}`); // the title counts twice
    const length = tokens.length || 1;

    const counts = new Map<string, number>();
    for (const token of tokens) {
      if (idf.has(token)) counts.set(token, (counts.get(token) ?? 0) + 1);
    }

    let score = 0;
    for (const [term, tf] of counts) {
      const weight = idf.get(term) ?? 0.01;
      score += (weight * (tf * (K1 + 1))) / (tf + K1 * (1 - B + (B * length) / avglen));
    }

    return {
      book: row.book,
      book_title: row.book_title,
      chapter: row.chapter,
      chapter_title: row.chapter_title,
      section: row.section,
      title: row.title,
      excerpt: excerpt(row.body, idf, width),
      score: Number(score.toFixed(3)),
    };
  });

  return scored.sort((a, b) => b.score - a.score).slice(0, limit);
}

/** One section in full, for when an excerpt was not enough. */
export async function readSection(path: string, max = 6000) {
  const [book, chapter, section] = path.replace(/^\//, "").split("/");
  if (!book || !chapter || !section) return null;

  const [row] = await sql<{ title: string; chapter_title: string; body: string }[]>`
    select s.title, c.title as chapter_title, s.body
      from sections s
      join chapters c on c.id = s.chapter_id
      join books b on b.id = c.book_id
     where b.slug = ${book} and c.slug = ${chapter} and s.slug = ${section}
       and b.published and b.deleted_at is null
       and c.deleted_at is null and s.deleted_at is null
  `;
  if (!row) return null;

  return {
    title: row.title,
    chapter: row.chapter_title,
    text: row.body.replace(/\s+/g, " ").trim().slice(0, max),
  };
}
