import os
from src.files.utility_functions import load_dotenv, get_secret_from_keyvault,\
create_data_lake_directory_client, get_current_date_path, delete_directory

"""
In this challenge, run this script.

After you have run it, in ADF run the pipeline for AdventureWorks again, to 
see what has happened!

You can then run pytest to see what is happening:
---------------------------------------------------------------------------
pytest -vv ./challenges/tests/test_challenge_4.py
---------------------------------------------------------------------------

"""

# Refresh dotenv:
load_dotenv(override = True)

# Keyvault name:
keyvault_name = os.getenv('keyvault_name')

# Define sas token:
sas_token = get_secret_from_keyvault(keyvault_name, 'sastoken')

# Define account url:
account_url = os.getenv('account_url')

# Define the expected directory locations:
expected_file_locations_bronze = [
f'/framework-j1/BRONZE/AdventureWorks/customer_AW/{get_current_date_path()}',
f'/framework-j1/BRONZE/AdventureWorks/products_AW/{get_current_date_path()}',
f'/framework-j1/BRONZE/AdventureWorks/sales_order_AW/{get_current_date_path()}'
]

# Iterate through expected_file_locations:
for loc in expected_file_locations_bronze:
    # Create client for location:
    client = create_data_lake_directory_client(account_url, loc, sas_token)
    delete_directory(client)

    