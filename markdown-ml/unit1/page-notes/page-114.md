# Unit 1 Page 114 Image Understanding

## Page Overview
The purpose of this slide is to clarify the fundamental distinction between **Probability** and **Likelihood**, two concepts often confused in statistics and machine learning. It uses concise definitions and side-by-side visual comparisons of a normal distribution curve to illustrate that probability deals with predicting outcomes from a known model, while likelihood deals with estimating model parameters from observed data.

## Visible Text
*   **Difference between Likelihood and Probability:**
*   **Probability:** Given a **known model** and parameters, probability predicts future outcomes.
*   **Likelihood:** Given **observed data**, likelihood estimates the best parameters for a model.
*   **Probability** (Heading for the left graph)
*   **Likelihood** (Heading for the right graph)
*   **X-axis labels (both graphs):** 155, 160, 165, 170, 175, 180, 185

## Visual Layout
*   **Title:** Large, blue, bold text at the top left.
*   **Content Blocks:** Two bullet points follow the title. Key terms "**known model**" and "**observed data**" are highlighted in red bold text.
*   **Comparison Box:** A large white rectangular area at the bottom contains two side-by-side graphs.
*   **Colors:** 
    *   Background: Light blue gradient with thin, dark blue curved lines on the left.
    *   Title: Blue.
    *   Text: Black with red highlights.
    *   Graphs: Gray curves on a light gray background.
*   **Visual Hierarchy:** The title establishes the topic, the text provides the theoretical definitions, and the bottom graphs provide the visual intuition.
*   **Graphic Element:** A dark gray arrow-like chevron points toward the title from the left margin.

## Diagram Type
This is a **comparison diagram** using **mathematical graphs** (specifically, Normal Distribution/Gaussian curves). It is designed to show how the same mathematical curve is interpreted differently depending on whether one is calculating probability or likelihood.

## Diagram / Visual Explanation
The diagram consists of two identical Normal Distribution curves centered at 170.

1.  **Probability Graph (Left):**
    *   **Visual:** A specific region under the curve between the x-axis values of approximately 175 and 180 is shaded in dark gray.
    *   **Meaning:** In probability, we assume the model (the curve) is fixed. The shaded **area** represents the probability of a random variable falling within that specific range (e.g., the probability that a person's height is between 175cm and 180cm).

2.  **Likelihood Graph (Right):**
    *   **Visual:** Instead of a shaded area, there is a specific point marked with an "**x**" on the curve at $x \approx 177$. A vertical line connects the x-axis to this point, and a horizontal line connects the y-axis to this point.
    *   **Meaning:** In likelihood, we have an observed data point (the 'x'). We use the **y-value** (the height of the curve at that point) to determine how well this specific model (this specific curve) explains the observed data. Likelihood is about finding the curve (parameters) that maximizes this y-value for the given data.

## Math / Formula / Curve Notes
*   **Curve Type:** Both graphs show a **Normal (Gaussian) Distribution** curve.
*   **X-axis:** Represents a continuous variable, likely height in centimeters, ranging from 155 to 185.
*   **Mean ($\mu$):** The peak of the curve is at 170.
*   **Probability Calculation:** Represented by the integral of the probability density function (PDF) over an interval: $P(a < X < b) = \int_{a}^{b} f(x|\theta) dx$. This corresponds to the **shaded area**.
*   **Likelihood Calculation:** Represented by the value of the PDF at a specific observed point $x$: $L(\theta|x) = f(x|\theta)$. This corresponds to the **vertical height (y-value)** of the curve at the observed data point.

## Table Description
No table is visible on this page.

## Concept Explanation
*   **Probability (Forward Process):** You start with a known population or model (e.g., "I know the average height is 170cm with a certain standard deviation"). You then ask: "What is the chance of picking someone and finding their height is between 175cm and 180cm?" You are predicting data from a model.
*   **Likelihood (Backward Process):** You start with data you have already collected (e.g., "I measured a person and they are 177cm tall"). You then look at different possible models (different means or standard deviations) and ask: "Which model makes this specific measurement of 177cm most likely to occur?" You are estimating the model parameters from the data.

## Exam / Viva Points
*   **Definition of Probability:** Predicting the frequency of outcomes given a fixed set of parameters/model.
*   **Definition of Likelihood:** Evaluating how well different parameter values explain the observed data.
*   **Visual Distinction:** Probability is represented by the **area** under the curve; Likelihood is represented by the **y-axis value** (point on the curve) for a specific observation.
*   **The "Knowns":** In probability, the **parameters** are known. In likelihood, the **data** is known.
*   **Directionality:** Probability is a "forward" inference (Model $\rightarrow$ Data). Likelihood is a "backward" inference (Data $\rightarrow$ Model).

## Diagram Recreation Prompt
Create a high-resolution comparison graphic titled "Probability vs. Likelihood". 
- On the left, show a standard Normal Distribution curve (mean=170) with the area between x=175 and x=180 shaded in a distinct color (e.g., blue). Label this graph "Probability: Area under the curve". 
- On the right, show the exact same Normal Distribution curve. Mark a single point on the curve at x=177 with a bold 'X'. Draw a dashed vertical line from the x-axis to the 'X' and a dashed horizontal line from the y-axis to the 'X'. Label this graph "Likelihood: Point on the curve". 
- Use a clean, professional sans-serif font. Ensure the x-axis is clearly labeled from 155 to 185. Use a white background for the graphs and a light professional accent color for the slide background.

## Diagram Data
*   **Title:** Difference between Likelihood and Probability:
*   **Bullet 1:** Probability: Given a known model and parameters, probability predicts future outcomes.
*   **Bullet 2:** Likelihood: Given observed data, likelihood estimates the best parameters for a model.
*   **Graph 1 (Probability):**
    *   Type: Normal Distribution Curve
    *   Mean: 170
    *   X-axis Range: 155 to 185
    *   Annotation: Shaded area between x=175 and x=180.
*   **Graph 2 (Likelihood):**
    *   Type: Normal Distribution Curve
    *   Mean: 170
    *   X-axis Range: 155 to 185
    *   Annotation: Point 'x' at x $\approx$ 177, with vertical and horizontal projection lines.
