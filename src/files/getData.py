import json
from dotenv import load_dotenv
import os
from azure.core.exceptions import ResourceNotFoundError
import pyodbc
import requests

# Load the dotenv:
load_dotenv()

"""
SQL SERVER/DATABASE CONNECTION
"""

# Database connection details:
server = os.getenv('serverName')
database = os.getenv('databaseName')
admin = os.getenv('serverAdmin')
password = os.getenv('serverPassword')
connectionString = os.getenv('connectionString')

# Open Connection:
conn = pyodbc.connect(connectionString) 

# Create cursor:
cursor = conn.cursor()
conn.autocommit = True

# Query the Metadata:
SQL_QUERY_METADATA = f"""SELECT * FROM metaData;"""

# Execute the query:
try:
    cursor.execute(SQL_QUERY_METADATA)
    rows = cursor.fetchall()
except Exception as e:
    print(e)

# Save metaData to dictionary:
metaData = {
    'entityID': rows[0][0],
    'entityName': rows[0][1],
    'entityDescription': rows[0][2],
    'connectionSourceType': rows[0][3],
    'connectionRequestType': rows[0][4],
    'connectionString': rows[0][5],
    'fileName': rows[0][6],
    'fileFormat': rows[0][7],
    'delimiterColumn': rows[0][8],
    'delimiterRow': rows[0][9]
}

# Close connection:
cursor.close()
conn.close()

# Make GET request to the API:
x = requests.get(metaData['connectionString'])
y = x.text.split(metaData['delimiterRow'])
header = y[0]
data = y[1:]

print(data[1])