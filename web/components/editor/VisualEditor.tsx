"use client";

import { useEffect, useRef, useState } from "react";
import EditorJS, { type OutputData } from "@editorjs/editorjs";
import Header from "@editorjs/header";
import List from "@editorjs/list";
import Quote from "@editorjs/quote";
import Table from "@editorjs/table";
import ImageTool from "@editorjs/image";
import Delimiter from "@editorjs/delimiter";
import Marker from "@editorjs/marker";
import InlineCode from "@editorjs/inline-code";
import { FencedTool, RawTool } from "./tools";
import { blocksToMarkdown, type Block } from "@/lib/blocks";

/**
 * The block editor: no standing toolbar, a "+" to add a block, a floating bar on
 * selection, and drag handles for reordering — the writing surface stays quiet until it
 * is needed.
 *
 * Markdown remains the document. Blocks are built from it when the editor opens, and
 * every edit is converted straight back, so the Markdown pane and the preview are never
 * looking at anything but the real page.
 */
/** What the parent can ask this editor to do once it is running. */
export type VisualApi = { insertImage: (url: string, caption: string) => void };

export default function VisualEditor({
  markdown,
  onChange,
  stageImage,
  onUnsupported,
  register,
}: {
  markdown: string;
  onChange: (value: string) => void;
  stageImage: (file: File) => string;
  onUnsupported: (reason: string) => void;
  /**
   * Hands the parent a way to put something into the document.
   *
   * The editor owns its content and is never re-rendered from the outside, so appending
   * to the Markdown behind its back does nothing — and would be lost on the next
   * keystroke. Anything inserted from elsewhere has to come through here.
   */
  register?: (api: VisualApi | null) => void;
}) {
  const holder = useRef<HTMLDivElement>(null);
  const editor = useRef<EditorJS | null>(null);
  const [loading, setLoading] = useState(true);

  // The initial Markdown only; later edits flow outward, never back in, so the editor is
  // never rebuilt under the author's cursor.
  const initial = useRef(markdown);
  const emit = useRef(onChange);
  emit.current = onChange;
  const stage = useRef(stageImage);
  stage.current = stageImage;
  const unsupported = useRef(onUnsupported);
  unsupported.current = onUnsupported;
  const expose = useRef(register);
  expose.current = register;

  useEffect(() => {
    let cancelled = false;
    let instance: EditorJS | null = null;

    (async () => {
      const res = await fetch("/api/admin/blocks", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ markdown: initial.current }),
      });
      const { blocks, safe } = (await res.json()) as { blocks: Block[]; safe: boolean };
      if (cancelled) return;

      if (!safe) {
        // The page uses Markdown the block model would alter. Hand it back rather than
        // let the editor rewrite someone's work.
        unsupported.current("This page's markup cannot be edited as blocks without changing it.");
        setLoading(false);
        return;
      }

      instance = new EditorJS({
        holder: holder.current!,
        data: { blocks } as OutputData,
        placeholder: "Write, or press Tab to add a block",
        minHeight: 240,
        tools: {
          header: { class: Header as never, inlineToolbar: true, config: { levels: [2, 3, 4], defaultLevel: 2 } },
          // One registration only: this tool already offers ordered, unordered and
          // checklist as variants, and registering it twice put "Checklist" in the block
          // menu twice.
          list: { class: List as never, inlineToolbar: true },
          quote: { class: Quote as never, inlineToolbar: true },
          table: { class: Table as never, inlineToolbar: true },
          delimiter: Delimiter as never,
          marker: Marker as never,
          inlineCode: InlineCode as never,
          fenced: FencedTool as never,
          raw: RawTool as never,
          image: {
            class: ImageTool as never,
            config: {
              // Dropped images are held in the browser and given a blob: URL; the upload
              // happens when the page is saved.
              uploader: {
                uploadByFile: async (file: File) => ({
                  success: 1,
                  file: { url: stage.current(file) },
                }),
              },
              captionPlaceholder: "Caption",
              /**
               * The image tool offers border, stretch and background as block tunes.
               * A page is stored as Markdown — `![caption](url)` — which has nowhere to
               * put any of them, so they would appear to work and then be gone on save.
               * Only the tunes that survive a round trip are left in the menu: move,
               * delete, and the caption.
               */
              features: { border: false, background: false, stretch: false, caption: true },
            },
          },
        },
        onChange: () => schedule(),
        onReady: () => {
          setLoading(false);
          expose.current?.({
            insertImage(url, caption) {
              instance?.blocks.insert(
                "image",
                { file: { url }, caption },
                undefined,
                instance.blocks.getBlocksCount(),
                true,
              );
              schedule();
            },
          });
        },
      });

      editor.current = instance;
    })();

    // Editor.js fires onChange per keystroke and `save()` walks every block, so the
    // conversion is collapsed into one pass after typing pauses.
    let timer: ReturnType<typeof setTimeout>;
    function schedule() {
      clearTimeout(timer);
      timer = setTimeout(async () => {
        try {
          const output = await instance?.save();
          if (output) emit.current(blocksToMarkdown(output.blocks as Block[]));
        } catch {
          /* a block mid-edit: the next keystroke will try again */
        }
      }, 300);
    }

    return () => {
      cancelled = true;
      expose.current?.(null);
      clearTimeout(timer);
      // destroy() only exists once the editor finished initialising.
      instance?.isReady
        ?.then(() => instance?.destroy())
        .catch(() => {});
      editor.current = null;
    };
  }, []);

  return (
    <div className="visual-editor">
      {loading ? <p className="empty">Opening…</p> : null}
      <div ref={holder} className="block-holder" />
    </div>
  );
}
