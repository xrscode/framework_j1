from utility_functions import ddl_metadata, ddl_totesys

# Setup the sourceSystem table:
with open('./src/sql/setupSourceSystem.sql', 'r') as file:
    query = file.read()
    try:
        ddl_metadata(query)
        print('sourceSystem table successfully created.')
    except Exception as e:
        print(f'Error: {e}')

# Setup the sourceEntity table:
with open('./src/sql/setupSourceEntity.sql', 'r') as file:
    query = file.read()
    try:
        ddl_metadata(query)
        print('sourceEntity table successfully created.')
    except Exception as e:
        print(f'Error: {e}')
