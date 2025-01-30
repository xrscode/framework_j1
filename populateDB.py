import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# First Establish Connection Details
with open('./src/contracts/_sourceSystem.json', 'r') as f:
    connectionDetails = json.load(f)


products_conneciton_string = connectionDetails['connectionDetails']['blobConnectionString']