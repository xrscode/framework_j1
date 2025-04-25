from src.files.utility_functions import open_csv, list_folders, choose_source
import json


# First get list of source systems:
list_source_systems = list_folders('./src/contracts/')

# Next, prompt user to select source system:
source_system = choose_source(list_source_systems)

csv_location = f'./src/contracts/{source_system}/{source_system}_entity.csv'

# Save the data to variable:
csv_data = open_csv(csv_location, True)

# Create a set for unique entity names:
list_of_entities = list({x[0] for x in csv_data})


# Iterate through entities to create json:
for entity in list_of_entities:
    # Grab all columns associated with current entity:
    entity_data = [x for x in csv_data if x[0] == entity]

    # Define the JSON structures for entities:
    json_structure = {
        "$schema": "../../json_schema/_entitySchema.json",
        "name": str(entity_data[0][0]).strip(),
        "description": str(entity_data[0][1]).strip(),
        "connectionDetails": {
            "connectionString": str(entity_data[0][2]).strip(),
            "sourceQuery": str(entity_data[0][3]).strip()
        },
        "ingestion_columns": [

        ]
    }

    # Iterate through entity_data and append to json_structure:
    for row in entity_data:
        # Define structure of ingestion columns:
        ingestion_column_structure = {
            "sortOrder": int(str(row[4]).strip()),
            "columnName": str(row[5]).strip(),
            "dataType": str(row[6]).strip(),
            "required": bool(True if str(row[7]).strip() in ['true', 'True']
                             else False),
            "primary_key": bool(True if str(row[8]).strip() in ['true', 'True']
                                else False)
        }

        # Now append columns to json
        json_structure["ingestion_columns"].append(ingestion_column_structure)

    # Write json to file:
    with open(f'./src/contracts/{source_system}/{entity}.json', "w") as json_file:
        # Set indent to 4 to make more readable:
        json.dump(json_structure, json_file, indent=4)
