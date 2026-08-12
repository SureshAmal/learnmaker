# Unit 1 Page 19 Image Understanding

## Page Overview
The purpose of this slide is to introduce and define the primary **Evaluation Metrics** used to assess the performance and accuracy of linear regression models. It provides a high-level overview of five key statistical measures: Mean Squared Error (MSE), Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), R-Squared, and Adjusted R-Squared.

## Visible Text
*   **Title:** Evaluation Metrics
*   **Introductory Text:** A variety of evaluation measures can be used to determine the strength of any linear regression model. These assessment metrics often give an indication of how well the model is producing the observed outputs.
*   **Numbered List:**
    1.  **Mean Squared Error (MSE):** Measures the average squared difference between actual and predicted values to avoid cancellation of errors.
    2.  **Mean Absolute Error (MAE):** Calculate the accuracy of a regression model. MAE measures the average absolute difference between the predicted values and actual values.
    3.  **Root Mean Squared Error (RMSE):** Square root of the residuals variance is RMSE. It describes how well the observed data points match the expected values or the model's absolute fit to the data.
    4.  **R-Squared:** Indicates how much variation the model explains. Its value is typically between 0 and 1, but it can be negative if the model performs worse than a simple baseline model (e.g., predicting the mean).
    5.  **Adjusted R-square:** Measures the proportion of variance explained by the model while adjusting for the number of predictors and penalizing irrelevant features.

## Visual Layout
*   **Title Position:** Top center, rendered in a large, bold, green sans-serif font.
*   **Background:** A light gradient background (pale green/yellow) featuring abstract, thin brown curved lines on the left side.
*   **Decorative Element:** A thick, dark brown horizontal arrow-like shape points from the left margin toward the start of the introductory text.
*   **Content Block:** The main body consists of a paragraph of introductory text followed by a numbered list of five items.
*   **Typography:** The body text uses a black serif font. The names of the metrics in the list are underlined and colored in a dark teal/green shade to distinguish them as key terms.
*   **Alignment:** The text is left-aligned with standard indentation for the numbered list.

## Diagram Type
This is a **text-only slide** organized as a numbered list. It serves as a glossary or a conceptual overview page rather than a visual representation of data or a process flow.

## Diagram / Visual Explanation
No diagram is present on this page. The visual elements (curved lines and the brown arrow) are purely decorative and do not convey specific technical information.

## Math / Formula / Curve Notes
No mathematical formulas or curves are visible on this page. While the text describes mathematical operations (squaring differences, taking square roots, calculating proportions of variance), the actual equations (e.g., $MSE = \frac{1}{n} \sum (y - \hat{y})^2$) are not shown.

## Table Description
No table is visible on this page.

## Concept Explanation
The slide explains how to measure the "goodness of fit" for a regression model:
*   **Error-Based Metrics (MSE, MAE, RMSE):** These focus on the "residuals" (the distance between the actual data point and the model's prediction). 
    *   **MSE** squares these distances to ensure positive and negative errors don't cancel out and to penalize large outliers more heavily.
    *   **MAE** uses absolute values, providing a more linear representation of error that is less sensitive to outliers than MSE.
    *   **RMSE** is the square root of MSE, which brings the error metric back into the original units of the target variable, making it easier to interpret.
*   **Variance-Based Metrics (R-Squared, Adjusted R-Squared):** These focus on how much of the data's total "spread" or "variance" is captured by the model.
    *   **R-Squared** tells you the percentage of variance explained. A value of 0.8 means the model explains 80% of the variation in the data.
    *   **Adjusted R-Squared** is a more sophisticated version used in multiple regression. It prevents "overfitting" by penalizing the score if you add variables that don't actually improve the model's predictive power.

## Exam / Viva Points
*   **MSE vs. MAE:** Be prepared to explain why MSE is often preferred in optimization (it's differentiable) but MAE is more robust to outliers.
*   **Why square the errors?** To prevent positive and negative errors from canceling each other out and to emphasize larger errors.
*   **Interpreting R-Squared:** Know that R-squared ranges from 0 to 1 (usually), where 1 is a perfect fit. Explain that a negative R-squared means the model is performing worse than just guessing the average value of the data.
*   **The "Penalty" in Adjusted R-Squared:** Understand that Adjusted R-squared will decrease if you add a predictor that does not improve the model significantly, unlike standard R-squared which always stays the same or increases when more variables are added.
*   **RMSE Units:** Remember that RMSE is in the same units as the dependent variable ($y$), whereas MSE is in units squared ($y^2$).

## Diagram Recreation Prompt
Create a professional educational slide titled "Evaluation Metrics for Regression". Use a clean white background with a dark green header. Divide the content into two columns. In the left column, list "Error-Based Metrics" with sub-points for MSE, MAE, and RMSE, including a small icon of a ruler for each. In the right column, list "Variance-Based Metrics" with sub-points for R-Squared and Adjusted R-Squared, including a small icon of a percentage sign. Use a modern sans-serif font like Roboto or Arial. Add a small "Note" box at the bottom explaining that Adjusted R-Squared penalizes model complexity.

## Diagram Data
*   **Title:** Evaluation Metrics
*   **Section 1: Error Metrics**
    *   MSE: Average squared difference.
    *   MAE: Average absolute difference.
    *   RMSE: Square root of MSE; absolute fit.
*   **Section 2: Variance Metrics**
    *   R-Squared: Proportion of variance explained (0 to 1).
    *   Adjusted R-square: Variance explained adjusted for number of predictors.
