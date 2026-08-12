# Unit 1 Page 22 Image Understanding

## Page Overview
The purpose of this slide is to define and compare the four primary **Linkage Methods** used in Hierarchical Clustering. It serves as a reference guide for students to understand how the distance between two clusters is calculated, which determines the merging process in agglomerative clustering.

## Visible Text
*   **Linkage Methods** (Main Title)
*   **Linkage Method** (Left Column Header)
*   **Description** (Right Column Header)
*   **Single Linkage**: Minimum distance between two clusters
*   **Complete Linkage**: Maximum distance between two clusters
*   **Average Linkage**: Average distance between all pairs of points
*   **Ward's Linkage**: Minimizes the increase in within-cluster variance

## Visual Layout
*   **Title:** Large, bold green text at the top center-left.
*   **Header Bar:** A brown arrow-like shape points from the left margin toward the title.
*   **Content Structure:** A two-column list layout. The headers "Linkage Method" and "Description" are in red. The specific methods are in bold black text, and their descriptions are in standard black text.
*   **Background:** A light pale-green gradient background with abstract, thin brown curved lines on the far left side, resembling grass or wheat stalks.
*   **Alignment:** The text is left-aligned within two distinct vertical columns, creating a clean, tabular feel without using actual grid lines.

## Diagram Type
This is a **Comparison Table** (or a structured list). It is designed to map specific machine learning terms to their functional definitions for easy comparison.

## Diagram / Visual Explanation
While there is no graphical diagram (like a flowchart or plot), the visual hierarchy uses color and bolding to separate the **Term** (Linkage Method) from its **Definition** (Description). 
*   The **Red Headers** signal the start of the data categories.
*   The **Bold Black Terms** on the left act as the primary keys.
*   The **Standard Text** on the right provides the corresponding value/logic for each key.

## Math / Formula / Curve Notes
No explicit mathematical formulas or curves are visible. However, the text describes mathematical operations:
*   **Minimum:** $d(u, v) = \min(dist(u_i, v_j))$
*   **Maximum:** $d(u, v) = \max(dist(u_i, v_j))$
*   **Average:** The mean of all distances between points in cluster $u$ and cluster $v$.
*   **Variance:** Ward’s method uses the Sum of Squared Errors (SSE) logic.

## Table Description
| Linkage Method | Description |
| :--- | :--- |
| **Single Linkage** | Uses the distance between the two closest members of the clusters. |
| **Complete Linkage** | Uses the distance between the two most distant members of the clusters. |
| **Average Linkage** | Calculates the mean distance between all possible pairs of points between two clusters. |
| **Ward's Linkage** | Instead of direct distance, it calculates which merger will result in the smallest increase in total within-cluster variance. |

## Concept Explanation
In Hierarchical Clustering, the algorithm needs a rule to decide which two clusters to merge at each step. This rule is called a **Linkage Method**.
1.  **Single Linkage (Nearest Neighbor):** Tends to produce long, "chain-like" clusters. It is sensitive to outliers and noise.
2.  **Complete Linkage (Furthest Neighbor):** Tends to produce compact, spherical clusters of similar size. It is less sensitive to outliers than single linkage.
3.  **Average Linkage (UPGMA):** A compromise between single and complete linkage. It considers the overall structure of the clusters.
4.  **Ward's Linkage:** This is often the default in many software packages. It treats clustering as an analysis of variance problem, aiming to keep clusters tight and minimize the "loss of information" (variance) when merging.

## Exam / Viva Points
*   **What is the "Chaining Effect"?** It is a phenomenon in **Single Linkage** where clusters are joined together because of single points being close, even if the bulk of the clusters are far apart.
*   **Which method is most robust to noise?** **Complete Linkage** or **Ward's Linkage** are generally more robust than Single Linkage.
*   **Define Ward's Method:** It is a linkage method that minimizes the total within-cluster variance. At each step, the pair of clusters that leads to the minimum increase in total within-cluster sum of squares is merged.
*   **Difference between Single and Complete:** Single looks at the *minimum* distance (closest points), while Complete looks at the *maximum* distance (furthest points) between two clusters.

## Diagram Recreation Prompt
Create a clean, professional comparison table for "Linkage Methods" in machine learning. 
- **Title:** "Linkage Methods" in bold green.
- **Columns:** Two columns titled "Linkage Method" (Red) and "Description" (Red).
- **Rows:** 
  1. Single Linkage: Minimum distance between two clusters.
  2. Complete Linkage: Maximum distance between two clusters.
  3. Average Linkage: Average distance between all pairs of points.
  4. Ward's Linkage: Minimizes the increase in within-cluster variance.
- **Style:** Use a light, modern background (e.g., soft grey or white). Add small illustrative icons next to each method: two dots very close for Single, two dots at opposite ends of circles for Complete, a web of lines for Average, and a tight circle for Ward's.

## Diagram Data
*   **Title:** Linkage Methods
*   **Headers:** [Linkage Method, Description]
*   **Row 1:** [Single Linkage, Minimum distance between two clusters]
*   **Row 2:** [Complete Linkage, Maximum distance between two clusters]
*   **Row 3:** [Average Linkage, Average distance between all pairs of points]
*   **Row 4:** [Ward's Linkage, Minimizes the increase in within-cluster variance]
