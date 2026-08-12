# Unit 1 Page 68 Image Understanding

## Page Overview
The purpose of this slide is to provide a high-level classification of **Ensemble Learning** techniques. It organizes the various methods into a hierarchical structure, distinguishing between ensembles that use the same type of base model (Homogeneous) versus those that use different types of base models (Heterogeneous). This serves as a foundational roadmap for students to understand the landscape of ensemble methods in machine learning.

## Visible Text
*   **Title:** Types of Ensemble learning
*   **Root Node:** Ensemble Learning
*   **Level 1 Categories:**
    *   Homogeneous ensemble method
    *   Heterogeneous ensemble method
*   **Level 2 Specific Methods:**
    *   Bagging (under Homogeneous)
    *   Boosting (under Homogeneous)
    *   Stacking (under Heterogeneous)

## Visual Layout
*   **Title:** Positioned at the top left in a large, bold, blue sans-serif font.
*   **Background:** A light grey central rectangular area contains the diagram. The overall slide background has a subtle pale green gradient on the right and abstract brown/grey decorative lines on the far left.
*   **Diagram Structure:** A top-down tree hierarchy (taxonomy).
*   **Color Coding:**
    *   **Blue Box:** Represents the primary concept (Ensemble Learning).
    *   **Green Boxes:** Represent the primary sub-categories based on model uniformity.
    *   **Yellow/Orange Boxes:** Represent specific algorithmic families.
*   **Connectors:** Thin, black, curved arrows originate from the bottom center of parent boxes and point to the top center of child boxes.
*   **Alignment:** The diagram is horizontally centered within the grey content block.

## Diagram Type
This is a **Taxonomy / Classification Hierarchy Diagram**. It is used to categorize a broad concept (Ensemble Learning) into specific sub-types based on defining characteristics (homogeneity vs. heterogeneity), eventually leading to specific well-known techniques.

## Diagram / Visual Explanation
The diagram illustrates the breakdown of Ensemble Learning:
1.  **Ensemble Learning (Root):** The starting point, representing the general practice of combining multiple models.
2.  **First Level Split:** The field is divided based on whether the base learners are of the same type or different types.
    *   **Homogeneous ensemble method:** This branch indicates methods where all individual models in the ensemble are of the same algorithm type (e.g., all are Decision Trees).
    *   **Heterogeneous ensemble method:** This branch indicates methods where the individual models can be of different algorithm types (e.g., a mix of SVM, Logistic Regression, and k-NN).
3.  **Second Level Split (Specific Techniques):**
    *   From **Homogeneous**, the diagram branches into **Bagging** (Bootstrap Aggregating) and **Boosting**. These are the two most common ways to combine identical base learners.
    *   From **Heterogeneous**, the diagram branches into **Stacking** (Stacked Generalization), which is the primary method for combining diverse base learners.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page.

## Table Description
No table is visible on this page.

## Concept Explanation
**Ensemble Learning** is a machine learning strategy where multiple models (often called "base learners" or "weak learners") are trained to solve the same problem and then combined to produce a single, more robust prediction. The goal is typically to achieve better predictive performance than any single constituent model could alone.

*   **Homogeneous Ensembles:** These use multiple instances of the **same algorithm**.
    *   **Bagging (Bootstrap Aggregating):** Focuses on reducing **variance**. It trains multiple models in parallel on different random subsets of the training data (sampled with replacement). The final prediction is usually an average (for regression) or a majority vote (for classification). Example: Random Forest.
    *   **Boosting:** Focuses on reducing **bias**. It trains models sequentially. Each new model attempts to correct the errors made by the previous models in the sequence by giving more weight to misclassified instances. Examples: AdaBoost, Gradient Boosting, XGBoost.
*   **Heterogeneous Ensembles:** These use **different algorithms** as base learners.
    *   **Stacking (Stacked Generalization):** Different types of models (e.g., a Decision Tree, an SVM, and a Neural Network) are trained on the dataset. Their individual predictions are then used as input features for a "meta-model" (or "blender") which learns how to best combine these predictions to make the final output.

## Exam / Viva Points
*   **Definition:** What is Ensemble Learning? (Combining multiple models to improve performance).
*   **Classification Criteria:** What is the difference between Homogeneous and Heterogeneous ensembles? (Homogeneous uses the same base algorithm; Heterogeneous uses different base algorithms).
*   **Bagging vs. Boosting:** Both are homogeneous. Bagging works in parallel to reduce variance; Boosting works sequentially to reduce bias.
*   **Stacking:** It is a heterogeneous method that uses a meta-learner to combine predictions from diverse base models.
*   **Examples:** Be prepared to name a specific algorithm for each category (e.g., Random Forest for Bagging, XGBoost for Boosting).

## Diagram Recreation Prompt
Create a professional hierarchical taxonomy diagram titled "Types of Ensemble learning". 
- Place a central root node at the top labeled "Ensemble Learning" in a blue rounded rectangle.
- Draw two curved arrows downward to a second level.
- The left node should be "Homogeneous ensemble method" and the right node "Heterogeneous ensemble method", both in green rounded rectangles.
- From "Homogeneous ensemble method", draw two curved arrows downward to "Bagging" and "Boosting" in yellow rounded rectangles.
- From "Heterogeneous ensemble method", draw one curved arrow downward to "Stacking" in a yellow rounded rectangle.
- Use a clean, light-colored background. Ensure all text is legible and boxes are evenly spaced.

## Diagram Data
*   **Nodes:**
    *   Node 1 (Root): "Ensemble Learning", Color: Blue
    *   Node 2 (Level 1, Left): "Homogeneous ensemble method", Color: Green
    *   Node 3 (Level 1, Right): "Heterogeneous ensemble method", Color: Green
    *   Node 4 (Level 2, under Node 2): "Bagging", Color: Yellow
    *   Node 5 (Level 2, under Node 2): "Boosting", Color: Yellow
    *   Node 6 (Level 2, under Node 3): "Stacking", Color: Yellow
*   **Edges (Arrows):**
    *   Node 1 -> Node 2
    *   Node 1 -> Node 3
    *   Node 2 -> Node 4
    *   Node 2 -> Node 5
    *   Node 3 -> Node 6
