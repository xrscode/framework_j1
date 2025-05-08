from src.files.utility_functions import query_database, delete_file, write_to_csv
import inquirer
from challenges.recovery_data.adventureWorks_csv_working_data import working_list
import subprocess
import os

"""
RUN SCRIPT TO START CHALLENGE
"""

welcome_message = """

Welcome to the first challenge - contract generation!

DO NOT CHANGE ANYTHING IN THIS SCRIPT.

To begin this challenge run this script and select Challenge_State_1 from the
options.

This script will perform the following actions:
1. The Entity Contracts for AdventureWorks will be deleted/modified.
2. Removal of AdventureWorks from the metadata database.

To Reset;
If you get stuck and need to return everything to a working order, run this
script again and select 'Reset'.

If the user selects to reset to 'working' - this file will reset the
csv back to a working order.  Only use this option if you get stuck.

The path to the customer data is:
https://raw.githubusercontent.com/MicrosoftLearning/dp-203-azure-data-engineer/refs/heads/master/Allfiles/labs/03/data/2020.csv

The path to the products data is:
https://raw.githubusercontent.com/MicrosoftLearning/dp-203-azure-data-engineer/master/Allfiles/labs/01/adventureworks/products.csv

Your challenge is to replace the deleted contracts.

To do this you can either write the contracts by hand.  Or complete the CSV;
'AdventureWorks_entity.csv' enclosed within the AdventureWorks folder.  This
is the recommended way!

Once the csv has been created, you can generate the contract by running this:

-------------------------------------------------------------------------------
python src/build_contract/create_entity_contracts.py
-------------------------------------------------------------------------------

Hint: open the file and make sure that the path setting is correct!  This
file should generate the contracts for you.

To test your contracts run pytest:
-------------------------------------------------------------------------------
pytest -vv ./challenges/tests/test_challenge_1.py
-------------------------------------------------------------------------------
See if you can pass all the tests!

DO NOT CHANGE ANYTHING IN THIS SCRIPT.
"""


print(welcome_message)


# Define query to remove AdventureWorks from metadata database if exists:
query = """
-- Create source system id variable first
DECLARE @ssid INT;

IF EXISTS (SELECT 1 FROM dbo.sourceSystem
    WHERE sourceSystemName = 'AdventureWorks')
BEGIN
    PRINT 'AdventureWorks exists.';

    -- Save source system id variable:
    SELECT @ssid = sourceSystemID
    FROM dbo.sourceSystem
    WHERE sourceSystemName = 'AdventureWorks';

    -- Print source system id:
    PRINT CONCAT('AdventureWorks sourceSystemID is: ', @ssid);

    -- Now delete from entity table
    DELETE FROM dbo.sourceEntity WHERE sourceSystemID = @ssid;
    DELETE FROM dbo.sourceSystem WHERE sourceSystemID = @ssid;
END
ELSE
BEGIN
    PRINT 'AdventureWorks not found.';
END
"""

# First remove contracts and metadata data:
# Call query against metada database:
query_database('metadata', query)

# Define path to Adventure Works folder:
path_to_adventureWorks = 'src\\contracts\\AdventureWorks\\'

# Expected path to csv file:
path = f'{path_to_adventureWorks}AdventureWorks_entity.csv'

# Define header for entities:
header_entity = ['name', 'description', 'connectionString',
                 'sourceQuery', 'sortOrder', 'columnName',
                 'dataType', 'required', 'primary_key']


# Prompt user to start challenge, or Reset:
while True:
    questions = [
        inquirer.List(
            'choice',
            message="Please select",
            choices=['Challenge_State_1', 'Reset', 'Exit'],
        )]

    choice = inquirer.prompt(questions)['choice']

    if choice == 'Exit':
        # Return Nothing if the user chooses to exit:
        break
    elif choice == 'Challenge_State_1':
        # Define ENTITY contracts to delete if they exist:
        contracts_to_delete = {
            'customer_AW': f'{path_to_adventureWorks}customer_AW.json',
            'products_AW': f'{path_to_adventureWorks}products_AW.json',
            'sales_order_AW': f'{path_to_adventureWorks}sales_order_AW.json'
        }

        # Delete the contracts:
        for contract in contracts_to_delete:
            contract_path = contracts_to_delete[contract]
            delete_file(contract_path)

        # Recompile contract(s) and partially remove data:
        # Filter customer and products:
        filtered_csv_data = [x for x in working_list if x[0] not in
                             ['customer_AW', 'products_AW']]
        
        message = """Challenge state has been activated.  Contracts deleted:
        """

        break
    else:
        print('Restoring CSV file to working order...')
        # First create the csv file:
        write_to_csv(path, working_list, header_entity)

        # Use the same Python interpreter that's running this script
        python_executable = r"C:\\Repos\\framework_j1\\venv\\Scripts\\python.exe"

        # Get the absolute path to the target script
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                    '../src/build_contract/create_entity_contracts.py'))

        # Run the subprocess with the correct Python interpreter
        subprocess.run([python_executable, script_path])

        break
