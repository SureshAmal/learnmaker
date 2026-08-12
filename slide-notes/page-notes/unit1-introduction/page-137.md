# Unit 1 Page 137 Image Understanding

## Page Overview
The purpose of this slide is to introduce the concept of **Discriminant Functions** in the context of classification. It explains how a classifier makes a decision by choosing the class that maximizes a specific function, $g_i(\mathbf{x})$. The slide provides mathematical definitions for these functions based on risk, posterior probability, and joint probability, and visually demonstrates how these functions partition a feature space into distinct decision regions.

## Visible Text
*   **Title:** Discriminant Functions
*   **Decision Rule:** $\text{choose } C_i \text{ if } g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})$
*   **Discriminant Function Definitions:**
    $g_i(\mathbf{x}) = \begin{cases} - R(\alpha_i \mid \mathbf{x}) \\ P(C_i \mid \mathbf{x}) \\ p(\mathbf{x} \mid C_i)P(C_i) \end{cases}$
*   **General Notation:** $g_i(\mathbf{x}), i = 1, \dots, K$
*   **Decision Regions Text:** $K \text{ decision regions } \mathcal{R}_1, \dots, \mathcal{R}_K$
*   **Region Definition Formula:** $\mathcal{R}_i = \{\mathbf{x} \mid g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})\}$
*   **Graph Labels:**
    *   $x_1$ (horizontal axis)
    *   $x_2$ (vertical axis)
    *   $C_1, C_2, C_3$ (class labels)
    *   "reject" (central region label)

## Visual Layout
*   **Title:** Located at the top left in a large, orange, serif font.
*   **Left Column:** Contains the core mathematical formulas and definitions. The text is black and uses standard LaTeX-style formatting for math.
*   **Right Column:** Features a 2D coordinate plot illustrating decision regions.
*   **Diagram Details:** 
    *   The plot has two axes, $x_1$ and $x_2$, representing a two-dimensional feature space.
    *   Three distinct clusters of data points are shown: yellow squares (top-left), purple triangles (bottom-left), and green circles (right).
    *   Colored boundary lines (yellow, purple, green) separate these clusters.
    *   Black arrows point from the text "$g_i(\mathbf{x}), i = 1, \dots, K$" toward the decision boundaries in the plot, indicating that the boundaries are determined by these functions.
*   **Color Palette:** Uses a clean white background with a light blue vertical bar on the right edge and a dark grey abstract graphic on the far left.

## Diagram Type
The main visual is a **Decision Region Diagram** (or a partitioned feature space plot). It is used to show how a classifier divides a continuous feature space into discrete regions, each assigned to a specific class, based on the values of discriminant functions.

## Diagram / Visual Explanation
*   **Axes:** The horizontal axis $x_1$ and vertical axis $x_2$ represent two input features used for classification.
*   **Data Clusters:**
    *   **$C_1$ (Yellow Squares):** Located in the upper-left quadrant.
    *   **$C_2$ (Purple Triangles):** Located in the lower-left quadrant.
    *   **$C_3$ (Green Circles):** Located on the right side of the plot.
*   **Decision Boundaries:** The curved lines represent the points where the discriminant functions for two adjacent classes are equal (e.g., $g_1(\mathbf{x}) = g_3(\mathbf{x})$).
*   **Decision Regions ($\mathcal{R}_i$):** The areas enclosed by the boundaries. For any point $\mathbf{x}$ inside region $\mathcal{R}_1$, the function $g_1(\mathbf{x})$ is greater than all other $g_k(\mathbf{x})$.
*   **Reject Region:** The central area where no data points are present is labeled "reject". This typically represents a region where the classifier's confidence is too low (e.g., the maximum posterior probability is below a threshold), and it chooses not to classify the input to avoid high risk.

## Math / Formula / Curve Notes
*   **$\text{choose } C_i \text{ if } g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})$**: This is the fundamental decision rule. The classifier evaluates all $K$ discriminant functions for a given input $\mathbf{x}$ and assigns it to the class $i$ that yields the maximum value.
*   **$g_i(\mathbf{x}) = - R(\alpha_i \mid \mathbf{x})$**: Here, the discriminant function is the negative of the conditional risk. Minimizing risk is equivalent to maximizing negative risk.
*   **$g_i(\mathbf{x}) = P(C_i \mid \mathbf{x})$**: The discriminant function is the posterior probability. This corresponds to the Maximum A Posteriori (MAP) decision rule, which minimizes the probability of error.
*   **$g_i(\mathbf{x}) = p(\mathbf{x} \mid C_i)P(C_i)$**: This is the product of the class-conditional density and the prior probability. Since the denominator in Bayes' rule ($p(\mathbf{x})$) is the same for all classes, maximizing this product is equivalent to maximizing the posterior probability.
*   **$\mathcal{R}_i = \{\mathbf{x} \mid g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})\}$**: This formally defines the decision region for class $i$ as the set of all points in the feature space where $g_i$ is the maximum.

## Table Description
No table is visible on this page.

## Concept Explanation
Discriminant functions provide a unified framework for classification. Instead of calculating complex probabilities directly, we define a set of functions $\{g_1(\mathbf{x}), g_2(\mathbf{x}), \dots, g_K(\mathbf{x})\}$—one for each class. The classification task then becomes a simple comparison: find the index $i$ that produces the largest output.

This approach is powerful because it allows us to implement different decision criteria (like minimum error or minimum risk) just by changing the definition of $g_i(\mathbf{x})$. The feature space is effectively partitioned into $K$ regions. The boundaries between these regions are the "decision boundaries," where the two highest discriminant functions are equal. If a "reject" option is included, it creates a region where the classifier refuses to make a choice, usually because the highest $g_i(\mathbf{x})$ is not significantly larger than the others.

## Exam / Viva Points
*   **Definition:** What is a discriminant function? (A function $g_i(\mathbf{x})$ used to represent a classification rule).
*   **Decision Rule:** How is a class chosen using these functions? (Choose class $i$ if $g_i(\mathbf{x})$ is the maximum among all $k$ classes).
*   **Common Forms:** Name three ways to define $g_i(\mathbf{x})$. (Negative risk, posterior probability, and the product of likelihood and prior).
*   **Decision Regions:** Define $\mathcal{R}_i$. (The set of points in feature space where class $i$ is the chosen class).
*   **Boundaries:** What mathematical condition defines the boundary between region $\mathcal{R}_i$ and $\mathcal{R}_j$? (It is the set of points where $g_i(\mathbf{x}) = g_j(\mathbf{x})$).
*   **Reject Option:** Why might a "reject" region exist in a decision space? (To handle cases of high uncertainty or to minimize the risk of making a costly wrong classification).

## Diagram Recreation Prompt
Create a professional educational slide titled "Discriminant Functions" in orange. 
On the left, list the following mathematical formulas using LaTeX formatting:
1. "choose $C_i$ if $g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})$"
2. A piecewise function for $g_i(\mathbf{x})$ with three cases: "$- R(\alpha_i \mid \mathbf{x})$", "$P(C_i \mid \mathbf{x})$", and "$p(\mathbf{x} \mid C_i)P(C_i)$".
3. "$\mathcal{R}_i = \{\mathbf{x} \mid g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})\}$" labeled as "K decision regions $\mathcal{R}_1, \dots, \mathcal{R}_K$".

On the right, include a 2D scatter plot with axes $x_1$ and $x_2$. 
- Plot three clusters of points: yellow squares (top-left), purple triangles (bottom-left), and green circles (right). 
- Draw smooth, color-coded boundary lines (yellow, purple, green) that partition the space into three regions labeled $C_1, C_2, C_3$. 
- Leave a central gap between the boundaries and label it "reject". 
- Add two black arrows pointing from the text "$g_i(\mathbf{x}), i = 1, \dots, K$" on the left toward the decision boundaries in the plot. 
Ensure the layout is clean, with ample white space and high-contrast colors.

## Diagram Data
*   **Title:** Discriminant Functions
*   **Formulas (Left):**
    *   Decision Rule: $\text{choose } C_i \text{ if } g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})$
    *   $g_i(\mathbf{x})$ options: $\{-R(\alpha_i|\mathbf{x}), P(C_i|\mathbf{x}), p(\mathbf{x}|C_i)P(C_i)\}$
    *   Region definition: $\mathcal{R}_i = \{\mathbf{x} \mid g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})\}$
*   **Plot Elements (Right):**
    *   **X-axis:** $x_1$
    *   **Y-axis:** $x_2$
    *   **Cluster 1 ($C_1$):** ~10 yellow squares, top-left region.
    *   **Cluster 2 ($C_2$):** ~7 purple triangles, bottom-left region.
    *   **Cluster 3 ($C_3$):** ~10 green circles, right region.
    *   **Boundaries:** Three curved lines meeting near the center, creating a "Y" shape with a gap.
    *   **Special Label:** "reject" placed in the central gap between boundaries.
