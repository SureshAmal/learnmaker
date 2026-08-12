# Unit 1 Page 136 Image Understanding

## Page Overview
The purpose of this slide is to introduce the concept of **Non-linear Discriminant Functions** in the context of pattern classification. It illustrates a scenario where two classes of data points in a two-dimensional feature space cannot be separated by a simple straight line (linear boundary). Instead, a complex, curved decision boundary is required, which is defined by a non-linear mathematical function $g(x)$.

## Visible Text
*   **Title:** Discriminant Functions...
*   **Axis Labels:** $x_1$ (horizontal axis), $x_2$ (vertical axis).
*   **Legend:**
    *   $\square$ Class 1
    *   $\bigcirc$ Class 2
*   **Mathematical Labels on Plot:**
    *   $g(x) = 0$ (pointing to the curved decision boundary)
    *   $g(x) > 0$ (labeling the region containing Class 1 squares)
    *   $g(x) < 0$ (labeling the region containing Class 2 circles)
*   **Callout Text (in red bubble):** "The design of discriminator for this case is not straightforward. The discriminant functions may result as nonlinear functions of $x_1$ and $x_2$"
*   **Bottom Caption:** (c) (a) into $R$ categories, (b) dichotomizer ($R = 2$), and... [text is cut off]

## Visual Layout
*   **Title:** Positioned at the top left in a large, sans-serif font.
*   **Main Content:** A central scatter plot showing data points and a decision boundary.
*   **Scatter Plot:**
    *   Uses a standard Cartesian coordinate system with $x_1$ and $x_2$ axes.
    *   Data points are represented by two distinct shapes: squares for Class 1 and circles for Class 2.
    *   A thick, curved black line acts as the decision boundary.
    *   Arrows point from labels ($g(x)=0$, etc.) to their respective parts of the graph.
*   **Callout Bubble:** A red-outlined oval bubble on the right side contains explanatory text, with a pointer directed toward the non-linear decision boundary.
*   **Legend:** Located at the bottom left of the plot area, clearly defining the symbols for Class 1 and Class 2.
*   **Background:** The slide has a white background with a subtle light-blue gradient at the bottom and a dark gray decorative element on the far left edge.

## Diagram Type
The main visual is a **Scatter Plot with a Decision Boundary**. It is used to visualize a classification problem in a 2D feature space. It specifically demonstrates a **non-linear dichotomizer** (a two-class classifier with a non-linear boundary).

## Diagram / Visual Explanation
*   **Feature Space:** The $x_1$ and $x_2$ axes represent two different features or measurements used to describe the data points.
*   **Data Distribution:**
    *   **Class 1 (Squares):** These points are clustered primarily in the upper and left portions of the plot.
    *   **Class 2 (Circles):** These points are clustered primarily in the lower and right portions.
*   **Decision Boundary ($g(x) = 0$):** The curved line represents the set of points where the discriminant function $g(x)$ equals zero. This is the "threshold" where the classifier is uncertain.
*   **Decision Regions:**
    *   **Region $g(x) > 0$:** The area to the left/top of the curve. Any new data point falling in this region would be classified as Class 1.
    *   **Region $g(x) < 0$:** The area to the right/bottom of the curve. Any new data point falling here would be classified as Class 2.
*   **Non-linearity:** The curve is S-shaped and complex, indicating that a simple linear equation (like $w_1x_1 + w_2x_2 + w_0 = 0$) cannot accurately separate these two classes. A higher-order polynomial or other non-linear function is needed.

## Math / Formula / Curve Notes
*   **$g(x)$:** Represents the **discriminant function**. It takes a feature vector $x = [x_1, x_2]^T$ as input and outputs a scalar value.
*   **$g(x) = 0$:** This equation defines the **decision surface**. In 2D, it is a line or curve; in higher dimensions, it is a hyperplane or manifold.
*   **Classification Rule:**
    *   Decide Class 1 if $g(x) > 0$
    *   Decide Class 2 if $g(x) < 0$
*   The curve shown is non-linear, implying that $g(x)$ contains terms like $x_1^2$, $x_2^2$, $x_1x_2$, or other non-linear transformations of the input features.

## Table Description
No table is visible on this page.

## Concept Explanation
In machine learning, a **discriminant function** is a mathematical tool used to perform classification. For a two-class problem (a **dichotomizer**), we define a single function $g(x)$. The sign of the output determines the predicted class.

While many introductory models use **linear discriminants** (which result in straight-line boundaries), real-world data is often not "linearly separable." As shown in the slide, the two groups of points are intertwined in a way that a straight line would misclassify many points. To achieve better accuracy, we must design **non-linear discriminant functions**. These functions create more flexible decision boundaries that can "bend" to fit the complex distribution of the data classes.

## Exam / Viva Points
*   **Definition of Discriminant Function:** A function $g(x)$ used to partition the feature space into different decision regions.
*   **Decision Boundary:** The boundary is defined by the set of points where $g(x) = 0$.
*   **Classification Logic:** For two classes, $g(x) > 0 \implies$ Class 1, and $g(x) < 0 \implies$ Class 2.
*   **Linear vs. Non-linear:** A linear discriminant produces a straight line/hyperplane boundary. A non-linear discriminant produces curved/complex boundaries.
*   **Why use non-linear functions?** They are necessary when classes are not linearly separable, allowing for more complex and accurate classification models.
*   **Dichotomizer:** A specific term for a classifier that deals with exactly two categories ($R=2$).

## Diagram Recreation Prompt
Create a high-quality educational diagram for a machine learning slide titled "Non-linear Discriminant Functions".
*   **Layout:** A 2D scatter plot on the left, with a large explanatory callout bubble on the right.
*   **Axes:** Draw a horizontal axis labeled "$x_1$" and a vertical axis labeled "$x_2$".
*   **Data Points:** Plot approximately 10 blue squares (Class 1) and 10 orange circles (Class 2). Arrange them so they are separated by a distinct S-shaped curve.
*   **Decision Boundary:** Draw a smooth, bold S-shaped curve snaking between the two groups of points. Label this curve "$g(x) = 0$".
*   **Regions:** Label the area with squares as "$g(x) > 0$" and the area with circles as "$g(x) < 0$".
*   **Legend:** Include a legend at the bottom left: "$\square$ Class 1", "$\bigcirc$ Class 2".
*   **Callout:** Add a red-bordered speech bubble pointing to the curve. Inside, write: "The design of the discriminator for this case is not straightforward. The discriminant functions result in nonlinear functions of $x_1$ and $x_2$."
*   **Style:** Use a clean, modern, high-contrast aesthetic suitable for a presentation.

## Diagram Data
*   **Title:** Discriminant Functions...
*   **Axes:** $x_1$ (x-axis), $x_2$ (y-axis).
*   **Class 1 (Squares):** Coordinates roughly at $(-2, 2), (-1, 3), (0, 4), (-3, 1), (-2, 0), (-1, -1)$.
*   **Class 2 (Circles):** Coordinates roughly at $(1, 2), (2, 1), (3, 0), (1, -1), (2, -2), (0, -3)$.
*   **Boundary:** A non-linear, curved line $g(x)=0$ passing between the two clusters.
*   **Labels:** $g(x) > 0$ in the top-left region; $g(x) < 0$ in the bottom-right region.
*   **Callout Text:** "The design of discriminator for this case is not straightforward. The discriminant functions may result as nonlinear functions of $x_1$ and $x_2$"
