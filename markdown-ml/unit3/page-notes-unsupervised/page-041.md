# Unit 1 Page 41 Image Understanding

## Page Overview
The purpose of this slide is to introduce the concept of **non-linear discriminant functions**. It illustrates a scenario where two classes of data points in a two-dimensional feature space cannot be separated by a simple straight line. The slide emphasizes that in complex real-world scenarios, the decision boundary (discriminant function) often needs to be a non-linear curve to accurately classify data.

## Visible Text
*   **Title:** Discriminant Functions...
*   **Axis Labels:** $x_1$ (horizontal axis), $x_2$ (vertical axis).
*   **Legend:** 
    *   $\square$ Class 1
    *   $\bigcirc$ Class 2
*   **Mathematical Labels on Graph:**
    *   $g(\mathbf{x}) = 0$ (pointing to the curved boundary line)
    *   $g(\mathbf{x}) > 0$ (indicating the region to the left of the boundary)
    *   $g(\mathbf{x}) < 0$ (indicating the region to the right of the boundary)
*   **Caption below graph:** (c) (a) into $R$ categories, (b) dichotomizer ($R = 2$), and
*   **Callout Text (in red bubble):** "The design of discriminator for this case is not straightforward. The discriminant functions may result as nonlinear functions of $x_1$ and $x_2$"

## Visual Layout
*   **Title:** Positioned at the top left in a large, sans-serif font.
*   **Main Content:** A central 2D scatter plot showing data points and a decision boundary.
*   **Color Palette:** Primarily black and white for the graph, with a prominent red oval callout bubble on the right. A brown decorative bar is visible on the far left edge.
*   **Graph Elements:**
    *   A coordinate system with $x_1$ and $x_2$ axes.
    *   Data points represented by squares (Class 1) and circles (Class 2).
    *   A thick, curved black line representing the decision boundary.
    *   A legend at the bottom left of the plot area.
*   **Callout:** A red-outlined oval bubble with a pointer directed toward the non-linear decision boundary, containing explanatory text.
*   **Hierarchy:** The title sets the topic, the visual graph provides the primary example, and the callout provides the key takeaway message.

## Diagram Type
The main visual is a **mathematical graph / scatter plot with a decision boundary**. It is used to visualize how a classifier separates two distinct classes in a feature space. It specifically demonstrates a **non-linear classifier** because the boundary is a curve rather than a straight line.

## Diagram / Visual Explanation
*   **Axes ($x_1, x_2$):** These represent the two features or dimensions of the input data $\mathbf{x}$.
*   **Data Points:** The plot shows two sets of points. Squares represent samples from "Class 1," and circles represent samples from "Class 2."
*   **Decision Boundary ($g(\mathbf{x}) = 0$):** The solid curved line is the decision surface. It is the set of all points where the discriminant function $g(\mathbf{x})$ equals zero. This is the "border" where the classifier is most uncertain.
*   **Decision Regions:**
    *   **$g(\mathbf{x}) > 0$:** The region to the left of the curve. Any new data point falling in this area will be classified as Class 1.
    *   **$g(\mathbf{x}) < 0$:** The region to the right of the curve. Any new data point falling in this area will be classified as Class 2.
*   **The Red Callout:** It highlights that because the classes are interleaved in a complex way, a simple linear boundary (a straight line) would result in many misclassifications. Therefore, a more complex, non-linear function of the features $x_1$ and $x_2$ is required.

## Math / Formula / Curve Notes
*   **$g(\mathbf{x})$:** This denotes the **discriminant function**, where $\mathbf{x}$ is the input feature vector $[x_1, x_2]^T$.
*   **$g(\mathbf{x}) = 0$:** This equation defines the **decision boundary**.
*   **Non-linearity:** Unlike a linear discriminant function (which would look like $w_1x_1 + w_2x_2 + w_0 = 0$), this curve implies that $g(\mathbf{x})$ contains higher-order terms (e.g., $x_1^2, x_2^2, x_1x_2$) or other non-linear transformations.
*   **Classification Rule:**
    *   Decide Class 1 if $g(\mathbf{x}) > 0$
    *   Decide Class 2 if $g(\mathbf{x}) < 0$

## Table Description
No table is visible on this page.

## Concept Explanation
In machine learning, a **discriminant function** is a function that takes an input vector and outputs a value used to assign that input to a specific category. 

When we have two classes (a "dichotomizer"), we typically use a single function $g(\mathbf{x})$. The sign of the output determines the class. The boundary where the decision changes from one class to another is called the **decision boundary**, defined by $g(\mathbf{x}) = 0$.

While many simple problems can be solved with **linear discriminants** (straight lines or planes), real-world data is often not "linearly separable." In such cases, we must design **non-linear discriminant functions**. These functions create curved or complex decision surfaces that can better wrap around the actual distribution of the data points, leading to higher classification accuracy.

## Exam / Viva Points
*   **Definition of Decision Boundary:** It is the locus of points where $g(\mathbf{x}) = 0$.
*   **Classification Logic:** A point is assigned to a class based on whether the discriminant function evaluated at that point is greater than or less than zero.
*   **Linear vs. Non-linear:** Be prepared to explain that a linear boundary is a hyperplane, while a non-linear boundary is a curved surface.
*   **Why use non-linear functions?** They are necessary when data classes overlap or are distributed in a way that a straight line cannot separate them without high error.
*   **Feature Space:** The axes $x_1$ and $x_2$ represent the dimensions of the feature space.

## Diagram Recreation Prompt
Create a clean, professional machine learning slide diagram showing a non-linear decision boundary.
*   **Layout:** A 2D coordinate system with horizontal axis labeled "$x_1$" and vertical axis labeled "$x_2$".
*   **Data:** Plot approximately 10 blue square markers on the left side and 10 orange circle markers on the right side. Arrange them so they are not perfectly separable by a straight line.
*   **Boundary:** Draw a smooth, dark-grey S-shaped curve that passes between the two groups of points. Label this curve "$g(\mathbf{x}) = 0$".
*   **Annotations:** Label the region containing squares as "$g(\mathbf{x}) > 0$" and the region containing circles as "$g(\mathbf{x}) < 0$".
*   **Legend:** Include a legend box: "$\square$ Class 1", "$\bigcirc$ Class 2".
*   **Callout:** Add a modern, rounded callout box on the right with a pointer to the curve. Text inside: "Non-linear discriminant functions are required for complex data distributions where linear separation is not possible."
*   **Style:** Use a clean white background, distinct colors for classes, and clear, legible mathematical fonts.

## Diagram Data
*   **Title:** Discriminant Functions...
*   **Axes:** 
    *   X-axis: $x_1$ (Feature 1)
    *   Y-axis: $x_2$ (Feature 2)
*   **Classes:**
    *   Class 1: Square markers, located generally in the region where $x_1$ is low.
    *   Class 2: Circle markers, located generally in the region where $x_1$ is high.
*   **Decision Boundary:** A non-linear curve defined by $g(\mathbf{x}) = 0$.
*   **Decision Logic:**
    *   Region $g(\mathbf{x}) > 0 \rightarrow$ Class 1
    *   Region $g(\mathbf{x}) < 0 \rightarrow$ Class 2
*   **Key Message:** Discriminant functions for complex cases result in non-linear functions of the input features.
