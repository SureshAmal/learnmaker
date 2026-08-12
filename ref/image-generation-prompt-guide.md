# Reference Image Generation Prompt Guide

Use this guide when prompting an image model to create educational machine-learning diagrams, plots, mathematical visuals, flow diagrams, or technical illustrations in the same style as the images in this `ref/` folder.

## Reference Style Summary

The reference images use a clean scientific textbook style. The canvas is mostly white or very light gray, with precise geometry, thin construction lines, readable labels, and selective color only where it explains meaning. The style is technical, minimal, and high clarity rather than decorative.

Core visual qualities:

- White or near-white background.
- Wide horizontal composition, usually slide-friendly.
- Thin gray or black outlines.
- Fine axis lines, leader lines, and annotation ticks.
- Small but sharp sans-serif labels.
- Carefully spaced labels outside the main object when possible.
- Muted technical colors with occasional saturated accent colors.
- Diagrams are compact and centered with generous white space.
- No dark theme, no heavy shadows, no glossy UI cards, no decorative gradients unless the diagram itself is a scientific color gradient.
- No clutter: every color, arrow, label, and shape must explain something.

## Universal Prompt Formula

Use this structure for every generated image:

```text
Create a clean scientific educational diagram in the style of the provided reference images.

Subject: <exact ML/math concept>
Diagram type: <flowchart | curve plot | scatter plot | decision tree | pipeline | formula visual | comparison table | architecture diagram | layered system | data distribution | clustering diagram>
Canvas: wide 16:9 landscape, white background, generous margins, centered composition.
Style: precise textbook/vector illustration, thin gray construction lines, sharp sans-serif labels, minimal color, no dark background, no decorative UI cards.
Color palette: white background, charcoal text, light gray axes/lines, accent colors only for categories or important regions.
Layout: <describe left-to-right, top-to-bottom, grid, split-panel, or compact flow layout>
Labels: include all labels exactly as written: <label list>
Data/geometry: <nodes, edges, axes, formulas, plotted curve shape, cluster coordinates, table rows>
Explanation focus: the visual must make <learning point> obvious.
Quality constraints: high-resolution, crisp lines, all text readable, no cropped labels, no overlapping text, no unnecessary decoration.
Avoid: dark theme, blurred text, random icons, photorealism, 3D gimmicks unless requested, noisy backgrounds, incorrect formulas, misspelled labels.
```

## Global Style Instructions

Add these lines to most prompts:

```text
Use a clean white canvas with subtle gray guide lines.
Use a neutral sans-serif font similar to Helvetica/Arial.
Use thin 1-2 px strokes for axes, arrows, connectors, and outlines.
Keep labels small but readable, horizontally aligned when possible.
Use leader lines for labels instead of placing text on top of shapes.
Use accent color only to encode categories, stages, regions, or curves.
Keep enough whitespace around the diagram so it fits fully on a slide.
Make the image look like a polished scientific textbook figure, not a marketing graphic.
```

## Color System

Preferred colors:

```text
Background: #ffffff or #f8f9fb
Primary text: #202124 or #222222
Secondary labels: #555555
Thin construction lines: #b8bec7
Axis/grid lines: #d5d9df
Main outline: #555555 or #333333
Blue accent: #2563eb
Green accent: #22a06b
Red accent: #e5484d
Yellow accent: #f4c430
Purple accent: #8b5cf6
Cyan accent: #06b6d4
```

Rules:

- Use black/gray for structure.
- Use bright colors only for data categories, clusters, curves, or highlighted regions.
- Use transparent pastel fills for probability areas, decision regions, or distributions.
- Avoid large saturated backgrounds.
- Avoid one-color diagrams where every element is the same hue.

## Typography Rules

```text
Use a clean sans-serif font.
Use uppercase only for short technical labels, not long sentences.
Use 10-14 pt label scale relative to a 16:9 slide.
Keep formula text sharp and mathematically correct.
Use consistent label placement and alignment.
Do not warp, stylize, or handwrite text.
Do not let text overlap axes, arrows, boxes, or data points.
```

## Flowchart / Pipeline Prompt Template

Use for ML pipeline, data preprocessing pipeline, pattern recognition workflow, training workflow, model deployment workflow.

```text
Create a compact horizontal scientific flowchart in the reference style.
Canvas: 16:9 white background.
Layout: arrange the process as two rows or a left-to-right compact pipeline, not one tall vertical column.
Nodes: rounded rectangles with thin gray outline, white fill, subtle colored top strip or small colored dot for stage category.
Connectors: thin gray arrows with simple arrowheads.
Text: short labels centered inside each node, dark charcoal, readable.
Spacing: equal gaps, aligned centers, generous margins.
Add small stage numbers in muted blue circles.
No shadows, no dark boxes, no decorative cards.

Nodes:
1. <node 1>
2. <node 2>
...

Edges:
<node 1> -> <node 2>
...

If there are more than 6 steps, wrap into two balanced rows with a clear continuation arrow.
```

Example for ML pipeline:

```text
Create a compact two-row ML lifecycle flowchart in a clean scientific textbook style.
White background, thin gray connector arrows, small blue numbered circles, rounded white nodes with subtle pastel header strips.
Row 1: Problem Definition -> Data Collection -> Data Cleaning and Preprocessing -> Exploratory Data Analysis -> Feature Engineering.
Row 2: Model Selection -> Model Training -> Model Evaluation and Tuning -> Model Deployment -> Model Monitoring and Maintenance.
Use one clean continuation arrow from row 1 to row 2. Keep all text readable and fit inside a 16:9 slide.
```

## Mathematical Curve / Function Plot Template

Use for regression curves, loss curves, cost functions, sigmoid, bias-variance, overfitting/underfitting, gradient descent, ROC, error surfaces.

```text
Create a clean mathematical plot in the reference scientific style.
Canvas: white 16:9, centered plot area.
Axes: thin charcoal x-axis and y-axis, light gray grid, tick marks minimal.
Labels: x-axis "<x label>", y-axis "<y label>", title "<title>".
Curves: draw smooth colored curves with 2-3 px stroke.
Annotations: use thin leader lines and small labels for important points.
Fills: use translucent pastel fill only if showing area, confidence region, or decision region.
Legend: compact legend in top-right or outside plot; no box if possible.
No 3D unless the concept requires an error surface.

Data/shape:
<describe exact curve shape or data points>

Learning point:
<what the student should understand from the curve>
```

Example for bias-variance:

```text
Create a clean bias-variance tradeoff plot.
White background, light gray grid, thin axes.
x-axis: Model Complexity. y-axis: Error.
Draw three smooth curves: Bias^2 decreasing in blue, Variance increasing in red, Total Error U-shaped in dark charcoal.
Mark the minimum total error point with a small green dot and label "best generalization".
Use compact labels with leader lines, no overlapping text, no dark theme.
```

## Scatter Plot / Clustering Template

Use for k-means, hierarchical clustering, DBSCAN, classification boundaries, regression points.

```text
Create a clean 2D scatter plot in the reference scientific style.
Canvas: 16:9 white background.
Plot area: centered with light gray grid and thin axes.
Points: small colored geometric markers, one color per class/cluster.
Centroids: black plus signs or outlined stars.
Decision regions: very light translucent pastel fills with thin boundary lines.
Labels: cluster names, centroid labels, axis labels, and legend.
Keep all labels outside dense point regions using leader lines.

Data:
<cluster centers, approximate point groups, boundary lines, axes>

Do not add random extra points beyond the specified data.
```

## Table / Matrix Prompt Template

Use for confusion matrix, comparison table, feature table, evaluation metrics, categorical encoding, train/test split.

```text
Create a clean technical table diagram in the reference style.
Canvas: white background, wide 16:9.
Table: thin gray grid lines, light gray header row, dark charcoal text.
Highlight important cells with muted pastel fills.
Use consistent column widths and row heights.
Add short labels or callouts outside the table with thin leader lines.
No heavy borders, no dark backgrounds, no decorative icons.

Columns:
<column names>

Rows:
<row data>

Emphasis:
<cells or comparisons to highlight>
```

## Formula / Equation Visual Template

Use for gradient descent update rule, cost function, normalization, standardization, entropy, Gini, regression equation.

```text
Create a clean formula explainer figure in the reference scientific style.
Canvas: white 16:9.
Center the main equation in large crisp math text.
Use thin leader lines from each symbol to small explanatory labels.
Place related examples or mini diagrams around the equation with generous spacing.
Use one accent color to highlight the current term being explained.
No handwritten math, no distorted symbols, no random notation.

Formula:
<exact formula>

Symbol explanations:
<symbol>: <meaning>
...
```

## Decision Tree / Hierarchy Template

Use for decision trees, hierarchical clustering, dendrograms, taxonomy diagrams.

```text
Create a clean hierarchy diagram in the reference scientific style.
Canvas: white 16:9.
Nodes: white boxes or circles with thin gray outline.
Edges: thin gray connector lines.
Layout: balanced tree, compact and centered, no cropped branches.
Use color only to distinguish final classes or cluster groups.
Labels: short, readable, horizontally aligned.
Add small annotations only where needed.

Root:
<root label>

Branches:
<parent> -> <child> [condition/meaning]
...
```

## 3D Surface / Error Landscape Template

Use only when a 3D surface helps: gradient descent, loss landscape, convex vs non-convex objective.

```text
Create a clean 3D mathematical surface plot in the reference style.
Canvas: white 16:9.
Surface: smooth pastel mesh or shaded surface, not glossy.
Axes: thin gray 3D axes with labels.
Add a highlighted descent path with small arrows and numbered points.
Use a compact perspective view with no cropping.
Keep labels outside the surface when possible.

x-axis: <label>
y-axis: <label>
z-axis: <label>
Surface shape: <convex bowl | saddle | multi-minima landscape>
Highlighted path: <path description>
```

## Layered Architecture / Stack Template

Use for neural network layers, model deployment stack, preprocessing stack, CNN layers.

```text
Create a clean layered technical architecture diagram in the reference style.
Canvas: white 16:9.
Use isometric or slightly exploded layers only if it improves clarity.
Each layer has thin gray outline, soft pastel fill, and a short label.
Use arrows to show data flow.
Add side callouts with thin leader lines.
Keep the diagram centered with generous margins.
No photorealistic materials, no heavy shadows, no dark background.

Layers:
<layer 1>
<layer 2>
...

Flow:
<input> -> <layer sequence> -> <output>
```

## Prompt Rules For Redrawing Existing Slide Diagrams

When converting a slide diagram into a better reference-style diagram:

```text
Redraw the concept from the source slide, but do not copy its poor layout.
Keep the exact educational content and labels.
Improve the layout to match the reference style: white background, compact, centered, readable, thin gray lines, restrained accent colors.
If the original is a tall vertical flow, convert it into a balanced two-row horizontal flow.
If the original has dark boxes, convert them to white boxes with thin gray outlines and small colored stage markers.
If the original has crowded labels, move labels outside the diagram and connect them with leader lines.
If the original has a math plot, redraw axes, curves, labels, and annotations cleanly.
If the original has a table, redraw it as a clean technical table with light header shading and consistent spacing.
```

## Negative Prompt / Avoid List

Always include when using an image model that supports negative instructions:

```text
Avoid dark theme, black background, heavy shadows, glossy 3D, random icons, decorative blobs, bokeh, noisy textures, stock-photo style, cartoon style, hand-drawn sketch style, distorted text, misspelled labels, cropped labels, overlapping labels, incorrect formulas, arbitrary data, low-resolution raster text, cluttered layout, oversized arrows, thick borders, colorful background gradients.
```

## Output Quality Checklist

Before accepting a generated diagram:

- Does it fit in a 16:9 slide without cropping?
- Is every label readable?
- Are formulas correct?
- Are axes labeled?
- Are curves or points consistent with the described data?
- Are arrows pointing in the correct direction?
- Is color used for meaning, not decoration?
- Does the image use a white/light scientific style?
- Are there no dark cards, heavy shadows, or decorative backgrounds?
- Can a student understand the concept from the diagram alone?

## Reusable Master Prompt

```text
Create a polished scientific educational diagram for a machine-learning course, matching the visual style of the reference images: white background, precise vector-like geometry, thin gray outlines, clean sans-serif labels, restrained technical colors, generous white space, compact slide-friendly 16:9 composition, and no decorative UI styling.

Topic: <topic>
Diagram type: <type>
Learning goal: <goal>
Required labels: <labels>
Data or structure: <nodes/edges/table/axes/formulas/points>
Layout: <layout instructions>
Style constraints: thin lines, readable labels, muted colors, centered composition, no clutter.
Avoid: dark background, heavy shadows, random icons, wrong labels, incorrect formulas, cropped text.
```
