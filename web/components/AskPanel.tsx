"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { Sparkles, X, CornerDownLeft, Loader2, KeyRound } from "lucide-react";
import { loadConfig, ask as askModel, type AiConfig } from "@/lib/ai-browser";
import AiKeyForm from "@/components/AiKeyForm";

/**
 * Small talk, which the book should not be searched for.
 *
 * A score threshold looked like the obvious test and is the wrong one: BM25 scores are
 * not comparable between queries, so "hello" scored 5.2 against a Gradio demo while
 * "what is fine tuning" scored 3.1 — gating on the number would have primed the greeting
 * and starved the real question. What actually distinguishes them is the words.
 */
const PLEASANTRIES = new Set([
  "hi", "hey", "hello", "yo", "sup", "thanks", "thank", "thankyou", "ta", "cheers",
  "ok", "okay", "k", "cool", "nice", "great", "bye", "goodbye", "test", "testing",
  "please", "you", "u", "good", "morning", "afternoon", "evening", "there",
]);

function smallTalk(question: string) {
  const words = question.toLowerCase().replace(/[^a-z\s]/g, " ").split(/\s+/).filter(Boolean);
  return words.length > 0 && words.length <= 4 && words.every((w) => PLEASANTRIES.has(w));
}

type Source = { title: string; chapter: string; href: string };
type Turn = {
  question: string;
  answer: string;
  sources: Source[];
  /** What the model chose to look up, shown while it works. */
  lookups: string[];
  error?: string;
};

const SYSTEM = `You answer questions about a technical book. Passages from it are given
to you with the question; call search_book if they are not enough, and read_section to
see a whole section.

- Prefer the passages you were given. Search again only when they genuinely do not
  contain the answer, and search once with good terms rather than many times with vague
  ones.
- If the reader is greeting you or making small talk, reply in one short line and invite
  a question. Do not list topics, and do not search.
- Answer only from what the tools return. If they do not contain the answer, say so
  plainly in one sentence and stop — do not fall back on general knowledge.
- Lead with the answer. Never describe your searching, and never mention "passages",
  "excerpts" or "context" as things the reader can see.
- Prefer the book's own terms and notation over synonyms.
- Do not list your sources or name the sections at the end. They are shown to the reader
  underneath your answer already, so repeating them only says everything twice.
- Be brief: a few sentences, or a short list when the answer really is a list.`;

/**
 * Answers questions from the book's own pages, using the reader's own model.
 *
 * The site holds no key and never sees a question: this page fetches passages from the
 * book's search index, then calls Google directly from the browser with credentials the
 * reader supplied. The key lives in this browser's localStorage; the conversation lives
 * only in this component's memory and is gone when the panel closes. Nothing is written
 * to the database.
 */
export default function AskPanel({ bookSlug }: { bookSlug?: string }) {
  const [open, setOpen] = useState(false);
  const [config, setConfig] = useState<AiConfig | null>(null);
  const [editingKey, setEditingKey] = useState(false);
  const [question, setQuestion] = useState("");
  const [turns, setTurns] = useState<Turn[]>([]);
  const [busy, setBusy] = useState(false);
  const input = useRef<HTMLTextAreaElement>(null);
  const log = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const show = () => setOpen(true);
    window.addEventListener("learn:ask", show);
    return () => window.removeEventListener("learn:ask", show);
  }, []);

  useEffect(() => {
    if (!open) return;
    const saved = loadConfig();
    setConfig(saved);
    setEditingKey(!saved);
  }, [open]);

  // The page keeps a lane open for the panel, so the column narrows instead of being
  // covered. That is a document-level concern, hence the class on the root.
  useEffect(() => {
    document.documentElement.classList.toggle("with-ask", open);
    if (open && !editingKey) input.current?.focus();
    return () => document.documentElement.classList.remove("with-ask");
  }, [open, editingKey]);

  useEffect(() => {
    log.current?.scrollTo({ top: log.current.scrollHeight, behavior: "smooth" });
  }, [turns]);

  async function ask() {
    const q = question.trim();
    if (!q || busy || !config) return;

    setQuestion("");
    setBusy(true);
    setTurns((t) => [...t, { question: q, answer: "", sources: [], lookups: [] }]);

    const patch = (change: (turn: Turn) => Partial<Turn>) =>
      setTurns((t) => t.map((turn, i) => (i === t.length - 1 ? { ...turn, ...change(turn) } : turn)));

    // Whatever the model looked at becomes the citation list, so the sections shown are
    // the ones actually consulted rather than a guess made before the answer existed.
    const consulted = new Map<string, Source>();

    async function runTool(name: string, args: Record<string, unknown>) {
      const res = await fetch("/api/passages", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(
          name === "read_section"
            ? { tool: "read", path: args.path }
            : { tool: "search", query: args.query, limit: args.limit, book: bookSlug },
        ),
      });
      const data = (await res.json()) as {
        results?: { path: string; title: string; chapter: string; excerpt: string; score?: number }[];
      };

      for (const hit of data.results ?? []) {
        consulted.set(hit.path, { title: hit.title, chapter: hit.chapter, href: hit.path });
      }
      patch(() => ({ sources: [...consulted.values()] }));
      return data;
    }

    try {
      // Fetched before asking: a local BM25 lookup costs a fraction of a model round
      // trip, and having it in hand usually saves one.
      // A greeting is not a lookup: searching for it turns up whichever section happens
      // to contain the word, and the model then answers as though it had been asked
      // about those topics.
      let primed: string | undefined;
      if (!smallTalk(q)) {
        const opening = (await runTool("search_book", { query: q })) as {
          results?: unknown[];
        };
        if (opening.results?.length) {
          primed = `Passages from the book:\n${JSON.stringify(opening.results)}`;
        }
      }

      for await (const piece of askModel(config, q, SYSTEM, runTool, (name, args) =>
        patch((turn) => ({
          lookups: [
            ...turn.lookups,
            name === "read_section" ? `Reading ${args.path}` : `Searching for “${args.query}”`,
          ],
        })),
        primed,
      )) {
        patch((turn) => ({ answer: turn.answer + piece }));
      }
    } catch (err) {
      patch(() => ({ error: err instanceof Error ? err.message : "That did not work." }));
    } finally {
      setBusy(false);
    }
  }

  if (!open) return null;

  return (
    <aside className="ask">
      <div className="ask-head">
        <Sparkles size={13} strokeWidth={1.8} />
        <span className="grow">Ask this book</span>
        {config && !editingKey ? (
          <button type="button" onClick={() => setEditingKey(true)} title="Change your key">
            <KeyRound size={13} strokeWidth={1.8} />
          </button>
        ) : null}
        <button type="button" onClick={() => setOpen(false)} aria-label="Close">
          <X size={14} strokeWidth={1.8} />
        </button>
      </div>

      {editingKey ? (
        <AiKeyForm
          config={config}
          onDone={(cfg) => {
            setConfig(cfg);
            setEditingKey(false);
          }}
          onCancel={config ? () => setEditingKey(false) : undefined}
        />
      ) : (
        <>
          <div className="ask-log" ref={log}>
            {turns.map((turn, i) => (
              <div className="ask-turn" key={i}>
                <p className="ask-q">{turn.question}</p>
                {turn.error ? (
                  <p className="ask-error">{turn.error}</p>
                ) : (
                  <>
                    {turn.lookups.length ? (
                      <ul className="ask-lookups">
                        {turn.lookups.map((l, k) => (
                          <li key={k}>{l}</li>
                        ))}
                      </ul>
                    ) : null}
                    <div className="ask-a">
                      {turn.answer ||
                        (turn.lookups.length ? null : (
                          <span className="ask-wait">
                            <Loader2 size={13} className="spin" strokeWidth={2} /> Thinking…
                          </span>
                        ))}
                    </div>
                    {turn.answer && turn.sources.length ? (
                      <ol className="ask-sources">
                        {turn.sources.map((s) => (
                          <li key={s.href}>
                            <Link href={s.href}>{s.title}</Link>
                            <span>{s.chapter}</span>
                          </li>
                        ))}
                      </ol>
                    ) : null}
                  </>
                )}
              </div>
            ))}
          </div>

          <div className="ask-field">
            <textarea
              ref={input}
              rows={2}
              value={question}
              placeholder="Ask about anything in this book…"
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  ask();
                }
              }}
            />
            <button type="button" onClick={ask} disabled={busy || !question.trim()}>
              <CornerDownLeft size={13} strokeWidth={1.9} />
            </button>
          </div>
        </>
      )}
    </aside>
  );
}
