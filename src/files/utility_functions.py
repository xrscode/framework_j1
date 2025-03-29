from dotenv import load_dotenv
import os
import pyodbc
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Load dotenv:
load_dotenv()

# Get the keyvault name:
kv = os.getenv('k-v_name')


def keyvault_connection_strings(keyvault_name: str) -> dict:
    """
    Arguments:
        keyvault_name (str) : The name of the keyvault to access.
        secret (str) : The name of the secret to access.

    Raises:
        TypeError: if keyvault_name, or secret are not strings.

    Returns:
        Dict: of connection strings to sql databases used in this project.
    """

    # Raise error if keyvault_name is not a string:
    if not isinstance(keyvault_name, str):
        raise TypeError(f'Expecting strings.  Got: keyvault_name:\
                        {type(keyvault_name)}.')

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
        string_dict = {'metadata': client.get_secret(metadata_string).value,
                   'totesys': client.get_secret(totesys_string).value}
    except Exception as e:
        return e
    # Return connection string dictionary:
    return string_dict


def query_database(database_name: str, query: str):
    """
    This function accepts the name of a database and a query.
    It then queries the database and returns the results if there are any.

    Arguments:
        database_name (str): name of the database to query.
        query (str): the query to execute.
    Returns: 
        Tuples: If SELECT statement 10 results.
        String: Rows affected if not SELECT statement.

    Raises:
        pydobc.Error: if there is an error querying the database.
        TypeError: if the database_name or query are not string types.
    """

    # Check database is a string and query is a string:
    if not isinstance(database_name, str) or not isinstance(query, str):
        raise TypeError(f'Expected strings.  Got\
                        database_name: {type(database_name)}\
                        query:{type(query)}]')

    # Get connection string:
    connection_string = keyvault_connection_strings(kv)[database_name]

    # Open the Connection:
    conn = pyodbc.connect(connection_string, autocommit=False)

    # Create Cursor:
    cursor = conn.cursor()

    
    try:
        # Execute Query
        cursor.execute(query)
        rows_affected = cursor.rowcount

        # Fetch Results (if it's a SELECT query)
        if query.strip().lower().startswith("select"):
            results = cursor.fetchmany(10)  # Returns max 10 tuples
        else:
            results = f"Rows affected: {rows_affected}"
        
        # Commit changes for non-SELECT queries
        conn.commit()

        return results  # Return results or affected row count
    
    except pyodbc.Error as e:
        # Rollback changes if error:
        if conn:
            conn.rollback()
        # Handle specific database errors
        error_code = e.args[0] if e.args else "Unknown"
        return error_code
    
    finally:
        # Check if there is an open connection:
        if conn:
            # Close
            cursor.close()
            conn.close()
    


def list_folders(path: str) -> list:
    """
    Description: This function aims to list the folders/directories
    in the given path.  It can be used to help identify the individual source
    systems.  This function will return a list of all the directories/source
    systems at the specified location.  It does NOT return a path to the 
    source system.

    Args:
        path (str): Path to check for folders.

    Returns:
        folders (list): A list of folders located in the path.

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


def read_sql(path: str) -> str:
    """
    Args:
        path (str): Path to the sql file to read.

    Returns:
        query (str): SQL query as a string.

    Raises:
        TypeError: if path is not a string.
        ValueError: if path does not lead to sql file
    """

    # Check path is a string:
    if not isinstance(path, str):
        raise TypeError(f'Path must be a string.  Got: {type(path)}.')

    # Check path is valid:
    if not os.path.exists(path):
        raise FileNotFoundError(f'File: {path} does not exist.')

    # Read from file and convert to string:
    with open(path, 'r') as file:
        query = file.read()

    return query