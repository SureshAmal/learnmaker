/** URL-safe slug. Kept deliberately plain: these end up in reader-visible paths. */
export function slugify(input: string, fallback = "untitled"): string {
  const slug = input
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
  return slug || fallback;
}

/**
 * Slugs that would shadow a real route. `/admin/edit/<book>/settings` and
 * `/admin/edit/<book>/<chapter>/settings` are static segments, so a chapter or section
 * actually called "settings" would be unreachable in the editor.
 */
const RESERVED = new Set(["settings"]);

/** `chapter-1`, then `chapter-1-2`, `chapter-1-3`… when the first is taken. */
export function uniqueSlug(base: string, taken: Iterable<string>): string {
  const used = new Set([...taken, ...RESERVED]);
  if (!used.has(base)) return base;
  for (let n = 2; ; n++) {
    const candidate = `${base}-${n}`;
    if (!used.has(candidate)) return candidate;
  }
}
