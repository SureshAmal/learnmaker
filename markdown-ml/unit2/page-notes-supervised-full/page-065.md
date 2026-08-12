# Unit 1 Page 65 Image Understanding

## Page Overview
The purpose of this slide is to introduce **Accuracy** as a fundamental performance metric in machine learning. It provides a plain-language definition, the formal mathematical formula based on confusion matrix components, and a step-by-step numerical example to demonstrate how to calculate it.

## Visible Text
*   **Performance Metrics** (Title)
*   **1. Accuracy**
*   **How many predictions were correct?**
*   **Formula:**
    $$Accuracy = \frac{TP + TN}{TP + TN + FP + FN}$$
*   **Calculation Example:**
    $$= \frac{35 + 50}{35 + 50 + 10 + 5} = \frac{85}{100} = 85\%$$

## Visual Layout
*   **Header:** The title "Performance Metrics" is positioned at the top center in a large, bold, black sans-serif font. To its left is a thick, dark red arrow pointing towards the title.
*   **Background:** The slide has a light gradient background (white to pale green) with thin, wispy brown curved lines on the far left side.
*   **Content Box:** The main information is enclosed within a large white rectangular box with a thin black border, centered on the page.
*   **Text Alignment:** The heading "1. Accuracy" and the descriptive question are left-aligned within the box. The mathematical formula and the subsequent calculation steps are centered horizontally.
*   **Visual Hierarchy:** The title is the most prominent element, followed by the specific metric name ("Accuracy"). The formula and calculation are the core technical content, presented clearly in the center.

## Diagram Type
This slide features a **formula derivation and calculation block**. It is not a graphical diagram but a structured mathematical presentation designed to teach a specific calculation method.

## Diagram / Visual Explanation
The central visual element is the mathematical progression:
1.  **Symbolic Representation:** It starts with the general formula for Accuracy using standard machine learning abbreviations ($TP, TN, FP, FN$).
2.  **Substitution:** The next line replaces these symbols with specific numerical values ($35, 50, 10, 5$).
3.  **Simplification:** The third step shows the sum of the numerator ($85$) and the denominator ($100$).
4.  **Final Result:** The last step converts the fraction into a final percentage ($85\%$).

## Math / Formula / Curve Notes
The formula defines **Accuracy** using the four components of a confusion matrix:
*   **$TP$ (True Positives):** The number of positive instances correctly predicted as positive. (Value in example: $35$)
*   **$TN$ (True Negatives):** The number of negative instances correctly predicted as negative. (Value in example: $50$)
*   **$FP$ (False Positives):** The number of negative instances incorrectly predicted as positive (Type I error). (Value in example: $10$)
*   **$FN$ (False Negatives):** The number of positive instances incorrectly predicted as negative (Type II error). (Value in example: $5$)
*   **Numerator ($TP + TN$):** Represents the total count of all correct predictions made by the model.
*   **Denominator ($TP + TN + FP + FN$):** Represents the total number of all predictions made (the total size of the dataset).
*   **Calculation:** The example shows that out of $100$ total cases, the model got $85$ right, resulting in an accuracy of $0.85$ or $85\%$.

## Table Description
No table is visible on this page.

## Concept Explanation
**Accuracy** is the most intuitive performance measure for classification models. It is simply a ratio of correctly predicted observations to the total observations. 

*   **When to use:** It is a great metric when you have a **balanced dataset**, meaning the number of samples in each class is roughly equal.
*   **Limitations:** Accuracy can be highly misleading if the dataset is **imbalanced**. For example, if $99\%$ of your data belongs to Class A, a model that simply predicts "Class A" every single time will achieve $99\%$ accuracy, even though it completely fails to identify Class B. In such cases, other metrics like Precision, Recall, or F1-Score are necessary.

## Exam / Viva Points
*   **Definition:** Accuracy is the ratio of correct predictions to the total number of input samples.
*   **Formula:** $Accuracy = \frac{TP + TN}{Total\ Samples}$.
*   **Components:** Be prepared to define $TP, TN, FP,$ and $FN$.
*   **Interpretation:** An accuracy of $85\%$ means the model correctly classified $85$ out of every $100$ instances.
*   **Critical Thinking:** Why is accuracy not always the best metric? (Answer: Class imbalance issues).

## Diagram Recreation Prompt
Create a clean educational slide titled "Performance Metrics: Accuracy". 
- Use a professional white background with a subtle blue header bar.
- Place the text "1. Accuracy" in a bold sub-header.
- Below it, add the text "Definition: The proportion of total predictions that were correct."
- Create a centered, highlighted box containing the LaTeX formula: $Accuracy = \frac{TP + TN}{TP + TN + FP + FN}$.
- Below the formula, show a clear step-by-step example: 
  - "Example: $TP=35, TN=50, FP=10, FN=5$"
  - "$Accuracy = \frac{35 + 50}{35 + 50 + 10 + 5} = \frac{85}{100} = 85\%$"
- Use high-contrast black text on a white background for maximum readability.

## Diagram Data
*   **Title:** Performance Metrics
*   **Section:** 1. Accuracy
*   **Question:** How many predictions were correct?
*   **Formula Components:**
    *   Numerator: $TP + TN$
    *   Denominator: $TP + TN + FP + FN$
*   **Example Values:**
    *   $TP = 35$
    *   $TN = 50$
    *   $FP = 10$
    *   $FN = 5$
*   **Result:** $85/100 = 85\%$
