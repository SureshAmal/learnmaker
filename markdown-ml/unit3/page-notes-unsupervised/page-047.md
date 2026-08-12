# Unit 1 Page 47 Image Understanding

## Page Overview
The purpose of this slide is to introduce **Linear Discriminant Analysis (LDA)** as a supervised dimensionality reduction technique. It specifically contrasts LDA with Principal Component Analysis (PCA) to show that while PCA focuses on capturing maximum variance, LDA focuses on finding a projection that maximizes the separation between different classes.

## Visible Text
*   **Title:** Linear Discriminant Analysis
*   **Subtitle:** LDA projection onto directions that can best separate data of different classes.
*   **Left Plot Label:** Adversary situation for PCA
*   **Middle Plot Label:** Ideal situation for LDA
*   **Right Box Labels:** Before LDA, After LDA
*   **Footer:** 10 (Page number), 2021/3/4 (Date)

## Visual Layout
*   **Background:** The left two-thirds of the slide has a dark teal gradient background. The right third features a white rectangular box with a thin red border.
*   **Title Area:** The title is at the top left in a bold, white sans-serif font, underlined by a thin black horizontal line that spans the teal section.
*   **Content Blocks:**
    *   **Teal Section:** Contains two comparative scatter plots. The first shows a failure case for PCA, and the second shows the success of LDA on the same data.
    *   **White Box Section:** Contains two vertical scatter plots illustrating the state of data "Before LDA" and "After LDA".
*   **Colors:** 
    *   Data points: White 'x', purple 'o', black circles, and blue triangles.
    *   Projection vectors: Bright yellow arrows.
    *   Axes: White lines in the teal section, black lines in the white section.
*   **Hierarchy:** The title establishes the topic, the subtitle defines the goal, and the four diagrams provide visual proof of the concept.

## Diagram Type
This page uses **comparison scatter plots**. These diagrams are used to visualize how different algorithms (PCA vs. LDA) or different stages of a process (Before vs. After) affect the distribution and separability of data points in a 2D space.

## Diagram / Visual Explanation
### 1. Adversary situation for PCA (Left Plot)
*   **Data:** Two classes represented by white 'x' marks and purple 'o' marks.
*   **PCA Projection:** The long yellow arrow represents the first principal component (direction of maximum variance). 
*   **Problem:** If the data is projected onto this long arrow, the 'x' and 'o' classes will overlap significantly, losing the ability to distinguish between them. This is why it is called an "adversary situation."

### 2. Ideal situation for LDA (Middle Plot)
*   **Data:** Same as the PCA plot.
*   **LDA Projection:** The yellow arrow points in a different direction than the PCA arrow. 
*   **Solution:** This direction is chosen specifically to maximize the distance between the means of the two classes while minimizing the spread within each class. Projecting onto this line results in perfect class separation.

### 3. Before LDA vs. After LDA (Right Box)
*   **Before LDA:** Shows a 2D scatter plot of black circles and blue triangles. The classes are somewhat mixed and not easily separable by a simple vertical or horizontal line.
*   **After LDA:** A black diagonal line is drawn through the data. This represents the projection axis found by LDA. Along this axis, the black circles and blue triangles are clearly separated into two distinct groups.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page. The concepts are represented purely through geometric projections and vector arrows.

## Table Description
No table is visible on this page.

## Concept Explanation
**Linear Discriminant Analysis (LDA)** is a supervised learning method used for dimensionality reduction and classification. 
*   **Supervised Nature:** Unlike PCA, which is unsupervised and only looks at the features ($X$), LDA uses the class labels ($y$) to find the best projection.
*   **The Goal:** LDA seeks to project data from a high-dimensional space onto a lower-dimensional space (like a line) such that:
    1.  The distance between the means of the classes is maximized (**Between-class variance**).
    2.  The variation within each class is minimized (**Within-class variance**).
*   **Comparison with PCA:** PCA is great for data compression and visualization by keeping the most "information" (variance). However, as shown in the "Adversary situation," the direction of most variance is not always the direction that helps distinguish between classes. LDA fixes this by prioritizing class separability.

## Exam / Viva Points
*   **LDA vs. PCA:** Remember that PCA is unsupervised (ignores labels) while LDA is supervised (uses labels).
*   **Objective Function:** LDA maximizes the ratio of between-class scatter to within-class scatter ($S_B / S_W$).
*   **Failure of PCA:** PCA can fail in classification tasks if the direction of maximum variance leads to class overlap.
*   **Dimensionality:** For a $C$-class problem, LDA can project the data onto at most $C-1$ dimensions.
*   **Assumptions:** LDA assumes that the data for each class is normally distributed and that all classes share the same covariance matrix.

## Diagram Recreation Prompt
Create a comparison slide for Linear Discriminant Analysis. 
- **Left Side (Dark Blue Background):** Two scatter plots side-by-side. 
    - Plot 1: "PCA Adversary". Show two clusters of points (white 'x' and purple 'o') arranged diagonally. Draw a long yellow arrow along the diagonal (max variance) and a short perpendicular one. 
    - Plot 2: "LDA Ideal". Use the same points. Draw a yellow arrow in a direction that clearly separates the two clusters when projected. 
- **Right Side (White Box with Red Border):** Two vertical scatter plots. 
    - Plot 3: "Before LDA". Mix black dots and blue triangles in a 2D space. 
    - Plot 4: "After LDA". Show the same points with a single diagonal line passing through them, demonstrating how the points are separated along that specific axis. 
- Use clean sans-serif fonts and high-contrast colors for arrows.

## Diagram Data
*   **Plot 1 (PCA):** 
    - Class 1: White 'x' (bottom-left cluster).
    - Class 2: Purple 'o' (top-right cluster).
    - Vectors: Long yellow arrow (approx. 45 degrees), short yellow arrow (approx. 135 degrees).
*   **Plot 2 (LDA):** 
    - Same classes as Plot 1.
    - Vector: Yellow arrow pointing towards the top-left, perpendicular to the gap between classes.
*   **Plot 3 (Before):** 
    - Class 1: Black circles.
    - Class 2: Blue triangles.
    - Distribution: Overlapping in 2D space.
*   **Plot 4 (After):** 
    - Same classes as Plot 3.
    - Feature: A black projection line separating the two clusters.
