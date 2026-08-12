# Unit 1 Page 56 Image Understanding

## Page Overview
The purpose of this slide is to introduce the concept of **Label Encoding**, a fundamental data preprocessing step in machine learning. It demonstrates how categorical text data (like gender) is transformed into numerical values (integers) so that mathematical models can process the information.

## Visible Text
*   **Title:** C. Encoding Categorical Data
*   **Table Headers:** Gender, Label Encoding
*   **Table Content:**
    *   Male | 0
    *   Female | 1

## Visual Layout
*   **Background:** A light blue gradient background featuring abstract, dark blue curved lines on the left side.
*   **Title Position:** Located at the top left, written in a bold, bright blue sans-serif font.
*   **Main Content:** A centrally placed two-column table.
*   **Table Styling:**
    *   **Header Row:** Dark charcoal gray background with lime green text.
    *   **Data Rows:** Alternating backgrounds of light gray (for "Male") and off-white (for "Female").
    *   **Text Font:** The data inside the table uses a black, serif font (resembling Times New Roman), contrasting with the sans-serif title.
*   **Decorative Element:** A black horizontal arrow-like shape points inward from the far left edge, aligned with the title area.

## Diagram Type
**Table.**
This is a simple mapping table used to illustrate the transformation of categorical labels into numerical representations.

## Diagram / Visual Explanation
The table serves as a direct mapping guide:
1.  **Input Column (Gender):** Contains the original categorical labels "Male" and "Female".
2.  **Output Column (Label Encoding):** Shows the resulting numerical values after the encoding process.
3.  **Mapping:** The label "Male" is assigned the integer **0**, and the label "Female" is assigned the integer **1**. This conversion is necessary because most machine learning algorithms cannot operate directly on strings.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page.

## Table Description
| Gender | Label Encoding |
| :--- | :--- |
| Male | 0 |
| Female | 1 |

*   **Columns:** The first column represents the categorical feature, and the second column represents the encoded numerical feature.
*   **Rows:** Each row represents a unique category and its corresponding integer mapping.
*   **Conclusion:** The table illustrates a binary encoding where two categories are mapped to 0 and 1.

## Concept Explanation
**Label Encoding** is a technique used in the data preprocessing phase of a machine learning pipeline. 
*   **Why it's needed:** Machine learning models are essentially mathematical equations that require numerical input. They cannot perform calculations on words like "Male" or "Female".
*   **How it works:** It assigns a unique integer to each category in a feature. Usually, this is done alphabetically (e.g., Female=0, Male=1) or based on the order of appearance.
*   **Limitation:** A potential drawback of Label Encoding is that models might mistakenly interpret the numerical values as having an inherent order or rank (e.g., thinking 1 is "greater than" or "better than" 0), which is not true for nominal data like gender.

## Exam / Viva Points
*   **Definition:** Label Encoding converts categorical labels into numerical integers.
*   **Use Case:** It is typically used for the target variable (y) or for ordinal features where a natural ranking exists.
*   **Difference from One-Hot Encoding:** Unlike One-Hot Encoding, which creates new binary columns for each category, Label Encoding keeps the data in a single column but changes the format to integers.
*   **Key Mapping:** In this specific example, Male is mapped to 0 and Female is mapped to 1.

## Diagram Recreation Prompt
Create a slide titled "C. Encoding Categorical Data" in bold blue text. Below the title, place a clean, professional table with two columns: "Gender" and "Label Encoding". The header row should have a dark gray background with bright green text. The first data row should have a light gray background with the text "Male" and "0". The second data row should have a white background with the text "Female" and "1". Use a serif font for the table data. The background of the slide should be a soft light-blue gradient.

## Diagram Data
*   **Title:** C. Encoding Categorical Data
*   **Table Data:**
    *   Header: ["Gender", "Label Encoding"]
    *   Row 1: ["Male", "0"]
    *   Row 2: ["Female", "1"]
*   **Colors:** 
    *   Title: #00AEEF (Bright Blue)
    *   Header BG: #333333 (Dark Gray)
    *   Header Text: #92D050 (Lime Green)
    *   Row 1 BG: #D9D9D9 (Light Gray)
    *   Row 2 BG: #FFFFFF (White)
