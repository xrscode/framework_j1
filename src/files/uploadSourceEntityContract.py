import json
from utility_functions import ddl_metadata
import os

"""
This python file will take a sourceEntityContract.json and upload it into the database. 
"""

# Set the source system name to be uploaded:
sourceSystemName = input('Enter the source system name:')
sourceEntityPath = f'./src/contracts/{sourceSystemName}/'

# List all files in the folder
json_files = [f for f in os.listdir(sourceEntityPath) if f.endswith(".json") and f != "_sourceSystem.json"]

# Iterate through the contracts and upload them to the database:
for contract in json_files:
    # Reconstruct full file path:
    file = sourceEntityPath + contract
    # Open contract:
    with open(file, 'r') as c:
        d = json.load(c)
    
    # Save variables:
    entityName = d['name']
    entityDescription = d['description']
    entitySourceQuery = str(d['connectionDetails']).replace("'", '"')
    entityColumns = str(d['columns']).replace("'", '"')
   
    # Build up query
    query = f"""
    --First create varaiable to store sourceEntityID:
    DECLARE @sourceEntityID INT;

    -- Save the sourceEntityID to variable:
    SELECT @sourceEntityID = sourceEntityID
    FROM sourceSystem
    WHERE sourceEntityName = '{sourceSystemName}';

    --Delete from sourceEntity If exists:
    DELETE FROM sourceEntity
    WHERE entityName = '{sourceSystemName}';

    --Insert data into sourceEntity table:
    INSERT INTO sourceEntity (sourceEntityID, entityName, entityDescription, entitySourceQuery, entityColumns)
    VALUES (@sourceEntityID, '{entityName}', '{entityDescription}', '{entitySourceQuery}', '{entityColumns}');"""


    # Execute the query:
    try:
        print(f'Uploading entity: {entityName}')
        rowCount = ddl_metadata(query)
        if rowCount == -1:
            print(f'Entity: {entityName} upload successful.')
    except Exception as e:
        print(f'Error message: {e}')