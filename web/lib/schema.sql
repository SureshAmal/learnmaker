-- Content store. Books hold chapters, chapters hold sections; a section is one page
-- of Markdown. Everything the reader sees is derived from these three tables, so the
-- build output stays a pure function of the content.

create table if not exists books (
  id          serial primary key,
  slug        text not null unique,
  title       text not null,
  subtitle    text not null default '',
  blurb       text not null default '',
  source_url  text not null default '',
  license     text not null default '',
  position    integer not null default 0,
  published   boolean not null default true,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

create table if not exists chapters (
  id          serial primary key,
  book_id     integer not null references books(id) on delete cascade,
  slug        text not null,
  title       text not null,
  position    integer not null default 0,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  unique (book_id, slug)
);

create table if not exists sections (
  id          serial primary key,
  chapter_id  integer not null references chapters(id) on delete cascade,
  slug        text not null,
  title       text not null,
  dek         text not null default '',
  body        text not null default '',
  position    integer not null default 0,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  unique (chapter_id, slug)
);

-- Images live in the database with everything else, so a book is one backup rather than
-- a database plus an object store, and the app needs no storage credentials to run.
create table if not exists assets (
  id          serial primary key,
  url         text not null,
  pathname    text not null,
  alt         text not null default '',
  size        integer not null default 0,
  created_at  timestamptz not null default now()
);

alter table assets add column if not exists data bytea;
alter table assets add column if not exists mime text not null default 'image/png';
-- Where the file came from, when it was loaded in bulk rather than uploaded by hand.
alter table assets add column if not exists source text not null default '';
alter table assets add column if not exists tag text not null default '';

create unique index if not exists assets_source_idx on assets (source) where source <> '';
create index if not exists assets_tag_idx on assets (tag);

create index if not exists chapters_book_idx on chapters (book_id, position);
create index if not exists sections_chapter_idx on sections (chapter_id, position);

-- Nothing is destroyed by an editor action: archiving stamps deleted_at, which hides the
-- row from readers and from the normal admin lists while leaving it restorable. Only the
-- explicit "delete permanently" in the archive removes a row for good.
alter table books add column if not exists deleted_at timestamptz;
alter table chapters add column if not exists deleted_at timestamptz;
alter table sections add column if not exists deleted_at timestamptz;

create index if not exists books_live_idx on books (position) where deleted_at is null;
create index if not exists chapters_live_idx on chapters (book_id, position) where deleted_at is null;
create index if not exists sections_live_idx on sections (chapter_id, position) where deleted_at is null;

-- Search runs over title + body of every section, weighted so a title hit outranks a
-- body hit. Stored generated so it stays correct on every write without a trigger.
alter table sections
  add column if not exists search tsvector
  generated always as (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(body, '')), 'B')
  ) stored;

create index if not exists sections_search_idx on sections using gin (search);
