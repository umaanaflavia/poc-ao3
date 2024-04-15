import pandas as pd
import networkx as nx
import time

start = time.time()

# Read the CSV file
df = pd.read_csv('Coletas/1001-100000/ptBR.csv')

# Create a graph
G = nx.Graph()

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    start_row = time.time()
    
    work_id = row['work_id']
    freeforms = row['freeforms']
    G.add_node(work_id)  # Add the work as a node
    
    # Convert the freeforms string to a list
    freeforms = eval(freeforms)
    
    # Iterate over other rows to check for shared freeforms
    for _, other_row in df.iloc[index+1:].iterrows():
        other_work_id = other_row['work_id']
        other_freeforms = other_row['freeforms']
        other_freeforms = eval(other_freeforms)
        
        # Calculate the number of common freeforms
        common_freeforms = len(set(freeforms) & set(other_freeforms))
        
        # Add an edge if there are common freeforms
        if common_freeforms > 0:
            G.add_edge(work_id, other_work_id, weight=common_freeforms)
    
    end_row = time.time()
    print(index + 1, '/', len(df), ' - ', end_row - start_row)

# Export the graph to a GraphML file
nx.write_graphml(G, "ptBR.graphml")
end = time.time()

print(G)
print(end - start)
