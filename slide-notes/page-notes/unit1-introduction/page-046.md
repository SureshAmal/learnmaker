# Unit 1 Page 46 Image Understanding

## Page Overview
The purpose of this slide is to provide a comprehensive taxonomy of **Data Transformation Techniques** used in machine learning. It categorizes various preprocessing methods based on the type of input data: Numerical, Categorical, Text, and Image. This serves as a high-level roadmap for students to understand how raw data is converted into a format suitable for mathematical models.

## Visible Text
*   **Main Title:** Data Transformation Techniques
*   **Primary Categories:**
    *   Numerical data Transformation
    *   Categorical Data Transformation
    *   Text Transformation
    *   Image Transformation
*   **Numerical Sub-techniques:**
    *   Normalization (Min-Max Scaler)
    *   Standardization (z-Transformation)
*   **Categorical Sub-techniques:**
    *   One-Hot Encoding (Dummy Encoding)
    *   Label Encoding
*   **Text Sub-techniques:**
    *   (BOW) Bag of Words
    *   TF - IDF
*   **Image Sub-techniques:**
    *   Flattening

## Visual Layout
*   **Background:** The main content area has a dark charcoal/black background, set within a larger frame that has a light blue-grey border on the left with curved lines.
*   **Title Position:** Centered at the top in white bold text.
*   **Hierarchy:** A top-down tree structure.
*   **Color Coding:**
    *   **Green:** Used for the path leading to Numerical data Transformation.
    *   **Orange/Brown:** Used for the path leading to Categorical Data Transformation.
    *   **Red/Pink:** Used for the path leading to Text Transformation.
    *   **Purple:** Used for the path leading to Image Transformation.
*   **Connectors:** Thin colored lines with downward-pointing arrows connect the levels of the hierarchy.
*   **Alignment:** The four primary categories are aligned horizontally across the middle of the slide. Their respective sub-techniques are aligned vertically beneath them.

## Diagram Type
This is a **Hierarchical Tree Diagram** (or Taxonomy Chart). It is used to classify and organize complex information into logical groups and subgroups, showing the relationship between the general concept of "Data Transformation" and specific implementation methods.

## Diagram / Visual Explanation
1.  **Root Node:** "Data Transformation Techniques" sits at the top.
2.  **Level 1 Branches:** The root splits into four distinct paths based on data type.
    *   **Numerical Path (Green):** Focuses on scaling continuous values.
    *   **Categorical Path (Orange):** Focuses on converting non-numeric labels into numbers.
    *   **Text Path (Red):** Focuses on vectorizing natural language.
    *   **Image Path (Purple):** Focuses on preparing pixel data.
3.  **Level 2 Branches (Specific Methods):**
    *   From **Numerical**, two arrows point to **Normalization** and **Standardization**.
    *   From **Categorical**, two arrows point to **One-Hot Encoding** and **Label Encoding**.
    *   From **Text**, two arrows point to **Bag of Words** and **TF-IDF**.
    *   From **Image**, a single arrow points to **Flattening**.

## Math / Formula / Curve Notes
No mathematical formulas or curves are explicitly written on this page. However, the text references mathematical concepts:
*   **Min-Max Scaler:** Implies the formula $x' = \frac{x - \min(x)}{\max(x) - \min(x)}$.
*   **z-Transformation:** Implies the formula $z = \frac{x - \mu}{\sigma}$.
*   **TF-IDF:** Refers to the product of Term Frequency and Inverse Document Frequency.

## Table Description
No table is visible on this page.

## Concept Explanation
*   **Numerical Transformation:** Essential because features with different scales (e.g., age vs. salary) can bias a model. **Normalization** squashes data into a range (usually 0 to 1), while **Standardization** centers data around a mean of 0 with a standard deviation of 1.
*   **Categorical Transformation:** Machine learning models require numerical input. **Label Encoding** assigns a unique integer to each category. **One-Hot Encoding** creates binary columns for each category to avoid implying a false mathematical order between categories.
*   **Text Transformation:** Converts words into numbers. **Bag of Words** counts word occurrences. **TF-IDF** weighs words based on how unique they are to a specific document compared to a whole corpus.
*   **Image Transformation:** **Flattening** takes a multi-dimensional array (like a 28x28 pixel grid) and turns it into a long 1D vector (784 elements) so it can be fed into a standard neural network layer.

## Exam / Viva Points
*   **Normalization vs. Standardization:** Know when to use which. Normalization is sensitive to outliers; Standardization is generally more robust.
*   **One-Hot Encoding Pitfall:** Mention the "Dummy Variable Trap" (multicollinearity) which is why we sometimes drop one column.
*   **TF-IDF Purpose:** It helps identify "important" words by penalizing common words like "the" or "is" that appear everywhere.
*   **Data Leakage:** Transformation parameters (like mean or max) should be calculated on the training set only and then applied to the test set.

## Diagram Recreation Prompt
Create a hierarchical tree diagram on a dark gray background. The root node at the top center is "Data Transformation Techniques" in white bold text. Branch out into four colored paths: 
1. Green path to "Numerical data Transformation", which then branches into "Normalization (Min-Max Scaler)" and "Standardization (z-Transformation)". 
2. Orange path to "Categorical Data Transformation", branching into "One-Hot Encoding (Dummy Encoding)" and "Label Encoding". 
3. Red path to "Text Transformation", branching into "(BOW) Bag of Words" and "TF - IDF". 
4. Purple path to "Image Transformation", leading to a single node "Flattening". 
Use clean lines with arrowheads. Ensure all text is white and clearly legible.

## Diagram Data
*   **Root:** Data Transformation Techniques
*   **Level 1 Nodes:**
    *   Numerical data Transformation (Color: Green)
    *   Categorical Data Transformation (Color: Orange)
    *   Text Transformation (Color: Red)
    *   Image Transformation (Color: Purple)
*   **Edges (Parent -> Child):**
    *   Numerical -> Normalization (Min-Max Scaler)
    *   Numerical -> Standardization (z-Transformation)
    *   Categorical -> One-Hot Encoding (Dummy Encoding)
    *   Categorical -> Label Encoding
    *   Text -> (BOW) Bag of Words
    *   Text -> TF - IDF
    *   Image -> Flattening
