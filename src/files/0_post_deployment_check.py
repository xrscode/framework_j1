import os
from dotenv import load_dotenv
from utility_functions import get_secret_from_keyvault
from check_db_connection import check_connection

"""
The purpose of this file is to run post deployment logic to make sure
that the infrastructure has been setup correctly. 
"""
# Get the project root (Go two levels up!)
project_root = \
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) 


# Define path to env:
env_path = os.path.join(project_root, '.env')


# Check that the env has been created:
env_path = os.path.join(project_root, '.env')

# Check that the env exists:
if not os.path.exists(env_path):
    raise FileNotFoundError(f'The env does not exist at path: {env_path}.')


# Define variables to check:
required_vars = [
    'server_name', 'server_user', 'server_password',
    'account_url', 'keyvault_name',
    'totesysConnectionStringADO', 'dataLakeConnectionString'
]

# Remove from dotenv incase of updates:
for var in required_vars:
    os.environ.pop(var, None)

# Now reload env:
load_dotenv(dotenv_path=env_path, override=True)

# Determine if any are missing:
missing_variables = [var for var in required_vars if os.getenv(var) == None]


# Raise error if missing:
if missing_variables:
    raise FileNotFoundError(f"The following variables were not found in the env file: {', '.join(missing_variables)}. Without variables in the env file, it is not possible to establish connectionis with Azure resources.")


"""
KEYVAULT
"""
# Try to get sas_token from keyvault:
sas_token = get_secret_from_keyvault(os.getenv('keyvault_name'), 'sastoken')


"""
SQL DATABASE
"""
# This function will check the connection to the sql database:
check_connection()