/**
 * One Markdown pipeline for the whole application: the public reading pages, the admin
 * preview and the search snippets all render through `renderMarkdown`, so what an author
 * sees while typing is byte-for-byte what a reader gets.
 *
 * What a page may contain:
 *   - GitHub Markdown (tables, task lists, strikethrough, footnotes)
 *   - $inline$ and $$display$$ math, rendered to static KaTeX HTML at build time
 *   - ```mermaid fences, handed to the browser as <pre class="mermaid"> and drawn there
 *     (Mermaid needs a DOM to measure text, so it cannot run on the server)
 *   - raw HTML and inline <svg>, kept verbatim for hand-drawn figures and plots
 *   - fenced code in any language, highlighted by Shiki against the app's own palette
 */
import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import remarkRehype from "remark-rehype";
import rehypeRaw from "rehype-raw";
import rehypeSlug from "rehype-slug";
import rehypeKatex from "rehype-katex";
import rehypeStringify from "rehype-stringify";
import { visit } from "unist-util-visit";
import { createHighlighter, type Highlighter } from "shiki";
import type { Root, Element, Text } from "hast";
import type { Root as MdRoot, Code } from "mdast";

export type Heading = { depth: number; id: string; text: string };

export type Rendered = {
  html: string;
  headings: Heading[];
  /** Set when the page needs the client Mermaid runtime. */
  diagrams: number;
  /** Set when the page contains math, so KaTeX CSS is only shipped where it is used. */
  math: boolean;
};

// Shiki loads a WASM engine and a theme bundle; both are expensive and both are pure, so
// one highlighter is built per process and reused across every render.
let highlighterPromise: Promise<Highlighter> | null = null;

const LANGS = [
  "bash", "c", "cpp", "csharp", "css", "diff", "docker", "go", "graphql", "html", "ini",
  "java", "javascript", "json", "jsx", "kotlin", "latex", "lua", "markdown", "php",
  "powershell", "python", "r", "ruby", "rust", "scala", "sql", "swift", "toml", "tsx",
  "typescript", "vb", "xml", "yaml",
];

function highlighter() {
  highlighterPromise ??= createHighlighter({
    themes: ["github-light", "github-dark"],
    langs: LANGS,
  });
  return highlighterPromise;
}

/**
 * Marks fences whose info string says the block is program output — "```python out",
 * which is how the Hugging Face book writes the result of running the sample above.
 *
 * remark keeps that trailing word in `meta` and remark-rehype throws it away, so it is
 * copied onto the element here. Output is not source: it should not be syntax
 * highlighted, and its long lines should wrap rather than be clipped, because nobody
 * scrolls sideways to read a stack trace.
 */
function remarkOutputBlocks(this: unknown) {
  return (tree: MdRoot): undefined => {
    visit(tree, "code", (node: Code) => {
      if (!/(^|\s)out(\s|$)/.test(node.meta ?? "")) return;
      node.data = {
        ...node.data,
        hProperties: { ...(node.data?.hProperties ?? {}), "data-output": "true" },
      };
    });
  };
}

const ALIAS: Record<string, string> = {
  "c#": "csharp", cs: "csharp", "f#": "fsharp", js: "javascript", ts: "typescript",
  sh: "bash", shell: "bash", zsh: "bash", console: "bash", py: "python", yml: "yaml",
  "vb.net": "vb", dotnetcli: "bash", cli: "bash", text: "plaintext", txt: "plaintext",
  output: "plaintext",
};

function textOf(node: Element): string {
  let out = "";
  visit(node, "text", (t: Text) => {
    out += t.value;
  });
  return out;
}

/**
 * Mermaid fences must survive the whole pipeline untouched — no highlighting, no entity
 * mangling — because the browser re-reads their text content to draw the diagram. They
 * are lifted out before the Markdown pass and put back as plain <pre> afterwards.
 */
const MERMAID_FENCE = /^```mermaid[ \t]*\r?\n([\s\S]*?)\r?\n```[ \t]*$/gm;

function escapeHtml(s: string) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/** Turns fenced code into the same .codeblock markup the Python build produced. */
function rehypeShiki(this: unknown, hl: Highlighter) {
  return (tree: Root): undefined => {
    const jobs: (() => void)[] = [];
    visit(tree, "element", (node: Element, index, parent) => {
      if (node.tagName !== "pre" || !parent || index === undefined) return;
      const code = node.children.find(
        (c): c is Element => c.type === "element" && c.tagName === "code",
      );
      if (!code) return;

      const className = (code.properties?.className as string[] | undefined) ?? [];
      const raw = className.find((c) => c.startsWith("language-"))?.slice(9) ?? "";
      const lang = ALIAS[raw.toLowerCase()] ?? raw.toLowerCase();
      /**
       * The marker can land on either element — mdast-util-to-hast applies a code node's
       * hProperties to the <pre> it wraps the <code> in — and under either spelling:
       * rehype-raw serialises the tree and re-parses it, and hast names a parsed
       * `data-output` attribute `dataOutput`.
       */
      const marked = (el: Element) =>
        el.properties?.["data-output"] === "true" || el.properties?.dataOutput === "true";
      const isOutput = marked(node) || marked(code) || raw === "output";
      const known = !isOutput && lang && LANGS.includes(lang);
      const source = textOf(code).replace(/\n$/, "");

      jobs.push(() => {
        // Both themes are emitted at once as CSS variables, so a theme switch is a class
        // flip in the browser rather than a re-render on the server.
        const inner = known
          ? hl.codeToHtml(source, {
              lang,
              themes: { light: "github-light", dark: "github-dark" },
              defaultColor: false,
              cssVariablePrefix: "--sh-",
            })
          : `<pre><code>${escapeHtml(source)}</code></pre>`;

        const label = isOutput
          ? '<span class="lang">Output</span>'
          : raw
            ? `<span class="lang">${escapeHtml(raw)}</span>`
            : "";
        const html =
          `<div class="codeblock${isOutput ? " output" : ""}">${label}` +
          `<button class="copy" type="button" aria-label="Copy code"` +
          ` data-code="${escapeHtml(source)}">` +
          `<svg class="icon" width="14" height="14" viewBox="0 0 24 24" fill="none"` +
          ` stroke="currentColor" stroke-width="1.7" stroke-linecap="round"` +
          ` stroke-linejoin="round" aria-hidden="true">` +
          `<rect x="9" y="9" width="11" height="11" rx="2"/>` +
          `<path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg></button>` +
          `${inner}</div>`;

        parent.children[index] = { type: "raw", value: html } as unknown as Element;
      });
    });
    for (const job of jobs) job();
  };
}

/**
 * A paragraph holding nothing but an image becomes a figure, with the alt text as the
 * caption. Authors write plain Markdown — `![Caption](/media/…)` — and get the book's
 * figure treatment: bordered plate, caption underneath, click to view full screen. It
 * also keeps raw `<figure>` HTML out of section bodies, which is what lets the visual
 * editor round-trip them safely.
 */
function rehypeFigures(this: unknown) {
  return (tree: Root): undefined => {
    visit(tree, "element", (node: Element, index, parent) => {
      if (node.tagName !== "p" || !parent || index === undefined) return;

      const meaningful = node.children.filter(
        (child) => child.type !== "text" || child.value.trim() !== "",
      );
      const [only] = meaningful;
      if (
        meaningful.length !== 1 ||
        only.type !== "element" ||
        only.tagName !== "img" ||
        !only.properties
      ) {
        return;
      }

      const caption = String(only.properties.alt ?? "").trim();
      parent.children[index] = {
        type: "element",
        tagName: "figure",
        properties: { className: ["figimg"], title: "Click to view full screen" },
        children: caption
          ? [
              only,
              {
                type: "element",
                tagName: "figcaption",
                properties: {},
                children: [{ type: "text", value: caption }],
              },
            ]
          : [only],
      };
    });
  };
}

/** Collects h2/h3 for the in-page table of contents, and hangs a # anchor off each. */
function rehypeHeadings(this: unknown, headings: Heading[]) {
  return (tree: Root): undefined => {
    visit(tree, "element", (node: Element) => {
      if (!/^h[23]$/.test(node.tagName)) return;
      const id = String(node.properties?.id ?? "");
      if (!id) return;
      headings.push({ depth: Number(node.tagName[1]), id, text: textOf(node) });
      node.children.push({
        type: "element",
        tagName: "a",
        properties: { className: ["anchor"], href: `#${id}`, "aria-hidden": "true" },
        children: [{ type: "text", value: "#" }],
      });
    });
  };
}

export async function renderMarkdown(markdown: string): Promise<Rendered> {
  const diagrams: string[] = [];
  const source = markdown.replace(MERMAID_FENCE, (_m, body: string) => {
    diagrams.push(body);
    return `\n<div data-mermaid="${diagrams.length - 1}"></div>\n`;
  });

  const headings: Heading[] = [];
  const hl = await highlighter();

  const file = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkMath)
    .use(remarkOutputBlocks)
    // allowDangerousHtml + rehypeRaw is what lets a page carry inline <svg> plots and the
    // hand-written figure markup the old build emitted. Content is authored by the single
    // admin, never by the public, so raw HTML is a feature here rather than an XSS hole.
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeRaw)
    .use(rehypeSlug)
    .use(rehypeFigures)
    .use(rehypeHeadings, headings)
    // rehype-katex handles its own errors (a broken formula is left as red source text),
    // so throwOnError is not among the options it accepts.
    .use(rehypeKatex, { strict: false, output: "html" })
    .use(rehypeShiki, hl)
    .use(rehypeStringify, { allowDangerousHtml: true })
    .process(source);

  // Diagrams go back in last, so nothing in the pipeline ever saw their source.
  const html = String(file).replace(
    /<div data-mermaid="(\d+)"><\/div>/g,
    (_m, i: string) => `<pre class="mermaid">${escapeHtml(diagrams[Number(i)])}</pre>`,
  );

  return {
    html,
    headings,
    diagrams: diagrams.length,
    math: /class="katex/.test(html),
  };
}

/** First paragraph of a page, flattened — used as the deck under a title. */
export function firstParagraph(markdown: string, max = 200): string {
  const body = markdown
    .replace(/^#.*$/gm, "")
    .replace(/^```[\s\S]*?```$/gm, "")
    .replace(/<[^>]+>/g, "")
    .trim();
  const para = body.split(/\n\s*\n/).find((p) => p.trim().length > 40) ?? "";
  const flat = para.replace(/\s+/g, " ").replace(/[*_`]/g, "").trim();
  return flat.length > max ? flat.slice(0, max).replace(/\s\S*$/, "") + "…" : flat;
}
