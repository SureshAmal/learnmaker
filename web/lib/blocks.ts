/**
 * Markdown ↔ Editor.js blocks.
 *
 * Markdown stays the source of truth: it is what the database holds, what the renderer
 * reads and what a diff shows. The block editor is a view onto it, so both directions
 * have to survive a round trip without quietly rewriting an author's page.
 *
 * Anything the block model has no honest representation for — display maths, a Mermaid
 * fence, raw HTML — is carried verbatim in a `raw` block rather than approximated. The
 * editor shows those as a plain source box, and they come back out byte-identical.
 *
 * `blocksToMarkdown` is pure string work and runs in the browser on every keystroke.
 * `markdownToBlocks` needs the Markdown parser, so it runs on the server and is only
 * called when the visual editor opens.
 */

export type Inline = string;

export type Block =
  | { type: "paragraph"; data: { text: Inline } }
  | { type: "header"; data: { text: Inline; level: number } }
  | { type: "list"; data: { style: "ordered" | "unordered"; items: ListItem[] } }
  | { type: "checklist"; data: { items: { text: Inline; checked: boolean }[] } }
  | { type: "quote"; data: { text: Inline; caption: string } }
  | { type: "fenced"; data: { code: string; language: string } }
  | { type: "table"; data: { withHeadings: boolean; content: string[][] } }
  | { type: "image"; data: { file: { url: string }; caption: string } }
  | { type: "delimiter"; data: Record<string, never> }
  | { type: "raw"; data: { html: string } };

export type ListItem = { content: Inline; items: ListItem[] };

// ---------------------------------------------------------------------------------
// blocks → markdown
// ---------------------------------------------------------------------------------

/** The inline HTML Editor.js produces, back to Markdown. */
export function inlineToMarkdown(html: string): string {
  let text = html;

  // <br> is the only structural tag inside a block; everything else is a span style.
  text = text.replace(/<br\s*\/?>/gi, "  \n");
  text = text.replace(/<\/?(?:b|strong)>/gi, "**");
  text = text.replace(/<\/?(?:i|em)>/gi, "_");
  text = text.replace(/<\/?(?:s|del|strike)>/gi, "~~");
  text = text.replace(/<\/?mark[^>]*>/gi, "==");
  // Inline code is lifted out before any tag stripping: its contents are literal, and
  // something like `<<SYS>>` would otherwise be mistaken for markup and deleted.
  const codes: string[] = [];
  text = text.replace(/<code[^>]*>([\s\S]*?)<\/code>/gi, (_m, code: string) => {
    const inner = decode(String(code));
    // A backtick inside inline code needs a longer fence around it.
    const fence = "`".repeat(Math.max(1, longestRun(inner, "`") + 1));
    codes.push(`${fence}${inner}${fence}`);
    return `\u0000CODE${codes.length - 1}\u0000`;
  });
  text = text.replace(
    /<a[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi,
    (_m, href: string, label: string) => `[${label}](${href})`,
  );

  // Anything else the editor let through is not ours to interpret; drop the tags rather
  // than leak markup into the Markdown.
  text = text.replace(/<[^>]+>/g, "");
  text = decode(text);
  text = text.replace(/\u0000CODE(\d+)\u0000/g, (_m, i: string) => codes[Number(i)]);
  return text.trim();
}

function longestRun(text: string, char: string) {
  let best = 0;
  let run = 0;
  for (const c of text) {
    run = c === char ? run + 1 : 0;
    if (run > best) best = run;
  }
  return best;
}

function decode(text: string) {
  return text
    .replace(/&nbsp;/g, " ")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, "&");
}

function listToMarkdown(items: ListItem[], ordered: boolean, depth = 0): string {
  return items
    .map((item, i) => {
      const bullet = ordered ? `${i + 1}.` : "-";
      const pad = "  ".repeat(depth);
      const head = `${pad}${bullet} ${inlineToMarkdown(item.content)}`;
      const nested = item.items?.length
        ? "\n" + listToMarkdown(item.items, ordered, depth + 1)
        : "";
      return head + nested;
    })
    .join("\n");
}

export function blocksToMarkdown(blocks: Block[]): string {
  const out: string[] = [];

  for (const block of blocks) {
    switch (block.type) {
      case "header":
        out.push(`${"#".repeat(Math.min(6, Math.max(1, block.data.level)))} ${inlineToMarkdown(block.data.text)}`);
        break;

      case "paragraph":
        out.push(inlineToMarkdown(block.data.text));
        break;

      case "list":
        out.push(listToMarkdown(block.data.items ?? [], block.data.style === "ordered"));
        break;

      case "checklist":
        out.push(
          (block.data.items ?? [])
            .map((item) => `- [${item.checked ? "x" : " "}] ${inlineToMarkdown(item.text)}`)
            .join("\n"),
        );
        break;

      case "quote": {
        const body = inlineToMarkdown(block.data.text)
          .split("\n")
          .map((line) => `> ${line}`)
          .join("\n");
        out.push(block.data.caption ? `${body}\n>\n> — ${inlineToMarkdown(block.data.caption)}` : body);
        break;
      }

      case "fenced": {
        const code = block.data.code ?? "";
        // Only a run of backticks at the start of a line can close the block early, so
        // only those force a wider fence — a stray ``` mid-line is harmless.
        const closing = code
          .split("\n")
          .map((line) => line.match(/^\s*(`{3,})/)?.[1].length ?? 0)
          .reduce((a, b) => Math.max(a, b), 0);
        const fence = "`".repeat(Math.max(3, closing + 1));
        out.push(`${fence}${block.data.language ?? ""}\n${code}\n${fence}`);
        break;
      }

      case "table": {
        const rows = block.data.content ?? [];
        if (!rows.length) break;
        const cells = (row: string[]) =>
          `| ${row.map((c) => inlineToMarkdown(c).replace(/\|/g, "\\|")).join(" | ")} |`;
        const width = rows[0].length;
        // Markdown tables always carry a header row; a table without headings gets an
        // empty one so the shape survives.
        const [first, ...rest] = block.data.withHeadings ? rows : [Array(width).fill(""), ...rows];
        out.push([cells(first), `| ${Array(width).fill("---").join(" | ")} |`, ...rest.map(cells)].join("\n"));
        break;
      }

      case "image": {
        const caption = (block.data.caption ?? "").replace(/([[\]])/g, "\\$1");
        out.push(`![${inlineToMarkdown(caption)}](${block.data.file?.url ?? ""})`);
        break;
      }

      case "delimiter":
        out.push("---");
        break;

      case "raw":
        out.push(block.data.html ?? "");
        break;
    }
  }

  return out.filter((part) => part.trim()).join("\n\n") + "\n";
}
