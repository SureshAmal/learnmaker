import { NextResponse } from "next/server";
import { search } from "@/lib/content";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const q = url.searchParams.get("q") ?? "";
  const book = url.searchParams.get("book") ?? undefined;
  if (!q.trim()) return NextResponse.json({ hits: [] });

  try {
    const hits = await search(q, book);
    return NextResponse.json({ hits });
  } catch {
    // A malformed query (a lone operator, say) makes websearch_to_tsquery unhappy; an
    // empty result reads better to someone mid-keystroke than a red error does.
    return NextResponse.json({ hits: [] });
  }
}
