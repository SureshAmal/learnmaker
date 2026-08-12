# Unit 1 Page 98 Image Understanding

## Page Overview
The purpose of this slide is to define the mathematical cost function for **Elastic Net Regularization**. It provides the full equation, which combines the Mean Squared Error (MSE) with both L1 (Lasso) and L2 (Ridge) penalty terms. The slide further defines each variable and parameter used in the formula, specifically explaining how the mixing parameter $\alpha$ allows the model to transition between Lasso and Ridge regularization.

## Visible Text
**Formula:**
$$\text{Cost} = \frac{1}{n} \sum_{i=1}^{n}(y_i - \hat{y}_i)^2 + \lambda \left( (1 - \alpha) \sum_{j=1}^{m} |w_j| + \alpha \sum_{j=1}^{m} w_j^2 \right)$$

**Where**
* **$n$:** Number of examples (data points)
* **$m$:** Number of features (predictor variables)
* **$y_i$:** Actual target value for the $i^{th}$ example
* **$\hat{y}_i$:** Predicted target value for the $i^{th}$ example
* **$w_i$:** Coefficients of the features
* **$\lambda$:** Regularization parameter that controls the strength of regularization
* **$\alpha$:** Mixing parameter where $0 \le \alpha \le 1$ and $\alpha = 1$ corresponds to Lasso ($L_1$) regularization, $\alpha = 0$ corresponds to Ridge ($L_2$) regularization and Values between 0 and 1 provide a balance of both L1 and L2 regularization

## Visual Layout
* **Header/Background:** A dark red horizontal bar is visible at the top left. The background features light green and beige tones with subtle curved decorative lines on the left.
* **Main Content Box:** A large white rectangular area with a thin black border contains all the text and formulas.
* **Formula Box:** The main cost function is placed at the top of the white area, enclosed in a light gray rounded rectangle to make it stand out as the primary focus.
* **Variable Definitions:** Below the formula, the word "Where" introduces a bulleted list of definitions.
* **Alignment:** The formula is centered within its gray box. The definitions are left-aligned with standard bullet points.
* **Typography:** Mathematical symbols are rendered in LaTeX-style font, while descriptive text uses a clean sans-serif font.

## Diagram Type
**Formula Derivation / Definition Slide.**
This is a text-heavy slide centered around a complex mathematical equation. It does not contain flowcharts or graphs but serves as a reference for the components of the Elastic Net cost function.

## Diagram / Visual Explanation
There is no diagram on this page. The visual hierarchy is established through the use of a shaded box for the main formula and a clear bulleted list for the supporting definitions.

## Math / Formula / Curve Notes
The formula represents the **Elastic Net Cost Function**:
* **$\frac{1}{n} \sum_{i=1}^{n}(y_i - \hat{y}_i)^2$**: This is the **Mean Squared Error (MSE)**, representing the loss or error between actual values ($y_i$) and predicted values ($\hat{y}_i$).
* **$\lambda$ (Lambda)**: The overall regularization strength. A higher $\lambda$ penalizes large coefficients more heavily.
* **$(1 - \alpha) \sum_{j=1}^{m} |w_j|$**: The **L1 penalty** (Lasso). It uses the absolute values of the weights ($w_j$).
* **$\alpha \sum_{j=1}^{m} w_j^2$**: The **L2 penalty** (Ridge). It uses the squared values of the weights ($w_j$).
* **$\alpha$ (Alpha)**: The mixing parameter. 
    * *Note on Slide Discrepancy:* In the provided formula, if $\alpha=1$, the L1 term becomes 0 and the L2 term is active (Ridge). If $\alpha=0$, the L2 term becomes 0 and the L1 term is active (Lasso). However, the text description on the slide states the opposite ($\alpha=1$ for Lasso, $\alpha=0$ for Ridge). Students should be aware that different libraries (like scikit-learn) might use different conventions for $\alpha$.

## Table Description
No table is visible on this page.

## Concept Explanation
**Elastic Net Regularization** is a regularized regression method that linearly combines the $L_1$ and $L_2$ penalties of the Lasso and Ridge methods. 

* **Why use it?** Lasso can be too aggressive by zeroing out coefficients (feature selection), which might not be ideal if features are highly correlated. Ridge handles correlated features well but doesn't perform feature selection. Elastic Net provides a middle ground.
* **The Mixing Parameter ($\alpha$):** By adjusting $\alpha$, a data scientist can choose how much of each penalty to apply. 
    * If $\alpha$ is close to the Lasso side, the model will favor sparsity (fewer non-zero weights).
    * If $\alpha$ is close to the Ridge side, the model will favor small, distributed weights across all features.
* **The Regularization Strength ($\lambda$):** This controls the trade-off between fitting the training data well (low MSE) and keeping the model simple (low weights) to prevent overfitting.

## Exam / Viva Points
* **Define Elastic Net:** It is a hybrid regularization technique that adds both L1 and L2 penalties to the loss function.
* **Identify the components:** Be able to point out the MSE part, the L1 part (absolute weights), and the L2 part (squared weights).
* **Role of $\lambda$:** It controls the overall impact of regularization. If $\lambda = 0$, it's just standard OLS regression.
* **Role of $\alpha$:** It is the mixing ratio. Explain what happens when $\alpha$ is 0, 1, or in between. (Be careful to follow the specific convention used in your textbook/exam, as the slide text and formula here are contradictory).
* **Advantage over Lasso/Ridge:** Elastic Net is often preferred when there are multiple features that are correlated with each other.

## Diagram Recreation Prompt
Create a clean educational slide for "Elastic Net Cost Function". 
- At the top, place the formula: $\text{Cost} = \text{MSE} + \lambda [ (1-\alpha) \cdot L1\_Penalty + \alpha \cdot L2\_Penalty ]$ inside a prominent, light-blue shaded box with rounded corners.
- Below the formula, create two columns. 
- Left column: "Variable Definitions" with a bulleted list for $n, m, y_i, \hat{y}_i, w_j, \lambda$.
- Right column: "Mixing Parameter ($\alpha$)" with a small horizontal slider graphic. Label the left end "$\alpha=0$ (Lasso)" and the right end "$\alpha=1$ (Ridge)". 
- Use a professional sans-serif font and high-contrast colors (dark text on a light background).

## Diagram Data
**Title:** Elastic Net Cost Function
**Formula:** $\text{Cost} = \frac{1}{n} \sum_{i=1}^{n}(y_i - \hat{y}_i)^2 + \lambda \left( (1 - \alpha) \sum_{j=1}^{m} |w_j| + \alpha \sum_{j=1}^{m} w_j^2 \right)$
**Definitions:**
- $n$: Number of data points
- $m$: Number of features
- $y_i$: Actual value
- $\hat{y}_i$: Predicted value
- $w_j$: Feature weights/coefficients
- $\lambda$: Regularization strength
- $\alpha$: Mixing parameter (0 to 1)
