# Unit 1 Page 82 Image Understanding

## Page Overview
The purpose of this slide is to explain the **Nearest Class Mean (NCM)** classification algorithm. It illustrates how a data point in a multi-dimensional feature space is assigned to a specific category based on its proximity to the average (centroid) of that category's known data points. The slide also introduces the concept of a "rejection" threshold for points that are too far from any known class mean.

## Visible Text
*   **Title:** Classification using nearest class mean
*   **Bullet Points:**
    *   Compute the Euclidean distance between feature vector X and the mean of each class.
    *   Choose closest class, if close enough (reject otherwise)
*   **Diagram Labels:**
    *   $x_2$ (Vertical axis label)
    *   $x_1$ (Horizontal axis label)
    *   Class 2 (Label for the upper-left cluster)
    *   Class 1 (Label for the lower-right cluster)
    *   o class mean (Label with an arrow pointing to the center of Class 2)
    *   x class mean (Label with an arrow pointing to the center of Class 1)

## Visual Layout
*   **Title:** Large, bold, centered at the top of the page.
*   **Content Split:** The page is divided into two main sections.
    *   **Left Side:** Contains a 2D scatter plot diagram showing two distinct clusters of data points.
    *   **Right Side:** Contains a bulleted list explaining the algorithmic steps.
*   **Colors:** The slide uses a white background with black text and lines. There is a decorative blue-grey vertical bar and curved lines on the far left edge.
*   **Visual Hierarchy:** The title establishes the topic, the diagram provides a visual mental model, and the text provides the formal procedural steps.

## Diagram Type
**Mathematical Graph / Scatter Plot:** The main visual is a 2D coordinate system ($x_1$ vs $x_2$) representing a feature space. It uses different symbols ('o' and 'x') to represent data points belonging to two different classes, effectively showing how data is distributed and where the class centers lie.

## Diagram / Visual Explanation
*   **Axes:** The horizontal axis represents feature $x_1$, and the vertical axis represents feature $x_2$.
*   **Clusters:**
    *   **Class 2 (Top-Left):** Represented by small circles ('o'). These points are enclosed within a larger boundary circle. A solid black dot in the center represents the **mean** of all 'o' points. An arrow points from the text "o class mean" to this central dot.
    *   **Class 1 (Bottom-Right):** Represented by 'x' marks. These points are also enclosed within a boundary circle. A solid black dot in the center represents the **mean** of all 'x' points. An arrow points from the text "x class mean" to this central dot.
*   **Classification Logic:** The diagram implies that for any new point $X$, the distance to the 'o' mean and the 'x' mean would be calculated. The point would then be assigned to the class with the shorter distance.

## Math / Formula / Curve Notes
*   **$x_1, x_2$:** These represent the two dimensions of the feature vector.
*   **Euclidean Distance:** While the formula is not explicitly written, the text refers to it. For a point $X = (x_1, x_2)$ and a class mean $\mu = (\mu_1, \mu_2)$, the distance is calculated as:
    $d(X, \mu) = \sqrt{(x_1 - \mu_1)^2 + (x_2 - \mu_2)^2}$
*   **Mean ($\mu$):** The central dot in each cluster represents the arithmetic mean of the feature vectors for all training samples in that class.

## Table Description
No table is visible on this page.

## Concept Explanation
**Nearest Class Mean (NCM) Classifier**
NCM is a simple generative classification model. 
1.  **Training:** During the training phase, the algorithm calculates the "centroid" or "mean" for every class in the dataset. If you have a set of images of cats and dogs, you would average all the feature vectors of cats to get the "Cat Mean" and all dog feature vectors to get the "Dog Mean."
2.  **Prediction:** When a new, unknown data point (feature vector $X$) arrives, the algorithm calculates its Euclidean distance to every class mean.
3.  **Decision Rule:** The point is assigned to the class whose mean is closest.
4.  **Rejection:** A sophisticated version of NCM (as mentioned in the slide) includes a threshold. If the distance to the nearest mean is greater than a predefined value, the system "rejects" the classification, meaning it labels the point as "unknown" or "outlier" rather than making a potentially wrong guess.

## Exam / Viva Points
*   **Definition:** NCM classifies a sample based on the minimum distance to class centroids.
*   **Distance Metric:** Euclidean distance is the standard metric used, though others (like Mahalanobis distance) can be applied.
*   **Computational Efficiency:** NCM is very efficient because, after training, you only need to store the mean vector for each class, not the entire training set (unlike k-Nearest Neighbors).
*   **Rejection Criterion:** Understand that "reject otherwise" means the model can handle outliers by not classifying points that are too far from any known cluster.
*   **Limitation:** NCM assumes that classes are roughly spherical and have similar variances. It may perform poorly if classes have elongated shapes or significantly different spreads.

## Diagram Recreation Prompt
Create a professional machine learning slide diagram on a white background. 
1. **Graph:** Draw a 2D coordinate system with arrows for axes, labeled $x_1$ (horizontal) and $x_2$ (vertical).
2. **Clusters:** 
   - Create a cluster of blue 'o' markers in the top-left quadrant. Draw a light blue dashed circle around them. Place a bold blue dot at the center. Label it "Class 2 Mean" with an arrow.
   - Create a cluster of red 'x' markers in the bottom-right quadrant. Draw a light red dashed circle around them. Place a bold red dot at the center. Label it "Class 1 Mean" with an arrow.
3. **Text Box:** On the right side, add a clean box with the heading "Algorithm Steps" and two bullet points: 
   - "1. Calculate Euclidean distance from input $X$ to each class mean $\mu_i$."
   - "2. Assign $X$ to the class with the minimum distance, provided it is within a threshold $T$ (else Reject)."
4. **Style:** Use high-contrast colors, clear sans-serif fonts, and ensure the layout is balanced and spacious.

## Diagram Data
*   **Title:** Classification using nearest class mean
*   **Axes:** $x_1$ (x-axis), $x_2$ (y-axis)
*   **Class 2 Data:** 
    *   Markers: 'o'
    *   Location: Top-left cluster
    *   Annotation: "Class 2", "o class mean" pointing to centroid.
*   **Class 1 Data:** 
    *   Markers: 'x'
    *   Location: Bottom-right cluster
    *   Annotation: "Class 1", "x class mean" pointing to centroid.
*   **Text Content:**
    *   Step 1: Compute Euclidean distance between feature vector X and the mean of each class.
    *   Step 2: Choose closest class, if close enough (reject otherwise).
