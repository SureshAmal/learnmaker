# Unit 1 Page 51 Image Understanding

## Page Overview
The purpose of this slide is to introduce **Data Cleaning**, the second major step in the machine learning data preprocessing pipeline. It specifically focuses on the definition of data cleaning and provides a list of common strategies for **Handling Missing Values**, which is a frequent issue in real-world datasets.

## Visible Text
*   **2. Data Cleaning** (Title)
*   Identify and correct errors in the dataset.
*   Handling Missing Values
*   Methods:
    *   Remove records with missing values
    *   Replace with Mean
    *   Replace with Median
    *   Replace with Mode

## Visual Layout
*   **Title:** Positioned at the top left, written in a large, bold, red sans-serif font.
*   **Content Block:** A vertical list of bulleted points aligned to the left. The text is in a dark grey, bold sans-serif font.
*   **Bullet Style:** Uses hollow square icons ($\square$) for each point.
*   **Visual Hierarchy:** The red title stands out most, followed by the primary bullet points. The "Methods:" section acts as a sub-header for the final four points.
*   **Background:** A light blue to white gradient background.
*   **Decorative Elements:** 
    *   A dark grey arrow-like shape pointing right is located at the top left edge.
    *   Several thin, dark blue curved lines sweep upwards from the bottom-left corner, adding a professional aesthetic.

## Diagram Type
This is a **text-only slide**. It uses a structured bulleted list to categorize information rather than using flowcharts, graphs, or architectural diagrams.

## Diagram / Visual Explanation
No diagram is present on this page. The visual elements (curves and arrow) are purely decorative and do not represent data flow or logical relationships.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page. While the terms "Mean," "Median," and "Mode" refer to mathematical concepts, their specific formulas are not provided here.

## Table Description
No table is visible on this page.

## Concept Explanation
*   **Data Cleaning:** This is the process of preparing raw data for analysis by removing or modifying data that is incorrect, incomplete, irrelevant, duplicated, or improperly formatted. "Dirty" data can lead to inaccurate machine learning models.
*   **Handling Missing Values:** Real-world data often has "null" or "NaN" entries where information was not recorded. This slide lists four ways to address this:
    1.  **Remove records:** Deleting the entire row containing the missing value. This is only advisable if the dataset is large and the number of missing values is very small.
    2.  **Replace with Mean:** Filling the gap with the average of all other values in that column. This is common for numerical data that follows a normal distribution.
    3.  **Replace with Median:** Filling the gap with the middle value of the sorted data. This is preferred for numerical data when outliers are present, as the median is more robust than the mean.
    4.  **Replace with Mode:** Filling the gap with the most frequent value. This is the standard approach for categorical (non-numerical) data.

## Exam / Viva Points
*   **Definition:** Data cleaning is the identification and correction of errors within a dataset to ensure data quality.
*   **Missing Value Strategies:** Be prepared to list the four methods mentioned: Deletion, Mean imputation, Median imputation, and Mode imputation.
*   **Selection Criteria:** 
    *   Use **Mean** for numerical data without significant outliers.
    *   Use **Median** for numerical data with outliers.
    *   Use **Mode** for categorical data (e.g., "Color," "City").
*   **Risk of Deletion:** Removing records can lead to a loss of valuable information and potentially introduce bias if the missingness is not random.

## Diagram Recreation Prompt
Create a professional presentation slide titled "2. Data Cleaning" in bold red text. The background should be a clean light-blue gradient. On the left, include a list of bullet points using square icons. The first point is "Identify and correct errors in the dataset." The second point is "Handling Missing Values." Below a sub-heading "Methods:", list four items: "Remove records with missing values", "Replace with Mean", "Replace with Median", and "Replace with Mode". Add a decorative element of thin, dark blue sweeping curves in the bottom-left corner to match a modern corporate style.

## Diagram Data
*   **Title:** 2. Data Cleaning
*   **Main Points:**
    *   Identify and correct errors in the dataset.
    *   Handling Missing Values
*   **Sub-List (Methods):**
    *   Remove records with missing values
    *   Replace with Mean
    *   Replace with Median
    *   Replace with Mode
