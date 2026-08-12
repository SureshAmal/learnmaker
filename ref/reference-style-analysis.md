# Reference Style Analysis

This folder contains 37 reference images. They share a technical/scientific illustration style suitable for educational diagrams, math plots, and ML course figures.

## Overall Style

The visual language is clean, precise, and textbook-like:

- Wide horizontal figure layouts.
- White or very pale gray background.
- High information density but controlled spacing.
- Small, accurate labels around the diagram.
- Thin gray outlines and construction lines.
- Color is used to encode data, categories, layers, or optical/scientific properties.
- No dark theme or decorative slide-card treatment.
- Most figures look like exported vector diagrams, not screenshots.

## Major Reference Categories

### 1. Scientific Curve And Spectrum Plots

Visual traits:

- Thin x/y axes.
- Light grid or no grid.
- Smooth colored curves.
- Legends are compact.
- Gradient spectrum bars are used only when the concept needs a continuous scale.
- Labels are small and precise.

Use for:

- Regression curves.
- Bias-variance curves.
- Cost/loss curves.
- ROC/AUC curves.
- Gradient descent objective curves.
- Probability distributions.
- Activation functions.

Prompt direction:

```text
Use a clean scientific plot style with white background, thin axes, light gray grid, smooth colored curves, compact legend, and small leader-line annotations.
```

### 2. Color/Surface/3D Math Figures

Visual traits:

- White background.
- Smooth surfaces with rainbow or pastel gradients.
- Thin axes and minimal labels.
- Perspective is controlled, not dramatic.
- Surface color represents quantity, not decoration.

Use for:

- Cost-function surfaces.
- Gradient descent landscapes.
- 3D feature spaces.
- Model decision surfaces.
- Convex/non-convex comparison.

Prompt direction:

```text
Use a clean 3D mathematical surface view with thin gray axes, smooth pastel/rainbow surface, minimal labels, and a compact perspective that keeps all labels readable.
```

### 3. Layered Technical Exploded Diagrams

Visual traits:

- Stack/layer composition.
- Semi-transparent layers or pastel fills.
- Thin leader lines pointing to labels.
- Slight isometric view.
- Important components separated vertically with even spacing.

Use for:

- Neural network layer stacks.
- Feature extraction layers.
- CNN architecture.
- Model deployment pipeline layers.
- Data preprocessing layers.

Prompt direction:

```text
Create a clean exploded-layer technical diagram with soft pastel layers, thin gray outlines, side labels with leader lines, and a centered isometric layout on a white background.
```

### 4. Flow And Process Diagrams

Visual traits:

- Simple boxes or nodes.
- Thin arrow connectors.
- Mostly horizontal or compact multi-row layouts.
- Labels are short and readable.
- Minimal color accents.

Use for:

- ML lifecycle.
- Pattern recognition workflow.
- Data preprocessing steps.
- Training/evaluation pipeline.
- Deployment/monitoring pipeline.

Prompt direction:

```text
Use a compact two-row horizontal flowchart with white rounded nodes, thin gray arrows, small colored step markers, and generous slide margins.
```

### 5. Geometric And Coordinate Diagrams

Visual traits:

- Coordinate axes with light construction grids.
- Thin blue/gray geometry lines.
- Points and shapes are cleanly drawn.
- Labels sit outside the shape with leader lines.

Use for:

- Feature space.
- Decision boundaries.
- Distance metrics.
- SVM margin.
- k-nearest neighbors.
- PCA projections.

Prompt direction:

```text
Use a clean coordinate geometry style with thin axes, pale grid, precise points/lines, and external labels connected by leader lines.
```

### 6. Tables, Matrices, And Pixel Grids

Visual traits:

- Small matrix/table layout.
- Thin gray grid lines.
- Light header or highlighted cells.
- Pixel/block graphics for image data or confusion matrices.
- Labels are close but not overlapping.

Use for:

- Confusion matrix.
- Categorical encoding tables.
- Feature matrix.
- Train/test splits.
- Image pixel representation.
- Kernel/filter diagrams.

Prompt direction:

```text
Use a clean matrix/table style with thin grid lines, light header shading, readable dark text, and muted highlight colors for important cells.
```

### 7. Tree And Hierarchy Diagrams

Visual traits:

- Balanced branches.
- Thin connector lines.
- Compact node labels.
- White background.
- Little to no decorative color except final class/cluster labels.

Use for:

- Decision trees.
- Hierarchical clustering dendrograms.
- Taxonomies of ML algorithms.
- Supervised/unsupervised/reinforcement split diagrams.

Prompt direction:

```text
Create a balanced technical tree diagram with thin gray connectors, white nodes, compact labels, and muted color only for final categories.
```

## Reference Style Do / Do Not

Do:

- Prefer white background.
- Use thin lines.
- Use accurate labels.
- Keep diagrams wide and compact.
- Use color only for meaning.
- Use leader lines for annotations.
- Keep text readable and horizontally aligned.
- Use exact formulas and variables.

Do not:

- Use dark slide backgrounds.
- Make tall vertical diagrams when a two-row layout fits better.
- Use heavy shadows or glossy gradients.
- Use random decorative icons.
- Use thick borders.
- Place text over dense plots or shapes.
- Let labels overlap.
- Invent extra variables or incorrect formulas.

## Mapping Course Content To Prompt Template

| Course visual need | Best template |
| --- | --- |
| ML pipeline, preprocessing, modeling workflow | Flowchart / Pipeline |
| Cost function, gradient descent, bias-variance | Mathematical Curve / Function Plot |
| Regression line or polynomial fit | Scatter Plot / Curve Plot |
| k-means, DBSCAN, classification boundary | Scatter Plot / Clustering |
| Decision tree, hierarchical clustering | Decision Tree / Hierarchy |
| Confusion matrix, metric comparison | Table / Matrix |
| Normalization, standardization, entropy, Gini | Formula / Equation Visual |
| Neural network or CNN | Layered Architecture / Stack |
| PCA, SVM margin, feature space | Geometric / Coordinate Diagram |

## Standard Slide-Fit Layout Rules

- Use 16:9 landscape.
- Keep main figure within 80% width and 75% height.
- Leave at least 8% margin on all sides.
- For 7 or more flow steps, use two rows.
- For formulas plus plot, use split panel: formula left, plot right.
- For table plus explanation, use table center with callouts around it.
- For dense labels, push labels outside the main drawing and use leader lines.

## Preferred Prompt Ending

Add this ending to all prompts:

```text
The final image must be crisp, slide-ready, and readable at classroom projection size. Keep all labels accurate and inside the canvas. Match the clean scientific reference style: white background, thin gray geometry, restrained colors, precise spacing, and no decorative dark UI styling.
```
