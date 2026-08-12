#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import random
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


TOOL_ROOT = Path(__file__).resolve().parent
ROOT = TOOL_ROOT.parent
DEFAULT_REF_IMAGE = ROOT / "ref" / "Pasted image (10).png"
DEFAULT_OUTPUT_DIR = ROOT / "ref" / "gemini-test-images"
DEFAULT_MODEL = "gemini-2.5-flash-image-preview"


STYLE_PREFIX = """Create a polished scientific educational diagram for a machine-learning course.
Match the visual style of the provided reference image: white background, precise vector-like geometry, thin gray outlines, clean readable labels, restrained technical colors, generous white space, compact slide-friendly 16:9 composition, and no decorative UI styling.
Use crisp readable text, accurate labels, thin 1-2 px lines, no cropped labels, and no overlapping text.
Use technical figure aesthetics: flat vector drawing, clean mathematical notation where useful, lightly filled regions where they clarify the concept, no card UI, no drop shadows, no large rounded cards, no app-style icons, no decorative pictograms.
Avoid dark theme, heavy shadows, glossy 3D, random icons, noisy background, misspelled labels, incorrect formulas, clutter, and marketing infographic style.
"""


PROMPTS = {
    "ml-pipeline": STYLE_PREFIX
    + """
Topic: Machine Learning Pipeline.
Diagram type: compact technical process diagram, not a card UI.
Layout: two balanced horizontal rows of five small rectangular technical nodes each, connected by thin gray arrows. Row 1: Problem Definition -> Data Collection -> Data Cleaning and Preprocessing -> Exploratory Data Analysis -> Feature Engineering and Selection. Row 2: Model Selection -> Model Training -> Model Evaluation and Tuning -> Model Deployment -> Model Monitoring and Maintenance.
Each node must contain only one icon/symbol and one numbered circle. Do not place any words inside any rectangle.
Place the step label once above each rectangle, centered. Do not place labels below rectangles. Do not repeat labels as captions. Do not duplicate any step text anywhere.
Use these ten labels exactly once total in the whole image: Problem Definition, Data Collection, Data Cleaning and Preprocessing, Exploratory Data Analysis, Feature Engineering and Selection, Model Selection, Model Training, Model Evaluation and Tuning, Model Deployment, Model Monitoring and Maintenance.
Use small abstract line symbols made from simple geometry, not logos or pictograms: target/crosshair for problem, database cylinder for data, grid-cleaning mark for preprocessing, tiny scatter/bar chart for EDA, feature grid for feature engineering, model comparison mini plot for selection, network nodes for training, line chart and sliders for evaluation, simple deployment box/cloud outline, monitoring line chart/bell outline.
Use exactly one small muted blue numbered circle per node, numbered 1 through 10. Do not duplicate any number. Do not add a main title. Use thin gray arrow connectors, no shadows, no large rounded cards, no colored header bars. Make it fit cleanly on one 16:9 slide.
Negative examples to avoid: do not write Model Selection twice; do not write Model Training twice; do not add any bottom captions under the second row.
""",
    "bias-variance": STYLE_PREFIX
    + """
Topic: Bias-Variance Tradeoff.
Diagram type: mathematical curve plot.
Axes: x-axis labeled Model Complexity, y-axis labeled Prediction Error. Thin charcoal axes, small tick marks, numeric ticks, subtle light gray grid lines.
Curves: Bias^2 decreasing smoothly in blue, Variance increasing smoothly in red, Total Error U-shaped in dark charcoal. Use exactly these three legend entries: Bias^2, Variance, Total Error.
Mark the minimum of Total Error with a small green dot and a thin leader-line label Best generalization. Place Optimal complexity as a vertical dashed gray guide line under the green dot.
Add small leader-line annotations: Underfitting on the left region, Overfitting on the right region. Keep labels small and outside curves when possible.
Make the chart look like a clean scientific textbook plot, not a large presentation chart: smaller typography, thinner strokes, more whitespace, compact legend, no duplicated legend labels.
""",
    "kmeans": STYLE_PREFIX
    + """
Topic: k-Means Clustering.
Diagram type: 2D scatter plot with centroids and Voronoi-like decision regions.
Axes: x-axis Feature 1, y-axis Feature 2. Light gray grid and thin charcoal axes.
Data: three clusters of small points: blue circles in lower-left, green squares in upper-left, red triangles on the right. Black plus-sign centroids labeled m1, m2, m3.
Decision regions: thin gray boundary lines with very light translucent blue, green, and red fills.
Use only these text labels inside the plot area: Feature 1, Feature 2, m1, m2, m3.
Include one compact legend outside the plot with only: Cluster 1, Cluster 2, Cluster 3, Centroid.
Do not write Decision boundary anywhere as visible text. The gray boundary lines must explain the decision regions without a text label. Do not add formulas or extra annotation paragraphs.
""",
    "linear-regression": STYLE_PREFIX
    + """
Topic: Simple Linear Regression.
Diagram type: scatter plot with fitted regression line.
Axes: x-axis House Size, y-axis Price. Thin charcoal axes, small numeric ticks, subtle light gray grid.
Data: blue circular scatter points trending upward. Draw one clean red fitted line labeled y = mx + b. Add light gray residual segments from selected points to the line. Add labels: Observed data, Best-fit line, Residual error.
Keep it like a scientific textbook plot with compact labels and no decorative icons.
""",
    "gradient-descent": STYLE_PREFIX
    + """
Topic: Gradient Descent on a Convex Cost Function.
Diagram type: mathematical curve plot.
Axes: x-axis Parameter w, y-axis Cost J(w). Draw a smooth U-shaped convex curve in dark charcoal. Place a sequence of small blue points with arrows descending from the upper left side toward the minimum. Mark the minimum with a green dot labeled Minimum cost.
Add labels: Learning rate step, Negative gradient direction, Convergence. Thin leader lines, light gray grid, white background.
""",
    "train-test-split": STYLE_PREFIX
    + """
Topic: Train Test Split.
Diagram type: dataset partition diagram.
Layout: one long horizontal row of small equal rectangular cells representing dataset records. Use thin gray cell outlines. Fill 80% of cells pale blue labeled Training set, 20% pale orange labeled Test set. Add a bracket above each region and a thin vertical split line.
Add labels: Full dataset, Train 80%, Test 20%, Model learns only from training data, Final evaluation on test data. Keep compact and slide-friendly.
""",
    "confusion-matrix": STYLE_PREFIX
    + """
Topic: Confusion Matrix.
Diagram type: 2x2 technical matrix.
Create a clean 2x2 table with columns Predicted Positive and Predicted Negative, rows Actual Positive and Actual Negative. Cells: True Positive, False Negative, False Positive, True Negative.
Use thin gray grid lines, light gray headers, pale green fill for correct cells, pale red fill for error cells. Add small side labels: Precision uses predicted positives, Recall uses actual positives.
No heavy border, no decorative icons.
""",
    "decision-tree": STYLE_PREFIX
    + """
Topic: Decision Tree Classification.
Diagram type: balanced tree diagram.
Root node: Feature A <= threshold. Branch labels: Yes and No. Second-level nodes: Feature B <= threshold and Feature C <= threshold. Leaf nodes: Class 0, Class 1, Class 2, Class 1.
Use white rectangular nodes with thin gray outlines, thin gray branch lines, muted green/blue/red leaf fills, compact labels. Keep tree balanced and centered with generous whitespace.
""",
    "svm-margin": STYLE_PREFIX
    + """
Topic: Support Vector Machine Margin.
Diagram type: 2D coordinate geometry plot.
Axes: Feature 1 and Feature 2. Draw two classes: blue circles and red triangles separated by a dark decision boundary line. Draw two parallel dashed margin lines. Highlight support vectors with larger outlined markers.
Add labels: Decision boundary, Margin, Support vectors. Use thin leader lines, pale grid, white background.
""",
    "knn-classification": STYLE_PREFIX
    + """
Topic: k-Nearest Neighbors Classification.
Diagram type: local neighborhood scatter plot.
Axes: Feature 1 and Feature 2. Show blue circle class points and red triangle class points. Add one black query point at the center. Draw a thin dashed circle around the query point containing exactly five nearest neighbors.
Add labels: Query point, k = 5 neighborhood, Majority class. Keep all labels outside dense point areas with thin leader lines.
""",
    "roc-curve": STYLE_PREFIX
    + """
Topic: ROC Curve and AUC.
Diagram type: mathematical curve plot.
Axes: x-axis False Positive Rate, y-axis True Positive Rate, both scaled 0 to 1 with numeric ticks. Draw a blue ROC curve bowing toward the top-left. Draw a gray dashed diagonal baseline labeled Random classifier. Lightly fill the area under the curve in translucent blue and label AUC.
Add label: Better classifier near top-left. Thin grid, compact legend, no clutter.
""",
    "overfit-underfit": STYLE_PREFIX
    + """
Topic: Underfitting, Good Fit, and Overfitting.
Diagram type: three-panel comparison plot.
Create three small side-by-side plots with shared clean style. Each plot has blue scatter points from a curved trend. Panel 1 Underfitting: straight red line misses curve. Panel 2 Good Fit: smooth red curve follows trend. Panel 3 Overfitting: wiggly red curve passes through points.
Use thin axes, small titles, white background, no legend box.
""",
    "normalization-standardization": STYLE_PREFIX
    + """
Topic: Normalization vs Standardization.
Diagram type: formula comparison visual.
Layout: two clean side-by-side panels. Left panel title Normalization, formula x' = (x - min) / (max - min), show values compressed to 0-1 range on a horizontal number line. Right panel title Standardization, formula z = (x - mean) / standard deviation, show bell curve centered at 0.
Use thin gray dividers, blue accents for normalization, green accents for standardization, crisp formula text.
""",
    "pca-projection": STYLE_PREFIX
    + """
Topic: Principal Component Analysis Projection.
Diagram type: coordinate geometry plot.
Show an elongated cloud of blue points in 2D feature space. Draw a long red arrow through the cloud labeled PC1 and a shorter green perpendicular arrow labeled PC2. Project several points onto PC1 using thin dashed gray lines.
Axes: Feature 1 and Feature 2. Add label: maximum variance direction. Use pale grid and precise linework.
""",
    "dbscan": STYLE_PREFIX
    + """
Topic: DBSCAN Clustering.
Diagram type: density-based scatter plot.
Show two dense clusters of points, one blue and one green, plus several gray noise points. Around one core point draw a dashed epsilon radius circle labeled eps. Mark core point, border point, and noise point with leader lines.
Use thin axes, light grid, compact legend: Core, Border, Noise. White scientific figure style.
""",
    "hierarchical-dendrogram": STYLE_PREFIX
    + """
Topic: Hierarchical Clustering Dendrogram.
Diagram type: dendrogram tree.
Use a clean white canvas with a horizontal baseline of leaf labels A, B, C, D, E, F. Draw thin gray merge lines upward into clusters. y-axis label Distance. Use small colored cluster bands at the bottom for two final clusters.
Add labels: Merge distance, Cluster cut threshold, Leaves. No thick lines, no dark background.
""",
    "cross-validation": STYLE_PREFIX
    + """
Topic: k-Fold Cross Validation.
Diagram type: fold schedule table.
Create five horizontal rows labeled Fold 1 through Fold 5. Each row has five equal blocks. In each row, one block is orange labeled Validation and the other blocks are pale blue labeled Training. Move the orange validation block across columns from left to right.
Add title k-Fold Cross Validation and a small note: each subset is used once for validation. Thin grid lines, white background.
""",
    "regularization": STYLE_PREFIX
    + """
Topic: L1 and L2 Regularization.
Diagram type: comparison plot and constraint shapes.
Create two side-by-side coordinate panels. Left title: L1 Regularization Sparse solution. Right title: L2 Regularization Small weights.
Each panel has thin gray x/y axes labeled w1 and w2, gray elliptical loss contours, and a red solution point where the contour touches the constraint boundary.
Left panel: draw a translucent blue filled diamond for the L1 constraint, labeled ||w||_1 <= C, with the red point near a diamond corner and label Regularized solution.
Right panel: draw a translucent blue filled circle for the L2 constraint, labeled ||w||_2^2 <= C, with the red point on the circle boundary and label Regularized solution.
Use thin gray contour lines, blue filled constraint regions, red solution points, clean math notation, and generous whitespace. Make it look like the best previous regularization batch image, not a sparse empty sketch.
""",
    "neural-network": STYLE_PREFIX
    + """
Topic: Artificial Neural Network.
Diagram type: layered network architecture.
Show four vertical layers of small circles: Input layer with 4 nodes, Hidden layer 1 with 5 nodes, Hidden layer 2 with 4 nodes, Output layer with 2 nodes. Connect adjacent layers with thin gray lines. Use muted blue input nodes, pale purple hidden nodes, pale green output nodes.
Add labels: Input features, Hidden layers, Output prediction, Weights. Keep layout centered and clean.
""",
    "polynomial-regression": STYLE_PREFIX
    + """
Topic: Polynomial Regression.
Diagram type: scatter plot with curved fit.
Axes: x and y. Show blue scatter points following a curved quadratic trend. Draw a smooth red polynomial curve labeled Polynomial fit. Add a faint gray straight line labeled Linear model cannot capture curvature.
Use light grid, compact legend, thin linework, white background.
""",
    "feature-scaling": STYLE_PREFIX
    + """
Topic: Feature Scaling.
Diagram type: before-and-after scatter comparison.
Create two side-by-side plots. Left title Before scaling: elongated point cloud with x-axis much wider than y-axis. Right title After scaling: same points normalized into balanced circular cloud. Use blue points, thin axes, light grids, arrow between panels labeled Scaling transform.
Add labels: different ranges and comparable ranges.
""",
    "classification-boundary": STYLE_PREFIX
    + """
Topic: Classification Decision Boundary.
Diagram type: 2D scatter plot with nonlinear boundary.
Axes: Feature 1 and Feature 2. Show blue circles and red triangles in two curved regions. Draw a smooth dark decision boundary separating classes. Fill regions with very light blue and red translucent background.
Add labels: Class A region, Class B region, Decision boundary. Keep labels outside dense areas.
""",
    "gradient-descent-surface": STYLE_PREFIX
    + """
Topic: Gradient Descent Loss Surface.
Diagram type: clean 3D convex bowl surface.
Show a smooth pastel 3D bowl-shaped surface with thin gray x, y, z axes labeled w1, w2, J(w). Add a descending path of small blue points with arrows toward a green minimum point.
Labels: loss surface, descent path, global minimum. Use compact perspective, no glossy rendering, white background.
""",
}


def load_env() -> None:
    load_dotenv(TOOL_ROOT / ".env", override=True)
    load_dotenv(ROOT / ".env", override=False)


def required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing {name}. Add it to .env or the environment.")
    return value


def mime_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if ext == ".webp":
        return "image/webp"
    return "image/png"


def image_part(path: Path) -> types.Part:
    return types.Part.from_bytes(data=path.read_bytes(), mime_type=mime_type(path))


def call_genai(
    prompt: str,
    ref_images: list[Path],
    model: str,
    credential: str,
    retries: int,
    retry_initial_delay: float,
    retry_max_delay: float,
) -> object:
    client = genai.Client(api_key=credential, vertexai=True)
    metadata = ""
    if ref_images:
        metadata = "\n\nReference images supplied only for broad visual inspiration; do not copy their text, fonts, artifacts, layout mistakes, logos, or decorative details:\n" + "\n".join(
            f"- {path.name}" for path in ref_images
        )
    contents: list[object] = [
        prompt
        + "\nReturn one final generated diagram image. Include image output, not text only."
        + metadata,
        *[image_part(path) for path in ref_images],
    ]
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
            )
        except Exception as exc:
            last_error = exc
            if "429" not in str(exc) or attempt >= retries:
                break
            delay = min(retry_max_delay, retry_initial_delay * (2**attempt))
            delay *= random.uniform(0.85, 1.15)
            print(
                f"429 quota/rate limit; retry {attempt + 1}/{retries} after {delay:.1f}s",
                file=sys.stderr,
                flush=True,
            )
            time.sleep(delay)
    raise RuntimeError(str(last_error))


def extract_outputs(response: object, output_dir: Path, slug: str) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    text_chunks: list[str] = []
    candidates = getattr(response, "candidates", None) or []
    parts = []
    if candidates:
        content = getattr(candidates[0], "content", None)
        parts = getattr(content, "parts", None) or []
    for index, part in enumerate(parts):
        text = getattr(part, "text", None)
        if text:
            text_chunks.append(text)
        inline = getattr(part, "inline_data", None)
        data = getattr(inline, "data", None) if inline else None
        if data:
            mime = getattr(inline, "mime_type", None) or "image/png"
            ext = ".jpg" if mime == "image/jpeg" else ".png"
            path = output_dir / f"{slug}-{index:02d}{ext}"
            path.write_bytes(data)
            paths.append(path)
    if text_chunks:
        (output_dir / f"{slug}.txt").write_text("\n\n".join(text_chunks), encoding="utf-8")
    if not paths:
        raw = response.model_dump_json(indent=2) if hasattr(response, "model_dump_json") else repr(response)
        (output_dir / f"{slug}-response.json").write_text(raw, encoding="utf-8")
        raise RuntimeError(f"No image part returned for {slug}; saved raw response JSON.")
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Gemini/Vertex diagram images with google-genai.")
    parser.add_argument("--model", default=os.environ.get("GEMINI_IMAGE_MODEL", DEFAULT_MODEL))
    parser.add_argument("--ref-image", type=Path, action="append", help="Reference image. Can be repeated.")
    parser.add_argument("--ref-glob", action="append", help="Glob of reference images, relative to repo root or absolute.")
    parser.add_argument("--no-ref", action="store_true", help="Do not send the default reference image.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--only", choices=sorted(PROMPTS), nargs="*")
    parser.add_argument("--start", type=int, default=0, help="Zero-based start index within the selected prompt list.")
    parser.add_argument("--limit", type=int, help="Generate only the first N selected prompts.")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel Gemini requests.")
    parser.add_argument("--skip-existing", action="store_true", help="Skip prompts that already have at least one output image.")
    parser.add_argument("--rate-limit-seconds", type=float, default=15.0, help="Delay between sequential requests when --workers 1.")
    parser.add_argument("--retries", type=int, default=8, help="Number of retries for 429 quota/rate-limit errors.")
    parser.add_argument("--retry-initial-delay", type=float, default=30.0, help="Initial 429 retry delay in seconds.")
    parser.add_argument("--retry-max-delay", type=float, default=300.0, help="Maximum 429 retry delay in seconds.")
    parser.add_argument("--suffix", default="")
    return parser.parse_args()


def generate_one(
    slug: str,
    args: argparse.Namespace,
    credential: str,
    ref_images: list[Path],
) -> list[Path]:
    output_slug = f"{slug}{args.suffix}"
    if args.skip_existing and any(args.output_dir.resolve().glob(f"{output_slug}-*.png")):
        return []
    response = call_genai(
        PROMPTS[slug],
        ref_images,
        args.model,
        credential,
        args.retries,
        args.retry_initial_delay,
        args.retry_max_delay,
    )
    return extract_outputs(response, args.output_dir.resolve(), output_slug)


def resolve_ref_images(args: argparse.Namespace) -> list[Path]:
    paths = [] if args.no_ref else [DEFAULT_REF_IMAGE.resolve()]
    paths.extend(path.resolve() for path in (args.ref_image or []))
    for pattern in args.ref_glob or []:
        glob_root = Path(pattern)
        if glob_root.is_absolute():
            matches = sorted(glob_root.parent.glob(glob_root.name))
        else:
            matches = sorted(ROOT.glob(pattern))
        paths.extend(path.resolve() for path in matches if path.is_file())
    seen: set[Path] = set()
    unique = []
    for path in paths:
        if path in seen:
            continue
        if not path.exists():
            raise SystemExit(f"Reference image not found: {path}")
        seen.add(path)
        unique.append(path)
    return unique


def main() -> int:
    load_env()
    args = parse_args()
    if args.limit is not None and args.limit < 1:
        raise SystemExit("--limit must be greater than 0.")
    if args.start < 0:
        raise SystemExit("--start must be 0 or greater.")
    if args.workers < 1:
        raise SystemExit("--workers must be greater than 0.")
    if args.retries < 0:
        raise SystemExit("--retries must be 0 or greater.")
    if args.rate_limit_seconds < 0:
        raise SystemExit("--rate-limit-seconds must be 0 or greater.")
    credential = required_env("GEMINI_API_KEY")
    ref_images = resolve_ref_images(args)
    if ref_images:
        print("reference images: " + ", ".join(path.relative_to(ROOT).as_posix() for path in ref_images), flush=True)
    else:
        print("reference images: none", flush=True)
    selected = args.only or list(PROMPTS)
    selected = selected[args.start :]
    if args.limit is not None:
        selected = selected[: args.limit]

    if args.workers == 1:
        for index, slug in enumerate(selected):
            print(f"generating {slug}", flush=True)
            paths = generate_one(slug, args, credential, ref_images)
            for path in paths:
                print(path.relative_to(ROOT), flush=True)
            if index != len(selected) - 1 and args.rate_limit_seconds:
                print(f"waiting {args.rate_limit_seconds:.1f}s before next request", flush=True)
                time.sleep(args.rate_limit_seconds)
        return 0

    print(f"generating {len(selected)} diagrams with {args.workers} parallel workers", flush=True)
    failures: list[tuple[str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(generate_one, slug, args, credential, ref_images): slug
            for slug in selected
        }
        for future in concurrent.futures.as_completed(futures):
            slug = futures[future]
            try:
                paths = future.result()
            except Exception as exc:
                failures.append((slug, str(exc)))
                print(f"failed {slug}: {exc}", file=sys.stderr, flush=True)
                continue
            for path in paths:
                print(path.relative_to(ROOT), flush=True)
    if failures:
        print("\nFailures:", file=sys.stderr)
        for slug, message in failures:
            print(f"- {slug}: {message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
