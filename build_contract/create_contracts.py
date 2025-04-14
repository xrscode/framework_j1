from src.files.utility_functions import open_csv
import json

# Define location of CSV file:
location = './build_contract/entity.csv'

# Save the data to variable:
csv_data = open_csv(location, True)

# Create a set for unique entity names:
list_of_entities = list({x[0] for x in csv_data})


# Iterate through entities to create json:
for entity in list_of_entities:
    # Grab all columns associated with current entity:
    entity_data = [x for x in csv_data if x[0] == entity]

    # Define the JSON structures for entities:
    json_structure = {
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
    with open(f"./build_contract/contracts/{entity}.json", "w") as json_file:
        # The indent parameter to make more readable:
        json.dump(json_structure, json_file, indent=4)
