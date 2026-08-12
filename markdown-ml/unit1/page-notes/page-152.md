# Unit 1 Page 152 Image Understanding

## Page Overview
The purpose of this slide is to provide a clear, side-by-side comparison between two fundamental dimensionality reduction techniques in machine learning: **Fisher's Discriminant Analysis (FDA)** and **Principal Component Analysis (PCA)**. It highlights their differences across four key dimensions: supervision, objective, application, and output characteristics.

## Visible Text
*   **Title:** Difference between FDA and PCA
*   **Table Headers:**
    *   Feature
    *   FDA (Fisher)
    *   PCA
*   **Row 1 (Supervision):**
    *   Feature: Supervision (in red)
    *   FDA (Fisher): Supervised (uses class labels)
    *   PCA: Unsupervised
*   **Row 2 (Goal):**
    *   Feature: Goal (in red)
    *   FDA (Fisher): Maximize class separability
    *   PCA: Maximize variance
*   **Row 3 (Use case):**
    *   Feature: Use case (in red)
    *   FDA (Fisher): Classification
    *   PCA: Data compression
*   **Row 4 (Output):**
    *   Feature: Output (in red)
    *   FDA (Fisher): Best directions for class separation
    *   PCA: Best directions for data spread

## Visual Layout
*   **Title:** Positioned at the top center in a bold, magenta/pink font.
*   **Header Icon:** A dark grey arrow-like shape points from the left margin toward the title.
*   **Table Structure:** A 5-row by 3-column grid with black borders.
*   **Color Palette:**
    *   The background is a light blue gradient.
    *   The left side features decorative dark blue/grey curved lines.
    *   The "Feature" column labels are highlighted in a bright red font to draw attention to the comparison criteria.
    *   The rest of the table text is in standard black.
*   **Alignment:** Text within the table cells is left-aligned. Headers are bolded.

## Diagram Type
**Table.** This is a comparison table designed to contrast two distinct algorithms based on specific attributes.

## Diagram / Visual Explanation
The table serves as a structured comparison tool:
*   **Columns:** The first column defines the criteria for comparison ("Feature"). The second and third columns represent the two algorithms being compared (FDA and PCA).
*   **Rows:** Each row represents a specific point of divergence. For instance, the "Goal" row explains that while both reduce dimensions, they do so with different mathematical objectives (separability vs. variance).

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page.

## Table Description
| Feature | FDA (Fisher) | PCA |
| :--- | :--- | :--- |
| **Supervision** | Supervised (uses class labels) | Unsupervised |
| **Goal** | Maximize class separability | Maximize variance |
| **Use case** | Classification | Data compression |
| **Output** | Best directions for class separation | Best directions for data spread |

**Conclusion:** The table concludes that FDA is label-dependent and focused on distinguishing between groups, making it ideal for classification. In contrast, PCA is label-agnostic and focused on preserving information through variance, making it ideal for data compression.

## Concept Explanation
*   **PCA (Principal Component Analysis):** This is an unsupervised learning technique. It ignores class labels and focuses solely on the internal structure of the data. It identifies the directions (principal components) along which the data varies the most. By projecting data onto these directions, we can reduce dimensions while retaining as much information (variance) as possible.
*   **FDA (Fisher's Discriminant Analysis):** This is a supervised learning technique. It uses class labels to find a projection that makes different classes as distinct as possible. It specifically looks for a direction that maximizes the distance between the means of different classes (inter-class variance) while minimizing the spread within each class (intra-class variance).

## Exam / Viva Points
*   **Supervision:** PCA is unsupervised (no labels needed); FDA is supervised (requires labels).
*   **Primary Objective:** PCA seeks to maximize total variance; FDA seeks to maximize class separability.
*   **Application:** Use PCA when you want to compress data or reduce noise without knowing the classes. Use FDA when you want to prepare data for a classifier to improve accuracy.
*   **Output Meaning:** PCA outputs directions of maximum "spread." FDA outputs directions of maximum "separation."

## Diagram Recreation Prompt
Create a professional comparison table slide. 
- **Title:** "Difference between FDA and PCA" in bold magenta.
- **Background:** Light blue gradient with subtle abstract curved lines on the left.
- **Table:** 3 columns and 5 rows. 
- **Headers:** "Feature", "FDA (Fisher)", and "PCA" in bold black text.
- **First Column Labels:** "Supervision", "Goal", "Use case", "Output" in bold red text.
- **Content:** 
    - Row 1: "Supervised (uses class labels)" vs "Unsupervised"
    - Row 2: "Maximize class separability" vs "Maximize variance"
    - Row 3: "Classification" vs "Data compression"
    - Row 4: "Best directions for class separation" vs "Best directions for data spread"
- **Style:** Clean black borders for the table, professional sans-serif font.

## Diagram Data
*   **Title:** Difference between FDA and PCA
*   **Table Data:**
    *   Headers: ["Feature", "FDA (Fisher)", "PCA"]
    *   Row 1: ["Supervision", "Supervised (uses class labels)", "Unsupervised"]
    *   Row 2: ["Goal", "Maximize class separability", "Maximize variance"]
    *   Row 3: ["Use case", "Classification", "Data compression"]
    *   Row 4: ["Output", "Best directions for class separation", "Best directions for data spread"]
