-- Drop table IF EXISTSs if they exist
DROP TABLE IF EXISTS dbo.counterparty;

CREATE TABLE dbo.counterparty (
    counterparty_id INT PRIMARY KEY,
    counterparty_legal_name NVARCHAR(255),
    legal_address_id INT,
    commercial_contact NVARCHAR(255),
    delivery_contact NVARCHAR(255),
    created_at VARCHAR(255),
    last_updated VARCHAR(255) 
);


DROP TABLE IF EXISTS dbo.address;

CREATE TABLE dbo.address (
    address_id INT PRIMARY KEY,
    address_line_1 NVARCHAR(255),
    address_line_2 NVARCHAR(255),
    district NVARCHAR(255),
    city NVARCHAR(255),
    postal_code NVARCHAR(50),
    country NVARCHAR(100),
    phone NVARCHAR(50),
    created_at VARCHAR(255),
    last_updated VARCHAR(255)
);


DROP TABLE IF EXISTS dbo.currency;

CREATE TABLE dbo.currency (
    currency_id INT PRIMARY KEY,
    currency_code NVARCHAR(50),
    created_at VARCHAR(255),
    last_updated VARCHAR(255)
);


DROP TABLE IF EXISTS dbo.department;

CREATE TABLE dbo.department (
    department_id INT PRIMARY KEY,
    department_name NVARCHAR(255),
    location NVARCHAR(255),
    manager NVARCHAR(255),
    created_at VARCHAR(255),
    last_updated VARCHAR(255)
);


DROP TABLE IF EXISTS dbo.design;

CREATE TABLE dbo.design (
    design_id INT PRIMARY KEY,
    created_at VARCHAR(255),
    last_updated VARCHAR(255),
    design_name NVARCHAR(255),
    file_location NVARCHAR(255),
    file_name NVARCHAR(255)
);


DROP TABLE IF EXISTS dbo.payment;

CREATE TABLE dbo.payment (
    payment_id INT PRIMARY KEY,
    created_at VARCHAR(255),
    last_updated VARCHAR(255),
    transaction_id INT,
    counterparty_id INT,
    payment_amount NUMERIC(18, 2),
    currency_id INT,
    payment_type_id INT,
    paid BIT DEFAULT 0,
    payment_date NVARCHAR(50),
    company_ac_number INT,
    counterparty_ac_number INT
);


DROP TABLE IF EXISTS dbo.payment_type;

CREATE TABLE dbo.payment_type (
    payment_type_id INT PRIMARY KEY,
    payment_type_name NVARCHAR(255),
    created_at VARCHAR(255),
    last_updated VARCHAR(255)
);


DROP TABLE IF EXISTS dbo.purchase_order;

CREATE TABLE dbo.purchase_order (
    purchase_order_id INT PRIMARY KEY,
    created_at VARCHAR(255),
    last_updated VARCHAR(255),
    staff_id INT,
    counterparty_id INT,
    item_code NVARCHAR(50),
    item_quantity INT,
    item_unit_price NUMERIC(18, 2),
    currency_id INT,
    agreed_delivery_date NVARCHAR(50),
    agreed_payment_date NVARCHAR(50),
    agreed_delivery_location_id INT
);


DROP TABLE IF EXISTS dbo.sales_order;

CREATE TABLE dbo.sales_order (
    sales_order_id INT PRIMARY KEY,
    created_at VARCHAR(255),
    last_updated VARCHAR(255),
    design_id INT,
    staff_id INT,
    counterparty_id INT,
    units_sold INT,
    unit_price NUMERIC(18, 2),
    currency_id INT,
    agreed_delivery_date NVARCHAR(50),
    agreed_payment_date NVARCHAR(50),
    agreed_delivery_location_id INT
);


DROP TABLE IF EXISTS dbo.staff;

CREATE TABLE dbo.staff (
    staff_id INT PRIMARY KEY,
    first_name NVARCHAR(255),
    last_name NVARCHAR(255),
    department_id INT,
    email_address NVARCHAR(255),
    last_updated VARCHAR(255),
    created_at VARCHAR(255)
);


DROP TABLE IF EXISTS [transaction];

CREATE TABLE [transaction] (
    transaction_id INT PRIMARY KEY,
    transaction_type NVARCHAR(50),
    sales_order_id VARCHAR(255),
    purchase_order_id VARCHAR(255),
    created_at VARCHAR(255),
    last_updated VARCHAR(255)
);





