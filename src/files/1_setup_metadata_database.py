from utility_functions import query_database

"""
This python file will setup the metadata datasbse.
First it will read the setup_source_system_tables.sql file and
create the sourceSystem table.
Next it will read the setup_source_entity_tables.sql file and
create the sourceEntity table.
"""
print('Please make sure keyvault name is in the .env file!')

# Setup the sourceSystem table:
with open('./src/sql/setup_source_system_tables.sql', 'r') as file:
    query = file.read()
    try:
        query_database('metadata', query)
        print('sourceSystem table successfully created.')
    except Exception as e:
        print(f'Error: {e}')

# Setup the sourceEntity table:
with open('./src/sql/setup_source_entity_tables.sql', 'r') as file:
    query = file.read()
    try:
        query_database('metadata', query)
        print('sourceEntity table successfully created.')
    except Exception as e:
        print(f'Error: {e}')
