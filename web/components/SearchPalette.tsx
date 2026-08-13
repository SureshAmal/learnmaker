"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Search, CornerDownLeft, ArrowUp, ArrowDown } from "lucide-react";
import type { Hit } from "@/lib/content";

/**
 * Ctrl+K search. Queries run against Postgres full-text on the server, so the client
 * never downloads an index — the books are large enough that shipping one would cost
 * more than the round trip does.
 */
export default function SearchPalette({ bookSlug }: { bookSlug?: string }) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [hits, setHits] = useState<Hit[]>([]);
  const [cursor, setCursor] = useState(0);
  const input = useRef<HTMLInputElement>(null);
  const results = useRef<HTMLDivElement>(null);
  const router = useRouter();

  // Arrow keys move the highlight past the bottom of the list, so the list has to follow
  // it. `nearest` keeps the mouse-driven case from jumping the scroll around.
  useEffect(() => {
    const active = results.current?.querySelector<HTMLElement>(".hit.on");
    active?.scrollIntoView({ block: "nearest" });
  }, [cursor, hits]);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen((v) => !v);
      }
      if (e.key === "Escape") setOpen(false);
    }
    window.addEventListener("keydown", onKey);
    // The topbar button and the palette live in different trees, so they meet on an event.
    const show = () => setOpen(true);
    window.addEventListener("learn:search", show);
    return () => {
      window.removeEventListener("keydown", onKey);
      window.removeEventListener("learn:search", show);
    };
  }, []);

  useEffect(() => {
    if (open) input.current?.focus();
  }, [open]);

  useEffect(() => {
    const q = query.trim();
    if (!q) {
      setHits([]);
      return;
    }
    // Typing is faster than the round trip; debounce and drop stale answers.
    const ac = new AbortController();
    const timer = setTimeout(async () => {
      try {
        const url = `/api/search?q=${encodeURIComponent(q)}${bookSlug ? `&book=${bookSlug}` : ""}`;
        const res = await fetch(url, { signal: ac.signal });
        const data = (await res.json()) as { hits: Hit[] };
        setHits(data.hits ?? []);
        setCursor(0);
      } catch {
        /* aborted or offline: keep the previous results */
      }
    }, 140);
    return () => {
      clearTimeout(timer);
      ac.abort();
    };
  }, [query, bookSlug]);

  const go = useCallback(
    (hit: Hit) => {
      setOpen(false);
      setQuery("");
      router.push(`/${hit.book}/${hit.chapter}/${hit.section}`);
    },
    [router],
  );

  if (!open) return null;

  return (
    <div className="palette" onMouseDown={(e) => e.target === e.currentTarget && setOpen(false)}>
      <div className="palette-box">
        <div className="palette-field">
          <Search size={16} strokeWidth={1.7} />
          <input
            ref={input}
            type="search"
            placeholder="Search every page…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "ArrowDown") {
                e.preventDefault();
                setCursor((c) => Math.min(c + 1, hits.length - 1));
              } else if (e.key === "ArrowUp") {
                e.preventDefault();
                setCursor((c) => Math.max(c - 1, 0));
              } else if (e.key === "Enter" && hits[cursor]) {
                e.preventDefault();
                go(hits[cursor]);
              }
            }}
          />
          <span className="esc">ESC</span>
        </div>

        <div className="palette-results" ref={results}>
          {hits.length === 0 ? (
            <p className="palette-empty">
              {query.trim() ? "Nothing matched." : "Type to search."}
            </p>
          ) : (
            hits.map((hit, i) => (
              <a
                key={`${hit.book}/${hit.chapter}/${hit.section}`}
                className={`hit${i === cursor ? " on" : ""}`}
                href={`/${hit.book}/${hit.chapter}/${hit.section}`}
                onMouseEnter={() => setCursor(i)}
                onClick={(e) => {
                  e.preventDefault();
                  go(hit);
                }}
              >
                <div className="hit-where">
                  {hit.book_title} · {hit.chapter_title}
                </div>
                <div className="hit-title">{hit.title}</div>
                {/* the snippet is ts_headline output: server-built, <mark> only */}
                <div className="hit-snip" dangerouslySetInnerHTML={{ __html: hit.snippet }} />
              </a>
            ))
          )}
        </div>

        <div className="palette-foot">
          <span>
            <kbd>
              <ArrowUp size={9} />
            </kbd>
            <kbd>
              <ArrowDown size={9} />
            </kbd>
            Move
          </span>
          <span>
            <kbd>
              <CornerDownLeft size={9} />
            </kbd>
            Open
          </span>
          <span className="hits">{hits.length} results</span>
        </div>
      </div>
    </div>
  );
}
