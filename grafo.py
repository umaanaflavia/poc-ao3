import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import pygraphviz as pgv

# Load the correlation matrix from the CSV file
correlation_matrix = pd.read_csv('correlation_matrix.csv', index_col=0)
print('1')
# Create a graph object
G = nx.Graph()
print('2')
# Add nodes to the graph
for work_id in correlation_matrix.columns:
    G.add_node(work_id)
print('3')
# Add edges to the graph based on correlations
for i, work_id1 in enumerate(correlation_matrix.columns):
    for j, work_id2 in enumerate(correlation_matrix.columns):
        if i != j:
            correlation = correlation_matrix.iloc[i, j]
            # Add an edge if correlation is non-zero
            if correlation != 0:
                G.add_edge(work_id1, work_id2, weight=correlation)

print(G)

# Generate positions for plotting
pos = nx.nx_agraph.graphviz_layout(G, prog="sfdp")
print('4')
# Create edge traces
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5, color="#888"),
    hoverinfo="none",
    mode="lines"
)
print('5')

# Add edges to edge_trace
for i, edge in enumerate(G.edges()):
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace["x"] += tuple([x0, x1, None])
    edge_trace["y"] += tuple([y0, y1, None])
    print(i)
print('6')
# Create node traces
node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode="markers",
    hoverinfo="text",
    marker=dict(
        showscale=True,
        colorscale="YlGnBu",
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title="Correlation",
            xanchor="left",
            titleside="right"
        )
    )
)
print('7')
# Add nodes to node_trace
for node in G.nodes():
    x, y = pos[node]
    node_trace["x"] += tuple([x])
    node_trace["y"] += tuple([y])
    node_trace["text"] += tuple([f"Work ID: {node}"])
print('8')
# Add correlation values to the node colors
for node, adjacencies in enumerate(G.adjacency()):
    node_trace["marker"]["color"] += tuple([sum(adjacencies[1].values())])
print('9')
# Create the plot
fig = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        title="Network Graph based on Correlation Matrix",
        titlefont=dict(size=16),
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
)
print('10')
# Display the plot
fig.show()