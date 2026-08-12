# Unit 1 Page 101 Image Understanding

## Page Overview
The purpose of this slide is to introduce the concept of **Conditional Probability**. It provides a formal definition and uses a concrete, visual example involving marbles in a bag to demonstrate how the probability of an event changes based on a preceding event (sampling without replacement).

## Visible Text
*   **Main Title:** Conditional Probability:
*   **Sub-title (in blue header):** Conditional Probability
*   **Definition Text:** 
    *   "Conditional probability is the probability of an event occurring based on the occurrence of another event. Conditional probability is a fundamental aspect of probability theory."
    *   "Conditional probability questions often involve picking two objects from a set. This is because once you have picked the first object, the probabilities change for the second pick, based on the outcome of the first pick."
*   **Example Label:** Example (with a pencil icon)
*   **Left Comparison Box:**
    *   "You have a bag containing 3 red marbles and 4 blue marbles."
    *   (Visual of 7 marbles)
    *   "The probabilities of picking each color marble are"
    *   $P(\text{red marble}) = \frac{3}{7}$
    *   $P(\text{blue marble}) = \frac{4}{7}$
*   **Right Comparison Box:**
    *   "If you picked out one red marble, there would be 2 red marbles and 4 blue marbles left."
    *   (Visual of 7 marbles with one red crossed out)
    *   "The probabilities would now be"
    *   $P(\text{red marble}) = \frac{2}{6}$
    *   $P(\text{blue marble}) = \frac{4}{6}$
*   **Footer Text:** "The probabilities are calculated based on what has already occurred."
*   **Logo:** THIRD SPACE LEARNING (bottom right)

## Visual Layout
*   **Header:** A large light blue title at the very top. Below it, a dark blue rounded rectangle serves as a secondary header for the main content area.
*   **Content Area:** A large white rounded container with a thin blue border.
*   **Text Blocks:** The top half contains three paragraphs of explanatory text in a standard sans-serif font.
*   **Comparison Boxes:** Two side-by-side white boxes with blue outlines illustrate the "before" and "after" states of a probability experiment.
*   **Visual Aids:** Inside the boxes, colored circles (red and cyan-blue) represent marbles. A red 'X' is used in the second box to denote the removal of an item.
*   **Mathematical Notation:** Probabilities are written using standard $P(\text{event})$ notation with fractions.
*   **Branding:** A logo with two overlapping circles (yellow and blue) and the text "THIRD SPACE LEARNING" is in the bottom right corner.
*   **Background:** The overall background is light grey with abstract dark grey curved lines on the left side.

## Diagram Type
This page uses a **Comparison Diagram** (specifically a "Before and After" illustration). It is used to show the state of a system (a bag of marbles) before an event and how that state—and the resulting mathematical probabilities—change after a specific condition is met.

## Diagram / Visual Explanation
*   **Left Box (Initial State):**
    *   **Visual:** Shows 7 marbles: 3 red and 4 blue.
    *   **Logic:** The total sample space ($n$) is 7. The number of favorable outcomes for red is 3, and for blue is 4.
    *   **Result:** Probabilities are calculated as $\frac{\text{favorable}}{\text{total}}$.
*   **Right Box (Conditional State):**
    *   **Visual:** Shows the same 7 marbles, but one red marble has a large black 'X' over it.
    *   **Logic:** This represents the condition "given that a red marble was already picked." Because the marble was not replaced, the total sample space ($n$) decreases to 6. The number of remaining red marbles decreases to 2. The number of blue marbles remains 4.
    *   **Result:** The new probabilities reflect this reduced sample space: $P(\text{red}) = \frac{2}{6}$ and $P(\text{blue}) = \frac{4}{6}$.

## Math / Formula / Curve Notes
*   **$P(\text{red marble}) = \frac{3}{7}$**: Initial probability. 3 red marbles divided by 7 total marbles.
*   **$P(\text{blue marble}) = \frac{4}{7}$**: Initial probability. 4 blue marbles divided by 7 total marbles.
*   **$P(\text{red marble}) = \frac{2}{6}$**: Conditional probability. After 1 red is removed, 2 red remain out of a new total of 6.
*   **$P(\text{blue marble}) = \frac{4}{6}$**: Conditional probability. After 1 red is removed, all 4 blue remain, but the total is now 6.
*   **General Principle:** The denominator (sample space) changes when an item is removed without replacement. The numerator changes if the item removed matches the event being calculated.

## Table Description
No table is visible on this page.

## Concept Explanation
**Conditional Probability** is the likelihood of an event occurring, given that another event has already happened. In mathematical notation, this is written as $P(A|B)$, read as "the probability of $A$ given $B$."

This slide illustrates **Dependent Events**. In dependent events, the outcome of the first trial affects the outcome of the second. The most common example is "sampling without replacement." 
1.  **Sample Space Reduction:** When you take an item out of a set and don't put it back, the total number of possible outcomes for the next draw is reduced by one.
2.  **Probability Shift:** Because the total (denominator) has changed, the probability of every subsequent event changes. If the item removed was of a specific type (e.g., a red marble), the probability of picking that same type again decreases even further because the numerator also dropped.

## Exam / Viva Points
*   **Definition:** Conditional probability is the probability of an event $A$ occurring given that event $B$ has already occurred.
*   **Notation:** Represented as $P(A|B)$.
*   **Dependent vs. Independent:** Explain that the marble example shows dependent events because the first draw changes the probability of the second draw.
*   **Calculation:** Be prepared to calculate new probabilities after an item is removed from a set. Remember to subtract 1 from the total (denominator) and, if applicable, 1 from the specific category (numerator).
*   **Formula (Advanced):** While not on the slide, a student should know the formula $P(A|B) = \frac{P(A \cap B)}{P(B)}$.

## Diagram Recreation Prompt
Create a educational slide titled "Conditional Probability" with a clean, modern layout. 
- Top section: A text box defining conditional probability as the likelihood of an event based on a prior event. 
- Middle section: Two side-by-side comparison panels. 
- Left Panel: Title "Initial State". Show a cluster of 3 red circles and 4 blue circles. Below them, write $P(\text{Red}) = 3/7$ and $P(\text{Blue}) = 4/7$. 
- Right Panel: Title "After picking 1 Red marble". Show the same cluster, but put a prominent 'X' over one red circle. Below them, write $P(\text{Red}) = 2/6$ and $P(\text{Blue}) = 4/6$. 
- Use a professional color palette (e.g., Navy blue headers, light blue accents, white background). 
- Add a footer note: "The sample space changes based on previous outcomes."

## Diagram Data
*   **Title:** Conditional Probability
*   **Intro Text:** Definition of conditional probability and its application in sequential picking.
*   **Comparison Box 1 (Initial):**
    *   Items: 3 Red Marbles, 4 Blue Marbles.
    *   Total: 7.
    *   Math: $P(R) = 3/7$, $P(B) = 4/7$.
*   **Comparison Box 2 (Conditional):**
    *   Condition: 1 Red Marble removed.
    *   Remaining Items: 2 Red Marbles, 4 Blue Marbles.
    *   Total: 6.
    *   Math: $P(R) = 2/6$, $P(B) = 4/6$.
*   **Conclusion:** Probabilities are dependent on prior events.
