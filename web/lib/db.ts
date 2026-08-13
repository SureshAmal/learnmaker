import postgres from "postgres";

declare global {
  // eslint-disable-next-line no-var
  var __sql: ReturnType<typeof postgres> | undefined;
}

function connect() {
  const url = process.env.DATABASE_URL;
  if (!url) throw new Error("DATABASE_URL is not set");
  return postgres(url, {
    ssl: url.includes("localhost") || url.includes("127.0.0.1") ? false : "require",
    // Serverless functions are short-lived and many run at once, so each one keeps a
    // single connection rather than a pool the platform would have to tear down.
    max: process.env.VERCEL ? 1 : 10,
    idle_timeout: 20,
    connect_timeout: 15,
  });
}

// Next's dev server reloads modules on every edit; without the global the old sockets
// are never closed and Postgres runs out of connections after a few saves.
export const sql = global.__sql ?? connect();
if (process.env.NODE_ENV !== "production") global.__sql = sql;

export type Book = {
  id: number;
  slug: string;
  title: string;
  subtitle: string;
  blurb: string;
  source_url: string;
  license: string;
  position: number;
  published: boolean;
};

export type Chapter = {
  id: number;
  book_id: number;
  slug: string;
  title: string;
  position: number;
};

export type Section = {
  id: number;
  chapter_id: number;
  slug: string;
  title: string;
  dek: string;
  body: string;
  position: number;
};
