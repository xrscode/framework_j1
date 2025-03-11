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
        sourceSystemName = sourceSystemContract['name']
        sourceSystemDescription = sourceSystemContract['description']
        keyVaultQuery = sourceSystemContract['keyVaultQuery']
        entityNames = str(sourceSystemContract['entityNames']).replace("'", '"')
        notebooks = str(sourceSystemContract['notebooks']).replace("'", '"')

      
        # Merge prevents sourceSystemID from incrementing on match:
        query = f"""
        MERGE INTO dbo.sourceSystem AS target
        USING (VALUES ('{sourceSystemName}', '{sourceSystemDescription}', '{entityNames}', '{keyVaultQuery}', '{notebooks}')) AS source (sourceSystemName, sourceSystemDescription, entityNames, keyVaultQuery, notebooks)
        ON target.sourceSystemName = source.sourceSystemName
        WHEN MATCHED THEN
            UPDATE SET 
                target.sourceSystemDescription = source.sourceSystemDescription,
                target.entityNames = source.entityNames,
                target.keyVaultQuery = source.keyVaultQuery,
                target.notebooks = source.notebooks
        WHEN NOT MATCHED THEN
            INSERT (sourceSystemName, sourceSystemDescription, entityNames, keyVaultQuery, notebooks)
            VALUES ('{sourceSystemName}', '{sourceSystemDescription}', '{entityNames}', '{keyVaultQuery}', '{notebooks}');
        """

        # Execute the query:
        try:
            ddl_metadata(query) 
        except Exception as e:
            print(f'Error message: {e}')
        break
    