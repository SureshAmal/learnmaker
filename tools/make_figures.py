#!/usr/bin/env python3
"""Turn the rendered slide images into web-sized figures for the ML book.

The slide PNGs under slide-notes/assets are 1.5-2 MB each at full resolution, which is far
more than a reading page needs. This copies the ones the course text actually references
into ml-course/figures as WebP, capped at 1200px wide, which lands around 40-80 KB each.

    python3 tools/make_figures.py                 # every figure referenced by ml-course/*.md
    python3 tools/make_figures.py --all unit1-introduction
    python3 tools/make_figures.py --pages unit1-introduction:44,45,46

Naming: slide-notes/assets/unit1-introduction/page-044.png -> ml-course/figures/u1-044.webp
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "slide-notes" / "assets"
OUT = ROOT / "ml-course" / "figures"
UNITS = ROOT / "ml-course"

# short prefix per deck, used in the figure filenames
DECKS = {
    "unit1-introduction": "u1",
    "unit2-supervised-full": "u2",
    "unit2-supervised-short": "u2s",
    "unit3-algorithms": "u3a",
    "unit3-unsupervised": "u3u",
}
PREFIX_TO_DECK = {v: k for k, v in DECKS.items()}

MAX_W = 1200
QUALITY = 82


def convert(deck: str, page: int, force: bool = False) -> Path | None:
    prefix = DECKS[deck]
    src = SRC / deck / f"page-{page:03d}.png"
    if not src.exists():
        print(f"  missing {src}", file=sys.stderr)
        return None
    dst = OUT / f"{prefix}-{page:03d}.webp"
    if dst.exists() and not force and dst.stat().st_mtime >= src.stat().st_mtime:
        return dst
    with Image.open(src) as im:
        im = im.convert("RGB")
        if im.width > MAX_W:
            im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
        OUT.mkdir(parents=True, exist_ok=True)
        im.save(dst, "WEBP", quality=QUALITY, method=6)
    return dst


REF = re.compile(r'figures/([a-z0-9]+)-(\d{3})\.webp')


def referenced() -> list[tuple[str, int]]:
    """Every figure the course markdown asks for, as (deck, page) pairs."""
    want: list[tuple[str, int]] = []
    for md in sorted(UNITS.glob("unit-*.md")):
        for prefix, page in REF.findall(md.read_text(encoding="utf-8")):
            deck = PREFIX_TO_DECK.get(prefix)
            if deck and (deck, int(page)) not in want:
                want.append((deck, int(page)))
    return want


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", metavar="DECK", help="convert every page of one deck")
    ap.add_argument("--pages", metavar="DECK:1,2,3", help="convert specific pages")
    ap.add_argument("--force", action="store_true", help="re-encode even if up to date")
    args = ap.parse_args()

    if args.all:
        deck = args.all
        pages = sorted(int(p.stem.split("-")[1]) for p in (SRC / deck).glob("page-*.png"))
        jobs = [(deck, p) for p in pages]
    elif args.pages:
        deck, _, csv = args.pages.partition(":")
        jobs = [(deck, int(p)) for p in csv.split(",") if p.strip()]
    else:
        jobs = referenced()
        if not jobs:
            print("no figures referenced by ml-course/unit-*.md yet")
            return

    made = 0
    total = 0
    for deck, page in jobs:
        if deck not in DECKS:
            print(f"unknown deck {deck}; choose from {', '.join(DECKS)}", file=sys.stderr)
            raise SystemExit(2)
        dst = convert(deck, page, args.force)
        if dst:
            made += 1
            total += dst.stat().st_size
    print(f"{made} figures -> {OUT} ({total / 1048576:.2f} MB)")


if __name__ == "__main__":
    main()
