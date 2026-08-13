"use client";

import { useState, useTransition } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { GripVertical, Plus, Archive, ExternalLink, Menu, Settings } from "lucide-react";
import type { Toc } from "@/lib/content";
import { reorder, createChapter, createSection, archiveChapter, archiveSection } from "@/app/admin/actions";

/**
 * The contents, exactly where a reader sees them, but editable in place: drag to
 * reorder, a button to add, a button to archive. Everything is one click from the page
 * it changes, which is the point of editing on the real layout rather than in a
 * separate list screen.
 */

/** What is being dragged, and what it is currently hovering over. */
type Drag =
  | { kind: "section"; chapter: string; slug: string }
  | { kind: "chapter"; slug: string }
  | null;

type Over = { kind: "section" | "chapter"; slug: string; after: boolean } | null;

export default function EditSidebar({
  bookSlug,
  bookTitle,
  bookId,
  toc,
  ids,
}: {
  bookSlug: string;
  bookTitle: string;
  bookId: number;
  toc: Toc;
  /** slug → database id, for the chapters and sections shown. */
  ids: { chapters: Record<string, number>; sections: Record<string, number> };
}) {
  const pathname = usePathname();
  const router = useRouter();
  const [pending, startTransition] = useTransition();
  const [adding, setAdding] = useState<string | null>(null);
  const [drag, setDrag] = useState<Drag>(null);
  const [over, setOver] = useState<Over>(null);

  /** Which half of the row the pointer is in decides whether the item lands before or after. */
  function edge(e: React.DragEvent<HTMLElement>) {
    const box = e.currentTarget.getBoundingClientRect();
    return e.clientY > box.top + box.height / 2;
  }

  /** Moves `from` to sit before or after `to`, and returns the new order. */
  function rearrange(order: string[], from: string, to: string, after: boolean) {
    const next = order.filter((slug) => slug !== from);
    const at = next.indexOf(to);
    if (at < 0) return null;
    next.splice(after ? at + 1 : at, 0, from);
    return next.join() === order.join() ? null : next;
  }

  function commit(run: () => Promise<void>) {
    startTransition(async () => {
      await run();
      router.refresh();
    });
    setDrag(null);
    setOver(null);
  }

  function dropSection(chapterSlug: string, targetSlug: string, after: boolean) {
    if (drag?.kind !== "section" || drag.chapter !== chapterSlug) return;
    const chapter = toc.find((c) => c.slug === chapterSlug);
    if (!chapter) return;

    const next = rearrange(
      chapter.sections.map((s) => s.slug),
      drag.slug,
      targetSlug,
      after,
    );
    if (!next) {
      setDrag(null);
      setOver(null);
      return;
    }

    commit(() =>
      reorder(
        "section",
        ids.chapters[chapterSlug],
        next.map((slug) => ids.sections[`${chapterSlug}/${slug}`]).filter(Boolean),
      ),
    );
  }

  function dropChapter(targetSlug: string, after: boolean) {
    if (drag?.kind !== "chapter") return;
    const next = rearrange(toc.map((c) => c.slug), drag.slug, targetSlug, after);
    if (!next) {
      setDrag(null);
      setOver(null);
      return;
    }
    commit(() => reorder("chapter", bookId, next.map((slug) => ids.chapters[slug]).filter(Boolean)));
  }

  const marker = (kind: "section" | "chapter", slug: string) =>
    over?.kind === kind && over.slug === slug ? (over.after ? " drop-after" : " drop-before") : "";

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

      <nav className={`sidebar edit-sidebar${pending ? " busy" : ""}`}>
        <Link className="logo" href="/admin">
          ← EDITOR
        </Link>

        <section>
          <h2 style={{ display: "flex", alignItems: "center", gap: 2 }}>
            <span style={{ flex: 1 }}>{bookTitle}</span>
            <Link
              className="nudge"
              href={`/admin/edit/${bookSlug}/settings`}
              title="Book settings"
            >
              <Settings size={13} strokeWidth={1.7} />
            </Link>
            <Link className="nudge" href={`/${bookSlug}`} target="_blank" title="View live">
              <ExternalLink size={13} strokeWidth={1.7} />
            </Link>
          </h2>
        </section>

        {toc.map((chapter) => (
          <section
            key={chapter.slug}
            className={`edit-chapter-block${marker("chapter", chapter.slug)}${
              drag?.kind === "chapter" && drag.slug === chapter.slug ? " dragging" : ""
            }`}
            onDragOver={(e) => {
              if (drag?.kind !== "chapter") return;
              e.preventDefault();
              setOver({ kind: "chapter", slug: chapter.slug, after: edge(e) });
            }}
            onDrop={(e) => {
              if (drag?.kind !== "chapter") return;
              e.preventDefault();
              dropChapter(chapter.slug, edge(e));
            }}
          >
            <h2
              className="edit-chapter"
              draggable
              onDragStart={() => setDrag({ kind: "chapter", slug: chapter.slug })}
              onDragEnd={() => {
                setDrag(null);
                setOver(null);
              }}
            >
              <GripVertical className="grip" size={12} strokeWidth={1.7} />
              <span style={{ flex: 1 }}>{chapter.title}</span>
              <button
                className="nudge"
                title="Add a section"
                onClick={() => setAdding(adding === chapter.slug ? null : chapter.slug)}
              >
                <Plus size={13} strokeWidth={2} />
              </button>
              <Link
                className="nudge"
                href={`/admin/edit/${bookSlug}/${chapter.slug}/settings`}
                title="Rename this chapter"
              >
                <Settings size={12} strokeWidth={1.7} />
              </Link>
              <form action={archiveChapter}>
                <input type="hidden" name="id" value={ids.chapters[chapter.slug]} />
                <button className="nudge" title="Archive this chapter" type="submit">
                  <Archive size={13} strokeWidth={1.7} />
                </button>
              </form>
            </h2>

            {adding === chapter.slug ? (
              <form action={createSection} className="edit-add" onSubmit={() => setAdding(null)}>
                <input type="hidden" name="chapter_id" value={ids.chapters[chapter.slug]} />
                <input name="title" placeholder="New section title" autoFocus required />
              </form>
            ) : null}

            <ul>
              {chapter.sections.map((section) => {
                const href = `/admin/edit/${bookSlug}/${chapter.slug}/${section.slug}`;
                const dragging =
                  drag?.kind === "section" && drag.slug === section.slug && drag.chapter === chapter.slug;
                return (
                  <li
                    key={section.slug}
                    className={`${marker("section", `${chapter.slug}/${section.slug}`)}${
                      dragging ? " dragging" : ""
                    }`}
                    draggable
                    onDragStart={(e) => {
                      e.stopPropagation();
                      setDrag({ kind: "section", chapter: chapter.slug, slug: section.slug });
                    }}
                    onDragOver={(e) => {
                      if (drag?.kind !== "section" || drag.chapter !== chapter.slug) return;
                      e.preventDefault();
                      e.stopPropagation();
                      setOver({
                        kind: "section",
                        slug: `${chapter.slug}/${section.slug}`,
                        after: edge(e),
                      });
                    }}
                    onDrop={(e) => {
                      if (drag?.kind !== "section") return;
                      e.preventDefault();
                      e.stopPropagation();
                      dropSection(chapter.slug, section.slug, edge(e));
                    }}
                    onDragEnd={() => {
                      setDrag(null);
                      setOver(null);
                    }}
                  >
                    <span className="edit-row">
                      <GripVertical className="grip" size={12} strokeWidth={1.7} />
                      <Link
                        href={href}
                        className={pathname === href ? "active" : undefined}
                        style={{ flex: 1 }}
                        draggable={false}
                      >
                        {section.title}
                      </Link>
                      <form action={archiveSection}>
                        <input
                          type="hidden"
                          name="id"
                          value={ids.sections[`${chapter.slug}/${section.slug}`]}
                        />
                        <button className="nudge" title="Archive this section" type="submit">
                          <Archive size={12} strokeWidth={1.7} />
                        </button>
                      </form>
                    </span>
                  </li>
                );
              })}
            </ul>
          </section>
        ))}

        <form action={createChapter} className="edit-add">
          <input type="hidden" name="book_id" value={bookId} />
          <input name="title" placeholder="+ New chapter" required />
        </form>
      </nav>
    </>
  );
}
