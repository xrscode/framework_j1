import json
from utility_functions import *
from check_db_connection import check_connection

# Run Check Connection first:
check_connection()



"""
This python file will setup the totesys database.
First it will read the setup_totesys_tables.sql file and create
the totesys tables.
Next it will read totesys_data.json and upload the data into the tables.
"""

# Define path to the sql to setup the totesys database.
totesys_sql_setup_path = './src/sql/setup_totesys_tables.sql'

# Read the sql statement:
totesys_sql_setup = read_sql(totesys_sql_setup_path)

# Query the database:
query_database('totesys', totesys_sql_setup)


# Define path to totesys data:
totesys_data = './src/files/totesys_data.json'

# Read the data and convert to json:
data = json.loads(read_sql(totesys_data))


def bulk_insert_totesys(data: json):
    """
    This function iterates through (totesys_data.json)
    dictionary and bulk inserts data into a sql database.

    Arguments:
        data (json): Data in json format.

    Raises:
        TypeError: if data is not in json format.

    Returns:
        None.
    """

    # Check data is json:

    if not isinstance(data, dict):
        raise TypeError(f'Expecting json, got: {type(data)}')

    # For each table, create a bulk insert query:
    for table in data:

        print(f'Inserting data into {table} table...')

        # Column names to string:
        column_names_string = ', '.join([x for x in data[table][0]])

        # Values for each table:
        table_data = []

        # Iterate through values and append to list:
        for value in data[table]:
            values = [f"'{str(x)}'" for x in value.values()]
            # Convert list of values to string:
            value_to_string = f"({', '.join(values)})"
            # Append value to table_data list:
            table_data.append(value_to_string)

        # Upload in chunks of 1000 at a time:
        # Start at position 0.  Continue for length of table.  Step by 1000:
        for i in range(0, len(table_data), 1000):
            # Compose query:
            query = f"""INSERT INTO [{table}] ({column_names_string})
            VALUES {', '.join(table_data[i:i+1000])};"""
            # Execute query:
            query = query_database('totesys', query)
            print(query)
        
    return None


# Call function:
bulk_insert_totesys(data)

