from src.files.utility_functions import query_database

"""
-------------------------------------------------------------------------------
PIPELINE RUN FOR ADVENTUREWORKS
-------------------------------------------------------------------------------

Your next task is a simple one.  Simply go to the Azure Portal and run
either 1_Databricks_Ingest or 2_ADF_Ingest.   If it asks you for a parameter

To start a pipeline click on 'Debug' and then enter: AdventureWorks

Make sure to check that the 
pipeline has run successfully all the way through!


When you have done this, run the following test.  In the terminal run:
---------------------------------------------------------------------------
pytest -vv ./challenges/tests/test_challenge_4.py
---------------------------------------------------------------------------

These series of tests will ensure that the metadata database has been updated
correctly.  They will also ensure that the correct data has been written to 
the data lake.
"""