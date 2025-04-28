from src.files.utility_functions import query_database
import json

def test_sourceSystem_table_exists_with_data():
    """
    If the database has data it will return; [(1,)].
    Caution: Make sure to select the 1 with; result[0][0] and convert to int.
    If this test fails, there is no data in the metadata database.
    """
    result = query_database('metadata', 'SELECT 1 FROM dbo.sourceSystem')
    assert int(result[0][0]) == 1


def test_sourceEntity_table_exists_with_data():
    """
    If the database has data it will return; [(1,)].
    Caution: Make sure to select the 1 with; result[0][0] and convert to int.
    If this test fails, there is no data in the metadata database.
    """
    result = query_database('metadata', 'SELECT 1 FROM dbo.sourceEntity')
    assert int(result[0][0]) == 1


def test_AdventureWorks_exists_in_sourceSystem():
    query = """
    SELECT * FROM sourceSystem
    WHERE sourceSystemName = 'AdventureWorks'
    """
    results = query_database('metadata', query)
    assert results[0][1] == 'AdventureWorks'

def test_sourceSystem_AdventureWorks_sourceType_is_http():
    query = """
    SELECT * FROM sourceSystem
    WHERE sourceSystemName = 'AdventureWorks'
    """
    results = query_database('metadata', query)
    assert results[0][2] == 'http'

def test_sourceSystem_AdventureWorks_has_entity_columns():
    query = """
    SELECT * FROM sourceSystem
    WHERE sourceSystemName = 'AdventureWorks'
    """
    results = query_database('metadata', query)
    assert len(json.loads(results[0][4])) == 3

def test_sourceSystem_AdventureWorks_has_correct_entity_columns():
    query = """
    SELECT * FROM sourceSystem
    WHERE sourceSystemName = 'AdventureWorks'
    """
    results = query_database('metadata', query)
    entities_in_database = json.loads(results[0][4])
    expected_entities = ['sales_order_AW', 'products_AW', 'customer_AW']
    for entity in entities_in_database:
        assert entity in expected_entities


def test_sourceSystem_Adventureworks_has_correct_notebooks():
    query = """
    SELECT * FROM sourceSystem
    WHERE sourceSystemName = 'AdventureWorks'
    """
    notebooks = {
    'bronze': '/Workspace/Repos/Git/jf1/src/notebooks/AdventureWorks/BRONZE_AdventureWorks',
    'silver': '/Workspace/Repos/Git/jf1/src/notebooks/AdventureWorks/SILVER_AdventureWorks',
    'gold': '/Workspace/Repos/Git/jf1/src/notebooks/AdventureWorks/GOLD_AdventureWorks',
    'analysis': '/Workspace/Repos/Git/jf1/src/notebooks/AdventureWorks/Analysis_AdventureWorks'}
    results = query_database('metadata', query)
    notebooks_in_database = json.loads(results[0][6])
    assert notebooks_in_database == notebooks

def test_sourceEntity_entities_exist():
    query = """
    DECLARE @ssid INT;

    SELECT @ssid = sourceSystemID
    FROM dbo.sourceSystem
    WHERE sourceSystemName = 'AdventureWorks';

    SELECT * FROM dbo.sourceEntity
    WHERE sourceSystemID = @ssid;
    """
    results = query_database('metadata', query)
    assert len(results) > 2

def test_sourceEntity_entities_names_are_correct():
    query = """
    DECLARE @ssid INT;

    SELECT @ssid = sourceSystemID
    FROM dbo.sourceSystem
    WHERE sourceSystemName = 'AdventureWorks';

    SELECT * FROM dbo.sourceEntity
    WHERE sourceSystemID = @ssid;
    """
    results = query_database('metadata', query)
    entity_names_in_database = [x[2] for x in results]
    expected_entities = ['sales_order_AW', 'products_AW', 'customer_AW']
    for entity in entity_names_in_database:
        assert entity in expected_entities

def test_sourceEntity_customer_and_sales_order_have_correct_connection_string():
    query = """
    DECLARE @ssid INT;

    SELECT @ssid = sourceSystemID
    FROM dbo.sourceSystem
    WHERE sourceSystemName = 'AdventureWorks';

    SELECT * FROM dbo.sourceEntity
    WHERE sourceSystemID = @ssid;
    """
    connectionString = 'https://raw.githubusercontent.com/MicrosoftLearning/dp-203-azure-data-engineer/refs/heads/master/Allfiles/labs/03/data/2020.csv'
    results = query_database('metadata', query)
    for row in results:
        if row[2] == 'customer_AW' or row[2] == 'sales_order_AW':
            assert json.loads(row[4])['connectionString'] == connectionString

def test_sourceEntity_product_has_correct_connection_string():
    query = """
    DECLARE @ssid INT;

    SELECT @ssid = sourceSystemID
    FROM dbo.sourceSystem
    WHERE sourceSystemName = 'AdventureWorks';

    SELECT * FROM dbo.sourceEntity
    WHERE sourceSystemID = @ssid;
    """
    connectionString = 'https://raw.githubusercontent.com/MicrosoftLearning/dp-203-azure-data-engineer/master/Allfiles/labs/01/adventureworks/products.csv'
    results = query_database('metadata', query)
    for row in results:
        if row[2] == 'products_AW':
            assert json.loads(row[4])['connectionString'] == connectionString
    
    
def test_sourceEntity_customer_has_entityIngestionColumns():
    query = """
    DECLARE @ssid INT;

    SELECT @ssid = sourceSystemID
    FROM dbo.sourceSystem
    WHERE sourceSystemName = 'AdventureWorks';

    SELECT * FROM dbo.sourceEntity
    WHERE sourceSystemID = @ssid 
    AND entityName = 'customer_AW' or entityName = 'sales_order_AW';
    """
    results = query_database('metadata', query)
    columns =  len(json.loads(results[0][5]))
    for row in results:
        column = row[5]
        print('Here')
        assert len(json.loads(column)) > 8
  
    