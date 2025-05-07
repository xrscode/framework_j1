from dotenv import load_dotenv
import os
import pyodbc
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import csv
import inquirer
import json

# Refresh dotenv:
load_dotenv(override=True)

# Get the keyvault name:
keyvault_name = os.getenv('keyvault_name')


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

    accepted_databases = ['metadata', 'totesys']

    if database_name not in accepted_databases:
        raise ValueError(f'Database name: {database_name} not accepted.\
            Accepted database names are: {accepted_databases}.')

    # Check database is a string and query is a string:
    if not isinstance(database_name, str) or not isinstance(query, str):
        raise TypeError(f'Expected strings.  Got\
                        database_name: {type(database_name)}\
                        query:{type(query)}]')

    # Get connection string:
    connection_string = \
        keyvault_connection_strings(keyvault_name)[database_name]

    # Open the Connection:
    conn = pyodbc.connect(connection_string, autocommit=False)

    try:
        # Open the Connection
        conn = pyodbc.connect(connection_string, autocommit=False)
        
        # Create Cursor
        cursor = conn.cursor()
        
        # Execute Query
        cursor.execute(query)
        
        # Try to fetch results - this will work for SELECT statements
        try:
            results = cursor.fetchall()
            conn.commit()
            return results
        except pyodbc.ProgrammingError as pe:
            # If we get "No results. Previous SQL was not a query"
            if "No results" in str(pe) and "not a query" in str(pe):
                # It's an UPDATE/INSERT/DELETE or other non-query statement
                affected_rows = cursor.rowcount
                conn.commit()
                if affected_rows == -1:
                    return f"Query executed successfully. Database infrastructure created."
                else:
                    return f"Query executed successfully. Rows affected: {affected_rows}"
            else:
                # Some other programming error
                raise pe
            
    except pyodbc.Error as e:
        # Rollback changes if error
        if conn:
            conn.rollback()
        return f"Database error!"
        
    finally:
        # Check if there is an open connection
        if cursor:
            cursor.close()
        if conn:
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
    list_of_folders = [folder for folder in os.listdir(path)
                       if os.path.isdir(os.path.join(path, folder))]

    return list_of_folders


def read_sql(path: str) -> str:
    """
    Description: This function reads a sql file and returns the query
    as a string.

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


def open_csv(path):
    """
    Args:
        path (str): path of the CSV file to read.
    
    Returns:
        data (list): List of rows within CSV (excluding header if specified).
    
    Raises:
        ValueError: if the csv is empty.
        ValueError: if the found header is missing or invalid.
        FileNotFoundError: if the path is not valid.
        CSV Error: if the csv file can not be read.
    
    """
    # Define anticipated header for entity contract:
    header_entity = ['name','description','connectionString',\
                     'sourceQuery', 'sortOrder','columnName',\
                        'dataType','required','primary_key']
    
    # Define anticipated header for source contract:
    header_source = ['name','description','sourceType','keyVaultQuery',\
                     'entityNames','notebooks']

    # Check path is correct:
    if not os.path.isfile(path):
        raise FileNotFoundError(f'File not found at: {path}!')

    # Check if file is empty
    if os.path.getsize(path) == 0:
        raise ValueError('CSV file is empty!')

    # Try to open csv:
    try:
        with open(path, newline='', encoding='utf8') as csvfile:
            # Create a reader object:
            reader = csv.reader(csvfile, delimiter=',')
            
            # Access the first row and remove whitespaces:
            header = [x.strip() for x in next(reader)]
            # Reader has now iterated along by 1.  Remaining data
            # should just be the data needed to build the contract.
            
            # Check header exists and is valid:    
            if header != header_entity and header != header_source:
                raise ValueError(f"""Header does not exist or is invalid!
                                Header in csv is; {header}.
                                """)
            
            # Return data, make sure to remove whitespace:
            data = [[cell.strip() for cell in row] for row in reader]

    # Return csv error if csv can't be opened:
    except csv.Error as e:
        raise csv.Error(f"Error reading CSV file: {e}")
    
    # Return data: 
    return data


def choose_source(source_systems: list) -> str:
    """
    Description: The purpose of this function is to accept a list
    (of source systems) and present the user with those options to choose from.
    The user will be prompted to select the source system using the up/down
    arrows in the terminal.

    The function will check that 'Exit' is in the list of source systems.
    If it is not, it will append it to the list so the user can select 'Exit',
    if they do not wish to upload a contract.

    When a source system has been chosen, this function will return the
    name of that selected source system.

    Args:
        source_systems (list) of (str's): List of source systems to choose.
    Returns:
        Name of the source system.
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
                message="Select source system",
                choices=source_systems,
            )]

        source_system_name = inquirer.prompt(questions)['choice']

        if source_system_name == 'Exit':
            # Return Nothing if the user chooses to exit:
            return

        else:
            # Return path of the source system:
            return source_system_name


def return_source_system_path(source_system: list) -> str:
    """
    The purpose of this function is to accept the name of a source system.
    It will then return the path to the _sourceSystem.json.

    Args:
        source_system (str): Name of source system.
    Returns:
        path to source system (str): The path to the source system contract.
        e.g: './src/contracts/AdventureWorks/_sourceSystem.json'
    Raises:
        TypeError: If source_system is not a string.
        FileNotFoundError: If the file does not exist for source system.
    """

    # Check if source_system is a list:
    if not isinstance(source_system, str):
        raise TypeError(f'source_system must be a string.\
                        Got {type(source_system)}.')

    # Expected path:
    path = f'./src/contracts/{source_system}/_sourceSystem.json'

    # Check that the file exists:
    if not os.path.isfile(path):
        raise FileNotFoundError(f'File not found at path: \n{path}!')

    else:
        # Return path of the source system:
        return path


def delete_file(path: str):
    """
    This function deletes a file at the specified path.

    Args:
        path (str): string file path.
    Returns:
        Nothing.
    Raises:
        Nothing: This function should not raise an error.  As it removes
        file if the file exists and does nothing if it does not exist.
    """
    if os.path.isfile(path):
        # Delete if file exists:
        os.remove(path)
        return
    else:
        return


def write_to_csv(path: str, data: list, header: list = None):
    """
    This function writes to a csv file.

    Args:
        path (str): The path where the csv file should be saved.
        data (list): Data to write to csv.
        header (list, optional): List of strings - to define the header.

    Raises:
        TypeError: If path is not a string or if data/header are not lists.

    Returns:
        str: Success message.
    """
    # Set header to empty list if it does not exist:
    if header is None:
        header = []

    # Check that path is a string
    if not isinstance(path, str):
        raise TypeError(f'Path expects string. Got: {type(path)}.')

    # Check that data and header are lists:
    if not isinstance(data, list):
        raise TypeError(f'Data should be a list, got: {type(data)}.')
    if not isinstance(header, list):
        raise TypeError(f'Header should be a list, got: {type(header)}.')

    # Write to CSV:
    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file)
        if header:
            writer.writerow(header)
        writer.writerows(data)

    return 'File written successfully.'


def load_json(path: str):
    """
    This function accepts a path to a JSON file. 
    It reads the JSON and returns it as a python object. 

    Args:
        path (str): The path to the JSON file. 

    Returns:
        object: : The python object parsed from the JSON file.
    """
    # Check path exists:
    if not isinstance(path, str):
        raise TypeError(f'Expected type string, got: {type(path)}')

    # Check file exists:
    if not os.path.isfile(path):
        raise FileNotFoundError(f'File not found at; {path}!')

    # Open JSON file:
    with open(path, 'r') as json_data:
        data = json.load(json_data)

    # Return the data:
    return data

    