import os
import csv

def save_rows_in_batches(input_file, output_folder, batch_size=10):
    # Check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the input CSV file
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        
        # Initialize batch number and row counter
        batch_number = 1
        row_counter = 0
        
        # Prepare for the first file
        output_file = os.path.join(output_folder, f'batch_{batch_number}.csv')
        outfile = open(output_file, mode='w', newline='', encoding='utf-8')
        writer = csv.writer(outfile)
        
        # Process each row in the input CSV file
        
        for row in reader:
            writer.writerow(row)
            row_counter += 1

            # If the row counter reaches the batch size, close the current file and open a new one
            if row_counter >= batch_size:
                outfile.close()  # Close the current file
                batch_number += 1  # Increment batch number
                row_counter = 0  # Reset row counter
                output_file = os.path.join(output_folder, f'batch_{batch_number}.csv')
                outfile = open(output_file, mode='w', newline='', encoding='utf-8')
                writer = csv.writer(outfile)
        
        # Close the last opened file
        outfile.close()
    
    print(f'CSV rows saved in batches to folder: {output_folder}')

# Example usage
input_file = 'apartment_links.csv'  # Replace with your CSV file path
output_folder = 'output_batches'  # The directory where the new files will be saved
save_rows_in_batches(input_file, output_folder, batch_size=10)
