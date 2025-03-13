from dotenv import load_dotenv
import os
from azure.core.exceptions import ResourceNotFoundError
import pyodbc
from azure.identity import DefaultAzureCredential   
from azure.keyvault.secrets import SecretClient

# Load dotenv:
load_dotenv()

# Get the keyvault name:
kv = os.getenv('k-v_name')

def connection_strings(keyvault_name: str) -> dict:
    # Define secret name for metadata:
    metadata_string = "metadataConnectionString"
    # Define seccret name for totesys:
    totesys_string = "totesysConnectionString"
    # Compose keyvault url:
    kv_url = f"https://{keyvault_name}.vault.azure.net/"
    # Define credential:
    credential = DefaultAzureCredential()
    # Define client:
    client = SecretClient(vault_url=kv_url, credential=credential)
    # Try to get secrets:
    try:
        strings = {'metadata': client.get_secret(metadata_string).value,\
                   'totesys': client.get_secret(totesys_string).value}
    except Exception as e:
        return e
    # Return connection string dictionary:
    return strings


def query_database(database_name: str, query: str):
    """
    This function accepts the name of a datbase and a query. 
    It then queries the database and returns the reuslts if there are any.
    
    Arguments: 
        database_name (str): name of the database to query.
        query (str): the query to execute.
    Returns: Nothing.

    Raises:
        pydobc.Error: if there is an error querying the database.
        TypeError: if the database_name or query are not string types. 
    """

    if not isinstance(database_name, str) or not isinstance(query, str):
        raise TypeError(f'Expected strings.  Got\
                        database_name: {type(database_name)}\
                        query:{type(query)}]')

    # Establish Connection Details:
    connectionString = connection_strings(kv)[database_name]

    # Open the Connection:
    conn = pyodbc.connect(connectionString, autocommit = False)

    # Create Cursor:
    cursor = conn.cursor()

    # Execute the query:
    try:
        cursor.execute(query)
        
    except pyodbc.Error as e:
        # Rollback changes if error:
        if conn:
            conn.rollback()
        # Handle specific database errors
        error_code = e.args[0] if e.args else "Unknown"
        return error_code

    # Rows affected
    rows_affected = cursor.rowcount
    if rows_affected > 0:
        print(f'Rows affected: {rows_affected}')
    else:
        print(f'No rows were changed.')

    # Commit:
    conn.commit()
    # Close
    cursor.close()
    conn.close()

    return cursor.rowcount


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