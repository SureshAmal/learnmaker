# Unit 1 Page 52 Image Understanding

## Page Overview
The purpose of this slide is to introduce two critical data preprocessing steps in machine learning: **Handling Duplicate Data** and **Handling Outliers**. While the title focuses on duplicates, the majority of the content defines outliers, provides a concrete numerical example of an outlier in a salary dataset, and lists three standard statistical techniques used to manage them.

## Visible Text
*   **Handling Duplicate Data**
*   Remove repeated records to avoid bias.
*   **Handling Outliers**
*   Outliers are unusually high or low values.
*   **Example:**
*   **Salary = [25,000, 30,000, 35,000, 500,000]**
*   Here, 500,000 is an outlier.
*   **Techniques:**
*   Z-Score
*   IQR (Interquartile Range)
*   Clipping

## Visual Layout
*   **Title:** Located at the top left in a large, bold, red font. It is preceded by a square checkbox icon and a black horizontal arrow-like graphic pointing from the left margin.
*   **Background:** A light blue to white gradient. On the far left, there are several thin, dark blue curved lines that sweep from the bottom to the top.
*   **Content Alignment:** The text is left-aligned and organized as a series of bullet points using small black squares.
*   **Hierarchy:** The main title is red. Sub-headings like "Handling Outliers," "Example:", and "Techniques:" are in a bold black font to distinguish them from the descriptive text.
*   **Spacing:** Generous line spacing is used between bullet points for readability.

## Diagram Type
This is a **text-only slide** with a bulleted list. It uses a structured textual format to present definitions, an example, and a list of methods rather than a visual flowchart or graph.

## Diagram / Visual Explanation
No diagram is present on this page. The visual elements (lines on the left and the black arrow) are purely decorative and do not represent data flow or relationships.

## Math / Formula / Curve Notes
While no complex formulas are written out, a mathematical set (array) is provided as an example:
*   **Salary Array:** `[25,000, 30,000, 35,000, 500,000]`
*   **Logic:** The first three values are within a close range (5,000 units apart), while the final value (500,000) is over 14 times larger than the next highest value, mathematically qualifying it as an outlier in this context.
*   **Mentioned Concepts:** The slide mentions **Z-Score** (which involves mean and standard deviation) and **IQR** (which involves quartiles), but does not show their respective formulas ($Z = \frac{x - \mu}{\sigma}$ or $IQR = Q3 - Q1$).

## Table Description
No table is visible on this page.

## Concept Explanation
*   **Duplicate Data:** In machine learning, having the same record multiple times can lead to "over-representation" or bias. The model might learn that a specific pattern is more common than it actually is in the real world, leading to poor generalization.
*   **Outliers:** These are data points that differ significantly from other observations. They can be caused by experimental error, variability in measurement, or genuine but extreme rare cases.
*   **Impact of Outliers:** Outliers can skew statistical measures like the mean and can negatively impact the performance of many algorithms (like Linear Regression) by pulling the "best fit" line toward the extreme value.
*   **Handling Techniques:**
    *   **Z-Score:** A method that describes a value's relationship to the mean of a group of values, measured in terms of standard deviations. Typically, a Z-score greater than 3 or less than -3 is considered an outlier.
    *   **IQR (Interquartile Range):** This method defines outliers based on the spread of the middle 50% of the data. Points falling below $Q1 - 1.5 \times IQR$ or above $Q3 + 1.5 \times IQR$ are flagged.
    *   **Clipping (Winsorizing):** Instead of removing outliers, they are "capped" at a specific threshold (e.g., the 1st and 99th percentiles).

## Exam / Viva Points
*   **Why must duplicate records be removed?** To prevent the model from becoming biased toward specific repeated instances.
*   **Define an outlier.** An observation that lies an abnormal distance from other values in a random sample from a population.
*   **Identify the outlier in a set:** If given the set `[25k, 30k, 35k, 500k]`, be prepared to explain why 500k is the outlier (it is significantly distant from the cluster of other points).
*   **Name three techniques for handling outliers.** Z-Score, Interquartile Range (IQR), and Clipping.
*   **What is Clipping?** It is the process of limiting extreme values in the data to a maximum or minimum threshold to reduce their impact on the model.

## Diagram Recreation Prompt
Create a clean, professional educational slide titled "Handling Duplicates & Outliers." 
- Use a white background with a subtle blue header bar. 
- On the left side, place a text block explaining that duplicate records should be removed to avoid bias. 
- On the right side, create a "Handling Outliers" section. 
- Include a visual callout box for the example: "Salary = [25k, 30k, 35k, 500k]" with "500k" highlighted in red. 
- At the bottom, create three distinct colored icons or boxes for the techniques: "Z-Score," "IQR (Interquartile Range)," and "Clipping." 
- Use a modern sans-serif font (like Roboto or Arial).

## Diagram Data
*   **Title:** Handling Duplicate Data
*   **Section 1 (Duplicates):**
    *   Action: Remove repeated records.
    *   Reason: Avoid bias.
*   **Section 2 (Outliers):**
    *   Definition: Unusually high or low values.
    *   Example Data: [25,000, 30,000, 35,000, 500,000]
    *   Target Outlier: 500,000
*   **Section 3 (Techniques List):**
    *   Technique 1: Z-Score
    *   Technique 2: IQR (Interquartile Range)
    *   Technique 3: Clipping
