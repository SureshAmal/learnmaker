import { NextResponse } from "next/server";
import { markdownToBlocks, roundTrips } from "@/lib/blocks-parse";
import { requireAdmin } from "@/lib/auth";

export const dynamic = "force-dynamic";

/**
 * Converts a page's Markdown into blocks for the visual editor, and says whether the
 * conversion is safe. Called once when the editor opens — the other direction is pure
 * string work and runs in the browser.
 */
export async function POST(request: Request) {
  await requireAdmin();
  const { markdown } = (await request.json()) as { markdown?: string };
  const source = markdown ?? "";

  return NextResponse.json({
    blocks: markdownToBlocks(source),
    safe: roundTrips(source),
  });
}
