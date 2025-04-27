"""
This file contains a single source of truth for the AdventureWorks entity
csv data.  It can be used to re-build the csv.
"""

# Working list to restore if things go wrong:
working_list = [
    [
        'customer_AW',
        'dim_customer',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '1', 'SalesOrderNumber', 'varchar', 'false', 'false'
    ],
    [
        'customer_AW',
        'dim_customer',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '2', 'SalesOrderLineNumber', 'int', 'false', 'false'
    ],
    [
        'customer_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '3', 'OrderDate', 'date', 'false', 'false'
    ],
    [
        'customer_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '4', 'CustomerName', 'varchar', 'true', 'false'
    ],
    [
        'customer_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '5', 'EmailAddress', 'varchar', 'true', 'false'
    ],
    [
        'customer_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '6', 'Item', 'varchar', 'false', 'false'
    ],
    [
        'customer_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '7', 'Quantity', 'int', 'false', 'false'
    ],
    [
        'customer_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '8', 'UnitPrice', 'double', 'false', 'false'
    ],
    [
        'customer_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '9', 'TaxAmount', 'double', 'false', 'false'
    ],
    [
        'products_AW',
        'dim_products',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/master/'
            'Allfiles/labs/01/adventureworks/products.csv'
        ),
        'None', '1', 'ProductID', 'int', 'true', 'true'
    ],
    [
        'products_AW',
        'dim_products',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/master/'
            'Allfiles/labs/01/adventureworks/products.csv'
        ),
        'None', '2', 'ProductName', 'varchar', 'true', 'false'
    ],
    [
        'products_AW',
        'dim_products',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/master/'
            'Allfiles/labs/01/adventureworks/products.csv'
        ),
        'None', '3', 'Category', 'varchar', 'true', 'false'
    ],
    [
        'products_AW',
        'dim_products',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/master/'
            'Allfiles/labs/01/adventureworks/products.csv'
        ),
        'None', '4', 'ListPrice', 'double', 'true', 'false'
    ],
    [
        'sales_order_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '1', 'SalesOrderNumber', 'varchar', 'true', 'false'
    ],
    [
        'sales_order_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '2', 'SalesOrderLineNumber', 'int', 'true', 'false'
    ],
    [
        'sales_order_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '3', 'OrderDate', 'date', 'true', 'false'
    ],
    [
        'sales_order_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '4', 'CustomerName', 'varchar', 'false', 'false'
    ],
    [
        'sales_order_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '5', 'EmailAddress', 'varchar', 'true', 'false'
    ],
    [
        'sales_order_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '6', 'Item', 'varchar', 'true', 'false'
    ],
    [
        'sales_order_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '7', 'Quantity', 'int', 'true', 'false'
    ],
    [
        'sales_order_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '8', 'UnitPrice', 'double', 'true', 'false'
    ],
    [
        'sales_order_AW',
        'sales_order',
        (
            'https://raw.githubusercontent.com/MicrosoftLearning/'
            'dp-203-azure-data-engineer/refs/heads/master/'
            'Allfiles/labs/03/data/2020.csv'
        ),
        'None', '9', 'TaxAmount', 'double', 'true', 'false'
    ],
]