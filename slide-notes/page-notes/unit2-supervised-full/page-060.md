# Unit 1 Page 60 Image Understanding

## Page Overview
The purpose of this slide is to introduce and define the primary evaluation metrics used to assess the performance and accuracy of linear regression models. It provides a high-level overview of five key metrics: Mean Squared Error (MSE), Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), R-Squared, and Adjusted R-Squared, explaining what each measures and its significance in model evaluation.

## Visible Text
**Evaluation Metrics**

A variety of evaluation measures can be used to determine the strength of any linear regression model. These assessment metrics often give an indication of how well the model is producing the observed outputs.

1.  **Mean Squared Error (MSE):** Measures the average squared difference between actual and predicted values to avoid cancellation of errors.
2.  **Mean Absolute Error (MAE):** Calculate the accuracy of a regression model. MAE measures the average absolute difference between the predicted values and actual values.
3.  **Root Mean Squared Error (RMSE):** Square root of the residuals variance is RMSE. It describes how well the observed data points match the expected values or the model's absolute fit to the data.
4.  **R-Squared:** Indicates how much variation the model explains. Its value is typically between 0 and 1, but it can be negative if the model performs worse than a simple baseline model (e.g., predicting the mean).
5.  **Adjusted R-square:** Measures the proportion of variance explained by the model while adjusting for the number of predictors and penalizing irrelevant features.

## Visual Layout
*   **Title:** "Evaluation Metrics" is written in a large, bold, green sans-serif font, centered at the top of the page.
*   **Background:** The background is a light cream or off-white color with a subtle gradient.
*   **Decorative Elements:** On the left side, there are several thin, overlapping curved lines in shades of brown and grey. A thick, dark brown horizontal bar extends from the left edge into the top-left corner of the text area.
*   **Text Content:** The main body text is in a dark grey, serif font.
*   **List Structure:** The five metrics are presented as a numbered list. Each metric name is highlighted in green and underlined, followed by a colon and a descriptive sentence.
*   **Alignment:** The text is left-aligned, creating a clear vertical flow for the reader.

## Diagram Type
This is a **text-only slide** with decorative graphic elements. It uses a structured numbered list to organize information rather than a flowchart, architecture diagram, or data plot.

## Diagram / Visual Explanation
No diagram is present on this page. The visual elements (curved lines and the brown bar) are purely decorative and do not convey specific machine-learning data or processes.

## Math / Formula / Curve Notes
No mathematical formulas or curves are explicitly visible on this page. However, the text describes the mathematical logic behind the metrics:
*   **MSE:** Implies a formula involving $\frac{1}{n} \sum (y - \hat{y})^2$.
*   **MAE:** Implies a formula involving $\frac{1}{n} \sum |y - \hat{y}|$.
*   **RMSE:** Implies $\sqrt{MSE}$.
*   **R-Squared:** Mentions a range of 0 to 1.
*   **Adjusted R-square:** Mentions a penalty for the number of predictors.

## Table Description
No table is visible on this page.

## Concept Explanation
This slide covers the fundamental ways to measure how "wrong" or "right" a regression model is:

*   **Error-based Metrics (MSE, MAE, RMSE):** These focus on the distance between the predicted value ($\hat{y}$) and the actual value ($y$). 
    *   **MSE** squares the errors, which penalizes large outliers more heavily and ensures positive values (so positive and negative errors don't cancel out).
    *   **MAE** uses absolute values, providing a linear representation of error that is easier to interpret in the original units of the data.
    *   **RMSE** brings the MSE back to the original units of the target variable by taking the square root, making it a popular choice for reporting "average" error.
*   **Goodness-of-Fit Metrics (R-Squared, Adjusted R-Squared):**
    *   **R-Squared ($R^2$):** Known as the coefficient of determination. It represents the percentage of the variance in the dependent variable that is predictable from the independent variables. A value of 1.0 indicates the model explains all variability.
    *   **Adjusted R-Squared:** A modification of $R^2$ that accounts for the number of predictors in the model. Standard $R^2$ always increases when new variables are added (even if they are useless). Adjusted $R^2$ only increases if the new term improves the model more than would be expected by chance, penalizing the addition of unnecessary complexity.

## Exam / Viva Points
*   **Why square the errors in MSE?** To ensure all error values are positive (preventing cancellation) and to give higher weight/penalty to larger errors (outliers).
*   **What is the difference between MAE and RMSE?** MAE treats all errors equally, while RMSE gives a relatively high weight to large errors. RMSE is often preferred when large errors are particularly undesirable.
*   **Can R-Squared be negative?** Yes, if the chosen model fits the data worse than a horizontal line representing the mean of the data.
*   **Why use Adjusted R-Squared instead of R-Squared?** To avoid "overfitting" by adding too many variables. Adjusted R-Squared penalizes the model for adding features that do not contribute significantly to its predictive power.
*   **Units:** Remember that MSE is in "units squared," while MAE and RMSE are in the "original units" of the target variable.

## Diagram Recreation Prompt
Create a clean, professional educational slide titled "Evaluation Metrics for Regression." 
- Use a white background with a modern blue and grey color scheme.
- Present the five metrics (MSE, MAE, RMSE, R-Squared, Adjusted R-Squared) as distinct cards or boxes arranged in a 2-column grid.
- Inside each box, include the name in bold blue, a short 1-sentence definition, and the standard mathematical formula (e.g., $MSE = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$).
- Use icons next to each title: a "squared" symbol for MSE, an "absolute value" symbol for MAE, a "square root" symbol for RMSE, and a "percentage/gauge" icon for the R-squared metrics.
- Ensure high contrast and clear typography.

## Diagram Data
*   **Title:** Evaluation Metrics
*   **Intro Text:** Measures used to determine the strength and accuracy of linear regression models.
*   **List Items:**
    1.  **Mean Squared Error (MSE):** Average of squared differences; avoids error cancellation.
    2.  **Mean Absolute Error (MAE):** Average of absolute differences; measures basic accuracy.
    3.  **Root Mean Squared Error (RMSE):** Square root of MSE; represents absolute fit in original units.
    4.  **R-Squared:** Proportion of variance explained (typically 0 to 1).
    5.  **Adjusted R-square:** Variance explained adjusted for the number of predictors; penalizes irrelevant features.
