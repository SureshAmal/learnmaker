# Unit 1 Page 151 Image Understanding

## Page Overview
The purpose of this slide is to define the fundamental objective of Fisher's Discriminant Analysis (FDA), a dimensionality reduction technique used in machine learning and statistics. It outlines the two primary criteria used to find an optimal projection for classification tasks.

## Visible Text
**GOAL OF FDA:**

*   To project high-dimensional data onto a **line** (or lower-dimensional space) such that:
*   The **distance between class means** is **maximized**.
*   The **variance within each class** is **minimized**.

## Visual Layout
*   **Title:** The title "GOAL OF FDA:" is positioned at the top, aligned slightly to the left, and rendered in a bold, bright pink/magenta font.
*   **Content Blocks:** The main content consists of three bulleted points. The first point introduces the action (projection), and the following two points (indented slightly) describe the specific optimization constraints.
*   **Colors:** 
    *   Background: A light blue to white gradient.
    *   Text: Dark gray/black for the body text, with specific keywords in bold.
    *   Accents: A dark gray arrow-like shape in the top left corner and thin, sweeping dark blue curved lines on the far left side.
*   **Visual Hierarchy:** The pink title draws immediate attention, followed by the bolded keywords in the bullet points ("line", "distance between class means", "maximized", "variance within each class", "minimized"), which summarize the core logic of the algorithm.

## Diagram Type
This is a **text-only slide**. It uses bullet points and bold text to convey conceptual information rather than using a flowchart, graph, or architecture diagram.

## Diagram / Visual Explanation
No diagram is present on this page.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page. However, the text describes mathematical concepts:
*   **Projection:** Mapping a vector from a high-dimensional space $\mathbb{R}^d$ to a lower-dimensional space $\mathbb{R}^k$ (where $k < d$).
*   **Class Means:** The average position of data points belonging to a specific category.
*   **Variance:** The spread or dispersion of data points around their respective class mean.

## Table Description
No table is visible on this page.

## Concept Explanation
Fisher's Discriminant Analysis (FDA), often used interchangeably with Linear Discriminant Analysis (LDA) in certain contexts, is a method used to find a linear combination of features that characterizes or separates two or more classes of objects.

Unlike Principal Component Analysis (PCA), which seeks to capture the maximum variance in the data regardless of class labels, FDA is **supervised**. Its goal is to reduce dimensions while preserving as much class-discriminatory information as possible.

To achieve this, it looks for a projection (a direction or "line") that satisfies two conditions simultaneously:
1.  **Maximize Between-Class Variance:** It wants the centers (means) of the different classes to be as far apart as possible after projection. This makes the classes easier to distinguish.
2.  **Minimize Within-Class Variance:** It wants the data points within each class to be tightly clustered together after projection. This reduces the overlap between classes.

The "Fisher Criterion" is the ratio of the between-class variance to the within-class variance. FDA works by maximizing this ratio.

## Exam / Viva Points
*   **What does FDA stand for?** Fisher's Discriminant Analysis.
*   **What is the primary goal of FDA?** To project high-dimensional data into a lower-dimensional space (like a line) to improve class separability.
*   **What are the two optimization criteria for FDA?** 
    1. Maximize the distance between the means of different classes (Between-class scatter).
    2. Minimize the variance/spread within each individual class (Within-class scatter).
*   **How does FDA differ from PCA?** PCA is unsupervised and focuses on total variance; FDA is supervised and focuses on class separation.
*   **Why project onto a line?** Projecting onto a single dimension (a line) is the simplest form of dimensionality reduction that allows for a clear decision boundary (a threshold point) to be set between two classes.

## Diagram Recreation Prompt
Create a professional educational slide titled "GOAL OF FDA:" in bold magenta. The background should be a clean light-blue gradient. On the left, include a conceptual illustration: show a 2D scatter plot with two distinct clusters of points (red and blue). Draw a dashed line representing the "optimal projection line." Show the points being projected onto this line. Annotate the line to show that the projected means are far apart (maximized distance) and the clusters on the line are tight (minimized variance). To the right of the illustration, list the following bullet points in dark gray text: 
- Project high-dimensional data onto a **line** (or lower-dimensional space).
- **Maximize** the distance between class means.
- **Minimize** the variance within each class.

## Diagram Data
*   **Title:** GOAL OF FDA:
*   **Point 1:** Project high-dimensional data onto a line (or lower-dimensional space).
*   **Point 2:** Maximize distance between class means.
*   **Point 3:** Minimize variance within each class.
*   **Visual Elements:** Dark gray arrow (top left), blue curved decorative lines (left edge).
