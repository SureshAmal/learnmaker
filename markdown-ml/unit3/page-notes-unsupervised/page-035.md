# Unit 1 Page 35 Image Understanding

## Page Overview
The slide provides a comprehensive, step-by-step numerical example of the **Apriori Algorithm**, a fundamental algorithm in data mining for finding frequent itemsets in a transactional database. It demonstrates the iterative process of candidate generation ($C_k$) and pruning to find frequent itemsets ($L_k$) based on a minimum support threshold.

## Visible Text
*   **Title:** APRIORI ALGORITHM EXAMPLE
*   **Database D:**
    *   Minsup = 0.5 (Minimum Support)
    *   **TID | Items**
    *   100 | 1 3 4
    *   200 | 2 3 5
    *   300 | 1 2 3 5
    *   400 | 2 5
*   **Step 1 ($C_1$):** Scan D $\rightarrow$ $C_1$
    *   **itemset | sup.**
    *   {1} | 2
    *   {2} | 3
    *   {3} | 3
    *   {4} | 1
    *   {5} | 3
*   **Step 2 ($L_1$):**
    *   **itemset | sup.**
    *   {1} | 2
    *   {2} | 3
    *   {3} | 3
    *   {5} | 3
*   **Step 3 ($C_2$ generation):** (Curved arrow indicating self-join of $L_1$)
    *   **itemset**
    *   {1 2}, {1 3}, {1 5}, {2 3}, {2 5}, {3 5}
*   **Step 4 ($C_2$ with support):** Scan D $\leftarrow$
    *   **itemset | sup.**
    *   {1 2} | 1
    *   {1 3} | 2
    *   {1 5} | 1
    *   {2 3} | 2
    *   {2 5} | 3
    *   {3 5} | 2
*   **Step 5 ($L_2$):** $\leftarrow$
    *   **itemset | sup.**
    *   {1 3} | 2
    *   {2 3} | 2
    *   {2 5} | 3
    *   {3 5} | 2
*   **Step 6 ($C_3$):** (Down arrow from $L_2$)
    *   **itemset**
    *   {2 3 5}
*   **Step 7 ($L_3$):** Scan D $\rightarrow$
    *   **itemset | sup.**
    *   {2 3 5} | 2

## Visual Layout
*   **Title:** Large, bold, centered at the top.
*   **Flow:** The process follows a "snake" or "S-curve" path. It starts at the top left (Database D), moves right to $L_1$, loops down to the right side for $C_2$, moves left to $L_2$, and finally moves down and right to $L_3$.
*   **Tables:** All tables have a consistent style with yellow headers and light blue/green bodies.
*   **Arrows:**
    *   Straight horizontal arrows indicate transitions between candidate sets and frequent sets.
    *   "Scan D" labels are placed above arrows where the database is read to count occurrences.
    *   A curved arrow on the far right indicates the join operation to create $C_2$ from $L_1$.
    *   A small curved arrow on the far left indicates the join/prune operation to create $C_3$ from $L_2$.
*   **Color Coding:** The background is a light textured gray. Tables use yellow for headers and a light cyan for data rows.

## Diagram Type
This is an **Algorithm Execution Trace / Pipeline Diagram**. It uses a series of tables and arrows to show the state of data as it passes through the various stages of the Apriori algorithm.

## Diagram / Visual Explanation
1.  **Input:** Starts with **Database D** containing 4 transactions. **Minsup** is set to 0.5, meaning an itemset must appear in at least $0.5 \times 4 = 2$ transactions to be considered "frequent".
2.  **Iteration 1:**
    *   **Scan D:** The database is scanned to count the occurrences of each individual item, resulting in candidate set **$C_1$**.
    *   **Pruning:** Item {4} has a support of 1, which is less than the required 2. It is removed to form frequent 1-itemset **$L_1$**.
3.  **Iteration 2:**
    *   **Join:** $L_1$ is joined with itself to create all possible pairs, forming the initial **$C_2$** list.
    *   **Scan D:** The database is scanned again to find the support counts for these pairs.
    *   **Pruning:** Pairs {1 2} and {1 5} have support counts of 1 and are removed, resulting in frequent 2-itemset **$L_2$**.
4.  **Iteration 3:**
    *   **Join & Prune:** $L_2$ is used to generate 3-item candidates. Only {2 3 5} is generated because its subsets ({2 3}, {2 5}, {3 5}) are all present in $L_2$. This forms **$C_3$**.
    *   **Scan D:** A final scan counts the occurrences of {2 3 5}.
    *   **Result:** Since its support is 2, it forms the frequent 3-itemset **$L_3$**.

## Math / Formula / Curve Notes
*   **Minimum Support (Minsup):** $0.5$.
*   **Support Count Calculation:** $\text{Support Count} = \text{Minsup} \times \text{Total Transactions} = 0.5 \times 4 = 2$.
*   **Support (sup.):** The raw count of transactions in which an itemset appears.
*   **Apriori Property:** If an itemset is frequent, all of its subsets must also be frequent. Conversely, if any subset is infrequent, the superset cannot be frequent (used to prune {4} in $C_1$ and {1 2}, {1 5} in $C_2$).

## Table Description
*   **Database D:** Shows Transaction IDs (TID) and the items purchased.
*   **$C_k$ Tables:** Candidate itemsets of size $k$ with their calculated support counts.
*   **$L_k$ Tables:** Frequent itemsets of size $k$ that met the minimum support threshold (count $\ge$ 2).
*   **Comparison:** By comparing $C_k$ to $L_k$, one can see which itemsets were pruned for failing the support threshold.

## Concept Explanation
The **Apriori Algorithm** is used for frequent itemset mining. It operates on the principle of **downward closure**: a set of items can only be frequent if all of its subsets are also frequent.
*   **Step 1: Candidate Generation:** Create larger itemsets by joining smaller frequent itemsets from the previous level.
*   **Step 2: Pruning:** Remove any candidate that contains a subset that was not frequent in the previous level.
*   **Step 3: Support Counting:** Scan the database to see how many times the remaining candidates actually appear.
*   **Step 4: Filtering:** Keep only those candidates that meet the minimum support threshold. Repeat until no more frequent itemsets can be found.

## Exam / Viva Points
*   **What is the Minsup in this example?** It is 0.5, which translates to a count of 2 transactions.
*   **Why was item {4} removed from $L_1$?** Because its support count was 1, which is less than the threshold of 2.
*   **How is $C_2$ generated?** By performing a self-join on $L_1$ (combining all frequent 1-itemsets into pairs).
*   **Explain the Apriori Property.** It states that all non-empty subsets of a frequent itemset must also be frequent. This allows the algorithm to significantly reduce the search space.
*   **How many database scans were performed?** Three scans (one for each level $k=1, 2, 3$).

## Diagram Recreation Prompt
"Create a technical diagram illustrating the Apriori Algorithm example. Use a white background. At the top left, place a table for 'Database D' with columns 'TID' and 'Items' (rows: 100: 1 3 4; 200: 2 3 5; 300: 1 2 3 5; 400: 2 5). Use a horizontal flow with arrows. Show the transition from Database D to a table $C_1$ (itemsets {1} to {5} with counts), then to $L_1$ (dropping {4}). Use a curved arrow to show $L_1$ generating $C_2$ (pairs). Arrange the $C_2$ and $L_2$ tables in a row below the first, flowing right-to-left. Finally, show $L_2$ leading down to $C_3$ and $L_3$ at the bottom. Use yellow headers for all tables and light blue for data rows. Label arrows with 'Scan D' where appropriate."

## Diagram Data
*   **Database D:** `[[100, "1 3 4"], [200, "2 3 5"], [300, "1 2 3 5"], [400, "2 5"]]`
*   **$C_1$:** `[{"{1}": 2}, {"{2}": 3}, {"{3}": 3}, {"{4}": 1}, {"{5}": 3}]`
*   **$L_1$:** `[{"{1}": 2}, {"{2}": 3}, {"{3}": 3}, {"{5}": 3}]`
*   **$C_2$ (with sup):** `[{"{1 2}": 1}, {"{1 3}": 2}, {"{1 5}": 1}, {"{2 3}": 2}, {"{2 5}": 3}, {"{3 5}": 2}]`
*   **$L_2$:** `[{"{1 3}": 2}, {"{2 3}": 2}, {"{2 5}": 3}, {"{3 5}": 2}]`
*   **$C_3$:** `{"{2 3 5}": "count pending"}`
*   **$L_3$:** `{"{2 3 5}": 2}`
