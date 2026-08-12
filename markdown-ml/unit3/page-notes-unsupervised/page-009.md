# Unit 1 Page 9 Image Understanding

## Page Overview
The purpose of this slide is to provide a comprehensive overview of the security vulnerabilities and potential attack vectors within a standard Machine Learning (ML) pipeline. It categorizes these threats into two distinct stages: the **Training phase** and the **Testing phase**. The diagram illustrates where specific types of attacks (like poisoning, backdoors, adversarial samples, and model theft) occur relative to the data flow and model development process.

## Visible Text
*   **Training phase** (Label on the left)
*   **Poisoning attack** (Attack vector pointing to Training data)
*   **Backdoor attack** (Attack vector pointing to Training data)
*   **Training data** (Cylinder icon)
*   **Machine learning algorithms** (Process box)
*   **Training completion model** (Resulting model box)
*   **Testing phase** (Label on the left)
*   **Counter sample attacks** (Attack vector pointing to Test Input)
*   **Test Input** (Input box)
*   **Trained model** (Process box)
*   **Output prediction labels** (Result box)
*   **Model theft attack** (Attack vector pointing to Output prediction labels)
*   **Training Data Recovery Attack** (Attack vector pointing to Output prediction labels)

## Visual Layout
*   **Background:** The slide has a light gray background with a subtle diagonal hatch pattern. A large, dark brown arrow-like shape is partially visible on the far left.
*   **Structure:** The content is divided into two horizontal sections by a central dashed black line.
*   **Top Section (Training Phase):**
    *   Uses a **green color scheme** for the main components.
    *   Flow: A cylinder (Training data) connects via an arrow to a rectangle (Machine learning algorithms), which connects to another rectangle (Training completion model).
    *   Attack vectors are represented by vertical arrows pointing toward the "Training data" cylinder.
*   **Bottom Section (Testing Phase):**
    *   Uses a **blue color scheme** for the main components.
    *   Flow: A rectangle (Test Input) connects via an arrow to a rectangle (Trained model), which connects to a final rectangle (Output prediction labels).
    *   Attack vectors are represented by vertical arrows pointing toward the "Test Input" and "Output prediction labels" boxes.
*   **Alignment:** Labels for the phases are boxed on the left. The flow moves from left to right.

## Diagram Type
This is an **Architecture/Pipeline Diagram with Security Annotations**. It maps the logical flow of a machine learning system and overlays specific security threats at the exact points where they compromise the system.

## Diagram / Visual Explanation
### 1. Training Phase (Top Row)
*   **Source:** The process starts with **Training data**.
*   **Attacks on Data:** 
    *   **Poisoning attack:** An attacker injects malicious data into the training set to degrade the model's overall performance or cause specific misclassifications.
    *   **Backdoor attack:** An attacker modifies the training data to include a "trigger." The model functions normally on standard data but performs a specific malicious action when the trigger is present.
*   **Process:** The (potentially compromised) data is fed into **Machine learning algorithms**.
*   **Outcome:** The result is a **Training completion model** that may contain inherent vulnerabilities or biases introduced during training.

### 2. Testing Phase (Bottom Row)
*   **Source:** The process begins with **Test Input**.
*   **Attacks on Input:**
    *   **Counter sample attacks (Adversarial attacks):** An attacker slightly perturbs the input data in a way that is often invisible to humans but causes the **Trained model** to make an incorrect prediction.
*   **Process:** The input is processed by the **Trained model**.
*   **Outcome:** The model generates **Output prediction labels**.
*   **Attacks on Output/Privacy:**
    *   **Model theft attack:** An attacker repeatedly queries the model and uses the outputs to train a "shadow model" that mimics the original's functionality, effectively stealing intellectual property.
    *   **Training Data Recovery Attack (Inversion):** An attacker analyzes the output labels to reconstruct or infer sensitive information about the original data used during the training phase.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page.

## Table Description
No table is visible on this page.

## Concept Explanation
This slide teaches the concept of **Adversarial Machine Learning**. It emphasizes that security in ML is not just about protecting the server, but protecting the integrity of the data and the privacy of the model itself.

*   **Integrity Attacks (Training Phase):** These happen before the model is even deployed. If the "foundation" (data) is compromised, the resulting model is untrustworthy.
*   **Evasion Attacks (Testing Phase):** These happen when the model is live. The attacker doesn't change the model but tricks it using carefully crafted inputs (Counter samples).
*   **Privacy/Confidentiality Attacks (Testing Phase):** These target the outputs. Even if a model is accurate, its responses might leak the proprietary logic of the model (Theft) or the private data of the individuals used to train it (Recovery).

## Exam / Viva Points
*   **Identify the two main phases where ML attacks occur:** Training phase and Testing (Inference) phase.
*   **Define Poisoning vs. Backdoor:** Poisoning aims for general performance degradation; Backdoor aims for a specific response to a specific trigger.
*   **Explain "Counter sample attacks":** These are adversarial inputs designed to fool a trained model at inference time.
*   **Distinguish between Model Theft and Data Recovery:** Model theft targets the algorithm/logic; Data recovery targets the privacy of the training dataset.
*   **Why is the dashed line significant?** It separates the development environment (Training) from the production/deployment environment (Testing).

## Diagram Recreation Prompt
Create a professional machine learning pipeline security diagram. Divide the page horizontally with a dashed line. 
**Top section (Training Phase):** Use light green boxes. Start with a cylinder labeled "Training data". Add a vertical arrow from above labeled "Poisoning attack" and one from below labeled "Backdoor attack" pointing to the cylinder. Draw a horizontal arrow to a rectangle labeled "Machine learning algorithms", then another arrow to a rectangle labeled "Training completion model". 
**Bottom section (Testing Phase):** Use light blue boxes. Start with a rectangle labeled "Test Input". Add a vertical arrow from below labeled "Counter sample attacks". Draw a horizontal arrow to a rectangle labeled "Trained model", then another arrow to a rectangle labeled "Output prediction labels". Add a vertical arrow from above labeled "Model theft attack" and one from below labeled "Training Data Recovery Attack" pointing to the output box. 
Use a clean, modern font and a light gray textured background.

## Diagram Data
**Nodes:**
*   Phase Labels: "Training phase", "Testing phase"
*   Training Components: "Training data" (Cylinder), "Machine learning algorithms" (Box), "Training completion model" (Box)
*   Testing Components: "Test Input" (Box), "Trained model" (Box), "Output prediction labels" (Box)
*   Attack Labels: "Poisoning attack", "Backdoor attack", "Counter sample attacks", "Model theft attack", "Training Data Recovery Attack"

**Edges (Flow):**
*   Training data -> Machine learning algorithms
*   Machine learning algorithms -> Training completion model
*   Test Input -> Trained model
*   Trained model -> Output prediction labels

**Edges (Attacks):**
*   Poisoning attack -> Training data
*   Backdoor attack -> Training data
*   Counter sample attacks -> Test Input
*   Model theft attack -> Output prediction labels
*   Training Data Recovery Attack -> Output prediction labels
