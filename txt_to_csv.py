import pandas as pd
import csv

# Define the input and output file paths
input_file = "lista_ptakow_polski.txt"
output_file = "birds.csv"  # Change this to your final CSV file name

# Read the birds from the input file
birds_data = []
with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        # Find the index of the first "("
        split_index = line.index("(")
        # Split the line into Polish name and scientific name
        polish_name = line[:split_index].strip()
        scientific_name = line[split_index:].strip()
        birds_data.append((polish_name, scientific_name))

# Convert the data to a pandas DataFrame
birds_df = pd.DataFrame(birds_data, columns=["Polish name", "Scientific name"])

# Write the DataFrame to a CSV file
birds_df.to_csv(output_file, index=False, encoding="utf-8")