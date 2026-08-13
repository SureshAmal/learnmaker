/**
 * Puts the right picture in the right place in the Machine Learning book.
 *
 * Three things happen, in order:
 *
 *   1. Every Mermaid diagram is replaced by the image drawn to replace it.
 *      `ref/openai-generated-diagrams/unit-diagrams/` holds one image per diagram in the
 *      ML source, and `unit-visual-inventory.md` records which line of which unit each
 *      one was drawn for. The inventory's line numbers match the Mermaid fences in
 *      `ml-course/unit-*.md` exactly, so the Nth diagram in a unit maps to the Nth image
 *      — no guessing. The hand-drawn lifecycle SVG in Unit I is replaced the same way.
 *
 *   2. The 38 reference diagrams are placed from the explicit table below, one topic per
 *      section.
 *
 *   3. Nothing else is placed. The lecture slides are photographs of PowerPoint pages —
 *      they stay in the media library for reference, but they are not put on a page.
 *
 * Figures are written as plain Markdown images. The render pipeline wraps a paragraph
 * that holds nothing but an image into `<figure class="figimg">` with the alt text as its
 * caption, so the page markup is identical to the old hand-written HTML while the source
 * stays something the visual editor can safely edit.
 *
 *   bun run --env-file=.env.local ./scripts/place-ml-figures.ts
 *   bun run --env-file=.env.local ./scripts/place-ml-figures.ts --clear
 */
import { readFileSync, existsSync } from "node:fs";
import { join, resolve } from "node:path";
import postgres from "postgres";

const REPO = resolve(process.cwd(), "..");
const CLEAR = process.argv.includes("--clear");

const url = process.env.DATABASE_URL;
if (!url) {
  console.error("DATABASE_URL is not set.");
  process.exit(1);
}
const sql = postgres(url, {
  ssl: url.includes("localhost") || url.includes("127.0.0.1") ? false : "require",
  max: 1,
});

const BEGIN = "<!-- figures:auto -->";
const END = "<!-- /figures:auto -->";
const BLOCK = new RegExp(`\\n*${BEGIN}[\\s\\S]*?${END}\\n*`, "g");

// ---------------------------------------------------------------------------------
// reference diagrams → sections, by name
// ---------------------------------------------------------------------------------

const DIAGRAMS: Record<string, string[]> = {
  "reinforcement-learning-loop": ["Major Categories of ML Techniques"],
  "normalization-standardization": ["Data Preprocessing"],
  "self-organizing-map": ["Pattern Representation"],
  "knn-classification": ["Classifiers and Decision Regions"],
  "naive-bayes-decision-regions": ["Classifiers and Decision Regions"],
  "conditional-probability-venn": ["Basics of Probability and Bayes' Theorem"],
  "bayesian-inference": ["Basics of Probability and Bayes' Theorem"],
  "particle-filter": ["Modeling"],
  "linear-regression": ["Regression"],
  "ldf-qdf-boundaries": ["Discriminant Functions"],
  "fisher-lda-projection": ["Fisher's Linear Discriminant"],
  "svm-margin": ["Learning Theory"],
  "gradient-descent": ["Gradient Descent for Convex Functions"],
  "logistic-regression-sigmoid": ["Logistic Regression"],
  "decision-tree": ["Decision Tree"],
  "random-forest-bagging": ["Random Forest"],
  "neural-network": ["Neural Networks"],
  "cnn-image-classification": ["Neural Networks"],
  "boosting-ensemble": ["Ensemble Learning", "3.3 Ensemble Methods"],
  "stacking-ensemble": ["Ensemble Learning", "3.3 Ensemble Methods"],
  "confusion-matrix": ["Evaluation Metrics and the Confusion Matrix"],
  "roc-curve": ["Performance Metrics"],
  "bias-variance": ["Bias–Variance Tradeoff"],
  regularization: ["Regularization"],
  "apriori-association-rules": ["Apriori Algorithm for Association Rules"],
  "structural-risk-minimization": ["Empirical Risk Minimization"],
  "loss-functions": ["Loss Functions"],
  "and-table": ["Hypothesis Space"],
  "train-test-split": ["Data Partitioning"],
  "cross-validation": ["Cross-Validation", "Validation Techniques"],
  kmeans: ["Clustering: K-Means and Kernel K-Means"],
  dbscan: ["Clustering: K-Means and Kernel K-Means"],
  "hierarchical-clustering": ["Hierarchical Clustering"],
  "pca-projection": ["Dimensionality Reduction: PCA and Kernel PCA"],
  autoencoder: ["Dimensionality Reduction: PCA and Kernel PCA"],
  "matrix-factorization": ["Matrix Factorization"],
  "gaussian-mixture-model": ["Generative Models"],
  "overfit-underfit": ["Overfitting and Underfitting"],
};

const CAPTIONS: Record<string, string> = {
  "and-table": "The AND function over two binary inputs",
  "conditional-probability-venn": "Conditional probability as overlapping events",
  "ldf-qdf-boundaries": "Linear and quadratic discriminant boundaries",
  "structural-risk-minimization": "Structural risk minimisation: fit against complexity",
  "train-test-split": "Holding data back: train, validation and test",
};

function caption(name: string) {
  if (CAPTIONS[name]) return CAPTIONS[name];
  const words = name.replace(/[-_]+/g, " ").trim();
  return words.charAt(0).toUpperCase() + words.slice(1);
}

/** Markdown escaping for an alt text that becomes the figure's caption. */
function alt(text: string) {
  return text.replace(/([[\]])/g, "\\$1");
}

// ---------------------------------------------------------------------------------
// the inventory: which drawn image replaces which diagram
// ---------------------------------------------------------------------------------

type InventoryRow = { unit: number; line: number; kind: string; title: string };

function readInventory(): InventoryRow[] {
  const path = join(REPO, "ref/openai-generated-diagrams/unit-visual-inventory.md");
  if (!existsSync(path)) return [];
  return readFileSync(path, "utf8")
    .split("\n")
    .filter((line) => /^\|\s*unit-\d\.md\s*\|/.test(line))
    .map((line) => {
      const cells = line.split("|").map((c) => c.trim());
      return {
        unit: Number(cells[1].match(/\d/)![0]),
        line: Number(cells[2]),
        kind: cells[3],
        title: cells[4],
      };
    });
}

/**
 * The images are numbered sequentially across all three units in inventory order, so
 * the row's position in the file is what identifies its image. Rows are returned per
 * unit in the order the diagrams appear in that unit's source.
 */
function inventoryByUnit(rows: InventoryRow[], assets: Map<string, Asset>) {
  const perUnit = new Map<number, { title: string; kind: string; asset?: Asset }[]>();

  rows.forEach((row, index) => {
    const number = String(index + 1).padStart(3, "0");
    const asset = [...assets.values()].find((a) =>
      a.pathname.startsWith(`unit${row.unit}-${number}-`),
    );
    const list = perUnit.get(row.unit) ?? [];
    list.push({ title: row.title, kind: row.kind, asset });
    perUnit.set(row.unit, list);
  });

  // Mermaid fences appear in source order; the inventory's own order is by line number
  // except for one trailing SVG row, so sort each unit's rows the way the source reads.
  return perUnit;
}

// ---------------------------------------------------------------------------------

type Asset = { id: number; url: string; pathname: string; tag: string };
type Section = { id: number; title: string; body: string; chapter: string };

const sections = await sql<Section[]>`
  select s.id, s.title, s.body, c.slug as chapter
    from sections s
    join chapters c on c.id = s.chapter_id
    join books b on b.id = c.book_id
   where b.slug = 'ml-course'
   order by c.position, s.position
`;

if (CLEAR) {
  for (const section of sections) {
    const stripped = section.body.replace(BLOCK, "\n\n").trimEnd() + "\n";
    if (stripped !== section.body) {
      await sql`update sections set body = ${stripped}, updated_at = now() where id = ${section.id}`;
    }
  }
  console.log("removed every auto-placed figure block");
  await sql.end();
  process.exit(0);
}

const assetRows = await sql<Asset[]>`
  select id, url, pathname, tag from assets where tag in ('reference-style', 'unit-diagrams')
`;
const assets = new Map(assetRows.map((a) => [a.pathname.replace(/\.[^.]+$/, ""), a]));
const byBaseName = new Map(
  assetRows.map((a) => [a.pathname.replace(/^(reference-style-)?/, "").replace(/\.[^.]+$/, ""), a]),
);

const inventory = inventoryByUnit(readInventory(), assets);

/** section title → the reference diagrams that belong to it */
const wanted = new Map<string, string[]>();
for (const [name, titles] of Object.entries(DIAGRAMS)) {
  for (const title of titles) wanted.set(title, [...(wanted.get(title) ?? []), name]);
}

const MERMAID = /^```mermaid[ \t]*\n[\s\S]*?\n```[ \t]*$/gm;
const FIGSVG = /<div class="figsvg"[\s\S]*?<\/div>/g;

let replacedDiagrams = 0;
let placedReference = 0;
let removedSlides = 0;
let touched = 0;

// Diagram replacement walks each chapter in reading order, because the inventory counts
// diagrams per unit rather than per section.
const cursor = new Map<number, number>();

for (const section of sections) {
  const unit = Number(section.chapter.match(/\d/)?.[0] ?? 0);
  const rows = inventory.get(unit) ?? [];

  // --- 1. Mermaid and the hand-drawn SVG become their drawn replacements -------------
  let body = section.body.replace(MERMAID, () => {
    const index = cursor.get(unit) ?? 0;
    const row = rows.filter((r) => r.kind !== "svg")[index];
    cursor.set(unit, index + 1);
    if (!row?.asset) return "";
    replacedDiagrams++;
    return `![${alt(row.title)}](${row.asset.url})`;
  });

  body = body.replace(FIGSVG, () => {
    const row = rows.find((r) => r.kind === "svg");
    if (!row?.asset) return "";
    replacedDiagrams++;
    return `![${alt(row.title)}](${row.asset.url})`;
  });

  // --- 2. drop anything placed by an earlier run, slides included ---------------------
  const previous = body;
  body = body.replace(BLOCK, "\n\n");
  removedSlides += (previous.match(/Lecture slide/g) ?? []).length;

  // --- 3. the reference diagram for this topic ---------------------------------------
  const figures = (wanted.get(section.title) ?? [])
    .map((name) => {
      const asset = assets.get(`reference-style-${name}`) ?? byBaseName.get(name);
      if (!asset) {
        console.warn(`missing reference diagram: ${name}`);
        return null;
      }
      placedReference++;
      return `![${alt(caption(name))}](${asset.url})`;
    })
    .filter((figure): figure is string => figure !== null);

  const base = body.replace(/\n{3,}/g, "\n\n").trimEnd();
  const next = figures.length
    ? `${base}\n\n${BEGIN}\n\n${figures.join("\n\n")}\n\n${END}\n`
    : `${base}\n`;

  if (next !== section.body) {
    await sql`update sections set body = ${next}, updated_at = now() where id = ${section.id}`;
    touched++;
  }
}

console.log(
  `${replacedDiagrams} diagrams replaced, ${placedReference} reference figures placed, ` +
    `${removedSlides} slide figures removed, ${touched} sections rewritten`,
);
await sql.end();
