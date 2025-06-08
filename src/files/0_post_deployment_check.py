from dotenv import load_dotenv
from utility_functions import get_secret_from_keyvault, query_database, pyodbc, os
import re
from azure.identity import DefaultAzureCredential
from azure.mgmt.sql import SqlManagementClient
from azure.storage.filedatalake import DataLakeServiceClient

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
missing_variables = [var for var in required_vars if os.getenv(var) is None]


# Raise error if missing:
if missing_variables:
    raise FileNotFoundError(f"The following variables were not found in the env file: {', '.join(missing_variables)}. Without variables in the env file, it is not possible to establish connectionis with Azure resources.")
else:
    print('ENV exists with expected variables.  Attempting to connect to sql database, keyvault and data lake.')


"""
KEYVAULT
"""
# Try to get sas_token from keyvault:
sas_token = get_secret_from_keyvault(os.getenv('keyvault_name'), 'sastoken')
# Note that the function already has error handling.


"""
DATALAKE
"""


def check_datalake_connection():
    """
    This function checks a connection has been made to the data lake.
    """
    try:
        # Setup credential:
        credential = DefaultAzureCredential()

        # Define url to check:
        url = os.getenv('account_url')

        # Define the client
        client = DataLakeServiceClient(url, credential)

        # Try to list file systems:
        file_systems = list(client.list_file_systems())

        # Print result:
        print(f"Connection successful.  Found file system named: {file_systems[0]['name']}.")

    except Exception as e:
        print(f'Failed to connect to Data Lake.  Error message is: {e}.')
        raise


"""
SQL DATABASE
"""
# This function will check the connection to the sql database:


def check_connection():
    """
    The purpose of this function is to check the connection to the SQL database.
    It will try to determine if there are any firewall rules blocking the users
    ip address.  If the ip address is blocked, it will attempt to add a firewall
    rule so that the user can make a connection to the database.

    Args:
        None
    Returns:
        None
    Raises:
        PYODBC Error: If there is an error connecting to the sql database.
        Exception: If there is a problem trying to update firewall rule.

    """
    # If there is an error, use this regex to extract ip address:
    ip_regex = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

    # Attempt to connect to the sql server:
    try:
        # Simple query
        query_database('metadata', 'Select 1')
        print('Your current ip address has access to Azure services.  Firewall update not necessary.')
        return
    except pyodbc.Error as e:
        # If database query fails, examine error message for ip address:

        # Take the first instance:
        ip_address = re.findall(ip_regex, str(e))[0]

        # If the error message does not relate to an ip issue, return that
        # message.
        if not ip_address:
            return print(
                f"Error message not relating to ip address issue.  Message is: {e}.")

        # Authenticate
        credential = DefaultAzureCredential()
        sql_client = SqlManagementClient(
            credential, os.getenv('subscription_id'))

        try:
            # Create or update the firewall rule
            firewall_rule = sql_client.firewall_rules.create_or_update(
                os.getenv('resource_group_name'),
                os.getenv('server_name').replace('.database.windows.net', ''),
                'allow_blocked_ip',
                {
                    "start_ip_address": ip_address,
                    "end_ip_address": ip_address,
                },
            )
            print(f"Firewall rule {firewall_rule.name} added successfully!")
            return

        except Exception as e:
            # If firewall update fails raise error:
            raise


check_datalake_connection()
check_connection()
