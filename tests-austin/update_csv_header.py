import os
import pandas as pd

def add_id_column_to_headers(directory):
    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            
            # Read the entire CSV (including data)
            df = pd.read_csv(file_path)

            # Add the 'id' column as the first column in the header
            df.columns = ['id'] + list(df.columns)

            # Write the updated DataFrame back to the CSV file (including the data)
            df.to_csv(file_path, index=False)

            print(f"Updated header for file: {filename}")

# Example usage
directory_path = 'output_batches'
add_id_column_to_headers(directory_path)
