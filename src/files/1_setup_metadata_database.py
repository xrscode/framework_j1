from utility_functions import *


"""
This python file will setup the metadata datasbse.
First it will read the setup_source_system_tables.sql file and
create the sourceSystem table.
Next it will read the setup_source_entity_tables.sql file and
create the sourceEntity table.
"""

# Define path to source system sql query:
source_system_sql_path = './src/sql/setup_source_system_tables.sql'
# Save source system sql query:
source_system_sql_query = read_sql(source_system_sql_path)
# Call source system sql query:
results = query_database('metadata', source_system_sql_query)
# Print results:
print(results)

# Define path to source entity sql query:
source_entity_sql_path = './src/sql/setup_source_entity_tables.sql'
# Save source entity sql query:
source_entity_sql_query = read_sql(source_entity_sql_path)
# Query database:
results = query_database('metadata', source_entity_sql_query)
# Print results:
print(results)
