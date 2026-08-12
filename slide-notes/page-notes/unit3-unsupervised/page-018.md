# Unit 1 Page 18 Image Understanding

## Page Overview
This slide serves as an introductory page for **Hierarchical Clustering** in the context of Machine Learning. Its purpose is to define the technique, highlight its primary advantage over K-Means (not needing a pre-specified number of clusters), and provide a visual representation of how data is organized into nested levels.

## Visible Text
*   **Title:** Hierarchical Clustering in Machine Learning
*   **Bullet Point 1:** Hierarchical clustering is an **unsupervised machine learning** technique used to group similar data points into clusters.
*   **Bullet Point 2:** Unlike algorithms such as K-Means, it does **not require the number of clusters to be specified in advance.**
*   **Diagram Header:** What is Hierarchical Clustering
*   **Diagram Subtext:** Hierarchical clustering is an unsupervised machine learning algorithm that groups data into a tree of nested clusters
*   **Diagram Labels:**
    *   Level 1
    *   Level 2
    *   Level 3
*   **Diagram Icons:** Various fruit icons (avocado, pineapple, strawberry, cherry, grapes, etc.) representing data points.

## Visual Layout
*   **Background:** A light pale-green gradient background with thin, dark, curved abstract lines on the left side.
*   **Header:** The main title is positioned at the top, aligned slightly to the left, in a bold, green sans-serif font.
*   **Left Margin Graphic:** A solid dark-red arrow shape points inward from the left edge towards the title.
*   **Content Blocks:** Two bullet points are listed below the title with square bullet icons.
*   **Central Image:** A white rectangular box contains the diagram. The diagram uses a nested circle (Euler diagram) approach to show hierarchy.
*   **Color Palette:** Green for titles, black for body text, and a variety of colors for the fruit icons within the diagram. The nested circles use thin orange and green outlines.

## Diagram Type
The main visual is a **Nested Cluster Diagram** (or a Venn-style Euler diagram). It is used to illustrate the concept of a hierarchy where smaller groups are contained within larger groups, representing the "tree of nested clusters" mentioned in the text.

## Diagram / Visual Explanation
The diagram illustrates the hierarchical nature of clustering using fruit icons as data points:
1.  **Level 1 (Smallest Circles):** These represent the most granular clusters. For example, two similar fruits (like a strawberry and a cherry) are grouped in a small green-outlined circle.
2.  **Level 2 (Medium Circles):** These represent a higher level of abstraction. Multiple Level 1 clusters are grouped together into a larger circle. In the diagram, there are three distinct Level 2 clusters.
3.  **Level 3 (Largest Circle):** This is the outermost orange-outlined circle that encompasses all data points and all sub-clusters. It represents the entire dataset viewed as a single cluster.
*   **Logic:** The diagram shows that as you move from Level 1 to Level 3, you are merging smaller, more specific clusters into larger, more general ones.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page.

## Table Description
No table is visible on this page.

## Concept Explanation
**Hierarchical Clustering** is a method of cluster analysis which seeks to build a hierarchy of clusters. 
*   **Unsupervised Learning:** Like other clustering methods, it works on unlabeled data to find inherent patterns or groupings based on similarity.
*   **No Pre-defined 'K':** In K-Means clustering, the user must decide the number of clusters ($k$) before running the algorithm. Hierarchical clustering avoids this by creating a tree-like structure (often visualized as a dendrogram) where the user can decide where to "cut" the tree to get the desired number of clusters *after* the algorithm has run.
*   **Nested Structure:** The algorithm views data as a hierarchy. You can start with every point as its own cluster and merge them (Agglomerative) or start with one giant cluster and split it (Divisive).

## Exam / Viva Points
*   **Definition:** It is an unsupervised learning algorithm that groups data into a nested tree structure.
*   **Key Advantage:** You do not need to specify the number of clusters ($k$) beforehand.
*   **Visualization:** While this slide uses nested circles, the most common way to visualize this hierarchy is through a **Dendrogram**.
*   **Similarity:** Data points within the same cluster at Level 1 are more similar to each other than points grouped only at Level 2 or Level 3.

## Diagram Recreation Prompt
Create a professional educational slide diagram titled "What is Hierarchical Clustering". The diagram should feature a nested circle layout on a clean white background. 
- **Level 3:** Draw one large outer circle with a thin orange border. Label it "Level 3" at the bottom right.
- **Level 2:** Inside the large circle, draw three medium-sized circles with thin green borders. Label the middle one "Level 2" at the bottom.
- **Level 1:** Inside each medium circle, place 2-3 small clusters. Each small cluster should be a tiny circle containing 2-3 distinct colorful icons (like different fruits or geometric shapes). Label one of these small clusters "Level 1".
- **Text:** Above the circles, include the subtext: "Hierarchical clustering is an unsupervised machine learning algorithm that groups data into a tree of nested clusters". Use a clean sans-serif font.

## Diagram Data
*   **Hierarchy Levels:**
    *   **Root (Level 3):** 1 Cluster (Contains all data).
    *   **Intermediate (Level 2):** 3 Clusters.
        *   Cluster A: Contains 2 sub-clusters.
        *   Cluster B: Contains 2 sub-clusters.
        *   Cluster C: Contains 3 sub-clusters.
    *   **Leaf (Level 1):** Individual small groupings of 2-3 data points (fruits).
*   **Data Points (Icons):**
    *   Top Cluster: Avocado, Pear, Pineapple.
    *   Bottom Left Cluster: Strawberry, Cherry, Raspberry.
    *   Bottom Right Cluster: Grapes, Apple, Orange, Plum.
