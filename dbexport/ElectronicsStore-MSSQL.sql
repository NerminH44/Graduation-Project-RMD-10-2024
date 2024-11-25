USE ElectronicsStore;

-- Create Tables
CREATE TABLE Products (
  SKU                BIGINT IDENTITY(1,1) PRIMARY KEY,
  manufacturer_id    BIGINT,
  product_name       VARCHAR(255),
  Description        VARCHAR(255),
  Stock_quantity     INT, 
  unit_price         DECIMAL(12, 2),
  inventory_id       BIGINT,
  order_id           BIGINT,
  category_id        BIGINT
);

CREATE TABLE Categories (
  category_id   BIGINT IDENTITY(1,1) PRIMARY KEY,
  category_name VARCHAR(20),
  Brand         VARCHAR(20)
);

CREATE TABLE Inventory (
  inventory_id       BIGINT IDENTITY(1,1) PRIMARY KEY,
  Available_quantity INT,   
  Min_stock_level    INT,    
  Max_stock_level    INT,    
  Reorder_point      VARCHAR(20),
  location_id        BIGINT,
  manager_id         BIGINT
);

CREATE TABLE Manufacturer (
  manufacturer_id   BIGINT IDENTITY(1,1) PRIMARY KEY,
  manufacturer_name VARCHAR(100),
  phone_number      VARCHAR(20),
  email             VARCHAR(20)
);

CREATE TABLE Warehouse (
  warehouse_id BIGINT IDENTITY(1,1) PRIMARY KEY,
  location_id  BIGINT,
  capacity     INT,
  manager_id   BIGINT
);

CREATE TABLE Orders (
  order_id       BIGINT IDENTITY(1,1) PRIMARY KEY,
  order_date     DATE,
  SKU            BIGINT,
  quantity       INT, 
  shipment_id    BIGINT,
  retailer_id    BIGINT,
  employee_id    BIGINT NULL,
  payment_id     BIGINT,
  order_status   VARCHAR(20) DEFAULT 'Pending'
);

CREATE TABLE Payments (
  payment_id     BIGINT IDENTITY(1,1) PRIMARY KEY,
  order_id       BIGINT,
  payment_method VARCHAR(50), 
  payment_date   DATE,
  payment_amount DECIMAL(12, 2)
);

CREATE TABLE Shipments (
  shipment_id       BIGINT IDENTITY(1,1) PRIMARY KEY,
  order_id          BIGINT,
  shipment_address  VARCHAR(255), 
  shipment_date     DATE,
  arrival_date      DATE,
  shipment_status   VARCHAR(20) DEFAULT 'Pending',
  employee_id       BIGINT,
  retailer_id       BIGINT
);

CREATE TABLE Retailers (
  retailer_id  BIGINT IDENTITY(1,1) PRIMARY KEY,
  first_name   VARCHAR(50),
  last_name    VARCHAR(50),
  phone_number VARCHAR(20),
  email        VARCHAR(100),
  location_id  BIGINT
);

CREATE TABLE Locations (
  location_id   BIGINT IDENTITY(1,1) PRIMARY KEY,
  location_name VARCHAR(50),
  city          VARCHAR(50),
  postal_code   VARCHAR(20)
);

CREATE TABLE Employees (
  employee_id   BIGINT IDENTITY(1,1) PRIMARY KEY,
  first_name    VARCHAR(50),
  last_name     VARCHAR(50),
  phone_number  VARCHAR(20),
  email         VARCHAR(100),
  job_id        BIGINT,
  salary        DECIMAL(12, 2),
  hire_date     DATE,
  department_id BIGINT
);

CREATE TABLE Managers (
  manager_id   BIGINT IDENTITY(1,1) PRIMARY KEY,
  manager_name VARCHAR(50),
  job_id       BIGINT
);

CREATE TABLE Departments (
  department_id   BIGINT IDENTITY(1,1) PRIMARY KEY,
  department_name VARCHAR(50),
  location_id     BIGINT,
  manager_id      BIGINT
);

CREATE TABLE Jobs (
  job_id        BIGINT IDENTITY(1,1) PRIMARY KEY,
  job_name      VARCHAR(50),
  department_id BIGINT
);

-- Add Constraints
ALTER TABLE Products ADD CONSTRAINT fk_manufacturer_products FOREIGN KEY (manufacturer_id) REFERENCES Manufacturer(manufacturer_id);
ALTER TABLE Products ADD CONSTRAINT fk_inventory_products FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id);
ALTER TABLE Products ADD CONSTRAINT fk_order_products FOREIGN KEY (order_id) REFERENCES Orders(order_id);
ALTER TABLE Products ADD CONSTRAINT fk_category_products FOREIGN KEY (category_id) REFERENCES Categories(category_id);

ALTER TABLE Inventory ADD CONSTRAINT fk_location_inventory FOREIGN KEY (location_id) REFERENCES Locations(location_id);
ALTER TABLE Inventory ADD CONSTRAINT fk_manager_inventory FOREIGN KEY (manager_id) REFERENCES Managers(manager_id);

ALTER TABLE Warehouse ADD CONSTRAINT fk_location_warehouse FOREIGN KEY (location_id) REFERENCES Locations(location_id);
ALTER TABLE Warehouse ADD CONSTRAINT fk_manager_warehouse FOREIGN KEY (manager_id) REFERENCES Managers(manager_id);

ALTER TABLE Orders ADD CONSTRAINT fk_sku_orders FOREIGN KEY (SKU) REFERENCES Products(SKU);
ALTER TABLE Orders ADD CONSTRAINT fk_shipment_orders FOREIGN KEY (shipment_id) REFERENCES Shipments(shipment_id);
ALTER TABLE Orders ADD CONSTRAINT fk_retailer_orders FOREIGN KEY (retailer_id) REFERENCES Retailers(retailer_id);
ALTER TABLE Orders ADD CONSTRAINT fk_payment_orders FOREIGN KEY (payment_id) REFERENCES Payments(payment_id);
ALTER TABLE Orders ADD CONSTRAINT fk_employee_orders FOREIGN KEY (employee_id) REFERENCES Employees(employee_id);

ALTER TABLE Payments ADD CONSTRAINT fk_order_payments FOREIGN KEY (order_id) REFERENCES Orders(order_id);

ALTER TABLE Shipments ADD CONSTRAINT fk_order_shipments FOREIGN KEY (order_id) REFERENCES Orders(order_id);
ALTER TABLE Shipments ADD CONSTRAINT fk_employee_shipments FOREIGN KEY (employee_id) REFERENCES Employees(employee_id);
ALTER TABLE Shipments ADD CONSTRAINT fk_retailer_shipments FOREIGN KEY (retailer_id) REFERENCES Retailers(retailer_id);

ALTER TABLE Retailers ADD CONSTRAINT fk_location_retailers FOREIGN KEY (location_id) REFERENCES Locations(location_id);

ALTER TABLE Employees ADD CONSTRAINT fk_job_employees FOREIGN KEY (job_id) REFERENCES Jobs(job_id);
ALTER TABLE Employees ADD CONSTRAINT fk_department_employees FOREIGN KEY (department_id) REFERENCES Departments(department_id);

ALTER TABLE Managers ADD CONSTRAINT fk_job_managers FOREIGN KEY (job_id) REFERENCES Jobs(job_id);

ALTER TABLE Departments ADD CONSTRAINT fk_location_departments FOREIGN KEY (location_id) REFERENCES Locations(location_id);
ALTER TABLE Departments ADD CONSTRAINT fk_manager_departments FOREIGN KEY (manager_id) REFERENCES Managers(manager_id);

ALTER TABLE Jobs ADD CONSTRAINT fk_department_jobs FOREIGN KEY (department_id) REFERENCES Departments(department_id);

-- Create Users and Grant Privileges in SQL Server
-- Note: Users need to be mapped to a database and a SQL Server login.
USE ElectronicsStore;

-- Create Login and User for DBA
CREATE LOGIN dba_user WITH PASSWORD = 'dba_password';
CREATE USER dba_user FOR LOGIN dba_user;
ALTER ROLE db_owner ADD MEMBER dba_user;

-- Create Login and User for Warehouse Manager
CREATE LOGIN warehouse_manager WITH PASSWORD = 'warehouse_password';
CREATE USER warehouse_manager FOR LOGIN warehouse_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON Warehouse TO warehouse_manager;

-- Create Login and User for Sales Manager
CREATE LOGIN sales_manager WITH PASSWORD = 'sales_password';
CREATE USER sales_manager FOR LOGIN sales_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON Orders TO sales_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON Payments TO sales_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON Retailers TO sales_manager;

-- Create Login and User for Executive User
CREATE LOGIN executive_user WITH PASSWORD = 'executive_password';
CREATE USER executive_user FOR LOGIN executive_user;
GRANT SELECT ON Managers TO executive_user;
GRANT SELECT ON Departments TO executive_user;
GRANT SELECT ON Jobs TO executive_user;

-- Create Login and User for Order Processor
CREATE LOGIN order_processor WITH PASSWORD = 'order_password';
CREATE USER order_processor FOR LOGIN order_processor;
GRANT SELECT, UPDATE ON Orders TO order_processor;
GRANT SELECT, UPDATE ON Shipments TO order_processor;

-- Create Login and User for Location Manager
CREATE LOGIN location_manager WITH PASSWORD = 'location_password';
CREATE USER location_manager FOR LOGIN location_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON Locations TO location_manager;

-- Create Login and User for HR Manager
CREATE LOGIN hr_manager WITH PASSWORD = 'hr_password';
CREATE USER hr_manager FOR LOGIN hr_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON Employees TO hr_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON Managers TO hr_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON Departments TO hr_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON Jobs TO hr_manager;

-- Create Login and User for Data Analyst
CREATE LOGIN data_analyst WITH PASSWORD = 'analyst_password';
CREATE USER data_analyst FOR LOGIN data_analyst;
GRANT SELECT ON Products TO data_analyst;
GRANT SELECT ON Categories TO data_analyst;
GRANT SELECT ON Inventory TO data_analyst;
GRANT SELECT ON Manufacturer TO data_analyst;
GRANT SELECT ON Warehouse TO data_analyst;
GRANT SELECT ON Orders TO data_analyst;
GRANT SELECT ON Payments TO data_analyst;
GRANT SELECT ON Shipments TO data_analyst;

CREATE LOGIN Yousef WITH PASSWORD = '123';
CREATE USER Yousef FOR LOGIN Yousef;

GRANT ALTER ANY ROLE TO Yousef;
EXEC sp_addrolemember 'db_owner', 'Yousef';
EXEC sp_addrolemember 'db_datareader', 'Yousef';
EXEC sp_addrolemember 'db_datawriter', 'Yousef';
EXEC sp_addrolemember 'db_ddladmin', 'Yousef';
EXEC sp_addsrvrolemember 'Yousef', 'sysadmin';
SELECT @@servername