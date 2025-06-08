from utility_functions import return_source_system_path, choose_source, \
    query_database, list_folders
from check_db_connection import check_connection
import json
import os

"""
This python file will take a sourceSystemContract.json and upload
it into the database.Note that in order to get the correct
sourceSystemContract, when prompted enter the source system
Use the up and down arrow keys to select the source system to upload.
New source systems should be placed in src/contracts/<sourceSystemName>
"""

def upload_source_system_contract(path: str) -> None:
    """
    Description:
    Args:
        path (str): Path to the source system contract to upload.
    Returns:
        Nothing.
    Raises:
        TypeError: If path is not a string.
        FileNotFoundError: If path does not exist.
        FileNotFoundError: If path is not a file.
    """

    # Check path is not 'Exit':
    if path == 'Exit':
        print('Exiting...')
        return

    # Check type of path is string:
    if not isinstance(path, str):
        raise TypeError('Path must be a string')

    # Check path is valid:
    if not os.path.exists(path):
        raise FileNotFoundError(f'Path: {path} does not exist.')

    # Open the path:
    with open(path, 'r') as file:
        # Load the json file:
        sourceSystemContract = json.load(file)

    source_system_name = sourceSystemContract['name']
    source_system_type = sourceSystemContract['sourceType']
    source_system_description = sourceSystemContract['description']
    entity_names = str(sourceSystemContract['entityNames']).replace("'", '"')
    key_vault_query = sourceSystemContract['keyVaultQuery']
    notebooks = str(sourceSystemContract['notebooks']).replace("'", '"')

    # Merge prevents sourceSystemID from incrementing on match:
    query = f"""
    MERGE INTO dbo.sourceSystem AS target
USING (
    VALUES (
    '{source_system_name}',
    '{source_system_type}',
    '{source_system_description}',
    '{entity_names}',
    '{key_vault_query}',
    '{notebooks}'
    )
) AS source (
    sourceSystemName,
    sourceType,
    sourceSystemDescription,
    entityNames,
    keyVaultQuery,
    notebooks
)
ON target.sourceSystemName = source.sourceSystemName
WHEN MATCHED THEN
    UPDATE SET
        target.sourceSystemName = source.sourceSystemName,
        target.sourceType = source.sourceType,
        target.sourceSystemDescription = source.sourceSystemDescription,
        target.entityNames = source.entityNames,
        target.keyVaultQuery = source.keyVaultQuery,
        target.notebooks = source.notebooks
WHEN NOT MATCHED THEN
    INSERT (
        sourceSystemName,
        sourceType,
        sourceSystemDescription,
        entityNames,
        keyVaultQuery,
        notebooks
    )
    VALUES (
    '{source_system_name}',
    '{source_system_type}',
    '{source_system_description}',
    '{entity_names}',
    '{key_vault_query}',
    '{notebooks}'
    );
    """
    print('Query: \n')
    
    # Execute the query:
    result = query_database('metadata', query)
    print(result)
    return result


# First get list of source systems:
source_systems = list_folders('./src/contracts/')

# Next, prompt user to select source system:
choice = choose_source(source_systems)

# Define the path to the _sourceSystem.json:
path = return_source_system_path(choice)

# Upload sourceSystem.json contract:
upload_source_system_contract(path)
