# Unit 1 Page 49 Image Understanding

## Page Overview
The purpose of this slide is to provide a comprehensive comparison between two essential feature scaling techniques in machine learning: **Normalisation** and **Standardisation**. It serves as a reference guide for students to understand the technical differences, use cases, and properties of each method, helping them decide which technique is appropriate for a given dataset.

## Visible Text
*   **Top Header (Partial):** The resulting values are compressed into a consistent scale of 0 to 1.
*   **Table Headers:**
    *   Parameter
    *   Normalisation
    *   Standardisation
*   **Row 1 (Scaling):**
    *   Normalisation: Scaling is done by the highest and the lowest values.
    *   Standardisation: Scaling is done by mean and standard deviation.
*   **Row 2 (Applying):**
    *   Normalisation: It is applied when the features are of separate scales.
    *   Standardisation: It is applied when we verify zero mean and unit standard deviation.
*   **Row 3 (Range):**
    *   Normalisation: Scales range from 0 to 1
    *   Standardisation: Not bounded
*   **Row 4 (Affection):**
    *   Normalisation: Affected by outliers
    *   Standardisation: Less affected by outliers
*   **Row 5 (Data distribution):**
    *   Normalisation: It is applied when we are not sure about the data distribution
    *   Standardisation: It is used when the data is Gaussian or normally distributed
*   **Row 6 (Also known):**
    *   Normalisation: It is also known as Scaling Normalization
    *   Standardisation: It is also known as Z-Score

## Visual Layout
*   **Background:** The slide has a light blue-grey background with a dark grey vertical bar on the far left and decorative thin curved lines.
*   **Main Content:** A large, centrally placed table with a double-line black border.
*   **Table Structure:** The table consists of 3 columns and 7 rows. The first column acts as the header for the comparison criteria.
*   **Typography:** The text is sans-serif, grey, and left-aligned within the cells. The headers are centered.
*   **Visual Hierarchy:** The table is the dominant element. The "Parameter" column is clearly separated to guide the reader through different comparison points horizontally.

## Diagram Type
This is a **Comparison Table**. It is used to contrast two related concepts (Normalisation vs. Standardisation) across several specific dimensions (Parameters) to highlight their differences and specific applications.

## Diagram / Visual Explanation
The table functions as a matrix for decision-making:
1.  **Horizontal Axis:** Compares the two methods side-by-side.
2.  **Vertical Axis:** Lists the criteria for comparison, such as the mathematical basis (Scaling), the output range (Range), and sensitivity to noise (Affection).
3.  **Relationship:** By reading across a row, a student can immediately see how the two methods differ on a specific property. For example, looking at the "Range" row, one can see that Normalisation constrains data while Standardisation does not.

## Math / Formula / Curve Notes
No explicit mathematical formulas are visible on this page. However, the text refers to mathematical concepts:
*   **Highest and lowest values:** Refers to the Min-Max formula: $X_{new} = \frac{X - X_{min}}{X_{max} - X_{min}}$.
*   **Mean and standard deviation:** Refers to the Z-score formula: $z = \frac{x - \mu}{\sigma}$.
*   **Zero mean and unit standard deviation:** Describes the result of Standardisation where $\mu = 0$ and $\sigma = 1$.
*   **Gaussian / Normally distributed:** Refers to the bell curve distribution of data.

## Table Description
| Parameter | Normalisation | Standardisation |
| :--- | :--- | :--- |
| **Scaling** | Uses Min and Max values. | Uses Mean and Standard Deviation. |
| **Applying** | Used for features with different scales. | Used to achieve zero mean and unit variance. |
| **Range** | Fixed between 0 and 1. | Not bounded (can be any value). |
| **Affection** | Highly sensitive to outliers. | More robust/less affected by outliers. |
| **Data distribution** | Used when distribution is unknown. | Used for Gaussian/Normal distributions. |
| **Also known** | Scaling Normalization / Min-Max Scaling. | Z-Score. |

## Concept Explanation
*   **Feature Scaling:** In machine learning, features often have different units and scales (e.g., age vs. income). Scaling ensures that no single feature dominates the model's learning process due to its magnitude.
*   **Normalisation (Min-Max Scaling):** This technique shifts and rescales the data so that all values fall within the range [0, 1]. It is very useful when you need a bounded range, but because it relies on the absolute minimum and maximum, a single outlier can "squish" all other data points into a tiny range.
*   **Standardisation (Z-Score):** This technique centers the data around a mean of 0 with a standard deviation of 1. It does not produce a fixed range. It is generally preferred for algorithms that assume a Gaussian distribution (like Linear Regression or Logistic Regression) and is more reliable when the data contains outliers.

## Exam / Viva Points
*   **Range Difference:** Normalisation is bounded (0 to 1), while Standardisation is unbounded.
*   **Outlier Sensitivity:** Normalisation is highly sensitive to outliers because it uses $X_{min}$ and $X_{max}$. Standardisation is more robust.
*   **Distribution Assumption:** Use Standardisation if the data follows a Gaussian (Normal) distribution. Use Normalisation if you don't know the distribution or if the algorithm requires a bounded range (like Image Processing).
*   **Alternative Names:** Normalisation is often called Min-Max scaling; Standardisation is called Z-score scaling.
*   **Mathematical Basis:** Normalisation is based on the range of the data; Standardisation is based on the central tendency and spread (mean/std dev).

## Diagram Recreation Prompt
Create a clean, modern comparison table for a machine learning presentation. 
- **Title:** "Comparison: Normalisation vs. Standardisation"
- **Columns:** "Parameter", "Normalisation", "Standardisation".
- **Rows:** Scaling, Applying, Range, Affection (Outliers), Data Distribution, Also Known As.
- **Style:** Use a professional color palette. Header row in dark blue with white text. Alternating light grey and white rows for readability. 
- **Content:** Populate with the text from the provided image. 
- **Layout:** Ensure the table fills the width of the slide and has generous padding within cells.

## Diagram Data
*   **Title:** Comparison of Feature Scaling Techniques
*   **Headers:** Parameter, Normalisation, Standardisation
*   **Row 1:** Scaling | Highest/Lowest values | Mean/Std Dev
*   **Row 2:** Applying | Separate scales | Zero mean/Unit std dev
*   **Row 3:** Range | 0 to 1 | Not bounded
*   **Row 4:** Affection | Affected by outliers | Less affected by outliers
*   **Row 5:** Data distribution | Unknown distribution | Gaussian/Normal distribution
*   **Row 6:** Also known | Scaling Normalization | Z-Score
