"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import dynamic from "next/dynamic";
import CodeMirror, { type ReactCodeMirrorRef } from "@uiw/react-codemirror";
import { EditorView } from "@codemirror/view";
import { markdown, markdownLanguage } from "@codemirror/lang-markdown";
import { languages } from "@codemirror/language-data";
import {
  Bold, Italic, Heading2, Link2, Code2, Quote, List, Table, Sigma,
  Workflow, ImagePlus, Save, ExternalLink, Eye, PenLine, FileCode2, PanelRightClose,
  PanelRightOpen, ChevronLeft, ChevronRight, Settings, Sparkles, Loader2,
} from "lucide-react";
import PageRuntime from "@/components/PageRuntime";
import ErrorBoundary from "@/components/ErrorBoundary";
import DiagramPanel from "@/components/editor/DiagramPanel";
import type { VisualApi } from "./VisualEditor";

// MDXEditor reaches for the DOM as it loads, so it is only ever pulled in on the client.
const VisualEditor = dynamic(() => import("./VisualEditor"), {
  ssr: false,
  loading: () => <p className="empty">Loading the visual editor…</p>,
});

/** The figure style the books already use, so a generated diagram matches its neighbours. */
const STYLE_PREFIX = `Clean technical textbook diagram, flat vector style, white background.
Thin gray lines, generous whitespace, no shadows, no gradients, no 3D, no photographic
elements, no decorative icons, no borders around the image. Muted palette: grays with a
single blue accent, plus restrained green and red only where meaning requires it.
Typeset labels in a plain sans-serif, correctly spelled, positioned clear of the marks
they name. The diagram must be self-explanatory and uncluttered.

`;

type Status = "idle" | "dirty" | "saving" | "saved" | "error";
type Mode = "visual" | "raw";

const SNIPPET_MERMAID = `\`\`\`mermaid
flowchart TD
    A["Start"] --> B["Next step"]
\`\`\``;

const SNIPPET_TABLE = `| Column | Column |
| --- | --- |
|  |  |`;

function useDarkMode() {
  const [dark, setDark] = useState(false);
  useEffect(() => {
    const root = document.documentElement;
    const read = () => setDark(root.getAttribute("data-theme") === "dark");
    read();
    const observer = new MutationObserver(read);
    observer.observe(root, { attributes: true, attributeFilter: ["data-theme"] });
    return () => observer.disconnect();
  }, []);
  return dark;
}

export default function Editor({
  sectionId,
  initialBody,
  viewHref,
  details,
  title,
  dek,
  crumbs = [],
  prev,
  next,
  onPage = false,
  aiReady = false,
}: {
  sectionId: number;
  initialBody: string;
  viewHref: string;
  details: React.ReactNode;
  title?: string;
  /** The line under the title, exactly as a reader will see it. */
  dek?: string;
  crumbs?: string[];
  prev?: string | null;
  next?: string | null;
  /** Render inside the reading layout rather than as a split-pane workbench. */
  onPage?: boolean;
  /** Whether this deployment has an image model configured. */
  aiReady?: boolean;
}) {
  const [body, setBody] = useState(initialBody);
  const [mode, setMode] = useState<Mode>("visual");
  const [showPreview, setShowPreview] = useState(!onPage);
  const [showDetails, setShowDetails] = useState(false);
  const [html, setHtml] = useState("");
  const [diagrams, setDiagrams] = useState(0);
  const [status, setStatus] = useState<Status>("idle");
  // Set when the rich-text model cannot represent this page's Markdown.
  const [unsupported, setUnsupported] = useState<string | null>(null);
  const editor = useRef<ReactCodeMirrorRef>(null);
  const saved = useRef(initialBody);
  const dark = useDarkMode();

  /**
   * Images dropped into the editor are held in the browser until the page is saved:
   * the document gets a `blob:` URL that only this tab can resolve, and the file itself
   * waits here. Nothing reaches the server for a picture the author pastes and then
   * thinks better of.
   */
  const pending = useRef(new Map<string, File>());

  /**
   * Where each staged image ended up once it was uploaded.
   *
   * The block editor keeps its own copy of the document and is deliberately never
   * re-rendered from the outside, so it goes on emitting the `blob:` URL it was given
   * long after the file has a real one. Every conversion out of the editor is therefore
   * translated through this map, and the blob URLs stay alive until the editor closes —
   * revoking one while the editor still referenced it was what turned a saved image into
   * a broken one the moment its caption was edited.
   */
  const uploaded = useRef(new Map<string, string>());

  const stage = useCallback((file: File) => {
    const url = URL.createObjectURL(file);
    pending.current.set(url, file);
    return url;
  }, []);

  /** Rewrites any staged URL in a document to the address it was uploaded to. */
  const settle = useCallback((text: string) => {
    let out = text;
    for (const [blob, real] of uploaded.current) out = out.split(blob).join(real);
    return out;
  }, []);

  useEffect(
    () => () => {
      for (const url of uploaded.current.keys()) URL.revokeObjectURL(url);
      for (const url of pending.current.keys()) URL.revokeObjectURL(url);
    },
    [],
  );

  // ---- preview ---------------------------------------------------------------------
  useEffect(() => {
    if (!showPreview) return;
    const ac = new AbortController();
    const timer = setTimeout(async () => {
      try {
        const res = await fetch("/api/admin/preview", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ markdown: body }),
          signal: ac.signal,
        });
        const data = (await res.json()) as { html: string; diagrams: number };
        setHtml(data.html);
        setDiagrams(data.diagrams);
      } catch {
        /* superseded by a newer keystroke */
      }
    }, 800);
    return () => {
      clearTimeout(timer);
      ac.abort();
    };
  }, [body, showPreview]);

  // ---- saving ----------------------------------------------------------------------
  const save = useCallback(async () => {
    setStatus("saving");
    try {
      // Staged images are uploaded first, then their blob: URLs are swapped for the real
      // ones, so a save either lands complete or not at all.
      let text = settle(body);
      for (const [url, file] of pending.current) {
        if (!text.includes(url)) {
          // Dropped, then deleted before saving: it never existed as far as the server
          // is concerned.
          pending.current.delete(url);
          URL.revokeObjectURL(url);
          continue;
        }
        const form = new FormData();
        form.append("file", file);
        const res = await fetch("/api/upload", { method: "POST", body: form });
        const data = (await res.json()) as { url?: string; error?: string };
        if (!data.url) throw new Error(data.error ?? "Upload failed");
        text = text.split(url).join(data.url);
        // Remembered, not revoked: the editor still holds the blob URL in its blocks.
        uploaded.current.set(url, data.url);
        pending.current.delete(url);
      }

      if (text !== body) setBody(text);

      const res = await fetch("/api/admin/section", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ id: sectionId, body: text }),
      });
      if (!res.ok) throw new Error(await res.text());
      saved.current = text;
      setStatus((s) => (s === "saving" ? "saved" : s));
    } catch {
      setStatus("error");
    }
  }, [body, sectionId, settle]);

  // No autosave: a page is written when the author says so, with Save or Ctrl/Cmd+S.
  // Typing only marks the page dirty, which the status in the bar reports.
  useEffect(() => {
    setStatus(body === saved.current ? "idle" : "dirty");
  }, [body]);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") {
        e.preventDefault();
        save();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [save]);

  useEffect(() => {
    function onLeave(e: BeforeUnloadEvent) {
      if (body !== saved.current) e.preventDefault();
    }
    window.addEventListener("beforeunload", onLeave);
    return () => window.removeEventListener("beforeunload", onLeave);
  }, [body]);

  // ---- raw-mode toolbar --------------------------------------------------------------
  function surround(before: string, after = before, placeholder = "") {
    const view = editor.current?.view;
    if (!view) return;
    const { from, to } = view.state.selection.main;
    const selected = view.state.sliceDoc(from, to) || placeholder;
    view.dispatch({
      changes: { from, to, insert: `${before}${selected}${after}` },
      selection: { anchor: from + before.length, head: from + before.length + selected.length },
    });
    view.focus();
  }

  function insertBlock(text: string) {
    const view = editor.current?.view;
    if (!view) return;
    const { from, to } = view.state.selection.main;
    const line = view.state.doc.lineAt(from);
    const pad = line.text.trim() ? "\n\n" : "";
    view.dispatch({
      changes: { from, to, insert: `${pad}${text}\n` },
      selection: { anchor: from + pad.length + text.length + 1 },
    });
    view.focus();
  }

  function prefixLine(prefix: string) {
    const view = editor.current?.view;
    if (!view) return;
    const { from } = view.state.selection.main;
    const line = view.state.doc.lineAt(from);
    view.dispatch({ changes: { from: line.from, insert: prefix } });
    view.focus();
  }

  const fileInput = useRef<HTMLInputElement>(null);

  /** A file chosen or dropped by hand: staged now, uploaded when the page is saved. */
  function dropImage(file: File) {
    const url = stage(file);
    insertBlock(`![${file.name.replace(/\.[^.]+$/, "").replace(/[-_]+/g, " ")}](${url})`);
    setStatus("dirty");
  }

  // Drawing lives in its own docked panel; this only says whether it is open.
  const [genOpen, setGenOpen] = useState(false);

  /** The visual editor's insert hook, while it is mounted. */
  const visual = useRef<VisualApi | null>(null);

  /**
   * Puts a picture into the page, whichever way it is being written.
   *
   * The block editor owns its own document, so it has to be told; the Markdown pane is
   * driven by `body`, so it is appended to. Getting this wrong is invisible until the
   * next keystroke throws the insert away.
   */
  const insertImage = useCallback(
    (url: string, caption: string) => {
      if (mode === "visual" && !unsupported && visual.current) {
        visual.current.insertImage(url, caption);
      } else {
        setBody((current) => `${current.replace(/\s+$/, "")}\n\n![${caption}](${url})\n`);
      }
      setStatus("dirty");
    },
    [mode, unsupported],
  );

  const words = useMemo(() => (body.trim() ? body.trim().split(/\s+/).length : 0), [body]);
  const staged = pending.current.size;

  const surface =
    mode === "raw" || unsupported ? (
      <div
        className="editor-code on-page"
        onDrop={(e) => {
          const file = e.dataTransfer.files?.[0];
          if (file?.type.startsWith("image/")) {
            e.preventDefault();
            dropImage(file);
          }
        }}
        onDragOver={(e) => {
          if (e.dataTransfer.types.includes("Files")) e.preventDefault();
        }}
      >
        <CodeMirror
          ref={editor}
          value={body}
          onChange={setBody}
          theme={dark ? "dark" : "light"}
          basicSetup={{ lineNumbers: false, foldGutter: false, highlightActiveLine: false }}
          extensions={[
            markdown({ base: markdownLanguage, codeLanguages: languages }),
            EditorView.lineWrapping,
          ]}
        />
      </div>
    ) : (
      <ErrorBoundary
        fallback={<p className="empty">The visual editor could not open this page.</p>}
        onError={(error) => setUnsupported(error.message)}
      >
        <VisualEditor
          markdown={body}
          onChange={(value) => setBody(settle(value))}
          stageImage={stage}
          onUnsupported={(reason) => {
            setUnsupported(reason);
            setMode("raw");
          }}
        />
      </ErrorBoundary>
    );

  if (onPage) {
    return (
      <>
        <div className="topbar">
          {prev ? (
            <a className="nudge" href={prev} aria-label="Previous section">
              <ChevronLeft size={15} strokeWidth={1.7} />
            </a>
          ) : (
            <span className="nudge off">
              <ChevronLeft size={15} strokeWidth={1.7} />
            </span>
          )}
          {next ? (
            <a className="nudge" href={next} aria-label="Next section">
              <ChevronRight size={15} strokeWidth={1.7} />
            </a>
          ) : (
            <span className="nudge off">
              <ChevronRight size={15} strokeWidth={1.7} />
            </span>
          )}

          <div className="crumb">
            {crumbs.map((c, i) => (
              <span key={i}>
                {i > 0 ? <b>/</b> : null}
                {c}
              </span>
            ))}
            {title ? (
              <span className="here">
                <b>/</b>
                {title}
              </span>
            ) : null}
          </div>

          <div className="seg desk-only">
            <button
              type="button"
              className={mode === "visual" && !unsupported && !showPreview ? "on" : ""}
              onClick={() => {
                setUnsupported(null);
                setShowPreview(false);
                setMode("visual");
              }}
            >
              <PenLine size={12} strokeWidth={1.9} /> Write
            </button>
            <button
              type="button"
              className={mode === "raw" && !showPreview ? "on" : ""}
              onClick={() => {
                setShowPreview(false);
                setMode("raw");
              }}
            >
              <FileCode2 size={12} strokeWidth={1.9} /> Markdown
            </button>
            <button
              type="button"
              className={showPreview ? "on" : ""}
              onClick={() => setShowPreview(true)}
            >
              <Eye size={12} strokeWidth={1.9} /> Read
            </button>
          </div>

          <span className={`editor-status ${status} desk-only`}>
            {status === "saving"
              ? "Saving…"
              : status === "saved"
                ? "Saved"
                : status === "dirty"
                  ? "Unsaved"
                  : status === "error"
                    ? "Save failed"
                    : ""}
          </span>

          {aiReady ? (
            <button
              type="button"
              className="nudge desk-only"
              onClick={() => setGenOpen((v) => !v)}
              title="Draw a diagram from a description"
            >
              <Sparkles size={15} strokeWidth={1.7} />
            </button>
          ) : null}
          <button
            type="button"
            className="nudge desk-only"
            onClick={() => setShowDetails((v) => !v)}
            title="Section settings"
          >
            <Settings size={15} strokeWidth={1.7} />
          </button>
          <a className="nudge desk-only" href={viewHref} target="_blank" rel="noopener" title="View live page">
            <ExternalLink size={15} strokeWidth={1.7} />
          </a>
          <button className="btn primary desk-only" type="button" onClick={save}>
            <Save size={12} strokeWidth={2} /> Save
          </button>
        </div>

        {unsupported ? (
          <p className="notice bad" style={{ margin: "14px 40px 0" }}>
            This page is being edited as Markdown: its markup is richer than the block
            editor can hold without changing it.
          </p>
        ) : null}

        {showDetails ? <div className="workbench-details">{details}</div> : null}

        <div className={`onpage${genOpen ? " with-panel" : ""}`}>
        <article className="lesson">
          <header className="lesson-head">
            <p className="meta">{crumbs[crumbs.length - 1]}</p>
            <h1>{title}</h1>
            {dek ? <p className="dek">{dek}</p> : null}
          </header>
          <p className="rule">§ § §</p>

          {showPreview ? (
            <>
              <div dangerouslySetInnerHTML={{ __html: html }} />
              <PageRuntime key={diagrams} hasDiagrams={diagrams > 0} />
            </>
          ) : (
            surface
          )}
        </article>

        {genOpen ? (
          <DiagramPanel
            sectionId={sectionId}
            onClose={() => setGenOpen(false)}
            onInsert={insertImage}
          />
        ) : null}
        </div>
      </>
    );
  }

  return (
    <div className="workbench">
      <div className="workbench-bar">
        <div className="seg">
          <button
            type="button"
            className={mode === "visual" && !unsupported ? "on" : ""}
            onClick={() => {
              setUnsupported(null);
              setMode("visual");
            }}
            title={
              unsupported
                ? "This page uses markup the visual editor cannot represent"
                : "Write with formatting"
            }
          >
            <PenLine size={12} strokeWidth={1.9} /> Visual
          </button>
          <button
            type="button"
            className={mode === "raw" ? "on" : ""}
            onClick={() => setMode("raw")}
          >
            <FileCode2 size={12} strokeWidth={1.9} /> Markdown
          </button>
        </div>

        <span className="editor-status-group">
          <span className="editor-count">{words} words</span>
          {staged ? <span className="chip">{staged} image{staged > 1 ? "s" : ""} pending</span> : null}
          <span className={`editor-status ${status}`}>
            {status === "saving"
              ? "Saving…"
              : status === "saved"
                ? "Saved"
                : status === "dirty"
                  ? "Unsaved changes"
                  : status === "error"
                    ? "Save failed"
                    : "Up to date"}
          </span>
        </span>

        <span className="grow" />

        <button
          type="button"
          className="btn"
          onClick={() => setShowPreview((v) => !v)}
          title={showPreview ? "Hide the preview" : "Show the preview"}
        >
          {showPreview ? <PanelRightClose size={12} /> : <PanelRightOpen size={12} />}
          Preview
        </button>
        <button type="button" className="btn" onClick={() => setShowDetails((v) => !v)}>
          Details
        </button>
        <a className="btn" href={viewHref} target="_blank" rel="noopener">
          <ExternalLink size={12} strokeWidth={1.7} /> Live
        </a>
        <button className="btn primary" type="button" onClick={save}>
          <Save size={12} strokeWidth={2} /> Save
        </button>
      </div>

      {unsupported ? (
        <p className="notice bad" style={{ margin: "10px 14px 0" }}>
          This page is being edited as Markdown: its markup is richer than the visual
          editor can round-trip without changing it.
        </p>
      ) : null}

      {showDetails ? <div className="workbench-details">{details}</div> : null}

      <div className={`workbench-panes${showPreview ? "" : " solo"}`}>
        <div className="editor-pane">
          {mode === "raw" || unsupported ? (
            <>
              <div className="editor-toolbar">
                <button type="button" title="Bold" onClick={() => surround("**", "**", "bold")}>
                  <Bold size={13} strokeWidth={2} />
                </button>
                <button type="button" title="Italic" onClick={() => surround("_", "_", "italic")}>
                  <Italic size={13} strokeWidth={2} />
                </button>
                <button type="button" title="Heading" onClick={() => prefixLine("## ")}>
                  <Heading2 size={13} strokeWidth={2} />
                </button>
                <button type="button" title="Link" onClick={() => surround("[", "](https://)", "text")}>
                  <Link2 size={13} strokeWidth={2} />
                </button>
                <button type="button" title="Inline code" onClick={() => surround("`", "`", "code")}>
                  <Code2 size={13} strokeWidth={2} />
                </button>
                <button type="button" title="Quote" onClick={() => prefixLine("> ")}>
                  <Quote size={13} strokeWidth={2} />
                </button>
                <button type="button" title="List" onClick={() => prefixLine("- ")}>
                  <List size={13} strokeWidth={2} />
                </button>
                <button type="button" title="Table" onClick={() => insertBlock(SNIPPET_TABLE)}>
                  <Table size={13} strokeWidth={2} />
                </button>
                <button
                  type="button"
                  title="Display maths"
                  onClick={() => insertBlock("$$\n\\hat{y} = w^{T}x + b\n$$")}
                >
                  <Sigma size={13} strokeWidth={2} />
                </button>
                <button type="button" title="Mermaid diagram" onClick={() => insertBlock(SNIPPET_MERMAID)}>
                  <Workflow size={13} strokeWidth={2} />
                </button>
                <button type="button" title="Insert image" onClick={() => fileInput.current?.click()}>
                  <ImagePlus size={13} strokeWidth={2} />
                </button>
                <input
                  ref={fileInput}
                  type="file"
                  accept="image/*"
                  hidden
                  onChange={(e) => {
                    const file = e.target.files?.[0];
                    if (file) dropImage(file);
                    e.target.value = "";
                  }}
                />
              </div>

              <div
                className="editor-code"
                onDrop={(e) => {
                  const file = e.dataTransfer.files?.[0];
                  if (file?.type.startsWith("image/")) {
                    e.preventDefault();
                    dropImage(file);
                  }
                }}
                onDragOver={(e) => {
                  if (e.dataTransfer.types.includes("Files")) e.preventDefault();
                }}
              >
                <CodeMirror
                  ref={editor}
                  value={body}
                  onChange={setBody}
                  theme={dark ? "dark" : "light"}
                  basicSetup={{ lineNumbers: true, foldGutter: false, highlightActiveLine: true }}
                  extensions={[
                    markdown({ base: markdownLanguage, codeLanguages: languages }),
                    EditorView.lineWrapping,
                  ]}
                />
              </div>
            </>
          ) : (
            <ErrorBoundary
              fallback={<p className="empty">The visual editor could not open this page.</p>}
              onError={(error) => setUnsupported(error.message)}
            >
              <VisualEditor
                markdown={body}
                onChange={(value) => setBody(settle(value))}
                stageImage={stage}
                register={(api) => {
                  visual.current = api;
                }}
                onUnsupported={(reason) => {
                  setUnsupported(reason);
                  setMode("raw");
                }}
              />
            </ErrorBoundary>
          )}
        </div>

        {showPreview ? (
          <div className="editor-pane">
            <div className="editor-head">
              <Eye size={12} strokeWidth={1.9} />
              <span className="grow">Preview</span>
            </div>
            <div className="editor-preview">
              <div className="lesson" dangerouslySetInnerHTML={{ __html: html }} />
              <PageRuntime key={diagrams} hasDiagrams={diagrams > 0} />
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
