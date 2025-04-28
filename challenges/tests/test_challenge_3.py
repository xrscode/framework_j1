from src.files.utility_functions import query_database
from challenges.challenge_3 import *
import pytest

def test_task_1():
    # All rows from dbo.sourceSystem:
    query = """
    SELECT * FROM dbo.sourceSystem
    WHERE sourceSystemName = 'AdventureWorks'
    """
    results = query_database('metadata', query)
    t_1_results = task_1()

    if t_1_results == 'Not completed.':
        pytest.skip('Test skipped as it is not yet complete.')
    else:
        assert results == t_1_results

def test_task_2():
    # All rows from dbo.sourceEntity where entityName == 'customers_AW'
    t_2_results = task_2()
    if t_2_results == 'Not completed.':
        pytest.skip('Test skipped as it is not yet complete.')
    else:
        assert t_2_results[0][2] == 'customer_AW'

def test_task_3():
    # All rows from dbo.sourceEntity where entityName == 'products_AW'
    t_3_results = task_3()
    if t_3_results == 'Not completed.':
        pytest.skip('Test skipped as it is not yet complete.')
    else:
        assert t_3_results[0][2] == 'products_AW'

def test_task_4():
    t_4_results = task_4()
    if t_4_results == 'Not completed.':
        pytest.skip('Test skipped as it is not yet complete.')
    else:
        assert 'declare' in t_4_results['query'].lower()
        assert 'set' in t_4_results['query'].lower()
        assert 'select' in t_4_results['query'].lower()
        assert t_4_results['results'][0][0] == 5