from src.files.utility_functions import *
import json

# Define location of CSV file:
location = './build_contract/entity.csv'

# Save the data to variable:
csv_data = open_csv(location, True)

# Create a set of entity names:
list_of_entities = list({x[0] for x in csv_data})




# Iterate through entities to create json:
for entity in list_of_entities:

    # Define the JSON structures for entities:
    json_structure = {
        "name": None,
        "description": None,
        "connectionDetails": {
            "connectionString": None,
            "sourceQuery": None
        },
        "ingestion_columns": [

        ]
    }

    
    # Read through csv data and grab all data associated with current entity:
    entity_data = [x for x in csv_data if x[0]==entity]

    # Fill out json_copy:
    json_structure["name"] = entity_data[0][0]
    json_structure["description"] = entity_data[0][1]
    json_structure["connectionDetails"]['connectionString'] = entity_data[0][2]
    json_structure["connectionDetails"]['sourceQuery'] = entity_data[0][3]
    
    # Iterate through entity_data and append to json_structure:
    for row in entity_data:
        # Define structure of ingestion columns:
        ingestion_column_structure = {
            "sortOrder": None,
            "columnName": None,
            "dataType": None,
            "required": None,
            "primary_key": None
        }
        # Grab the ingestion_columns data:
        ingestion_column_structure["sortOrder"] = int(row[4])
        ingestion_column_structure["columnName"] = row[5]
        ingestion_column_structure["dataType"] = row[6]
        ingestion_column_structure["required"] = bool(row[7])
        ingestion_column_structure["primary_key"] = bool(row[8])

        # Now append columns to json
        json_structure["ingestion_columns"].append(ingestion_column_structure)

    # Write json to file:
    with open(f"./build_contract/{entity}.json", "w") as json_file:
        # The indent parameter to make more readable:
        json.dump(json_structure, json_file, indent=4)
        


