import json
from dotenv import load_dotenv
import os
from azure.core.exceptions import ResourceNotFoundError
import pyodbc

# Load the dotenv:
load_dotenv()

"""
SQL SERVER/DATABASE CONNECTION
This will set up the metaData table. 
If run, it will remove all data from the table.
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

SQL_QUERY_SCHEMA = f"""DROP TABLE IF EXISTS metaData;
CREATE TABLE metaData (
entityID INT IDENTITY(1,1) PRIMARY KEY,
entityName VARCHAR(255),
entityDescription VARCHAR(255),
connectionSourceType VARCHAR(255),
connectionRequestType VARCHAR(255),
connectionString VARCHAR(255),
fileName VARCHAR(255),
fileFormat VARCHAR(255),
delimiterColumn VARCHAR(255),
delimiterRow VARCHAR(255));"""


# Create Table
try:
    cursor.execute(SQL_QUERY_SCHEMA)
    print('Table and Schema created.')
except Exception as e:
    print(e)












"""
ADD METADATA TO DATABASE
"""

# First Establish Connection Details from Contract:
with open('../contracts/_sourceSystem.json', 'r') as f:
    connectionDetails = json.load(f)

entityName = connectionDetails['name']
entityDescription = connectionDetails['description']
connectionSourceType = connectionDetails['connectionDetails']['sourceType']
connectionRequestType = connectionDetails['connectionDetails']['requestType']
connectionString = connectionDetails['connectionDetails']['connectionString']
fileName = connectionDetails['connectionDetails']['fileName']
fileFormat = connectionDetails['connectionDetails']['fileFormat']
delimiterColumn = connectionDetails['connectionDetails']['delimiterColumn']
delimiterRow = connectionDetails['connectionDetails']['delimiterRow']

SQL_QUERY_DATA = f"""
INSERT INTO metaData (entityName, entityDescription, connectionSourceType, connectionRequestType, connectionString, fileName, fileFormat, delimiterColumn, delimiterRow)
VALUES
('{entityName}', '{entityDescription}', '{connectionSourceType}',
'{connectionRequestType}', '{connectionString}', '{fileName}',
'{fileFormat}', '{delimiterColumn}', '{delimiterRow}');"""
print(SQL_QUERY_DATA)

# # Add data:
try:
    print('Adding data... ', SQL_QUERY_DATA)
    cursor.execute(SQL_QUERY_DATA)
    print('Data added.')
except Exception as e:
    print(e)

# Close connection:
cursor.close()
conn.close()