# Unit 1 Page 115 Image Understanding

## Page Overview
This slide provides a conceptual and mathematical comparison between **Probability** and **Likelihood** in statistics and machine learning. It aims to clarify the directional relationship between models and data: probability predicts data given a model, while likelihood evaluates a model given observed data.

## Visible Text
*   **Top Diagram:**
    *   Probability
    *   Model
    *   Outcomes
    *   Likelihood
*   **Bottom Left Section (Probability):**
    *   **Probability**
    *   Area under curve between 5 and 10
    *   Y-axis: Probability density
    *   X-axis: Values of x (0, 5, 10, 15, 20, 25, 30)
    *   "What is the *probability* that $5 \le x \le 10$ given a normal distribution with $\mu = 13$ and $\sigma = 4$? Answer: 0.204"
    *   "What is the *probability* that $-1000 \le x \le 1000$ given a normal distribution with $\mu = 13$ and $\sigma = 4$? Answer: 1.000"
*   **Bottom Right Section (Likelihood):**
    *   **Likelihood**
    *   Height of curve at $x = 10$
    *   Height of curve at $x = 14$
    *   Y-axis: Probability density
    *   X-axis: Values of x (0, 5, 10, 15, 20, 25, 30)
    *   "What is the *likelihood* that $\mu = 13$ and $\sigma = 4$ if you observed a value of"
    *   "(a) $x = 10$ (answer: the *likelihood* is 0.075)"
    *   "(b) $x = 14$ (answer: the *likelihood* is 0.097)"
    *   "Conclusion: if the observed value was 14, it is *more likely* that the parameters are $\mu = 13$ and $\sigma = 4$, because 0.097 is higher than 0.075."

## Visual Layout
*   **Top Section:** A conceptual cycle diagram enclosed in a black border. It features a purple box for "Model" and a blue box for "Outcomes" connected by two curved arrows forming a loop. The top arrow is labeled "Probability" and the bottom "Likelihood" in red text.
*   **Bottom Section:** Divided into two vertical columns by a thin grey line.
    *   **Left Column:** Focuses on Probability. It contains a normal distribution plot with a green shaded area and explanatory text below.
    *   **Right Column:** Focuses on Likelihood. It contains a similar normal distribution plot with vertical indicators for specific points and explanatory text below.
*   **Color Palette:** Purple and blue for the main entities (Model/Outcomes), red for the core concepts, and green for highlighting the area in the probability graph.

## Diagram Type
The slide contains two types of visuals:
1.  **Relationship/Cycle Diagram (Top):** Shows the reciprocal relationship between models and outcomes.
2.  **Mathematical Graphs (Bottom):** Two normal distribution curves (Probability Density Functions) used to illustrate the geometric interpretation of probability (area) vs. likelihood (height).

## Diagram / Visual Explanation
*   **Top Cycle Diagram:**
    *   **Model $\rightarrow$ Outcomes (via Probability):** This represents the forward process. If we know the model parameters, we use probability to predict what outcomes are likely to occur.
    *   **Outcomes $\rightarrow$ Model (via Likelihood):** This represents the inverse process. Given observed data (outcomes), we use likelihood to determine which model parameters are most consistent with that data.
*   **Bottom Left (Probability Graph):**
    *   The graph shows a bell curve. An arrow points to a green shaded region between $x=5$ and $x=10$.
    *   This visualizes that **probability is the area under the curve** for a specific interval of data.
*   **Bottom Right (Likelihood Graph):**
    *   The graph shows the same bell curve. Two vertical dashed lines extend from the x-axis ($x=10$ and $x=14$) to the curve.
    *   This visualizes that **likelihood is the height of the curve** (the y-value) at a specific observed data point.

## Math / Formula / Curve Notes
*   **Normal Distribution Curve:** Both graphs represent the Probability Density Function (PDF) of a normal distribution: $f(x | \mu, \sigma) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}(\frac{x-\mu}{\sigma})^2}$ with parameters $\mu = 13$ and $\sigma = 4$.
*   **Probability Calculation:**
    *   $P(5 \le x \le 10) = \int_{5}^{10} f(x | \mu=13, \sigma=4) dx = 0.204$. This is the area of the green region.
    *   $P(-\infty < x < \infty) = 1.000$. The text uses $-1000$ to $1000$ as a practical approximation for the entire area under the curve.
*   **Likelihood Calculation:**
    *   Likelihood $L(\mu, \sigma | x)$ is equal to the PDF value at $x$.
    *   For $x=10$: $L(13, 4 | 10) = f(10 | 13, 4) \approx 0.075$.
    *   For $x=14$: $L(13, 4 | 14) = f(14 | 13, 4) \approx 0.097$.
*   **Comparison:** Because $0.097 > 0.075$, the model with $\mu=13$ is a better fit for an observation of 14 than for an observation of 10.

## Table Description
No table is visible on this page.

## Concept Explanation
*   **Probability** is used when the model parameters ($\mu, \sigma$) are fixed and known. It answers: "Given this model, what is the chance of seeing data in this range?" It is calculated as the integral (area) over a range of values.
*   **Likelihood** is used when the data ($x$) is fixed and observed. It answers: "Given this specific data point, how well do these model parameters explain it?" It is the value of the PDF at that specific point.
*   In Machine Learning, **Maximum Likelihood Estimation (MLE)** is a method to find the parameters that maximize the likelihood of the observed training data.

## Exam / Viva Points
*   **Definition:** Probability is the area under the PDF for a range; Likelihood is the height of the PDF at a point.
*   **Directionality:** Probability goes from Model to Data. Likelihood goes from Data to Model.
*   **Fixed vs. Variable:** In probability, parameters are fixed and data is variable. In likelihood, data is fixed and parameters are variable.
*   **Total Probability:** The total area under a probability density curve must always equal 1.0.
*   **Interpretation:** A higher likelihood value for a set of parameters means those parameters are more plausible given the observed data.

## Diagram Recreation Prompt
Create a high-resolution educational slide divided into two horizontal halves.
**Top Half:** A cycle diagram. Place a purple rounded rectangle labeled "Model" on the left and a blue rounded rectangle labeled "Outcomes" on the right. Connect them with two thick black curved arrows. The top arrow (Model to Outcomes) should have the label "Probability" in bold red text above it. The bottom arrow (Outcomes to Model) should have the label "Likelihood" in bold red text below it.
**Bottom Half:** Split into two columns.
- **Left Column:** Title "Probability". Draw a normal distribution curve ($\mu=13, \sigma=4$). Shade the area between $x=5$ and $x=10$ in green. Add an arrow pointing to the shaded area labeled "Area under curve between 5 and 10". Below the graph, add text: "P(5 ≤ x ≤ 10 | μ=13, σ=4) = 0.204".
- **Right Column:** Title "Likelihood". Draw the same normal distribution curve. Add two vertical dashed lines at $x=10$ and $x=14$ reaching the curve. Label the intersection points with "Height at x=10 (0.075)" and "Height at x=14 (0.097)". Below the graph, add text: "Conclusion: x=14 is more likely for this model than x=10."
Use a clean, white background with professional sans-serif fonts.

## Diagram Data
*   **Cycle Diagram Nodes:**
    *   Node A: "Model", Style: Purple border, rounded.
    *   Node B: "Outcomes", Style: Blue border, rounded.
*   **Cycle Diagram Edges:**
    *   Edge A $\rightarrow$ B: Label "Probability", Color: Red.
    *   Edge B $\rightarrow$ A: Label "Likelihood", Color: Red.
*   **Probability Graph Data:**
    *   Type: Normal Distribution PDF.
    *   Parameters: Mean ($\mu$) = 13, Std Dev ($\sigma$) = 4.
    *   X-axis range: [0, 30].
    *   Annotation: Shaded area from $x=5$ to $x=10$.
*   **Likelihood Graph Data:**
    *   Type: Normal Distribution PDF.
    *   Parameters: Mean ($\mu$) = 13, Std Dev ($\sigma$) = 4.
    *   X-axis range: [0, 30].
    *   Points: $(10, 0.075)$, $(14, 0.097)$.
