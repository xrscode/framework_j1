from src.files.utility_functions import open_csv
import json

# Define location of CSV file:
csv_location = './src/build_contract/_sourceSystem.csv'

# Save the data to variable:
csv_data = open_csv(csv_location, True)

# Create a set for unique entity names:
data = [x for x in csv_data[0]]

source_system_structure = {
    "name": data[0],
    "description": data[1],
    "sourceType": data[2],
    "keyVaultQuery": data[3],
    "entityNames": json.loads(data[4]),
    "notebooks": json.loads(data[5])
}

# Write json to file:
with open(f"./src/build_contract/contracts/_sourceSystem.json", "w") as json_file:
    # Set indent to 4 to make more readable:
    json.dump(source_system_structure, json_file, indent=4)
