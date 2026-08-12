# Unit 1 Page 107 Image Understanding

## Page Overview
The purpose of this slide is to provide a visual breakdown and definition of the components of **Bayes' Theorem**. It serves as a foundational mathematical explanation for probability-based machine learning algorithms, such as Naive Bayes. The slide identifies the four key terms of the equation: Likelihood, Prior, Posterior, and Marginalization, providing a brief definition for each.

## Visible Text
*   **LIKELIHOOD**: The probability of "B" being True, given "A" is True
*   **PRIOR**: The probability "A" being True. This is the knowledge.
*   **POSTERIOR**: The probability of "A" being True, given "B" is True
*   **MARGINALIZATION**: The probability "B" being True.
*   **Formula**: $P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$

## Visual Layout
*   **Background**: A light blue to white radial gradient background. On the left side, there are several dark blue, thin, curved abstract lines.
*   **Central Element**: The Bayes' Theorem formula is written in a large, bold, blue font in the center of the slide.
*   **Annotations**: Four blocks of orange text are placed around the formula, each defining a specific part of the equation.
*   **Arrows**: Four thick yellow arrows with black outlines point from the text blocks to the specific mathematical terms they describe.
    *   Top-left arrow points down to $P(B|A)$.
    *   Top-right arrow points down to $P(A)$.
    *   Bottom-left arrow points up to $P(A|B)$.
    *   Bottom-right arrow points up to $P(B)$.
*   **Color Coding**: 
    *   Blue: Mathematical formula.
    *   Orange: Labels and definitions.
    *   Yellow: Directional pointers (arrows).

## Diagram Type
This is a **formula derivation/annotation diagram**. It uses a central mathematical equation as the anchor and uses text blocks and arrows to map conceptual definitions to specific algebraic variables.

## Diagram / Visual Explanation
The diagram explains the relationship between conditional probabilities:
1.  **Posterior ($P(A|B)$)**: Located on the left side of the equals sign. The bottom-left arrow points to it, identifying it as the result we are trying to calculate—the probability of hypothesis $A$ after considering evidence $B$.
2.  **Likelihood ($P(B|A)$)**: Located in the numerator on the right side. The top-left arrow points to it, defining it as how likely the evidence $B$ is, assuming the hypothesis $A$ is true.
3.  **Prior ($P(A)$)**: Located in the numerator, multiplied by the likelihood. The top-right arrow points to it, defining it as the original "knowledge" or probability of $A$ before any evidence was seen.
4.  **Marginalization ($P(B)$)**: Located in the denominator. The bottom-right arrow points to it, defining it as the total probability of the evidence $B$ occurring across all possible outcomes.

## Math / Formula / Curve Notes
The formula shown is **Bayes' Theorem**:
$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$

*   **$P(A|B)$**: The conditional probability of event $A$ occurring given that $B$ is true.
*   **$P(B|A)$**: The conditional probability of event $B$ occurring given that $A$ is true.
*   **$P(A)$**: The independent probability of event $A$.
*   **$P(B)$**: The independent probability of event $B$ (acting as a normalizing constant).
*   **$|$**: The vertical bar denotes "given" or "conditioned on."
*   **$\cdot$**: The dot denotes multiplication between the Likelihood and the Prior.
*   **$-$**: The horizontal bar denotes division by the Marginalization (Evidence).

## Table Description
No table is visible on this page.

## Concept Explanation
Bayes' Theorem is a way to find a probability when we know other probabilities. It is essentially a way to update our beliefs based on new evidence.

*   **Prior Knowledge**: We start with a belief ($P(A)$). For example, the probability that a person has a specific disease in the general population.
*   **New Evidence**: We receive new data ($B$), such as a positive lab test result.
*   **Likelihood**: We know how reliable the test is—the probability of a positive test if the person actually has the disease ($P(B|A)$).
*   **Posterior**: By combining our prior knowledge with the likelihood of the new evidence (and dividing by the total probability of that evidence occurring), we get a new, updated probability ($P(A|B)$) that the person has the disease given the positive test.

In Machine Learning, this is the backbone of **Bayesian Inference**, where $A$ is often a class label and $B$ is a set of features.

## Exam / Viva Points
*   **State the formula**: Be prepared to write $P(A|B) = [P(B|A) \cdot P(A)] / P(B)$ from memory.
*   **Define the terms**: You must be able to name and define all four parts (Posterior, Likelihood, Prior, Marginalization/Evidence).
*   **Directionality**: Understand that $P(A|B)$ is not the same as $P(B|A)$. One is the probability of the hypothesis given data, the other is the probability of data given the hypothesis.
*   **The Role of the Prior**: Explain that the Prior represents "domain knowledge" or existing information before an experiment begins.
*   **The Role of Marginalization**: Explain that $P(B)$ ensures the resulting posterior probabilities sum to 1 (normalization).

## Diagram Recreation Prompt
Create a high-resolution educational graphic for Bayes' Theorem. 
- **Center**: Place the formula $P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$ in a large, clear, professional serif font. 
- **Layout**: Use a clean white background. 
- **Annotations**: Place four distinct colored text boxes around the formula. 
    - Top-Left (Green): "LIKELIHOOD: $P(B|A)$ - Prob. of evidence given hypothesis". 
    - Top-Right (Blue): "PRIOR: $P(A)$ - Initial belief/knowledge". 
    - Bottom-Left (Red): "POSTERIOR: $P(A|B)$ - Updated prob. after seeing evidence". 
    - Bottom-Right (Purple): "EVIDENCE / MARGINALIZATION: $P(B)$ - Total prob. of the evidence".
- **Connectors**: Draw sleek, tapered arrows from each box pointing directly to the corresponding variable in the formula. 
- **Style**: Use a modern, flat design aesthetic with high contrast for readability.

## Diagram Data
*   **Main Equation**: $P(A|B) = (P(B|A) * P(A)) / P(B)$
*   **Mapping**:
    *   Term: $P(A|B)$ | Label: POSTERIOR | Definition: Prob. of A being True given B is True.
    *   Term: $P(B|A)$ | Label: LIKELIHOOD | Definition: Prob. of B being True given A is True.
    *   Term: $P(A)$ | Label: PRIOR | Definition: Prob. of A being True (Initial knowledge).
    *   Term: $P(B)$ | Label: MARGINALIZATION | Definition: Prob. of B being True.
*   **Visual Elements**: 4 Labels, 4 Arrows, 1 Central Equation.
