# Unit 1 Page 102 Image Understanding

## Page Overview
The purpose of this slide is to formally define **Conditional Probability** and present its fundamental mathematical properties. It introduces the notation for conditional probability, provides the core formula, demonstrates how to derive the joint probability (multiplication rule), generalizes this rule to multiple events (chain rule), and shows the symmetric definition for the inverse condition.

## Visible Text
*   **Title:** Conditional Probability
*   **Body Text:**
    *   The conditional probability of an event $A$ assuming that $B$ has occurred, denoted $P(A | B)$, equals
    *   $P(A | B) = \frac{P(A \cap B)}{P(B)}$, (1)
    *   which can be proven directly using a Venn diagram. Multiplying through, this becomes
    *   $P(A | B) P(B) = P(A \cap B)$, (2)
    *   which can be generalized to
    *   $P(A \cap B \cap C) = P(A) P(B | A) P(C | A \cap B)$. (3)
    *   Rearranging (1) gives
    *   $P(B | A) = \frac{P(B \cap A)}{P(A)}$. (4)

## Visual Layout
*   **Title:** Located at the top left in a large, blue sans-serif font.
*   **Divider:** A thin, horizontal light-green line separates the title from the main content.
*   **Content Alignment:** The text is left-aligned. The mathematical formulas are centered horizontally relative to the text block, with equation numbers (1) through (4) right-aligned.
*   **Color Palette:** Uses a clean white background with black text. Key terms like "event" and "Venn diagram" are highlighted in a teal/blue color.
*   **Background Graphics:** Faint, decorative mathematical watermarks are visible on the left and right margins (e.g., a summation symbol on the top left and integral formulas on the right).
*   **Spacing:** Generous vertical spacing between text lines and formulas to ensure readability.

## Diagram Type
This is a **formula derivation and definition slide**. It does not contain a graphical diagram like a flowchart or plot, but rather a structured sequence of mathematical expressions that build upon one another logically.

## Diagram / Visual Explanation
While no explicit diagram is present, the text references a **Venn diagram** as a method of proof. In such a diagram, $P(A | B)$ would be visualized by looking only at the area of circle $B$ (the new sample space) and determining what fraction of that area is covered by the intersection of $A$ and $B$. The slide itself functions as a logical flow:
1.  **Definition (1):** Establishes the base ratio.
2.  **Transformation (2):** Shows the multiplication rule for the intersection of two events.
3.  **Generalization (3):** Extends the logic to three events (the Chain Rule).
4.  **Symmetry (4):** Shows the formula for the reverse condition ($B$ given $A$).

## Math / Formula / Curve Notes
*   **$P(A | B)$**: The probability of event $A$ occurring, given the knowledge that event $B$ has already occurred.
*   **$P(A \cap B)$**: The joint probability of both events $A$ and $B$ occurring.
*   **$P(B)$**: The marginal probability of event $B$. It must be $> 0$ for the conditional probability to be defined.
*   **Equation (1):** Defines conditional probability as the ratio of the joint probability to the probability of the condition.
*   **Equation (2):** The **Multiplication Rule**. It expresses the joint probability as the product of the condition's probability and the conditional probability.
*   **Equation (3):** The **Chain Rule** for three events. It shows that the probability of $A, B,$ and $C$ all occurring is the probability of $A$, times the probability of $B$ given $A$, times the probability of $C$ given both $A$ and $B$.
*   **Equation (4):** Demonstrates that the definition is symmetric; to find $P(B | A)$, you divide the same intersection $P(B \cap A)$ by the new condition $P(A)$.

## Table Description
No table is visible on this page.

## Concept Explanation
**Conditional Probability** is a measure of the probability of an event occurring, given that another event has already occurred. If the event of interest is $A$ and the event that has occurred is $B$, we write this as $P(A | B)$.

Think of it as "shrinking" the sample space. Instead of looking at all possible outcomes, we only look at the outcomes where $B$ is true. Within this new, smaller universe, we calculate how likely $A$ is to happen. This is why we divide by $P(B)$ in the formula.

The **Chain Rule** (Equation 3) is a powerful extension. It allows us to calculate the probability of a complex sequence of events by breaking it down into a series of conditional steps. This is a foundational concept for Bayesian networks and many machine learning algorithms like Naive Bayes or Hidden Markov Models.

## Exam / Viva Points
*   **State the formula for $P(A | B)$:** $P(A | B) = \frac{P(A \cap B)}{P(B)}$.
*   **What is the condition for Equation (1) to be valid?** $P(B)$ must be greater than zero ($P(B) > 0$).
*   **Explain the Chain Rule:** It is used to calculate the joint probability of multiple events by multiplying conditional probabilities (e.g., $P(A \cap B \cap C) = P(A) \cdot P(B|A) \cdot P(C|A \cap B)$).
*   **How does a Venn diagram help explain conditional probability?** It shows that $P(A | B)$ is the proportion of the area of $B$ that is shared with $A$.
*   **What is the relationship between $P(A \cap B)$ and $P(B \cap A)$?** They are identical; the intersection of sets is commutative.

## Diagram Recreation Prompt
Create a clean educational slide titled "Conditional Probability" in a professional blue font. Below the title, add a horizontal green separator line. Present the following four equations centered on the page, each with a right-aligned index number in parentheses:
1. $P(A | B) = \frac{P(A \cap B)}{P(B)}$
2. $P(A | B) P(B) = P(A \cap B)$
3. $P(A \cap B \cap C) = P(A) P(B | A) P(C | A \cap B)$
4. $P(B | A) = \frac{P(B \cap A)}{P(A)}$
Include brief explanatory text between the equations as seen in the original: "The conditional probability of an event A assuming that B has occurred...", "which can be proven directly using a Venn diagram...", "which can be generalized to...", and "Rearranging (1) gives...". Use a clean white background and highlight the words "event" and "Venn diagram" in teal.

## Diagram Data
*   **Title:** Conditional Probability
*   **Section 1 Text:** The conditional probability of an event A assuming that B has occurred, denoted P(A | B), equals
*   **Equation 1:** P(A | B) = P(A ∩ B) / P(B)
*   **Section 2 Text:** which can be proven directly using a Venn diagram. Multiplying through, this becomes
*   **Equation 2:** P(A | B) P(B) = P(A ∩ B)
*   **Section 3 Text:** which can be generalized to
*   **Equation 3:** P(A ∩ B ∩ C) = P(A) P(B | A) P(C | A ∩ B)
*   **Section 4 Text:** Rearranging (1) gives
*   **Equation 4:** P(B | A) = P(B ∩ A) / P(A)
