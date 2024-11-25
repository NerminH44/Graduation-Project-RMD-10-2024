# SQL Server table creation queries based on the star schema design
sql_queries = [
    """
    CREATE TABLE Fact_Orders (
        order_id INT PRIMARY KEY,
        amount FLOAT,
        date_key VARCHAR(8),
        order_date DATE,
        SKU INT,
        quantity INT,
        shipment_id INT,
        retailer_id INT,
        employee_id INT,
        payment_id INT,
        order_status VARCHAR(MAX)
    );
    """,
    """
    CREATE TABLE dim_products_manufacturers (
        SKU INT PRIMARY KEY,
        product_name VARCHAR(MAX),
        description VARCHAR(MAX),
        stock_quantity INT,
        unit_price DECIMAL(18, 2),
        manufacturer_id INT,
        manufacturer_name VARCHAR(MAX),
        phone_number VARCHAR(MAX),
        email VARCHAR(MAX),
        category_id INT
    );
    """,
    """
    CREATE TABLE dim_categories (
        category_id INT PRIMARY KEY,
        category_name VARCHAR(MAX),
        Brand VARCHAR(MAX)
    );
    """,
    """
    CREATE TABLE dim_department_jobs_managers (
        department_id INT PRIMARY KEY,
        department_name VARCHAR(MAX),
        location_id INT,
        manager_id INT,
        manager_name VARCHAR(MAX),
        job_id INT,
        job_name VARCHAR(MAX)
    );
    """,
    """
    CREATE TABLE dim_employees (
        employee_id INT PRIMARY KEY,
        first_name VARCHAR(MAX),
        last_name VARCHAR(MAX),
        phone_number VARCHAR(MAX),
        email VARCHAR(MAX),
        salary DECIMAL(18, 2),
        hire_date DATE,
        department_id INT FOREIGN KEY REFERENCES dim_department_jobs_managers(department_id)
    );
    """,
    """
    CREATE TABLE dim_retailers_locations (
        retailer_id INT PRIMARY KEY,
        location_id INT,
        retailer_name VARCHAR(MAX),
        location_address VARCHAR(MAX)
    );
    """,
    """
    CREATE TABLE dim_shipments (
        shipment_id INT PRIMARY KEY,
        order_id INT,
        shipment_address VARCHAR(MAX),
        shipment_date DATE,
        arrival_date DATE,
        shipment_status VARCHAR(MAX),
        employee_id INT,
        retailer_id INT
    );
    """,
    """
    CREATE TABLE dim_inventory_warehouse (
        inventory_id INT PRIMARY KEY,
        available_quantity INT,
        min_stock_level INT,
        max_stock_level INT,
        reorder_point INT,
        location_id INT,
        warehouse_id INT,
        warehouse_capacity INT,
        manager_id INT
    );
    """,
    """
    CREATE TABLE dim_date (
        date_id INT PRIMARY KEY,
        date DATE NOT NULL,
        date_key VARCHAR(8) NOT NULL UNIQUE,
        day INT,
        month INT,
        month_name VARCHAR(MAX),
        quarter INT,
        year INT,
        day_of_week INT,
        day_of_week_name VARCHAR(MAX),
        week_of_year INT,
        is_weekend BIT,
        fiscal_year INT,
        fiscal_quarter INT
    );
    """
]


# Schema
# ---

# Entities:1.Products-SKU(pk)-manufacturer_id(fk)-product_name-description-stock_quantity-unit_price-inventory_id(fk)-order_id(fk)-category_id(fk)2.Categories-category_id(pk)-category_name-brand3.Inventory-inventory_id(pk)-quantity_available-minimum_stock_level-maximum_stock_level-reorder_point-location_id(fk)-manager_id(fk)4.Warehouse-warehouse_id(pk)-location_id(fk)-capacity-manager_id(fk)5.Manufacturers-manufacturer_id(pk)-manufacturer_name-phone_number
# -email6.Orders-order_id(pk)-order_date-SKU(fk)-quantity-shipment_id(fk)-retailer_id(fk)-employee_id(Note:Nonebydefault)-payment_id(fk)-order_status(Note:Pending,Approved,Success,Declined)(Pendingbydefault)7.Payments-payment_id(pk)-order_id(fk)-payment_method-Payment_date-Payment_amount8.Shipments-shipment_id(pk)-order_id(fk)-shipment_address-shipment_date-arrival_date-shipment_status(Note:Pending,Approved,Shipped,Delivered)-employee_id(fk)-retailer_id(fk)9.Retailers-retailer_id(pk)-first_name-last_name-phone_number-email-location_id(fk)
# 10.Locations-location_id(pk)-location_name-city-postal_code11.Employees-employee_id(pk)-first_name-last_name-phone_number-email-job_id(fk)-salary-hire_date-department_id(fk)12.Managers-manager_id(pk)-manager_name-job_id(fk)13.Departments-department_id(pk)-department_name-location_id(fk)-manager_id(fk)14.Jobs-job_id(pk)-job_name-department_id(fk)
# Relationships:●Products.category_id(fk)->Categories.category_id(pk)●Products.manufacturer_id(fk)->Manufacturers.manufacturer_id(pk)●Inventory.inventory_id(pk)->Products.SKU(fk),Warehouse.warehouse_id(fk)●Warehouse.location_id(fk)->Locations.location_id(pk)●Orders.SKU(fk)->Products.SKU(pk)●Orders.shipment_id(fk)->Shipments.shipment_id(pk)●Orders.retailer_id(fk)->Retailers.retailer_id(pk)●Payments.order_id(fk)->Orders.order_id(pk)●Shipments.order_id(fk)->Orders.order_id(pk)●Shipments.employee_id(fk)->Employees.employee_id(pk)●Retailers.location_id(fk)->Locations.location_id(pk)●Employees.job_id(fk)->Jobs.job_id(pk)●Departments.location_id(fk)->Locations.location_id(pk)●Departments.manager_id(fk)->Employees.employee_id(pk)●Jobs.department_id(fk)->Departments.department_id(pk)
# microsoft sql server
import pymssql

# Create a connection to the SQL Server database
connection = pymssql.connect(
                    host='localhost',
                    user='Yousef',
                    password='123',
                    database='ElectronicsDW',
                    as_dict=True
                ) 

# Create a cursor object using the connection
cursor = connection.cursor()

import pandas as pd

# Read the olap\ElectronicsStore-DatabaseExport.xls file into a DataFrame by sheets
import pandas as pd
Categories=pd.read_excel('olap\ElectronicsStore-DatabaseExport.xls',sheet_name='Categories')
Departments=pd.read_excel('olap\ElectronicsStore-DatabaseExport.xls',sheet_name='Departments')
Employees=pd.read_excel('olap\ElectronicsStore-DatabaseExport.xls',sheet_name='Employees')
Inventory=pd.read_excel('olap\ElectronicsStore-DatabaseExport.xls',sheet_name='Inventory')
Jobs=pd.read_excel('olap\ElectronicsStore-DatabaseExport.xls',sheet_name='Jobs')
Locations=pd.read_excel('olap\ElectronicsStore-DatabaseExport.xls',sheet_name='Locations')
Managers=pd.read_excel('olap\ElectronicsStore-DatabaseExport.xls',sheet_name='Managers')
Manufacturer=pd.read_excel('olap\ElectronicsStore-DatabaseExport.xls',sheet_name='Manufacturer')
Orders=pd.read_excel('olap\ElectronicsStore-DatabaseExport.xls',sheet_name='Orders')
Payments=pd.read_excel('olap\ElectronicsStore-DatabaseExport.xls',sheet_name='Payments')
Products=pd.read_excel('olap\ElectronicsStore-DatabaseExport.xls',sheet_name='Products')
Retailers=pd.read_excel('olap\ElectronicsStore-DatabaseExport.xls',sheet_name='Retailers')                                  
Shipments=pd.read_excel('olap\ElectronicsStore-DatabaseExport.xls',sheet_name='Shipments')  
Warehouse=pd.read_excel('olap\ElectronicsStore-DatabaseExport.xls',sheet_name='Warehouse')

# Merge Inventory with Warehouse to get warehouse capacity, manager_id, and quantity available
Inventory = Inventory.merge(Warehouse[['warehouse_id', 'capacity', 'manager_id']], on='location_id', how='left')

# Merge Departments and Managers to get manager name
Departments = Departments.merge(Managers[['manager_id', 'manager_name']], on='manager_id', how='left')

# Merge Departments with Employees to get job_id
Departments = Departments.merge(Employees[['employee_id', 'job_id']], left_on='manager_id', right_on='employee_id', how='left')

# Merge Departments with Jobs to get job name
Departments = Departments.merge(Jobs[['job_id', 'job_name']], on='job_id', how='left')

# Insert data into dim_categories
for index, row in Categories.iterrows():
    cursor.execute("""
        INSERT INTO dim_categories (category_id, category_name, Brand)
        VALUES (%s, %s, %s)
    """, (row['category_id'], row['category_name'], row['Brand']))

# Insert data into dim_department_jobs_managers
for index, row in Departments.iterrows():
    cursor.execute("""
        INSERT INTO dim_department_jobs_managers (department_id, department_name, location_id, manager_id, manager_name, job_id, job_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (row['department_id'], row['department_name'], row['location_id'], row['manager_id'], row['manager_name'], row['job_id'], row['job_name']))

# Insert data into dim_employees
for index, row in Employees.iterrows():
    cursor.execute("""
        INSERT INTO dim_employees (employee_id, first_name, last_name, phone_number, email, salary, hire_date, department_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['employee_id'], row['first_name'], row['last_name'], row['phone_number'], row['email'], row['salary'], row['hire_date'], row['department_id']))

# Insert data into dim_inventory_warehouse
for index, row in Inventory.iterrows():
    cursor.execute("""
        INSERT INTO dim_inventory_warehouse (inventory_id, available_quantity, min_stock_level, max_stock_level, reorder_point, location_id, warehouse_id, warehouse_capacity, manager_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['inventory_id'], row['quantity_available'], row['minimum_stock_level'], row['maximum_stock_level'], row['reorder_point'], row['location_id'], row['warehouse_id'], row['capacity'], row['manager_id']))

# Insert data into dim_products_manufacturers
for index, row in Products.iterrows():
    cursor.execute("""
        INSERT INTO dim_products_manufacturers (SKU, product_name, description, stock_quantity, unit_price, manufacturer_id, manufacturer_name, phone_number, email, category_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['SKU'], row['product_name'], row['description'], row['stock_quantity'], row['unit_price'], row['manufacturer_id'], row['manufacturer_name'], row['phone_number'], row['email'], row['category_id']))

# Insert data into dim_retailers_locations
for index, row in Retailers.iterrows():
    cursor.execute("""
        INSERT INTO dim_retailers_locations (retailer_id, location_id, retailer_name, location_address)
        VALUES (%s, %s, %s, %s)
    """, (row['retailer_id'], row['location_id'], row['retailer_name'], row['location_address']))

# Insert data into dim_shipments
for index, row in Shipments.iterrows():
    cursor.execute("""
        INSERT INTO dim_shipments (shipment_id, order_id, shipment_address, shipment_date, arrival_date, shipment_status, employee_id, retailer_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['shipment_id'], row['order_id'], row['shipment_address'], row['shipment_date'], row['arrival_date'], row['shipment_status'], row['employee_id'], row['retailer_id']))

# Insert data into Fact_Orders
for index, row in Orders.iterrows():
    cursor.execute("""
        INSERT INTO Fact_Orders (order_id, amount, date_key, order_date, SKU, quantity, shipment_id, retailer_id, employee_id, payment_id, order_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['order_id'], row['amount'], row['date_key'], row['order_date'], row['SKU'], row['quantity'], row['shipment_id'], row['retailer_id'], row['employee_id'], row['payment_id'], row['order_status']))

# Commit the transaction
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
