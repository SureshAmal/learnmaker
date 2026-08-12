# Unit 1 Page 119 Image Understanding

## Page Overview
The purpose of this slide is to provide a high-level, step-by-step overview of the standard **Machine Learning Modeling Workflow**. It serves as a roadmap for students to understand the sequential stages involved in building, refining, and deploying a machine learning model, from initial data collection to final prediction.

## Visible Text
*   **Title:** Modeling Workflow:
*   **Collect Data**
    *   Input dataset (e.g., CSV, Excel)
*   **Preprocess Data**
    *   Cleaning, encoding, normalization, feature scaling, splitting
*   **Select Model (Algorithm)**
    *   Classification $\rightarrow$ SVM, KNN, Decision Tree
    *   Regression $\rightarrow$ Linear Regression
    *   Clustering $\rightarrow$ K-Means
*   **Train Model**
    *   Model learns from training data
*   **Evaluate Model**
    *   Accuracy, precision, recall, confusion matrix, etc.
*   **Tune Parameters**
    *   Adjust hyperparameters (e.g., GridSearchCV)
*   **Predict on New Data**
    *   Final model makes predictions on unseen data

## Visual Layout
*   **Title:** Positioned at the top center-right in a large, bold, magenta font.
*   **Background:** A light blue to white gradient.
*   **Decorative Elements:** 
    *   A dark grey, horizontal arrow-like shape pointing right is located at the top left.
    *   Several thin, dark blue curved lines sweep upward from the bottom-left corner, creating a sense of movement or progress.
*   **Content Alignment:** The main content is a left-aligned vertical list of seven steps.
*   **Hierarchy:** 
    *   Main steps are in bold black text, preceded by a small square bullet point.
    *   Sub-details for each step are in a smaller, regular grey font, indented and preceded by a smaller square bullet point.
*   **Spacing:** Generous vertical spacing between steps ensures readability.

## Diagram Type
This is a **Pipeline / Sequential List**. It is classified as such because it presents a linear, chronological progression of tasks required to complete a machine learning project.

## Diagram / Visual Explanation
While not a traditional flowchart with boxes and arrows, the vertical list represents a logical flow:
1.  **Collect Data:** The starting point where raw data is gathered.
2.  **Preprocess Data:** The data is cleaned and transformed into a format suitable for algorithms.
3.  **Select Model:** A strategic decision point where the user chooses an algorithm based on the problem type (Classification, Regression, or Clustering).
4.  **Train Model:** The core phase where the algorithm processes the training data to find patterns.
5.  **Evaluate Model:** A quality check phase using metrics to see how well the model learned.
6.  **Tune Parameters:** An optimization phase to improve the model's performance by adjusting its internal settings.
7.  **Predict on New Data:** The final goal where the trained and tuned model is used on real-world data.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page.

## Table Description
No table is visible on this page.

## Concept Explanation
The **Machine Learning Workflow** is the standard operational procedure for developing predictive models.
*   **Data Collection:** Gathering data from sources like databases, CSV files, or web scraping.
*   **Preprocessing:** This is often the most time-consuming step. It involves **Cleaning** (handling missing values/outliers), **Encoding** (turning text into numbers), **Scaling** (ensuring all features have a similar range), and **Splitting** (dividing data into Training and Testing sets).
*   **Model Selection:** Choosing the right tool for the job. If you want to predict a category (e.g., Spam vs. Not Spam), you use **Classification**. If you want to predict a number (e.g., house price), you use **Regression**. If you want to find hidden groups, you use **Clustering**.
*   **Training:** The process of "fitting" the model to the training data.
*   **Evaluation:** Using the test data to calculate metrics like **Accuracy** (correctness) or **Recall** (ability to find all positive cases).
*   **Hyperparameter Tuning:** Adjusting the "knobs" of the algorithm (like the number of neighbors in KNN) to find the best configuration, often using tools like **GridSearchCV**.
*   **Prediction:** The final stage where the model is used in production to provide insights on new, unseen data.

## Exam / Viva Points
*   **List the 7 steps of the ML workflow in order.**
*   **What happens during the preprocessing stage?** (Be ready to mention cleaning, scaling, and splitting).
*   **Give examples of algorithms for different ML tasks.** (e.g., SVM for classification, K-Means for clustering).
*   **Why is "Evaluate Model" a critical step?** (To ensure the model generalizes well and isn't just memorizing the training data).
*   **What is the purpose of Hyperparameter Tuning?** (To optimize the model's performance beyond the default settings).
*   **What is the difference between training data and "unseen" data?** (Training data is used to build the model; unseen data is used to test its real-world effectiveness).

## Diagram Recreation Prompt
Create a professional vertical pipeline diagram titled "Machine Learning Modeling Workflow" in bold magenta. Use seven distinct, rounded rectangular boxes arranged vertically. Connect them with downward-pointing arrows. 
- Box 1: "Collect Data" (Subtext: CSV, Excel, SQL). 
- Box 2: "Preprocess Data" (Subtext: Cleaning, Scaling, Encoding, Splitting). 
- Box 3: "Select Model" (Subtext: Classification, Regression, Clustering). 
- Box 4: "Train Model" (Subtext: Learning from training set). 
- Box 5: "Evaluate Model" (Subtext: Accuracy, Precision, Recall). 
- Box 6: "Tune Parameters" (Subtext: Hyperparameter optimization, GridSearchCV). 
- Box 7: "Predict" (Subtext: Inference on unseen data). 
Use a clean white background with subtle blue accents.

## Diagram Data
*   **Title:** Modeling Workflow:
*   **Workflow Steps:**
    1.  **Collect Data** [Details: Input dataset (e.g., CSV, Excel)]
    2.  **Preprocess Data** [Details: Cleaning, encoding, normalization, feature scaling, splitting]
    3.  **Select Model (Algorithm)** [Details: Classification (SVM, KNN, Decision Tree), Regression (Linear Regression), Clustering (K-Means)]
    4.  **Train Model** [Details: Model learns from training data]
    5.  **Evaluate Model** [Details: Accuracy, precision, recall, confusion matrix, etc.]
    6.  **Tune Parameters** [Details: Adjust hyperparameters (e.g., GridSearchCV)]
    7.  **Predict on New Data** [Details: Final model makes predictions on unseen data]
