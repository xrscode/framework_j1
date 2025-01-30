import json
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv
import os
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError

# Load the dotenv:
load_dotenv()


# First Establish Connection Details from Contract:
with open('./src/contracts/_sourceSystem.json', 'r') as f:
    connectionDetails = json.load(f)

# Define the Connection String and Container Name:
sas_token = os.getenv("SAS_TOKEN")
account_url = connectionDetails['connectionDetails']['account_url']
container_name = connectionDetails['connectionDetails']['containerName']

# Create a blob service client:
blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)

# Get a container client to interact with the container
container_client = blob_service_client.get_container_client(container_name)

print(container_client)

