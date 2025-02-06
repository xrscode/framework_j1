import json
from utility_functions import ddl

"""
This python file will take a sourceSystemContract.json and upload it into the database. 
Note that in order to get the correct sourceSystemContract, when prompted enter the
source system name/folder name.  For example, 'AdventureWorks' is a folder that contains
the _sourceSystem.json for the AdventureWorks source System.
"""

# Set the source system name to be uploaded:
sourceSystemName = input('Enter the source system name:')
sourceSystemPath = f'./src/contracts/{sourceSystemName}/_sourceSystem.json'

# Load the source system contract JSON:
with open(sourceSystemPath, 'r') as file:
    sourceSystemContract = json.load(file)
    
# Begin to build up query:
sourceEntityName = sourceSystemContract['name']
sourceEntityDescription = sourceSystemContract['description']
keyVaultQuery = sourceSystemContract['keyVaultQuery']

# Define the query:
query = f"""
DELETE FROM sourceSystem
WHERE sourceEntityName = '{sourceEntityName}';
INSERT INTO sourceSystem (sourceEntityName, sourceEntityDescription, keyVaultQuery)
VALUES ('{sourceEntityName}', '{sourceEntityDescription}', '{keyVaultQuery}');
"""

# Execute the query:
try:
    rowCount = ddl(query)
    if rowCount == -1:
        print(f'Source System: {sourceEntityName} upload successful.')
except Exception as e:
    print(f'Error message: {e}')
    