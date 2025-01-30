import json
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

try:
    print("Azure Blob Storage Python quickstart sample")

    # Quickstart code goes here

except Exception as ex:
    print('Exception:')
    print(ex)

# First Establish Connection Details
with open('./src/contracts/_sourceSystem.json', 'r') as f:
    connectionDetails = json.load(f)


products_conneciton_string = connectionDetails['connectionDetails']['blobConnectionString']

try:
    print("Azure Blob Storage Python quickstart sample")

    # Quickstart code goes here

except Exception as ex:
    print('Exception:')
    print(ex)