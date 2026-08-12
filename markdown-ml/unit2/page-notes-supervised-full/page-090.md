# Unit 1 Page 90 Image Understanding

## Page Overview
The purpose of this slide is to define the mathematical cost function for **Lasso Regression**. It introduces the concept of L1 regularization by showing how a penalty term based on the absolute values of weights is added to the standard Mean Squared Error (MSE). The slide also provides a legend defining the variables used in the equation.

## Visible Text
*   **Lasso Regression** (Title)
*   $\text{Cost} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 + \lambda \sum_{j=1}^{m} |w_j|$
*   **Where**
    *   $m$: Number of Features
    *   $n$: Number of Examples
    *   $y_i$: Actual Target Value
    *   $\hat{y}_i$: Predicted Target Value

## Visual Layout
*   **Title:** "Lasso Regression" is positioned at the top center-left in a large, bold red font.
*   **Header Accent:** A dark red horizontal arrow-like shape is located on the far left, aligned with the title.
*   **Main Content Box:** A large white rectangular container with rounded corners holds the formula and text.
*   **Formula Highlight:** The cost function formula is placed inside a light-grey horizontal band at the top of the white container to make it stand out.
*   **Variable Definitions:** Below the formula, the word "Where" introduces a bulleted list of variable definitions.
*   **Background:** The overall background is a light beige with a subtle, abstract curved line pattern on the left side.
*   **Hierarchy:** The red title draws immediate attention, followed by the highlighted formula, and then the supporting text definitions.

## Diagram Type
This is a **formula derivation/definition slide**. It uses mathematical notation to define a core machine learning concept rather than using a flowchart or graph.

## Diagram / Visual Explanation
While not a graphical diagram, the visual structure separates the **Cost Function** from its **Variable Definitions**.
*   The formula itself is split into two logical parts:
    1.  **Loss Term:** $\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$ (Mean Squared Error).
    2.  **Regularization Term:** $\lambda \sum_{j=1}^{m} |w_j|$ (L1 Penalty).
*   The bullet points below act as a key to decode the mathematical symbols used in the formula above.

## Math / Formula / Curve Notes
The formula shown is the **Lasso Regression Cost Function**:
$$\text{Cost} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 + \lambda \sum_{j=1}^{m} |w_j|$$

*   **$\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$**: This is the **Mean Squared Error (MSE)**. It calculates the average of the squares of the errors—that is, the average squared difference between the estimated values ($\hat{y}_i$) and the actual value ($y_i$).
*   **$n$**: The total number of data points or training examples in the dataset.
*   **$y_i$**: The actual ground-truth target value for the $i$-th observation.
*   **$\hat{y}_i$**: The value predicted by the regression model for the $i$-th observation.
*   **$\lambda$ (Lambda)**: The **regularization parameter** (tuning parameter). It controls the strength of the penalty. A higher $\lambda$ increases the penalty on the size of the coefficients.
*   **$\sum_{j=1}^{m} |w_j|$**: The **L1 Regularization term**. It is the sum of the absolute values of the model's weights (coefficients).
*   **$m$**: The total number of features (independent variables) in the model.
*   **$w_j$**: The weight or coefficient assigned to the $j$-th feature.

## Table Description
No table is visible on this page.

## Concept Explanation
**Lasso Regression** (Least Absolute Shrinkage and Selection Operator) is a type of linear regression that uses **L1 regularization**. 

In standard linear regression, the goal is to minimize the Mean Squared Error (MSE). However, this can lead to **overfitting**, especially when there are many features. Lasso addresses this by adding a penalty term to the cost function equal to the absolute value of the magnitude of coefficients.

**Key characteristics of Lasso:**
1.  **Shrinkage:** It shrinks the coefficient estimates towards zero.
2.  **Feature Selection:** Unlike Ridge regression (which uses L2 regularization), Lasso can force some coefficient estimates to be exactly zero when $\lambda$ is sufficiently large. This effectively removes those features from the model, making it a built-in feature selection tool.
3.  **Sparsity:** It produces "sparse" models, which are simpler and easier to interpret.

## Exam / Viva Points
*   **Full Form:** LASSO stands for Least Absolute Shrinkage and Selection Operator.
*   **Regularization Type:** Lasso uses **L1 Regularization**.
*   **Penalty Term:** The penalty is the sum of the **absolute values** of the weights ($|w|$).
*   **Feature Selection:** Be prepared to explain why Lasso is used for feature selection (it can zero out coefficients) while Ridge cannot.
*   **Lambda ($\lambda$):** Explain that if $\lambda = 0$, the cost function becomes standard OLS (Ordinary Least Squares) regression. As $\lambda \to \infty$, all coefficients tend toward zero.
*   **Bias-Variance Trade-off:** Regularization increases bias slightly but significantly reduces variance, helping the model generalize better to unseen data.

## Diagram Recreation Prompt
Create a professional educational slide titled "Lasso Regression" in bold red font. Below the title, include a light-grey rectangular box containing the mathematical formula: "Cost = (1/n) * Σ(yi - ŷi)² + λ * Σ|wj|". Underneath the formula box, add a section titled "Where" in a standard black font, followed by a clean bulleted list defining the variables: "m: Number of Features", "n: Number of Examples", "yi: Actual Target Value", and "ŷi: Predicted Target Value". Use a clean white background with a subtle decorative geometric pattern on the left edge. Ensure high contrast and clear mathematical typesetting.

## Diagram Data
*   **Title:** Lasso Regression
*   **Formula Components:**
    *   Term 1: Mean Squared Error (MSE) = $\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$
    *   Term 2: L1 Penalty = $\lambda \sum_{j=1}^{m} |w_j|$
*   **Variable Definitions:**
    *   $m$: Number of Features
    *   $n$: Number of Examples
    *   $y_i$: Actual Target Value
    *   $\hat{y}_i$: Predicted Target Value
    *   $\lambda$: Regularization Parameter
    *   $w_j$: Model Weights/Coefficients
