import json
import os
from dotenv import load_dotenv

# Re-load dotenv:
load_dotenv(override=True)

# Set values:
databricks_cluster_id = os.getenv('databricksClusterID')
databricks_domain = f'https://{os.getenv('databricks_workspace_url')}'
keyvault_address = f'https://{os.getenv('keyvault_name')}.vault.azure.net/'
metadata_database_server = os.getenv('server_name')

# Define paths to linked services:
linked_service_path = './linkedService/'
azure_key_vault_ls = f'{linked_service_path}Azure Key Vault.json'
databricks_ls = f'{linked_service_path}Framework Databricks.json'
data_lake_ls = f'{linked_service_path}Azure Key Vault.json'
metadata_ls = f'{linked_service_path}Metadata Database.json'


# Create list of file_paths to check:
linked_service_list = [azure_key_vault_ls, databricks_ls, data_lake_ls, 
                       metadata_ls]

# Iterate through list and check files exist
for path in linked_service_list:
    if not os.path.isfile(path):
        raise FileNotFoundError(f'Path: {path} does not exist!')
    

# Modify Azure Key Vault.json
with open(azure_key_vault_ls, 'r') as file:
    data = json.load(file)
    # Update properties > typeProperties > baseUrl:
    data['properties']['typeProperties']['baseUrl'] = keyvault_address
    # Write back to file:
    with open(azure_key_vault_ls, 'w') as file:
        json.dump(data, file, indent=4)
   



    


