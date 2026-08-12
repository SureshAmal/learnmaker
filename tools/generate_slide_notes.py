#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDFS = [
    ("unit1-introduction", "Unit I - Introduction to Machine Learning", "ml class/Unit-I Introduction to Machine Learning.pptx.pdf"),
    ("unit2-supervised-short", "Unit II - Supervised Learning", "ml class/ML_UNIT-2 Supervised Learning.pptx.pdf"),
    ("unit2-supervised-full", "Unit II - Supervised Learning (Full Deck)", "ml class/ML_UNIT-2 Supervised Learning.pptx (1).pdf"),
    ("unit3-unsupervised", "Unit III - Unsupervised Learning", "ml class/UNIT-III Unsupervised Learning.pptx.pdf"),
    ("unit3-algorithms", "Unit III - Different Algorithms in Machine Learning", "ml class/UNIT-III Different Algorithms in Machine Learning.pptx.pdf"),
]


@dataclass(frozen=True)
class Page:
    number: int
    text: str
    lines: list[str]
    title: str


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, cwd=ROOT, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def pdf_pages(pdf: Path) -> int:
    out = run(["pdfinfo", str(pdf)])
    match = re.search(r"^Pages:\s+(\d+)", out, re.MULTILINE)
    if not match:
        raise RuntimeError(f"Could not read page count for {pdf}")
    return int(match.group(1))


def extract_text(pdf: Path) -> list[str]:
    out = run(["pdftotext", "-layout", str(pdf), "-"])
    pages = out.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def clean_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if line:
            lines.append(line)
    return lines


def title_for(lines: list[str], fallback: str, number: int) -> str:
    for line in lines:
        if len(line) <= 90:
            return line
    return f"{fallback} Page {number}"


def classify(lines: list[str]) -> str:
    joined = " ".join(lines).lower()
    if not lines:
        return "visual-only or image-heavy slide"
    if len(lines) <= 3:
        return "title or transition slide"
    if any(token in joined for token in ["=", "∑", "√", "²", "formula", "equation", "cost function"]):
        return "formula or calculation slide"
    if any(token in joined for token in ["matrix", "table", "accuracy", "precision", "recall", "mse", "rmse", "mae"]):
        return "metric/table slide"
    if any(token in joined for token in ["diagram", "architecture", "flow", "steps", "process"]):
        return "process or diagram slide"
    if any(line[:1] in {"❑", "✔", "▪", "•", "-"} or re.match(r"^\d+[.)]", line) for line in lines):
        return "bullet explanation slide"
    return "concept explanation slide"


def compact_text(lines: list[str], limit: int = 16) -> list[str]:
    if len(lines) <= limit:
        return lines
    return lines[: limit - 2] + ["...", lines[-1]]


def added_since(previous: list[str], current: list[str]) -> list[str]:
    prev = set(previous)
    return [line for line in current if line not in prev]


def key_terms(lines: list[str]) -> list[str]:
    text = " ".join(lines)
    terms = re.findall(r"\b[A-Z][A-Za-z0-9+/#-]*(?:\s+[A-Z][A-Za-z0-9+/#-]*){0,3}\b", text)
    cleaned: list[str] = []
    seen: set[str] = set()
    stop = {"OR", "Ex", "A", "B", "C", "I", "II", "III", "ML", "AI"}
    for term in terms:
        term = term.strip(" :-")
        if term in stop or len(term) < 3 or term in seen:
            continue
        seen.add(term)
        cleaned.append(term)
        if len(cleaned) == 8:
            break
    return cleaned


def sentence_from_lines(lines: list[str]) -> str:
    text = " ".join(lines).strip()
    text = re.sub(r"\s+", " ", text)
    return text.rstrip(".") + "." if text else ""


def explain_points(points: list[str]) -> list[str]:
    notes: list[str] = []
    for point in compact_text(points, 10):
        clean = point.strip()
        if clean == "...":
            notes.append("- Additional bullets continue on the slide; use the extracted text list above for the complete wording.")
            continue
        lowered = clean.lower()
        if any(word in lowered for word in ["definition", "is a", "is an", "refers to"]):
            notes.append(f"- `{clean}` gives the definition-level meaning. Explain it first in simple words, then connect it to how a model learns from data.")
        elif any(word in lowered for word in ["advantage", "benefit", "improves", "helps", "supports"]):
            notes.append(f"- `{clean}` states a benefit. Use it to justify why this method or concept is useful in a machine-learning workflow.")
        elif any(word in lowered for word in ["disadvantage", "cannot", "limitation", "problem", "error"]):
            notes.append(f"- `{clean}` is a limitation or risk. Mention when the method may fail and what alternative or precaution can reduce the issue.")
        elif any(word in lowered for word in ["example", "ex:", "application", "used for", "use"]):
            notes.append(f"- `{clean}` is an application/example point. Convert it into a concrete real-world case while teaching.")
        elif re.match(r"^\d+[.)]", clean) or clean[:1] in {"❑", "✔", "▪", "•", "-"}:
            notes.append(f"- `{clean}` is one item in the slide's list. Treat it as a separate subtopic and prepare a one-line explanation for it.")
        else:
            notes.append(f"- `{clean}` is a core visible point. Explain what it means, why it matters, and how it connects to the slide title.")
    return notes


def explain_page(page: Page, previous: Page | None) -> list[str]:
    kind = classify(page.lines)
    terms = key_terms(page.lines)
    additions = added_since(previous.lines if previous else [], page.lines) if previous else []
    body_lines = [line for line in page.lines if line != page.title]
    summary = sentence_from_lines(body_lines[:6])

    notes: list[str] = []
    notes.append(f"Slide type: {kind}.")
    if summary:
        notes.append(f"Main idea: {summary}")
    else:
        notes.append("Main idea: the slide is visual-first, so the image should be treated as the source for the content and structure.")

    if kind == "title or transition slide":
        notes.append(
            "This page sets the context for the next topic. Treat it as a section marker: it tells the learner what concept or unit is starting before the deck moves into definitions, examples, or formulas."
        )
    elif kind == "visual-only or image-heavy slide":
        notes.append(
            "This page is primarily visual. The embedded slide image is the authoritative visual output; read it as a diagram or illustration first, then connect any visible labels to the surrounding pages."
        )
    elif kind == "formula or calculation slide":
        notes.append(
            "This page should be read carefully because it introduces a calculation, objective, or optimization idea. Identify the variables in the formula, what quantity is being minimized or measured, and how the equation supports model training or evaluation."
        )
    elif kind == "metric/table slide":
        notes.append(
            "This page organizes evaluation or comparison information. Focus on what each metric measures, when it is useful, and what mistake it prevents when judging a machine-learning model."
        )
    elif kind == "process or diagram slide":
        notes.append(
            "This page describes a flow, algorithm, or sequence. Read the visual from start to finish and explain how each stage transforms data, parameters, or decisions into the next stage."
        )
    elif kind == "bullet explanation slide":
        notes.append(
            "This page breaks the topic into separate points. Each bullet should be treated as a distinct exam or viva talking point, with the learner able to define it and give a small example."
        )
    else:
        notes.append(
            "This page explains a core concept in prose. The main task is to convert the definition into a clear statement of what the concept is, why it is used, and where it appears in a machine-learning workflow."
        )

    if body_lines:
        notes.append("Detailed page understanding:")
        notes.extend(explain_points(body_lines))
    else:
        notes.append("- No reliable selectable text was extracted; use the slide image for the visible diagram, chart, or screenshot.")

    if terms:
        notes.append("Important visible terms: " + ", ".join(terms) + ".")

    if previous and page.title == previous.title and additions:
        notes.append(
            "Progressive reveal note: compared with the previous page, this page adds or exposes: "
            + "; ".join(compact_text(additions, 6))
            + "."
        )
    elif previous and page.title == previous.title:
        notes.append(
            "Progressive reveal note: this page appears to continue the same slide state as the previous page, so compare the embedded images for the exact visual change."
        )

    notes.append(
        "Visual/layout description: the embedded image preserves the actual slide. Describe the title area first, then read bullets, formulas, tables, arrows, grouped boxes, or diagrams in their visible order. If the slide contains a diagram, explain the relationship shown by arrows/positioning before explaining the text labels."
    )
    notes.append(
        "Teaching note: after reading the slide, ask the learner to restate the page in one or two sentences and give one example. For formula or metric slides, also ask what each variable or metric means and when it should be used."
    )
    notes.append(
        "Exam/viva note: prepare the slide title as a short-answer question, then use the bullets or visual labels as the expected answer points."
    )
    return notes


def render_images(pdf: Path, asset_dir: Path, expected_pages: int) -> None:
    asset_dir.mkdir(parents=True, exist_ok=True)
    expected = {asset_dir / f"page-{page:03d}.png" for page in range(1, expected_pages + 1)}
    current = set(asset_dir.glob("page-*.png"))
    if not expected.issubset(current) or len(current) != expected_pages:
        for path in current:
            path.unlink()
    for page in range(1, expected_pages + 1):
        target = asset_dir / f"page-{page:03d}.png"
        if target.exists():
            continue
        prefix = asset_dir / f"render-{page:03d}"
        subprocess.run(
            ["pdftoppm", "-png", "-r", "120", "-f", str(page), "-l", str(page), str(pdf), str(prefix)],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        rendered = sorted(asset_dir.glob(f"render-{page:03d}*.png"))
        if not rendered:
            raise RuntimeError(f"pdftoppm did not render page {page} of {pdf}")
        rendered[0].rename(target)
        for extra in rendered[1:]:
            extra.unlink()


def write_notes(slug: str, unit_title: str, pdf_rel: str) -> None:
    print(f"Generating {slug}", flush=True)
    pdf = ROOT / pdf_rel
    pages_count = pdf_pages(pdf)
    text_pages = extract_text(pdf)
    asset_dir = ROOT / "slide-notes" / "assets" / slug
    render_images(pdf, asset_dir, pages_count)

    pages: list[Page] = []
    for idx in range(pages_count):
        text = text_pages[idx] if idx < len(text_pages) else ""
        lines = clean_lines(text)
        pages.append(Page(idx + 1, text.strip(), lines, title_for(lines, unit_title, idx + 1)))

    out = ROOT / "slide-notes" / f"{slug}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        f"# {unit_title}",
        "",
        f"Source PDF: `{pdf_rel}`",
        f"Total pages: {pages_count}",
        "",
        "These notes are written page by page. Every page includes the rendered slide image as visual output, the extracted text, and a detailed explanation of how to read the slide.",
        "",
    ]

    previous: Page | None = None
    for page in pages:
        image_rel = f"assets/{slug}/page-{page.number:03d}.png"
        lines.extend(
            [
                f"## Page {page.number}: {page.title}",
                "",
                f"![Page {page.number}]({image_rel})",
                "",
                "### Extracted Slide Text",
                "",
            ]
        )
        if page.lines:
            lines.extend([f"- {line}" for line in page.lines])
        else:
            lines.append("- No selectable text extracted from this page.")
        lines.extend(["", "### Page Description And Teaching Notes", ""])
        lines.extend(explain_page(page, previous))
        lines.append("")
        previous = page

    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    selected = set(sys.argv[1:])
    for slug, title, pdf in PDFS:
        if selected and slug not in selected:
            continue
        write_notes(slug, title, pdf)


if __name__ == "__main__":
    main()
