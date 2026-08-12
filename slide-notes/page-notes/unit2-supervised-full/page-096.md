# Unit 1 Page 96 Image Understanding

## Page Overview
The purpose of this slide is to provide a visual comparison between **Lasso (L1 Regularization)** and **Ridge (L2 Regularization)**. It illustrates how the geometric shape of the constraint regions in parameter space leads to different outcomes: Lasso tends to produce sparse solutions (feature selection), while Ridge shrinks coefficients toward zero without necessarily making them zero (coefficient shrinkage).

## Visible Text
*   **Lasso and Ridge** (Main Title)
*   **L1 Regularization (Lasso) - Feature Selection** (Left Heading)
*   **L2 Regularization (Ridge) - Coefficient Shrinkage** (Right Heading)
*   **Coefficient $\beta_2$** (Y-axis label for both graphs)
*   **Coefficient $\beta_1$** (X-axis label for both graphs)
*   **Lasso Solution (Sparse, $\beta_2 = 0$)** (Label with arrow pointing to the intersection on the x-axis)
*   **$|\beta_1| + |\beta_2| \leq C$** (L1 constraint formula)
*   **Ridge Solution (Shrunk, $\beta_1, \beta_2 \neq 0$)** (Label with arrow pointing to the intersection point)
*   **$\beta_1^2 + \beta_2^2 \leq C$** (L2 constraint formula)

## Visual Layout
*   **Title:** Large blue text centered at the top.
*   **Header Decoration:** A thick brown horizontal arrow-like shape points from the left margin toward the title.
*   **Content Blocks:** The page is split into two equal vertical halves, each containing a mathematical graph and descriptive text.
*   **Color Palette:** 
    *   **Blue:** Used for the title and the elliptical loss contours.
    *   **Red:** Used for the constraint boundaries (diamond and circle).
    *   **Black:** Used for axes, labels, and solution arrows.
*   **Alignment:** The two graphs are aligned horizontally to allow for direct comparison of their shapes and intersection points.
*   **Visual Hierarchy:** The title establishes the topic, the subheadings define the specific method, and the diagrams provide the technical proof of the concept.

## Diagram Type
This page features two **mathematical graphs** (specifically, contour plots overlaid with constraint regions). They are used to demonstrate the geometric interpretation of optimization under constraints in a 2D parameter space ($\beta_1, \beta_2$).

## Diagram / Visual Explanation
Both diagrams show a coordinate system where the x-axis represents coefficient $\beta_1$ and the y-axis represents coefficient $\beta_2$.

1.  **Loss Contours (Blue Ellipses):** In both graphs, the blue concentric ellipses represent the contours of the Least Squares error function (RSS). The center of these ellipses (not shown, but implied to be further to the top-right) is the Ordinary Least Squares (OLS) estimate. As you move outward from the center, the error increases.
2.  **Constraint Regions (Red Shapes):**
    *   **Lasso (Left):** The red shape is a **diamond** centered at the origin. This represents the L1 norm constraint $|\beta_1| + |\beta_2| \leq C$.
    *   **Ridge (Right):** The red shape is a **circle** centered at the origin. This represents the L2 norm constraint $\beta_1^2 + \beta_2^2 \leq C$.
3.  **The Solution Point:** The regularized solution is the point where the smallest possible blue ellipse (lowest error) first touches the red constraint region.
    *   **Lasso Intersection:** Because the diamond has sharp corners on the axes, the elliptical contours are highly likely to hit a corner first. In the diagram, the intersection happens exactly on the $\beta_1$ axis, meaning $\beta_2$ is forced to zero.
    *   **Ridge Intersection:** Because the circle is smooth, the ellipse typically touches it at a point that is not on an axis. In the diagram, the intersection occurs at a point where both $\beta_1$ and $\beta_2$ have non-zero values, though they are smaller (shrunk) compared to the OLS solution.

## Math / Formula / Curve Notes
*   **$|\beta_1| + |\beta_2| \leq C$**: This is the **L1 Norm**. The sum of the absolute values of the coefficients must be less than or equal to a constant $C$. Geometrically, in 2D, this creates a square rotated by 45 degrees (a diamond).
*   **$\beta_1^2 + \beta_2^2 \leq C$**: This is the **L2 Norm**. The sum of the squares of the coefficients must be less than or equal to a constant $C$. Geometrically, this creates a circle with radius $\sqrt{C}$.
*   **$\beta_1, \beta_2$**: These represent the weights or coefficients of the features in a linear model.
*   **$C$**: A budget parameter. A smaller $C$ corresponds to a larger regularization penalty ($\lambda$).

## Table Description
No table is visible on this page.

## Concept Explanation
Regularization is a technique used to prevent overfitting by penalizing large coefficients in a model. 

*   **Lasso (Least Absolute Shrinkage and Selection Operator):** By using the L1 penalty, Lasso performs "Feature Selection." Because the constraint region is a diamond, the optimization process often finds a solution at the "corners" of the diamond, which lie on the axes. When a solution lies on an axis, the coefficients for other dimensions become exactly zero. This effectively removes those features from the model.
*   **Ridge Regression:** By using the L2 penalty, Ridge performs "Coefficient Shrinkage." The circular constraint region doesn't have sharp corners. Therefore, the solution point is unlikely to fall exactly on an axis. Instead, all coefficients are pulled closer to zero (shrunk), but they rarely reach exactly zero. This keeps all features in the model but reduces their impact to prevent the model from being too sensitive to noise.

## Exam / Viva Points
*   **Shape Difference:** Remember that L1 (Lasso) is a diamond/polyhedron, while L2 (Ridge) is a circle/hypersphere.
*   **Sparsity:** Lasso produces sparse models (some coefficients = 0). Ridge produces dense models (coefficients $\approx$ 0 but $\neq$ 0).
*   **Feature Selection:** Lasso is used for automated feature selection; Ridge is not.
*   **Optimization:** The solution is the point of tangency between the loss function contours and the constraint boundary.
*   **Constraint vs. Penalty:** The formulas shown ($|\beta| \leq C$) are the "constrained optimization" form. In the "penalty" form, this is expressed as adding $\lambda \sum |\beta|$ or $\lambda \sum \beta^2$ to the cost function. A smaller $C$ in the diagram corresponds to a larger $\lambda$ (more regularization).

## Diagram Recreation Prompt
Create a high-quality educational graphic comparing Lasso and Ridge regularization. 
- **Left Side:** Title "L1 Regularization (Lasso)". Draw a 2D Cartesian coordinate system with axes labeled "Coefficient $\beta_1$" and "Coefficient $\beta_2$". Draw a red diamond centered at the origin. Draw a series of blue concentric ellipses (loss contours) centered in the upper right quadrant. Show the innermost ellipse just touching the right-most corner of the red diamond on the x-axis. Add a black arrow pointing to this intersection labeled "Lasso Solution (Sparse, $\beta_2 = 0$)". Below the graph, write the formula "$|\beta_1| + |\beta_2| \leq C$".
- **Right Side:** Title "L2 Regularization (Ridge)". Draw an identical coordinate system. Draw a red circle centered at the origin. Draw the same blue concentric ellipses. Show the innermost ellipse touching the edge of the red circle at a point not on the axes. Add a black arrow pointing to this intersection labeled "Ridge Solution (Shrunk, $\beta_1, \beta_2 \neq 0$)". Below the graph, write the formula "$\beta_1^2 + \beta_2^2 \leq C$".
- **Style:** Clean, professional, white background, clear vector lines.

## Diagram Data
*   **Axes:** X-axis ($\beta_1$), Y-axis ($\beta_2$).
*   **Lasso Constraint:** Vertices at $(1,0), (0,1), (-1,0), (0,-1)$ forming a diamond.
*   **Ridge Constraint:** Circle with radius $r=1$ centered at $(0,0)$.
*   **Loss Contours:** Ellipses centered at approximately $(2, 1.5)$.
*   **Lasso Intersection Point:** $(1, 0)$.
*   **Ridge Intersection Point:** Approximately $(0.8, 0.6)$ (tangent point on the circle).
