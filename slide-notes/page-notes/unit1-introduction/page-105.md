# Unit 1 Page 105 Image Understanding

## Page Overview
The purpose of this slide is to introduce and define **Bayes' Theorem**, a fundamental concept in probability theory and machine learning (specifically for Bayesian inference and Naive Bayes classifiers). The slide presents the mathematical formula and provides a clear, annotated breakdown of what each component represents in plain English.

## Visible Text
*   **Title:** Bayes' Theorem
*   **Main Formula:** $P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$
*   **Annotation for $P(A|B)$:** Probability of A occurring given evidence B has already occurred
*   **Annotation for $P(B|A)$:** Probability of B occurring given evidence A has already occurred
*   **Annotation for $P(A)$:** Probability of A occurring
*   **Annotation for $P(B)$:** Probability of B occurring

## Visual Layout
*   **Title Position:** The title "Bayes' Theorem" is located at the top left in a large, bold, blue sans-serif font. It is partially overlaid on a dark grey horizontal bar that extends from the left edge.
*   **Content Block:** The central content is a large white rectangular area containing the formula and its annotations.
*   **Formula:** The mathematical equation is centered and rendered in a large, black serif font.
*   **Annotations:** Four text blocks in a typewriter-style (monospace) font surround the formula.
*   **Arrows:** Four thin black arrows point from the descriptive text blocks to the specific variables in the equation:
    *   Bottom-left arrow points to $P(A|B)$.
    *   Top-middle arrow points to $P(B|A)$.
    *   Top-right arrow points to $P(A)$.
    *   Bottom-right arrow points to $P(B)$.
*   **Background:** The overall background is white, with a decorative blue-grey abstract line pattern on the far left side.

## Diagram Type
This is a **formula derivation/explanation diagram**. It uses a mathematical equation as the core element and uses callouts (text and arrows) to map abstract symbols to their conceptual meanings.

## Diagram / Visual Explanation
The diagram functions as a map for the Bayes' Theorem equation:
1.  **The Target ($P(A|B)$):** The arrow from the bottom-left text points to the left side of the equation. This represents the "Posterior" probability—what we want to calculate.
2.  **The Likelihood ($P(B|A)$):** The arrow from the top-middle text points to the first term in the numerator. It represents how likely the evidence $B$ is, assuming hypothesis $A$ is true.
3.  **The Prior ($P(A)$):** The arrow from the top-right text points to the second term in the numerator. It represents our initial belief in hypothesis $A$ before seeing any evidence.
4.  **The Evidence ($P(B)$):** The arrow from the bottom-right text points to the denominator. It represents the total probability of the evidence occurring under all possible hypotheses.

## Math / Formula / Curve Notes
The formula shown is:
$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$

*   **$P$**: Stands for "Probability."
*   **$A$**: Represents an event or hypothesis.
*   **$B$**: Represents evidence or a new data point.
*   **$|$**: The vertical bar denotes "conditional" probability, read as "given."
*   **$P(A|B)$**: The probability of $A$ given that $B$ has occurred (Posterior).
*   **$P(B|A)$**: The probability of $B$ given that $A$ has occurred (Likelihood).
*   **$P(A)$**: The independent probability of $A$ (Prior).
*   **$P(B)$**: The independent probability of $B$ (Marginal Likelihood/Evidence).

## Table Description
No table is visible on this page.

## Concept Explanation
Bayes' Theorem is a way to update our beliefs based on new evidence. In machine learning, it allows us to calculate the probability of a class (Hypothesis $A$) given a set of features (Evidence $B$).

*   **Prior ($P(A)$):** What we knew before the data. For example, in a spam filter, what is the general probability that any email is spam?
*   **Likelihood ($P(B|A)$):** If the email is indeed spam, how likely is it to contain the word "Winner"?
*   **Evidence ($P(B)$):** How likely is the word "Winner" to appear in any email (spam or not)?
*   **Posterior ($P(A|B)$):** Given that the email contains the word "Winner," what is the updated probability that it is spam?

## Exam / Viva Points
*   **State the formula:** Be able to write $P(A|B) = [P(B|A) \cdot P(A)] / P(B)$ from memory.
*   **Define the terms:** Know the formal names: Posterior, Likelihood, Prior, and Evidence (or Marginal Likelihood).
*   **Conditional Probability:** Understand that the "|" symbol means "given that" and changes the sample space to only those instances where the condition is true.
*   **Application:** Bayes' Theorem is the foundation for the **Naive Bayes Classifier**, which assumes features are independent to simplify the calculation of $P(B|A)$.

## Diagram Recreation Prompt
Create a clean, educational slide titled "Bayes' Theorem" in a bold blue font. In the center, display the formula $P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$ in large, clear black text. Use four distinct colored boxes (e.g., light blue, light green, light orange, light red) with thin arrows pointing to the four components of the formula. 
- Box 1 (pointing to $P(A|B)$): "Posterior Probability: Prob(Hypothesis | Evidence)"
- Box 2 (pointing to $P(B|A)$): "Likelihood: Prob(Evidence | Hypothesis)"
- Box 3 (pointing to $P(A)$): "Prior Probability: Prob(Hypothesis)"
- Box 4 (pointing to $P(B)$): "Marginal Likelihood: Prob(Evidence)"
Ensure the layout is spacious and uses a professional sans-serif font for annotations.

## Diagram Data
*   **Title:** Bayes' Theorem
*   **Equation:** $P(A|B) = (P(B|A) * P(A)) / P(B)$
*   **Nodes/Labels:**
    *   Label 1: "Probability of A occurring given evidence B has already occurred" -> Target: $P(A|B)$
    *   Label 2: "Probability of B occurring given evidence A has already occurred" -> Target: $P(B|A)$
    *   Label 3: "Probability of A occurring" -> Target: $P(A)$
    *   Label 4: "Probability of B occurring" -> Target: $P(B)$
