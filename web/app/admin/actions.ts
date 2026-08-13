"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { sql } from "@/lib/db";
import { requireAdmin, checkCredentials, issueSession, clearSession } from "@/lib/auth";
import { slugify, uniqueSlug } from "@/lib/slug";

// ---------------------------------------------------------------------------------
// session
// ---------------------------------------------------------------------------------

export async function signIn(_prev: { error?: string } | undefined, form: FormData) {
  const user = String(form.get("user") ?? "");
  const password = String(form.get("password") ?? "");
  const next = String(form.get("next") ?? "/admin");

  if (!checkCredentials(user, password)) {
    // One message for both failure modes, so the form cannot be used to find out
    // whether a username exists.
    return { error: "Wrong username or password." };
  }
  await issueSession(user);
  redirect(next.startsWith("/") ? next : "/admin");
}

export async function signOut() {
  await clearSession();
  redirect("/admin/login");
}

// ---------------------------------------------------------------------------------
// cache
// ---------------------------------------------------------------------------------

/**
 * The reading pages are statically cached, so every write has to say what it invalidated.
 * Book-level changes (a rename, a reorder) touch the sidebar on every page of that book,
 * which is why this clears the whole subtree rather than one path.
 */
async function refreshBook(bookId: number) {
  const [book] = await sql<{ slug: string }[]>`select slug from books where id = ${bookId}`;

  // Structural edits — archiving, reordering, renaming — change the contents shown on
  // every page of the book, not just the one that was touched. Purging the concrete
  // paths alone left the cover and the sidebars serving a prerender from before the
  // change, so the route patterns are cleared too: that is what drops every cached
  // instance of a dynamic route.
  revalidatePath("/", "page");
  revalidatePath("/[book]", "page");
  revalidatePath("/[book]/[chapter]/[section]", "page");
  if (book) {
    revalidatePath(`/${book.slug}`, "layout");
    revalidatePath(`/${book.slug}`, "page");
  }
}

async function bookIdOfChapter(chapterId: number) {
  const [row] = await sql<{ book_id: number }[]>`
    select book_id from chapters where id = ${chapterId}
  `;
  return row?.book_id ?? null;
}

async function bookIdOfSection(sectionId: number) {
  const [row] = await sql<{ book_id: number }[]>`
    select c.book_id from sections s join chapters c on c.id = s.chapter_id
     where s.id = ${sectionId}
  `;
  return row?.book_id ?? null;
}

// ---------------------------------------------------------------------------------
// books
// ---------------------------------------------------------------------------------

export async function createBook(form: FormData) {
  await requireAdmin();
  const title = String(form.get("title") ?? "").trim();
  if (!title) return;

  const taken = await sql<{ slug: string }[]>`select slug from books`;
  const slug = uniqueSlug(
    slugify(String(form.get("slug") ?? "") || title),
    taken.map((r) => r.slug),
  );

  const [{ position }] = await sql<{ position: number }[]>`
    select coalesce(max(position), 0) + 1 as position from books
  `;

  const [book] = await sql<{ id: number }[]>`
    insert into books (slug, title, subtitle, blurb, source_url, license, position)
    values (${slug}, ${title}, ${String(form.get("subtitle") ?? "")},
            ${String(form.get("blurb") ?? "")}, ${String(form.get("source_url") ?? "")},
            ${String(form.get("license") ?? "")}, ${position})
    returning id
  `;

  revalidatePath("/", "page");
  revalidatePath("/admin");
  // Straight into the book, which asks for its first chapter by name rather than
  // inventing a "Chapter 1" the author then has to rename.
  redirect(`/admin/edit/${slug}`);
}

export async function updateBook(form: FormData) {
  await requireAdmin();
  const id = Number(form.get("id"));
  const title = String(form.get("title") ?? "").trim();
  if (!id || !title) return;

  const taken = await sql<{ slug: string }[]>`select slug from books where id <> ${id}`;
  const slug = uniqueSlug(
    slugify(String(form.get("slug") ?? "") || title),
    taken.map((r) => r.slug),
  );

  await sql`
    update books set
      slug = ${slug},
      title = ${title},
      subtitle = ${String(form.get("subtitle") ?? "")},
      blurb = ${String(form.get("blurb") ?? "")},
      source_url = ${String(form.get("source_url") ?? "")},
      license = ${String(form.get("license") ?? "")},
      published = ${form.get("published") === "on"},
      updated_at = now()
    where id = ${id}
  `;

  await refreshBook(id);
  revalidatePath("/admin", "layout");
  redirect(`/admin/edit/${slug}/settings`);
}

/** Show or hide a book on the public shelf without opening its settings. */
export async function togglePublished(form: FormData) {
  await requireAdmin();
  const id = Number(form.get("id"));
  if (!id) return;
  await sql`update books set published = not published, updated_at = now() where id = ${id}`;
  await refreshBook(id);
  revalidatePath("/admin");
}

/**
 * Archiving, not deleting. The row keeps its content and its place; `deleted_at` takes
 * it off the shelf, out of search and out of the normal admin lists, and the archive
 * page can put it back. Nothing an editor clicks destroys writing.
 */
export async function archiveBook(form: FormData) {
  await requireAdmin();
  const id = Number(form.get("id"));
  if (!id) return;
  const [book] = await sql<{ slug: string }[]>`select slug from books where id = ${id}`;
  await sql`update books set deleted_at = now() where id = ${id}`;
  if (book) revalidatePath(`/${book.slug}`, "layout");
  revalidatePath("/", "page");
  revalidatePath("/admin");
  redirect("/admin");
}

export async function restoreBook(form: FormData) {
  await requireAdmin();
  const id = Number(form.get("id"));
  if (!id) return;
  await sql`update books set deleted_at = null where id = ${id}`;
  await refreshBook(id);
  revalidatePath("/admin");
  revalidatePath("/admin/archive");
}

/** The only call that actually removes content, and only from the archive. */
export async function purgeBook(form: FormData) {
  await requireAdmin();
  const id = Number(form.get("id"));
  if (!id) return;
  await sql`delete from books where id = ${id} and deleted_at is not null`;
  revalidatePath("/admin/archive");
  redirect("/admin/archive");
}

// ---------------------------------------------------------------------------------
// chapters
// ---------------------------------------------------------------------------------

export async function createChapter(form: FormData) {
  await requireAdmin();
  const bookId = Number(form.get("book_id"));
  const title = String(form.get("title") ?? "").trim();
  if (!bookId || !title) return;

  const taken = await sql<{ slug: string }[]>`
    select slug from chapters where book_id = ${bookId}
  `;
  const slug = uniqueSlug(slugify(title), taken.map((r) => r.slug));
  const [{ position }] = await sql<{ position: number }[]>`
    select coalesce(max(position), 0) + 1 as position from chapters where book_id = ${bookId}
  `;

  await sql`
    insert into chapters (book_id, slug, title, position)
    values (${bookId}, ${slug}, ${title}, ${position})
  `;

  const [book] = await sql<{ slug: string }[]>`select slug from books where id = ${bookId}`;
  await refreshBook(bookId);
  revalidatePath("/admin", "layout");
  // The chapter's own page asks for its first section.
  if (book) redirect(`/admin/edit/${book.slug}/${slug}`);
}

export async function updateChapter(form: FormData) {
  await requireAdmin();
  const id = Number(form.get("id"));
  const title = String(form.get("title") ?? "").trim();
  if (!id || !title) return;

  const bookId = await bookIdOfChapter(id);
  if (!bookId) return;

  const taken = await sql<{ slug: string }[]>`
    select slug from chapters where book_id = ${bookId} and id <> ${id}
  `;
  const slug = uniqueSlug(
    slugify(String(form.get("slug") ?? "") || title),
    taken.map((r) => r.slug),
  );

  await sql`
    update chapters set slug = ${slug}, title = ${title}, updated_at = now()
     where id = ${id}
  `;

  await refreshBook(bookId);
  revalidatePath("/admin", "layout");

  const [book] = await sql<{ slug: string }[]>`select slug from books where id = ${bookId}`;
  if (book) redirect(`/admin/edit/${book.slug}/${slug}`);
}


/**
 * Where to send an editor after the page they were on stops existing.
 *
 * Archiving from the contents list is normally done while standing on that very page, so
 * leaving the browser at its URL means a 404. This picks the nearest surviving page —
 * preferring one in the same chapter — and falls back to the book's settings when the
 * book has nothing left to show.
 */
async function nextLivePage(bookId: number, preferChapterId: number | null) {
  const [row] = await sql<{ book: string; chapter: string; section: string }[]>`
    select b.slug as book, c.slug as chapter, s.slug as section
      from sections s
      join chapters c on c.id = s.chapter_id
      join books b on b.id = c.book_id
     where b.id = ${bookId}
       and s.deleted_at is null and c.deleted_at is null
     order by case when c.id = ${preferChapterId ?? 0} then 0 else 1 end,
              c.position, s.position
     limit 1
  `;
  if (row) return `/admin/edit/${row.book}/${row.chapter}/${row.section}`;

  // Nothing left to show: the book's own page offers the first chapter.
  const [book] = await sql<{ slug: string }[]>`select slug from books where id = ${bookId}`;
  return book ? `/admin/edit/${book.slug}` : "/admin";
}

export async function archiveChapter(form: FormData) {
  await requireAdmin();
  const id = Number(form.get("id"));
  if (!id) return;
  const bookId = await bookIdOfChapter(id);
  await sql`update chapters set deleted_at = now() where id = ${id}`;
  if (!bookId) return;

  await refreshBook(bookId);
  revalidatePath("/admin", "layout");
  redirect(await nextLivePage(bookId, null));
}

export async function restoreChapter(form: FormData) {
  await requireAdmin();
  const id = Number(form.get("id"));
  if (!id) return;
  const bookId = await bookIdOfChapter(id);
  await sql`update chapters set deleted_at = null where id = ${id}`;
  if (bookId) await refreshBook(bookId);
  revalidatePath("/admin/archive");
}

export async function purgeChapter(form: FormData) {
  await requireAdmin();
  const id = Number(form.get("id"));
  if (!id) return;
  await sql`delete from chapters where id = ${id} and deleted_at is not null`;
  revalidatePath("/admin/archive");
}

// ---------------------------------------------------------------------------------
// sections
// ---------------------------------------------------------------------------------

export async function createSection(form: FormData) {
  await requireAdmin();
  const chapterId = Number(form.get("chapter_id"));
  const title = String(form.get("title") ?? "").trim();
  if (!chapterId || !title) return;

  const taken = await sql<{ slug: string }[]>`
    select slug from sections where chapter_id = ${chapterId}
  `;
  const slug = uniqueSlug(slugify(title), taken.map((r) => r.slug));
  const [{ position }] = await sql<{ position: number }[]>`
    select coalesce(max(position), 0) + 1 as position from sections
     where chapter_id = ${chapterId}
  `;

  await sql`
    insert into sections (chapter_id, slug, title, body, position)
    values (${chapterId}, ${slug}, ${title}, '', ${position})
  `;

  const [where] = await sql<{ book: string; chapter: string }[]>`
    select b.slug as book, c.slug as chapter
      from chapters c join books b on b.id = c.book_id
     where c.id = ${chapterId}
  `;

  const bookId = await bookIdOfChapter(chapterId);
  if (bookId) await refreshBook(bookId);
  revalidatePath("/admin", "layout");
  if (where) redirect(`/admin/edit/${where.book}/${where.chapter}/${slug}`);
}

/** Metadata only — the body is saved by the editor through /api/admin/section. */
export async function updateSectionMeta(form: FormData) {
  await requireAdmin();
  const id = Number(form.get("id"));
  const title = String(form.get("title") ?? "").trim();
  if (!id || !title) return;

  const [row] = await sql<{ chapter_id: number }[]>`
    select chapter_id from sections where id = ${id}
  `;
  if (!row) return;

  const taken = await sql<{ slug: string }[]>`
    select slug from sections where chapter_id = ${row.chapter_id} and id <> ${id}
  `;
  const slug = uniqueSlug(
    slugify(String(form.get("slug") ?? "") || title),
    taken.map((r) => r.slug),
  );

  await sql`
    update sections set slug = ${slug}, title = ${title},
                        dek = ${String(form.get("dek") ?? "")}, updated_at = now()
     where id = ${id}
  `;

  const bookId = await bookIdOfSection(id);
  if (bookId) await refreshBook(bookId);
  revalidatePath("/admin", "layout");

  const [where] = await sql<{ book: string; chapter: string }[]>`
    select b.slug as book, c.slug as chapter
      from sections s
      join chapters c on c.id = s.chapter_id
      join books b on b.id = c.book_id
     where s.id = ${id}
  `;
  if (where) redirect(`/admin/edit/${where.book}/${where.chapter}/${slug}`);
}

export async function archiveSection(form: FormData) {
  await requireAdmin();
  const id = Number(form.get("id"));
  if (!id) return;
  const [row] = await sql<{ chapter_id: number }[]>`
    select chapter_id from sections where id = ${id}
  `;
  const bookId = await bookIdOfSection(id);
  await sql`update sections set deleted_at = now() where id = ${id}`;
  if (bookId) await refreshBook(bookId);
  if (!row || !bookId) return;
  revalidatePath("/admin", "layout");
  // The archived page may well be the one being looked at, so always land somewhere real.
  redirect(await nextLivePage(bookId, row.chapter_id));
}

export async function restoreSection(form: FormData) {
  await requireAdmin();
  const id = Number(form.get("id"));
  if (!id) return;
  const bookId = await bookIdOfSection(id);
  await sql`update sections set deleted_at = null where id = ${id}`;
  if (bookId) await refreshBook(bookId);
  revalidatePath("/admin/archive");
}

export async function purgeSection(form: FormData) {
  await requireAdmin();
  const id = Number(form.get("id"));
  if (!id) return;
  await sql`delete from sections where id = ${id} and deleted_at is not null`;
  revalidatePath("/admin/archive");
}

/**
 * Writes a whole sibling order at once, which is what a drag-and-drop list needs: the
 * browser already knows the arrangement it wants, and sending it in one call avoids the
 * flicker of replaying a sequence of swaps.
 */
export async function reorder(kind: "chapter" | "section", parentId: number, ids: number[]) {
  await requireAdmin();
  if (!ids.length) return;

  // Positions are rewritten from the given order; the parent is checked so a stray id
  // from another chapter cannot be spliced in.
  if (kind === "chapter") {
    await sql`
      update chapters set position = data.position, updated_at = now()
        from (select * from unnest(${ids}::int[]) with ordinality as t(id, position)) as data
       where chapters.id = data.id and chapters.book_id = ${parentId}
    `;
    await refreshBook(parentId);
  } else {
    await sql`
      update sections set position = data.position, updated_at = now()
        from (select * from unnest(${ids}::int[]) with ordinality as t(id, position)) as data
       where sections.id = data.id and sections.chapter_id = ${parentId}
    `;
    const bookId = await bookIdOfChapter(parentId);
    if (bookId) await refreshBook(bookId);
  }

  revalidatePath("/admin", "layout");
}

// ---------------------------------------------------------------------------------
// media
// ---------------------------------------------------------------------------------

export async function deleteAsset(form: FormData) {
  await requireAdmin();
  const id = Number(form.get("id"));
  if (!id) return;
  // Pages that already reference the image keep their Markdown; the picture simply stops
  // resolving, which is visible in the editor preview straight away.
  await sql`delete from assets where id = ${id}`;
  revalidatePath("/admin/media");
}

// ---------------------------------------------------------------------------------
// ordering
// ---------------------------------------------------------------------------------

/**
 * Moves one row up or down among its siblings by swapping positions with its neighbour.
 * Positions are rewritten densely first, so a list that arrived with gaps or ties (an
 * import, say) still reorders predictably.
 */
export async function move(form: FormData) {
  await requireAdmin();
  const kind = String(form.get("kind")); // "book" | "chapter" | "section"
  const id = Number(form.get("id"));
  const dir = String(form.get("dir")) === "up" ? -1 : 1;
  if (!id) return;

  if (kind === "book") {
    await sql`
      with ranked as (
        select id, row_number() over (order by position, id) as rn from books
      )
      update books b set position = ranked.rn from ranked where ranked.id = b.id
    `;
    const [row] = await sql<{ position: number }[]>`select position from books where id = ${id}`;
    if (!row) return;
    await sql`
      update books set position = case when id = ${id} then position + ${dir}
                                       else position - ${dir} end
       where id = ${id} or position = ${row.position + dir}
    `;
    revalidatePath("/", "page");
    revalidatePath("/admin");
    return;
  }

  if (kind === "chapter") {
    const bookId = await bookIdOfChapter(id);
    if (!bookId) return;
    await sql`
      with ranked as (
        select id, row_number() over (order by position, id) as rn
          from chapters where book_id = ${bookId}
      )
      update chapters c set position = ranked.rn from ranked where ranked.id = c.id
    `;
    const [row] = await sql<{ position: number }[]>`
      select position from chapters where id = ${id}
    `;
    if (!row) return;
    await sql`
      update chapters set position = case when id = ${id} then position + ${dir}
                                          else position - ${dir} end
       where book_id = ${bookId} and (id = ${id} or position = ${row.position + dir})
    `;
    await refreshBook(bookId);
    return;
  }

  const [section] = await sql<{ chapter_id: number }[]>`
    select chapter_id from sections where id = ${id}
  `;
  if (!section) return;
  await sql`
    with ranked as (
      select id, row_number() over (order by position, id) as rn
        from sections where chapter_id = ${section.chapter_id}
    )
    update sections s set position = ranked.rn from ranked where ranked.id = s.id
  `;
  const [row] = await sql<{ position: number }[]>`select position from sections where id = ${id}`;
  if (!row) return;
  await sql`
    update sections set position = case when id = ${id} then position + ${dir}
                                        else position - ${dir} end
     where chapter_id = ${section.chapter_id}
       and (id = ${id} or position = ${row.position + dir})
  `;
  const bookId = await bookIdOfSection(id);
  if (bookId) await refreshBook(bookId);
}
