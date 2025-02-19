from dotenv import load_dotenv
import os
from azure.core.exceptions import ResourceNotFoundError
import pyodbc

def connection_string_metaData():
    # Load password:
    password = os.getenv('serverPassword')
    connectionString = os.getenv('connectionStringMetaData')
    connectionString = connectionString.replace("{your_password_here}", password)
    return connectionString

def connection_string_totesys():
    # Load password:
    password = os.getenv('serverPassword')
    connectionString = os.getenv('connectionStringTotesys')
    connectionString = connectionString.replace("{your_password_here}", password)
    return connectionString



def ddl(query):
    """
    Arguments: query (str).
    Returns: result of query. 
    Description: This function queries the database and returns the result. 
    """
    # Load dotenv:
    load_dotenv()


    # Establish Connection Details:
    connectionString = connection_string_metaData()

    # Open the Connection:
    conn = pyodbc.connect(connectionString)

    # Create Cursor:
    cursor = conn.cursor()
    # Enable autocommit:
    conn.autocommit = True

    # Execute the query:
    try:
        cursor.execute(query)
    except Exception as e:
        print(f'Error: {e}')

    # Close the connection:
    cursor.close()
    conn.close()

    return cursor.rowcount


def ddl_totesys(query):
    """
    Arguments: query (str).
    Returns: result of query. 
    Description: This function queries the database and returns the result. 
    """
    # Load dotenv:
    load_dotenv()

    # Establish Connection Details:
    connectionString = connection_string_totesys()

    # Open the Connection:
    conn = pyodbc.connect(connectionString)

    # Create Cursor:
    cursor = conn.cursor()
    # Enable autocommit:
    conn.autocommit = True

    # Execute the query:
    try:
        cursor.execute(query)
    except Exception as e:
        print(f'Error: {e}')

    # Close the connection:
    cursor.close()
    conn.close()

    return cursor.rowcount