import json
from utility_functions import ddl_totesys

"""
This python file will setup the totesys database.
First it will read the setup_totesys_tables.sql file and create
the totesys tables.
Next it will read totesys_data.json and upload the data into the tables.
"""

# Setup the toteSys tables:
with open('./src/sql/setup_totesys_tables.sql', 'r') as file:
    q = file.read()

    # Execute query:
    ddl_totesys(q)


# Load data in json:
with open('./src/files/totesys_data.json') as file:
    data = json.loads(file.read())


# Create bulk insert query:
for table in data:

    print(f'Inserting data into {table} table...')

    # Extract column names:
    column_names = [x for x in data[table][0]]
    # Convert to string:
    column_names_string = ', '.join(column_names)
    # Values for each table:
    table_data = []

    # Iterate through values:
    for value in data[table]:
        values = [f"'{str(x)}'" for x in value.values()]
        # Convert list of values to string:
        value_string = ', '.join(values)
        # Ensure string is in correct format: (value1, value2, value3...valueN)
        val_string = f"({value_string})"
        # Append value to table_data list:
        table_data.append(val_string)

    # SQL can only upload 1000 values at a time, so split data into chunks of
    # 1000:
    if len(table_data) > 1000:
        # Start at position 0.  Continue for length of table.  Step by 1000:
        for i in range(0, len(table_data), 1000):
            # Compose query:
            query = f"""INSERT INTO [{table}] ({column_names_string})
            VALUES {', '.join(table_data[i:i+1000])};"""
            # Execute query:
            ddl_totesys(query)
    else:
        # Compose query:
        query = f"""INSERT INTO [{table}] ({column_names_string})
        VALUES {', '.join(table_data)}"""
        # Execute query:
        ddl_totesys(query)
