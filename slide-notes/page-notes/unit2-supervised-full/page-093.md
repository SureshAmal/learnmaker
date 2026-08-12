# Unit 1 Page 93 Image Understanding

## Page Overview
The purpose of this slide is to introduce **Ridge Regression**, a specific type of linear regression that incorporates regularization to prevent overfitting. It defines the technique, explains its primary mechanism (L2 regularization), describes its utility in handling multicollinearity, and provides the formal mathematical cost function used to train the model.

## Visible Text
*   **2. Ridge Regression** (Title)
*   A regression model that uses the L2 regularization technique is called **Ridge regression**.
*   It adds the squared magnitude of the coefficient as a penalty term to the loss function(L).
*   It handles multicollinearity by shrinking the coefficients of correlated features, reducing their variance and preventing any single feature from dominating the model.
*   **Formula in box:**
    $$\text{Cost} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 + \lambda \sum_{j=1}^{m} w_j^2$$

## Visual Layout
*   **Title:** Located at the top left, in large, bold red font.
*   **Header Graphic:** A thick red arrow-like shape points from the far left margin toward the title.
*   **Background:** A light green gradient background with abstract, thin, dark curved lines on the left side for aesthetic framing.
*   **Content Blocks:** Three bullet points using square bullet icons, aligned to the left. The term "Ridge regression" in the first bullet is underlined and colored orange-red.
*   **Formula Box:** The mathematical equation is centered at the bottom of the slide, enclosed in a white rectangular box with a thin black border.
*   **Visual Hierarchy:** The title is the most prominent, followed by the descriptive text, and finally the boxed formula which serves as the technical summary.

## Diagram Type
**Mathematical Formula.** This slide is primarily text-based with a central mathematical expression that defines the cost function of the machine learning algorithm.

## Diagram / Visual Explanation
The visual focus is the **Cost Function Box**. It represents the objective function that the Ridge Regression algorithm seeks to minimize.
*   **Left Part (Loss Term):** Represents the standard Mean Squared Error (MSE), which measures how well the model fits the training data.
*   **Right Part (Penalty Term):** Represents the L2 regularization term, which penalizes large coefficients to prevent overfitting.
*   **The "+" Sign:** Indicates that the total cost is a combination of fitting the data and keeping the model simple (small weights).

## Math / Formula / Curve Notes
The formula is: $\text{Cost} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 + \lambda \sum_{j=1}^{m} w_j^2$

*   **$\text{Cost}$**: The total objective function to be minimized during training.
*   **$n$**: The total number of data points (samples).
*   **$\sum_{i=1}^{n}$**: Summation over all $n$ samples.
*   **$y_i$**: The actual observed value for the $i$-th sample.
*   **$\hat{y}_i$**: The predicted value for the $i$-th sample.
*   **$(y_i - \hat{y}_i)^2$**: The squared error for a single prediction.
*   **$\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$**: The Mean Squared Error (MSE) component.
*   **$\lambda$ (Lambda)**: The regularization parameter (tuning parameter). It controls the strength of the penalty. If $\lambda = 0$, it becomes standard OLS regression. As $\lambda \to \infty$, coefficients approach zero.
*   **$m$**: The number of features (independent variables).
*   **$w_j$**: The coefficient (weight) associated with the $j$-th feature.
*   **$\sum_{j=1}^{m} w_j^2$**: The sum of the squares of the coefficients (L2 norm).

## Table Description
No table is visible on this page.

## Concept Explanation
**Ridge Regression** is a technique used when the data suffers from **multicollinearity** (independent variables are highly correlated). In standard Linear Regression (Ordinary Least Squares), multicollinearity can lead to very high variance in coefficient estimates, making the model sensitive to small changes in the data.

**How it works:**
1.  **L2 Regularization:** It modifies the standard loss function by adding a penalty equivalent to the square of the magnitude of coefficients.
2.  **Shrinkage:** This penalty forces the learning algorithm to not only fit the data but also keep the weights ($w_j$) as small as possible. This "shrinks" the coefficients toward zero, though they never quite reach zero (unlike Lasso regression).
3.  **Bias-Variance Tradeoff:** By adding a little bias (via the penalty), Ridge regression significantly reduces the variance of the model, leading to better generalization on unseen data.

## Exam / Viva Points
*   **Definition:** Ridge regression is a linear regression variant that uses **L2 regularization**.
*   **Penalty Term:** The penalty is the **squared magnitude** of the coefficients ($\lambda \sum w^2$).
*   **Purpose:** It is primarily used to handle **multicollinearity** and prevent **overfitting**.
*   **Effect on Coefficients:** It shrinks coefficients toward zero but does not perform feature selection (coefficients remain non-zero).
*   **Lambda ($\lambda$):** Know that $\lambda$ is the hyperparameter that controls the trade-off between fitting the training data and keeping the weights small.
*   **Comparison:** Be prepared to compare it with Lasso (L1 regularization), which uses the absolute value of coefficients and can perform feature selection by setting some weights to exactly zero.

## Diagram Recreation Prompt
Create a professional educational slide titled "2. Ridge Regression" in bold red. Use a clean white background with a subtle light-blue side accent. 
Include three bullet points: 
1. "A regression model using L2 regularization." 
2. "Adds squared magnitude of coefficients as a penalty to the loss function." 
3. "Reduces variance and handles multicollinearity by shrinking coefficients." 
At the bottom center, place a prominent, clearly formatted LaTeX formula inside a light-grey shaded box with a dark border: "Cost = 1/n * sum_{i=1 to n}(y_i - y_hat_i)^2 + lambda * sum_{j=1 to m}(w_j^2)". Use high-contrast black text for the body.

## Diagram Data
*   **Title:** 2. Ridge Regression
*   **Bullet 1:** A regression model that uses the L2 regularization technique is called Ridge regression.
*   **Bullet 2:** It adds the squared magnitude of the coefficient as a penalty term to the loss function(L).
*   **Bullet 3:** It handles multicollinearity by shrinking the coefficients of correlated features, reducing their variance and preventing any single feature from dominating the model.
*   **Formula Components:**
    *   **Term 1:** Mean Squared Error (MSE) = $\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$
    *   **Term 2:** L2 Penalty = $\lambda \sum_{j=1}^{m} w_j^2$
    *   **Total:** $\text{Cost} = \text{Term 1} + \text{Term 2}$
