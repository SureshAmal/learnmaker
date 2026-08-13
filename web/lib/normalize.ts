/**
 * Repairs code fences whose opening and closing lines disagree about indentation.
 *
 * Microsoft's docs contain blocks like this, indented into a list item on the way in but
 * not on the way out:
 *
 *     1. Declare a method:
 *
 *         ```csharp
 *     public override string ToString(){}
 *     ```
 *
 * CommonMark reads that as a fence that never closes inside the list item: the body
 * leaks out as prose and the stray ``` shows up as literal text. The old Python build
 * used a lenient parser and got away with it; remark, correctly, does not.
 *
 * The repair indents the body and the closing fence to match the opening fence, which
 * keeps the block inside its list item and leaves the code's own relative indentation
 * intact. Well-formed fences are returned untouched.
 */
const FENCE = /^(\s*)(`{3,}|~{3,})(.*)$/;

/**
 * The Python build wrote its own `#` anchor links into every heading. This renderer
 * generates those itself from the heading id, so the ones in the source are duplicates —
 * and, being raw HTML inside a heading, they are the single biggest reason a page cannot
 * be opened in the block editor. Stripping them loses nothing a reader sees.
 */
const HEADING_ANCHOR = /\s*<a class="anchor"[^>]*>#<\/a>\s*$/gm;

export function stripHeadingAnchors(markdown: string): string {
  return markdown.replace(HEADING_ANCHOR, "");
}

export function normalizeFences(markdown: string): string {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const out: string[] = [];

  for (let i = 0; i < lines.length; i++) {
    const open = lines[i].match(FENCE);
    if (!open) {
      out.push(lines[i]);
      continue;
    }

    const [, indent, marker] = open;
    // An info string containing the marker character would not be an opening fence.
    if (open[3].includes(marker[0])) {
      out.push(lines[i]);
      continue;
    }

    // Find the closing fence: same character, at least as long, nothing else on the line.
    let close = -1;
    for (let j = i + 1; j < lines.length; j++) {
      const m = lines[j].match(FENCE);
      if (m && m[2][0] === marker[0] && m[2].length >= marker.length && !m[3].trim()) {
        close = j;
        break;
      }
    }

    if (close === -1) {
      // Unterminated: leave it exactly as written rather than guessing where it ends.
      out.push(lines[i]);
      continue;
    }

    const body = lines.slice(i + 1, close);
    const closeIndent = lines[close].match(FENCE)![1];

    if (indent.length === 0 || closeIndent.length >= indent.length) {
      // Already consistent.
      out.push(lines[i], ...body, lines[close]);
    } else {
      const shortest = body
        .filter((line) => line.trim())
        .reduce((min, line) => Math.min(min, line.match(/^ */)![0].length), Infinity);
      const pad = " ".repeat(Math.max(0, indent.length - (Number.isFinite(shortest) ? shortest : 0)));
      out.push(
        lines[i],
        ...body.map((line) => (line.trim() ? pad + line : line)),
        indent + lines[close].trim(),
      );
    }

    i = close;
  }

  return out.join("\n");
}
