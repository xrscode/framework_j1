from dotenv import load_dotenv
import os
from azure.core.exceptions import ResourceNotFoundError
import pyodbc
from azure.identity import DefaultAzureCredential   # Required for Azure Key Vault
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
        strings = {'metadata': client.get_secret(metadata_string).value, 'totesys': client.get_secret(totesys_string).value}
    except Exception as e:
        return e
    # Return connection string dictionary:
    return strings


def ddl_metadata(query):
    """
    Arguments: query (str).
    Returns: result of query. 
    Description: This function queries the database and returns the result. 
    """
    

    # Establish Connection Details:
    connectionString = connection_strings(kv)['metadata']

    # Open the Connection:
    conn = pyodbc.connect(connectionString, autocommit = True)

    # Create Cursor:
    cursor = conn.cursor()

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
    
    # Establish Connection Details:
    connectionString = connection_strings(kv)['totesys']

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