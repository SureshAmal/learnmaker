# Unit 1 Page 67 Image Understanding

## Page Overview
This slide explains the machine learning performance metric **Recall**, also known as **Sensitivity**. Its purpose is to define the metric both conceptually and mathematically using a practical example of spam email detection. It provides a step-by-step calculation to show how the formula is applied to raw data (True Positives and False Negatives).

## Visible Text
*   **3. Recall (Sensitivity)**
*   Out of all actual spam emails, how many were detected?
*   $Recall = \frac{TP}{TP + FN}$
*   $= \frac{35}{35 + 5} = \frac{35}{40} = 87.5\%$

## Visual Layout
*   **Background:** The slide features a light gradient background (pale green to white) with abstract, dark brown curved lines on the far left.
*   **Content Box:** A large white rectangular box with a thin black border contains the primary information.
*   **Title:** The heading "3. Recall (Sensitivity)" is positioned at the top-left inside the white box.
*   **Descriptive Text:** A single sentence explaining the intuition behind the metric is placed directly below the title.
*   **Formula and Calculation:** The mathematical formula and the numerical example are centered vertically and horizontally within the lower half of the white box.
*   **Decorative Element:** A thick, solid brown arrow points from the left edge of the slide toward the main content box.

## Diagram Type
This is a **formula derivation and calculation slide**. It does not contain a complex flowchart or graph but rather uses mathematical notation to define a concept and demonstrates its application through a numerical example.

## Diagram / Visual Explanation
The slide presents a logical progression of information:
1.  **Identification:** It labels the metric as the third in a series (Recall/Sensitivity).
2.  **Intuition:** It asks a guiding question ("Out of all actual spam emails, how many were detected?") to help the student understand the "real-world" meaning of the metric.
3.  **Formalization:** It provides the standard algebraic formula.
4.  **Application:** It substitutes specific values into the formula to arrive at a final percentage, showing the intermediate arithmetic steps.

## Math / Formula / Curve Notes
*   **$Recall$ (Sensitivity):** The ratio of correctly predicted positive observations to all observations in the actual class.
*   **$TP$ (True Positives):** The number of positive instances correctly identified by the model. In this example, $TP = 35$.
*   **$FN$ (False Negatives):** The number of positive instances that the model incorrectly identified as negative (missed detections). In this example, $FN = 5$.
*   **$TP + FN$:** The denominator represents the total number of actual positive cases in the dataset (Total Actual Spam = 40).
*   **Calculation Steps:**
    *   $\frac{35}{35 + 5}$ (Substitution of values)
    *   $\frac{35}{40}$ (Simplification of the denominator)
    *   $87.5\%$ (Final result expressed as a percentage)

## Table Description
No table is visible on this page.

## Concept Explanation
**Recall**, often referred to as **Sensitivity** or the **True Positive Rate (TPR)**, measures the ability of a classification model to identify all relevant instances within a dataset. 

In the context of binary classification (like Spam vs. Not Spam):
*   It focuses on the **Actual Positive** class.
*   It answers the question: "What fraction of the things that are actually positive did we successfully find?"
*   A high recall indicates that the model is very good at capturing the positive class and has a low rate of **False Negatives** (missing actual positive cases).
*   In fields like medicine, high recall (sensitivity) is critical for screening tests to ensure that as few sick patients as possible are missed, even if it means some healthy patients are flagged for further testing.

## Exam / Viva Points
*   **Definition:** Recall is the proportion of actual positives that were correctly identified.
*   **Synonyms:** Sensitivity, True Positive Rate (TPR).
*   **Formula:** $Recall = \frac{TP}{TP + FN}$.
*   **Interpretation:** A recall of 87.5% means the model caught 87.5% of the target class, while 12.5% were missed (False Negatives).
*   **Trade-off:** Recall is often discussed alongside Precision. Improving Recall usually involves lowering the classification threshold, which may decrease Precision (increasing False Positives).
*   **When to prioritize Recall:** Use it when the cost of a False Negative is high (e.g., missing a cancer diagnosis or a fraudulent transaction).

## Diagram Recreation Prompt
Create a clean, professional educational slide titled "Recall (Sensitivity)". 
- **Top Section:** Include the text "Concept: Out of all actual positive cases, how many were correctly detected?"
- **Middle Section:** Display the formula $Recall = \frac{TP}{TP + FN}$ in a large, clear font using LaTeX formatting.
- **Bottom Section:** Show a worked example: "Example (Spam Detection): $TP = 35$, $FN = 5$". Below this, show the calculation steps: "$= \frac{35}{35 + 5} = \frac{35}{40} = 87.5\%$".
- **Styling:** Use a white background with a subtle blue border. Use dark blue for headings and black for formulas. Ensure plenty of white space for readability.

## Diagram Data
*   **Title:** 3. Recall (Sensitivity)
*   **Contextual Question:** Out of all actual spam emails, how many were detected?
*   **Formula:** Recall = TP / (TP + FN)
*   **Example Values:**
    *   True Positives (TP) = 35
    *   False Negatives (FN) = 5
*   **Calculation Result:** 35 / 40 = 0.875 (87.5%)
