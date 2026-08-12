# Unit 1 Page 72 Image Understanding

## Page Overview
The purpose of this slide is to provide a relatable, real-world example to explain the four fundamental outcomes of a binary classification model: **True Positive (TP)**, **True Negative (TN)**, **False Positive (FP)**, and **False Negative (FN)**. By using a COVID-19 test scenario, it helps students intuitively understand the difference between correct predictions and different types of errors.

## Visible Text
*   **Title:** Imagine a COVID test :
*   **1. TP:** Sick person → Test says **Sick** ✅
*   **2. TN:** Healthy person → Test says **Healthy** ✅
*   **3. FP:** Healthy person → Test says **Sick** ❌ (False Alarm)
*   **4. FN:** Sick person → Test says **Healthy** ❌ (Missed Case)

## Visual Layout
*   **Title Position:** The title is centered at the top in large, bold, red font.
*   **Content Blocks:** The main content is a numbered list of four items, left-aligned.
*   **Colors:** 
    *   The background is a light green gradient.
    *   The title is red.
    *   The numbers (1-4) are dark red.
    *   The abbreviations (TP, TN, FP, FN) and the test results (Sick, Healthy) are in bold black.
    *   Correct outcomes are marked with a green square icon containing a white checkmark.
    *   Incorrect outcomes are marked with a large red 'X' icon.
*   **Visual Hierarchy:** The title draws immediate attention, followed by the numbered list. The use of icons (✅ and ❌) provides a quick visual indicator of success versus error.
*   **Decorative Elements:** A thick dark red arrow points from the left margin toward the title. Abstract, thin curved lines are visible on the left side of the background.

## Diagram Type
This is a **text-based list with icons**. It functions as a conceptual mapping diagram, translating abstract machine learning terms into a concrete scenario. It is not a formal flowchart or graph but uses arrows to show the relationship between the actual state and the predicted result.

## Diagram / Visual Explanation
The slide maps the "Actual State" of a person to the "Predicted State" (the test result):
1.  **TP (True Positive):** The person is actually sick, and the test correctly identifies them as sick. This is a correct prediction (✅).
2.  **TN (True Negative):** The person is actually healthy, and the test correctly identifies them as healthy. This is a correct prediction (✅).
3.  **FP (False Positive):** The person is actually healthy, but the test incorrectly says they are sick. This is an error (❌), commonly called a **"False Alarm."**
4.  **FN (False Negative):** The person is actually sick, but the test incorrectly says they are healthy. This is an error (❌), commonly called a **"Missed Case."**

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page. It introduces the components (TP, TN, FP, FN) that are used to calculate metrics like Accuracy, Precision, and Recall.

## Table Description
No table is visible on this page.

## Concept Explanation
In binary classification, a model predicts one of two classes (Positive or Negative). The performance of such a model is evaluated by comparing its predictions against the ground truth (the actual reality).
*   **True (T):** The model's prediction matches reality.
*   **False (F):** The model's prediction is wrong.
*   **Positive (P):** The model predicted the presence of a condition (e.g., "Sick").
*   **Negative (N):** The model predicted the absence of a condition (e.g., "Healthy").

Combining these gives the four outcomes:
*   **True Positive (TP):** Correctly predicted the positive class.
*   **True Negative (TN):** Correctly predicted the negative class.
*   **False Positive (FP):** Incorrectly predicted the positive class (Type I Error).
*   **False Negative (FN):** Incorrectly predicted the negative class (Type II Error). In medical contexts, FN is often more dangerous because a sick individual remains untreated.

## Exam / Viva Points
*   **Definitions:** Be able to define TP, TN, FP, and FN using the COVID test example.
*   **Type I Error:** Know that a False Positive is also called a Type I Error or a "False Alarm."
*   **Type II Error:** Know that a False Negative is also called a Type II Error or a "Missed Case."
*   **Impact of Errors:** Understand why a False Negative (Missed Case) is typically considered more critical in medical diagnostics than a False Positive (False Alarm).
*   **Correct vs. Incorrect:** Identify that TP and TN represent correct classifications, while FP and FN represent misclassifications.

## Diagram Recreation Prompt
Create a clean, educational slide titled "Binary Classification: COVID Test Example" in bold red. Use a professional light-colored background. List four items vertically with clear spacing:
1. "TP: Sick person → Test says Sick" followed by a green checkmark icon.
2. "TN: Healthy person → Test says Healthy" followed by a green checkmark icon.
3. "FP: Healthy person → Test says Sick" followed by a red 'X' icon and the text "(False Alarm)" in parentheses.
4. "FN: Sick person → Test says Healthy" followed by a red 'X' icon and the text "(Missed Case)" in parentheses.
Bold the abbreviations (TP, TN, FP, FN) and the test results (Sick, Healthy). Ensure all text is left-aligned and easy to read.

## Diagram Data
*   **Title:** Imagine a COVID test :
*   **Item 1:** Label="TP", Actual="Sick person", Prediction="Sick", Status="Correct", Icon="Green Check"
*   **Item 2:** Label="TN", Actual="Healthy person", Prediction="Healthy", Status="Correct", Icon="Green Check"
*   **Item 3:** Label="FP", Actual="Healthy person", Prediction="Sick", Status="Incorrect", Icon="Red X", Alias="False Alarm"
*   **Item 4:** Label="FN", Actual="Sick person", Prediction="Healthy", Status="Incorrect", Icon="Red X", Alias="Missed Case"
