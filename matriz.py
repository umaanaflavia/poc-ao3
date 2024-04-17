import pandas as pd
import time

start = time.time()

# Read the CSV file
df = pd.read_csv('Coletas/1001-100000/sv.csv')

# Initialize a dictionary to store work_ids and their associated freeforms
work_freeforms = {}

# Initialize the correlation matrix with zeros
correlation_matrix = pd.DataFrame(0, index=work_freeforms.keys(), columns=work_freeforms.keys())

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    work_id = row['work_id']
    freeforms = row['freeforms']
    
    # Convert the freeforms string to a list
    freeforms = eval(freeforms)

    # Iterate over other rows to check for shared freeforms
    for _, other_row in df.iloc[index+1:].iterrows():
        other_work_id = other_row['work_id']
        other_freeforms = other_row['freeforms']
        other_freeforms = eval(other_freeforms)
        
        # Calculate the number of common freeforms
        common_freeforms = len(set(freeforms) & set(other_freeforms))    
    
        if work_id != other_work_id:
            # If they share at least one freeform, increase the corresponding cell in the matrix by 1
            correlation_matrix.at[work_id, other_work_id] = common_freeforms

        print(work_id, other_work_id)

# Save the correlation matrix as a CSV file
correlation_matrix.to_csv('correlation_matrix_sv.csv', index_label='work_id')

end = time.time()

# Display the correlation matrix
print(correlation_matrix)
print(end - start)