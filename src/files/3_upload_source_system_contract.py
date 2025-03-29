from utility_functions import query_database, list_folders
import inquirer
import json
import os

"""
This python file will take a sourceSystemContract.json and upload
it into the database.Note that in order to get the correct
sourceSystemContract, when prompted enter the source system
Use the up and down arrow keys to select the source system to upload.
New source systems should be placed in src/contracts/<sourceSystemName>
"""


def choose_source_system(source_systems: list) -> str:
    """
    Description: The purpose of this function is to accept a list
    (of source systems) and present the user with those options to choose from.
    The user will be prompted to select the source system using the up/down
    arrows in the terminal.

    The function will check that 'Exit' is in the list of source systems.
    If it is not, it will append it to the list so the user can select 'Exit',
    if they do not wish to upload a contract.

    Args:
        source_systems (list) of (str's): List of source systems to choose.
    Returns:
        path to source system (str): The path to the source system contract.
        e.g: './src/contracts/AdventureWorks/_sourceSystem.json'
    Raises:
        TypeError: If source_systems is not a list.
        TypeError: If value in list is not string.
    """

    # Check if source_systems is a list:
    if not isinstance(source_systems, list):
        raise TypeError('source_systems must be a list')

    # Check all values are strings:
    if not all(isinstance(i, str) for i in source_systems):
        raise TypeError('All values in source_systems must be strings')

    # Check 'Exit' exists in list of source_systems:
    if 'Exit' not in source_systems:
        # If not append:
        source_systems.append('Exit')

    while True:
        questions = [
            inquirer.List(
                'choice',
                message="Which source system would you like to upload?",
                choices=source_systems,
            )]

        source_system_name = inquirer.prompt(questions)['choice']

        if source_system_name == 'Exit':
            # Return 'Exit' if the user chooses to exit:
            return 'Exit'

        else:
            # Return path of the source system:
            return f'./src/contracts/{source_system_name}/_sourceSystem.json'


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

    # Begin to build up query:
    sourceSystemName = sourceSystemContract['name']
    sourceSystemDescription = sourceSystemContract['description']
    keyVaultQuery = sourceSystemContract['keyVaultQuery']
    entityNames = str(
        sourceSystemContract['entityNames']).replace(
        "'", '"')
    notebooks = str(sourceSystemContract['notebooks']).replace("'", '"')

    # Merge prevents sourceSystemID from incrementing on match:
    query = f"""
    MERGE INTO dbo.sourceSystem AS target
    USING (VALUES ('{sourceSystemName}', '{sourceSystemDescription}',
    '{entityNames}','{keyVaultQuery}', '{notebooks}'))
        AS source (sourceSystemName, sourceSystemDescription,
    entityNames, keyVaultQuery, notebooks)
    ON target.sourceSystemName = source.sourceSystemName
    WHEN MATCHED THEN
        UPDATE SET
            target.sourceSystemDescription = source.sourceSystemDescription,
            target.entityNames = source.entityNames,
            target.keyVaultQuery = source.keyVaultQuery,
            target.notebooks = source.notebooks
    WHEN NOT MATCHED THEN
        INSERT (sourceSystemName, sourceSystemDescription, entityNames,
        keyVaultQuery, notebooks)
            VALUES ('{sourceSystemName}', '{sourceSystemDescription}',
            '{entityNames}', '{keyVaultQuery}', '{notebooks}');
    """

    # Execute the query:
    try:
        result = query_database('metadata', query)
        print(f"Uploaded: {sourceSystemName}. {result}.")
    except Exception as e:
        print(f'Error message: {e}')


# First get list of source systems:
source_systems = list_folders('./src/contracts/')

# Next, prompt user to select source system:
source_system_path = choose_source_system(source_systems)

# Next call the upload_source_system_contract function:
upload_source_system_contract(source_system_path)
