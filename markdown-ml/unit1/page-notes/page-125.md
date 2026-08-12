# Unit 1 Page 125 Image Understanding

## Page Overview
The purpose of this slide is to introduce and briefly define three advanced types of regression techniques used in machine learning: **Polynomial Regression**, **Ridge and Lasso Regression**, and **Logistic Regression**. It serves as a categorical overview to distinguish how these methods handle non-linearity, overfitting, and classification tasks compared to standard linear regression.

## Visible Text
*   **Title:** Types of Regression:
*   **Bullet Point 1:** •Polynomial Regression
    *   **Description:** Fits a non-linear curve (polynomial equation)
*   **Bullet Point 2:** •Ridge and Lasso Regression
    *   **Description:** Regularized versions of linear regression to reduce over fitting
*   **Bullet Point 3:** •Logistic Regression *(Actually for classification)*
    *   **Description:** Predicts probability of class (used in classification)

## Visual Layout
*   **Title Position:** Centered at the top of the page in a bold, magenta (pinkish-purple) font.
*   **Content Blocks:** The text is left-aligned, consisting of three main bullet points. Each bullet point has a bold header followed by a descriptive sentence on the next line.
*   **Colors:** 
    *   Background: A soft light-blue to white radial gradient.
    *   Title: Magenta.
    *   Body Text: Black.
*   **Decorative Elements:** 
    *   A dark grey pentagonal arrow shape is located at the top left corner, pointing towards the title.
    *   Several thin, dark blue/grey curved lines sweep up from the bottom left corner, acting as a decorative border.
*   **Spacing and Alignment:** The text is positioned in the center-left area of the slide with ample white space on the right.

## Diagram Type
This is a **text-only slide**. It uses a list format to present information rather than a flowchart, graph, or architecture diagram.

## Diagram / Visual Explanation
No diagram is present on this page. The visual elements (curves and arrow) are purely decorative and do not convey specific data or process steps.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page. However, the text references mathematical concepts:
*   **Polynomial equation:** Implies a formula of the form $y = \beta_0 + \beta_1x + \beta_2x^2 + ... + \beta_nx^n$.
*   **Probability of class:** Refers to the output of the sigmoid function in Logistic Regression, which ranges between 0 and 1.

## Table Description
No table is visible on this page.

## Concept Explanation
*   **Polynomial Regression:** While linear regression assumes a straight-line relationship, polynomial regression models the relationship between the independent variable $x$ and the dependent variable $y$ as an $n^{th}$ degree polynomial. This allows the model to fit data that follows a curved path.
*   **Ridge and Lasso Regression:** These are "Regularization" techniques. In standard linear regression, models can become too complex and "overfit" the training data (memorizing noise). Ridge (L2 regularization) and Lasso (L1 regularization) add a penalty term to the loss function based on the size of the coefficients, forcing the model to stay simpler and generalize better to new data.
*   **Logistic Regression:** Despite the name "regression," this is a fundamental algorithm for **classification**. It uses a logistic (sigmoid) function to transform a linear combination of inputs into a probability value between 0 and 1. This probability is then used to assign the input to a specific category (e.g., "Yes" or "No").

## Exam / Viva Points
*   **Distinction:** Be prepared to explain why Logistic Regression is considered a classification tool despite its name.
*   **Overfitting:** Identify Ridge and Lasso as the primary tools mentioned here for combating overfitting through regularization.
*   **Non-linearity:** Understand that Polynomial Regression is the go-to method when the data trend is not a straight line but still follows a predictable curve.
*   **Output Type:** Remember that while Polynomial and Ridge/Lasso predict continuous values, Logistic Regression predicts the **probability** of a discrete class.

## Diagram Recreation Prompt
Create a clean, professional presentation slide titled "Types of Regression" in bold magenta. Use a light blue gradient background. Create three distinct sections using a vertical list. 
1. Header: "Polynomial Regression" in bold black; Subtext: "Fits a non-linear curve (polynomial equation)". 
2. Header: "Ridge and Lasso Regression" in bold black; Subtext: "Regularized versions of linear regression to reduce over fitting". 
3. Header: "Logistic Regression (Actually for classification)" in bold black; Subtext: "Predicts probability of class (used in classification)". 
Add a decorative dark grey arrow icon in the top left and subtle abstract curved lines on the left margin for visual flair.

## Diagram Data
*   **Title:** Types of Regression:
*   **List Item 1:**
    *   Label: Polynomial Regression
    *   Detail: Fits a non-linear curve (polynomial equation)
*   **List Item 2:**
    *   Label: Ridge and Lasso Regression
    *   Detail: Regularized versions of linear regression to reduce over fitting
*   **List Item 3:**
    *   Label: Logistic Regression (Actually for classification)
    *   Detail: Predicts probability of class (used in classification)
