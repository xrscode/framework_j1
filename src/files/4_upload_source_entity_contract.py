import json
from utility_functions import ddl_metadata
import os
import inquirer

"""
This python file will take a sourceEntityContract.json and upload it into
the metadata database.
"""

path = './src/contracts'


def list_folders(path: str) -> list:
    """
    Description: This function aims to list the folders/directories
    in the given path.  It can be used to help identify the individual source
    systems.  This function will return a list of all the directories/source
    systems at the specified location.

    Args:
        Str: Path to check for folders.

    Returns:
        List: A list of folders located in the path.

    Raises:
        TypeError: If path is not string format.
        FileNotFoundError: If path does not exist.
        FileNotFoundError: If path is not a directory.
    """
    # Check path is string:
    if not isinstance(path, str):
        raise TypeError('Path must be a string')

    # Check path is valid:
    if not os.path.exists(path):
        raise FileNotFoundError(f'Path: {path} does not exist.')

    # Check path is valid directory:
    if not os.path.isdir(path):
        raise FileNotFoundError(f'Path: {path} is not a directory.')

    # Assimilate list of folders to return:
    list_of_folders = [folder for folder in os.listdir(path)]

    return list_of_folders


def choose_entity_contract(sourceSystems: list) -> str:
    """
    This function accepts a list of source systems.
    It appends 'exit' to the list.  Using inquirier, it creates a selection
    of source systems for the user to choose from.  After selection, the
    function returns that source system name as a string:

    Args:
        List: A list of the source system names to choose from.

    Returns:
        Str:  The users choice of source system as a string.

    Raises:
        TypeError:  If the argument is not a list or is empty.
    """

    # Check is list and not empty:
    if not isinstance(sourceSystems, list) or not sourceSystems:
        raise TypeError(f"""Expected type: list of length > 0.
        Got: {type(sourceSystems)} of length {len(sourceSystems)}""")

    # Check list composed of strings:
    if not all(isinstance(item, str) for item in sourceSystems):
        raise TypeError('All sourceSystems must be of type list.')

    # Append 'Exit' to sourceSystems list:
    sourceSystems.append('Exit')

    while True:
        questions = [
            inquirer.List(
                'SourceSystem',
                message="Please select a source system.",
                choices=sourceSystems)]
        choice = inquirer.prompt(questions)['SourceSystem']

        return choice


def upload_source_entity_contract(path: str, sourceSystemName: str):
    """
    This function accepts a path to a list of contracts.  It also accepts
    The name of the entity to upload.  This function determines which contracts
    there are to upload.  It then creates a query before querying the metadata
    database to upload the contract:

    Args:
        List: Path to source system and name of source system.

    Returns:

    Raises:
        TypeError:  If arguments are not in string format..
    """

    # Raise TypeError if incorrect types given.
    if not isinstance(path, str) or not isinstance(sourceSystemName, str):
        raise TypeError(f'Expected strings.  Path is {type(path)}.\
                        SourceSystemName is {type(sourceSystemName)} ')

    # If sourceSystemName is Exit return:
    if sourceSystemName == 'Exit':
        return

    # Define the path to the source entity contract:
    sourceEntityPath = f'{path}/{sourceSystemName}/'

    # List all files in the folder and ignore _sourceSystem.json:
    json_files = [f for f in os.listdir(sourceEntityPath) if f.endswith(
        ".json") and f != "_sourceSystem.json"]

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
        entityIngestionColumns = str(
            d['ingestion_columns']).replace(
            "'",
            '"').replace(
            "True",
            "true").replace(
            "False",
            "false")

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
                PRINT 'Error: sourceSystemName ''{sourceSystemName}''
                does not exist.';
                RETURN; -- Exit the script
            END;

            -- Perform MERGE operation
            MERGE INTO sourceEntity AS target
            USING (SELECT @sourceSystemID AS sourceSystemID, '{entityName}'
                AS entityName) AS source
            ON target.sourceSystemID = source.sourceSystemID
                AND target.entityName = source.entityName
            WHEN MATCHED THEN
                UPDATE SET
                    entityDescription = '{entityDescription}',
                    entitySourceQuery = '{entitySourceQuery}',
                    entityIngestionColumns = '{entityIngestionColumns}'
            WHEN NOT MATCHED THEN
                INSERT (sourceSystemID, entityName, entityDescription,
                entitySourceQuery, entityIngestionColumns)
                VALUES (@sourceSystemID, '{entityName}', '{entityDescription}',
                '{entitySourceQuery}', '{entityIngestionColumns}');
            """

        # Execute the query:
        try:
            print(f'Uploading entity: {entityName}')
            ddl_metadata(query)
        except Exception as e:
            print(f'Error message: {e}')


# First determine list of source entities:
source_entities = list_folders(path)

# Choose which source entity to upload:
choice = choose_entity_contract(source_entities)

# Upload source entity contract to metadata database:
upload_source_entity_contract(path, choice)
