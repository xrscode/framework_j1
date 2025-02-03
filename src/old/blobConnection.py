import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
import os

# Load the dotenv:
load_dotenv()


# First Establish Connection Details from Contract:
with open('../contracts/_sourceSystem.json', 'r') as f:
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

print(blob_data)