# Unit 1 Page 48 Image Understanding

## Page Overview
The purpose of this slide is to introduce **Linear Discriminant Analysis (LDA)** as a linear method for classification and dimensionality reduction. It explains the fundamental objective of LDA—finding an optimal projection for class separation—and mentions its extension to multi-class problems. A visual scatter plot is provided to illustrate how a projection direction is chosen to distinguish between two data clusters.

## Visible Text
*   **Title:** Linear Method: Linear Discriminant Analysis (LDA)
*   **Bullet Point 1:** LDA finds the projection that best separates the two classes
*   **Bullet Point 2:** Multiple discriminant analysis (MDA) extends LDA to multiple classes
*   **Diagram Label:** Best projection direction for classification
*   **Footer (Left):** 4/22/2019
*   **Footer (Right):** 24

## Visual Layout
*   **Title Position:** Located at the top left, written in a dark blue serif font. It is underlined by a thin blue horizontal line.
*   **Decorative Elements:** A small icon consisting of overlapping red, yellow, and blue squares is placed to the left of the title. The left margin features stylized, thin brown curved lines.
*   **Content Blocks:** The text is organized into two blue bullet points in the upper half of the slide. The lower half is occupied by a large scatter plot diagram.
*   **Colors:** The text is primarily dark blue. The diagram uses red and cyan for data points and a bold blue for the projection vector.
*   **Spacing and Alignment:** The text is left-aligned. The diagram is centered horizontally below the text. The slide has a clean white background with a light green border on the right and bottom edges.

## Diagram Type
The main visual is a **2D Scatter Plot with a Projection Vector**. It is used to demonstrate a supervised dimensionality reduction technique where data points from two different classes are projected onto a lower-dimensional subspace (a 1D line) to maximize their separability.

## Diagram / Visual Explanation
*   **Axes:** The diagram features a standard 2D coordinate system with a vertical Y-axis and a horizontal X-axis, both represented by black arrows.
*   **Data Points:**
    *   **Red Circles:** Represent Class 1, clustered primarily in the lower-left region of the plot.
    *   **Cyan (Light Blue) Circles:** Represent Class 2, clustered primarily in the upper-right region.
*   **Projection Vector:** A thick, bold blue arrow originates near the origin and points diagonally toward the top-right. 
*   **Meaning:** This arrow represents the "Best projection direction." If you were to drop perpendicular lines from every red and cyan dot onto this blue arrow, the resulting points on the arrow would show the maximum possible distance between the centers of the two groups while keeping each group tightly clustered. This makes it easier to draw a single threshold point on that line to classify new data.

## Math / Formula / Curve Notes
No mathematical formula is explicitly written on this page. However, the blue arrow represents a linear transformation vector $\mathbf{w}$ that maximizes the Fisher criterion:
$$J(\mathbf{w}) = \frac{\mathbf{w}^T S_B \mathbf{w}}{\mathbf{w}^T S_W \mathbf{w}}$$
Where $S_B$ is the between-class scatter matrix and $S_W$ is the within-class scatter matrix.

## Table Description
No table is visible on this page.

## Concept Explanation
**Linear Discriminant Analysis (LDA)** is a supervised learning algorithm used for both classification and dimensionality reduction. 
*   **Goal:** Unlike Principal Component Analysis (PCA), which looks for directions of maximum variance regardless of class, LDA specifically looks for a direction (projection) that maximizes the separation between multiple classes.
*   **Mechanism:** It achieves this by maximizing the distance between the means of the classes (between-class variance) while minimizing the spread within each class (within-class variance).
*   **MDA:** While basic LDA is designed for two classes, **Multiple Discriminant Analysis (MDA)** is the generalization used when there are three or more classes.

## Exam / Viva Points
*   **Definition:** LDA is a linear method used to find a feature subspace that maximizes class separability.
*   **Supervised vs. Unsupervised:** LDA is **supervised** because it uses class labels to find the best projection, unlike PCA which is unsupervised.
*   **Optimization Criterion:** LDA maximizes the ratio of between-class variance to within-class variance.
*   **Extension:** Multiple Discriminant Analysis (MDA) is the multi-class version of LDA.
*   **Visual Interpretation:** In a 2D plot, the "best projection" is the line where the shadows (projections) of the two data clusters have the least amount of overlap.

## Diagram Recreation Prompt
Create a clean, academic slide diagram showing Linear Discriminant Analysis. 
1.  Draw a 2D coordinate system with black X and Y axes.
2.  Plot two distinct clusters of circles: one cluster of 12-15 red circles in the bottom-left area and one cluster of 12-15 cyan circles in the top-right area. The clusters should have a slight diagonal orientation.
3.  Draw a thick, bold blue arrow starting from the origin $(0,0)$ and extending diagonally through the space between the two clusters toward the top-right corner.
4.  Add a text label in blue next to the arrowhead: "Best projection direction for classification".
5.  Ensure the background is white and the overall look is professional for a machine learning lecture.

## Diagram Data
*   **Title:** Linear Method: Linear Discriminant Analysis (LDA)
*   **Bullet Points:**
    *   LDA finds the projection that best separates the two classes
    *   Multiple discriminant analysis (MDA) extends LDA to multiple classes
*   **Scatter Plot Data (Inferred):**
    *   **Class 1 (Red):** Points roughly centered around $(2, 2)$ with some spread.
    *   **Class 2 (Cyan):** Points roughly centered around $(6, 6)$ with some spread.
    *   **Vector:** A line defined by $y = x$ (or similar diagonal) representing the projection axis.
    *   **Annotation:** "Best projection direction for classification" pointing to the vector.
