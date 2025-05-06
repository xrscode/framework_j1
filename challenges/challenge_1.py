from src.files.utility_functions import query_database, delete_file, write_to_csv
import inquirer
from challenges.recovery_data.adventureWorks_csv_working_data import working_list

"""
RUN SCRIPT TO START CHALLENGE
"""

welcome_message = """

Welcome to the first challenge - contract generation!

DO NOT CHANGE ANYTHING IN THIS SCRIPT.

In this challenge you need to create three contracts:
1. customer_AW.json
2. products_AW.json
3. sales_order_AW.json

You can choose if you want to restore the CSV file to a working order, if you
get stuck!

By running this script, the csv files for Adventure Works will be set to a
'challenge' state - where students will have to work to complete the contracts.

This script will perform the following actions:
1. The contracts from AdventureWorks will ALWAYS be deleted.  
2. Removal of AdventureWorks from the metada database.

To Reset; 
Select 'Reset' and follow the onscreen prompts.

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

# Define contracts to delete if they exist:
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

# Define header:
header = ['name', 'description', 'connectionString', 'sourceQuery'
          'sortOrder', 'columnName', 'dataType', 'required', 'primary_key']


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
        write_to_csv(path, filtered_csv_data)
        break
    else:
        print('Restoring CSV file to working order...')
        write_to_csv(path, working_list)
        print('Run this command in terminal to build contracts:\n')
        print(f'python src/build_contract/create_entity_contracts.py', '\n')
        break
        

