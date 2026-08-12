# Unit 1 Page 78 Image Understanding

## Page Overview
This slide, titled **"Feature extraction methods,"** provides a conceptual and visual comparison between two primary techniques for dimensionality reduction in machine learning: **Feature Extraction** and **Feature Selection**. It further categorizes these methods into **Supervised** and **Unsupervised** approaches, explaining their underlying objectives and providing classic examples like PCA and LDA.

## Visible Text
*   **Title:** Feature extraction methods
*   **Sub-headings (Red):**
    *   Feature extraction
    *   Feature selection
*   **Diagram Labels:**
    *   Inputs: $m_1, m_2, \dots, m_k$
    *   Transformation functions: $\varphi_1, \varphi_2, \dots, \varphi_n$
    *   Outputs: $x_1, x_2, \dots, x_n$
*   **Main Text:**
    *   Problem can be expressed as optimization of parameters of featrure extractor.
    *   **Supervised methods:** objective function is a criterion of separability (discriminability) of labeled examples, e.g., linear discriminat analysis (LDA).
    *   **Unsupervised methods:** lower dimesional representation which preserves important characteristics of input data is sought for, e.g., principal component analysis (PCA).

*(Note: The slide contains minor typos: "featrure", "discriminat", and "dimesional".)*

## Visual Layout
*   **Header:** Large black title at the top center.
*   **Comparison Section:** Two side-by-side diagrams occupy the middle of the slide.
    *   The left diagram represents "Feature extraction" with red labeling.
    *   The right diagram represents "Feature selection" with red labeling.
*   **Text Section:** Three blocks of black text at the bottom explain the mathematical framing and the two main categories of methods.
*   **Styling:** The background is white with a decorative dark gray arrow-like shape on the top left and light blue curved lines on the bottom left. The diagrams use simple black lines, nodes (triangles/circles), and boxes.

## Diagram Type
The main visual is a **Comparison Architecture Diagram**. It uses a node-and-link structure to illustrate the flow of data from a high-dimensional input space to a lower-dimensional output space, highlighting the structural difference between "extracting" new features versus "selecting" existing ones.

## Diagram / Visual Explanation
### 1. Feature Extraction (Left Diagram)
*   **Input Layer:** A vertical column of nodes representing original features $m_1$ through $m_k$.
*   **Transformation Layer:** A middle column of rectangular boxes labeled $\varphi_1, \varphi_2, \dots, \varphi_n$.
*   **Output Layer:** A final column of nodes representing the new reduced features $x_1$ through $x_n$.
*   **Process:** Every input node is connected to every transformation box. This indicates that each new feature $x_j$ is a function (combination) of all original features. The mapping is $x = \Phi(m)$.

### 2. Feature Selection (Right Diagram)
*   **Input Layer:** A vertical column of nodes representing original features $m_1$ through $m_k$.
*   **Output Layer:** A final column of nodes representing the selected features $x_1$ through $x_n$.
*   **Process:** Direct arrows point from specific input nodes to specific output nodes. There are no transformation boxes. This indicates that the output is simply a subset of the original features. The mapping is $x \subset m$.

## Math / Formula / Curve Notes
While no complex equations are written out, the slide uses mathematical notation to define the problem:
*   **$m_k$**: Represents the dimensionality of the original input space.
*   **$x_n$**: Represents the dimensionality of the reduced output space (where $n < k$).
*   **$\varphi$**: Represents the transformation function or parameters that are optimized to map input to output.
*   **Optimization:** The text states the problem is an "optimization of parameters," implying finding a set of $\varphi$ that minimizes an error or maximizes a criterion (like variance or class separation).

## Table Description
No table is visible on this page.

## Concept Explanation
Dimensionality reduction is the process of reducing the number of random variables under consideration. This slide breaks it down into two strategies:

1.  **Feature Extraction:** This creates entirely new features. Imagine you have "height" and "weight"; feature extraction might create a new feature called "Body Mass Index." It transforms the data into a new coordinate system.
    *   **Unsupervised (PCA):** Finds directions (principal components) that maximize the variance in the data without looking at labels.
    *   **Supervised (LDA):** Finds directions that maximize the distance between different classes while minimizing the distance within each class.

2.  **Feature Selection:** This simply picks the "best" features from the original set and throws the rest away. If you have 100 measurements but only 5 are relevant to your prediction, you select those 5.

## Exam / Viva Points
*   **Distinguish between Extraction and Selection:** Extraction creates new features via transformation ($\varphi$); Selection picks a subset of original features.
*   **Goal of Supervised Methods:** To maximize the **separability** (discriminability) between classes. Example: **LDA**.
*   **Goal of Unsupervised Methods:** To preserve the **intrinsic characteristics** or variance of the data. Example: **PCA**.
*   **Dimensionality Relationship:** In both cases, the goal is to move from a high-dimensional space ($k$) to a lower-dimensional space ($n$), where $n < k$.
*   **Optimization:** Dimensionality reduction is framed as an optimization problem where we tune parameters to satisfy a specific objective function.

## Diagram Recreation Prompt
Create a professional comparison slide for "Feature Extraction vs. Feature Selection."
*   **Layout:** Two side-by-side panels.
*   **Left Panel (Feature Extraction):** Title "Feature Extraction" in red. Draw a column of 5 circular input nodes ($m_1 \dots m_k$). Draw a middle column of 3 square boxes ($\varphi_1 \dots \varphi_n$). Draw lines connecting every input node to every square box. Draw arrows from each box to a final column of 3 output nodes ($x_1 \dots x_n$).
*   **Right Panel (Feature Selection):** Title "Feature Selection" in red. Draw a column of 5 circular input nodes ($m_1 \dots m_k$). Draw a column of 3 output nodes ($x_1 \dots x_n$). Draw direct arrows from the 1st, 3rd, and 5th input nodes to the 1st, 2nd, and 3rd output nodes respectively.
*   **Footer Text:** Include two bullet points: "Supervised: Focus on class separability (e.g., LDA)" and "Unsupervised: Focus on data variance/characteristics (e.g., PCA)."
*   **Colors:** Use a clean, modern color palette (e.g., blue for nodes, light gray for boxes, red for titles).

## Diagram Data
*   **Title:** Feature extraction methods
*   **Left Diagram (Extraction):**
    *   Nodes: Input ($m_1, m_2, \dots, m_k$), Transform ($\varphi_1, \varphi_2, \dots, \varphi_n$), Output ($x_1, x_2, \dots, x_n$).
    *   Edges: Fully connected between Input and Transform; One-to-one between Transform and Output.
*   **Right Diagram (Selection):**
    *   Nodes: Input ($m_1, m_2, \dots, m_k$), Output ($x_1, x_2, \dots, x_n$).
    *   Edges: Sparse, direct mapping from a subset of Input to Output.
*   **Text Content:**
    *   Optimization of parameters.
    *   Supervised: Separability criterion (LDA).
    *   Unsupervised: Preserving characteristics (PCA).
