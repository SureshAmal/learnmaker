/**
 * Applies lib/schema.sql. Every statement is `if not exists`, so running it again on a
 * live database is a no-op — that is what makes it safe to wire into a deploy step.
 */
import { readFileSync } from "node:fs";
import { join } from "node:path";
import postgres from "postgres";

const url = process.env.DATABASE_URL;
if (!url) {
  console.error("DATABASE_URL is not set. Put it in web/.env.local first.");
  process.exit(1);
}

const sql = postgres(url, {
  ssl: url.includes("localhost") || url.includes("127.0.0.1") ? false : "require",
  max: 1,
});

const schema = readFileSync(join(process.cwd(), "lib/schema.sql"), "utf8");

await sql.unsafe(schema);
console.log("schema applied");
await sql.end();
