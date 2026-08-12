# Unit 1 Page 42 Image Understanding

## Page Overview
The purpose of this slide is to define and illustrate the concept of **Discriminant Functions** in the context of multi-class classification. It explains how these functions are used to partition a feature space into decision regions and provides different mathematical forms these functions can take (risk-based, posterior-based, or likelihood-based).

## Visible Text
*   **Title:** Discriminant Functions
*   **Decision Rule:** $\text{choose } C_i \text{ if } g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})$
*   **Discriminant Function Definitions:**
    $g_i(\mathbf{x}) = \begin{cases} - R(\alpha_i \mid \mathbf{x}) \\ P(C_i \mid \mathbf{x}) \\ p(\mathbf{x} \mid C_i)P(C_i) \end{cases}$
*   **Function Index:** $g_i(\mathbf{x}), i = 1, \dots, K$
*   **Decision Regions:** $K$ decision regions $\mathcal{R}_1, \dots, \mathcal{R}_K$
*   **Region Definition:** $\mathcal{R}_i = \{\mathbf{x} \mid g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})\}$
*   **Plot Labels:**
    *   $x_1, x_2$ (Axes)
    *   $C_1, C_2, C_3$ (Class labels)
    *   reject (Region label)
    *   $g_i(\mathbf{x}), i = 1, \dots, K$ (Annotation with arrows)

## Visual Layout
*   **Title:** Located at the top left in a large, orange, serif font.
*   **Left Column:** Contains the mathematical definitions and formulas in black text. The piecewise bracket for $g_i(\mathbf{x})$ clearly shows three alternative definitions.
*   **Right Column:** Features a 2D scatter plot/decision region diagram.
*   **Diagram Details:**
    *   Black axes for $x_1$ and $x_2$.
    *   Three distinct clusters of shapes: yellow squares ($C_1$), purple triangles ($C_2$), and green circles ($C_3$).
    *   Colored boundary lines (yellow, purple, green) delineate the regions for each class.
    *   A central white space is labeled "reject".
    *   Two arrows point from the text "$g_i(\mathbf{x}), i = 1, \dots, K$" to the decision boundaries.
*   **Background:** Plain white with a decorative brown/tan abstract graphic on the far left edge.

## Diagram Type
This is a **Mathematical Graph / Decision Region Plot**. It visualizes how a 2D feature space is divided into discrete regions ($\mathcal{R}_i$) based on the values of discriminant functions, showing the boundaries where classification decisions change.

## Diagram / Visual Explanation
The diagram illustrates a 3-class classification problem in a 2D feature space ($x_1, x_2$):
1.  **Data Clusters:** Points belonging to classes $C_1$ (yellow squares), $C_2$ (purple triangles), and $C_3$ (green circles) are grouped in different areas of the plot.
2.  **Decision Boundaries:** The colored curves represent the boundaries where the discriminant functions for adjacent classes are equal (e.g., $g_1(\mathbf{x}) = g_2(\mathbf{x})$).
3.  **Decision Regions ($\mathcal{R}_i$):** The area enclosed by the yellow boundary is $\mathcal{R}_1$, the purple is $\mathcal{R}_2$, and the green is $\mathcal{R}_3$. Within each region, the corresponding $g_i(\mathbf{x})$ is the maximum.
4.  **Reject Region:** The central area labeled "reject" represents a part of the feature space where the classifier might refuse to make a prediction, typically because the confidence is too low or the risk of error is too high.
5.  **Arrows:** The arrows emphasize that the boundaries themselves are defined by the set of discriminant functions $g_i(\mathbf{x})$.

## Math / Formula / Curve Notes
*   **$\mathbf{x}$:** The input feature vector.
*   **$C_i$:** The $i$-th class label.
*   **$g_i(\mathbf{x})$:** The discriminant function for class $i$. The classifier picks the class with the highest $g_i$ value.
*   **$- R(\alpha_i \mid \mathbf{x})$:** Negative conditional risk. Maximizing negative risk is equivalent to minimizing the expected loss (risk) of choosing class $C_i$.
*   **$P(C_i \mid \mathbf{x})$:** Posterior probability. This is the probability that the input belongs to class $C_i$ given the observed features $\mathbf{x}$. Maximizing this minimizes the error rate.
*   **$p(\mathbf{x} \mid C_i)P(C_i)$:** The product of the class-conditional density (likelihood) and the prior probability. According to Bayes' rule, this is proportional to the posterior probability, as the evidence $p(\mathbf{x})$ is a constant for all classes.
*   **$\mathcal{R}_i$:** The decision region for class $i$, defined as the set of all points $\mathbf{x}$ where $g_i(\mathbf{x})$ is the maximum among all $K$ functions.

## Table Description
No table is visible on this page.

## Concept Explanation
**Discriminant Functions** are a fundamental tool in pattern recognition. Instead of modeling the full probability distribution, we define a set of functions—one for each class—that "discriminate" between them.

The core idea is to map every point in the feature space to a specific class. We do this by calculating $K$ different values for an input $\mathbf{x}$ and choosing the index $i$ that yields the largest value. 

Depending on the objective, $g_i(\mathbf{x})$ can be defined in different ways:
1.  **MAP (Maximum A Posteriori) Rule:** Using $P(C_i \mid \mathbf{x})$ directly.
2.  **Generative Approach:** Using $p(\mathbf{x} \mid C_i)P(C_i)$, which is easier to compute if we know the class distributions and priors.
3.  **Minimum Risk:** Using negative risk when different types of misclassification have different costs.

The boundaries where these functions "tie" create the decision boundaries that partition the space into **Decision Regions**.

## Exam / Viva Points
*   **Definition:** What is a discriminant function? (A function used to represent a decision rule by assigning an input to the class with the maximum function value).
*   **Decision Rule:** State the rule: $\text{choose } C_i \text{ if } g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})$.
*   **Three Forms:** Be able to list and explain the three common forms of $g_i(\mathbf{x})$ shown on the slide (Negative Risk, Posterior, Likelihood $\times$ Prior).
*   **Decision Regions:** Define $\mathcal{R}_i$ mathematically.
*   **Reject Region:** Explain why a "reject" region might exist (e.g., when the maximum posterior is below a certain threshold).
*   **Bayes Connection:** Explain why maximizing $p(\mathbf{x} \mid C_i)P(C_i)$ is equivalent to maximizing the posterior $P(C_i \mid \mathbf{x})$.

## Diagram Recreation Prompt
Create a professional educational slide titled "Discriminant Functions" in orange. 
On the left side, display the following mathematical formulas in a clean, large font:
1. "choose $C_i$ if $g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})$"
2. A piecewise function $g_i(\mathbf{x})$ with three branches: "$- R(\alpha_i \mid \mathbf{x})$", "$P(C_i \mid \mathbf{x})$", and "$p(\mathbf{x} \mid C_i)P(C_i)$".
3. Below these, write "$K$ decision regions $\mathcal{R}_1, \dots, \mathcal{R}_K$" and the set definition "$\mathcal{R}_i = \{\mathbf{x} \mid g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})\}$".

On the right side, include a 2D scatter plot with $x_1$ and $x_2$ axes. 
- Plot a cluster of yellow squares in the top-left labeled $C_1$.
- Plot a cluster of purple triangles in the bottom-left labeled $C_2$.
- Plot a cluster of green circles on the right side labeled $C_3$.
- Draw smooth, color-coded boundary lines around each cluster. 
- Label the central empty area between the boundaries as "reject".
- Add an annotation "$g_i(\mathbf{x}), i = 1, \dots, K$" with arrows pointing to the boundary lines.
Use a white background and a modern, minimalist aesthetic.

## Diagram Data
*   **Title:** Discriminant Functions
*   **Math Content:**
    *   Rule: $\text{choose } C_i \text{ if } g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})$
    *   $g_i(\mathbf{x})$ options: $\{-R(\alpha_i|\mathbf{x}), P(C_i|\mathbf{x}), p(\mathbf{x}|C_i)P(C_i)\}$
    *   Region: $\mathcal{R}_i = \{\mathbf{x} \mid g_i(\mathbf{x}) = \max_k g_k(\mathbf{x})\}$
*   **Plot Elements:**
    *   **Axes:** $x_1$ (horizontal), $x_2$ (vertical)
    *   **Class $C_1$:** Yellow squares, approx. coordinates $(-2, 2)$
    *   **Class $C_2$:** Purple triangles, approx. coordinates $(-2, -2)$
    *   **Class $C_3$:** Green circles, approx. coordinates $(3, 0)$
    *   **Boundaries:** Curved lines separating the three clusters.
    *   **Reject Region:** Central area $(0, 0)$ where boundaries converge.
    *   **Annotation:** "$g_i(\mathbf{x}), i = 1, \dots, K$" with arrows to boundaries.
