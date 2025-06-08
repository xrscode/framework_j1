import re
from utility_functions import query_database, pyodbc, load_dotenv, os
from azure.identity import DefaultAzureCredential
from azure.mgmt.sql import SqlManagementClient

"""
There is a strange bug where if this project is deployed from the London
Telefonica office the WAN ip address of the computer ends in 210.
When pyodbc tries to connect to SQL server from the same machine Azure
registers the ip address as coming from a different WAN ip; 209.

This file queries the metadata database.  If an error is thrown, it will
grab the blocked ip address.

It will then add a firewall rule to sql server allowing the blocked ip address.

Remaining python files should then work correctly to setup the database.
"""

# Refresh dotenv:
load_dotenv(override=True)

# Access subscription id:
subscription_id = os.getenv('subscription_id')
# Access resource group name:
resource_group = os.getenv('resource_group_name')
# Acces sql server NAME NOT server address.
sql_server = os.getenv('server_name').replace('.database.windows.net', '')


def check_connection():
    # Attempt to connect to the sql server:
    try:
        # Simple query
        query_database('metadata', 'Select 1')
        
        print('Your current ip address has access to Azure services.  Firewall update not necessary.')
    except pyodbc.Error as e:
        # If there is an error extract the ip address:
        ip_regex = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        # Take the first instance:
        ip_address = re.findall(ip_regex, str(e))[0]
        print(f'ip {ip_address} is blocked...adding firewall rule.')

        # Authenticate
        credential = DefaultAzureCredential()
        sql_client = SqlManagementClient(credential, subscription_id)

        try:
            # Create or update the firewall rule
            firewall_rule = sql_client.firewall_rules.create_or_update(
                resource_group,
                sql_server,
                'allow_blocked_ip',
                {
                    "start_ip_address": ip_address,
                    "end_ip_address": ip_address,
                },
            )
            print(f"Firewall rule {firewall_rule.name} added successfully!")
        except Exception as e:
            print(e)
            raise