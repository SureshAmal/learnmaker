"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Sparkles, X, Loader2, RotateCcw, Plus, Trash2, KeyRound } from "lucide-react";
import { loadConfig, generateImage, type AiConfig } from "@/lib/ai-browser";
import AiKeyForm from "@/components/AiKeyForm";

/**
 * Drawing diagrams, docked beside the page being written.
 *
 * Generation runs in this browser with the author's own key, which means a refresh
 * mid-request would otherwise lose it with nothing to show for the wait. So the request
 * is written down before it starts and cleared when it lands: on load, an unfinished one
 * is offered back for retry, and everything already drawn for this section is listed with
 * its prompt, ready to drop into the page again.
 *
 * The record lives in this browser only. Nothing about a prompt reaches the database
 * until an image is actually filed in the media library.
 */

const STYLE_PREFIX = `Clean technical textbook diagram, flat vector style, white background.
Thin gray lines, generous whitespace, no shadows, no gradients, no 3D, no photographic
elements, no decorative icons, no borders around the image. Muted palette: grays with a
single blue accent, plus restrained green and red only where meaning requires it.
Typeset labels in a plain sans-serif, correctly spelled, positioned clear of the marks
they name. The diagram must be self-explanatory and uncluttered.

`;

type Drawn = { url: string; prompt: string; at: number };
type Record_ = { pending?: { prompt: string; at: number }; drawn: Drawn[] };

const key = (sectionId: number) => `learn-diagrams:${sectionId}`;

function read(sectionId: number): Record_ {
  try {
    const raw = localStorage.getItem(key(sectionId));
    return raw ? (JSON.parse(raw) as Record_) : { drawn: [] };
  } catch {
    return { drawn: [] };
  }
}

function write(sectionId: number, value: Record_) {
  try {
    localStorage.setItem(key(sectionId), JSON.stringify(value));
  } catch {
    /* private mode: history simply does not persist */
  }
}

export default function DiagramPanel({
  sectionId,
  onClose,
  onInsert,
}: {
  sectionId: number;
  onClose: () => void;
  onInsert: (url: string, caption: string) => void;
}) {
  const [prompt, setPrompt] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [drawn, setDrawn] = useState<Drawn[]>([]);
  const [unfinished, setUnfinished] = useState<string | null>(null);
  const [config, setConfig] = useState<AiConfig | null>(null);
  const [keyOpen, setKeyOpen] = useState(false);
  const resumed = useRef(false);

  const draw = useCallback(
    async (description: string) => {
      const text = description.trim();
      if (!text) return;

      const cfg = loadConfig();
      if (!cfg) {
        setKeyOpen(true);
        return;
      }

      setBusy(true);
      setError(null);
      setUnfinished(null);

      // Written down before the request, so a refresh mid-draw leaves a trace.
      const before = read(sectionId);
      write(sectionId, { ...before, pending: { prompt: text, at: Date.now() } });

      try {
        const image = await generateImage(cfg, STYLE_PREFIX + text);
        if (!image) {
          throw new Error("The model replied without a picture. Try describing it differently.");
        }

        const res = await fetch("/api/admin/image", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ data: image.data, prompt: text }),
        });
        const stored = (await res.json()) as { url?: string; error?: string };
        if (!stored.url) throw new Error(stored.error ?? "The picture could not be saved.");

        const entry: Drawn = { url: stored.url, prompt: text, at: Date.now() };
        const after = read(sectionId);
        const next = [entry, ...after.drawn].slice(0, 12);
        write(sectionId, { drawn: next });
        setDrawn(next);
        setPrompt("");
        onInsert(stored.url, text);
      } catch (err) {
        const record = read(sectionId);
        write(sectionId, record); // keeps `pending`, so it can be retried after a reload
        setUnfinished(text);
        setError(err instanceof Error ? err.message : "That did not work.");
      } finally {
        setBusy(false);
      }
    },
    [sectionId, onInsert],
  );

  // What this browser already knows about this section.
  useEffect(() => {
    const record = read(sectionId);
    setDrawn(record.drawn ?? []);
    setConfig(loadConfig());
    setKeyOpen(!loadConfig());

    if (record.pending && !resumed.current) {
      resumed.current = true;
      setUnfinished(record.pending.prompt);
      setPrompt(record.pending.prompt);
    }
  }, [sectionId]);

  function forget(url: string) {
    const next = drawn.filter((d) => d.url !== url);
    write(sectionId, { drawn: next });
    setDrawn(next);
  }

  return (
    <aside className="genpanel">
      <div className="ask-head">
        <Sparkles size={13} strokeWidth={1.8} />
        <span className="grow">Draw a diagram</span>
        <button type="button" onClick={() => setKeyOpen((v) => !v)} title="Key and model">
          <KeyRound size={13} strokeWidth={1.8} />
        </button>
        <button type="button" onClick={onClose} aria-label="Close">
          <X size={14} strokeWidth={1.8} />
        </button>
      </div>

      <div className="genpanel-body">
        {keyOpen ? (
          <AiKeyForm
            config={config}
            onDone={(cfg) => {
              setConfig(cfg);
              setKeyOpen(false);
              setError(null);
            }}
            onCancel={config ? () => setKeyOpen(false) : undefined}
          />
        ) : null}

        {error ? <p className="notice bad">{error}</p> : null}

        {unfinished && !busy ? (
          <p className="notice">
            An unfinished request is waiting: <em>{unfinished.slice(0, 80)}</em>
            <button className="ask-more" type="button" onClick={() => draw(unfinished)}>
              <RotateCcw size={11} strokeWidth={2} /> Try again
            </button>
          </p>
        ) : null}

        <label className="field">
          <span>Describe it — drawn in the book&rsquo;s figure style</span>
          <textarea
            rows={4}
            value={prompt}
            placeholder="A bias–variance tradeoff curve: error against model complexity, with training and test curves crossing."
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) draw(prompt);
            }}
          />
        </label>

        <button className="btn primary" type="button" onClick={() => draw(prompt)} disabled={busy}>
          {busy ? (
            <>
              <Loader2 size={12} className="spin" strokeWidth={2} /> Drawing…
            </>
          ) : (
            <>
              <Sparkles size={12} strokeWidth={2} /> Draw
            </>
          )}
        </button>

        {drawn.length ? (
          <>
            <h2 style={{ margin: "26px 0 10px" }}>Drawn for this page</h2>
            <div className="genpanel-shots">
              {drawn.map((d) => (
                <figure key={d.url}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={d.url} alt={d.prompt} loading="lazy" />
                  <figcaption>{d.prompt}</figcaption>
                  <div className="media-actions">
                    <button
                      className="btn"
                      type="button"
                      onClick={() => onInsert(d.url, d.prompt)}
                    >
                      <Plus size={11} strokeWidth={2} /> Insert
                    </button>
                    <button
                      className="btn danger"
                      type="button"
                      onClick={() => forget(d.url)}
                      title="Remove from this list — the image stays in the media library"
                    >
                      <Trash2 size={11} strokeWidth={1.7} />
                    </button>
                  </div>
                </figure>
              ))}
            </div>
          </>
        ) : null}
      </div>
    </aside>
  );
}
