# Unit 1 Page 68 Image Understanding

## Page Overview
The purpose of this slide is to introduce and define the **F1 Score**, a critical evaluation metric in machine learning. It explains that the F1 Score is used to find a balance between two other metrics: Precision and Recall. The slide provides the standard mathematical formula for the F1 Score and demonstrates its calculation using a numerical example.

## Visible Text
*   **4. F1 Score**
*   **Balances Precision and Recall.**
*   $F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}$
*   $= 2 \times \frac{0.7778 \times 0.875}{0.7778 + 0.875} \approx 82.3\%$

## Visual Layout
*   **Title:** "4. F1 Score" is positioned at the top left of the main content area in a bold, sans-serif font.
*   **Subtext:** A single descriptive sentence, "Balances Precision and Recall.", is placed directly below the title.
*   **Mathematical Content:** The core formula and the worked-out example are centered in the middle of the slide. The math is rendered in a serif font, typical for LaTeX or mathematical notation, making it stand out from the plain text.
*   **Background/Border:** The slide has a white central area surrounded by a thin black border. To the left, there is a decorative background featuring abstract curved lines and a solid dark red rectangular bar at the top.
*   **Hierarchy:** The title is the most prominent element, followed by the descriptive text, with the mathematical formula serving as the primary technical detail.

## Diagram Type
This is a **formula derivation and calculation slide**. It presents a mathematical definition and then applies it to specific data points to show how the metric is computed in practice.

## Diagram / Visual Explanation
While not a graphical diagram, the visual flow of the math is as follows:
1.  **Definition:** The top line of the math block defines the F1 score as a function of Precision and Recall.
2.  **Substitution:** The second line replaces the variable names with specific decimal values ($0.7778$ for Precision and $0.875$ for Recall).
3.  **Result:** The final part of the second line provides the approximate result expressed as a percentage ($82.3\%$).

## Math / Formula / Curve Notes
*   **$F1$:** Represents the F1 Score, which is the harmonic mean of precision and recall.
*   **$Precision$:** The ratio of true positive predictions to the total number of positive predictions made by the model.
*   **$Recall$:** The ratio of true positive predictions to the total number of actual positive instances in the dataset.
*   **The Formula:** $F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}$ is the standard way to calculate the harmonic mean of two values.
*   **Calculation Breakdown:**
    *   Numerator: $0.7778 \times 0.875 = 0.680575$
    *   Denominator: $0.7778 + 0.875 = 1.6528$
    *   Final Step: $2 \times (0.680575 / 1.6528) \approx 2 \times 0.41177 \approx 0.8235$ or $82.3\%$.

## Table Description
No table is visible on this page.

## Concept Explanation
The **F1 Score** is a single-number evaluation metric used primarily in binary classification. 
*   **The Problem:** In many machine learning tasks, there is a trade-off between Precision (being right when you predict "positive") and Recall (finding all the "positive" cases). Improving one often degrades the other.
*   **The Solution:** The F1 Score combines both into a single value. It uses the **harmonic mean** rather than a simple arithmetic average. 
*   **Why Harmonic Mean?** The harmonic mean is sensitive to low values. If either Precision or Recall is very low (close to 0), the F1 Score will also be low, even if the other metric is high. This forces the model to perform well in both areas to achieve a high F1 Score.
*   **Use Case:** It is especially useful for **imbalanced datasets** where one class is much more frequent than the other. In such cases, simple "Accuracy" can be misleadingly high, whereas the F1 Score provides a more honest assessment of model performance on the minority class.

## Exam / Viva Points
*   **Definition:** The F1 Score is the harmonic mean of Precision and Recall.
*   **Formula:** $F1 = \frac{2 \cdot P \cdot R}{P + R}$.
*   **Range:** The score ranges from 0 to 1 (or 0% to 100%), where 1 is perfect precision and recall.
*   **Key Advantage:** It provides a balanced view of model performance, especially when there is an uneven class distribution.
*   **Comparison:** Unlike the arithmetic mean, the F1 score penalizes extreme values. If a model has a Precision of 1.0 but a Recall of 0.0, the arithmetic mean is 0.5, but the F1 score is 0.0.

## Diagram Recreation Prompt
Create a professional educational slide titled "4. F1 Score". 
- At the top left, include the text "Balances Precision and Recall." 
- In the center of the slide, place a large, clear mathematical formula box. 
- Inside the box, display the formula: $F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}$. 
- Directly below this formula, show a worked example: $= 2 \times \frac{0.7778 \times 0.875}{0.7778 + 0.875} \approx 82.3\%$. 
- Use a clean, modern sans-serif font for text and a clear LaTeX-style font for the math. 
- Use a light blue or soft gray background for the formula box to make it pop against a white slide background.

## Diagram Data
*   **Title:** 4. F1 Score
*   **Description:** Balances Precision and Recall.
*   **Formula Components:**
    *   Variable 1: Precision (Value used: 0.7778)
    *   Variable 2: Recall (Value used: 0.875)
    *   Operator: Harmonic Mean ($2 \times \text{Product} / \text{Sum}$)
*   **Calculated Result:** 82.3%
