from src.files.utility_functions import query_database, get_secret_from_keyvault, load_dotenv,\
get_service_client_sas, list_directory_contents, get_current_date_path
import os
from datetime import date

# Refresh dotenv:
load_dotenv(override = True)

# File storage account:
account_url = os.getenv('account_url')

# Keyvault name:
keyvault_name = os.getenv('keyvault_name')

# Get SaS token from keyvault:
sas_token = get_secret_from_keyvault(keyvault_name, 'sastoken')

# Create Data Lake Object:
data_lake = get_service_client_sas(account_url, sas_token)

# Get the FileSystemClient:
file_system_client = data_lake.get_file_system_client(file_system='vivaldi')

# Get the current date:
current_date = get_current_date_path()


def test_bronzeLocation_in_metadata_database_has_data():
    """
    If the pipeline has run successfully, in the sourceEntity table you should
    see that there is a file path to data in the bronze location.
    """

    query = """
    DECLARE @ssid INT;

    SELECT @ssid = sourceSystemID
    FROM sourceSystem
    WHERE sourceSystemName = 'AdventureWorks';

    SELECT bronzeLocation 
    FROM dbo.sourceEntity
    WHERE sourceSystemID = @ssid;
    """ 

    results = query_database('metadata', query)
    assert all(x[0] != '' for x in results)



def test_silverLocation_in_metadata_database_has_data():
    """
    If the pipeline has run successfully, in the sourceEntity table you should
    see that there is a file path to data in the silver location.
    """

    query = """
    DECLARE @ssid INT;

    SELECT @ssid = sourceSystemID
    FROM sourceSystem
    WHERE sourceSystemName = 'AdventureWorks';

    SELECT silverLocation 
    FROM dbo.sourceEntity
    WHERE sourceSystemID = @ssid;
    """ 

    results = query_database('metadata', query)
    assert all(x[0] != '' for x in results)


def test_goldLocation_in_metadata_database_has_data():
    """
    If the pipeline has run successfully, in the sourceEntity table you should
    see that there is a file path to data in the gold location.
    """

    query = """
    DECLARE @ssid INT;

    SELECT @ssid = sourceSystemID
    FROM sourceSystem
    WHERE sourceSystemName = 'AdventureWorks';

    SELECT goldLocation 
    FROM dbo.sourceEntity
    WHERE sourceSystemID = @ssid;
    """ 
    results = query_database('metadata', query)
    assert all(x[0] != '' for x in results)


def test_bronzeLocation_has_todays_date_in_path():
    """
    If the pipeline has run successfully, in the sourceEntity table you should
    see that there is a file path to data in the bronze location.
    """

    query = """
    DECLARE @ssid INT;

    SELECT @ssid = sourceSystemID
    FROM sourceSystem
    WHERE sourceSystemName = 'AdventureWorks';

    SELECT bronzeLocation 
    FROM dbo.sourceEntity
    WHERE sourceSystemID = @ssid;
    """ 
    bronze_date = query_database('metadata', query)
    assert all(current_date in x[0] for x in bronze_date)

def test_silverLocation_path_is_correct():
    """
    If the pipeline has run successfully, the file paths should be in 
    the correct format.
    """

    query = """
    DECLARE @ssid INT;

    SELECT @ssid = sourceSystemID
    FROM sourceSystem
    WHERE sourceSystemName = 'AdventureWorks';

    SELECT silverLocation 
    FROM dbo.sourceEntity
    WHERE sourceSystemID = @ssid;
    """ 
    silver_paths = query_database('metadata', query)
    expected_paths = ['/AdventureWorks/customer_AW/', \
                      '/AdventureWorks/products_AW/', \
                        '/AdventureWorks/sales_order_AW/']
    found_paths = [x[0] for x in silver_paths]
    assert all(current_date not in x[0] for x in silver_paths)
    assert all(path in found_paths for path in expected_paths)


def test_goldLocation_path_is_correct():
    """
    If the pipeline has run successfully, the file paths should be in 
    the correct format.
    """

    query = """
    DECLARE @ssid INT;

    SELECT @ssid = sourceSystemID
    FROM sourceSystem
    WHERE sourceSystemName = 'AdventureWorks';

    SELECT goldLocation 
    FROM dbo.sourceEntity
    WHERE sourceSystemID = @ssid;
    """ 
    gold_paths = query_database('metadata', query)
    expected_paths = ['/AdventureWorks/customer_AW', \
                      '/AdventureWorks/products_AW', \
                        '/AdventureWorks/sales_order_AW']
    found_paths = [x[0] for x in gold_paths]
    print(gold_paths, found_paths)
    assert all(current_date not in x[0] for x in gold_paths)
    assert all(path in found_paths for path in expected_paths), f"Missing expected goldLocation paths. Expected: {expected_paths}, Found: {found_paths}"




def test_bronzeLocation_links_to_data_in_data_lake():
    """
    Data must also exist in the data lake.  This function will check to 
    ensure there is data.
    """
    # Define the expected file locations:
    expected_file_locations = [
    f'/framework-j1/BRONZE/AdventureWorks/customer_AW/{current_date}/customer_AW.csv',
    f'/framework-j1/BRONZE/AdventureWorks/products_AW/{current_date}/products_AW.csv',
    f'/framework-j1/BRONZE/AdventureWorks/sales_order_AW/{current_date}/sales_order_AW.csv'
    ]

    # Iterate through the expected file locations:
    for file in expected_file_locations:
        # Query the data lake to see if file exists:
        files = list_directory_contents(file, file_system_client)
        # Check that the file is in the expected format:
        assert files[0]['name'] == file[1:]



def test_silverLocation_is_delta_table():
    """
    Data must also exist in the data lake.  This function will check to 
    ensure there is data.
    """
    # Define the expected file locations:
    expected_file_locations = [
    f'/framework-j1/SILVER/AdventureWorks/customer_AW/',
    f'/framework-j1/SILVER/AdventureWorks/products_AW/',
    f'/framework-j1/SILVER/AdventureWorks/sales_order_AW/'
    ]

    # Iterate through the expected file locations:
    for file in expected_file_locations:
        if 'customer_AW' in file:
            # Query the data lake to see if file exists:
            files = list_directory_contents(file, file_system_client)
            # Check that the file is in the expected format:
            expected_log_path = f"{file[1:]}_delta_log"
            # Check that expected delta log exists:    
            assert any(f['name'] == expected_log_path for f in files)


def test_goldLocation_is_delta_table():
    """
    Data must also exist in the data lake.  This function will check to 
    ensure there is data.
    """
    # Define the expected file locations:
    expected_file_locations = [
    f'/framework-j1/GOLD/AdventureWorks/customer_AW/',
    f'/framework-j1/GOLD/AdventureWorks/products_AW/',
    f'/framework-j1/GOLD/AdventureWorks/sales_order_AW/'
    ]

    # Iterate through the expected file locations:
    for file in expected_file_locations:
        if 'customer_AW' in file:
            # Query the data lake to see if file exists:
            files = list_directory_contents(file, file_system_client)
            # Check that the file is in the expected format:
            expected_log_path = f"{file[1:]}_delta_log"
            # Check that expected delta log exists:    
            assert any(f['name'] == expected_log_path for f in files)
           







    