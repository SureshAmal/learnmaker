# Unit 1 Page 148 Image Understanding

## Page Overview
This slide introduces **Fisher's Linear Discriminant (FLD)** within the context of supervised learning. Its primary purpose is to define FLD as a classification tool and explain the specific mathematical objective it aims to achieve: maximizing class separation by balancing the distance between class means against the internal variance of each class.

## Visible Text
*   Fisher’s linear discriminant can be used as a supervised learning classifier.
*   Given labeled data, the classifier can find a set of weights to draw a decision boundary, classifying the data.
*   Fisher’s linear discriminant attempts to find the vector that maximizes the separation between classes of the projected data.
*   Maximizing "separation" can be ambiguous.
*   The criteria that Fisher’s linear discriminant follows :
*   To maximize the distance of the projected means and to minimize the projected within-class variance.

## Visual Layout
*   **Background:** A light blue gradient background that fades from a slightly darker blue on the left to a very light blue/white on the right.
*   **Decorative Elements:** On the far left, there is a graphic consisting of several thin, dark blue curved lines that sweep upward from the bottom corner.
*   **Header/Intro Bullet:** The first sentence is preceded by a dark grey horizontal bar with a pointed right end, acting as a prominent bullet point or section marker.
*   **Main Body Text:** The rest of the content is presented as a list of bullet points using small open square icons ($\square$).
*   **Typography:** The text uses a serif font (similar to Times New Roman). Key terms like **"decision boundary"**, **"separation"**, and the final criteria are **bolded** for emphasis.
*   **Alignment:** All text is left-aligned with standard indentation for the bulleted list.

## Diagram Type
This is a **text-only slide**. It uses bullet points to explain conceptual definitions and criteria rather than using charts, flowcharts, or mathematical notation.

## Diagram / Visual Explanation
No diagram is present on this page.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page. However, the text describes the conceptual components of the Fisher criterion formula:
*   **"Vector":** Refers to the projection vector $\mathbf{w}$.
*   **"Weights":** The components of the vector $\mathbf{w}$ that determine the orientation of the decision boundary.
*   **"Distance of the projected means":** Refers to the between-class scatter ($S_B$).
*   **"Projected within-class variance":** Refers to the within-class scatter ($S_W$).

## Table Description
No table is visible on this page.

## Concept Explanation
Fisher's Linear Discriminant (FLD) is a method used in supervised learning to find a linear combination of features that best separates two or more classes.

1.  **Supervised Learning:** It requires labeled training data to understand the distribution of different classes.
2.  **Dimensionality Reduction for Classification:** FLD works by projecting high-dimensional data onto a lower-dimensional space (typically a 1D line). The goal is to find the specific direction (vector) for this projection that makes the classes most distinguishable.
3.  **The Fisher Criterion:** Simply moving the means of the classes far apart isn't enough if the data points within each class are very spread out, as they will still overlap. FLD solves this by optimizing two things simultaneously:
    *   **Maximize Between-Class Variance:** Make the centers (means) of the projected classes as far apart as possible.
    *   **Minimize Within-Class Variance:** Make the spread of data points within each individual class as small as possible after projection.
4.  **Decision Boundary:** Once the optimal projection vector is found, a threshold is placed on the resulting line to separate the classes, creating a decision boundary.

## Exam / Viva Points
*   **Definition:** FLD is a supervised dimensionality reduction technique used for classification.
*   **Objective:** To find a projection vector $\mathbf{w}$ that maximizes the "Fisher Criterion."
*   **The Two Pillars of Fisher's Criterion:** 
    1. Maximize the distance between the means of the projected classes.
    2. Minimize the variance (scatter) within each projected class.
*   **Why not just maximize mean distance?** Because if within-class variance is high, classes will overlap significantly even if their means are far apart. FLD ensures classes are both far apart and tightly clustered.
*   **Output:** The result of FLD is a set of weights that define a linear decision boundary.

## Diagram Recreation Prompt
Create a professional educational slide titled "Fisher's Linear Discriminant (FLD) Criteria". 
- **Left side:** Use a clean bulleted list explaining that FLD is a supervised classifier that finds a projection vector to maximize class separation. Explicitly list the two criteria: 1) Maximize distance between projected means, and 2) Minimize projected within-class variance.
- **Right side:** Include a 2D scatter plot with two clusters of points (Red circles and Blue squares). Show a dashed line representing a projection axis. Project the points onto this axis. 
- **Visual Contrast:** Show two scenarios. Scenario A: Means are far apart but variance is high (overlapping projections). Scenario B (The FLD solution): Means are far apart and variance is low (distinct, non-overlapping projections). 
- **Style:** Use a modern flat design with a white background, dark grey text, and professional accent colors (Blue/Red).

## Diagram Data
*   **Title:** Fisher’s linear discriminant can be used as a supervised learning classifier.
*   **Content Points:**
    *   Uses labeled data to find weights for a decision boundary.
    *   Finds a vector to maximize separation of projected data.
    *   **Fisher's Criterion:**
        *   Maximize distance of projected means.
        *   Minimize projected within-class variance.
