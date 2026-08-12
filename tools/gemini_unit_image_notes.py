#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMAGE_DIR = ROOT / "slide-notes" / "assets" / "unit1-introduction"
DEFAULT_OUTPUT_DIR = ROOT / "markdown-ml" / "unit1" / "page-notes"
DEFAULT_MODEL = "gemini-3-flash-preview"
DEFAULT_VERTEX_LOCATION = "global"


PROMPT = """You are analyzing one machine-learning course slide image.

Write detailed markdown notes for this exact page. Do not summarize shortly and do not skip visual details.

Use this exact structure:

## Page Overview
Explain the slide purpose in detail.

## Visible Text
Transcribe all readable text. Preserve formulas, labels, table headers, axis labels, and step names.

## Visual Layout
Describe the page layout: title position, content blocks, colors, boxes, arrows, tables, charts, icons, spacing, alignment, and visual hierarchy.

## Diagram Type
Classify the main visual if present: flowchart, pipeline, table, decision tree, scatter plot, curve, mathematical graph, formula derivation, architecture diagram, comparison diagram, or text-only slide. Explain why.

## Diagram / Visual Explanation
Explain the diagram step by step. If there are arrows, describe source, target, and meaning. If there are boxes, describe each box and its relationship to the others. If there are axes or curves, describe the x-axis, y-axis, curve shape, important points, and interpretation.

## Math / Formula / Curve Notes
If math exists, explain every symbol, variable, equation, curve, graph, and calculation. If no math exists, say "No mathematical formula or curve is visible on this page."

## Table Description
If a table exists, describe columns, rows, comparisons, and the conclusion. If no table exists, say "No table is visible on this page."

## Concept Explanation
Explain the machine-learning concept being taught, with enough detail for a student to understand without the original slide.

## Exam / Viva Points
List detailed answer points a student should remember.

## Diagram Recreation Prompt
Write a clean prompt that can be used to recreate or improve this page's diagram/image. Include layout, colors, labels, shape types, arrow directions, table structure, and fitting constraints. If the original diagram is too tall/dark/plain, explicitly improve it with a compact page-fitting colored layout.

## Diagram Data
Provide structured data needed to recreate the diagram. For flowcharts, list nodes and edges. For charts/curves, list axes, plotted values or inferred shape, labels, and annotations. For tables, provide markdown table data. For text-only pages, list title and content sections.

Return only markdown content for this one page.
"""


def load_env(path: Path = ROOT / ".env") -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def gemini_key() -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit(
            "Missing GEMINI_API_KEY. Add GEMINI_API_KEY to .env or the environment. Do not hardcode keys into this file."
        )
    return key


def vertex_access_token() -> str:
    token = os.environ.get("VERTEX_ACCESS_TOKEN") or os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN")
    if not token:
        raise SystemExit(
            "Missing Vertex bearer token. Set VERTEX_ACCESS_TOKEN or GOOGLE_OAUTH_ACCESS_TOKEN in the environment."
        )
    return token


def image_payload(path: Path) -> dict:
    return {
        "inline_data": {
            "mime_type": "image/png",
            "data": base64.b64encode(path.read_bytes()).decode("ascii"),
        }
    }


def vertex_url(model: str, mode: str, project: str | None, location: str) -> str:
    if mode == "vertex-standard":
        if not project:
            raise SystemExit(
                "vertex-standard requires PROJECT_ID in .env or --project. "
                "The Vertex AI endpoint is /v1/projects/{PROJECT_ID}/locations/global/publishers/google/models/{MODEL_ID}:generateContent."
            )
        host = "aiplatform.googleapis.com" if location == "global" else f"{location}-aiplatform.googleapis.com"
        return (
            f"https://{host}/v1/projects/{project}/locations/{location}"
            f"/publishers/google/models/{model}:generateContent"
        )
    if mode == "vertex-express":
        return f"https://aiplatform.googleapis.com/v1/publishers/google/models/{model}:generateContent"
    raise SystemExit(f"Unknown API mode: {mode}")


def auth_headers(mode: str, key: str) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if mode == "vertex-standard":
        headers["Authorization"] = f"Bearer {vertex_access_token()}"
    else:
        headers["x-goog-api-key"] = key
    return headers


def request_note(
    image: Path,
    model: str,
    key: str,
    timeout: int,
    retries: int,
    mode: str,
    project: str | None,
    location: str,
) -> str:
    url = vertex_url(model, mode, project, location)
    body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": PROMPT},
                    image_payload(image),
                ],
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "topP": 0.9,
        },
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=auth_headers(mode, key), method="POST")

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            parts = payload["candidates"][0]["content"]["parts"]
            return "\n".join(part.get("text", "") for part in parts).strip()
        except urllib.error.HTTPError as exc:
            message = exc.read().decode("utf-8", errors="replace")
            last_error = RuntimeError(f"HTTP {exc.code}: {message[:1000]}")
            if attempt >= retries:
                break
            time.sleep(2**attempt)
        except (urllib.error.URLError, TimeoutError, KeyError, IndexError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt >= retries:
                break
            time.sleep(2**attempt)
    raise RuntimeError(f"Vertex AI request failed for {image.name}: {last_error}")


def write_page_note(
    image: Path,
    output_dir: Path,
    model: str,
    key: str,
    timeout: int,
    retries: int,
    force: bool,
    mode: str,
    project: str | None,
    location: str,
) -> str:
    page_id = image.stem.replace("page-", "")
    output = output_dir / f"page-{page_id}.md"
    if output.exists() and not force:
        return f"skip {output.relative_to(ROOT)}"

    note = request_note(image, model, key, timeout, retries, mode, project, location)
    output.write_text(f"# Unit 1 Page {int(page_id)} Image Understanding\n\n{note}\n", encoding="utf-8")
    return f"write {output.relative_to(ROOT)}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create one Gemini image-understanding markdown note per Unit 1 page image.")
    parser.add_argument("--image-dir", type=Path, default=DEFAULT_IMAGE_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--model", default=os.environ.get("GEMINI_MODEL", DEFAULT_MODEL))
    parser.add_argument(
        "--api-mode",
        choices=["vertex-express", "vertex-standard"],
        default=os.environ.get("VERTEX_API_MODE", "vertex-standard"),
        help="vertex-standard uses the project/location Vertex endpoint with bearer auth; vertex-express uses an API key.",
    )
    parser.add_argument(
        "--project",
        default=os.environ.get("PROJECT_ID") or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("VERTEX_PROJECT"),
    )
    parser.add_argument("--location", default=os.environ.get("GOOGLE_CLOUD_LOCATION") or os.environ.get("VERTEX_LOCATION", DEFAULT_VERTEX_LOCATION))
    parser.add_argument("--workers", type=int, default=1, help="Parallel Gemini calls. Use 1 for strict sequential calls.")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--from-page", type=int, default=1)
    parser.add_argument("--to-page", type=int)
    parser.add_argument("--force", action="store_true", help="Overwrite existing page notes.")
    return parser.parse_args()


def main() -> int:
    load_env()
    args = parse_args()
    key = gemini_key() if args.api_mode == "vertex-express" else ""
    image_dir = args.image_dir.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    images = sorted(image_dir.glob("page-*.png"))
    selected = []
    for image in images:
        try:
            page = int(image.stem.removeprefix("page-"))
        except ValueError:
            continue
        if page < args.from_page:
            continue
        if args.to_page is not None and page > args.to_page:
            continue
        selected.append(image)

    if not selected:
        print(f"No page images found in {image_dir}", file=sys.stderr)
        return 1

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = [
            executor.submit(
                write_page_note,
                image,
                output_dir,
                args.model,
                key,
                args.timeout,
                args.retries,
                args.force,
                args.api_mode,
                args.project,
                args.location,
            )
            for image in selected
        ]
        for future in as_completed(futures):
            print(future.result(), flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
