import os
from utility_functions import ddl_metadata
import inquirer
import json

"""
This python file will take a sourceSystemContract.json and upload it into the database. 
Note that in order to get the correct sourceSystemContract, when prompted enter the
source system name/folder name.  For example, 'AdventureWorks' is a folder that contains
the _sourceSystem.json for the AdventureWorks source System.
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
        print(f'Uploading source system: {sourceSystemName}...')
        # Set the source system name to be uploaded:
        sourceSystemPath = f'./src/contracts/{sourceSystemName}/_sourceSystem.json'

        # Load the source system contract JSON:
        with open(sourceSystemPath, 'r') as file:
            sourceSystemContract = json.load(file)

        # Begin to build up query:
        sourceEntityName = sourceSystemContract['name']
        sourceEntityDescription = sourceSystemContract['description']
        keyVaultQuery = sourceSystemContract['keyVaultQuery']
        entityNames = str(sourceSystemContract['entityNames']).replace("'", '"')
        notebooks = str(sourceSystemContract['notebooks']).replace("'", '"')

        # Define the query:
        query = f"""
        DELETE FROM sourceSystem
        WHERE sourceEntityName = '{sourceEntityName}';
        INSERT INTO sourceSystem (sourceEntityName, sourceEntityDescription, entityNames, keyVaultQuery, notebooks)
        VALUES ('{sourceEntityName}', '{sourceEntityDescription}', '{entityNames}', '{keyVaultQuery}', '{notebooks}');
        """

        # Execute the query:
        try:
            rowCount = ddl_metadata(query)
            if rowCount == -1:
                print(f'Source System: {sourceEntityName} upload successful.')
        except Exception as e:
            print(f'Error message: {e}')
        break
    