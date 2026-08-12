# Unit 1 Page 139 Image Understanding

## Page Overview
The purpose of this slide is to categorize and list the primary types of **Discriminant Functions** used in machine learning and pattern recognition. It serves as an introductory overview for a module discussing how different mathematical functions can be used to separate data into distinct classes.

## Visible Text
*   **Title:** Types of Discriminant Functions :
*   **List Items:**
    *   Linear Discriminant Function (LDF)
    *   Quadratic Discriminant Function (QDF)
    *   Bayesian Discriminant Function (BDF)

## Visual Layout
*   **Title Position:** Located at the top left, rendered in a large, bold, magenta (pinkish-purple) sans-serif font.
*   **Content Blocks:** A single list of three items occupies the center-left portion of the slide.
*   **Colors:** 
    *   Background: A light blue to white radial gradient.
    *   Text: Magenta for the title and dark gray/black for the list items.
    *   Accents: Dark blue abstract curved lines on the far left side.
*   **Icons/Shapes:** A black horizontal arrow-like pentagon points toward the title from the left margin. The list items are preceded by square bullet points (the third bullet point contains a diagonal slash).
*   **Spacing and Alignment:** The text is left-aligned with significant white space on the right and bottom, creating a minimalist and clear visual hierarchy.

## Diagram Type
This is a **text-only slide**. It functions as a list or a table of contents for the upcoming technical discussion. There are no flowcharts, graphs, or architectural diagrams present.

## Diagram / Visual Explanation
No diagram is present on this page. The visual elements (curved lines and the black arrow) are purely decorative and do not convey specific machine-learning data.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page.

## Table Description
No table is visible on this page.

## Concept Explanation
In machine learning, a **Discriminant Function** is a function that takes an input vector $x$ and assigns it to one of $K$ classes. The slide identifies three specific approaches:

1.  **Linear Discriminant Function (LDF):** This approach assumes that the decision boundaries between classes are linear (straight lines in 2D, planes in 3D, or hyperplanes in higher dimensions). It typically assumes that all classes share the same covariance matrix.
2.  **Quadratic Discriminant Function (QDF):** This is a more flexible version of LDF. It assumes that each class has its own covariance matrix, resulting in decision boundaries that are quadratic surfaces (such as parabolas, ellipses, or hyperbolas).
3.  **Bayesian Discriminant Function (BDF):** This approach is rooted in probability theory (Bayes' Theorem). It classifies an object by calculating the posterior probability $P(C_i | x)$—the probability that the object belongs to class $C_i$ given the observed features $x$. The object is assigned to the class with the highest posterior probability to minimize the average risk or error.

## Exam / Viva Points
*   **List the three types of discriminant functions:** Linear, Quadratic, and Bayesian.
*   **Key Difference between LDF and QDF:** LDF assumes a common covariance matrix across classes, leading to linear boundaries. QDF allows for class-specific covariance matrices, leading to non-linear (quadratic) boundaries.
*   **Basis of BDF:** The Bayesian Discriminant Function is based on the **Bayes Decision Rule**, which aims to minimize the probability of misclassification by using prior probabilities and class-conditional densities.
*   **Complexity:** QDF is computationally more expensive than LDF because it requires estimating a separate covariance matrix for every class.

## Diagram Recreation Prompt
Create a professional educational slide titled "Types of Discriminant Functions" in bold magenta text. Below the title, create three distinct, horizontally aligned cards or boxes. 
1. The first box labeled "Linear (LDF)" should contain a simple icon of a straight line separating two groups of dots. 
2. The second box labeled "Quadratic (QDF)" should contain an icon of a curved line (parabola) separating two groups of dots. 
3. The third box labeled "Bayesian (BDF)" should contain an icon representing a bell curve or the Bayes formula $P(A|B)$. 
Use a clean white background with subtle blue accents and ensure the text is high-contrast dark gray.

## Diagram Data
*   **Title:** Types of Discriminant Functions :
*   **List Item 1:** Linear Discriminant Function (LDF)
*   **List Item 2:** Quadratic Discriminant Function (QDF)
*   **List Item 3:** Bayesian Discriminant Function (BDF)
