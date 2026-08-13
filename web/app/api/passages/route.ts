import { NextResponse } from "next/server";
import { findPassages, readSection } from "@/lib/retrieval";

export const dynamic = "force-dynamic";

/**
 * The book, as two tools a model can call: search it, or read one section of it.
 *
 * No model is called here and no key is held here — the browser drives the conversation
 * with the reader's own credentials and calls this when it decides it needs to look
 * something up. Nothing about the question is recorded.
 */
export async function POST(request: Request) {
  const { tool, query, path, book, limit } = (await request.json()) as {
    tool?: "search" | "read";
    query?: string;
    path?: string;
    book?: string;
    limit?: number;
  };

  if (tool === "read") {
    const section = await readSection(path ?? "");
    return NextResponse.json(section ?? { error: "No such section." });
  }

  const passages = await findPassages(query ?? "", book, {
    limit: Math.min(Math.max(limit ?? 4, 1), 8),
  });

  return NextResponse.json({
    results: passages.map((p) => ({
      path: `/${p.book}/${p.chapter}/${p.section}`,
      title: p.title,
      chapter: p.chapter_title,
      excerpt: p.excerpt,
      score: p.score,
    })),
  });
}
