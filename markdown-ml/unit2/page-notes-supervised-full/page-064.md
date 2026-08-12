# Unit 1 Page 64 Image Understanding

## Page Overview
The purpose of this slide is to define and illustrate the four fundamental components of a confusion matrix used in binary classification: **True Positive (TP)**, **True Negative (TN)**, **False Positive (FP)**, and **False Negative (FN)**. It uses a practical "Spam Detection" scenario to make these abstract machine-learning concepts relatable and easy to understand for students.

## Visible Text
*   **Title:** Understanding Each Term
*   **Table Headers:** Term, Meaning, Example
*   **Row 1:**
    *   **Term:** True Positive (TP)
    *   **Meaning:** Model correctly predicts Spam
    *   **Example:** 35 spam emails correctly identified as spam
*   **Row 2:**
    *   **Term:** True Negative (TN)
    *   **Meaning:** Model correctly predicts Not Spam
    *   **Example:** 50 normal emails correctly identified
*   **Row 3:**
    *   **Term:** False Positive (FP)
    *   **Meaning:** Model predicts Spam but email is actually Not Spam
    *   **Example:** 10 normal emails marked as spam
*   **Row 4:**
    *   **Term:** False Negative (FN)
    *   **Meaning:** Model predicts Not Spam but email is actually Spam
    *   **Example:** 5 spam emails missed

## Visual Layout
*   **Title:** Positioned at the top center in a large, bold, red sans-serif font.
*   **Background:** A light greenish-beige gradient background with abstract, thin brown curved lines on the left side. A thick red arrow-like block points from the left margin toward the title.
*   **Table Structure:** A large 3-column by 5-row table (including the header) dominates the center and bottom of the slide.
*   **Color Coding:**
    *   **Headers:** Purple text.
    *   **"True" Terms:** The words "True Positive" and "True Negative" use a light blue/teal color for "True".
    *   **"False" Terms:** The words "False Positive" and "False Negative" use a red color for "False".
*   **Alignment:** Text within the table is left-aligned. Headers are centered vertically within their cells.

## Diagram Type
**Table.** This is a comparison and definition table. It is used to organize categorical information (the four classification outcomes) against their definitions and practical applications.

## Diagram / Visual Explanation
The table serves as a lookup guide for classification performance metrics:
1.  **Vertical Organization:** Each row represents one of the four possible outcomes when a model makes a prediction against the actual ground truth.
2.  **Horizontal Organization:**
    *   **Term Column:** Provides the technical name and its standard abbreviation.
    *   **Meaning Column:** Explains the logic behind the term (Prediction vs. Reality).
    *   **Example Column:** Provides concrete numbers (35, 50, 10, 5) in a spam filter context to show how these terms translate to real-world data.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page. However, the numerical values provided in the "Example" column are the raw data points that would typically be plugged into formulas for Accuracy, Precision, Recall, and F1-Score.

## Table Description
| Term | Meaning | Example (Spam Filter) |
| :--- | :--- | :--- |
| **True Positive (TP)** | Correct prediction of the positive class (Spam). | 35 spam emails correctly caught. |
| **True Negative (TN)** | Correct prediction of the negative class (Not Spam). | 50 normal emails correctly left in the inbox. |
| **False Positive (FP)** | Incorrect prediction of the positive class (Type I Error). | 10 normal emails wrongly sent to the spam folder. |
| **False Negative (FN)** | Incorrect prediction of the negative class (Type II Error). | 5 spam emails that "leaked" into the main inbox. |

**Conclusion:** The table highlights that "True" indicates a correct prediction, while "False" indicates an error. "Positive" and "Negative" refer to the model's prediction, not necessarily a "good" or "bad" outcome.

## Concept Explanation
In binary classification, we evaluate how well a model distinguishes between two classes (e.g., "Spam" vs. "Not Spam").
*   **True Positive (TP):** The model said "Yes" (Spam), and it was right. This is a success.
*   **True Negative (TN):** The model said "No" (Not Spam), and it was right. This is also a success.
*   **False Positive (FP):** Also known as a **Type I Error**. The model gave a "False Alarm." It predicted the positive class when it shouldn't have. In spam filtering, this is very bad because important emails are hidden from the user.
*   **False Negative (FN):** Also known as a **Type II Error**. The model "missed" the target. It predicted the negative class for something that was actually positive. In spam filtering, this is an annoyance (spam in the inbox), but in medical diagnosis, this can be life-threatening (missing a disease).

## Exam / Viva Points
*   **Define the four terms:** Be ready to explain TP, TN, FP, and FN using the "Prediction vs. Reality" logic.
*   **Type I vs. Type II Error:** Identify that FP is Type I and FN is Type II.
*   **Contextual Importance:** Be prepared to discuss which error is worse in different scenarios. (e.g., In a spam filter, FP is usually worse; in a cancer test, FN is much worse).
*   **Confusion Matrix Structure:** Understand that these four values are the contents of a 2x2 Confusion Matrix.

## Diagram Recreation Prompt
Create a clean, professional educational slide titled "Understanding Each Term" in bold red. Below the title, insert a 3-column table with the headers "Term", "Meaning", and "Example". Use a light, modern color palette. 
- Header row: Purple text, light grey background.
- Row 1: "True Positive (TP)" (True in blue), "Model correctly predicts Spam", "35 spam emails correctly identified as spam".
- Row 2: "True Negative (TN)" (True in blue), "Model correctly predicts Not Spam", "50 normal emails correctly identified".
- Row 3: "False Positive (FP)" (False in red), "Model predicts Spam but email is actually Not Spam", "10 normal emails marked as spam".
- Row 4: "False Negative (FN)" (False in red), "Model predicts Not Spam but email is actually Spam", "5 spam emails missed".
Ensure high contrast and clear borders between cells.

## Diagram Data
*   **Title:** Understanding Each Term
*   **Headers:** ["Term", "Meaning", "Example"]
*   **Data Rows:**
    1. ["True Positive (TP)", "Model correctly predicts Spam", "35 spam emails correctly identified as spam"]
    2. ["True Negative (TN)", "Model correctly predicts Not Spam", "50 normal emails correctly identified"]
    3. ["False Positive (FP)", "Model predicts Spam but email is actually Not Spam", "10 normal emails marked as spam"]
    4. ["False Negative (FN)", "Model predicts Not Spam but email is actually Spam", "5 spam emails missed"]
