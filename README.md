# Link Prediction and Clustering Based on Local Online Business Community
This project explores the structural dynamics and interaction patterns within local online business communities using advanced Social Network Analysis (SNA) techniques. It focuses on two primary objectives: community detection (clustering) and link prediction, leveraging real-world data collected from online business groups.

## Key Features
1. Community Detection:

- Identifies tightly-knit groups within the network.
- Implements and compares algorithms such as:
    - Louvain (modularity optimization).
    - Girvan-Newman (edge betweenness).
    - Label Propagation (local label assignment).
- Metrics evaluated:
    - Modularity for structural strength.
    - Conductance for inter-community separation.
    - Normalized Cut for partition quality.
2. Link Prediction:

- Predicts potential future connections between users based on historical data.
- Methods used:
    - Traditional approaches (e.g., Common Neighbors, Jaccard Coefficient, Adamic-Adar, Preferential Attachment).
    - Machine learning with Random Forest, which outperformed other methods in accuracy and reliability.
3. Dataset Insights:

- Real-world data collected from a local online business group.
- Includes nodes representing users and edges representing interactions (e.g., trades, collaborations).
4. Results:

- Community Detection: Louvain achieved the highest modularity, detecting meaningful groups.
- Link Prediction: Random Forest demonstrated superior performance, with an AUC of 0.811 and accuracy of 74.83%, predicting 214 potential new links.