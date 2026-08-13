import { NextResponse } from "next/server";
import { renderMarkdown } from "@/lib/markdown";
import { requireAdmin } from "@/lib/auth";

export const dynamic = "force-dynamic";

/**
 * The editor's preview renders through the same pipeline as the published page rather
 * than a client-side approximation, so what an author sees is exactly what ships —
 * including Shiki highlighting and KaTeX, neither of which a browser preview would match.
 */
export async function POST(request: Request) {
  await requireAdmin();
  const { markdown } = (await request.json()) as { markdown?: string };
  const rendered = await renderMarkdown(markdown ?? "");
  return NextResponse.json({
    html: rendered.html,
    headings: rendered.headings,
    diagrams: rendered.diagrams,
  });
}
