# Unit 1 Page 126 Image Understanding

## Page Overview
The purpose of this slide is to provide a high-level overview of the standard workflow or lifecycle involved in building a machine learning regression model. It outlines the sequential process from initial data gathering to the final assessment of the model's performance.

## Visible Text
*   **Title:** Steps in Regression Modeling:
*   **List Items:**
    *   Collect and prepare data
    *   Split data into training and testing sets
    *   Train the regression model
    *   Predict on test data
    *   Evaluate using metrics

## Visual Layout
*   **Title Position:** Located at the top right, styled in a bold, magenta (pinkish-purple) sans-serif font.
*   **Content Blocks:** A single list of five bullet points occupies the central and lower-right portion of the slide.
*   **Colors:** The background features a light blue to white gradient. The text is dark gray/black. A dark gray arrow icon is at the top left.
*   **Graphics:** On the left side, there are several thin, dark blue curved lines that sweep upwards from the bottom corner, serving as a decorative border.
*   **Icons:** Each list item is preceded by a simple square box icon instead of standard circular bullets.
*   **Spacing and Alignment:** The text is left-aligned with generous vertical spacing between the steps to ensure readability.

## Diagram Type
This is a **text-only slide** presenting a list of procedural steps. While it describes a process, it does not use a formal flowchart or architectural diagram to visualize the connections.

## Diagram / Visual Explanation
No diagram is present on this page. The visual elements (curved lines and top arrow) are decorative and do not represent data or logic flow.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page.

## Table Description
No table is visible on this page.

## Concept Explanation
The slide summarizes the **Regression Modeling Pipeline**:

1.  **Collect and prepare data:** This is the foundational step. It involves gathering raw data from various sources and cleaning it. Preparation includes handling missing values, removing outliers, encoding categorical variables, and feature scaling (normalization/standardization) to ensure the data is in a format the algorithm can process effectively.
2.  **Split data into training and testing sets:** To ensure the model can generalize to new, unseen data, the dataset is divided. The **Training Set** is used to teach the model, while the **Testing Set** (which the model never sees during training) is reserved for final evaluation. Common splits are 70/30 or 80/20.
3.  **Train the regression model:** The chosen regression algorithm (e.g., Linear Regression, Decision Tree Regressor) is applied to the training data. The algorithm "learns" the mathematical relationship (weights and biases) between the input features and the continuous target variable.
4.  **Predict on test data:** Once trained, the model is given the input features from the test set. It generates predicted values for the target variable based on what it learned during training.
5.  **Evaluate using metrics:** The predicted values are compared against the actual known values in the test set. Metrics such as Mean Absolute Error (MAE), Mean Squared Error (MSE), or R-squared ($R^2$) are calculated to determine the model's accuracy and error rate.

## Exam / Viva Points
*   **Sequence of Steps:** Be able to list these five steps in the correct chronological order.
*   **Data Splitting Purpose:** Why do we split data? To evaluate the model's ability to generalize to new data and to detect overfitting.
*   **Data Preparation:** What are common tasks in data preparation? (Handling missing values, feature scaling, etc.)
*   **Evaluation Metrics:** Name at least two metrics used specifically for regression (e.g., MSE, RMSE, R-squared).
*   **Training vs. Testing:** Understand that the model parameters are adjusted only during the "Train" phase, never during the "Predict" or "Evaluate" phases on the test set.

## Diagram Recreation Prompt
Create a professional presentation slide titled "Steps in Regression Modeling" in bold magenta. The background should be a clean light blue gradient. On the left, include a decorative element consisting of thin, dark blue curved lines sweeping upward. The main content should be a vertical list of five steps, each preceded by a small square bullet icon. The steps are: 1. Collect and prepare data, 2. Split data into training and testing sets, 3. Train the regression model, 4. Predict on test data, 5. Evaluate using metrics. Use a clear, dark gray serif font for the list items with ample line spacing.

## Diagram Data
*   **Title:** Steps in Regression Modeling:
*   **List Content:**
    1.  Collect and prepare data
    2.  Split data into training and testing sets
    3.  Train the regression model
    4.  Predict on test data
    5.  Evaluate using metrics
*   **Visual Style:** Light blue gradient background, magenta title, dark gray serif body text, square bullet points.
