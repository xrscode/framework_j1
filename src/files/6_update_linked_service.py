import json
import os
from dotenv import load_dotenv
from jsonschema import validate

"""
Note that paths need to be set from the ROOT folder.
"""
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

# Define paths to schemas:
keyvault_schema_path = './src/json_schema/azure_keyvault_schema.json'
databricks_schema_path = './src/json_schema/azure_databricks_schema.json'
metadata_database_schema_path = \
    './src/json_schema/azure_metadata_database_schema.json'

# Create list of file_paths to check:
file_paths = [azure_key_vault_ls, databricks_ls, data_lake_ls, 
                       metadata_ls, keyvault_schema_path, 
                       databricks_schema_path,
                       metadata_database_schema_path]

# Iterate through list and check files exist
for path in file_paths:
    if not os.path.isfile(path):
        raise FileNotFoundError(f'Path: {path} does not exist!')
    
# Load schema for keyvault:
with open(keyvault_schema_path, 'r') as file:
    keyvault_schema = json.load(file)

# Load schema for databricks:
with open(databricks_schema_path, 'r') as file:
    databricks_schema = json.load(file)

# Load schema for metada database:
with open(metadata_database_schema_path) as file:
    metadata_database_schema = json.load(file)

# Modify Azure Key Vault.json
with open(azure_key_vault_ls, 'r') as file:
    data = json.load(file)
    # Update properties > typeProperties > baseUrl:
    data['properties']['typeProperties']['baseUrl'] = keyvault_address
    
    # Validate schema:
    validate(data, keyvault_schema)

    # Write back to file:
    with open(azure_key_vault_ls, 'w') as file:
        json.dump(data, file, indent=4)
   
# Modify Metadata Database.json
with open(metadata_ls, 'r') as file:
    data = json.load(file)
    # Update properties > typeProperties > server:
    data['properties']['typeProperties']['server'] = metadata_database_server

    # Validate schema:
    validate(data, metadata_database_schema)
    
    # Write back to file:
    with open(metadata_ls, 'w') as file:
        json.dump(data, file, indent=4)

# Modify Framework Databricks.json
with open(databricks_ls, 'r') as file:
    data = json.load(file)
    # Update properties > typeProperties > domain:
    data['properties']['typeProperties']['domain'] = databricks_domain
    # ExistingClusterID:
    data['properties']['typeProperties']['existingClusterId'] = databricks_cluster_id
    
    # Validate schema:
    validate(data, databricks_schema)
    
    # Write back to file:
    with open(databricks_ls, 'w') as file:
        json.dump(data, file, indent=4)

    


