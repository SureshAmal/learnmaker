# Unit 1 Page 4 Image Understanding

## Page Overview
This slide serves as a high-level categorization of performance metrics used in machine learning. It organizes various evaluation methods into three primary task domains: Classification, Regression, and Ranking/Recommendation. The purpose is to provide a roadmap of the specific metrics that will likely be discussed in detail later in the course module.

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
*   **Title:** The title "2. Performance Metrics" is positioned at the top, rendered in a large, bold, blue sans-serif font.
*   **Background:** A light, pale-green gradient background. On the left side, there are abstract, thin brown curved lines that resemble blades of grass or stylized stalks.
*   **Graphic Element:** A thick, solid brown arrow-like shape points from the far left margin toward the start of the title.
*   **Content Structure:** The information is presented as a nested bulleted list. 
    *   Main categories ("For Classification", "For Regression", "For Ranking/Recommendation") are preceded by a hollow square bullet and are written in a bold, dark grey font.
    *   Specific metrics are indented under their respective categories, also preceded by hollow square bullets, and written in a regular weight dark grey font.
*   **Alignment:** The text is left-aligned, creating a clear vertical hierarchy.

## Diagram Type
This is a **text-only slide** organized as a hierarchical list. It does not contain flowcharts, graphs, or architectural diagrams. Its function is to provide a structured outline of topics.

## Diagram / Visual Explanation
While not a diagram, the visual hierarchy is established through indentation and font weight:
1.  **Primary Level (Bold):** Defines the machine learning task type (Classification, Regression, Ranking).
2.  **Secondary Level (Regular):** Lists the specific mathematical or statistical tools used to measure performance for that task.
The brown arrow on the left acts as a visual anchor, drawing the eye to the start of the section.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page. The slide lists the names of formulas (like MSE, R²) but does not show the equations themselves.

## Table Description
No table is visible on this page.

## Concept Explanation
The slide categorizes how we measure the "success" of a machine learning model based on the type of problem it solves:

*   **Classification:** Used when the output is a discrete label (e.g., Spam vs. Not Spam). 
    *   *Accuracy* is the simplest metric (correct/total). 
    *   *Precision, Recall, and F1-score* are used to handle class imbalances and trade-offs between false positives and false negatives. 
    *   *Confusion Matrix* provides a detailed breakdown of correct and incorrect predictions for each class. 
    *   *ROC/AUC* evaluates the model's ability to distinguish between classes across different decision thresholds.
*   **Regression:** Used when the output is a continuous numerical value (e.g., predicting house prices). 
    *   *MSE and RMSE* penalize larger errors more heavily by squaring them. 
    *   *MAE* provides a linear average of the error magnitude. 
    *   *R² score* indicates the proportion of variance in the dependent variable that is predictable from the independent variables.
*   **Ranking/Recommendation:** Used when the order of results matters (e.g., search engine results or movie suggestions). 
    *   *Precision@k and Recall@k* measure quality within the top 'k' results. 
    *   *MAP (Mean Average Precision)* and *NDCG (Normalized Discounted Cumulative Gain)* are sophisticated metrics that account for the specific position of relevant items in the list.

## Exam / Viva Points
*   **Categorization:** Be able to list which metrics belong to which ML task (e.g., "Is MSE used for classification or regression?").
*   **Classification Metrics:** Know the four basic components of a confusion matrix (TP, TN, FP, FN) and how they relate to Precision and Recall.
*   **Regression Metrics:** Understand the difference between MSE and MAE (MSE is more sensitive to outliers).
*   **Ranking Metrics:** Explain what the "@k" signifies in Precision@k (it refers to evaluating only the top 'k' items in a ranked list).
*   **R² Score:** Remember that R² is also known as the "coefficient of determination" and measures the goodness of fit.

## Diagram Recreation Prompt
Create a clean, professional presentation slide titled "Performance Metrics" in large blue text. Use a three-column layout to categorize metrics. 
- **Column 1 (Classification):** List Accuracy, Precision, Recall, F1-score, Confusion matrix, ROC curve, and AUC. Use a distinct icon like a checkmark/cross.
- **Column 2 (Regression):** List MSE, RMSE, MAE, and R² score. Use a distinct icon like a line graph.
- **Column 3 (Ranking/Recommendation):** List Precision@k, Recall@k, MAP, and NDCG. Use a distinct icon like a star or a list.
Use a light, neutral background (off-white or very light grey) with professional sans-serif typography. Ensure clear spacing between columns.

## Diagram Data
*   **Title:** 2. Performance Metrics
*   **Section 1: For Classification**
    *   Item 1: Accuracy, Precision, Recall, F1-score
    *   Item 2: Confusion matrix
    *   Item 3: ROC curve, AUC
*   **Section 2: For Regression**
    *   Item 1: Mean Squared Error (MSE), Root Mean Squared Error (RMSE)
    *   Item 2: Mean Absolute Error (MAE)
    *   Item 3: R² score (coefficient of determination)
*   **Section 3: For Ranking/Recommendation**
    *   Item 1: Precision@k, Recall@k, MAP, NDCG
