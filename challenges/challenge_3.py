from src.files.utility_functions import query_database

"""
-------------------------------------------------------------------------------
QUERY METADATA DATABASE
-------------------------------------------------------------------------------

By now, you should have successfully generated contracts and uploaded them
into the metadata database. 

Your next challenge is to write a query that queries the metadata database.

Carefully follow the instructions in this script to complete the task.

Hint: connect to SSMS to practice writing queries.  You can then copy and paste
them into this file!  Update the query variable so that between the qutoation
marks is your query.


To run the tests, simply run the following command:
-------------------------------------------------------------------------------
pytest -vv ./challenges/tests/test_challenge_3.py
-------------------------------------------------------------------------------

You do not need to run this script.  The tests will check the functions for 
you.  You just need to ensure that your SQL queries are correct.

"""



# Task 1:
"""
Your first task is to write a simple query to extract AdventureWorks from the
dbo.sourceSystem table.
"""
def task_1():
    query = """




    """
    # Remove whitespace:
    cleaned_query = query.strip()
    
    # Query metadata database:
    results = query_database('metadata', cleaned_query)
    
    # Check query has been attempted:
    if not cleaned_query:
        return 'Not completed.'
    else:
        return results


# Task 2:
"""
Access all rows from dbo.sourceEntity where the entityName is equal to 
customer_AW.
"""
def task_2():
    query = """
    



    """
    # Remove whitespace:
    cleaned_query = query.strip()
    
    # Query metadata database:
    results = query_database('metadata', cleaned_query)
    
    # Check query has been attempted:
    if not cleaned_query:
        return 'Not completed.'
    else:
        return results
    

# Task 3:
"""
Access all rows from dbo.sourceEntity table where the entityName is equal to
products_AW.
"""
def task_3():
    query = """
    



    """
    # Remove whitespace:
    cleaned_query = query.strip()
    
    # Query metadata database:
    results = query_database('metadata', cleaned_query)
    
    # Check query has been attempted:
    if not cleaned_query:
        return 'Not completed.'
    else:
        return results


# Task 4:
"""
1. Declare a variable as an INT.
2. Set the variable to a value of 5.
3. Select the variable.
"""
def task_4():
    query = """
  



    """
    # Remove whitespace:
    cleaned_query = query.strip()

    results = query_database('metadata', cleaned_query)
    
    # Check query has been attempted:
    if not cleaned_query:
        return 'Not completed.'
    else:
        return {'query': query, 'results': results}
    



# Task 5:
"""
Use an UPDATE statement to change a value in the metadata database.
Update the sourceSystemDescription for AdventureWorks.  Change it to 
anything of your choosing!
"""
def task_5():
    query = """
    



    """
    # Remove whitespace:
    cleaned_query = query.strip()

    results = query_database('metadata', cleaned_query)
    
    # Check query has been attempted:
    if not cleaned_query:
        return 'Not completed.'
    else:
        return {'query': query, 'results': results}