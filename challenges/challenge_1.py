from src.files.utility_functions import query_database, delete_file
import csv
import inquirer
from working_list import working_list

welcome_message = """

Welcome to the first challenge - contract generation!

You can choose if you want to restore the CSV file to a working order, if you
get stuck!

By running this script, the csv files for Adventure Works will be set to a
'challenge' state - where students will have to work to complete the contracts.

The contracts from AdventureWorks will ALWAYS be deleted.  

To recover; 
Select 'Recover' and follow the onscreen prompts.

If the user selects to reset to 'working' - this file will reset the
csv back to a working order.  Only use this option if you get stuck.

The path to the customer data is:
https://raw.githubusercontent.com/MicrosoftLearning/dp-203-azure-data-engineer/refs/heads/master/Allfiles/labs/03/data/2020.csv

The path to the products data is:
https://raw.githubusercontent.com/MicrosoftLearning/dp-203-azure-data-engineer/master/Allfiles/labs/01/adventureworks/products.csv

Note: This script will ALWAYS remove AdventureWorks from the metadata database!
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

# Call query:
try:
    query_database('metadata', query)
    print('!! AdventureWorks removed from metadata database!!\n')
except Exception as e:
    print(e)

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


# Filter customer and products:
filtered_csv_data = [x for x in working_list if x[0] not in
                     ['customer_AW', 'products_AW']]

# Define header:
header = ['name', 'description', 'connectionString', 'sourceQuery'
          'sortOrder', 'columnName', 'dataType', 'required', 'primary_key']


def write_csv_challenge_1(path, data):
    # Now write to CSV:
    with open(path, mode='w', newline='') as file:
        # Define csv writer:
        writer = csv.writer(file)
        # Define headers:
        writer.writerow(header)
        # Define rows:
        writer.writerows(data)


# Prompt user:
while True:
    questions = [
        inquirer.List(
            'choice',
            message="Please select",
            choices=['Challenge', 'Recover', 'Exit'],
        )]

    choice = inquirer.prompt(questions)['choice']

    if choice == 'Exit':
        # Return Nothing if the user chooses to exit:
        break
    elif choice == 'Challenge':
        write_csv_challenge_1(path, filtered_csv_data)
        break
    else:
        print('Restoring CSV file to working order...')
        write_csv_challenge_1(path, working_list)
        print('Run this command in terminal to build contracts:\n')
        print(f'python src/build_contract/create_entity_contracts.py', '\n')
        break
        

