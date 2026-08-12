# Unit 1 Page 18 Image Understanding

## Page Overview
The purpose of this slide is to provide a summary and categorization of various **Unsupervised Machine Learning algorithms**. It serves as a quick reference guide, mapping specific algorithms to their broader machine learning techniques and their primary practical applications.

## Visible Text
*   **Headers (in Red):** Algorithm, Technique, Main Use
*   **Row 1:** K-Means | Clustering | Group similar data
*   **Row 2:** Hierarchical Clustering | Clustering | Build cluster hierarchy
*   **Row 3:** DBSCAN | Clustering | Density-based clustering & outlier detection
*   **Row 4:** PCA | Dimensionality Reduction | Reduce features
*   **Row 5:** Apriori | Association | Find item relationships
*   **Row 6:** FP-Growth | Association | Efficient rule mining
*   **Row 7:** GMM | Clustering | Probabilistic clustering
*   **Row 8:** Autoencoder | Representation Learning | Feature extraction
*   **Row 9:** SOM | Visualization | Pattern discovery

## Visual Layout
*   **Title/Header:** The table headers are centered at the top of their respective columns in a bold red font.
*   **Table Structure:** A standard grid table with three columns and ten rows (including the header).
*   **Color Coding:** 
    *   The **Technique** column uses color-coding to group related algorithms:
        *   **Blue:** Clustering (K-Means, Hierarchical, DBSCAN, GMM)
        *   **Dark Green:** Dimensionality Reduction (PCA)
        *   **Pink/Magenta:** Association (Apriori, FP-Growth)
        *   **Light Green:** Representation Learning and Visualization (Autoencoder, SOM)
*   **Background:** The left side of the slide features a white background with dark, sweeping curved lines. The right side of the table has a light blue gradient background.
*   **Indicator:** A thick dark grey/black arrow points from the left margin toward the first row (K-Means).
*   **Alignment:** Text in the "Algorithm" and "Technique" columns is centered, while text in the "Main Use" column is left-aligned.

## Diagram Type
This is a **Table**. It is used to organize and compare categorical data across three distinct attributes: the name of the algorithm, its technical classification, and its functional purpose.

## Diagram / Visual Explanation
The table acts as a lookup matrix:
1.  **Algorithm Column:** Lists the specific name of the machine learning model.
2.  **Technique Column:** Categorizes the algorithm into a broader field of study within unsupervised learning. The color-coding here helps the viewer quickly identify that most of the listed algorithms belong to the "Clustering" family.
3.  **Main Use Column:** Provides a concise, one-sentence explanation of what a data scientist achieves by using that specific algorithm.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page.

## Table Description
The table consists of 3 columns and 9 data rows:
*   **Column 1 (Algorithm):** Identifies the specific tool (e.g., PCA, DBSCAN).
*   **Column 2 (Technique):** Identifies the category. Clustering is the most prominent category listed.
*   **Column 3 (Main Use):** Explains the output or goal, such as "Reduce features" for PCA or "Efficient rule mining" for FP-Growth.
*   **Conclusion:** The table highlights that unsupervised learning is diverse, covering tasks from grouping data to simplifying it and finding hidden associations.

## Concept Explanation
This slide covers **Unsupervised Learning**, where the model works with unlabeled data to find hidden patterns.
*   **Clustering:** The process of partitioning a dataset into groups (clusters) so that data points in the same group are more similar to each other than to those in other groups.
    *   *K-Means:* Uses distance to centroids.
    *   *DBSCAN:* Uses density to find clusters of arbitrary shapes and identify noise.
    *   *GMM (Gaussian Mixture Model):* A probabilistic approach assuming data comes from a mixture of Gaussian distributions.
*   **Dimensionality Reduction (PCA):** Reducing the number of random variables under consideration by obtaining a set of principal variables. It simplifies data without losing significant information.
*   **Association Rule Learning:** Discovering interesting relations between variables in large databases (e.g., "People who buy bread also buy butter").
*   **Representation Learning (Autoencoders):** Using neural networks to learn efficient data codings (features) in an unsupervised manner.
*   **Visualization (SOM - Self-Organizing Maps):** A type of artificial neural network that is trained using competitive learning to produce a low-dimensional (typically two-dimensional), discretized representation of the input space.

## Exam / Viva Points
*   **Name three clustering algorithms:** K-Means, Hierarchical Clustering, and DBSCAN.
*   **What is the main use of PCA?** To reduce the number of features (dimensionality reduction) in a dataset.
*   **Which algorithms are used for Association Rule Mining?** Apriori and FP-Growth.
*   **What is the difference between K-Means and GMM?** K-Means is a hard-clustering, distance-based method, while GMM is a soft-clustering, probabilistic method.
*   **What is an Autoencoder used for?** Feature extraction and representation learning.
*   **How does DBSCAN differ from K-Means?** DBSCAN is density-based and can detect outliers/noise, whereas K-Means is distance-based and assigns every point to a cluster.

## Diagram Recreation Prompt
Create a clean, professional summary table for Unsupervised Learning algorithms. 
- **Columns:** "Algorithm", "Technique", and "Main Use". 
- **Header Style:** Bold red text on a white background. 
- **Row Content:** 
  1. K-Means, Hierarchical Clustering, DBSCAN, GMM -> Technique: "Clustering" (Blue text).
  2. PCA -> Technique: "Dimensionality Reduction" (Dark Green text).
  3. Apriori, FP-Growth -> Technique: "Association" (Magenta text).
  4. Autoencoder -> Technique: "Representation Learning" (Light Green text).
  5. SOM -> Technique: "Visualization" (Light Green text).
- **Layout:** Use a light grey border for the table. Ensure the "Main Use" column has enough width for short descriptions. Use a modern sans-serif font like Roboto or Open Sans.

## Diagram Data
| Algorithm | Technique | Main Use |
| :--- | :--- | :--- |
| K-Means | Clustering | Group similar data |
| Hierarchical Clustering | Clustering | Build cluster hierarchy |
| DBSCAN | Clustering | Density-based clustering & outlier detection |
| PCA | Dimensionality Reduction | Reduce features |
| Apriori | Association | Find item relationships |
| FP-Growth | Association | Efficient rule mining |
| GMM | Clustering | Probabilistic clustering |
| Autoencoder | Representation Learning | Feature extraction |
| SOM | Visualization | Pattern discovery |
