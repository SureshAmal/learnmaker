# Unit 1 Page 81 Image Understanding

## Page Overview
This slide provides a concrete example of a **Decision Tree** used for classification. The purpose is to demonstrate how a hierarchical structure of features can be used to categorize input data—in this case, likely characters or symbols—into specific classes based on their geometric and topological properties. It illustrates the flow from a root node through various decision points (internal nodes) to final classifications (leaf nodes).

## Visible Text
*   **Title:** Decision Trees
*   **Internal Nodes (Boxes):**
    *   #holes
    *   moment of inertia
    *   #strokes
    *   best axis direction
*   **Branch Labels (Decisions):**
    *   From #holes: 0, 1, 2
    *   From moment of inertia: < t, $\ge$ t (represented by a symbol next to 't')
    *   From best axis direction: 0, 60, 90
    *   From #strokes (left): 2, 4
    *   From #strokes (middle): 0, 1
    *   From #strokes (right): 0, 1
*   **Leaf Nodes (Red Text - Classifications):**
    *   -
    *   /
    *   1
    *   x
    *   w
    *   0
    *   A
    *   8
    *   B

## Visual Layout
*   **Title:** Centered at the top in a large, black sans-serif font.
*   **Structure:** A top-down hierarchical tree structure.
*   **Nodes:** Internal decision nodes are enclosed in rectangular black boxes.
*   **Branches:** Black arrows point from parent nodes to child nodes or leaf nodes. Labels for the decision criteria are placed next to the arrows.
*   **Leaf Nodes:** The final output classes are written in red text at the bottom of each terminal branch, without boxes.
*   **Color Palette:** Primarily black and white, with red used specifically to highlight the final classification results.
*   **Alignment:** The tree is centered on the page, branching out wider as it moves toward the bottom.

## Diagram Type
**Decision Tree.** It is a classic representation of a classification model where each internal node represents a "test" on an attribute (e.g., number of holes), each branch represents the outcome of the test, and each leaf node represents a class label (the final decision).

## Diagram / Visual Explanation
The diagram shows a classification process for symbols:
1.  **Root Node (#holes):** The process starts by counting the number of holes in the symbol.
    *   **If 0 holes:** Move to the "moment of inertia" node.
    *   **If 1 hole:** Move to the middle "#strokes" node.
    *   **If 2 holes:** Move to the rightmost "#strokes" node.
2.  **Path for 0 holes:**
    *   If **moment of inertia < t**, check "best axis direction".
        *   Direction 0 $\rightarrow$ **-** (minus sign)
        *   Direction 60 $\rightarrow$ **/** (forward slash)
        *   Direction 90 $\rightarrow$ **1** (number one)
    *   If **moment of inertia $\ge$ t**, check "#strokes".
        *   2 strokes $\rightarrow$ **x**
        *   4 strokes $\rightarrow$ **w**
3.  **Path for 1 hole:**
    *   Check "#strokes".
        *   0 strokes $\rightarrow$ **0** (number zero)
        *   1 stroke $\rightarrow$ **A**
4.  **Path for 2 holes:**
    *   Check "#strokes".
        *   0 strokes $\rightarrow$ **8** (number eight)
        *   1 stroke $\rightarrow$ **B**

## Math / Formula / Curve Notes
*   **t:** Represents a threshold value for the "moment of inertia" feature.
*   **0, 60, 90:** Represent angular degrees for the "best axis direction" feature.
*   **< t and $\ge$ t:** Inequality operators used to split the data based on a continuous numerical feature (moment of inertia).

## Table Description
No table is visible on this page.

## Concept Explanation
A **Decision Tree** is a supervised learning algorithm used for classification and regression. 
*   **Feature Selection:** The tree uses specific features (like `#holes` or `#strokes`) to partition the data. In this example, these are likely computer vision features extracted from images of characters.
*   **Internal Nodes:** These represent a choice or a test. For example, "How many holes does this shape have?"
*   **Branches:** These represent the possible answers to the test in the node above.
*   **Leaf Nodes:** These are the terminal points where no further splitting is possible. They provide the final predicted category (e.g., identifying the shape as an 'A' or an '8').
*   **Logic:** The tree follows a "if-then" logic. If a character has 1 hole and 1 stroke, then it is classified as an 'A'.

## Exam / Viva Points
*   **Root Node:** The topmost node in a decision tree, representing the first feature used for splitting.
*   **Splitting Criteria:** Decisions can be based on categorical values (0, 1, 2 holes) or numerical thresholds (moment of inertia < t).
*   **Classification Path:** To classify a new data point, you start at the root and follow the branches corresponding to the data point's features until a leaf node is reached.
*   **Feature Importance:** Features closer to the root (like #holes) are generally considered more discriminative for the dataset provided.
*   **Leaf Nodes:** These represent the final class labels and have no outgoing branches.

## Diagram Recreation Prompt
Create a clean, professional decision tree diagram for character recognition. 
- **Root Node:** A box labeled "#holes". 
- **Level 1 Branches:** Three arrows labeled "0", "1", and "2". 
- **Level 2 Nodes:** 
    - From "0": A box labeled "moment of inertia".
    - From "1": A box labeled "#strokes".
    - From "2": A box labeled "#strokes".
- **Level 3 Branches & Nodes:**
    - From "moment of inertia": Two arrows labeled "< t" and "$\ge$ t". The "< t" branch leads to a box labeled "best axis direction". The "$\ge$ t" branch leads to a box labeled "#strokes".
    - From middle "#strokes": Two arrows labeled "0" and "1" leading to red text labels "0" and "A".
    - From rightmost "#strokes": Two arrows labeled "0" and "1" leading to red text labels "8" and "B".
- **Level 4 Branches & Leaf Nodes:**
    - From "best axis direction": Three arrows labeled "0", "60", and "90" leading to red text labels "-", "/", and "1".
    - From leftmost "#strokes": Two arrows labeled "2" and "4" leading to red text labels "x" and "w".
- **Styling:** Use black lines and boxes, white background, and distinct red color for the final leaf node characters. Ensure the layout is balanced and hierarchical.

## Diagram Data
*   **Nodes:**
    *   Root: "#holes"
    *   Internal: "moment of inertia", "#strokes" (middle), "#strokes" (right), "best axis direction", "#strokes" (left)
    *   Leaves (Red): "-", "/", "1", "x", "w", "0", "A", "8", "B"
*   **Edges (Parent -> Child [Label]):**
    *   "#holes" -> "moment of inertia" [0]
    *   "#holes" -> "#strokes" (middle) [1]
    *   "#holes" -> "#strokes" (right) [2]
    *   "moment of inertia" -> "best axis direction" [< t]
    *   "moment of inertia" -> "#strokes" (left) [$\ge$ t]
    *   "best axis direction" -> "-" [0]
    *   "best axis direction" -> "/" [60]
    *   "best axis direction" -> "1" [90]
    *   "#strokes" (left) -> "x" [2]
    *   "#strokes" (left) -> "w" [4]
    *   "#strokes" (middle) -> "0" [0]
    *   "#strokes" (middle) -> "A" [1]
    *   "#strokes" (right) -> "8" [0]
    *   "#strokes" (right) -> "B" [1]
