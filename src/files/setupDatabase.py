from utility_functions import ddl, ddl_totesys

# Setup the sourceSystem table:
with open('./src/sql/setupSourceSystem.sql', 'r') as file:
    query = file.read()
    try:
        ddl(query)
        print('sourceSystem table successfully created.')
    except Exception as e:
        print(f'Error: {e}')

# Setup the sourceEntity table:
with open('./src/sql/setupSourceEntity.sql', 'r') as file:
    query = file.read()
    try:
        ddl(query)
        print('sourceEntity table successfully created.')
    except Exception as e:
        print(f'Error: {e}')

# # Setup the toteSys tables:
# with open('./src/sql/create_totesys.sql', 'r') as file:
#     query = file.read()
#     try:
#         ddl_totesys(query)
#         print('ToteSys tables successfully created.')
#     except Exception as e:
#         print(f'Error: {e}')
