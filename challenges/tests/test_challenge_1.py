import os
from jsonschema import validate
from src.files.utility_functions import load_json

# From the root folder set the path to AdventureWorks
adventure_works_folder_path = 'src\\contracts\\AdventureWorks\\'


# Test that the csv exists:
def test_csv_exists():
    """
    The csv file to help build the contract should exist
    """
    path_to_csv = f'{adventure_works_folder_path}\\AdventureWorks_entity.csv'
    assert os.path.isfile(path_to_csv)


# Test that customer_AW exists:
def test_customer_AW_exists():
    """
    Check that the customer_AW.json file exists 
    """
    path_to_customer = f'{adventure_works_folder_path}\\customer_AW.json'
    assert os.path.isfile(path_to_customer)


def test_customer_AW_conforms_to_expected_schema():
    """
    The customer_AW contract should conform to the expected schema found in:
    .src/files/json_schema/_entitySchema.json
    """
    # Define path to schema:
    path_to_schema = 'src\\json_schema\\_entitySchema.json'
    # Load schema:
    schema = load_json(path_to_schema)

    # Define path to contract json:
    path_to_entity_json = f'{adventure_works_folder_path}\\customer_Aw.json'
    # Load contract:
    contract = load_json(path_to_entity_json)

    # Now validate the contract:
    assert validate(contract, schema) == None


# Test that customer_AW exists:
def test_products_AW_exists():
    """
    Check that the products_AW.json file exists 
    """
    path_to_products = f'{adventure_works_folder_path}\\products_AW.json'
    assert os.path.isfile(path_to_products)


def test_products_AW_conforms_to_expected_schema():
    """
    The products_AW contract should conform to the expected schema found in:
    .src/files/json_schema/_entitySchema.json
    """
    # Define path to schema:
    path_to_schema = 'src\\json_schema\\_entitySchema.json'
    # Load schema:
    schema = load_json(path_to_schema)

    # Define path to contract json:
    path_to_entity_json = f'{adventure_works_folder_path}\\products_Aw.json'
    # Load contract:
    contract = load_json(path_to_entity_json)

    # Now validate the contract:
    assert validate(contract, schema) == None


# Test that customer_AW exists:
def test_sales_order_AW_exists():
    """
    Check that the sales_order_AW.json file exists 
    """
    path_to_products = f'{adventure_works_folder_path}\\sales_order_AW.json'
    assert os.path.isfile(path_to_products)


def test_sales_order_AW_conforms_to_expected_schema():
    """
    The sales_order_AW contract should conform to the expected schema found in:
    .src/files/json_schema/_entitySchema.json
    """
    # Define path to schema:
    path_to_schema = 'src\\json_schema\\_entitySchema.json'
    # Load schema:
    schema = load_json(path_to_schema)

    # Define path to contract json:
    path_to_entity_json = f'{adventure_works_folder_path}\\sales_order_AW.json'
    # Load contract:
    contract = load_json(path_to_entity_json)

    # Now validate the contract:
    assert validate(contract, schema) == None

