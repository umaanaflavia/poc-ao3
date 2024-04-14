import pandas as pd

# Read the CSV file
df = pd.read_csv('C:/Users/umaanaflavia/OneDrive/Documentos/poc-ao3/Coletas/1001-100000/ptPT.csv')

# Initialize a dictionary to store work_ids and their associated freeforms
work_freeforms = {}

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    work_id = row['work_id']
    freeforms = row['freeforms']
    
    # Convert the freeforms string to a list
    freeforms = eval(freeforms)
    
    # Store the work_id and its associated freeforms in the dictionary
    work_freeforms[work_id] = freeforms
print(work_freeforms)

# Initialize the correlation matrix with zeros
correlation_matrix = pd.DataFrame(0, index=work_freeforms.keys(), columns=work_freeforms.keys())

# Iterate over each pair of work_ids
for work_id1, freeforms1 in work_freeforms.items():
    for work_id2, freeforms2 in work_freeforms.items():
        # Check if the two works share any freeforms
        shared_freeforms = set(freeforms1) & set(freeforms2)
        if work_id1 != work_id2:
            # If they share at least one freeform, increase the corresponding cell in the matrix by 1
            correlation_matrix.at[work_id1, work_id2] = len(shared_freeforms)
        print(work_id1, work_id2)

# Save the correlation matrix as a CSV file
correlation_matrix.to_csv('correlation_matrix.csv', index_label='work_id')

# Display the correlation matrix
print(correlation_matrix)
