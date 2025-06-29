-- ========== Master Data Tables ==========

-- Insert a new user record
-- This table stores basic user information like gender and age
INSERT INTO Users (user_id, gender, age) VALUES (101, 'Male', 35);

-- Insert a construction type
-- Reference table for different types of building construction methods
INSERT INTO ConstructionTypes (construction_type_id, type_name) VALUES (1, 'Monolith');

-- Insert a renovation type
-- Reference table for tracking different categories of renovation work
INSERT INTO RenovationTypes (renovation_type_id, type_name) VALUES (1, 'Major Renovation');

-- Insert a utility payment level
-- Defines different tiers of utility payment arrangements
INSERT INTO UtilityPaymentLevels (utility_payment_level_id, level_value, description) 
VALUES (1, 10, 'Standard Utility Payment Level');

-- Insert a balcony type
-- Reference table for different styles of balconies
INSERT INTO BalconyTypes (balcony_type_id, type_name) VALUES (1, 'Open balcony');

-- Insert a furniture status
-- Tracks whether and how furniture is provided
INSERT INTO FurnitureStatuses (furniture_status_id, status_name) VALUES (1, 'Available');

-- Insert currency records
-- Supports multiple currencies for international rentals
INSERT INTO Currencies (currency_id, currency_code, currency_name) VALUES (1, 'USD', 'United States Dollar');
INSERT INTO Currencies (currency_id, currency_code, currency_name) VALUES (2, 'AMD', 'Armenian Dram');

-- Insert address information
-- Stores detailed location data with separate fields for better searching and sorting
INSERT INTO Addresses (address_id, full_address, city, district, street, building_number) 
VALUES (1, 'Aram Street 107, Yerevan', 'Yerevan', 'Kentron', 'Aram Street', '107');

-- ========== Main Transaction Tables ==========

-- Insert apartment details
-- Core table containing all fixed apartment attributes
-- Uses foreign keys to reference master data tables
INSERT INTO Apartments (
    apartment_id, reg_id, user_id, construction_type_id, new_construction, elevator,
    floors_in_the_building, floor_area, number_of_rooms, number_of_bathrooms, ceiling_height,
    floor, furniture_status_id, children_welcome, pets_allowed, utility_payment_level_id,
    address_id, currency_id, duration, datetime
) VALUES (
    1001, 1, 101, 1, TRUE, TRUE, 
    12, 75.5, 3, 1, 2.8,
    7, 1, TRUE, TRUE, 1,
    1, 1, 'monthly', '2025-06-28 10:00:00'
);

-- ========== SCD (Slowly Changing Dimension) Tables ==========

-- Insert price history using SCD Type 2
-- Tracks historical price changes with validity periods
INSERT INTO ApartmentPrices (apartment_id, price, start_date, end_date)
VALUES (1001, 1200.00, '2025-01-01 00:00:00', '9999-12-31 23:59:59');

-- Insert renovation history using SCD Type 2
-- Tracks historical renovation status changes
INSERT INTO ApartmentRenovations (apartment_id, renovation_type_id, start_date, end_date)
VALUES (1001, 1, '2024-01-01 00:00:00', '9999-12-31 23:59:59');

-- ========== Many-to-Many Relationship Tables ==========

-- Insert balcony information
-- Links apartments to their balcony types (many-to-many relationship)
INSERT INTO ApartmentBalconies (apartment_id, balcony_type_id) VALUES (1001, 1);

-- Insert user-apartment relationship
-- Tracks different roles users can have for apartments (owner, agent, etc.)
INSERT INTO UserApartmentRoles (user_id, apartment_id, role) VALUES (101, 1001, 'Owner');

-- ========== Analysis Queries ==========

-- Query 1: Find apartments with elevator priced <= $1000
-- Joins multiple tables to get complete apartment information
-- Includes current prices only (end_date = '9999-12-31 23:59:59')
SELECT
    A.apartment_id,
    A.floor_area,
    A.number_of_rooms,
    AP.price,
    C.currency_code,
    AD.full_address
FROM
    Apartments AS A
JOIN
    ApartmentPrices AS AP ON A.apartment_id = AP.apartment_id
JOIN
    Currencies AS C ON A.currency_id = C.currency_id
JOIN
    Addresses AS AD ON A.address_id = AD.address_id
WHERE
    A.elevator = TRUE
    AND AP.price <= 1000
    AND C.currency_code = 'USD'
    AND AP.end_date = '9999-12-31 23:59:59';

-- Query 2: Calculate average price by currency
-- Groups prices by currency and calculates average
-- Only considers current prices (not historical)
SELECT
    C.currency_code,
    AVG(AP.price) AS average_price
FROM
    Apartments AS A
JOIN
    ApartmentPrices AS AP ON A.apartment_id = AP.apartment_id
JOIN
    Currencies AS C ON A.currency_id = C.currency_id
WHERE
    AP.end_date = '9999-12-31 23:59:59'
GROUP BY
    C.currency_code;