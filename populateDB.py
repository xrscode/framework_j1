import json
from azure.identity import DefaultAzureCredential, ClientSecretCredential, InteractiveBrowserCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
import os
from azure.core.exceptions import ResourceNotFoundError
import pandas as pd
from io import StringIO
import pyodbc

# Load the dotenv:
load_dotenv()


# First Establish Connection Details from Contract:
with open('./src/contracts/_sourceSystem.json', 'r') as f:
    connectionDetails = json.load(f)

# Define the Connection String and Container Name:
sas_token = os.getenv("SAS_TOKEN")
connection_string = connectionDetails['connectionDetails']['connectionString']
conatinerName = connectionDetails['connectionDetails']['containerName']
blob_location = connectionDetails['connectionDetails']['fileLocation']


# Create client:
blob_service_client = BlobServiceClient(account_url=connection_string, credential=sas_token)

# Get the blob client for the specific blob (products.csv):
blob_client = blob_service_client.get_blob_client(container=conatinerName, blob=blob_location)

# Download products.csv:
blob_data = blob_client.download_blob().readall().decode('utf-8').split('\n')

# Now Begin to build up SQL QUERY:

# Define headers:
header = ', '.join(blob_data[0].split(','))


# Define the values:
val_str = ""
values = blob_data
for value in values[1:]:
    v = value.split(',')
    x = [f"'{i}'" for i in v]
    val_str += f"({', '.join(x)}), \n"
# Remove final comma:
val_str = val_str[:-3]

# Construct SQL Query 
query = f"""INSERT INTO products ({header}) 

VALUES {val_str};"""


"""
The next step is  to connect to the SQL Server/Database.
"""

# Database connection details:
server = os.getenv('serverName')
database = os.getenv('databaseName')
admin = os.getenv('serverAdmin')
password = os.getenv('serverPassword')
connectionString = os.getenv('connectionString')

# # Set connection string:
# connectionString = f"""Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:framework-j1-sv.database.windows.net,1433;Database=framework-j1-db;Uid=adminsjp;Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"""

# Open Connection:
conn = pyodbc.connect(connectionString) 

# Create cursor:
cursor = conn.cursor()

SQL_QUERY = f"""CREATE TABLE Products (
ProductID int,
ProductName varchar,
ProductNumber varchar,
Category varchar,
ListPrice varchar
);"""

try:
    # Execute the query:
    cursor.execute(SQL_QUERY)
except Exception as e:
    print(e)

# Close connection:
cursor.close()
conn.close()