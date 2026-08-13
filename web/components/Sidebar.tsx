"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef } from "react";
import { Menu } from "lucide-react";
import type { Toc } from "@/lib/content";

const SCROLL_KEY = "learn-sidebar-scroll";

export default function Sidebar({
  bookSlug,
  bookTitle,
  toc,
  note,
}: {
  bookSlug: string;
  bookTitle: string;
  toc: Toc;
  note?: string;
}) {
  const pathname = usePathname();
  const nav = useRef<HTMLElement>(null);

  /**
   * The sidebar is a fixed element that React keeps mounted across a client-side
   * navigation, but a full page load rebuilds it at scroll 0 — which throws a reader
   * of a 250-section book back to chapter 1. The position is remembered per book, and
   * restored unless the section that is now current would be off-screen anyway.
   */
  useEffect(() => {
    const el = nav.current;
    if (!el) return;

    const key = `${SCROLL_KEY}:${bookSlug}`;
    let saved = 0;
    try {
      saved = Number(sessionStorage.getItem(key) ?? 0);
    } catch {
      /* private mode */
    }

    const active = el.querySelector<HTMLElement>("a.active");
    if (saved) el.scrollTop = saved;

    // If the restored position does not show the current section, the current section wins.
    if (active) {
      const top = active.offsetTop;
      if (top < el.scrollTop || top > el.scrollTop + el.clientHeight - 40) {
        el.scrollTop = Math.max(0, top - el.clientHeight / 2);
      }
    }

    function remember() {
      try {
        sessionStorage.setItem(key, String(el!.scrollTop));
      } catch {
        /* private mode */
      }
    }
    el.addEventListener("scroll", remember, { passive: true });
    return () => el.removeEventListener("scroll", remember);
  }, [pathname, bookSlug]);

  useEffect(() => {
    document.body.classList.remove("nav-open");
  }, [pathname]);

  return (
    <>
      <button
        className="nav-toggle"
        type="button"
        aria-label="Contents"
        onClick={() => document.body.classList.toggle("nav-open")}
      >
        <Menu size={17} strokeWidth={1.7} />
      </button>

      <nav className="sidebar" ref={nav}>
        <Link className="logo" href="/">
          ← LEARN
        </Link>

        <section>
          <h2>
            <Link href={`/${bookSlug}`} style={{ color: "inherit" }}>
              {bookTitle}
            </Link>
          </h2>
        </section>

        {toc.map((chapter) => (
          <section key={chapter.slug}>
            <h2>{chapter.title}</h2>
            <ul>
              {chapter.sections.map((section) => {
                const href = `/${bookSlug}/${chapter.slug}/${section.slug}`;
                return (
                  <li key={section.slug}>
                    <Link href={href} className={pathname === href ? "active" : undefined}>
                      {section.title}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </section>
        ))}

        {note ? <p className="side-note">{note}</p> : null}
      </nav>
    </>
  );
}
