welcome_message = """
Now that you have completed the first challenge, hopefully you will have four
contracts to upload: 

_sourceSystem.json
customer_AW.json
products_AW.json
sales_order_AW.json

There are a number of options available to you:
1.  Create your own python file that:
    a. Reads the csv. 
    b. Creates a sql DML (Data Manipulation Language) statement.
    c. Queries the metadata database and INSERTS the data.

2. Use the python scripts already created for you.  In the terminal sequentially
run:
-------------------------------------------------------------------------------
src/files/3_upload_source_system_contract.py
src/files/4_upload_source_entity_contract.py
-------------------------------------------------------------------------------

3. Or, more conveniently, run:
-------------------------------------------------------------------------------
src/contracts/upload.ps1
-------------------------------------------------------------------------------
Check that you have uploaded the contracts by checking the database using 
SSMS.

Remember that all the credentials you need are stored in the .env file after
deployment.

When you are done, run the following test before moving on:
-------------------------------------------------------------------------------
pytest -vv ./challenges/tests/test_challenge_2.py
-------------------------------------------------------------------------------
"""