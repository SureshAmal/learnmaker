# Unit 1 Page 9 Image Understanding

## Page Overview
This slide provides a conceptual overview of security vulnerabilities in the machine learning (ML) lifecycle. It categorizes various types of adversarial attacks based on whether they occur during the **Training phase** or the **Testing phase**. The purpose is to map specific threat vectors to the corresponding stages of a standard ML pipeline.

## Visible Text
*   **Training phase** (Label for the top section)
    *   Poisoning attack
    *   Training data
    *   Backdoor attack
    *   Machine learning algorithms
    *   Training completion model
*   **Testing phase** (Label for the bottom section)
    *   Test Input
    *   Counter sample attacks
    *   Trained model
    *   Output prediction labels
    *   Model theft attack
    *   Training Data Recovery Attack

## Visual Layout
*   **Structure:** The slide is divided horizontally into two main sections by a dashed black line.
*   **Top Section (Training Phase):** Uses a light green color theme for the process blocks.
*   **Bottom Section (Testing Phase):** Uses a light blue color theme for the process blocks.
*   **Labels:** The phase names are placed in white boxes on the far left.
*   **Flow:** Both sections follow a left-to-right linear flow indicated by black arrows.
*   **Attack Vectors:** Attacks are represented by vertical arrows pointing toward specific components of the pipeline, indicating the point of entry for the adversary.
*   **Background:** The main content area has a light grey diagonal hatch pattern. A thick vertical brown decorative bar is visible on the far left edge of the slide.

## Diagram Type
This is an **Architecture/Pipeline Diagram** focused on security. It illustrates the sequential stages of a machine learning workflow and overlays specific security threats (attacks) onto the relevant components of that workflow.

## Diagram / Visual Explanation
### 1. Training Phase (Top Row)
*   **Training data (Cylinder icon):** The starting point. This is the dataset used to teach the model.
    *   **Poisoning attack:** An arrow points down from the top, indicating an attack where malicious data is injected into the training set to corrupt the learning process.
    *   **Backdoor attack:** An arrow points up from the bottom, indicating an attack where a hidden trigger is embedded in the data so the model learns a specific malicious behavior for that trigger.
*   **Machine learning algorithms (Rectangle):** The data flows here to be processed by the learning logic.
*   **Training completion model (Rectangle):** The final output of the training phase.

### 2. Testing Phase (Bottom Row)
*   **Test Input (Rectangle):** New, unseen data provided to the model for inference.
    *   **Counter sample attacks:** An arrow points up from the bottom, representing adversarial examples—inputs specifically crafted to trick the model into making a wrong prediction.
*   **Trained model (Rectangle):** The model created in the training phase is now used to process the test input.
*   **Output prediction labels (Rectangle):** The final result/classification provided by the model.
    *   **Model theft attack:** An arrow points down from the top, indicating an attempt to reverse-engineer or duplicate the model's logic by observing its outputs.
    *   **Training Data Recovery Attack:** An arrow points up from the bottom, indicating an attempt to reconstruct sensitive information from the original training set by analyzing the model's output behavior.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page.

## Table Description
No table is visible on this page.

## Concept Explanation
The slide covers **Adversarial Machine Learning**, which focuses on the security of ML systems.

*   **Training Phase Attacks:** These target the "brain" of the model while it is being built.
    *   **Poisoning:** The attacker adds "bad" examples to the training set so the model learns the wrong patterns (e.g., making a spam filter ignore certain types of spam).
    *   **Backdoor:** The attacker ensures the model works perfectly except when a specific "key" (trigger) is present, at which point it performs a malicious action.
*   **Testing Phase Attacks:** These target the model while it is in use (inference).
    *   **Counter Samples (Adversarial Examples):** Small, often invisible changes to an input (like adding noise to an image) that cause a high-accuracy model to fail completely.
    *   **Model Theft:** By querying a model many times and seeing the results, an attacker can build their own version of the model without having the original code or data.
    *   **Data Recovery (Inversion):** Attackers use the model's outputs to figure out what the private training data looked like, which is a major privacy concern.

## Exam / Viva Points
*   **Distinguish between Training and Testing attacks:** Training attacks corrupt the model's logic; testing attacks exploit the model's existing logic or steal information.
*   **Define Poisoning:** Injecting malicious data into the training set to degrade performance or cause specific misclassifications.
*   **Define Adversarial Examples (Counter Samples):** Inputs designed to be misclassified by a model while appearing normal to humans.
*   **Explain Model Theft:** The process of extracting the functionality of a black-box model through repeated queries.
*   **Explain Data Recovery:** A privacy-violating attack where training data characteristics are inferred from model outputs.

## Diagram Recreation Prompt
Create a clean, professional machine learning security pipeline diagram. 
- Divide the page into two horizontal halves with a dashed line. 
- Label the top half "Training Phase" and the bottom half "Testing Phase". 
- In the top half, draw a flow: [Cylinder: Training Data] -> [Box: ML Algorithms] -> [Box: Trained Model]. Add vertical arrows to "Training Data" labeled "Poisoning Attack" (top) and "Backdoor Attack" (bottom). Use a soft green color for these boxes.
- In the bottom half, draw a flow: [Box: Test Input] -> [Box: Trained Model] -> [Box: Output Labels]. Add a vertical arrow to "Test Input" labeled "Adversarial Attacks". Add vertical arrows to "Output Labels" labeled "Model Theft" (top) and "Data Recovery" (bottom). Use a soft blue color for these boxes.
- Use a modern sans-serif font and ensure all text is clearly legible.

## Diagram Data
*   **Phase 1: Training**
    *   Nodes: Training Data (Cylinder), ML Algorithms (Rect), Training Completion Model (Rect).
    *   Edges: Data -> Algorithms -> Model.
    *   Attacks: Poisoning (to Data), Backdoor (to Data).
*   **Phase 2: Testing**
    *   Nodes: Test Input (Rect), Trained Model (Rect), Output Prediction Labels (Rect).
    *   Edges: Input -> Model -> Labels.
    *   Attacks: Counter sample (to Input), Model theft (to Labels), Data Recovery (to Labels).
