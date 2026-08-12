# Unit 1 Page 70 Image Understanding

## Page Overview
The purpose of this slide is to define and provide numerical examples for the four fundamental outcomes of a binary classification model (Confusion Matrix components) within a healthcare context. It specifically illustrates True Positives (TP), True Negatives (TN), False Positives (FP), and False Negatives (FN) using a hypothetical scenario of diagnosing sick versus healthy patients. The slide concludes by emphasizing the real-world consequence of False Negatives in medical diagnostics.

## Visible Text
*   **1. TP = 90:** Sick patients correctly identified.
*   **2. TN = 85:** Healthy patients correctly identified.
*   **3. FP = 15:** Healthy patients wrongly diagnosed as sick.
*   **4. FN = 10:** Sick patients missed by the model.
*   **In healthcare, False Negatives are often the most dangerous because an infected patient may not receive treatment.**

## Visual Layout
*   **Background:** A light green gradient background with abstract, thin, dark curved lines on the far left side.
*   **Title/Header:** There is no formal title; the content starts directly with a numbered list.
*   **Numbering:** Large, bold, dark red numbers (1 through 4) are used for the list items.
*   **Text Style:** The main text is a dark gray/black serif font. The abbreviations (TP, TN, FP, FN) and their values are bolded.
*   **Visual Cue:** A thick, horizontal dark red arrow points from the left edge of the slide toward the first list item ("1. TP = 90").
*   **Spacing:** The numbered list is vertically stacked with generous line spacing. A concluding paragraph is placed at the bottom, separated by a slightly larger gap.
*   **Alignment:** All text is left-aligned.

## Diagram Type
This is a **text-only slide** with a numbered list. It uses text to describe the components of a confusion matrix rather than a graphical matrix or flowchart.

## Diagram / Visual Explanation
No diagram is present. The visual elements (arrow and curved lines) serve as decorative or directional cues rather than data representations.

## Math / Formula / Curve Notes
While no complex formulas are present, the slide provides the raw counts for a confusion matrix:
*   **TP (True Positives) = 90**: The count of instances where the actual class was "Sick" and the model predicted "Sick".
*   **TN (True Negatives) = 85**: The count of instances where the actual class was "Healthy" and the model predicted "Healthy".
*   **FP (False Positives) = 15**: Also known as a **Type I Error**. The actual class was "Healthy," but the model predicted "Sick."
*   **FN (False Negatives) = 10**: Also known as a **Type II Error**. The actual class was "Sick," but the model predicted "Healthy."
*   **Total Population (N)**: Though not explicitly stated, the total number of patients evaluated is $90 + 85 + 15 + 10 = 200$.

## Table Description
No table is visible on this page.

## Concept Explanation
This slide explains the four possible outcomes when a machine learning model makes a binary prediction (e.g., Sick vs. Healthy):

1.  **True Positive (TP):** The model correctly identifies a positive case (e.g., a sick person is correctly told they are sick).
2.  **True Negative (TN):** The model correctly identifies a negative case (e.g., a healthy person is correctly told they are healthy).
3.  **False Positive (FP):** The model incorrectly flags a negative case as positive. In medicine, this is a "false alarm," leading to unnecessary stress or further testing for a healthy person.
4.  **False Negative (FN):** The model incorrectly flags a positive case as negative. This is the most critical error in healthcare because a sick person is told they are healthy, leading to a lack of necessary treatment and potential worsening of the condition or spread of disease.

## Exam / Viva Points
*   **Define the four components:** Be able to define TP, TN, FP, and FN using the "Actual vs. Predicted" logic.
*   **Type I vs. Type II Error:** Remember that False Positives are Type I errors and False Negatives are Type II errors.
*   **Contextual Risk:** Understand that the "cost" of an error depends on the domain. In healthcare, minimizing False Negatives (increasing Recall/Sensitivity) is usually prioritized over minimizing False Positives.
*   **Calculation:** Be prepared to calculate metrics like Accuracy, Precision, or Recall if given these four values ($TP=90, TN=85, FP=15, FN=10$).

## Diagram Recreation Prompt
Create a professional educational slide on a clean white background. 
- **Title:** "Confusion Matrix Components: Healthcare Example" in bold dark blue.
- **Content:** Create a 2x2 grid (Confusion Matrix) in the center. 
    - Columns labeled "Predicted: Sick" and "Predicted: Healthy". 
    - Rows labeled "Actual: Sick" and "Actual: Healthy".
    - Fill the cells with: TP=90, FN=10, FP=15, TN=85.
- **Side List:** To the right of the grid, list the definitions:
    1. **TP (90):** Sick patients correctly identified.
    2. **TN (85):** Healthy patients correctly identified.
    3. **FP (15):** Healthy patients wrongly diagnosed as sick (Type I Error).
    4. **FN (10):** Sick patients missed by the model (Type II Error).
- **Footer Note:** Add a highlighted box at the bottom with the text: "CRITICAL: In healthcare, False Negatives are the most dangerous as they result in missed treatments." Use a red border for this box to emphasize urgency.

## Diagram Data
*   **Title:** Confusion Matrix Components
*   **List Items:**
    *   Item 1: TP = 90 (True Positive)
    *   Item 2: TN = 85 (True Negative)
    *   Item 3: FP = 15 (False Positive / Type I Error)
    *   Item 4: FN = 10 (False Negative / Type II Error)
*   **Key Insight:** False Negatives are high-risk in medical diagnostics.
