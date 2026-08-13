import "server-only";
import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import type { Root, RootContent, PhrasingContent, ListItem as MdListItem } from "mdast";
import { blocksToMarkdown, type Block, type ListItem } from "./blocks";

/**
 * Markdown → Editor.js blocks, plus the check that makes the visual editor safe to open.
 *
 * Constructs the block model cannot hold — display maths, Mermaid fences, raw HTML —
 * become `raw` blocks carrying their exact source, so they survive editing untouched.
 */

function escapeHtml(text: string) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/**
 * mdast phrasing → the small HTML vocabulary Editor.js edits inline.
 *
 * `src` is the page's Markdown. Maths is reproduced by slicing it rather than rebuilt
 * from the parsed value, because `$$x$$` written inside a paragraph parses as an inline
 * node and rebuilding it would emit `$x$` — silently turning display maths into inline.
 */
function inline(nodes: PhrasingContent[], src: string): string {
  return nodes
    .map((node): string => {
      switch (node.type) {
        case "text":
          return escapeHtml(node.value);
        case "strong":
          return `<b>${inline(node.children, src)}</b>`;
        case "emphasis":
          return `<i>${inline(node.children, src)}</i>`;
        case "delete":
          return `<s>${inline(node.children, src)}</s>`;
        case "inlineCode":
          return `<code class="inline-code">${escapeHtml(node.value)}</code>`;
        case "link":
          return `<a href="${escapeHtml(node.url)}">${inline(node.children, src)}</a>`;
        case "break":
          return "<br>";
        case "image":
          return `<img src="${escapeHtml(node.url)}" alt="${escapeHtml(node.alt ?? "")}">`;
        case "inlineMath": {
          // Exactly as written — single or double dollars, escapes and all.
          const start = node.position?.start.offset;
          const end = node.position?.end.offset;
          return escapeHtml(
            start !== undefined && end !== undefined
              ? src.slice(start, end)
              : `$${(node as unknown as { value: string }).value}$`,
          );
        }
        case "html":
          return node.value;
        default:
          return "children" in node ? inline(node.children as PhrasingContent[], src) : "";
      }
    })
    .join("");
}

/**
 * Whether a list is the plain shape the block editor can hold: each item is one
 * paragraph, optionally followed by a nested list. Loose lists — an item carrying two
 * paragraphs, a code sample, a quote — are kept as source instead of being flattened.
 */
function simpleList(items: MdListItem[], ordered: boolean): boolean {
  return items.every((item) => {
    const [first, ...rest] = item.children;
    if (first?.type !== "paragraph") return false;
    if (first.children.some((child) => child.type === "html")) return false;
    if (rest.length === 0) return true;
    if (rest.length > 1) return false;
    if (rest[0].type !== "list") return false;
    // A nested list takes its parent's marker in the block model, so a bulleted list
    // inside a numbered one cannot be represented without changing it.
    if (Boolean(rest[0].ordered) !== ordered) return false;
    return simpleList(rest[0].children, ordered);
  });
}

function listItems(items: MdListItem[], src: string): ListItem[] {
  return items.map((item) => {
    const [first, ...rest] = item.children;
    const content = first?.type === "paragraph" ? inline(first.children, src) : "";
    const nested = rest.find((child) => child.type === "list");
    return {
      content,
      items: nested && nested.type === "list" ? listItems(nested.children, src) : [],
    };
  });
}

/** The source text a node came from — used to keep unmappable nodes byte-exact. */
function source(markdown: string, node: RootContent): string {
  const start = node.position?.start.offset;
  const end = node.position?.end.offset;
  return start !== undefined && end !== undefined ? markdown.slice(start, end) : "";
}

export function markdownToBlocks(markdown: string): Block[] {
  // The maths extension matters here even though nothing renders maths: without it a
  // $$...$$ block is read as prose, and LaTeX escapes like \, and \( are stripped as if
  // they were Markdown escapes. With it, the whole block is one node and is kept verbatim.
  const tree = unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkMath)
    .parse(markdown) as Root;
  const blocks: Block[] = [];

  for (const node of tree.children) {
    switch (node.type) {
      case "heading":
        if (node.children.some((child) => child.type === "html")) {
          blocks.push({ type: "raw", data: { html: source(markdown, node) } });
          break;
        }
        blocks.push({
          type: "header",
          data: { text: inline(node.children, markdown), level: node.depth },
        });
        break;

      case "paragraph": {
        // A paragraph holding only an image is a figure, and gets the image block so it
        // can be moved, replaced and captioned like one.
        const meaningful = node.children.filter(
          (child) => child.type !== "text" || child.value.trim() !== "",
        );
        if (meaningful.length === 1 && meaningful[0].type === "image") {
          const image = meaningful[0];
          blocks.push({
            type: "image",
            data: { file: { url: image.url }, caption: image.alt ?? "" },
          });
          break;
        }
        // Any paragraph carrying raw HTML keeps its source exactly: the inline model
        // would turn the tags into Markdown and change what the page renders.
        if (node.children.some((child) => child.type === "html")) {
          blocks.push({ type: "raw", data: { html: source(markdown, node) } });
          break;
        }
        blocks.push({ type: "paragraph", data: { text: inline(node.children, markdown) } });
        break;
      }

      case "list": {
        const isTask = node.children.some((item) => typeof item.checked === "boolean");
        if (isTask) {
          blocks.push({
            type: "checklist",
            data: {
              items: node.children.map((item) => {
                const [first] = item.children;
                return {
                  text: first?.type === "paragraph" ? inline(first.children, markdown) : "",
                  checked: item.checked === true,
                };
              }),
            },
          });
          break;
        }
        if (!simpleList(node.children, Boolean(node.ordered))) {
          blocks.push({ type: "raw", data: { html: source(markdown, node) } });
          break;
        }
        blocks.push({
          type: "list",
          data: {
            style: node.ordered ? "ordered" : "unordered",
            items: listItems(node.children, markdown),
          },
        });
        break;
      }

      case "blockquote": {
        // Callouts, admonitions and quotes containing lists or code carry structure the
        // quote block cannot hold, so only the simplest case is converted.
        const simple =
          node.children.length === 1 &&
          node.children[0].type === "paragraph" &&
          !node.children[0].children.some((child) => child.type === "html");
        if (!simple) {
          blocks.push({ type: "raw", data: { html: source(markdown, node) } });
          break;
        }
        const [paragraph] = node.children;
        blocks.push({
          type: "quote",
          data: {
            text: inline((paragraph as { children: PhrasingContent[] }).children, markdown),
            caption: "",
          },
        });
        break;
      }

      case "code":
        blocks.push({
          type: "fenced",
          // The info string can carry more than a language — "```python out" marks
          // expected output in the LLM book — and all of it has to come back.
          data: {
            code: node.value,
            language: [node.lang, node.meta].filter(Boolean).join(" "),
          },
        });
        break;

      case "table": {
        const ragged = new Set(node.children.map((row) => row.children.length)).size > 1;
        const aligned = (node.align ?? []).some((a) => a !== null && a !== undefined);
        const hasHtml = node.children.some((row) =>
          row.children.some((cell) => cell.children.some((child) => child.type === "html")),
        );
        if (ragged || hasHtml || aligned) {
          blocks.push({ type: "raw", data: { html: source(markdown, node) } });
          break;
        }
        const content = node.children.map((row) =>
          row.children.map((cell) => inline(cell.children, markdown)),
        );
        blocks.push({ type: "table", data: { withHeadings: true, content } });
        break;
      }

      case "thematicBreak":
        blocks.push({ type: "delimiter", data: {} });
        break;

      default:
        // Raw HTML, display maths, footnote definitions: kept exactly as written.
        blocks.push({ type: "raw", data: { html: source(markdown, node) } });
    }
  }

  return blocks;
}

/**
 * Exported so the round-trip audit can report *why* a page was refused.
 *
 * Whitespace, escaping and the choice of Markdown punctuation differ harmlessly between
 * the original and a rebuilt document — `*` and `-` are the same bullet, `*a*` and `_a_`
 * the same emphasis. What matters is the words, the structure and the links, so those
 * are what gets compared.
 */
export function normalise(markdown: string) {
  return markdown
    .replace(/\r\n/g, "\n")
    .replace(/[ \t]+$/gm, "")
    // A table's delimiter row may be written |---|, |:--|, or |------------|; they all
    // mean the same table, and cells may or may not be padded around the pipes.
    .replace(/^\|[ \t:|-]+\|$/gm, "|---|")
    .replace(/^(\|.*\|)$/gm, (row) => row.replace(/[ \t]*\|[ \t]*/g, "|"))
    // ATX headings may be closed with trailing hashes, which are not part of the text.
    .replace(/^(#{1,6}[ \t].*?)[ \t]+#+[ \t]*$/gm, "$1")
    .replace(/^[ \t]+/gm, "") // lazy continuation lines carry leading space
    .replace(/[ \t]+$/gm, "")
    .replace(/^[*+-][ \t]+/gm, "- ") // one bullet character
    .replace(/^\d+[.)][ \t]+/gm, "1. ") // lazy "1." numbering is equivalent
    .replace(/\\([[\]*_`~#()<>.!|])/g, "$1") // escaping is a serialiser's choice
    .replace(/[*_~]/g, "") // emphasis punctuation, not emphasis itself
    .replace(/[ \t]{2,}/g, " ")
    .replace(/\n{2,}/g, "\n")
    .trim();
}

/**
 * Whether the block editor can hold this page without changing it. The conversion is run
 * both ways and the result compared with the original; if anything a reader would see
 * differs, the editor refuses the page and the author keeps the Markdown pane. Better a
 * missing feature than a page silently rewritten.
 */
export function roundTrips(markdown: string): boolean {
  try {
    return normalise(blocksToMarkdown(markdownToBlocks(markdown))) === normalise(markdown);
  } catch {
    return false;
  }
}
