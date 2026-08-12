# Unit 1 Page 108 Image Understanding

## Page Overview
This slide introduces the **Naive Bayes Classifier** as a primary application of Bayes' Theorem in machine learning. The purpose is to define the classifier, present its foundational mathematical formula, and provide a visual representation of how it partitions data into different classes based on probability.

## Visible Text
*   **Applications of Bayes Theorem:**
*   **1. Naive Bayes Classifier**
*   In machine learning, naive Bayes classifiers are a family of simple "probabilistic classifiers" based on applying Bayes' theorem with strong (naive) independence assumptions between the features.
*   **Formula 1:**
    $$P(A|B) = \frac{P(B|A) P(A)}{P(B)}$$
*   using Bayesian probability terminology, the above equation can be written as
*   **Formula 2:**
    $$\text{Posterior} = \frac{\text{prior} \times \text{likelihood}}{\text{evidence}}$$
*   **Graph Title:** Naive bayes classifier
*   **Graph Legend:**
    *   Red dot: Classifier 1
    *   Orange dot: Classifier 2
    *   Blue dot: Classifier 3
*   **Graph Axes:**
    *   Y-axis: 0 to 6
    *   X-axis: 0 to 6

## Visual Layout
*   **Header:** The main title "Applications of Bayes Theorem:" is in blue. The subtitle "1. Naive Bayes Classifier" is in bold red. A dark grey chevron/arrow shape is positioned to the left of the title.
*   **Content Split:** The slide is divided into two main sections.
    *   **Left Side:** Contains the textual definition and the mathematical derivation of the Bayes formula.
    *   **Right Side:** Features a light grey rectangular box containing a scatter plot with decision boundaries.
*   **Colors:** Uses a clean white background. Formulas are in black. The graph uses distinct colors (Blue, Orange, Red) to represent different classes.
*   **Hierarchy:** The title clearly defines the topic, followed by a text definition, then the math, and finally a visual example to reinforce the concept.

## Diagram Type
The main visual is a **Scatter Plot with Decision Boundaries**. It is used to illustrate classification because it shows how a feature space (represented by X and Y coordinates) is partitioned into regions belonging to different classes (represented by colors) based on probabilistic boundaries.

## Diagram / Visual Explanation
*   **Axes:** The graph represents a 2D feature space with an X-axis and a Y-axis, both scaled from 0 to 6.
*   **Data Points:**
    *   **Blue dots (Classifier 3):** Clustered mostly on the left side, between X=1 to 3 and Y=2 to 6.
    *   **Orange dots (Classifier 2):** Clustered in the top right, between X=3 to 5 and Y=3.5 to 6.
    *   **Red dots (Classifier 1):** Clustered in the bottom center-right, between X=2.5 to 4.5 and Y=1 to 3.5.
*   **Decision Boundaries:** Three curved black lines originate from a central junction point (roughly at X=3, Y=3.7). These lines divide the plane into three distinct regions. Any new data point falling into a specific region would be classified into the corresponding color group based on the highest posterior probability.
*   **Legend:** Located at the top right of the graph, mapping colors to "Classifier" labels.

## Math / Formula / Curve Notes
The slide presents two versions of the same fundamental equation:

1.  **Standard Bayes Theorem:** $P(A|B) = \frac{P(B|A) P(A)}{P(B)}$
    *   $P(A|B)$: Conditional probability of event $A$ occurring given that $B$ is true.
    *   $P(B|A)$: Conditional probability of event $B$ occurring given that $A$ is true.
    *   $P(A)$ and $P(B)$: The probabilities of observing $A$ and $B$ independently of each other.

2.  **Machine Learning Terminology:** $\text{Posterior} = \frac{\text{prior} \times \text{likelihood}}{\text{evidence}}$
    *   **Posterior:** The probability of a class (hypothesis) given the observed features (data). This is what we want to calculate.
    *   **Prior:** The initial probability of the class before seeing the data.
    *   **Likelihood:** The probability of the observed features given that the class is true.
    *   **Evidence:** The total probability of the features across all possible classes.

## Table Description
No table is visible on this page.

## Concept Explanation
**Naive Bayes** is a classification algorithm. It is called "Bayes" because it relies on Bayes' Theorem to calculate the probability of a class. It is called "Naive" because it makes a massive simplifying assumption: it assumes that all input features are **independent** of each other. 

For example, if you are classifying a fruit as an "Apple" based on color (red) and shape (round), Naive Bayes assumes the redness has nothing to do with the roundness. While this is rarely true in the real world, the "naive" assumption makes the math much faster and surprisingly effective for complex tasks like spam detection or document classification.

## Exam / Viva Points
*   **Definition:** Naive Bayes is a probabilistic classifier based on Bayes' Theorem.
*   **The "Naive" Assumption:** It assumes strong independence between features (i.e., the presence of one feature does not affect the probability of another).
*   **Components of the Formula:** Be prepared to define Posterior, Prior, Likelihood, and Evidence.
*   **Decision Boundaries:** In the visual context, the classifier draws boundaries where the posterior probability of one class becomes higher than the others.
*   **Use Case:** It is widely used for text classification and real-time predictions due to its computational efficiency.

## Diagram Recreation Prompt
Create a professional educational slide graphic titled "Naive Bayes Classifier". On the left, display the formula "P(A|B) = [P(B|A) * P(A)] / P(B)" in large, clear font, followed by the text "Posterior = (Prior * Likelihood) / Evidence". On the right, include a 2D scatter plot on a light grey background. The plot should have X and Y axes from 0 to 6. Populate the plot with three distinct clusters of dots: Blue (top-left), Orange (top-right), and Red (bottom-center). Draw smooth, curved black lines (decision boundaries) that separate these three color regions. Include a legend identifying the colors as "Class 1", "Class 2", and "Class 3". Use a clean, modern sans-serif font.

## Diagram Data
*   **Title:** Applications of Bayes Theorem: 1. Naive Bayes Classifier
*   **Text Content:** Definition of Naive Bayes and the independence assumption.
*   **Formulas:**
    *   $P(A|B) = (P(B|A) * P(A)) / P(B)$
    *   $\text{Posterior} = (\text{Prior} \times \text{Likelihood}) / \text{Evidence}$
*   **Graph Data (Inferred):**
    *   **Class 1 (Red):** Points centered around (3.5, 2.5)
    *   **Class 2 (Orange):** Points centered around (4.5, 5.0)
    *   **Class 3 (Blue):** Points centered around (2.0, 4.0)
    *   **Boundaries:** Non-linear curves meeting at a central vertex near (3.2, 3.8).
