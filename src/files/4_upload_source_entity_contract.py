import json
from utility_functions import ddl_metadata
import os
import inquirer

"""
This python file will take a sourceEntityContract.json and upload it into the database. 
"""

# First get list of folders/sourcesystems:
sourceSystems = [folder for folder in os.listdir('./src/contracts')]
sourceSystems.append('Exit')

while True:
    questions = [
        inquirer.List('choice',
                      message="Which source system would you like to upload?",
                      choices=sourceSystems,
                      )
    ]

    sourceSystemName = inquirer.prompt(questions)['choice']

    if sourceSystemName == 'Exit':
        print('Exiting...')
        break
    else:
        
        # Define the path to the source entity contract:
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
            # Convert to string and lower case so that json is valid:
            entityIngestionColumns = str(d['ingestion_columns']).replace("'", '"').replace("True", "true").replace("False", "false")

        
            # Build up query
            query = f"""
            DECLARE @sourceSystemID INT;

            -- Retrieve the sourceSystemID
            SELECT @sourceSystemID = sourceSystemID
            FROM sourceSystem
            WHERE sourceSystemName = '{sourceSystemName}';

            -- Check if sourceSystemID was found
            IF @sourceSystemID IS NULL
            BEGIN
                PRINT 'Error: sourceSystemName ''{sourceSystemName}'' does not exist.';
                RETURN; -- Exit the script
            END;

            -- Perform MERGE operation
            MERGE INTO sourceEntity AS target
            USING (SELECT @sourceSystemID AS sourceSystemID, '{entityName}' AS entityName) AS source
            ON target.sourceSystemID = source.sourceSystemID AND target.entityName = source.entityName
            WHEN MATCHED THEN 
                UPDATE SET 
                    entityDescription = '{entityDescription}', 
                    entitySourceQuery = '{entitySourceQuery}', 
                    entityIngestionColumns = '{entityIngestionColumns}'
            WHEN NOT MATCHED THEN
                INSERT (sourceSystemID, entityName, entityDescription, entitySourceQuery, entityIngestionColumns)
                VALUES (@sourceSystemID, '{entityName}', '{entityDescription}', '{entitySourceQuery}', '{entityIngestionColumns}');
            """

            

            # Execute the query:
            try:
                print(f'Uploading entity: {entityName}')
                ddl_metadata(query)
            except Exception as e:
                print(f'Error message: {e}')

        break