USE ElectronicsStore;

SET IDENTITY_INSERT Jobs ON;

-- Step 2: Insert Data into Jobs table
INSERT INTO Jobs (job_id, job_name) 
VALUES 
(1, 'Inventory Manager'),
(2, 'Sales Manager'),
(3, 'Support Manager');

SET IDENTITY_INSERT Jobs OFF;

-- Step 3: Insert Data into Manufacturer table
INSERT INTO Manufacturer (manufacturer_name, phone_number, email)
VALUES 
('Dell Inc.', '123-456-7890', 'contact@dell.com'),
('HP Inc.', '234-567-8901', 'support@hp.com'),
('Apple Inc.', '345-678-9012', 'info@apple.com'),
('Realme', '456-789-0123', 'contact@realme.com'),
('Samsung Electronics', '567-890-1234', 'service@samsung.com');

-- Step 4: Insert Data into Locations table
INSERT INTO Locations (location_name, city, postal_code)
VALUES 
('Main Warehouse', 'New York', '10001'),
('East Warehouse', 'Los Angeles', '90001'),
('South Warehouse', 'Chicago', '60601');

-- Step 5: Insert Data into Managers table
INSERT INTO Managers (manager_name, job_id)
VALUES 
('Yousef Gomaa', 1),  -- Manager for Inventory
('Jane Smith', 2),    -- Manager for Sales
('Ali Hassan', 3);     -- Manager for Support

-- Step 6: Insert Data into Categories table
INSERT INTO Categories (category_name, Brand)
VALUES 
('Laptops', 'Dell'),
('Laptops', 'HP'),
('Laptops', 'Apple'),
('Smartphones', 'Realme'),
('Smartphones', 'Samsung'),
('Smartphones', 'Apple'),
('Tablets', 'Samsung'),
('Tablets', 'Apple');

-- Step 7: Insert Data into Inventory table
INSERT INTO Inventory (Available_quantity, Min_stock_level, Max_stock_level, Reorder_point, location_id, manager_id)
VALUES 
(100, 10, 200, '50 units', (SELECT location_id FROM Locations WHERE location_name = 'Main Warehouse'), (SELECT manager_id FROM Managers WHERE manager_name = 'Yousef Gomaa')),
(200, 20, 400, '100 units', (SELECT location_id FROM Locations WHERE location_name = 'East Warehouse'), (SELECT manager_id FROM Managers WHERE manager_name = 'Jane Smith')),
(150, 15, 300, '75 units', (SELECT location_id FROM Locations WHERE location_name = 'South Warehouse'), (SELECT manager_id FROM Managers WHERE manager_name = 'Ali Hassan'));

-- Step 8: Insert Data into Products table
SET IDENTITY_INSERT Products ON;

INSERT INTO Products (SKU, manufacturer_id, product_name, Description, Stock_quantity, unit_price, inventory_id, category_id)
VALUES 
(1, (SELECT manufacturer_id FROM Manufacturer WHERE manufacturer_name = 'Dell Inc.'), 'Dell Vostro 3500', 'Intel Core i3-1005G1 Processor 15.6in Display Laptop (8GB RAM, 1TB Hard Drive, U-HD Graphics, Windows 10)', 50, 550.00, 
(SELECT inventory_id FROM Inventory WHERE location_id = (SELECT location_id FROM Locations WHERE location_name = 'Main Warehouse') AND manager_id = (SELECT manager_id FROM Managers WHERE manager_name = 'Yousef Gomaa')), 
(SELECT category_id FROM Categories WHERE category_name = 'Laptops' AND Brand = 'Dell')),
(3, (SELECT manufacturer_id FROM Manufacturer WHERE manufacturer_name = 'Dell Inc.'), 'Dell G15-5520 Gaming Laptop', '12th Intel Core i7-12700H 14-Cores, 16GB RAM DDR5 4800 MHz, 512GB SSD, NVIDIA Geforce RTX3050 4GB GDDR6 Graphics, 15.6" FHD 120 Hz, Backlit Keyboard, UBUNTU - Black', 30, 1200.00, 
(SELECT inventory_id FROM Inventory WHERE location_id = (SELECT location_id FROM Locations WHERE location_name = 'Main Warehouse') AND manager_id = (SELECT manager_id FROM Managers WHERE manager_name = 'Yousef Gomaa')), 
(SELECT category_id FROM Categories WHERE category_name = 'Laptops' AND Brand = 'Dell')),
(5, (SELECT manufacturer_id FROM Manufacturer WHERE manufacturer_name = 'HP Inc.'), 'HP - Envy 2-in-1 15.6" Touch-Screen Laptop', 'Intel Core i7 - 16GB Memory - 512GB SSD - Natural Silver', 40, 900.00, 
(SELECT inventory_id FROM Inventory WHERE location_id = (SELECT location_id FROM Locations WHERE location_name = 'Main Warehouse') AND manager_id = (SELECT manager_id FROM Managers WHERE manager_name = 'Yousef Gomaa')), 
(SELECT category_id FROM Categories WHERE category_name = 'Laptops' AND Brand = 'HP')),
(6, (SELECT manufacturer_id FROM Manufacturer WHERE manufacturer_name = 'Apple Inc.'), 'Apple MacBook Pro 14 M1', 'Pro 8C CPU 14C GPU/16GB/512GB/Silver/AR', 20, 2000.00, 
(SELECT inventory_id FROM Inventory WHERE location_id = (SELECT location_id FROM Locations WHERE location_name = 'East Warehouse') AND manager_id = (SELECT manager_id FROM Managers WHERE manager_name = 'Jane Smith')), 
(SELECT category_id FROM Categories WHERE category_name = 'Laptops' AND Brand = 'Apple')),
(7, (SELECT manufacturer_id FROM Manufacturer WHERE manufacturer_name = 'Realme'), 'Realme 11 Pro+ 5G', '12GB RAM, 512GB Storage Oasis Green, Bluetooth, Wi-Fi', 70, 400.00, 
(SELECT inventory_id FROM Inventory WHERE location_id = (SELECT location_id FROM Locations WHERE location_name = 'East Warehouse') AND manager_id = (SELECT manager_id FROM Managers WHERE manager_name = 'Jane Smith')), 
(SELECT category_id FROM Categories WHERE category_name = 'Smartphones' AND Brand = 'Realme')),
(10, (SELECT manufacturer_id FROM Manufacturer WHERE manufacturer_name = 'Samsung Electronics'), 'Samsung Galaxy S23 Ultra 5G', '12GB/256GB Middle East edition', 45, 1000.00, 
(SELECT inventory_id FROM Inventory WHERE location_id = (SELECT location_id FROM Locations WHERE location_name = 'East Warehouse') AND manager_id = (SELECT manager_id FROM Managers WHERE manager_name = 'Jane Smith')), 
(SELECT category_id FROM Categories WHERE category_name = 'Smartphones' AND Brand = 'Samsung')),
(11, (SELECT manufacturer_id FROM Manufacturer WHERE manufacturer_name = 'Apple Inc.'), 'iPhone 15 Pro Max 5G', '8GB/1TB iOS 17.0', 25, 1400.00, 
(SELECT inventory_id FROM Inventory WHERE location_id = (SELECT location_id FROM Locations WHERE location_name = 'South Warehouse') AND manager_id = (SELECT manager_id FROM Managers WHERE manager_name = 'Ali Hassan')), 
(SELECT category_id FROM Categories WHERE category_name = 'Smartphones' AND Brand = 'Apple')),
(13, (SELECT manufacturer_id FROM Manufacturer WHERE manufacturer_name = 'Samsung Electronics'), 'Samsung Galaxy Tab A9 LTE', '8.7" Android Tablet, 8GB RAM, 128GB Storage, Silver', 50, 300.00, 
(SELECT inventory_id FROM Inventory WHERE location_id = (SELECT location_id FROM Locations WHERE location_name = 'South Warehouse') AND manager_id = (SELECT manager_id FROM Managers WHERE manager_name = 'Ali Hassan')), 
(SELECT category_id FROM Categories WHERE category_name = 'Tablets' AND Brand = 'Samsung')),
(15, (SELECT manufacturer_id FROM Manufacturer WHERE manufacturer_name = 'Apple Inc.'), 'Apple iPad Air', '10.9-inch Liquid Retina display, A14 Bionic chip', 35, 600.00, 
(SELECT inventory_id FROM Inventory WHERE location_id = (SELECT location_id FROM Locations WHERE location_name = 'South Warehouse') AND manager_id = (SELECT manager_id FROM Managers WHERE manager_name = 'Ali Hassan')), 
(SELECT category_id FROM Categories WHERE category_name = 'Tablets' AND Brand = 'Apple'));

SET IDENTITY_INSERT Products OFF;

-- Output the inserted records for verification
SELECT * FROM Manufacturer;
SELECT * FROM Locations;
SELECT * FROM Managers;
SELECT * FROM Inventory;
SELECT * FROM Categories;
SELECT * FROM Products;

