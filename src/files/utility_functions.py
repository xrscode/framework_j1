import json
from dotenv import load_dotenv
import os
from azure.core.exceptions import ResourceNotFoundError
import pyodbc
import requests


def create_tables(query):
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

    return 'Query executed successfully.'


my_query = """-- Purpose: Create the sourceSystem table.

-- Remove the existing table if it exists
DROP TABLE IF EXISTS sourceSystem;

-- Create the sourceSystem table
CREATE TABLE sourceSystem (
    entityID INT IDENTITY(1,1) PRIMARY KEY, -- Auto-incrementing primary key
    entityName VARCHAR(255) NOT NULL UNIQUE, -- Unique entity name
    entityDescription VARCHAR(255), -- Description of the entity
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
);"""

create_tables(my_query)