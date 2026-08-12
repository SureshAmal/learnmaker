# Unit 1 Page 103 Image Understanding

## Page Overview
The purpose of this slide is to define and demonstrate the concept of **Conditional Probability**. It provides a formal definition, standard mathematical notation, the core formula, and a practical example involving calendar dates (birthdays) to illustrate how the occurrence of one event affects the probability of another.

## Visible Text
**Example:**

**Conditional Probability**
*   **$\mathcal{D}ef$** A **conditional probability** of an event is a probability obtained with the additional information that some other event has already occurred.
*   **Notation:** $P(B | A)$ denotes the conditional probability that event B occurs, given that event A has already occurred.
*   **Formula:** $P(B | A) = \frac{P(A \text{ and } B)}{P(A)}$
*   **$\mathcal{E}x$:** Let $A =$ Today is your birthday and $B =$ Your birthday is in this month.
    *   (a) Are events $A$ and $B$ dependent?
    *   Yes, events A and B are dependent.
    *   (b) $P(A) = 1/31$
    *   (c) $P(A|B) = (1/31) / 1 = 1/31$
    *   (d) $P(B|A) = (1/31) / (1/31) = 1$

## Visual Layout
*   **Title:** The word "Example:" is written in a large, bold, light-blue sans-serif font at the top left.
*   **Header Graphic:** A dark gray horizontal bar with a pointed arrow-like end sits to the left of the title.
*   **Background:** The background is a very light blue-to-white gradient. On the far left, there are several thin, dark blue curved lines that sweep upwards.
*   **Content Alignment:** The text is left-aligned with standard margins.
*   **Typography:** 
    *   Section headers like "Conditional Probability", "Notation:", and "Formula:" are in bold.
    *   The definition uses a stylized script "$\mathcal{D}ef$" and the example uses a stylized script "$\mathcal{E}x$".
    *   Mathematical variables ($A, B, P$) are italicized.
*   **Spacing:** There is clear vertical spacing between the definition, notation, formula, and the example steps to ensure readability.

## Diagram Type
This is a **formula derivation and text-based instructional slide**. It does not contain flowcharts or plots but uses structured text and mathematical equations to convey a logical progression from theory to application.

## Diagram / Visual Explanation
No graphical diagram is present. The visual hierarchy relies on text formatting (bolding and indentation) to guide the reader from the general rule to a specific calculation.

## Math / Formula / Curve Notes
*   **$P(B | A)$**: Read as "Probability of B given A." It represents the likelihood of event B occurring under the condition that event A is known to have happened.
*   **$P(A \text{ and } B)$**: The joint probability that both events A and B occur simultaneously.
*   **$P(A)$**: The marginal probability of event A occurring.
*   **The Formula**: $P(B | A) = \frac{P(A \text{ and } B)}{P(A)}$. This shows that the conditional probability is the ratio of the joint probability to the probability of the condition.
*   **Example Calculation Breakdown (assuming a 31-day month):**
    *   **$P(A) = 1/31$**: The probability that today is your birthday (1 day out of 31).
    *   **$P(B) = 1$**: (Implicitly) If we are already considering "this month," the probability that your birthday is in this month is 1 (certainty) for the sake of this specific conditional logic.
    *   **$P(A|B) = (1/31) / 1 = 1/31$**: The probability today is your birthday, given it is your birthday month.
    *   **$P(B|A) = (1/31) / (1/31) = 1$**: The probability your birthday is this month, given that today is your birthday. If today is your birthday, it is 100% certain that your birthday falls within the current month.

## Table Description
No table is visible on this page.

## Concept Explanation
**Conditional Probability** is a fundamental concept in statistics and machine learning (especially in Bayesian networks and Naive Bayes classifiers). It adjusts the probability of an event based on new evidence.

1.  **Dependency:** Two events are dependent if the occurrence of one changes the probability of the other. In the example, knowing it is your birthday month ($B$) makes the probability of it being your birthday today ($A$) non-zero, whereas if it weren't your birthday month, $P(A)$ would be zero.
2.  **The "Given" Bar ($|$):** This vertical bar separates the event we are interested in (left) from the condition we already know to be true (right).
3.  **Sample Space Reduction:** Effectively, conditional probability reduces the sample space. Instead of looking at all possible days in a year, $P(A|B)$ looks only at the days within "this month."

## Exam / Viva Points
*   **Definition:** Be able to define conditional probability as the probability of an event given that another event has occurred.
*   **Formula:** Memorize $P(B|A) = \frac{P(A \cap B)}{P(A)}$. Note that $P(A)$ must be greater than 0.
*   **Notation:** Understand that the vertical bar $|$ means "given."
*   **Interpretation:** Explain why $P(B|A)$ is 1 in the birthday example. (If the condition "today is your birthday" is true, then the event "your birthday is this month" must also be true).
*   **Dependency:** Be prepared to explain that if $P(B|A) = P(B)$, the events are independent. If they are not equal, the events are dependent.

## Diagram Recreation Prompt
Create a clean, modern educational slide titled "Conditional Probability Example". 
- **Top Section:** Use a bold blue header. Define Conditional Probability clearly. 
- **Middle Section:** Display the formula $P(B | A) = \frac{P(A \text{ and } B)}{P(A)}$ inside a light-colored highlighted box (e.g., light yellow or pale blue). 
- **Bottom Section:** Present a worked example. Let Event A = "Today is your birthday" and Event B = "Your birthday is in this month". 
- **Step-by-step list:** 
  1. State that A and B are dependent. 
  2. Show $P(A) = 1/31$. 
  3. Show the calculation for $P(A|B)$. 
  4. Show the calculation for $P(B|A) = 1$. 
- **Style:** Use a professional sans-serif font, plenty of white space, and a subtle sidebar graphic to match a corporate or academic presentation style.

## Diagram Data
*   **Title:** Example:
*   **Section 1: Definition**
    *   Term: Conditional Probability
    *   Text: Probability obtained with additional information that another event occurred.
*   **Section 2: Notation & Formula**
    *   Notation: $P(B | A)$
    *   Formula: $P(B | A) = P(A \text{ and } B) / P(A)$
*   **Section 3: Example Problem**
    *   Event A: Today is your birthday.
    *   Event B: Your birthday is in this month.
    *   Question (a): Are they dependent? Answer: Yes.
    *   Calculation (b): $P(A) = 1/31$
    *   Calculation (c): $P(A|B) = (1/31) / 1 = 1/31$
    *   Calculation (d): $P(B|A) = (1/31) / (1/31) = 1$
