# Unit 1 Page 150 Image Understanding

## Page Overview
The purpose of this slide is to explain the fundamental objective of **Fisher's Linear Discriminant (FLD)**. It visually demonstrates how FLD finds an optimal projection direction that maximizes the separation between two classes by simultaneously maximizing the distance between their means and minimizing the variance within each class.

## Visible Text
*   **Main Heading:** "For fully separate them, Fisher’s linear discriminant minimizes the within-class variance of the projections at the same time as maximizing the projections between the means." (Note: The text contains a minor grammatical error; it likely intended to say "To fully separate them...")
*   **Left Plot Legend:**
    *   Fisher Linear Discriminant Direction (indicated by a blue line)
    *   Decision Boundary (indicated by an orange line)
*   **Left Plot Axes:**
    *   Y-axis: Range from -10.0 to 10.0
    *   X-axis: Range from -10.0 to 10.0
*   **Right Plot Legend:**
    *   Class 1 (purple square)
    *   Class 2 (teal square)
*   **Right Plot Axes:**
    *   Y-axis: Frequency/Count, range from 0 to 70
    *   X-axis: Projected values, range from -15 to 15

## Visual Layout
*   **Background:** A light blue gradient background with abstract curved lines on the left side.
*   **Header Section:** A dark grey arrow-shaped banner on the far left, followed by the main explanatory text in a bold, sans-serif blue font.
*   **Content Area:** Two side-by-side plots occupy the center and bottom of the slide.
    *   **Left Plot:** A 2D scatter plot showing two distinct clusters of data points with overlaid contour lines and two intersecting lines.
    *   **Right Plot:** A 1D histogram showing the distribution of the two classes after projection.
*   **Color Coding:** 
    *   **Purple:** Represents Class 1 data points and its corresponding histogram.
    *   **Teal:** Represents Class 2 data points and its corresponding histogram.
    *   **Blue Line:** Represents the projection vector.
    *   **Orange Line:** Represents the resulting decision boundary.

## Diagram Type
The slide features two related **mathematical graphs**: a **2D Scatter Plot with Contours** and a **1D Projection Histogram**. These are used to visualize the transformation of data from a high-dimensional space to a lower-dimensional space optimized for classification.

## Diagram / Visual Explanation
*   **Left Plot (2D Feature Space):**
    *   Shows two classes of data: **Class 1 (purple)** and **Class 2 (teal)**.
    *   **Contour Lines:** The concentric ellipses around each cluster represent the probability density (covariance) of the classes.
    *   **Fisher Linear Discriminant Direction (Blue Line):** This is the vector $\mathbf{w}$ onto which the 2D data is projected. FLD chooses this specific angle to ensure that when points are dropped onto this line, the two groups stay as far apart as possible while staying tightly bunched together.
    *   **Decision Boundary (Orange Line):** This line is perpendicular to the projection direction. It represents the threshold used to classify new data points.
*   **Right Plot (1D Projected Space):**
    *   This histogram shows the result of projecting all the 2D points from the left plot onto the blue line.
    *   The x-axis represents the position along the blue line.
    *   **Separation:** Because FLD was used, the purple and teal histograms are widely separated with almost no overlap. The means are far apart, and the "spread" (variance) of each colored block is narrow.

## Math / Formula / Curve Notes
While no explicit formulas are written, the text describes the **Fisher Criterion** $J(\mathbf{w})$:
$$J(\mathbf{w}) = \frac{(\mu_2 - \mu_1)^2}{s_1^2 + s_2^2}$$
*   **$(\mu_2 - \mu_1)^2$:** The squared difference between the means of the projected classes (maximizing the "projections between the means").
*   **$s_1^2 + s_2^2$:** The sum of the within-class variances of the projected classes (minimizing the "within-class variance").
*   The **contour lines** in the left plot represent Gaussian distributions where the ellipses' orientation indicates the correlation between the two features.

## Table Description
No table is visible on this page.

## Concept Explanation
**Fisher's Linear Discriminant (FLD)** is a supervised dimensionality reduction technique. Unlike Principal Component Analysis (PCA), which looks for directions of maximum total variance regardless of class labels, FLD specifically looks for a direction that makes the classes as discriminable as possible.

It achieves this by balancing two goals:
1.  **Maximize Between-Class Variance:** Push the centers (means) of the classes as far apart as possible.
2.  **Minimize Within-Class Variance:** Keep the data points of each individual class as close to their respective centers as possible.

By doing both, FLD creates a projection where classes have minimal overlap, making it much easier for a simple linear classifier (the decision boundary) to separate them accurately.

## Exam / Viva Points
*   **Objective of FLD:** To find a projection that maximizes the ratio of between-class variance to within-class variance.
*   **Supervised vs. Unsupervised:** FLD is **supervised** because it requires class labels to calculate means and variances. PCA is unsupervised.
*   **Projection Direction:** The blue line in the diagram represents the weight vector $\mathbf{w}$.
*   **Decision Boundary:** In a 2D space, the decision boundary is a line perpendicular to the projection vector. In higher dimensions, it is a hyperplane.
*   **Why minimize within-class variance?** Even if means are far apart, high variance within classes can cause them to overlap significantly, leading to classification errors. Minimizing variance ensures "tight" clusters.

## Diagram Recreation Prompt
Create a professional machine learning slide graphic with two panels. 
**Left Panel:** A 2D scatter plot. Plot two Gaussian clusters: Class 1 (purple dots) centered at (-4, 1) and Class 2 (teal dots) centered at (4, -1). Add 3-4 concentric elliptical contour lines around each cluster to show density. Draw a solid blue line passing through the origin with a slope of approximately -1.5 (label: "Fisher Linear Discriminant Direction"). Draw a solid orange line perpendicular to the blue line that passes between the two clusters (label: "Decision Boundary"). 
**Right Panel:** A 1D histogram. Show two distinct, non-overlapping bell-shaped histograms. The left one is purple (Class 1) and the right one is teal (Class 2). The x-axis should represent the projected values. 
**General Style:** Use a clean white or light blue background, clear legends, and a bold blue title: "Fisher's Linear Discriminant Objective".

## Diagram Data
*   **Left Plot Data:**
    *   **Class 1:** Mean $\approx (-4, 1)$, Covariance $\approx [[5, 1], [1, 2]]$, Color: Purple.
    *   **Class 2:** Mean $\approx (4, -1)$, Covariance $\approx [[5, 1], [1, 2]]$, Color: Teal.
    *   **Projection Vector:** Line $y = -1.5x$ (Blue).
    *   **Decision Boundary:** Line $y = 0.67x$ (Orange).
*   **Right Plot Data:**
    *   **Class 1 Histogram:** Normal distribution centered at $\approx -8$, $\sigma \approx 2$.
    *   **Class 2 Histogram:** Normal distribution centered at $\approx 8$, $\sigma \approx 2$.
    *   **Overlap:** Minimal to zero at $x=0$.
