import pandas as pd
import networkx as nx

# Load the correlation matrix from the CSV file
correlation_matrix = pd.read_csv("correlation_matrix.csv", index_col=0)

# Create a graph object
G = nx.Graph()

# Add nodes to the graph
for work_id in correlation_matrix.columns:
    G.add_node(work_id)

# Add edges to the graph based on correlations
for i, work_id1 in enumerate(correlation_matrix.columns):
    for j, work_id2 in enumerate(correlation_matrix.columns):
        if i != j:
            correlation = correlation_matrix.iloc[i, j]
            # Add an edge if correlation is non-zero
            if correlation != 0:
                G.add_edge(work_id1, work_id2, weight=correlation)

# Export the graph to a GraphML file
nx.write_graphml(G, "network_graph.graphml")
