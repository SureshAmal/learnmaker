# Unit 1 Page 84 Image Understanding

## Page Overview
This slide provides a detailed technical overview of **k-Means clustering**, presented as a quintessential example of an **unsupervised learning algorithm**. The page explains the algorithm through three lenses: a procedural flowchart showing the iterative loop, the mathematical objective function (minimization goal), and a visual representation of the resulting spatial partitioning (Voronoi cells).

## Visible Text
*   **Title:** Example of unsupervised learning algorithm
*   **Subtitle (Red):** k-Means clustering:
*   **Input Data:** $\{x_1, \dots, x_l\}$
*   **Classifier Box:** 
    *   Text: Classifier
    *   Formula: $y = q(x) = \arg \min_{i=1, \dots, k} \| x - m_i \|$
*   **Parameter Set:** $\theta = \{m_1, \dots, m_k\}$
*   **Learning Algorithm Box:**
    *   Text: Learning algorithm
    *   Formula: $m_i = \frac{1}{|I_i|} \sum_{j \in I_i} x_j, \quad I_i = \{j : q(x_j) = i\}$
*   **Output Data:** $\{y_1, \dots, y_l\}$
*   **Goal Section:**
    *   Text: Goal is to minimize
    *   Formula: $\sum_{i=1}^l \| x_i - m_{q(x_i)} \|^2$
*   **Plot Labels:** $m_1, m_2, m_3$

*Note: The original image contains rendering artifacts where some mathematical symbols (like the summation $\sum$ and minus $-$) appear as small icons (e.g., a cocktail glass for $\sum$) or extra dots. The transcriptions above reflect the intended mathematical meaning.*

## Visual Layout
*   **Title:** Large, centered at the top in black.
*   **Left Column (Flowchart):** A vertical pipeline showing the iterative process. 
    *   Input data enters from the top.
    *   Two rectangular boxes ("Classifier" and "Learning algorithm") are stacked vertically.
    *   Arrows indicate a feedback loop between the two boxes, representing the iterative nature of the algorithm.
    *   The final output $\{y_1, \dots, y_l\}$ exits from the bottom.
*   **Right Column (Math & Plot):**
    *   **Top:** The mathematical objective function is centered under the text "Goal is to minimize".
    *   **Bottom:** A 2D scatter plot showing three distinct clusters.
*   **Colors:** 
    *   Red is used for the subtitle.
    *   The scatter plot uses red (crosses), green (squares), and blue (circles) to distinguish clusters.
    *   Centroids are marked with black "+" symbols.
    *   Partition lines (Voronoi boundaries) are drawn in thin black lines.

## Diagram Type
This page features a **Hybrid Architecture and Scatter Plot diagram**. 
*   The left side is an **architecture diagram/flowchart** describing the algorithmic steps (Assignment and Update).
*   The right side is a **scatter plot** illustrating the spatial result of the algorithm, specifically showing cluster membership and centroids in a 2D feature space.

## Diagram / Visual Explanation
### The Algorithmic Loop (Left)
1.  **Input:** A set of unlabeled data points $\{x_1, \dots, x_l\}$ is provided.
2.  **Classifier (Assignment Step):** Each data point $x$ is assigned a label $y$ based on which centroid $m_i$ is closest to it (using Euclidean distance).
3.  **Learning Algorithm (Update Step):** The centroids $m_i$ are recalculated. A new centroid is the arithmetic mean of all data points currently assigned to that cluster ($I_i$).
4.  **Iteration:** The updated centroids $\theta$ are fed back into the Classifier, and the process repeats until the centroids no longer change significantly.
5.  **Output:** The final cluster assignments $\{y_1, \dots, y_l\}$.

### The Scatter Plot (Right)
*   **Data Points:** Represented by three different shapes/colors: red crosses (top left), blue circles (top right), and green squares (bottom).
*   **Centroids ($m_1, m_2, m_3$):** Indicated by black "+" signs at the center of each cluster mass.
*   **Decision Boundaries:** The lines dividing the space are Voronoi boundaries. Any point falling within a specific region is mathematically closer to that region's centroid than any other.

## Math / Formula / Curve Notes
*   **Objective Function:** $\sum_{i=1}^l \| x_i - m_{q(x_i)} \|^2$
    *   This is the **Within-Cluster Sum of Squares (WCSS)**.
    *   $x_i$: A specific data point.
    *   $m_{q(x_i)}$: The centroid of the cluster to which $x_i$ is assigned.
    *   $\| \cdot \|^2$: The squared Euclidean distance.
    *   The goal is to minimize the total distance between points and their respective cluster centers.
*   **Assignment Function ($q(x)$):** Uses $\arg \min$ to find the index $i$ of the centroid that has the minimum distance to point $x$.
*   **Centroid Update ($m_i$):** $m_i = \frac{1}{|I_i|} \sum x_j$. This is the standard formula for the mean (average) of a set of vectors.

## Table Description
No table is visible on this page.

## Concept Explanation
**k-Means Clustering** is an unsupervised learning algorithm used to group unlabeled data into $k$ distinct clusters. 

1.  **Unsupervised Nature:** Unlike supervised learning, there are no target labels provided in the input. The algorithm must discover patterns (clusters) based solely on the inherent structure of the data.
2.  **Iterative Optimization:** It works by alternating between two steps:
    *   **Expectation (Assignment):** Assigning every point to its nearest center.
    *   **Maximization (Update):** Moving the center to the average position of its assigned points.
3.  **Convergence:** The algorithm is guaranteed to converge to a local minimum of the objective function (WCSS), though not necessarily the global minimum.
4.  **Voronoi Partitioning:** The result is a partitioning of the input space into regions where every point in a region is closest to that region's centroid.

## Exam / Viva Points
*   **What does k-Means minimize?** It minimizes the sum of squared Euclidean distances between data points and their assigned cluster centroids (WCSS).
*   **Is k-Means a supervised or unsupervised algorithm?** It is unsupervised because it operates on unlabeled data.
*   **Explain the two main steps of the k-Means loop.** 
    1. The **Assignment step** (Classifier) where points are mapped to the nearest centroid.
    2. The **Update step** (Learning algorithm) where centroids are recalculated as the mean of the assigned points.
*   **What is a centroid?** The mathematical center (mean) of all data points belonging to a cluster.
*   **What determines the cluster boundaries in k-Means?** The boundaries are determined by the midpoints between centroids, creating a Voronoi diagram.

## Diagram Recreation Prompt
Create a professional machine learning slide titled "k-Means Clustering Overview". 
- **Left Side:** A vertical flowchart. Top: Input $\{x_1, \dots, x_l\}$. Middle: Two boxes labeled "Assignment Step (Classifier)" and "Update Step (Learning Algorithm)". Draw a loop arrow from the Update box back to the Assignment box labeled "Updated Centroids $\theta$". Bottom: Output $\{y_1, \dots, y_l\}$. Use clean blue and grey boxes.
- **Right Top:** Display the objective function clearly: "Minimize $J = \sum_{i=1}^n \| x_i - \mu_{c_i} \|^2$".
- **Right Bottom:** A 2D scatter plot. Show three clusters of points: Red crosses, Blue circles, and Green squares. Mark the center of each cluster with a bold black '+' and labels $m_1, m_2, m_3$. Draw thin grey lines representing the Voronoi boundaries between the clusters.
- **Style:** Modern, high-contrast, academic presentation style. Ensure all mathematical symbols (summation, subscripts) are rendered correctly.

## Diagram Data
**Flowchart Structure:**
- Node A: Input $\{x_1, \dots, x_l\}$
- Node B: Box "Classifier" [$y = q(x) = \arg \min \|x - m_i\|$]
- Node C: Box "Learning Algorithm" [$m_i = \text{mean}(x \in \text{Cluster } i)$]
- Node D: Output $\{y_1, \dots, y_l\}$
- Edge: A -> B
- Edge: B -> C
- Edge: C -> B (Label: $\theta = \{m_1, \dots, m_k\}$)
- Edge: C -> D

**Scatter Plot Data (Conceptual):**
- Cluster 1 (Red Crosses): Centered at (-2, 2)
- Cluster 2 (Blue Circles): Centered at (2, 2)
- Cluster 3 (Green Squares): Centered at (0, -2)
- Boundaries: Y-axis (between red and blue), and two diagonal lines meeting at the origin (separating green from the others).
