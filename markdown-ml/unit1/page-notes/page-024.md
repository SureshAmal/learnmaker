# Unit 1 Page 24 Image Understanding

## Page Overview
The purpose of this slide is to introduce and categorize the most common algorithms used in Reinforcement Learning (RL). It provides a high-level summary of five key approaches, highlighting their fundamental characteristics and differences, such as whether they are model-free, value-based, policy-based, or hybrid methods.

## Visible Text
*   **Title:** Common Reinforcement Learning Algorithms
*   **Q-Learning**
    *   Model-free RL algorithm.
    *   Learns the value of actions in each state.
*   **SARSA (State-Action-Reward-State-Action)**
    *   Updates values based on the action actually taken.
*   **Deep Q-Network (DQN)**
    *   Combines Q-Learning with neural networks.
    *   Used in game-playing AI.
*   **Policy Gradient Methods**
    *   Directly learn the policy function.
*   **Actor-Critic Methods**
    *   Combine value-based and policy-based learning.

## Visual Layout
*   **Title Position:** The title is located at the top left, rendered in a large, bold, cyan-colored font.
*   **Content Blocks:** The main content is organized as a structured bulleted list.
*   **Colors:** The background features a light blue gradient. A dark grey/black arrow-like graphic is positioned at the top left margin.
*   **Icons:** Main list items are preceded by square checkbox-style icons. Sub-points use small solid square bullets.
*   **Spacing and Alignment:** The text is left-aligned with clear indentation for sub-points, creating a clean hierarchical structure.
*   **Visual Hierarchy:** The bold headings for algorithm names immediately draw the eye, followed by the descriptive sub-points.

## Diagram Type
This is a **text-only slide** organized as a hierarchical list. It serves as a conceptual summary rather than a visual process or data representation.

## Diagram / Visual Explanation
No diagram is present on this page.

## Math / Formula / Curve Notes
No mathematical formula or curve is visible on this page.

## Table Description
No table is visible on this page.

## Concept Explanation
This slide covers the fundamental toolkit of a Reinforcement Learning practitioner:

*   **Q-Learning:** A "model-free" algorithm, meaning it doesn't need to understand the environment's underlying physics or rules to learn. It focuses on learning the "Q-value" (quality) of taking a specific action in a specific state to maximize long-term rewards.
*   **SARSA:** An acronym for State-Action-Reward-State-Action. Unlike Q-Learning, which is "off-policy" (it learns about the optimal policy while following a different one), SARSA is "on-policy." it updates its estimates based on the actual action the agent took, following its current strategy.
*   **Deep Q-Network (DQN):** This revolutionized RL by using Deep Neural Networks to approximate the Q-value function. This allows RL to solve complex problems with massive state spaces, like playing Atari games from raw pixel data.
*   **Policy Gradient Methods:** Instead of trying to figure out the value of every action (value-based), these methods directly optimize the "policy"—the mapping that tells the agent which action to take in a given state.
*   **Actor-Critic Methods:** A hybrid approach that uses two components. The **Actor** proposes actions (policy-based), and the **Critic** evaluates those actions by calculating a value function (value-based), helping the Actor improve over time.

## Exam / Viva Points
*   **Define Q-Learning:** It is a model-free, value-based RL algorithm that learns the optimal action-selection policy.
*   **What does SARSA stand for?** State-Action-Reward-State-Action.
*   **Difference between Q-Learning and SARSA:** Q-Learning is off-policy (learns optimal policy regardless of agent's actions), while SARSA is on-policy (updates based on the agent's actual behavior).
*   **What is a DQN?** It is a Q-Learning algorithm that utilizes a Deep Neural Network as a function approximator to handle high-dimensional state spaces.
*   **Policy-based vs. Value-based:** Value-based methods (like Q-learning) learn which states/actions are "good," while policy-based methods (like Policy Gradients) directly learn the best action to take.
*   **Explain Actor-Critic:** It combines the strengths of both value-based and policy-based methods; the Actor handles the policy, and the Critic handles the value estimation.

## Diagram Recreation Prompt
Create a professional educational slide titled "Common Reinforcement Learning Algorithms" using a clean, modern design.
*   **Layout:** Use a vertical arrangement of five distinct, rounded rectangular cards.
*   **Color Palette:** Use a professional dark blue and white theme with cyan accents for the title.
*   **Content per Card:**
    1.  **Q-Learning**: Include "Model-free" and "Learns state-action values."
    2.  **SARSA**: Include "On-policy" and "Updates based on actual actions."
    3.  **DQN**: Include "Q-Learning + Neural Networks" and "Used in complex AI/Gaming."
    4.  **Policy Gradient**: Include "Directly optimizes the policy function."
    5.  **Actor-Critic**: Include "Hybrid: Combines value-based and policy-based."
*   **Styling:** Use bold headers for algorithm names. Add a small, relevant icon (like a brain, a robot, or a gear) next to each header to improve visual engagement.

## Diagram Data
*   **Title:** Common Reinforcement Learning Algorithms
*   **List Structure:**
    *   **Node 1:** Q-Learning
        *   Detail A: Model-free RL algorithm.
        *   Detail B: Learns the value of actions in each state.
    *   **Node 2:** SARSA (State-Action-Reward-State-Action)
        *   Detail A: Updates values based on the action actually taken.
    *   **Node 3:** Deep Q-Network (DQN)
        *   Detail A: Combines Q-Learning with neural networks.
        *   Detail B: Used in game-playing AI.
    *   **Node 4:** Policy Gradient Methods
        *   Detail A: Directly learn the policy function.
    *   **Node 5:** Actor-Critic Methods
        *   Detail A: Combine value-based and policy-based learning.
