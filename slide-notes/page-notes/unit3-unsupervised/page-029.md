# Unit 1 Page 29 Image Understanding

## Page Overview
The purpose of this slide is to illustrate a **Dendrogram**, which is a tree-like diagram used to visualize the results of **Hierarchical Clustering**. Specifically, it demonstrates a clustering process using **Complete Linkage** as the grouping criterion and **Euclidean Distance** as the metric for measuring the space between data points. The dendrogram shows how 20 individual observations are progressively merged into larger clusters based on their similarity.

## Visible Text
*   **Title:** Dendrogram
*   **Subtitle:** Complete Linkage, Euclidean Distance
*   **Y-axis Label:** Similarity
*   **Y-axis Ticks:** 0.00, 33.33, 66.67, 100.00
*   **X-axis Label:** Observations
*   **X-axis Ticks (Leaf Nodes):** 1, 3, 6, 9, 10, 11, 15, 4, 12, 19, 2, 14, 17, 20, 18, 5, 8, 7, 13, 16

## Visual Layout
*   **Main Content:** A large central plot area containing the dendrogram.
*   **Background:** The plot has a light grey grid for easier reading of similarity values.
*   **Color Coding:** 
    *   **Blue:** Represents a major cluster on the left (observations 1 through 15 in the sequence).
    *   **Green:** Represents a smaller cluster (observations 4, 12, 19).
    *   **Red:** Represents a large cluster on the right (observations 2 through 8 in the sequence).
    *   **Purple:** Represents a small cluster on the far right (observations 7, 13, 16).
    *   **Grey:** Used for the top-level branches that connect these four main colored clusters.
*   **Hierarchy:** The diagram starts with individual observations at the bottom (Similarity = 100) and merges them as it moves upward toward Similarity = 0.
*   **Styling:** The slide has a minimalist design with a thin black border around the chart and a decorative brown/tan vertical bar on the far left edge.

## Diagram Type
This is a **Dendrogram**, a specific type of tree diagram used in hierarchical clustering. It is chosen because it effectively displays the nested relationship between clusters and the specific similarity levels at which different groups of data points are joined.

## Diagram / Visual Explanation
*   **X-axis (Observations):** The horizontal axis lists the individual data points (1 to 20). Note that they are not in numerical order, but rather ordered to prevent branches from crossing.
*   **Y-axis (Similarity):** The vertical axis measures similarity. 
    *   **100.00:** Represents maximum similarity (the starting point where each observation is its own cluster).
    *   **0.00:** Represents minimum similarity (where all data points are eventually merged into one single root cluster).
*   **Leaf Nodes:** The individual numbers at the bottom are the "leaves" of the tree.
*   **Branches and Merges:** 
    *   Vertical lines represent the clusters.
    *   Horizontal lines represent the "merging" event. The height of a horizontal line indicates the similarity level between the two clusters being joined.
    *   For example, observations **17 and 20** are merged at a very high similarity (near 95), indicating they are very similar.
    *   The **Blue** and **Green** clusters are merged at a similarity level of approximately 40.
    *   The final merge between the left half (Blue/Green) and the right half (Red/Purple) occurs at **0.00 similarity**, indicating these two large groups are highly distinct from each other.

## Math / Formula / Curve Notes
*   **Euclidean Distance:** The distance between two points $p$ and $q$ is calculated as $d(p, q) = \sqrt{\sum_{i=1}^{n} (p_i - q_i)^2}$. This is the underlying metric used to determine how "far apart" observations are before converting that to a similarity score.
*   **Complete Linkage:** Also known as "Maximum Linkage." The distance between two clusters $C_1$ and $C_2$ is defined as the maximum distance between any single element in $C_1$ and any single element in $C_2$: 
    $$D(C_1, C_2) = \max \{d(a, b) : a \in C_1, b \in C_2\}$$
    This method tends to produce compact, tightly bound clusters.
*   **Similarity Scale:** The Y-axis uses a percentage-based similarity scale where $Similarity = 100 \times (1 - \frac{d}{d_{max}})$, where $d$ is the distance.

## Table Description
No table is visible on this page.

## Concept Explanation
**Hierarchical Clustering** is an unsupervised machine learning algorithm that groups similar objects into clusters. Unlike K-Means, it doesn't require pre-specifying the number of clusters.
1.  **Agglomerative Approach:** This is a "bottom-up" approach. Each observation starts in its own cluster. At each step, the two most similar clusters are merged.
2.  **Linkage Criteria:** This defines how "similarity" is calculated between groups. **Complete Linkage** looks at the furthest members of two clusters to decide if they should merge. This prevents the "chaining effect" seen in single linkage and results in more spherical clusters.
3.  **Interpreting the Dendrogram:** To choose the number of clusters ($k$), a user can "cut" the dendrogram horizontally. 
    *   Cutting at similarity **66.67** would result in many small clusters.
    *   Cutting at similarity **50** would result in 4 main clusters (the colored groups).
    *   Cutting at similarity **20** would result in 2 large clusters.

## Exam / Viva Points
*   **Identify the Linkage:** The slide uses **Complete Linkage**, which uses the maximum distance between members of two clusters.
*   **Identify the Metric:** **Euclidean Distance** is used to measure the straight-line distance between points in multi-dimensional space.
*   **Reading the Y-axis:** Understand that on this specific chart, a higher value (100) means more similar, while a lower value (0) means less similar.
*   **Determining Cluster Count:** Be prepared to answer how many clusters exist at a specific similarity threshold (e.g., at similarity 60, there are 6 distinct vertical lines crossed).
*   **Observation Similarity:** Which observations are most similar? (Those joined by the lowest horizontal bars, like 17 & 20 or 13 & 16).

## Diagram Recreation Prompt
Create a professional dendrogram plot for a machine learning presentation. 
- **Title:** "Dendrogram" in bold, Subtitle: "Complete Linkage, Euclidean Distance".
- **Layout:** A white rectangular plot area with a light grey grid.
- **Y-axis:** Labeled "Similarity" on the left, ranging from 0.00 at the top to 100.00 at the bottom. Include major ticks at 0, 33.33, 66.67, and 100.
- **X-axis:** Labeled "Observations" at the bottom. Leaf nodes should be numbered 1 to 20 in the specific order: 1, 3, 6, 9, 10, 11, 15, 4, 12, 19, 2, 14, 17, 20, 18, 5, 8, 7, 13, 16.
- **Tree Structure:** Draw a hierarchical tree. 
    - Color the first subtree (leaves 1, 3, 6, 9, 10, 11, 15) in **Blue**.
    - Color the second subtree (leaves 4, 12, 19) in **Green**.
    - Color the third subtree (leaves 2, 14, 17, 20, 18, 5, 8) in **Red**.
    - Color the fourth subtree (leaves 7, 13, 16) in **Purple**.
    - Use **Grey** for the top-level horizontal and vertical lines that connect these four colored groups.
- **Final Merge:** The very top horizontal line connecting the left and right halves should align exactly with the 0.00 similarity mark.

## Diagram Data
*   **Leaves (X-axis order):** [1, 3, 6, 9, 10, 11, 15, 4, 12, 19, 2, 14, 17, 20, 18, 5, 8, 7, 13, 16]
*   **Similarity Thresholds for Merges (Approximate):**
    *   (17, 20) and (13, 16) merge at ~95 similarity.
    *   (6, 9) and (12, 19) and (5, 8) merge at ~90 similarity.
    *   (1, 3) and (2, 14) merge at ~85 similarity.
    *   Blue cluster internal merges complete at ~60 similarity.
    *   Red cluster internal merges complete at ~65 similarity.
    *   Blue and Green merge at ~40 similarity.
    *   Red and Purple merge at ~40 similarity.
    *   Final merge (Left half + Right half) at 0.00 similarity.
