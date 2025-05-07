from src.files.utility_functions import open_csv, choose_source, list_folders
import json


# First get list of source systems:
list_source_systems = list_folders('./src/contracts/')

# Next, prompt user to select source system:
source_system = choose_source(list_source_systems)

# Define the location of the csv_file used to build contract:
csv_location = \
    f'./src/contracts/{source_system}/{source_system}_sourceSystem.csv'

# Save the data to variable:
csv_data = open_csv(csv_location)

# Create a set for unique entity names:
data = [x for x in csv_data[0]]

source_system_structure = {
    "$schema": "../../json_schema/_sourceSystemSchema.json",
    "name": data[0],
    "description": data[1],
    "sourceType": data[2],
    "keyVaultQuery": data[3],
    "entityNames": json.loads(data[4]),
    "notebooks": json.loads(data[5])
}

# Write json to file:
with open(f'./src/contracts/{source_system}/_sourceSystem.json', "w") \
    as json_file:
    # Set indent to 4 to make more readable:
    json.dump(source_system_structure, json_file, indent=4)
