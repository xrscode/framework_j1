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
            entityColumns = str(d['columns']).replace("'", '"')
        
            # Build up query
            query = f"""
            --First create varaiable to store sourceSystemID:
            DECLARE @sourceSystemID INT;

            -- Save the sourceSystemID to variable:
            SELECT @sourceSystemID = sourceSystemID
            FROM sourceSystem
            WHERE sourceSystemName = '{sourceSystemName}';

            -- Check if sourceSystemID was found
            IF @sourceSystemID IS NULL
            BEGIN
                PRINT 'Error: sourceSystemName ''TotesysDB'' does not exist.';
                RETURN; -- Exit the script
            END
;
            --Insert data into sourceEntity table:
            INSERT INTO sourceEntity (sourceSystemID, entityName, entityDescription, entitySourceQuery, entityColumns)
            VALUES (@sourceSystemID, '{entityName}', '{entityDescription}', '{entitySourceQuery}', '{entityColumns}');"""

    
            
            # Execute the query:
            try:
                print(f'Uploading entity: {entityName}')
                ddl_metadata(query)
            except Exception as e:
                print(f'Error message: {e}')

        break