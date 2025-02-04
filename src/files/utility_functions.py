import json
from dotenv import load_dotenv
import os
from azure.core.exceptions import ResourceNotFoundError
import pyodbc
import requests


def ddl(query):
    """
    Arguments: query (str).
    Returns: result of query. 
    Description: This function queries the database and returns the result. 
    """
    # Load dotenv:
    load_dotenv()

    # Establish Connection Details:
    connectionString = os.getenv('connectionString')

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