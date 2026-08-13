"use client";

import { useEffect, useRef, useState } from "react";
import type { Heading } from "@/lib/markdown";

const TICKS = 21;
/** A mark's label is 14px tall; below this two of them print on top of each other. */
const MIN_GAP_PX = 17;

type Mark = { id: string; text: string; at: number };

/**
 * The outline ruler down the right edge: reading progress, one mark per heading, and a
 * scrubber. Clicking anywhere on it jumps to that point in the page — not only to a
 * heading — and hovering names the heading you are pointing at, so the ruler can be read
 * before it is used.
 */
export default function Ruler({ headings }: { headings: Heading[] }) {
  const [pct, setPct] = useState(0);
  const [marks, setMarks] = useState<Mark[]>([]);
  const [here, setHere] = useState<string | null>(null);
  const [hover, setHover] = useState<{ at: number; label: string } | null>(null);
  const gauge = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!headings.length) return;

    function measure() {
      const doc = document.documentElement;
      const height = doc.scrollHeight - window.innerHeight;
      const placed = headings
        .map((h) => {
          const el = document.getElementById(h.id);
          if (!el) return null;
          const top = el.getBoundingClientRect().top + window.scrollY;
          return { id: h.id, text: h.text, at: height > 0 ? Math.min(top / height, 1) : 0 };
        })
        .filter((m): m is Mark => m !== null);

      // Headings that sit close together in a long page land on nearly the same pixel,
      // and their labels print on top of one another. Push each one down until it clears
      // the previous by a label's height, then pull the whole run back inside the gauge.
      const room = gauge.current?.clientHeight ?? window.innerHeight;
      const gap = room > 0 ? MIN_GAP_PX / room : 0;

      for (let i = 1; i < placed.length; i++) {
        if (placed[i].at - placed[i - 1].at < gap) placed[i].at = placed[i - 1].at + gap;
      }
      const overflow = placed.length ? placed[placed.length - 1].at - 1 : 0;
      if (overflow > 0) {
        const scale = 1 / (1 + overflow);
        for (const mark of placed) mark.at *= scale;
      }

      setMarks(placed);
    }

    // A scroll event fires many times a frame. Re-rendering on each one made the ruler
    // fight the browser's smooth scrolling, so the work is collapsed into one frame.
    let frame = 0;
    function onScroll() {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(update);
    }

    function update() {
      const doc = document.documentElement;
      const height = doc.scrollHeight - window.innerHeight;
      setPct(height > 0 ? Math.round((window.scrollY / height) * 100) : 0);

      // "Here" is the last heading whose top has passed the reading line, a third of
      // the way down the viewport — the point the eye actually sits at.
      const line = window.scrollY + window.innerHeight / 3;
      let current: string | null = null;
      for (const h of headings) {
        const el = document.getElementById(h.id);
        if (el && el.getBoundingClientRect().top + window.scrollY <= line) current = h.id;
      }
      setHere(current);
    }

    measure();
    update();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", measure);
    // Images and diagrams settle after mount and change the page height, so remeasure
    // when they do — but on the next frame, never mid-scroll.
    const observer = new ResizeObserver(() => {
      measure();
      onScroll();
    });
    const paper = document.querySelector(".paper");
    if (paper) observer.observe(paper);
    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", measure);
      observer.disconnect();
    };
  }, [headings]);

  /** Where in the page a point on the ruler corresponds to, as a fraction. */
  function fractionAt(clientY: number) {
    const box = gauge.current?.getBoundingClientRect();
    if (!box || box.height === 0) return 0;
    return Math.min(1, Math.max(0, (clientY - box.top) / box.height));
  }

  function scrubTo(clientY: number) {
    const height = document.documentElement.scrollHeight - window.innerHeight;
    window.scrollTo({ top: fractionAt(clientY) * height, behavior: "smooth" });
  }

  if (!headings.length) return null;

  return (
    <div className="ruler">
      <div
        className="rail"
        onClick={(e) => scrubTo(e.clientY)}
        onMouseMove={(e) => {
          const at = fractionAt(e.clientY);
          // Name the heading this point belongs to: the last one at or above it.
          const nearest = [...marks].reverse().find((m) => m.at <= at + 0.005);
          setHover({ at, label: nearest?.text ?? "Top of the page" });
        }}
        onMouseLeave={() => setHover(null)}
        title="Click to jump"
      />
      <div className="gauge" ref={gauge}>
        {/* The readout shares its lane with the marks. Rather than print "100%" across a
            heading's tick, it yields whenever one is within a line's height of it. */}
        {hover || marks.some((m) => Math.abs(m.at * 100 - pct) < 2.5) ? null : (
          <div className="pct" style={{ top: `${pct}%` }}>
            {pct}%
          </div>
        )}

        {hover ? (
          <div className="scrub" style={{ top: `${hover.at * 100}%` }}>
            <span className="scrub-label">{hover.label}</span>
            <i />
          </div>
        ) : null}

        <div className="ticks">
          {Array.from({ length: TICKS }, (_, i) => (
            <i key={i} className={pct >= (i / (TICKS - 1)) * 100 ? "on" : undefined} />
          ))}
        </div>

        <div className="marks">
          {marks.map((m) => (
            <a
              key={m.id}
              className={`mark${here === m.id ? " here" : ""}`}
              href={`#${m.id}`}
              style={{ top: `${m.at * 100}%` }}
              title={m.text}
            >
              <span className="lbl">{m.text}</span>
              <i />
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}
