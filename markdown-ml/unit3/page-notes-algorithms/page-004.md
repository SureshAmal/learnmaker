# Unit 1 Page 4 Image Understanding

## Page Overview
This slide serves as a high-level overview and table of contents for the second section of a machine learning course, titled **"Performance Metrics."** Its purpose is to categorize and list the various quantitative measures used to evaluate the effectiveness of different types of machine learning models, specifically grouping them into Classification, Regression, and Ranking/Recommendation tasks.

## Visible Text
*   **2. Performance Metrics**
*   **For Classification**
    *   Accuracy, Precision, Recall, F1-score
    *   Confusion matrix
    *   ROC curve, AUC
*   **For Regression**
    *   Mean Squared Error (MSE), Root Mean Squared Error (RMSE)
    *   Mean Absolute Error (MAE)
    *   R² score (coefficient of determination)
*   **For Ranking/Recommendation**
    *   Precision@k, Recall@k, MAP, NDCG

## Visual Layout
*   **Title:** The title "2. Performance Metrics" is prominently placed at the top, rendered in a large, bold, blue sans-serif font.
*   **Background:** The background features a light green to white gradient. On the left side, there are decorative, thin, brown curved lines that resemble blades of grass or abstract waves.
*   **Content Alignment:** The main content is a bulleted list aligned to the left.
*   **Bullet Points:** 
    *   Primary categories (Classification, Regression, Ranking/Recommendation) are marked with a solid, dark red/brown square bullet.
    *   Specific metrics under each category are indented and marked with a smaller, hollow square bullet.
*   **Decorative Element:** A solid dark red arrow-like shape is positioned on the far left edge, pointing towards the title.
*   **Hierarchy:** The slide uses font size, bolding, and indentation to create a clear visual hierarchy, separating the main task types from the specific metrics associated with them.

## Diagram Type
This is a **text-only list slide**. It uses a structured hierarchical list to organize information rather than a flowchart, graph, or complex diagram.

## Diagram / Visual Explanation
No diagram is present on this page. The visual structure is purely a hierarchical list of text items.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page. The slide only lists the names and acronyms of various mathematical metrics.

## Table Description
No table is visible on this page.

## Concept Explanation
Performance metrics are essential tools in machine learning used to quantify how well a model is performing. Because different machine learning tasks have different goals, the metrics used to evaluate them also differ:

1.  **Classification Metrics:** Used when the model predicts discrete categories (e.g., "spam" or "not spam").
    *   **Accuracy:** The ratio of correct predictions to total predictions.
    *   **Precision/Recall/F1-score:** Metrics that provide a more nuanced view, especially for imbalanced datasets, focusing on the quality of positive predictions and the ability to find all positive instances.
    *   **Confusion Matrix:** A table used to describe the performance of a classification model by showing true vs. predicted labels.
    *   **ROC/AUC:** Tools to evaluate the performance of a classifier across different decision thresholds.

2.  **Regression Metrics:** Used when the model predicts continuous numerical values (e.g., predicting house prices).
    *   **MSE/RMSE/MAE:** These measure the "error" or distance between the predicted value and the actual value. MSE and RMSE penalize larger errors more heavily.
    *   **R² Score:** Indicates the proportion of the variance in the dependent variable that is predictable from the independent variables.

3.  **Ranking/Recommendation Metrics:** Used when the order of items is important (e.g., search engine results or movie recommendations).
    *   **Precision@k / Recall@k:** Measures accuracy within the top 'k' results.
    *   **MAP (Mean Average Precision) & NDCG (Normalized Discounted Cumulative Gain):** Advanced metrics that account for the specific rank/position of relevant items in a list.

## Exam / Viva Points
*   **Categorization:** Be able to identify which metrics belong to which task type (Classification vs. Regression vs. Ranking).
*   **Classification Basics:** Define Accuracy, Precision, and Recall and explain why Accuracy alone might be misleading (e.g., in imbalanced datasets).
*   **Regression Basics:** Explain the difference between MSE and MAE (MSE squares the error, making it more sensitive to outliers).
*   **Ranking Basics:** Understand that for recommendation systems, the position of a correct item in a list matters, which is why metrics like NDCG are used.
*   **R² Interpretation:** Know that R² (Coefficient of Determination) represents the goodness of fit of a regression model.

## Diagram Recreation Prompt
Create a clean, professional educational slide titled "2. Performance Metrics" using a modern sans-serif font. 
- **Layout:** Use a three-column layout or three distinct colored boxes to separate the categories.
- **Column 1 (Classification):** Use a light blue background. List: Accuracy, Precision, Recall, F1-score, Confusion matrix, ROC curve, AUC. Add a small "check-mark" icon.
- **Column 2 (Regression):** Use a light orange background. List: Mean Squared Error (MSE), Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), R² score. Add a small "line graph" icon.
- **Column 3 (Ranking/Recommendation):** Use a light purple background. List: Precision@k, Recall@k, MAP, NDCG. Add a small "numbered list" icon.
- **Style:** Use dark grey text for readability. Ensure the title is large and bold at the top. The overall design should be spacious and minimalist.

## Diagram Data
*   **Title:** 2. Performance Metrics
*   **Section 1: For Classification**
    *   Metric 1: Accuracy, Precision, Recall, F1-score
    *   Metric 2: Confusion matrix
    *   Metric 3: ROC curve, AUC
*   **Section 2: For Regression**
    *   Metric 1: Mean Squared Error (MSE), Root Mean Squared Error (RMSE)
    *   Metric 2: Mean Absolute Error (MAE)
    *   Metric 3: R² score (coefficient of determination)
*   **Section 3: For Ranking/Recommendation**
    *   Metric 1: Precision@k, Recall@k, MAP, NDCG
