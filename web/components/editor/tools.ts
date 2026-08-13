"use client";

import type { API, BlockTool, BlockToolData } from "@editorjs/editorjs";

/**
 * Two blocks Editor.js does not ship, both of which exist to protect content the block
 * model would otherwise flatten.
 */

type FencedData = { code: string; language: string };

/**
 * A fenced code block that remembers its language — which the stock code tool does not,
 * and which matters here because ```mermaid is how every diagram in these books is
 * written. Losing the language would turn a diagram into a grey box.
 */
export class FencedTool implements BlockTool {
  private data: FencedData;
  private wrapper: HTMLElement | null = null;

  static get toolbox() {
    return {
      title: "Code",
      icon: '<svg width="17" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 6l-5 6 5 6M16 6l5 6-5 6"/></svg>',
    };
  }

  static get enableLineBreaks() {
    return true;
  }

  constructor({ data }: { data: BlockToolData<FencedData> }) {
    this.data = { code: data?.code ?? "", language: data?.language ?? "" };
  }

  render() {
    const wrapper = document.createElement("div");
    wrapper.className = "block-fenced";

    const head = document.createElement("div");
    head.className = "block-fenced-head";

    const language = document.createElement("input");
    language.className = "block-fenced-lang";
    language.value = this.data.language;
    language.placeholder = "language (mermaid, python, csharp…)";
    language.addEventListener("input", () => {
      this.data.language = language.value.trim();
    });

    head.appendChild(language);

    const code = document.createElement("textarea");
    code.className = "block-fenced-code";
    code.value = this.data.code;
    code.placeholder = "Code or diagram source";
    code.rows = Math.max(3, this.data.code.split("\n").length);
    const grow = () => {
      code.style.height = "auto";
      code.style.height = `${code.scrollHeight}px`;
    };
    code.addEventListener("input", () => {
      this.data.code = code.value;
      grow();
    });
    // The textarea has to size itself once it is actually in the document.
    setTimeout(grow, 0);

    wrapper.append(head, code);
    this.wrapper = wrapper;
    return wrapper;
  }

  save(): FencedData {
    return this.data;
  }

  /**
   * `true` means "leave this field exactly as the tool returned it". The alternative,
   * `false`, runs the value through the HTML sanitiser — which parses Markdown as if it
   * were markup and re-serialises `>` as `&gt;`, quietly corrupting every blockquote.
   */
  static get sanitize() {
    return { code: true, language: true };
  }
}

type RawData = { html: string };

/**
 * Anything Markdown can express that blocks cannot: display maths, raw HTML, a footnote
 * definition. The source is shown as-is and handed back byte-identical, so opening the
 * visual editor can never rewrite it.
 */
export class RawTool implements BlockTool {
  private data: RawData;

  static get toolbox() {
    return {
      title: "Markdown / HTML",
      icon: '<svg width="17" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M4 12h10M4 17h13"/></svg>',
    };
  }

  static get enableLineBreaks() {
    return true;
  }

  constructor({ data }: { data: BlockToolData<RawData> }) {
    this.data = { html: data?.html ?? "" };
  }

  render() {
    const wrapper = document.createElement("div");
    wrapper.className = "block-raw";

    const label = document.createElement("span");
    label.className = "block-raw-label";
    label.textContent = "Markdown source — kept exactly as written";

    const area = document.createElement("textarea");
    area.className = "block-raw-code";
    area.value = this.data.html;
    area.rows = Math.max(2, this.data.html.split("\n").length);
    const grow = () => {
      area.style.height = "auto";
      area.style.height = `${area.scrollHeight}px`;
    };
    area.addEventListener("input", () => {
      this.data.html = area.value;
      grow();
    });
    setTimeout(grow, 0);

    wrapper.append(label, area);
    return wrapper;
  }

  save(): RawData {
    return this.data;
  }

  /** Untouched: this block exists precisely to carry source the editor must not rewrite. */
  static get sanitize() {
    return { html: true };
  }
}

/** Editor.js hands tools an API object; neither of these needs it. */
export type Unused = API;
