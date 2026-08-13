"use client";

import Link from "next/link";
import { ChevronLeft, ChevronRight, Search, Sparkles } from "lucide-react";
import ThemeToggle from "./ThemeToggle";

export default function Topbar({
  crumbs,
  prev,
  next,
  ask = false,
}: {
  crumbs: string[];
  prev?: string | null;
  next?: string | null;
  /** Whether this deployment has a model configured. */
  ask?: boolean;
}) {
  return (
    <div className="topbar">
      {prev ? (
        <Link className="nudge" href={prev} aria-label="Previous page">
          <ChevronLeft size={15} strokeWidth={1.7} />
        </Link>
      ) : (
        <span className="nudge off">
          <ChevronLeft size={15} strokeWidth={1.7} />
        </span>
      )}
      {next ? (
        <Link className="nudge" href={next} aria-label="Next page">
          <ChevronRight size={15} strokeWidth={1.7} />
        </Link>
      ) : (
        <span className="nudge off">
          <ChevronRight size={15} strokeWidth={1.7} />
        </span>
      )}

      <div className="crumb">
        {crumbs.map((c, i) => (
          <span key={i} className={i === crumbs.length - 1 ? "here" : undefined}>
            {i > 0 ? <b>/</b> : null}
            {c}
          </span>
        ))}
      </div>

      {ask ? (
        <button
          className="find"
          type="button"
          onClick={() => window.dispatchEvent(new Event("learn:ask"))}
          title="Ask this book"
        >
          <Sparkles size={14} strokeWidth={1.7} />
          <span>Ask</span>
        </button>
      ) : null}
      <button
        className="find"
        type="button"
        onClick={() => window.dispatchEvent(new Event("learn:search"))}
      >
        <Search size={14} strokeWidth={1.7} />
        <span>Search</span>
        <kbd>Ctrl K</kbd>
      </button>
      <ThemeToggle />
    </div>
  );
}
