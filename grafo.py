import pandas as pd
import networkx as nx
import time

start = time.time()

# Read the CSV file
df = pd.read_csv('Coletas/1001-100000/fr.csv')

# Create a graph
G = nx.Graph()

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    start_row = time.time()
    
    id = row['id']
    freeforms = row['freeforms']
    G.add_node(id)  # Add the work as a node
    
    # Convert the freeforms string to a list
    freeforms = eval(freeforms)
    
    # Iterate over other rows to check for shared freeforms
    for _, other_row in df.iloc[index+1:].iterrows():
        other_id = other_row['id']
        other_freeforms = other_row['freeforms']
        other_freeforms = eval(other_freeforms)
        
        # Calculate the number of common freeforms
        common_freeforms = len(set(freeforms) & set(other_freeforms))
        
        # Add an edge if there are common freeforms
        if id != other_id and common_freeforms > 0:
            G.add_edge(id, other_id, weight=common_freeforms)
    
    end_row = time.time()
    print(index + 1, '/', len(df), ' - ', end_row - start_row)

# Export the graph to a GraphML file
nx.write_graphml(G, "fr.graphml")
end = time.time()

print(G)
print(end - start)
