# import json
# from utility_functions import ddl_totesys

# # Setup the toteSys tables:
# with open('./src/sql/create_totesys.sql', 'r') as file:
#     query = file.read()
#     try:
#         ddl_totesys(query)
#         print('ToteSys tables successfully created.')
#     except Exception as e:
#         print(f'Error: {e}')

# # Load DB JSON
# with open('./src/files/totesysDB.json') as file:
#     data = json.loads(file.read())


# # Iterate through dictionary
# for table in data:
#     # Extract column names:
#     column_names = [x for x in data[table][0]]
#     # Convert to string:
#     column_names_string = ', '.join(column_names)   
    
#     # Iterate through values:
#     for value in data[table]:
#         values = [f"'{str(x)}'" for x in value.values()]
#         # Convert list of values to string:
#         value_string = ', '.join(values)
#         # Prepare query template
#         query = f"INSERT INTO [{table}] ({column_names_string}) VALUES ({value_string})"
#         print(f'Table:{table}.  Value_id: {values[0]}')
#         # Execute:
#         ddl_totesys(query)
            
        

